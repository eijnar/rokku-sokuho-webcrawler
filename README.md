# Rokku-Sokuho webcrawler
A simple webcrawler looking for changes in urls every 12 hours and emailing a list of failed and updated sites.

The webcrawler is a very tool that checks the html source code of the provided files, hashes them and saves it to the database, the next time the tool checks the current hash with the previous and if it differs adds the url to a list and then emails the list to an email address

## Installation
Currently you need to create your own environment for the script, this can be done by running `python -m venv .venv`.

Enter the new virtual environment by running `source .venv/bin/activate` and install the requirements with `pip install -r requirements.txt`

After that you should be able to run the script.

## Configuration
But before you start the script for the first time you should do some configuration. 

### Spreadsheet (.ods)
This file should be edited with the actual sites you need to monitor. It's currently a OpenDocuments spreadsheet.
The one provided only has some examples with *one address setup for failure and one that is always changing*. 

### SMTP server
You need to provide email settings in the `email_settings {}` bracket. The username is currently named `custom_sender_email` and the password is `sender_password`. 

Remember to change the `recipient_email` to the adress you would like to have the mail delivered.

_Currently only SSL accepting smtp servers are supported_

### Systemd
In order to run this at intervals i've included a sample systemd timer setting. You will need to change this to your particular setup. I will add instructions for this later, i might also add a bash script for some systems to do the installation
