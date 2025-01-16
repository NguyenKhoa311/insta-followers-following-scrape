import asyncio
from pyppeteer import launch
import instaloader
import requests
import time

all_following = []
all_followers = []
FOLLOWING_USERNAME_TXT = "following_usernames.txt"
FOLLOWERS_USERNAME_TXT = "followers_usernames.txt"

async def get_session_and_csrf_token():
    # Open browser
    browser = await launch(headless=False, args=['--auto-open-devtools-for-tabs'])
    page = await browser.newPage()

    # Direct to Instagram
    await page.goto('https://www.instagram.com', waitUntil='networkidle2')

    # User login manually
    print("Please login to Instagram manually.")

    def check_login_status(url):
        # Check if the URL contains the login success URL
        if 'instagram.com/accounts/' in url:
            print("Login successful.")
            return True
        return False

    # Listen for frame navigated event
    page.on('framenavigated', lambda frame: check_login_status(frame.url))

    # Wait for user to login
    while True:
        # wait for 1 second
        await asyncio.sleep(1)
        # check if login status is successful
        if check_login_status(page.url):
            break

    # get all cookies
    cookies = await page.cookies()

    # convert cookies to string
    cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    print(f"\nAll Cookies: {cookies_str}")
    
    # find csrf token in cookies
    csrf_token = None

    for cookie in cookies:
        if cookie['name'] == 'csrftoken':
            csrf_token = cookie['value']

    if csrf_token:
        print(f"CSRF Token: {csrf_token}")

    # close browser
    await browser.close()
    
    while True:
        print("Enter username to get user info (or type 'exit' to quit): ")
        username = input().strip()

        if username.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        try:
            user_info = get_user_info(username)
            if user_info:
                # Print user info
                print("User information fetched successfully:")
                print(f"User ID: {user_info['user_id']}")
                print(f"Followers: {user_info['followers']}")
                print(f"Following: {user_info['following']}")
                
                # Get info of target account
                user_id = user_info['user_id']
                following_count = user_info['following']
                break  # Exit the loop if user info is fetched successfully
        except instaloader.exceptions.LoginRequiredException:
            print("Error: Login is required to access this profile. Please check your credentials.")
        except instaloader.exceptions.ProfileNotExistsException:
            print("Error: The specified profile does not exist. Please check the username.")
        except instaloader.exceptions.InstaloaderException as e:
            print(f"An Instaloader error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        print("Please try again.")

    all_followers = get_followers(user_id, cookies_str, csrf_token)
    all_following = get_following(user_id, cookies_str, csrf_token, following_count)

    # Write data to txt file
    extract_username_to_txt(all_followers, FOLLOWERS_USERNAME_TXT)
    extract_username_to_txt(all_following, FOLLOWING_USERNAME_TXT)

def extract_username_to_txt(usernames, output_txt_file):
    try:
        # Write username to txt file
        with open(output_txt_file, 'w') as output_file:
            for index, username in enumerate(usernames, start=1):
                output_file.write(f"{index}. {username}\n")  

        print(f"Succesfully saved usernames to {output_txt_file}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Undefined error: {e}")

def get_user_info(username):
    loader = instaloader.Instaloader()

    try:
        # Login Instagram
        print("Logging in...")
        print("Enter your Instagram username: ")
        current_username = input().strip()
        print("Enter your Instagram password: ")
        password = input().strip()
        loader.login(current_username, password) 

        # Get user profile
        print(f"Fetching information for {username}...")
        profile = instaloader.Profile.from_username(loader.context, username)

        # Get user_id, followers, and following
        user_id = profile.userid
        followers = profile.followers
        following = profile.followees

        return {
            "user_id": user_id,
            "followers": followers,
            "following": following
        }

    except instaloader.exceptions.LoginRequiredException:
        print("Login required to access this profile.")
    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_followers(user_id, cookie, csrf_token, max_retries=3, timeout=10):
    all_usernames = []
    next_max_id = None  # start with no pagination
    url = f'https://www.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&search_surface=follow_list_page'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,en-US;q=0.6',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-csrftoken': csrf_token,
        'x-ig-app-id': '936619743392459',
        'x-requested-with': 'XMLHttpRequest'
    }
    unique_usernames = set()
    while True:
        try:
            # if next_max_id is not None, add it to the URL
            paginated_url = f"{url}&max_id={next_max_id}" if next_max_id else url
            print("Request URL:", paginated_url)
            retries = 0
            while retries < max_retries:
                try:
                    # Call API
                    response = requests.get(paginated_url, headers=headers, timeout=timeout)
                    
                    # Check HTTP status code
                    if response.status_code == 200:
                        print("Request successful!")
                        
                        # Parse JSON response
                        data = response.json()
                        
                        # Get usernames
                        usernames = [user.get("username") for user in data.get("users", [])]
                        all_usernames.extend(usernames)
                        
                        # Check if there is more data to fetch
                        next_max_id = data.get("next_max_id")
                        
                        # If there is no more data, return the list of usernames
                        if not next_max_id:
                            unique_usernames.update(all_usernames)
                            all_usernames = list(unique_usernames)
                            return sorted(all_usernames)  # return sorted list of usernames
                        break
                    else:
                        print(f"Request failed with status code {response.status_code}")
                        print("Response text:", response.text)
                        return None
                except requests.exceptions.ReadTimeout:
                    retries += 1
                    print(f"Read timeout occurred. Retrying {retries}/{max_retries}...")
                    time.sleep(2)  # wait for 2 seconds before retrying
                except requests.exceptions.RequestException as e:
                    print(f"Request error: {e}")
                    return None

            if retries == max_retries:
                print("Max retries reached. Exiting.")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def get_following(user_id, cookie, csrf_token, following_count):
    url = f'https://www.instagram.com/api/v1/friendships/{user_id}/following/?count={following_count}'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,en-US;q=0.6',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-csrftoken': csrf_token,
        'x-ig-app-id': '936619743392459',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        # call API
        response = requests.get(url, headers=headers)

        # Check HTTP status code
        if response.status_code == 200:
            print("Request successful!")

            # Parse JSON response
            data = response.json()
            
            # Get usernames
            return sorted([user.get("username") for user in data.get("users", [])])
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response text:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Run program
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_session_and_csrf_token())
