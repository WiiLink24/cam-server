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


def digicam_sender(file, toemail, password):
    """Sends the images to the users email"""
    msg = Mail(
        from_email="noahpistilli@gmail.com",
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

    sg = SendGridAPIClient(config.sendgrid_key)
    response = sg.send(msg)
    print(response.status_code)
    
