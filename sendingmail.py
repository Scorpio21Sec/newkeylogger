import smtplib 
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', 25)
server.ehlo()

with open('password.txt', 'r') as f:
    password = f.read()
server.login('mailtesting@host.com', password)

msg = MIMEMultipart
msg['From'] = 'mailtesting@host.com'
msg['Subject'] = 'Just a test for practice'

with open('test.txt', 'r') as f:
    body = f.read()
    msg.attach(MIMEText(body, 'plain'))
    
    filename =(         )
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)    
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)
    text = msg.as_string()
    server.sendmail