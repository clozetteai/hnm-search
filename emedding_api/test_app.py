import base64
import requests

BASE_URL = "https://4630-27-4-59-166.ngrok-free.app"


def test_embedding_api():
    query = "Hello, world!"
    response = requests.get(f"{BASE_URL}/api/text_embedding", params={"query": query})

    if response.status_code == 200:
        print("Request successful!")
        data = response.json()
        print("Status:", data["status"])
        print(len(eval(data["embedding"])))
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)


def test_image_embedding_api():
    image_path = "0108775015.jpg"

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_bs64 = base64.b64encode(image_bytes).decode("utf-8")
    payload = {"image_bs64": image_bs64}

    response = requests.post(f"{BASE_URL}/api/image_embedding", json=payload)

    if response.status_code == 200:
        print("Request successful!")
        data = response.json()
        print("Status:", data["status"])
        print(len(eval(data["embedding"])))
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    test_embedding_api()
    test_image_embedding_api()
