import fitz  # PyMuPDF
from datetime import datetime, timedelta
import spacy #pip install spacy
# ========== IMPORTS ==========

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# ========== PDF TEXT EXTRACTION ==========
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# ========== TOPIC EXTRACTION ==========
def extract_topics(text):
    doc = nlp(text)
    topics = set()
    for chunk in doc.noun_chunks:
        if 3 < len(chunk.text) < 50:
            topics.add(chunk.text.strip().lower())
    return list(topics)[:10]  # return top 10 for simplicity

# ========== STUDY ROUTINE CREATION ==========
def create_study_plan(topics, start_date_str, exam_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
    days = (exam_date - start_date).days

    if days < len(topics):
        return "Not enough days to study all topics!"

    plan = {}
    day_gap = days // len(topics)

    current_date = start_date
    for topic in topics:
        plan[current_date.strftime("%Y-%m-%d")] = f"Study: {topic}"
        current_date += timedelta(days=day_gap)

    return plan

# ========== MAIN ==========
if __name__ == "__main__":
    file_path = "your_pdf_file.pdf"  # Replace with your file
    start_date = "2025-04-16"
    exam_date = "2025-05-16"

    print("📄 Extracting PDF content...")
    text = extract_text_from_pdf(file_path)

    print("📚 Extracting study topics...")
    topics = extract_topics(text)
    print("🧠 Topics:", topics)

    print("📅 Creating study routine...")
    routine = create_study_plan(topics, start_date, exam_date)

    print("\n📘 Your Study Plan:")
    for date, task in routine.items():
        print(f"{date}: {task}")
