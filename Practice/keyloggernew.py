import threading
import time
import collections
import os
import asyncio
from tkinter import Tk, Text, Label, Button, END, DISABLED, NORMAL, Scrollbar, RIGHT, Y
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------- CONFIGURATION ----------
# Replace with your actual bot token and chat ID.
# This information is used to connect to your Telegram bot and send messages.
TELEGRAM_BOT_TOKEN = "8490061327:AAHXRHKwjndqqYcHVX1D7N7g-X8Fcl2-a4g"
CONTROL_CHAT_ID = 7673624123
LOG_FILE = "local_input_log.txt"
ALLOW_EXPORT = False
# ------------------------------------

# Global variables to manage monitoring state and the bot application instance
monitoring = False
monitoring_lock = threading.Lock()
bot_app = None
# We'll use a global variable to store the bot's event loop,
# so we can access it from the Tkinter thread.
bot_loop = None


def append_log(text: str):
    """Appends a timestamped log entry to the local log file."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {text}\n")


def summarize_log():
    """Reads the log file and provides a summary of characters, lines, and top words."""
    if not os.path.exists(LOG_FILE):
        return {"chars": 0, "lines": 0, "top_words": []}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        # Extract the text content, ignoring the timestamp
        lines = [line.strip().split("] ", 1)[1] if "] " in line else line.strip() for line in f.readlines()]
    alltext = "\n".join(lines)
    words = [w.strip(".,!?;:()[]\"'").lower() for w in alltext.split()]
    words = [w for w in words if w]
    top = collections.Counter(words).most_common(10)
    return {"chars": len(alltext), "lines": len(lines), "top_words": top}


class SafeInputApp:
    """A Tkinter GUI application for logging user input locally."""
    def __init__(self):
        self.root = Tk()
        self.root.title("Safe Local Input Logger (testing area)")
        
        Label(self.root, text="Type here. Only text typed in this box will be logged and sent.").pack()
        self.text = Text(self.root, width=80, height=20, wrap="word")
        self.text.pack()
        
        sb = Scrollbar(self.root)
        sb.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=sb.set)
        sb.config(command=self.text.yview)
        
        self.start_btn = Button(self.root, text="Enable Monitoring", command=self.enable_monitoring)
        self.start_btn.pack(side="left", padx=5, pady=5)
        self.stop_btn = Button(self.root, text="Disable Monitoring", command=self.disable_monitoring, state=DISABLED)
        self.stop_btn.pack(side="left", padx=5, pady=5)
        
        # Bind a function to key releases in the text box
        self.text.bind("<KeyRelease>", self.on_key_release)

    def enable_monitoring(self):
        """Enables the monitoring and logging of keystrokes."""
        global monitoring
        with monitoring_lock:
            monitoring = True
        self.start_btn.config(state=DISABLED)
        self.stop_btn.config(state=NORMAL)
        append_log("=== Monitoring enabled via local GUI ===")

    def disable_monitoring(self):
        """Disables the monitoring and logging of keystrokes."""
        global monitoring
        with monitoring_lock:
            monitoring = False
        self.start_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        append_log("=== Monitoring disabled via local GUI ===")

    def on_key_release(self, event):
        """
        Callback function for a key release event in the text box.
        Logs the input and schedules a Telegram message if monitoring is active.
        """
        global bot_loop
        with monitoring_lock:
            active = monitoring
        if not active or not bot_loop:
            return
        
        # Get the current line of text
        try:
            index = self.text.index("insert linestart")
            line = self.text.get(index, "insert lineend")
        except Exception:
            line = self.text.get("1.0", END).strip()
            
        sanitized = line.replace("\n", " ")
        append_log(sanitized)
        
        # This is the correct way to schedule an async function (coroutine)
        # from a synchronous thread. It safely adds the coroutine to the bot's event loop.
        asyncio.run_coroutine_threadsafe(send_live_message(sanitized), bot_loop)

    def run(self):
        """Starts the Tkinter main loop."""
        self.root.mainloop()

def restricted(func):
    """Decorator to restrict bot commands to a specific chat ID."""
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if chat_id != CONTROL_CHAT_ID:
            await update.message.reply_text("Unauthorized.")
            return
        return await func(update, context)
    return wrapped

# --- Telegram Bot Command Handlers ---

@restricted
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command, enabling monitoring."""
    global monitoring
    with monitoring_lock:
        monitoring = True
    await update.message.reply_text("Monitoring ENABLED. Typing in the local box will send to Telegram.")
    append_log("=== Monitoring enabled via Telegram (/start) ===")

@restricted
async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /stop command, disabling monitoring."""
    global monitoring
    with monitoring_lock:
        monitoring = False
    await update.message.reply_text("Monitoring DISABLED.")
    append_log("=== Monitoring disabled via Telegram (/stop) ===")

@restricted
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /status command, providing a summary of the log file."""
    s = summarize_log()
    top = "\n".join([f"{w}: {c}" for w, c in s["top_words"]]) if s["top_words"] else "No words yet."
    msg = f"Log summary:\nCharacters: {s['chars']}\nLines: {s['lines']}\nTop words:\n{top}"
    await update.message.reply_text(msg)

@restricted
async def getlog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /getlog command, sending the log file to the user."""
    if not ALLOW_EXPORT:
        await update.message.reply_text("Exporting raw logs is disabled in configuration.")
        return
    if not os.path.exists(LOG_FILE):
        await update.message.reply_text("No log file found.")
        return
    await update.message.reply_document(open(LOG_FILE, "rb"))

# --- Asynchronous Message Sending ---

async def send_live_message(text: str):
    """Sends a message to the control chat ID. This is an async coroutine."""
    if text.strip():
        # Ensure bot_app exists before trying to send a message
        if bot_app:
            await bot_app.bot.send_message(chat_id=CONTROL_CHAT_ID, text=f"[LIVE] {text}")

# --- Main Program Logic ---

def run_telegram_bot():
    """This function is run in a separate thread and manages the Telegram bot."""
    global bot_app, bot_loop
    
    # We must set a new event loop for this thread, as one doesn't exist by default
    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    
    bot_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start_command))
    bot_app.add_handler(CommandHandler("stop", stop_command))
    bot_app.add_handler(CommandHandler("status", status_command))
    bot_app.add_handler(CommandHandler("getlog", getlog_command))
    
    print("[*] Telegram bot thread started. Listening for commands...")
    
    # run_polling() is the correct, blocking way to start the bot
    # It runs its own event loop and will block this thread.
    bot_app.run_polling()
    

def main():
    """
    The main entry point of the application. 
    It starts the Telegram bot in a separate thread and runs the Tkinter GUI
    in the main thread.
    """
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w", encoding="utf-8").close()
    
    # Start the bot in a separate thread. This is the correct way
    # to run a blocking async process alongside a Tkinter GUI.
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    # Run the Tkinter GUI in the main thread.
    app = SafeInputApp()
    app.run()

if __name__ == "__main__":
    print("Starting Safe Local Input Logger with live Telegram updates.")
    print("IMPORTANT: Only run this on your own machine.")
    main()
