# import json
# import requests
# from typing import Dict

# BASE_URL = "http://127.0.0.1:6500"

# def send_get_request(endpoint: str) -> Dict:
#     """Sends a GET request and returns the JSON response."""
#     url = f"{BASE_URL}{endpoint}"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def send_post_request(endpoint: str, payload: Dict) -> Dict:
#     """Sends a POST request and returns the JSON response."""
#     url = f"{BASE_URL}{endpoint}"
#     response = requests.post(url, json=payload)
#     response.raise_for_status()
#     return response.json()


# # PASS
# def test_get_catalogue():
#     """Test retrieving the catalogue."""
#     response = send_get_request("/api/catalouge")
#     for item in response:
#         print(item.keys())


# def test_send_only_text(text_message: str):
#     """Test sending only a text message."""
#     payload = {"customer_message": text_message}
#     response = send_post_request("/api/search", payload)
#     print("Response for Only Text:", response)

# if __name__ == '__main__':

#     print("=> Testing Catalogue")
#     test_get_catalogue()

#     print("=> Testing Text based POST Request")
#     test_send_only_text("birthday gift")


# # curl -X POST "http://127.0.0.1:6500/api/search" -F "customer_message=Show me birthday gifts"

import requests

url = "http://127.0.0.1:6500/api/search"


def only_text():
    data = {"customer_message": "show me some nike shoes"}

    response = requests.post(url, data=data)

    # Print the response from the server
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())


def only_image():
    image_path = "/home/anindya/workspace/opensource/hnm-search/tests/0108775015.jpg"

    # Prepare the data and files for the request
    data = {"customer_message": "show me similar but now red in color"}

    with open(image_path, "rb") as img:
        files = {"file": ("image.jpg", img, "image/jpeg")}
        response = requests.post(url, data=data, files=files)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())


def test_get_article(article_id):
    # Replace with your actual base URL
    base_url = "http://127.0.0.1:6500"
    url = f"{base_url}/api/article/{article_id}"
    response = requests.get(url)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except ValueError:
        print("Response Text:", response.text)


test_get_article("508942001")
