import pandas as pd
import email_functions
import main_file


# Fetching a list of decrypted emails from the desired folder
emails=email_functions.fetch_emails_from_folder("Starred")
# Export the emails to MySQL
email_functions.export_to_mysql(emails, "starredEmails")


# # Example query to read from MySQL
query = "SELECT Sender, COUNT(Sender) FROM myEmails GROUP BY Sender"
s1 = email_functions.read_sql_to_dataframe(query)
print(s1)


# Exporting email data to MySQL
ls=email_functions.fetch_emails_from_folder("[Gmail]/Spam")
df = pd.DataFrame(ls, columns=[ 'Subject','From','Date'])
email_functions.export_to_mysql(ls, "spamEmails")


# Defining recipient emails and recipient names
recipient_emails = ["emailfortesting1025@gmail.com", "kushagraofficialpurpose@gmail.com","10.feelatitspeak.25@gmail.com","emailforprivacy9@gmail.com"]
names=["Kushagra","Anshul","Shreyansh","Akshat"];


# Sending a bulk of common emails
email_functions.send_common_emails(recipient_emails, "Office of Dean, IIT Bombay", "Hi, I am willing to give you LOR for Kyoto Internship!!" )


# Sending a bulk of distinct emails
email_functions.send_distinct_emails(recipient_emails,names,"Office of Dean, IIT Bombay")


# Establishing connection with Gmail
imap=main_file.connect_to_imap("imap.gmail.com")
# Fetching emails from the desired folder
starred_emails=main_file.fetch_emails(imap,"[Gmail]/Starred")
# Moving the required email to the desired folder
main_file.move_email(imap,starred_emails[0], "[Gmail]/Spam")