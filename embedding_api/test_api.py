import requests
import json

# The base URL of your FastAPI server
BASE_URL = "https://4630-27-4-59-166.ngrok-free.app"

def test_embedding_api():
    # Test query
    query = "Hello, world!"
    
    # Send GET request to the /api/embedding endpoint
    response = requests.get(f"{BASE_URL}/api/embedding", params={"query": query})
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        data = response.json()
        print("Status:", data["status"])
        print(eval(data["embedding"]))
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    test_embedding_api()
