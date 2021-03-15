import smtplib, email, ssl, tarfile, os, os.path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

subject = "Your 4-hour access report"
sender_email = os.environ["SENDER_EMAIL"]
receiver_email = os.environ["RECEIVER_EMAIL"]
password = os.environ["EMAIL_PASSWORD"]
smtp_server = os.environ["SMTP_SERVER"]
smtp_port = int(os.environ["SMTP_PORT"])

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Create the text of your message
text = """\
Hi,
How are you?
It's your 4-hour access report
"""

text = MIMEText(text, "plain")

# Add plain-text part to MIMEMultipart message
message.attach(text)

# Create file for sending
filename = "output/report.tar.gz"  # In same directory as script
display_filename = "report.tar.gz"

make_tarfile(filename, "output/")

# Open file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {display_filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, text
    )
