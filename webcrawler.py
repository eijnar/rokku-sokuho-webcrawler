import os
import asyncio
import hashlib
import time
import statistics
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import asyncpg
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from logging_config import setup_logging, get_logger


# Load environment variables from .env file
load_dotenv()

# Setup environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

setup_logging()
log = get_logger(__name__)


async def create_db_pool():
    log.debug("Creating database connection pool.")
    try:
        return await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        log.error(f"Failed to create database connection pool: {e}")
        raise


async def fetch_band_urls(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT band.band_id, band.band_name, band_url.url_id, band_url.url, band_url.class_name "
            "FROM band "
            "JOIN band_url ON band.band_id = band_url.band_id;"
        )
        band_data = {}
        for row in rows:
            if row['band_id'] not in band_data:
                band_data[row['band_id']] = {
                    'band_name': row['band_name'],
                    'urls': []
                }
            band_data[row['band_id']]['urls'].append({
                'url_id': row['url_id'],
                'url': row['url'],
                'class_name': row['class_name']  # Include class_name in the data structure
            })
        return band_data


async def process_band(band_id, band_info, pool, timing_list, updated_sites, failed_sites):
    log.info(f"Processing {band_info['band_name']}...")
    for url_info in band_info['urls']:
        await process_url(band_id, band_info['band_name'], url_info, pool, timing_list, updated_sites, failed_sites)


async def process_url(band_id, band_name, url_info, pool, timing_list, updated_sites, failed_sites):
    start_time = time.time()
    try:
        new_hash = await get_web_content(url_info['url'], url_info['class_name'])
        async with pool.acquire() as conn:
            old_hash = await conn.fetchval(
                "SELECT hash_value FROM band_url WHERE url_id = $1", url_info['url_id']
            )
            if new_hash != old_hash:
                log.info(f"Content has changed for URL {url_info['url']}. Updating database...")
                await conn.execute(
                    "UPDATE band_url SET hash_value = $1, last_updated = (NOW() AT TIME ZONE 'Europe/Stockholm') WHERE url_id = $2",
                    new_hash, url_info['url_id']
                )
                if band_name not in updated_sites:
                    updated_sites[band_name] = []
                updated_sites[band_name].append(url_info['url'])
            else:
                await conn.execute(
                    "UPDATE band_url SET last_updated = (NOW() AT TIME ZONE 'Europe/Stockholm') WHERE url_id = $1",
                    url_info['url_id']
                )
    except Exception as e:
        log.error(f"Failed to process URL {url_info['url']}: {str(e)}")
        if band_name not in failed_sites:
            failed_sites[band_name] = []
        failed_sites[band_name].append(url_info['url'])
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE band_url SET last_failed = (NOW() AT TIME ZONE 'Europe/Stockholm') WHERE url_id = $1",
                url_info['url_id']
            )
    duration = time.time() - start_time
    timing_list.append(duration)


async def compute_content_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


async def get_web_content(url, class_name):
    try:
        browser = await launch(headless=True)
        page = await browser.newPage()
        try:
            await page.goto(url, options={'timeout': 60000})
            html_content = await page.content()
        except TimeoutError as e:
            log.error(f"Timeout when accessing {url}: {str(e)}")
            return None  # Decide if you need to return a specific value here
        finally:
            await page.close()
    finally:
        await browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')
    if class_name:
        elements = soup.find_all(class_=class_name)
        content = " ".join([element.get_text(strip=True) for element in elements])
    else:
        content = soup.body.get_text(strip=True) if soup.body else ""
        log.debug(content)

    return await compute_content_hash(content)


def send_email(subject, body):
    sender_email = os.getenv('MAIL_SENDER')
    sender_password = os.getenv('MAIL_PASSWORD')
    recipient = os.getenv('MAIL_TO')
    smtp_url = os.getenv('MAIL_SMTP')
    smtp_port = os.getenv('MAIL_PORT')
    
    # Create the MIME structure
    message = MIMEMultipart()
    message["From"] = f"Rokku-Sokuho webcrawler <{sender_email}>"
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Connect to server using secure context
        with smtplib.SMTP_SSL(smtp_url, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
            log.info("Email sent successfully")
    except Exception as e:
        log.error(f"Failed to send email: {str(e)}")

def prepare_email_content(updated_sites, failed_sites):
    email_content = []
    if updated_sites:
        updated_message = ["Sites that are updated:\n"]
        for band, urls in updated_sites.items():
            updated_message.append(f"{band}")
            for url in urls:
                updated_message.append(f" - {url}")
            updated_message.append("\n")
        updated_content = "\n".join(updated_message)
        email_content.append(("Updated Sites", updated_content))

    if failed_sites:
        failed_message = ["Sites that failed to update:\n"]
        for band, urls in failed_sites.items():
            failed_message.append(f"{band}")
            for url in urls:
                failed_message.append(f" - {url}")
            failed_message.append("\n")
        failed_content = "\n".join(failed_message)
        email_content.append(("Failed Sites", failed_content))

    return email_content

async def send_email_async(subject, body):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, send_email, subject, body)

async def main():
    total_start_time = time.time()
    timing_list = []
    updated_sites = {}
    failed_sites = {}
    log.info('Webcrawler is starting...')
    pool = await create_db_pool()
    try:
        band_data = await fetch_band_urls(pool)
        tasks = [process_band(band_id, info, pool, timing_list, updated_sites, failed_sites) for band_id, info in band_data.items()]
        await asyncio.gather(*tasks)
        total_duration = time.time() - total_start_time

        if timing_list:
            median_time = statistics.median(timing_list)
            log.info(f"Median processing time per page: {median_time:.2f} seconds.")
        log.info(f'Total execution time: {total_duration:.2f} seconds.')
        emails = prepare_email_content(updated_sites, failed_sites)
        for subject, body in emails:
            await send_email_async(subject, body)
    finally:
        await pool.close()
        log.info('Closed the database connection')
        log.info('Hibernating.')


if __name__ == '__main__':
    asyncio.run(main())
