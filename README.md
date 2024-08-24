# Clozette.Ai

![](./assets/banner.png)

**Clozette.AI** we speak SQL, so you can speak fashion 😝. We translate your clothing descriptions into database queries, making it easier than ever to find the perfect outfit.

## Creators

- [Siddhant Prateek Mahanayak](https://github.com/siddhantprateek)
- [Anindyadeep](https://github.com/Anindyadeep)
- [Pratyush Patnaik](https://github.com/Pratyush-exe)


## Setting up the backend

To set up the backend you need to first create an environment
and install the requirements file. 

```
cd backend
pip install -r requirements.txt
```

**NOTE**: You should gather all the credentials show in `backend/.env.template` and create a `.env` file in the `backend` directory. 

Download all the assets from this [google drive link](https://drive.google.com/file/d/1OW_y8LNPishXXNOetkHR3ATC6rCm8R1u/view?usp=sharing) and place them in the `backend/assets` folder. After this paste this inside the `backend/assets` folder. Now unzip it inside the folder and you can delete the zip file.



For a sanity check, you can run the following command to see if the server is running.

```
# in the ./backend directory run:
uvicorn main:app --reload --port 7600

# And then test the runs by running the following command:

cd tests
pytest test_backend.py
```

## Using the API

For now there are two hosted API servers. One of them is the embedding service which is running on my device. Here is the base URL for that. 

```
https://4630-27-4-59-166.ngrok-free.app
```

You do not need to anything with this. To interact with backend, run the backend server on your local machine and use the following base URL.


### Python Integration Guide

To interact with the API using Python, follow these steps:

#### Prerequisites
- Ensure you have the `requests` library installed:

  ```bash
  pip install requests
  ```

#### Step 1: Send a POST Request with Text Only

```python
import requests

BASE_URL = "http://127.0.0.1:7600"
payload = {"customer_message": "birthday gift for my baby boy"}
response = requests.post(f"{BASE_URL}/api/search", json=payload)
print(response.json())
```

#### Step 2: Send a POST Request with Image Only

```python
payload = {"attached_image": image_base64}
response = requests.post(f"{BASE_URL}/api/search", json=payload)
print(response.json())
```

#### Step 3: Send a POST Request with Both Image and Text

```python
payload = {
    "customer_message": "birthday gift for my baby boy",
    "attached_image": image_base64
}
response = requests.post(f"{BASE_URL}/api/search", json=payload)
print(response.json())
```

#### Step 4: Retrieve the Catalogue with a GET Request

```python
response = requests.get(f"{BASE_URL}/api/catalouge")
print(response.json())
```
