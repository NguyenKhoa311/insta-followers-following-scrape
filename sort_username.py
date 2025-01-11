FOLLOWING_USERNAME_TXT = "following_usernames.txt"
FOLLOWERS_USERNAME_TXT = "followers_usernames.txt"

def sort_usernames(file_path):
    try:
        # Read file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Handle white space and sort
        users = [line.strip() for line in lines if line.strip()]  # remove white space
        sorted_users = sorted(users, key=lambda x: x.split('. ', 1)[-1].lower())  # sort username by alphabetical order

        # Overwrite into file
        with open(file_path, 'w') as file:
            for index, user in enumerate(sorted_users, start=1):
                file.write(f"{index}. {user.split('. ', 1)[-1]}\n")

        print(f"File '{file_path}' has been sorted alphabetically.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


sort_usernames(FOLLOWERS_USERNAME_TXT)
sort_usernames(FOLLOWING_USERNAME_TXT)