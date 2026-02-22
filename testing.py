import smtplib
from email.mime.text import MIMEText

# Define email parameters
sender = 'your_email@example.com'
receiver = 'receiver_email@example.com'
subject = 'Test Email'
body = 'This is a test email sent from Python.'

# Create the email message
msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = receiver

# Send the email
try:
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender, 'your_password')
        server.sendmail(sender, receiver, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
