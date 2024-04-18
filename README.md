# Rokku-Sokuho webcrawler
A simple webcrawler looking for changes in urls every 12 hours and emailing a list of failed and updated sites.

The webcrawler is a very tool that checks the html source code of the provided files, hashes them and saves it to the database, the next time the tool checks the current hash with the previous and if it differs adds the url to a list and then emails the list to an email address

## Installation
First you need to add two .env files. One in the frontend directory and one in the webcrawler.

Frontend only needs `DATABASE_URL`. Currently only postgresql is supported but install any driver and setup this as you like

Webcrawler needs a bit more:
```bash
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_HOST=
DB_PORT=

MAIL_SENDER=
MAIL_PASSWORD=
MAIL_TO=
MAIL_SMTP=
MAIL_PORT=
```

After this you should be able to run the `install.sh` script (untested on a real linux machine when writing). 


### Systemd
The installation script installs three files under the users systemd and enable linger.

## Gunicorn

The default port is 8000. Use it!
