import smtplib
import csv
import time
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtp_config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

# Function to send a single email
async def send_email(subject, recipient, html_content, semaphore):
    async with semaphore:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {recipient}")
            return True
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")
            return False

# Function to process CSV and send emails
async def process_csv_and_send_emails(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        emails = [row[0] for row in reader]

    subject = "Your Subject Here"
    with open('templates/email_template.html', 'r') as template_file:
        html_content = template_file.read()

    # Create a semaphore to limit concurrent connections
    semaphore = asyncio.Semaphore(50)  # Adjust this value based on SMTP server limits

    # Create tasks for sending emails
    tasks = [send_email(subject, email, html_content, semaphore) for email in emails]

    # Use asyncio.gather to run tasks concurrently
    results = await asyncio.gather(*tasks)
    return results

async def main():
    csv_file_path = 'emails.csv'
    start_time = time.time()

    # Run the email sending process
    results = await process_csv_and_send_emails(csv_file_path)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Emails sent successfully: {sum(results)}")
    print(f"Emails failed: {len(results) - sum(results)}")

if __name__ == "__main__":
    asyncio.run(main())

# Function to be called by the API
def send_single_email(subject, recipient, html_content):
    return asyncio.run(send_email(subject, recipient, html_content, asyncio.Semaphore(1)))