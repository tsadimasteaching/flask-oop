import requests

# Set the base URL for the JSONPlaceholder API
base_url = "https://jsonplaceholder.typicode.com"

def get_user_data(user_id):
    # Make a GET request to retrieve user data
    response = requests.get(f"{base_url}/users/{user_id}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        user_data = response.json()
        print(user_data)
        print(f"User Data for User ID {user_id}:")
        print(f"Name: {user_data['name']}")
        print(f"Email: {user_data['email']}")
        print(f"Phone: {user_data['phone']}")
    else:
        print(f"Failed to retrieve user data. Status code: {response.status_code}")

def get_posts_by_user(user_id):
    # Make a GET request to retrieve posts by a specific user
    response = requests.get(f"{base_url}/users/{user_id}/posts")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        posts = response.json()
        print(f"Posts by User ID {user_id}:")
        for post in posts:
            print(f"Title: {post['title']}")
            print(f"Body: {post['body']}")
            print("------")
    else:
        print(f"Failed to retrieve posts. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example: Get user data for user with ID 1
    get_user_data(1)

    # Example: Get posts by user with ID 1
    get_posts_by_user(1)
