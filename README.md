
# Keystroke Logger — Google Sheets + Local Backup

A Python-based keystroke logger that captures every keypress and uploads them to a Google Sheets spreadsheet in batched intervals, while also maintaining a local backup file.

---

## Features

- Logs all keystrokes including special keys (`[ENTER]`, `[TAB]`, `[BKSP]`, `[SHIFT]`, etc.)
- Uploads captured keystrokes to **Google Sheets** every 30 seconds (configurable)
- Writes a **local backup** to `keylog.txt` on every flush
- Assigns a unique **Session ID** per run for easy log identification
- Gracefully stops on **ESC** key press with a final flush of remaining data
- Falls back to local-only mode if Google Sheets authentication fails

---

## Project Structure

```
newkeylogger/
├── keylogger.py                        # Main script
├── keylogger-database-<id>.json        # Google service account credentials
├── keylog.txt                          # Local backup log (auto-created)
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.8+
- A Google Cloud project with the **Google Sheets API** and **Google Drive API** enabled
- A **service account** with a downloaded JSON key file

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/newkeylogger.git
cd newkeylogger
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Google Sheets access

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable the **Google Sheets API** and **Google Drive API**.
4. Create a **Service Account** and download the JSON credentials file.
5. Place the JSON file in the project root and update `SERVICE_ACCOUNT_FILE` in `keylogger.py`:

```python
SERVICE_ACCOUNT_FILE = "your-credentials-file.json"
```

6. Share the target Google Spreadsheet (or let the script create one automatically) with the service account email address (found inside the JSON file as `client_email`).

### 4. (Optional) Adjust configuration

Edit the constants at the top of `keylogger.py`:

| Variable | Default | Description |
|---|---|---|
| `SERVICE_ACCOUNT_FILE` | `"keylogger-database-....json"` | Path to service account credentials |
| `SPREADSHEET_NAME` | `"Keylogger Logs"` | Name of the Google Spreadsheet |
| `FLUSH_INTERVAL` | `30` | Seconds between uploads to Google Sheets |
| `LOCAL_BACKUP_FILE` | `"keylog.txt"` | Path to the local backup log file |

---

## Usage

```bash
python keylogger.py
```

The logger will start and display session details in the console:

```
============================================================
       KEYSTROKE LOGGER  →  Google Sheets
============================================================
  Session ID   : A1B2C3D4
  Spreadsheet  : Keylogger Logs
  Flush every  : 30 seconds
  Local backup : keylog.txt
============================================================

  ▶  Logging started.  Press ESC to stop.
```

Press **ESC** to stop logging. Any remaining buffered keystrokes will be flushed before the program exits.

---

## Google Sheets Log Format

Each row written to the spreadsheet contains:

| Session ID | Date | Time | Keys Typed |
|---|---|---|---|
| `A1B2C3D4` | `2026-02-23` | `14:35:10` | `hello [ENTER] world` |

---

## Local Backup Format

Each line in `keylog.txt` follows the format:

```
[2026-02-23 14:35:10] hello [ENTER] world
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `pynput` | >=1.7.6 | Keyboard listening |
| `gspread` | >=5.7.0 | Google Sheets API client |
| `google-auth` | >=2.20.0 | Google service account authentication |

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Disclaimer

This tool is intended for **educational purposes** and **authorized monitoring only** (e.g., monitoring your own device). Using keyloggers on systems or accounts without explicit consent is illegal and unethical. The author assumes no responsibility for misuse.

---

