"""
AI Personality Analyser — reads keystroke data from Google Sheets
and produces a Big Five (OCEAN) personality profile.

Personality Dimensions Analysed
────────────────────────────────
O  Openness          — vocabulary richness, creative / diverse language
C  Conscientiousness — low error-rate, neat corrections, consistent timing
E  Extraversion      — high typing volume, social keywords, exclamation use
A  Agreeableness     — positive sentiment, polite / warm language
N  Neuroticism       — high backspace rate, negative sentiment, late-night typing

How to run
──────────
    python ai_model.py
"""

import re
import math
from collections import Counter
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

try:
    from textblob import TextBlob
except Exception:  # fallback if TextBlob isn't installed
    class TextBlob:  # type: ignore
        def __init__(self, text: str) -> None:
            self._text = text or ""

        @property
        def sentiment(self):
            positive = {"good", "great", "love", "happy", "excellent", "awesome", "enjoy"}
            negative = {"bad", "sad", "hate", "angry", "terrible", "awful", "worst"}
            words = re.findall(r"[a-zA-Z']+", self._text.lower())
            if not words:
                return type("Sentiment", (), {"polarity": 0.0, "subjectivity": 0.0})()
            pos_hits = sum(1 for w in words if w in positive)
            neg_hits = sum(1 for w in words if w in negative)
            polarity = 0.0
            total = pos_hits + neg_hits
            if total:
                polarity = (pos_hits - neg_hits) / total
            subjectivity = min(1.0, total / max(1, len(words)))
            return type("Sentiment", (), {"polarity": polarity, "subjectivity": subjectivity})()

# ─────────────────────────────────────────────
# Configuration  (mirrors keylogger.py settings)
# ─────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = "keylogger-database-13f0c3b13a4e.json"
SPREADSHEET_NAME     = "Keylogger Logs"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ─────────────────────────────────────────────
# Word lists for trait scoring
# ─────────────────────────────────────────────
SOCIAL_WORDS = {
    "friend", "friends", "family", "love", "party", "meet", "chat",
    "fun", "hang", "together", "group", "team", "people", "everyone",
    "talk", "call", "laugh", "enjoy", "celebrate",
}

POLITE_WORDS = {
    "please", "thank", "thanks", "sorry", "excuse", "pardon", "welcome",
    "appreciate", "grateful", "kind", "care", "help", "support",
}

NEGATIVE_WORDS = {
    "hate", "angry", "terrible", "awful", "worst", "horrible", "sad",
    "depressed", "anxious", "stressed", "worried", "frustrated",
    "useless", "failed", "mistake", "error", "wrong", "bad",
}

INTELLECTUAL_WORDS = {
    "think", "because", "reason", "theory", "idea", "concept", "understand",
    "analyse", "analyze", "research", "study", "learn", "read", "book",
    "question", "explore", "discover", "knowledge", "science", "logic",
}

# ─────────────────────────────────────────────
# Step 1 — Fetch data from Google Sheets
# ─────────────────────────────────────────────
def fetch_sheet_data() -> list[dict]:
    """
    Authenticate with Google Sheets and return all data rows as a
    list of dicts with keys: session_id, date, time, keys_typed.
    """
    print("  Connecting to Google Sheets …")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc    = gspread.authorize(creds)
    sh    = gc.open(SPREADSHEET_NAME)
    ws    = sh.sheet1

    all_rows  = ws.get_all_values()
    if not all_rows:
        raise ValueError("The spreadsheet is empty.")

    header    = [h.strip().lower().replace(" ", "_") for h in all_rows[0]]
    data_rows = all_rows[1:]

    records   = []
    for row in data_rows:
        if len(row) < 4:
            continue
        record = dict(zip(header, row))
        records.append(record)

    print(f"  Fetched {len(records)} keystroke session(s).")
    return records


# ─────────────────────────────────────────────
# Step 2 — Parse raw keystroke strings
# ─────────────────────────────────────────────
def parse_keystrokes(raw: str) -> dict:
    """
    Parse a raw keystroke string like 'hello [BKSP]wrld [ENTER]' into:
      - clean_text   : readable text after applying backspaces
      - words        : list of words
      - backspaces   : count of [BKSP] tokens
      - caps_locks   : count of [CAPS] tokens
      - enters       : count of [ENTER] tokens
      - total_keys   : total keystrokes (including specials)
      - exclamations : count of '!' characters
    """
    # Count special keys before stripping
    backspaces   = raw.count("[BKSP]")
    caps_locks   = raw.count("[CAPS]")
    enters       = raw.count("[ENTER]")
    tabs         = raw.count("[TAB]")
    total_keys   = len(re.findall(r"\[.*?\]|.", raw))

    # Simulate backspace key to build clean text
    cleaned_chars: list[str] = []
    tokens = re.findall(r"\[.*?\]|.", raw)
    for token in tokens:
        if token == "[BKSP]":
            if cleaned_chars:
                cleaned_chars.pop()
        elif token.startswith("["):
            pass                        # skip other special keys
        else:
            cleaned_chars.append(token)

    clean_text   = "".join(cleaned_chars)
    exclamations = clean_text.count("!")
    words        = re.findall(r"[a-zA-Z']+", clean_text.lower())

    return {
        "clean_text"  : clean_text,
        "words"       : words,
        "backspaces"  : backspaces,
        "caps_locks"  : caps_locks,
        "enters"      : enters,
        "tabs"        : tabs,
        "total_keys"  : total_keys,
        "exclamations": exclamations,
    }


# ─────────────────────────────────────────────
# Step 3 — Aggregate metrics across all sessions
# ─────────────────────────────────────────────
def aggregate_metrics(records: list[dict]) -> dict:
    """
    Combine all sessions into a single set of aggregate metrics
    used for personality scoring.
    """
    total_keys   = 0
    total_bksp   = 0
    total_caps   = 0
    total_enters = 0
    total_excl   = 0
    all_words:   list[str] = []
    all_text:    list[str] = []
    active_hours:list[int] = []

    for rec in records:
        parsed = parse_keystrokes(rec.get("keys_typed", ""))

        total_keys   += parsed["total_keys"]
        total_bksp   += parsed["backspaces"]
        total_caps   += parsed["caps_locks"]
        total_enters += parsed["enters"]
        total_excl   += parsed["exclamations"]
        all_words    .extend(parsed["words"])
        all_text     .append(parsed["clean_text"])

        # Extract hour of day from time field e.g. "14:32:07"
        time_str = rec.get("time", "")
        try:
            hour = int(time_str.split(":")[0])
            active_hours.append(hour)
        except (ValueError, IndexError):
            pass

    full_text = " ".join(all_text)

    # Vocabulary richness  — Type-Token Ratio (TTR)
    word_count  = len(all_words)
    unique_words = len(set(all_words))
    ttr = unique_words / word_count if word_count > 0 else 0

    # Lexical diversity via log-entropy
    word_freq  = Counter(all_words)
    entropy    = 0.0
    if word_count > 0:
        for freq in word_freq.values():
            p = freq / word_count
            entropy -= p * math.log2(p)

    # Sentiment via TextBlob
    blob       = TextBlob(full_text)
    sentiment  = blob.sentiment.polarity      # -1 (negative) … +1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) … 1 (subjective)

    # Word-list hit counts
    word_set           = set(all_words)
    social_hits        = len(word_set & SOCIAL_WORDS)
    polite_hits        = len(word_set & POLITE_WORDS)
    negative_hits      = len(word_set & NEGATIVE_WORDS)
    intellectual_hits  = len(word_set & INTELLECTUAL_WORDS)

    # Error rate = backspaces / total keys
    error_rate = total_bksp / total_keys if total_keys > 0 else 0

    # Capitalisation intensity = CAPS locks per 1000 keys
    caps_rate  = (total_caps / total_keys * 1000) if total_keys > 0 else 0

    # Exclamation intensity
    excl_rate  = (total_excl / word_count * 100) if word_count > 0 else 0

    # Late-night activity ratio (22:00–04:00)
    late_night  = sum(1 for h in active_hours if h >= 22 or h <= 4)
    night_ratio = late_night / len(active_hours) if active_hours else 0

    # Session count
    session_count = len(records)

    return {
        "total_keys"       : total_keys,
        "word_count"       : word_count,
        "unique_words"     : unique_words,
        "ttr"              : round(ttr, 4),
        "entropy"          : round(entropy, 4),
        "error_rate"       : round(error_rate, 4),
        "caps_rate"        : round(caps_rate, 4),
        "excl_rate"        : round(excl_rate, 4),
        "sentiment"        : round(sentiment, 4),
        "subjectivity"     : round(subjectivity, 4),
        "social_hits"      : social_hits,
        "polite_hits"      : polite_hits,
        "negative_hits"    : negative_hits,
        "intellectual_hits": intellectual_hits,
        "night_ratio"      : round(night_ratio, 4),
        "session_count"    : session_count,
        "top_words"        : word_freq.most_common(15),
    }


# ─────────────────────────────────────────────
# Step 4 — Score Big Five traits
# ─────────────────────────────────────────────
def score_ocean(m: dict) -> dict[str, float]:
    """
    Map aggregate metrics to a 0–100 score for each Big Five dimension.

    Scoring logic
    ─────────────
    O  Openness          ← vocabulary diversity (TTR, entropy), intellectual words
    C  Conscientiousness ← low error-rate, low caps, consistent typing
    E  Extraversion      ← high word volume, social words, exclamations
    A  Agreeableness     ← positive sentiment, polite words, low negative words
    N  Neuroticism       ← high error-rate, negative words, late-night activity
    """

    def clamp(v: float) -> float:
        return max(0.0, min(100.0, v))

    # ── Openness (O) ──────────────────────────────────────────────────────────
    o_ttr         = m["ttr"] * 80                          # 0–80
    o_entropy     = min(m["entropy"] / 8, 1) * 50          # normalise entropy
    o_intellectual= min(m["intellectual_hits"] / 10, 1) * 30
    o_score       = clamp((o_ttr + o_entropy + o_intellectual) / 1.6)

    # ── Conscientiousness (C) ─────────────────────────────────────────────────
    c_accuracy    = (1 - m["error_rate"]) * 60             # low error → high C
    c_caps        = max(0, 20 - m["caps_rate"] * 2)        # low CAPS → high C
    c_sessions    = min(m["session_count"] / 10, 1) * 20   # consistent usage
    c_score       = clamp(c_accuracy + c_caps + c_sessions)

    # ── Extraversion (E) ──────────────────────────────────────────────────────
    e_volume      = min(m["word_count"] / 2000, 1) * 40    # word volume
    e_social      = min(m["social_hits"] / 8, 1) * 35
    e_excl        = min(m["excl_rate"] / 3, 1) * 25
    e_score       = clamp(e_volume + e_social + e_excl)

    # ── Agreeableness (A) ─────────────────────────────────────────────────────
    a_sentiment   = (m["sentiment"] + 1) / 2 * 50          # map -1..1 → 0..50
    a_polite      = min(m["polite_hits"] / 6, 1) * 30
    a_neg_penalty = min(m["negative_hits"] / 5, 1) * 20
    a_score       = clamp(a_sentiment + a_polite - a_neg_penalty + 20)

    # ── Neuroticism (N) ───────────────────────────────────────────────────────
    n_error       = min(m["error_rate"] / 0.3, 1) * 35     # high error → high N
    n_negative    = min(m["negative_hits"] / 8, 1) * 30
    n_night       = m["night_ratio"] * 25
    n_sentiment   = max(0, -m["sentiment"]) * 20            # negative sentiment
    n_score       = clamp(n_error + n_negative + n_night + n_sentiment)

    return {
        "Openness"         : round(o_score, 1),
        "Conscientiousness": round(c_score, 1),
        "Extraversion"     : round(e_score, 1),
        "Agreeableness"    : round(a_score, 1),
        "Neuroticism"      : round(n_score, 1),
    }


# ─────────────────────────────────────────────
# Step 5 — Generate human-readable interpretation
# ─────────────────────────────────────────────
TRAIT_INTERPRETATIONS = {
    "Openness": {
        "high"  : ("Highly imaginative and curious. You embrace new ideas, love learning, "
                   "and tend to use rich, varied vocabulary in your writing."),
        "medium": ("Moderately open to new experiences. You balance creativity with "
                   "practicality and adapt your language to situations."),
        "low"   : ("Prefers routine and familiarity. Straightforward and conventional "
                   "in expression, focused on what is concrete and reliable."),
    },
    "Conscientiousness": {
        "high"  : ("Organised, disciplined, and detail-oriented. You rarely make typing "
                   "mistakes and prefer to correct errors promptly."),
        "medium": ("Reasonably reliable and organised with occasional lapses, balancing "
                   "care with spontaneity."),
        "low"   : ("Spontaneous and flexible. You may type quickly without much "
                   "concern for precision, prioritising speed over accuracy."),
    },
    "Extraversion": {
        "high"  : ("Outgoing and energetic. Your text shows high volume, enthusiasm "
                   "(exclamation marks), and frequent social references."),
        "medium": ("Ambivert tendencies — comfortable in social and solitary contexts, "
                   "with moderate expressiveness."),
        "low"   : ("Reserved and introspective. You tend to type less and keep "
                   "expression concise and measured."),
    },
    "Agreeableness": {
        "high"  : ("Warm, cooperative, and empathetic. Your language is positive and "
                   "you frequently use polite, kind expressions."),
        "medium": ("Generally agreeable with a balance of assertiveness and warmth."),
        "low"   : ("Direct and task-focused. You may come across as blunt, but this "
                   "often reflects efficiency and no-nonsense communication."),
    },
    "Neuroticism": {
        "high"  : ("Emotionally sensitive, possibly experiencing stress or anxiety. "
                   "High correction rate and negative language patterns suggest "
                   "inner tension."),
        "medium": ("Moderate emotional reactivity — generally stable with occasional "
                   "stress-driven behaviour (e.g., late-night sessions, error bursts)."),
        "low"   : ("Emotionally stable and resilient. Calm typing patterns and "
                   "positive or neutral language reflect inner composure."),
    },
}


def interpret_score(trait: str, score: float) -> str:
    if score >= 65:
        level = "high"
    elif score >= 35:
        level = "medium"
    else:
        level = "low"
    return TRAIT_INTERPRETATIONS[trait][level]


def archetype_label(scores: dict[str, float]) -> str:
    """Return a one-line personality archetype based on dominant traits."""
    o, c, e, a, n = (
        scores["Openness"],
        scores["Conscientiousness"],
        scores["Extraversion"],
        scores["Agreeableness"],
        scores["Neuroticism"],
    )

    if o > 65 and c > 60:
        return "The Visionary — creative, disciplined, and goal-oriented."
    if e > 65 and a > 60:
        return "The Connector — sociable, warm, and genuinely people-focused."
    if c > 65 and n < 35:
        return "The Perfectionist — meticulous, stable, and highly reliable."
    if o > 65 and e < 40:
        return "The Deep Thinker — intellectual, introspective, and imaginative."
    if n > 60 and o > 55:
        return "The Sensitive Artist — emotionally rich, creative, and expressive."
    if n > 60 and c < 40:
        return "The Free Spirit — spontaneous, emotionally intense, and unpredictable."
    if c > 60 and a > 60:
        return "The Steady Helper — dependable, cooperative, and quietly devoted."
    if e > 65 and c < 40:
        return "The Adventurer — energetic, fun-loving, and lives in the moment."
    if a > 65 and n < 35:
        return "The Peacemaker — kind, calm, and harmonious in all interactions."
    return "The Balanced Individual — well-rounded across all five dimensions."


# ─────────────────────────────────────────────
# Step 6 — ASCII bar chart for terminal output
# ─────────────────────────────────────────────
def bar(score: float, width: int = 40) -> str:
    filled = int(score / 100 * width)
    return "█" * filled + "░" * (width - filled)


# ─────────────────────────────────────────────
# Main — orchestrate everything
# ─────────────────────────────────────────────
def main():
    print()
    print("═" * 62)
    print("       AI PERSONALITY ANALYSER  ·  Big Five (OCEAN) Model")
    print("═" * 62)

    # 1. Fetch
    try:
        records  = fetch_sheet_data()
    except Exception as e:
        print(f"\n  ✗ Failed to fetch data: {e}")
        return

    if not records:
        print("  ✗ No data found in the spreadsheet.")
        return

    # 2. Aggregate
    print("\n  Analysing keystroke patterns …")
    metrics = aggregate_metrics(records)

    # 3. Score
    scores = score_ocean(metrics)

    # 4. Display metrics summary
    print()
    print("─" * 62)
    print("  KEYSTROKE STATISTICS")
    print("─" * 62)
    print(f"  Sessions analysed    : {metrics['session_count']}")
    print(f"  Total keystrokes     : {metrics['total_keys']:,}")
    print(f"  Total words typed    : {metrics['word_count']:,}")
    print(f"  Unique words         : {metrics['unique_words']:,}")
    print(f"  Vocabulary richness  : {metrics['ttr']:.2%}  (Type-Token Ratio)")
    print(f"  Typing error rate    : {metrics['error_rate']:.2%}  (backspace ÷ keys)")
    print(f"  Sentiment polarity   : {metrics['sentiment']:+.3f}  (-1 negative → +1 positive)")
    print(f"  Subjectivity         : {metrics['subjectivity']:.3f}  (0 objective → 1 subjective)")
    print(f"  Late-night activity  : {metrics['night_ratio']:.2%}  (22:00–04:00 sessions)")
    print()
    print(f"  Top words  : {', '.join(w for w, _ in metrics['top_words'][:10])}")

    # 5. Display OCEAN scores
    print()
    print("─" * 62)
    print("  PERSONALITY PROFILE  —  Big Five (OCEAN)")
    print("─" * 62)
    for trait, score in scores.items():
        initial = trait[0]
        label   = f"  {initial}  {trait:<20}"
        print(f"{label}  {score:5.1f}/100  {bar(score, 30)}")

    # 6. Detailed interpretations
    print()
    print("─" * 62)
    print("  TRAIT INTERPRETATIONS")
    print("─" * 62)
    for trait, score in scores.items():
        level = "HIGH" if score >= 65 else ("MEDIUM" if score >= 35 else "LOW")
        print(f"\n  [{level}]  {trait}  ({score:.1f}/100)")
        # Word-wrap at ~60 chars
        desc = interpret_score(trait, score)
        words = desc.split()
        line  = "    "
        for word in words:
            if len(line) + len(word) + 1 > 62:
                print(line)
                line = "    " + word + " "
            else:
                line += word + " "
        if line.strip():
            print(line)

    # 7. Archetype
    print()
    print("─" * 62)
    print("  PERSONALITY ARCHETYPE")
    print("─" * 62)
    print(f"\n  ★  {archetype_label(scores)}")

    # 8. Key behavioural insights
    print()
    print("─" * 62)
    print("  KEY BEHAVIOURAL INSIGHTS")
    print("─" * 62)

    insights = []

    if metrics["error_rate"] > 0.15:
        insights.append("You tend to type fast and self-correct frequently — "
                        "suggesting urgency or impulsive thinking.")
    elif metrics["error_rate"] < 0.03:
        insights.append("Very low error-rate — you are a careful, deliberate typist.")

    if metrics["night_ratio"] > 0.4:
        insights.append("High late-night activity detected — you may be a night owl "
                        "or experience difficulty 'switching off'.")

    if metrics["caps_rate"] > 5:
        insights.append("Frequent CAPS LOCK usage — may indicate strong emotional "
                        "expression or emphasis-heavy communication style.")

    if metrics["excl_rate"] > 2:
        insights.append("Enthusiastic use of exclamation marks — expressive and energetic.")

    if metrics["social_hits"] > 5:
        insights.append("Vocabulary is socially oriented — people and relationships "
                        "are a strong theme.")

    if metrics["intellectual_hits"] > 5:
        insights.append("Intellectual vocabulary is prominent — you enjoy reasoning, "
                        "learning, and analysing.")

    if metrics["sentiment"] < -0.15:
        insights.append("Overall text tone leans negative — possible frustration, "
                        "stress, or critical thinking style.")
    elif metrics["sentiment"] > 0.15:
        insights.append("Overall text tone is positive — optimistic and constructive "
                        "communication style.")

    if not insights:
        insights.append("Typing patterns are balanced — no extreme behavioural markers detected.")

    for i, insight in enumerate(insights, 1):
        words  = insight.split()
        line   = f"  {i}.  "
        for word in words:
            if len(line) + len(word) + 1 > 62:
                print(line)
                line = "      " + word + " "
            else:
                line += word + " "
        if line.strip():
            print(line)

    print()
    print("═" * 62)
    print("  Analysis complete.  Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("═" * 62)
    print()


if __name__ == "__main__":
    main()
