# 📦 Import necessary libraries
import PyPDF2  # to read PDF files
import re  # to clean and process text
from collections import Counter  # to count word frequencies
import random  # for generating random choices (used in routine generator)

# ============================
# 📄 PART 1: PDF TEXT ANALYSIS
# ============================

# 📌 Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)  # creates a PDF reader object
        for page in reader.pages:
            text += page.extract_text() + "\n"  # extract text from each page
    return text

# 📌 Function to clean extracted text
def clean_text(text):
    # Convert text to lowercase, remove punctuation using regular expressions
    text = re.sub(r'\W+', ' ', text.lower())
    return text.split()  # return list of words

# 📌 Function to find most common keywords
def analyze_keywords(text, top_n=10):
    words = clean_text(text)
    common_words = Counter(words).most_common(top_n)  # count most frequent words
    return common_words

# ===================================
# 🧠 PART 2: SELF STUDY ROUTINE MAKER
# ===================================

# 📌 Function to generate a study routine
def generate_routine(subjects, daily_hours):
    hours_per_subject = daily_hours // len(subjects)  # divide time equally
    routine = {}
    
    for subject in subjects:
        routine[subject] = hours_per_subject  # assign base hours to each subject
    
    leftover = daily_hours % len(subjects)  # calculate leftover hours
    if leftover:
        random_subject = random.choice(subjects)  # assign leftovers randomly
        routine[random_subject] += leftover
    
    return routine

# =======================
# ▶️ MAIN EXECUTION BELOW
# =======================

# === INPUTS ===
pdf_path = "4thSEM.pdf"  # 🔄 change this to the actual PDF file path you want to analyze
subjects = ["Operating System", "Discrete Math", "Computer Networks", "Microprocessor", "Economics"]
daily_hours = 6  # ⏳ total hours available for self-study in a day

# === PART 1: PDF ANALYSIS ===
print("📄 Analyzing PDF...\n")
try:
    pdf_text = extract_text_from_pdf(pdf_path)  # extract all text
    keywords = analyze_keywords(pdf_text)  # analyze and get top keywords

    print("🔑 Top Keywords in PDF:")
    for word, freq in keywords:
        print(f"{word}: {freq}")
except FileNotFoundError:
    print(f"❌ Error: File '{pdf_path}' not found. Please check the path and try again.")
    keywords = []

# === PART 2: STUDY ROUTINE ===
print("\n📘 Generating Self Study Routine...\n")
routine = generate_routine(subjects, daily_hours)

print("📅 Study Plan:")
for subject, hours in routine.items():
    print(f"{subject}: {hours} hour(s)")
print("\n💡 Happy studying!")