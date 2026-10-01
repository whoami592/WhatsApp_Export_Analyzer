# WhatsApp Export Analyzer

A safe, offline Python GUI for analyzing **your own WhatsApp exported chat text files**. It does not access a phone, bypass encryption, read `msgstore.db.crypt*`, or recover deleted/private messages.

## Features

- Matrix-style Tkinter GUI
- Imports WhatsApp `Export chat` `.txt` files
- Handles common Android date formats and multiline messages
- Search by sender or message
- Participant/message counts and frequent words
- Export filtered results to CSV
- Works offline; standard Python library only

## Run

1. On Android WhatsApp, open your chat, tap **⋮ > More > Export chat > Without media**.
2. Copy the exported `.txt` file to your computer.
3. Install Python 3.10 or newer.
4. Open a terminal in this folder and run:

```bash
python main.py
```

No `pip install` command is required.

## Ethical use

Use only with chat data you own or have explicit permission to analyze. Keep exported chats secure because they contain private information.

**Coded by Cyber Security Engineer Mr Sabaz Ali Khan**
