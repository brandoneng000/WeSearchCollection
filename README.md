# WeSearchCollection

Creates collection and uploads 1000 random documents from a zip file into it.
Also states how many documents failed to ingest.
User may also delete the entire collection if necessary.

## Installation

Install [python](https://www.python.org/)

Use `pip install -r requirements.txt` to install libraries

## Config

User should create `.env` file in directory.
```
EMAIL=user_email
PASS=user_password
COLLECTION=collection_name
ZIPFILE=zip_file
```