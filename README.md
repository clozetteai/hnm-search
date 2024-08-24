# Clozette.AI
![1](https://github.com/user-attachments/assets/aa076e15-b902-4d57-a3b1-ae9543d812fc)


**Clozette.AI**: We speak SQL, so you can speak fashion! 😝 We translate your clothing descriptions into database queries, making it easier than ever to find the perfect outfit.

## Creators

- [Siddhant Prateek Mahanayak](https://github.com/siddhantprateek)
- [Anindyadeep](https://github.com/Anindyadeep)
- [Pratyush Patnaik](https://github.com/Pratyush-exe)

## Overview
![5](https://github.com/user-attachments/assets/dda6c3f4-2cdc-4a0d-92ac-727046c44dac)

## Setting Up the Backend

To set up the backend, you need to first create an environment and install the requirements from the provided file:

```bash
cd backend
pip install -r requirements.txt
```

**NOTE**: Ensure you gather all the credentials shown in `backend/.env.template` and create a `.env` file in the `backend` directory.

Next, download all the assets from this [Google Drive link](https://drive.google.com/file/d/1OW_y8LNPishXXNOetkHR3ATC6rCm8R1u/view?usp=sharing) and place them in the `backend/assets` folder. Unzip the downloaded file inside this folder, then delete the zip file.

For a sanity check, you can run the following command to ensure the server is running:

```bash
# In the ./backend directory run:
uvicorn main:app --reload --port 7600

# Then, test the server by running the following command:

cd tests
pytest test_backend.py
```

## Using the API

Currently, there are two hosted API servers. One of them is the embedding service and full-backend logic, where as the other is as a image-file storage system

You don't need to do anything with this. To interact with the backend, run the backend server on your local machine and use the following base URL.

### Python Integration Guide

To interact with the API using Python, follow these steps:

#### Prerequisites

Ensure you have the `requests` library installed:

```bash
pip install requests
```

#### Step 1: Send a POST Request with Text Only

**Python:**

```python
import requests

BASE_URL = "http://127.0.0.1:7600"
payload = {"customer_message": "birthday gift for my baby boy"}
response = requests.post(f"{BASE_URL}/api/search", json=payload)
print(response.json())
```

**cURL:**

```bash
curl -X POST "http://127.0.0.1:7600/api/search" \
-H "Content-Type: application/json" \
-d '{"customer_message": "birthday gift for my baby boy"}'
```

#### Step 2: Send a POST Request with Image Only

**Python:**

```python
payload = {"attached_image": image_base64}
response = requests.post(f"{BASE_URL}/api/search", json=payload)
print(response.json())
```

**cURL:**

```bash
curl -X POST "http://127.0.0.1:7600/api/search" \
-H "Content-Type: application/json" \
-d '{"attached_image": "<image_base64>"}'
```

#### Step 3: Send a POST Request with Both Image and Text

**Python:**

```python
payload = {
    "customer_message": "birthday gift for my baby boy",
    "attached_image": image_base64
}
response = requests.post(f"{BASE_URL}/api/search", json=payload)
print(response.json())
```

**cURL:**

```bash
curl -X POST "http://127.0.0.1:7600/api/search" \
-H "Content-Type: application/json" \
-d '{"customer_message": "birthday gift for my baby boy", "attached_image": "<image_base64>"}'
```

#### Step 4: Retrieve the Catalogue with a GET Request

**Python:**

```python
response = requests.get(f"{BASE_URL}/api/catalogue")
print(response.json())
```

**cURL:**

```bash
curl -X GET "http://127.0.0.1:7600/api/catalogue"
```

---
