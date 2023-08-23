import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
import hashlib
import ezodf
import requests
import time
from tqdm import tqdm

# Function to fetch web content (HTML source) from a URL
def get_web_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)

        # Check if the response content is not empty
        if response.text:
            return response.text  # Return the HTML source code
        else:
            print(f"Content from {url} is empty.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None  # Return None in case of an error or unsuccessful request

# Function to read web addresses from an ODS file, skipping the first row (header)
def read_web_addresses_from_ods(ods_file):
    web_addresses = []
    doc = ezodf.opendoc(ods_file)

    # Assuming data is in the first sheet
    sheet = doc.sheets[0]

    # Start from the second row (row index 1)
    for row_index, row in enumerate(sheet.rows()):
        if row_index == 0:  # Skip the first row (header)
            continue

        name = row[0].value
        urls = [cell.value for cell in row[1:]]
        
        # Filter out None or empty URLs
        valid_urls = [url for url in urls if url is not None and url.strip() != '']
        
        if valid_urls:
            web_addresses.append((name, valid_urls))
    
    return web_addresses

# Function to compute the hash of web content
def compute_content_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

# Function to create the database if it doesn't exist
def create_database(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Create a table to store web content information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            hash TEXT NOT NULL,
            timestamp INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Function to check for changes in web content and notify if changes are found
def send_failed_sites_summary(email_config, failed_sites_with_urls):
    subject = "Failed Sites Summary"
    body = "The following sites have failed to retrieve content:\n\n"
    
    for site_name, urls in failed_sites_with_urls:
        body += f"- {site_name}\n"
        for url in urls:
            body += f"  - {url}\n"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_config['custom_sender_email']
    msg['To'] = email_config['recipient_email']

    try:
        smtp_server = smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port'])
        smtp_server.login(email_config['custom_sender_email'], email_config['sender_password'])
        smtp_server.sendmail(email_config['custom_sender_email'], [email_config['recipient_email']], msg.as_string())
        smtp_server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


# Function to send an email summary of changed sites, their URLs, and timestamps
def send_changed_sites_summary(email_config, changed_sites_with_urls_and_timestamp):
    subject = "Changed Sites Summary"
    body = "The following sites have changed:\n\n"

    for site_name, urls, timestamp in changed_sites_with_urls_and_timestamp:
        body += f"- {site_name} (Last Change: {timestamp})\n"
        for url in urls:
            body += f"  - {url}\n"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_config['custom_sender_email']
    msg['To'] = email_config['recipient_email']

    try:
        smtp_server = smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port'])
        smtp_server.login(email_config['custom_sender_email'], email_config['sender_password'])
        smtp_server.sendmail(email_config['custom_sender_email'], [email_config['recipient_email']], msg.as_string())
        smtp_server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check for changes in web content and notify if changes are found
def check_for_changes_and_notify(ods_file, database_file, email_config):
    # Check if the database file exists, and if not, create it
    if not os.path.exists(database_file):
        create_database(database_file)

    web_addresses = read_web_addresses_from_ods(ods_file)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    changed_sites = []  # Store sites with changed content, their URLs, and the timestamp
    failed_sites = []  # Store sites with failed URLs as tuples

    print("Starting the crawler...")
    start_time = time.time()  # Record the start time

    for name, urls in web_addresses:
        site_changed = False
        changed_urls = []  # Store URLs that have changed
        failed_urls = []  # Store URLs that have failed

        # print(f"Processing site: {name}")

        for url_index, url in enumerate(tqdm(urls, desc=f"Band: {name}", ncols=100 , ascii=' >=', unit="url")):
            current_hash = None  # Initialize current_hash here

            current_content = get_web_content(url)

            if current_content is not None:
                current_hash = compute_content_hash(current_content)
            else:
                print(f"Failed to retrieve content from {url}. Skipping...")
                failed_urls.append(url)
                continue

            cursor.execute("SELECT hash, timestamp FROM web_content WHERE name=? AND url=?", (name, url))
            previous_data = cursor.fetchone()

            if previous_data is not None:  # Check if previous_data is not None
                previous_hash, previous_timestamp = previous_data

                if current_hash != previous_hash:
                    site_changed = True
                    changed_urls.append(url)

            cursor.execute("REPLACE INTO web_content (name, url, hash, timestamp) VALUES (?, ?, ?, ?)", (name, url, current_hash, int(time.time())))
            conn.commit()

        if site_changed:
            changed_sites.append((name, urls, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))  # Include timestamp in the changed_sites tuple

        if failed_urls:
            failed_sites.append((name, failed_urls))  # Store both the site name and failed URLs as a tuple

        if changed_urls:  # Print only if there are changed URLs for this site
            print(f"Changed URLs for band: {name}")
            for changed_url in changed_urls:
                print(f"\t- {changed_url}")

        #print(f"Finished processing site: {name}")

    conn.close()

    if failed_sites:
        send_failed_sites_summary(email_config, failed_sites)  # Send failed summary with URLs

    if changed_sites:
        send_changed_sites_summary(email_config, changed_sites)  # Send changed summary with URLs and timestamp

    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate execution time

    print("Crawler completed.")
    print(f"Execution time: {execution_time:.2f} seconds")  # Print execution time

if __name__ == "__main__":
    ods_file = "webcrawler.ods"  # Replace with the path to your ODS file
    database_file = "web_content.db"  # Replace with the desired SQLite database filename

    email_config = {
        # Email configuration
        'custom_sender_email': 'email@domain.com',
        'sender_password': 'password_of_importance',
        'recipient_email': 'reciever_of_news@domain.com',
        'smtp_server': 'smtp.domain.com',  # Update for your email provider
        'smtp_port': 465,  # Update for your email provider
    }

    # You can remove the sleep since you're using systemd timer

    check_for_changes_and_notify(ods_file, database_file, email_config)
