import pandas as pd
import email_functions
import main_file





# if emails:
#     print(f"Fetched {len(emails)} emails.")
#     # Export to MySQL
#     email_functions.export_to_mysql(emails, email_functions.mysql_host, email_functions.mysql_user, email_functions.mysql_password, email_functions.mysql_database, "myEmails")
# else:
#     print("No emails fetched.")

# # Example query to read from MySQL
query = "SELECT Sender, COUNT(Sender) FROM myEmails GROUP BY Sender"
s1 = email_functions.read_sql_to_dataframe(query)
print(s1)

# Exporting email data to MySQL
ls=email_functions.fetch_emails_from_folder("[Gmail]/Spam")
df = pd.DataFrame(ls, columns=[ 'Subject','From','Date'])
email_functions.export_to_mysql(ls, "spamEmails")

# Defining recipient emails and recipient names
recipient_emails = ["emailfortesting1025@gmail.com", "kushagraofficialpurpose@gmail.com","10.feelatitspeak.25@gmail.com","emailforprivacy9@gmail.com","Himansuabc2004@gmail.com"]
names=["Kushagra","Anshul","Shreyansh","Akshat","Himansu"];

# Sending a bulk of common emails
email_functions.send_common_emails(recipient_emails, "Office of Dean, IIT Bombay", "Hi, I am willing to give you LOR for Kyoto Internship!!" )

# Sending a bulk of distinct emails
email_functions.send_distinct_emails(recipient_emails,names,"Office of Dean, IIT Bombay")


imap=main_file.connect_to_imap("imap.gmail.com")
# Fetching emails from the desired folder
starred_emails=main_file.fetch_emails(imap,"[Gmail]/Starred")
# Moving the required email to the desired folder
main_file.move_email(imap,starred_emails[0], "[Gmail]/Spam")