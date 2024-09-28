import streamlit as st
import http.client
import json

# Set the API key and endpoint details
API_KEY = "AIzaSyBZPwUiFYI26QA7pxYYrWW7PP5funCeKb4"
API_HOST = "www.googleapis.com"
API_PATH = "/books/v1/volumes"

# Background images for categories
category_bg_images = {
    "Fiction": "https://preview.redd.it/cxeimwflyo881.png?width=800&format=png&auto=webp&s=2160be26be2b962a1b9048c2e6236bbfe643c71c",
    "Non-fiction": "https://media.licdn.com/dms/image/C4D12AQFwd6aXpolI6g/article-cover_image-shrink_720_1280/0/1643197965018?e=2147483647&v=beta&t=8BTD0HZ0LtP1tCuOTPOKqW_x-HcrzTDWdbhfwny0wIQ",
    "Mystery": "https://t3.ftcdn.net/jpg/03/20/02/22/360_F_320022201_iskWgYQZDICRWh64UPxwyV97EBOiQS3z.jpg",
    "Science Fiction": "https://static.vecteezy.com/system/resources/previews/022/006/638/non_2x/science-background-illustration-scientific-design-flasks-glass-and-chemistry-physics-elements-generative-ai-photo.jpeg",
    "Romance": "https://t3.ftcdn.net/jpg/06/86/12/68/360_F_686126831_qzRPATjMFPDCW9S2yXRP8Rhly15FGV8H.jpg"
}

# Default background image for the app
default_bg_img = "https://t4.ftcdn.net/jpg/07/47/96/53/360_F_747965396_v8RbcQEiwiheUiY0Cn3kD5i2ZVXvWIFt.jpg"

# Function to search books using Google Books API
def search_books(query):
    conn = http.client.HTTPSConnection(API_HOST)
    request_path = f"{API_PATH}?q={query}&key={API_KEY}&maxResults=10"

    conn.request("GET", request_path)
    response = conn.getresponse()
    data = response.read().decode("utf-8")

    return json.loads(data)

# Function to display book details
def display_book_details(book):
    st.image(book.get('imageLinks', {}).get('thumbnail', ''))
    st.write(f"**Title:** {book['title']}")
    st.write(f"**Authors:** {', '.join(book.get('authors', ['Unknown']))}")
    st.write(f"**Publisher:** {book.get('publisher', 'Unknown')}")
    st.write(f"**Published Date:** {book.get('publishedDate', 'Unknown')}")
    st.write(f"**Description:** {book.get('description', 'No description available.')}")
    st.write(f"**Page Count:** {book.get('pageCount', 'Unknown')}")
    st.write(f"**Categories:** {', '.join(book.get('categories', ['Unknown']))}")
    st.write(f"**Average Rating:** {book.get('averageRating', 'N/A')}")
    st.write(f"[Read Online](https://books.google.com/books?id={book.get('id')}&printsec=frontcover&source=gbs_ViewAPI)")
    st.markdown("---")

# Function to update background based on category
def set_background_image(category=None):
    if category and category in category_bg_images:
        background_img_url = category_bg_images[category]
    else:
        background_img_url = default_bg_img

    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("{background_img_url}");
        background-size: cover;
    }}
    .stSidebar {{
        background-color: gray;
        padding: 10px;
        border-radius: 10px;
    }}
    .stSidebar h2 {{
        color: white;
        text-align: center;
        font-size: 22px;
        margin-bottom: 20px;
    }}
    .st-title {{
        color: white !important;
    }}
    .start-button {{
        display: block;
        margin: 20px auto;
        padding: 15px 30px;
        font-size: 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }}
    .start-button:hover {{
        background-color: #45a049;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app layout
def main():
    if 'start' not in st.session_state:
        st.session_state['start'] = False

    if not st.session_state['start']:
        # Opening page
        set_background_image()
        st.title("📚 Welcome to the Online Bookstore")
        st.markdown("### Start Your Reading Journey!")
        st.button("Start Your Reading Journey", key='start_button', on_click=start_reading)
    else:
        # Home page
        set_background_image()

        st.title("📚 Welcome to the Online Bookstore")
        st.markdown("Explore and purchase your favorite books or read them online!")

        # Navigation state for category
        if "category" not in st.session_state:
            st.session_state["category"] = None

        # Search bar
        query = st.text_input("Search for books by title, author, or keyword:")

        if query:
            st.markdown(f"**Results for '{query}':**")
            results = search_books(query)

            if "items" in results:
                for item in results["items"]:
                    book_info = item["volumeInfo"]
                    display_book_details(book_info)
            else:
                st.write("No books found for your search query.")

        # Sidebar navigation with gray background
        st.sidebar.markdown("<h2>Navigation</h2>", unsafe_allow_html=True)

        # Category buttons with background change
        categories = ["Fiction", "Non-fiction", "Mystery", "Science Fiction", "Romance"]
        for category in categories:
            if st.sidebar.button(category):
                st.session_state["category"] = category
                set_background_image(category)

        # Display books related to selected category
        if st.session_state["category"]:
            category = st.session_state["category"]
            st.markdown(f"**Books in '{category}' category:**")
            results = search_books(category)

            if "items" in results:
                for item in results["items"]:
                    book_info = item["volumeInfo"]
                    display_book_details(book_info)
            else:
                st.write(f"No books found for the '{category}' category.")

        st.sidebar.markdown("<p>Let us know your favorite genres, and we'll suggest books!</p>", unsafe_allow_html=True)

def start_reading():
    st.session_state['start'] = True

if __name__ == "__main__":
    main()
