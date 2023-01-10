# Sends an image to a designated user over email
# and if we do, address concerns about user privacy, possibly IP locking them?
import base64
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

from camlib import current_order


def digicam_sender(file_path: str, user_email: str, is_for_card: bool):
    """Sends the images to the users email"""

    # Sending is optional.
    if config.smtp_key is None:
        return

    html_content = """Hello!
Attached are your images from the Digicam Print Channel.
We hope you enjoy, and thank you for using our service!"""

    if is_for_card:
        html_content += f"""

It looks like you ordered a business card. Did you know you can share these publicly via Digicard?
If you're interested, visit https://card.wiilink24.com. Your order ID to link is {current_order.order_id}.
Do not share this order ID with anyone else, or they will be able to use your card.
"""

    html_content += """

The WiiLink Team"""

    with open(file_path, "rb") as f:
        data = f.read()
        f.close()

    msg = MIMEMultipart()
    msg.attach(MIMEText(html_content))

    if is_for_card:
        part = MIMEApplication(data, Name="business_card.jpeg")
        part['Content-Disposition'] = f'attachment; filename="business_card.jpeg"'
    else:
        part = MIMEApplication(data, Name="images.zip")
        part['Content-Disposition'] = f'attachment; filename="images.zip"'

    msg.attach(part)

    msg["Subject"] = "Here is your order!"
    msg["From"] = "images@digicam.wiilink24.com"
    msg["To"] = user_email

    s = smtplib.SMTP('smtp.mailgun.org', 587)
    s.login('postmaster@digicam.wiilink24.com', config.smtp_key)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.close()
