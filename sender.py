# Sends an image to a designated user over email
# and if we do, address concerns about user privacy, possibly IP locking them?
import base64
import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)


def digicam_sender(file, user_email):
    """Sends the images to the users email"""
    msg = Mail(
        from_email="digicam@wiilink24.com",
        to_emails=user_email,
        subject="Here is your order!",
        html_content="""Hello!
Attached are your images from the Digicam Print Channel.
We hope you enjoy, and thank you for using our service!

The WiiLink24 Team""",
    )

    with open(file, "rb") as f:
        data = f.read()
        f.close()

    encoded_file = base64.b64encode(data).decode()

    msg.attachment = Attachment(
        FileContent(encoded_file),
        FileName("images.zip"),
        FileType("application/zip"),
        Disposition("attachment"),
    )

    sg = SendGridAPIClient(config.sendgrid_key)
    sg.send(msg)
