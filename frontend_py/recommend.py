import streamlit as st
import requests
import json
from PIL import Image, UnidentifiedImageError
from io import BytesIO

BASE_URL = "http://127.0.0.1:6500"

def fetch_recommendations(user_message=None, image_file=None):
    url = f"{BASE_URL}/api/search"
    data = {"customer_message": user_message} if user_message else {}
    files = {}
    
    if image_file:
        files = {"file": ("image.jpg", image_file, "image/jpeg")}
    
    response = requests.post(url, data=data, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def resize_image(image_url, max_size=(150, 150)):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        img = Image.open(BytesIO(response.content))
        img.thumbnail(max_size, Image.LANCZOS)
        return img
    except (requests.RequestException, UnidentifiedImageError, IOError) as e:
        st.warning(f"Failed to load image: {e}")
        return None

def display_products(products):
    cols = st.columns(4)
    for i, product in enumerate(products):
        with cols[i % 4]:
            img = resize_image(product['image_url'])
            if img:
                st.image(img, use_column_width=True)
            else:
                st.write("Image not available")
            st.markdown(f"##### {product['prod_name']}")
            st.caption(f"{product['product_type_name']} - {product['colour_group_name']}")
            with st.expander("Details"):
                st.write(product['detail_desc'])
            st.button(f"Add to Cart", key=f"add_to_cart_{product['article_id']}")

def sidebar():
    with st.sidebar:
        st.image("../assets/banner.png", use_column_width=True)
        st.markdown("---")
        st.write("Welcome to Clozetta AI!")
        st.markdown("---")
        uploaded_file = st.file_uploader("Upload an image for visual search", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
        return uploaded_file

def fetch_with_status(message=None, image=None):
    with st.status("Processing your request...", expanded=True) as status:
        st.write("Sending request to the server...")
        response = fetch_recommendations(user_message=message, image_file=image)
        st.write("Received response from the server.")
        
        if response:
            status.update(label="Request completed successfully!", state="complete", expanded=False)
            return response
        else:
            status.update(label="Failed to fetch recommendations.", state="error", expanded=False)
            st.error("Failed to fetch recommendations. Please try again.")
            return None

def main():
    st.set_page_config(page_title="Chat and Shop", layout="wide")
    uploaded_file = sidebar()

    st.title("Chat and Shop")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None
    if "products" not in st.session_state:
        st.session_state.products = None

    # Chat input
    prompt = st.chat_input("What would you like to shop for? (Type or upload an image)")

    # Check if a new image has been uploaded
    if uploaded_file and uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.last_uploaded_file = uploaded_file
        response = fetch_with_status(image=uploaded_file.getvalue())
        if response:
            st.session_state.messages.append({"role": "assistant", "content": "Here are some recommendations based on your uploaded image:"})
            st.session_state.messages.append({"role": "assistant", "content": response["bot_message"]})
            if response["is_catalouge_changed"]:
                st.session_state.products = response["catalouge"]

    # Handle text input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if uploaded_file:
            # Combined image and text search
            response = fetch_with_status(message=prompt, image=uploaded_file.getvalue())
        else:
            # Text-only search
            response = fetch_with_status(message=prompt)
        
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response["bot_message"]})
            if response["is_catalouge_changed"]:
                st.session_state.products = response["catalouge"]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display products if available
    if st.session_state.products:
        st.subheader("Recommended Products")
        display_products(st.session_state.products)

if __name__ == "__main__":
    main()
