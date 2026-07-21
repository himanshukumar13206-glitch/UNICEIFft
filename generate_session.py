"""
Run this ONCE locally to generate SESSION_STRING for your assistant account.
This account (a normal Telegram user, not the bot) is what actually joins
the voice chat and streams audio.

    python3 generate_session.py

Log in with the phone number of the account you want to use as the
assistant, then copy the printed string into your .env / Render env vars.
"""

from pyrogram import Client

API_ID = int(input("Enter your API_ID: "))
API_HASH = input("Enter your API_HASH: ").strip()

with Client("assistant_session_gen", api_id=API_ID, api_hash=API_HASH, in_memory=True) as app:
    print("\n--- SESSION_STRING (keep this secret!) ---\n")
    print(app.export_session_string())
    print("\n--------------------------------------------\n")
