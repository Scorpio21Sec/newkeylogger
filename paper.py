import os
import sys
from typing import Optional

try:
	from dotenv import load_dotenv  # optional; if installed
	load_dotenv()
except Exception:
	# dotenv is optional; proceed if not installed
	pass

def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
	val = os.environ.get(name)
	return val if val else default

def send_sms(to_number: str, message: str) -> str:
	"""Send an SMS using Twilio. Returns the message SID.

	Required env vars:
	  - TWILIO_ACCOUNT_SID
	  - TWILIO_AUTH_TOKEN
	  - TWILIO_FROM_NUMBER (your Twilio phone number or Messaging Service SID)
	"""
	account_sid = get_env("TWILIO_ACCOUNT_SID")
	auth_token = get_env("TWILIO_AUTH_TOKEN")
	from_number = get_env("TWILIO_FROM_NUMBER")

	if not account_sid or not auth_token or not from_number:
		raise RuntimeError(
			"Missing Twilio configuration. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER."
		)

	try:
		from twilio.rest import Client  # type: ignore
	except Exception as e:
		raise RuntimeError(
			"Twilio client not installed. Install with: pip install twilio"
		) from e

	client = Client(account_sid, auth_token)

	# Accept either E.164 phone number or a Messaging Service SID in from_number
	create_kwargs = {"body": message, "to": to_number}
	if from_number.startswith("MG"):
		create_kwargs["messaging_service_sid"] = from_number
	else:
		create_kwargs["from_"] = from_number

	msg = client.messages.create(**create_kwargs)
	return msg.sid

def main(argv: list[str]) -> int:
	if len(argv) < 3:
		print("Usage: python paper.py <phone_number> <message>")
		print("Example: python paper.py +1234567890 \"Hello from Twilio!\"")
		return 1

	to_number = argv[1]
	message = " ".join(argv[2:])
	try:
		sid = send_sms(to_number, message)
		print(f"Sent. SID: {sid}")
		return 0
	except Exception as e:
		print(f"Error: {e}")
		return 2

if __name__ == "__main__":
	sys.exit(main(sys.argv))
