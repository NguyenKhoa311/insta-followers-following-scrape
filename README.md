# 📱 Instagram Followers/Following Data Extractor

A Python script that helps you extract and save data about your(friends) Instagram followers and following lists using browser automation and network request interception.

## ✨ Features

- 🔄 Automatically captures Instagram followers and following data
- 💾 Saves raw data in JSON format
- 📄 Exports usernames to formatted text files

## 📋 Prerequisites

To run this script, you need to have the following installed:
- Python 3.7+
- pyppeteer
- asyncio

Install the required packages using pip:
```bash
pip install pyppeteer asyncio
```

## 🚀 Usage

1. Run the script:
```bash
python scraper.py
```

2. A browser window will open automatically with Instagram's login page.

3. Log in to your Instagram account manually when prompted.

4. Navigate to your profile and open your followers/following lists.

5. Scroll through the lists to load all data.

6. Close the browser window when you're done to process the collected data.

## 📂 Output Files

The script generates four output files:

1. `following_response_body.json`: Raw JSON data of all following accounts
2. `followers_response_body.json`: Raw JSON data of all followers accounts
3. `following_usernames.txt`: Formatted list of usernames you follow
4. `followers_usernames.txt`: Formatted list of usernames following you

## 📊 File Format

### 📝 JSON Files
The JSON files contain detailed information about each user in the following format:
```json
{
    "users": [
        {
            "username": "example_user",
            ...other user data
        }
    ]
}
```

### 📜 Text Files
The text files contain numbered lists of usernames:
```
1. username1
2. username2
3. username3
```

## ⚡ Limitations

- Requires manual login
- Depends on Instagram's web interface
- Network request patterns may change if Instagram updates their API
- Browser must remain open during data collection

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
