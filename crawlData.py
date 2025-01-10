import asyncio
from pyppeteer import launch
import json

all_following = []
all_followers = []
FOLLOWING_JSON_FILE = "following_response_body.json"
FOLLOWERS_JSON_FILE = "followers_response_body.json"
FOLLOWING_USERNAME_TXT = "following_usernames.txt"
FOLLOWERS_USERNAME_TXT = "followers_usernames.txt"

async def intercept_requests():
    # Setup and run browser
    browser = await launch(headless=False, args=['--auto-open-devtools-for-tabs'])
    page = await browser.newPage()

    # Connect to DevTools Protocol
    client = await page.target.createCDPSession()

    # # Enable the network domain to intercept and handle network requests
    await client.send('Network.enable')

    # list of requests captured
    captured_requests = []

    # Listen responseReceived event from client
    client.on('Network.responseReceived', lambda response: asyncio.ensure_future(process_response(response, captured_requests, client)))

    # Go to Instagram 
    await page.goto('https://www.instagram.com', waitUntil='networkidle2')

    # Wait for user login and open necessary tabs
    print("Please login.")
    
    # Wait until user closes the browser
    await wait_for_browser_close(browser)

    # Handle data
    write_into_json_file(FOLLOWERS_JSON_FILE, all_followers)
    write_into_json_file(FOLLOWING_JSON_FILE, all_following)
    extract_username_to_txt(FOLLOWERS_JSON_FILE, FOLLOWERS_USERNAME_TXT)
    extract_username_to_txt(FOLLOWING_JSON_FILE, FOLLOWING_USERNAME_TXT)


async def process_response(response, captured_requests, client):
    global all_following, all_followers  # global variables to store users.

    # handling response and request
    request_url = response['response']['url']
    
    if "following/?count=12" in request_url:
        print(f"Captured Request (Following): {request_url}")

        # Get response body
        try:
            response_body = await client.send('Network.getResponseBody', {'requestId': response['requestId']})
            body = response_body.get('body', '')
            decoded_body = body.encode('utf-8').decode('unicode_escape')
            body_data = json.loads(decoded_body)

            # Extract users and add to all_following
            users = body_data.get('users', [])
            all_following.extend(users)  # add to all_following

        except Exception as e:
            print(f"Lỗi khi lấy response body: {e}")

    elif "followers/?count=12" in request_url:
        print(f"Captured Request (Followers): {request_url}")

        # Get response body
        try:
            response_body = await client.send('Network.getResponseBody', {'requestId': response['requestId']})
            body = response_body.get('body', '')
            decoded_body = body.encode('utf-8').decode('unicode_escape')
            body_data = json.loads(decoded_body)

            # Extract users and add to all_followers
            users = body_data.get('users', [])
            all_followers.extend(users)  # add to all_followers

        except Exception as e:
            print(f"Lỗi khi lấy response body: {e}")


async def wait_for_browser_close(browser):
    # Listen on closing browser event
    while True:
        pages = await browser.pages()
        if not pages:
            break
        await asyncio.sleep(1)  # Recheck after 1s

def write_into_json_file(json_file, user_list):
    with open(json_file, 'w') as f:
        json.dump({"users": user_list}, f, indent=4)

def extract_username_to_txt(json_file, output_txt_file):
    try:
        # Open and read json file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Get all users
        users = data.get('users', []) 

        # Extract username
        user_names = [user['username'] for user in users]

        # Write username to txt file
        with open(output_txt_file, 'w') as output_file:
            for index, username in enumerate(user_names, start=1):
                output_file.write(f"{index}. {username}\n")  

        print(f"Succesfully saved usernames to {output_txt_file}")
    except FileNotFoundError:
        print(f"Error: File not found {json_file}")
    except json.JSONDecodeError:
        print(f"Error: File {json_file} is not a valid json file")
    except Exception as e:
        print(f"Undefined error: {e}")

# Run program
asyncio.get_event_loop().run_until_complete(intercept_requests())
