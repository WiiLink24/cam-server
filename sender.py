# Sends an image to a designated user over email
# TODO: Address concerns about file size and whether to store them on an external server
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


def digicam_sender(file, toemail, password):
    """Sends the images to the users email"""
    msg = Mail(
        from_email="digicam@wiilink24.com",
        to_emails=toemail,
        subject="Here is your photo!",
        html_content=f"The photo is in attachments! Enjoy! The password is {password}",
    )

    with open(file, 'rb') as f:
        data = f.read()
        f.close()

    encoded_file = base64.b64encode(data).decode()

    msg.attachment = Attachment(
        FileContent(encoded_file),
        FileName("images.zip"),
        FileType("application/zip"),
        Disposition("attachment"),
    )

    try:
        sg = SendGridAPIClient(config.sendgrid_key)
        response = sg.send(msg)
        print(response.status_code)
    except Exception as e:
        print(e.msg)
