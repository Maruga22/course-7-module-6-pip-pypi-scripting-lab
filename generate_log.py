from datetime import datetime

import requests


def fetch_data(url="https://jsonplaceholder.typicode.com/posts/1"):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def write_log(data):
    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"

    with open(filename, "w") as file:
        for entry in data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename


def generate_log(data):
    if not isinstance(data, list):
        raise ValueError("data must be a list")

    return write_log(data)


def main():
    try:
        post = fetch_data()
        print("Fetched Post Title:", post.get("title", "No title found"))
        log_data = [
            "User logged in",
            "User updated profile",
            "Report exported",
            f"Fetched post title: {post.get('title', 'No title found')}",
        ]
    except requests.RequestException as error:
        print(f"API request failed: {error}")
        log_data = ["User logged in", "User updated profile", "Report exported"]

    generate_log(log_data)


if __name__ == "__main__":
    main()
