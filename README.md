# 📱 Instagram Followers/Following Data Scraper

A Python script that helps you extract and save data about your(friends) Instagram followers and following lists using browser automation and network request interception.

## ✨ Features

- 🔄 Call API for fetching followers, following list
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

1. Clone the project
```bash
git clone https://github.com/NguyenKhoa311/insta-followers-following-scrape
```

2. Run the script:
```bash
python scraper.py
```

3. A browser window will open automatically with Instagram's login page.

4. Log in to your Instagram account manually when prompted. Once the login is successful, the browser will close automatically.

5. Enter the username of the Instagram account you want to scrape in the terminal.

6. Enter your own Instagram account credentials in the terminal to fetch data.

## 📂 Output Files

The script generates four output files:

1. `following_usernames.txt`: Formatted list of usernames you follow
2. `followers_usernames.txt`: Formatted list of usernames following you

## 📊 File Format

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

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
