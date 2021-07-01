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

from camlib import current_order


def digicam_sender(file_path: str, user_email: str, is_for_card: bool):
    """Sends the images to the users email"""

    # Sending is optional.
    if config.sendgrid_key is None:
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

The WiiLink24 Team"""

    msg = Mail(
        from_email="digicam@wiilink24.com",
        to_emails=user_email,
        subject="Here is your order!",
        html_content=html_content,
    )

    with open(file_path, "rb") as f:
        data = f.read()
        f.close()

    encoded_file = base64.b64encode(data).decode()

    if is_for_card:
        msg.attachment = Attachment(
            FileContent(encoded_file),
            FileName("business_card.jpeg"),
            FileType("application/jpeg"),
            Disposition("attachment"),
        )
    else:
        msg.attachment = Attachment(
            FileContent(encoded_file),
            FileName("images.zip"),
            FileType("application/zip"),
            Disposition("attachment"),
        )

    sg = SendGridAPIClient(config.sendgrid_key)
    sg.send(msg)
