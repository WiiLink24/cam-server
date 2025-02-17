# Primary config for cam-server
db_url = "postgresql://username:password@localhost/database_name"

# Put your super secret SendGrid API key here.
# If you do not wish to send email, set to None.
sendgrid_key = "please_change_me"

# Sentry configuration for error logging.
use_sentry = False
sentry_dsn = "https://public@sentry.example.com/1"
