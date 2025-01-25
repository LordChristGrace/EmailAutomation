import imaplib
import email
import pandas as pd
from email.header import decode_header
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
EMAIL = "emailforprivacy9@gmail.com"  # Replace with your email
PASSWORD = "epdi ijfc twbw xxfw"      # Replace with your app password or OAuth
SMTP_SERVER = "smtp.gmail.com"
IMAP_SERVER = "imap.gmail.com"
SMTP_PORT = 587  # For TLS
mysql_host = "localhost"  # Replace with your MySQL server's hostname
mysql_user = "root"       # Replace with your MySQL username
mysql_password = "KushagraGupta192035"  # Replace with your MySQL password
mysql_database = "GmailData"  # Replace with your MySQL database name


# Function to decode email headers
def decode_header_value(header_value):
    decoded_parts = decode_header(header_value)
    decoded_string = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_string += part.decode(encoding or "utf-8", errors="ignore")
        else:
            decoded_string += part
    return decoded_string


# Function to fetch emails from a specific Gmail folder
def fetch_emails_from_folder(folder_name):
    username= EMAIL
    app_password = PASSWORD
    # Connect to Gmail IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        imap.login(username, app_password)
        print("Successfully connected to the IMAP server.")
    except imaplib.IMAP4.error:
        print("Failed to authenticate. Check your username/app password.")
        return []
    
    # Select the specific folder (label)
    status, messages = imap.select(folder_name)
    if status != "OK":
        print(f"Failed to open folder: {folder_name}")
        return []

    # Search for all emails in the folder
    status, msg_nums = imap.search(None, "All")
    if status != "OK":
        print("Failed to retrieve messages.")
        return []
    
    email_ids = msg_nums[0].split()
    print(f"Found {len(email_ids)} emails in {folder_name}.")
    email_data = []
    for num in msg_nums[0].split():
        # Fetch email by ID
        res, msg = imap.fetch(num, "(RFC822)")
        if res != "OK":
            print(f"Failed to fetch email ID {num}")
            continue

        for response_part in msg:
            if isinstance(response_part, tuple):
                # Parse email content
                raw_email = response_part[1]
                msg = email.message_from_bytes(raw_email)

                # Extract email details
                email_subject = decode_header_value(msg["Subject"])
                email_from = decode_header_value(msg["From"])
                email_date = msg["Date"]

                # Append email data without body
                email_data.append({
                    "Subject": email_subject,
                    "From": email_from,
                    "Date": email_date
                })
    return email_data


# Export email data to MySQL
def export_to_mysql(data, table_name):
    # Create a Pandas DataFrame from the email data
    df = pd.DataFrame(data)

    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = conn.cursor()

    # Create the table if it doesn't exist (without Body column)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Subject TEXT,
        Sender VARCHAR(255),
        Date VARCHAR(255)
    )
    """)

    # Insert email data into the table
    for _, row in df.iterrows():
        cursor.execute(f"""
        INSERT INTO {table_name} (Subject, Sender, Date)
        VALUES (%s, %s, %s)
        """, (row["Subject"], row["From"], row["Date"]))

    # Commit and return
    conn.commit()
    print(f"Data successfully exported to the MySQL database, table: {table_name}")


# Read required data from sql_table to DataFrame
def read_sql_to_dataframe(query):
    try:
        # Establish connection to the MySQL database
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )

        # Execute the query and load the results into a Pandas DataFrame
        df = pd.read_sql(query, conn)

        # Close the connection
        conn.close()

        return df

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return pd.DataFrame()  # Return an empty DataFrame on failure


# Function to send email
def send_email(smtp_server, recipient, subject, content):
    """Send an email to a specific recipient."""
    try:
        print(f"Connecting to SMTP server: {smtp_server}...")
        server = smtplib.SMTP(smtp_server, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL, PASSWORD)

        message = MIMEMultipart()
        message["From"] = EMAIL
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))

        server.sendmail(EMAIL, recipient, message.as_string())
        print(f"Email sent to {recipient}.")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to send common email in bulk
def send_common_emails(recipients, subject, content):
    """Send the same email to multiple recipients."""
    for recipient in recipients:
        send_email(SMTP_SERVER, recipient, subject, content)


# Function to generate required content for each distinct email while sending bulk emails        
def generate_invitation(recipient_name):
    email_content=[]
    # Sample invitation letter wherein each email may have a different recipient_name
    for name in recipient_name:
        email_content.append(f"""

        Dear {name},

        We are delighted to invite you to our upcoming event, event_name"!
        Time: event_time
        Date: event_date
        Location: event_location

        We would be honored to have you join us for this special occasion. Your presence would mean a lot   to us.

        Kindly RSVP by event_date.

        Looking forward to seeing you at the event!

        Best regards,
        host_name
        """)

    return email_content


# Function to send distinct emails in bulk
def send_distinct_emails(recipients, recipient_name, subject):
    contents = generate_invitation(recipient_name)
    for recipient,content in zip(recipients,contents):
        send_email(SMTP_SERVER, recipient, subject, content)
