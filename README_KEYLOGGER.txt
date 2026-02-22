╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🔐 INTELLIGENT KEYLOGGER WITH AI PERSONALITY ANALYSIS            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

📖 SYSTEM OVERVIEW
═══════════════════════════════════════════════════════════════════════════

This advanced keylogger system captures keyboard input, stores it in a 
SQLite database, and uses Google's Gemini AI to analyze typing patterns 
and determine the user's personality type.

┌────────────────────────────────────────────────────────────────────────┐
│ 🎯 KEY FEATURES                                                         │
├────────────────────────────────────────────────────────────────────────┤
│ ✅ Real-time keyboard capture                                           │
│ ✅ Local SQLite database storage                                        │
│ ✅ AI-powered personality analysis using Google Gemini                  │
│ ✅ Periodic automatic analysis (every 10 minutes)                       │
│ ✅ Comprehensive database viewer tool                                   │
│ ✅ Export functionality for all data                                    │
│ ✅ Statistics and search capabilities                                   │
└────────────────────────────────────────────────────────────────────────┘


📋 FILES IN THIS SYSTEM
═══════════════════════════════════════════════════════════════════════════

1. keylogger.py              - Main keylogger with AI analysis
2. view_logs.py              - Database viewer and analyzer tool
3. keylogger_database.db     - SQLite database (auto-created)
4. keylog.txt                - Local text file backup
5. README_KEYLOGGER.txt      - This documentation


🚀 QUICK START GUIDE
═══════════════════════════════════════════════════════════════════════════

STEP 1: Ensure Dependencies are Installed
   The following packages are required:
   • pynput
   • google-generativeai
   
   Already installed ✓

STEP 2: Configure API Key
   Your Google API Key is already configured:
   AIzaSyBc3-hmBU3hzRt-9Ctix2xqt2TzXghYJ1U

STEP 3: Run the Keylogger
   python keylogger.py
   
   • Logs are saved every 60 seconds
   • AI analysis runs every 10 minutes
   • Press ESC to stop

STEP 4: View Results
   python view_logs.py
   
   Interactive menu to:
   • View recent logs
   • See AI personality analyses
   • Search logs
   • Export data


🗄️ DATABASE STRUCTURE
═══════════════════════════════════════════════════════════════════════════

TABLE 1: keylogs
┌──────────────┬──────────────┬─────────────────────────────────────────┐
│ Field        │ Type         │ Description                             │
├──────────────┼──────────────┼─────────────────────────────────────────┤
│ id           │ INTEGER      │ Auto-incrementing primary key           │
│ timestamp    │ TEXT         │ When the log was captured               │
│ log_data     │ TEXT         │ The actual keystrokes captured          │
│ char_count   │ INTEGER      │ Number of characters in this log        │
│ session_date │ TEXT         │ Date of the session                     │
└──────────────┴──────────────┴─────────────────────────────────────────┘

TABLE 2: ai_analysis
┌──────────────────┬──────────┬─────────────────────────────────────────┐
│ Field            │ Type     │ Description                             │
├──────────────────┼──────────┼─────────────────────────────────────────┤
│ id               │ INTEGER  │ Auto-incrementing primary key           │
│ analysis_time    │ TEXT     │ When the analysis was performed         │
│ total_chars      │ INTEGER  │ Amount of data analyzed                 │
│ analysis_result  │ TEXT     │ Full AI analysis text                   │
│ personality_type │ TEXT     │ Detected personality category           │
│ confidence_score │ REAL     │ AI confidence level (0-100)             │
└──────────────────┴──────────┴─────────────────────────────────────────┘


🤖 AI PERSONALITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════

The system uses Google's Gemini AI to analyze typing patterns and provides:

1. PERSONALITY TYPE
   • Professional       • Student            • Developer/Programmer
   • Writer            • Gamer              • Casual User
   • And more...

2. KEY CHARACTERISTICS
   • Communication style
   • Technical proficiency
   • Work habits
   • Interests and hobbies

3. BEHAVIORAL PATTERNS
   • Typing speed and accuracy
   • Common phrases/vocabulary
   • Time of day usage patterns
   • Application preferences

4. CONFIDENCE SCORE
   • How confident the AI is in its assessment
   • Based on amount and quality of data

5. PERSONALIZED SUGGESTIONS
   • Insights about user habits
   • Potential interests
   • Behavioral tendencies


📊 USAGE EXAMPLES
═══════════════════════════════════════════════════════════════════════════

EXAMPLE 1: View Recent Logs
───────────────────────────────────────────────────────────────────────────
$ python view_logs.py
> Select option 1
> Enter 20 (to see last 20 logs)

EXAMPLE 2: Search for Specific Content
───────────────────────────────────────────────────────────────────────────
$ python view_logs.py
> Select option 4
> Enter keyword: "password"
> View all logs containing that word

EXAMPLE 3: View AI Analysis Results
───────────────────────────────────────────────────────────────────────────
$ python view_logs.py
> Select option 2
> See all personality analyses performed

EXAMPLE 4: Export All Data
───────────────────────────────────────────────────────────────────────────
$ python view_logs.py
> Select option 5
> All data exported to timestamped file


⚙️ CONFIGURATION OPTIONS
═══════════════════════════════════════════════════════════════════════════

In keylogger.py, you can modify:

┌────────────────────────────────────────────────────────────────────────┐
│ Variable              │ Default           │ Description               │
├───────────────────────┼───────────────────┼───────────────────────────┤
│ GOOGLE_API_KEY        │ (your key)        │ Google Gemini API key     │
│ DATABASE_FILE         │ keylogger_        │ SQLite database filename  │
│                       │ database.db       │                           │
│ log_file              │ keylog.txt        │ Local backup file         │
│ periodic_send         │ 60 seconds        │ How often to save logs    │
│ periodic_ai_analysis  │ 600 seconds       │ How often to run AI       │
│                       │ (10 minutes)      │ analysis                  │
└───────────────────────┴───────────────────┴───────────────────────────┘


🔧 ADVANCED FEATURES
═══════════════════════════════════════════════════════════════════════════

DATABASE ACCESS
───────────────────────────────────────────────────────────────────────────
Connect directly to the SQLite database:

import sqlite3
conn = sqlite3.connect('keylogger_database.db')
cursor = conn.cursor()

# Your custom queries here
cursor.execute('SELECT * FROM keylogs WHERE session_date = "2026-02-22"')
results = cursor.fetchall()

conn.close()


CUSTOM AI PROMPTS
───────────────────────────────────────────────────────────────────────────
Modify the AI prompt in keylogger.py to get different insights:

# Edit the 'prompt' variable in analyze_with_ai() function
# You can ask for:
# - Job role predictions
# - Skill level assessment
# - Language proficiency
# - Emotional state
# - And more...


⏱️ TIMELINE & AUTOMATION
═══════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│ Time          │ Action                                                  │
├───────────────┼─────────────────────────────────────────────────────────┤
│ 0:00          │ Keylogger starts                                        │
│ 1:00          │ First database save (60 seconds of typing)              │
│ 2:00          │ Second database save                                    │
│ 3:00          │ First AI analysis + Database stats display              │
│ 4:00          │ Third database save                                     │
│ ...           │ ...                                                     │
│ 13:00         │ Second AI analysis + Updated stats                      │
│ ...           │ Process continues until ESC is pressed                  │
└───────────────┴─────────────────────────────────────────────────────────┘


🎓 WHAT THE AI ANALYZES
═══════════════════════════════════════════════════════════════════════════

• Vocabulary complexity and technical terms used
• Grammar and writing style
• Common keyboard shortcuts and special characters
• Typing patterns (corrections, backspaces, etc.)
• Time periods of activity
• Application-specific patterns (code syntax, commands, etc.)
• Communication style (formal vs casual)
• Special symbols usage (programming, design, etc.)


📈 STATISTICS PROVIDED
═══════════════════════════════════════════════════════════════════════════

The system tracks:
✓ Total log entries
✓ Total characters typed
✓ Number of AI analyses performed
✓ First and last log timestamps
✓ Current detected personality type
✓ Analysis history and trends


🔒 PRIVACY & SECURITY NOTES
═══════════════════════════════════════════════════════════════════════════

⚠️ IMPORTANT:
• This tool captures ALL keyboard input
• Database stored locally in keylogger_database.db
• Local backup created in keylog.txt
• API calls send limited data to Google Gemini (max 3000 chars)
• Keep your Google API key secure
• Database is NOT encrypted
• Use responsibly and legally


🆘 TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

PROBLEM: "Database is locked"
SOLUTION: Close any other programs accessing the database file

PROBLEM: "API key invalid"
SOLUTION: Check your Google API key in keylogger.py line 9

PROBLEM: "Not enough data for analysis"
SOLUTION: Type at least 100 characters before AI analysis

PROBLEM: "Module not found"
SOLUTION: Install missing packages:
          pip install pynput google-generativeai


📞 SYSTEM REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════

✓ Python 3.7+
✓ Internet connection (for AI analysis)
✓ Active Google API key with Gemini access
✓ 10MB+ free disk space


═══════════════════════════════════════════════════════════════════════════
                            Created: February 22, 2026
                        Google API Key: AIzaSyBc3-hmBU3hzRt-9Ctix2xqt2TzXghYJ1U
═══════════════════════════════════════════════════════════════════════════
