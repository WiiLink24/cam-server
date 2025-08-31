# Primary config for cam-server
db_url = "postgresql://username:password@localhost/database_name"

# Put your super secret SendGrid API key here.
# If you do not wish to send email, set to None.
smtp_key = "please_change_me"

# Sentry configuration for error logging.
use_sentry = False
sentry_dsn = "https://public@sentry.example.com/1"

# Printing service configurations
use_shutterfly = False
shutterfly_api_key = "your_shutterfly_key"
shutterfly_api_secret = "your_shutterfly_secret"

use_photobox = False
photobox_client_id = "your_photobox_id"
photobox_client_secret = "your_photobox_secret"
