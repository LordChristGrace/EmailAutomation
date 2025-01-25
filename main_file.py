import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Server Configurations
GMAIL_IMAP = "imap.gmail.com"
OUTLOOK_IMAP = "outlook.office365.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # For TLS

# User Authentication
EMAIL = "emailforprivacy9@gmail.com"  # Replace with your email
PASSWORD = "epdi ijfc twbw xxfw"      # Replace with your app password or OAuth


# Function to establish connection with Gmail
def connect_to_imap(server):
    """Connect to IMAP server and authenticate."""
    try:
        print(f"Connecting to IMAP server: {server}...")
        imap = imaplib.IMAP4_SSL(server, 993)  # Ensure SSL and port are correct
        imap.login(EMAIL, PASSWORD)
        print("Connected to IMAP server successfully.")
        return imap
    except imaplib.IMAP4.error as e:
        print(f"IMAP Authentication Error: {e}")
    except Exception as e:
        print(f"Failed to connect to IMAP server: {e}")
    return None


# Function to fetch emails from the desired folder
def fetch_emails(imap, folder="Inbox", search_filter="ALL"):
    """Fetch emails from a specific folder using search criteria."""
    try:
        imap.select(folder)
        status, messages = imap.search(None, search_filter)
        if status != "OK":
            print(f"Failed to fetch emails from {folder}.")
            return []

        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} emails in {folder}.")
        return email_ids
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []


# Function to move an email from source foldre to destination folder
def move_email(imap, email_id, target_folder):
    """Move an email to a specific folder (e.g., out of Spam)."""
    try:
        result = imap.copy(email_id,target_folder)
        if result[0] == "OK":
            print(f"Email {email_id.decode()} moved to {target_folder}.")
        else:
            print(f"Failed to move email {email_id.decode()}.")
    except Exception as e:
        print(f"Error moving email: {e}")