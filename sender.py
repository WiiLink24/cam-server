# Sends an image to a designated user over email
# TODO: Address concerns about file size and whether to store them on an external server
# and if we do, address concerns about user privacy, possibly IP locking them?
import binascii
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


def digicam_sender(file, toemail):
    msg = Mail(
        from_email="digicam@wiilink24.com",
        to_emails=toemail,
        subject="Here is your photo!",
        content="The photo is in attachments! Enjoy!",
    )
    handle = open(file)
    datatosend = handle.read()
    encoded_file = binascii.b2a_base64(datatosend, newline=True).decode()
    msg.attachment = Attachment(
        FileContent(encoded_file),
        FileName("image.jpg"),
        FileType("image/jpeg"),
        Disposition("attachment"),
    )
    response = SendGridAPIClient(config.sendgrid_key).send(msg)
    return (
        response.status_code,
        response.body,
        response.headers,
    )
