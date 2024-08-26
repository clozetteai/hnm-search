import json 
import requests

BASE_URL = "http://127.0.0.1:6500"
image_path = "/home/anindya/workspace/opensource/hnm-search/tests/test_image.jpg"

def test_only_test():
    data = {
        "customer_message": "show me some nike shoes"
    }
    url = f"{BASE_URL}/api/search"
    response = requests.post(url, data=data)
    print(json.dumps(response.json(), indent=4))

def test_only_image():
    url = f"{BASE_URL}/api/search"
    data = {"customer_message": None}

    with open(image_path, "rb") as img:
        files = {"file": ("image.jpg", img, "image/jpeg")}
        response = requests.post(url, data=data, files=files)
    print(response.status_code)


def test_both_image_and_text():
    data = {
        "customer_message": "show me some nike shoes"
    }
    url = f"{BASE_URL}/api/search"
    with open(image_path, "rb") as img:
        files = {"file": ("image.jpg", img, "image/jpeg")}
        response = requests.post(url, data=data, files=files)
    print(response.status_code)


def test_get_catalogue():
    url = f"{BASE_URL}/api/catalouge"
    response = requests.get(url)
    print(response.status_code)
    print(json.dumps(response.json(), indent=4))


def test_article_info():
    url = f"{BASE_URL}/api/article/508942001"
    response = requests.get(url)
    print(response.status_code)


if __name__ == '__main__':
    print("=> Testing Only Text")
    test_only_test()
    # print("=> Testing Only Image")
    # test_only_image()
    # print("=> Testing Both Image and Text")
    # test_both_image_and_text()
    # print("=> Testing Catalogue")
    # test_get_catalogue()
    # print("=> Testing Article Info")
    # test_article_info()
