# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

import requests
import base64
from typing import Optional, Dict

# Base API endpoint
BASE_URL = "http://127.0.0.1:7600" #"https://9baf-115-99-140-3.ngrok-free.app"

def encode_image_to_base64(image_path: str) -> str:
    """Encodes an image to a base64 string."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode("utf-8")

def send_post_request(endpoint: str, payload: Dict) -> Dict:
    """Sends a POST request and returns the JSON response."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def send_get_request(endpoint: str) -> Dict:
    """Sends a GET request and returns the JSON response."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def test_send_only_text(text_message: str):
    """Test sending only a text message."""
    payload = {"customer_message": text_message}
    response = send_post_request("/api/search", payload)
    print("Response for Only Text:", response)

def test_send_only_image(image_path: str):
    """Test sending only an image."""
    image_base64 = encode_image_to_base64(image_path)
    payload = {"attached_image": image_base64}
    response = send_post_request("/api/search", payload)
    print("Response for Only Image:", response)

def test_send_image_and_text(image_path: str, text_message: str):
    """Test sending both image and text."""
    image_base64 = encode_image_to_base64(image_path)
    payload = {
        "customer_message": text_message,
        "attached_image": image_base64
    }
    response = send_post_request("/api/search", payload)
    print("Response for Image + Text:", response)

def test_get_catalogue():
    """Test retrieving the catalogue."""
    response = send_get_request("/api/catalouge")
    for item in response:
        print(f"Article ID: {item['article_id']}")
        print(f"Image Base64: {item['image']}")

if __name__ == "__main__":
    # Path to your test image
    image_path = "./backend/assets/0309434009.jpg"
    text_message = "birthday gift for my baby boy"

    # Run the tests
    print("Testing only text...")
    test_send_only_text(text_message)
    
    print("\nTesting only image...")
    test_send_only_image(image_path)
    
    print("\nTesting image and text...")
    test_send_image_and_text(image_path, text_message)
    
    print("\nTesting catalogue retrieval...")
    test_get_catalogue()
