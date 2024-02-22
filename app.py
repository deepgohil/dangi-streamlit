import streamlit as st
from streamlit_option_menu import option_menu  # You might need to install this package
import requests

st.set_page_config(page_title="Page Title", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)


def fetch_services():
    # API endpoint for fetching services
    url = "https://dangi-steel.vercel.app/fetch-services"
    
    # Headers
    headers = {'accept': 'application/json'}
    
    # Making the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Assuming a successful response returns a 200 status code
        # Extract the services from the response
        services = response.json()
        return services
    else:
        # Request failed
        return []

# Function to handle registration
def api_register(username, password, phone):
    # API endpoint
    url = "https://dangi-steel.vercel.app/register"
    
    # Headers and payload
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    payload = {"username": username, "password": password, "phone": phone}
    
    # Making the POST request
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Assuming successful registration returns a 200 status code
        username = response.json().get('username')
        return True
    else:
        # Registration failed
        return False

# Mock function for API login call (replace with your actual API calls)
def api_login(username, password):
    # API endpoint for login
    url = "https://dangi-steel.vercel.app/token"
    
    # Headers and payload
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': '',  # Fill in if your API requires a specific grant type
        'username': username,
        'password': password,
        'scope': '',  # Fill in if your API requires a scope
        'client_id': '',  # Fill in if your API requires a client_id
        'client_secret': '',  # Fill in if your API requires a client_secret
    }
    
    # Making the POST request
    response = requests.post(url, data=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Assuming a successful login returns a 200 status code
        # Extract the access token from the response
        access_token = response.json().get('access_token')
        username = response.json().get('username')
        if access_token:
            # Store the access token in the session state for later use (optional)
            st.session_state['access_token'] = access_token
            return True
    # Login failed
    return False

def api_form(username, email, password):
    # The URL of the FastAPI endpoint
    url = "https://dangi-steel.vercel.app/create-order"  # Change this URL to your FastAPI server URL
    
    # Query parameters
    params = {
        'username': str(username),
        'email': str(email),
        'password': str(password)
    }
    
    # Making the GET request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Assuming a successful request returns a 200 status code
        print("Registration Successful")
        # Print the response JSON, or handle it as needed
        print(response.json())
        return True
    else:
        # Request failed
        print("Registration Failed")
        print(response.text)
        return False

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'navigate_to_home' not in st.session_state:
    st.session_state['navigate_to_home'] = False

# Sidebar for navigation
with st.sidebar:
    selected = option_menu("boostallsocials", ["Login", "Register", "Home"], 
                           icons=['house', 'book', 'gear'], menu_icon="instagram", default_index=2)

# Login Page
if selected == "Login":
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if api_login(username, password):
            st.session_state['logged_in'] = True
            # st.session_state['navigate_to_home'] = True  # Navigate to Home page after login
            st.success("You are now loged in go to Home tab")
            # st.experimental_rerun()
        else:
            st.error("Login failed. Please check your username and password.")

# Register Page
elif selected == "Register":
    st.title("Register")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone")
    
    if st.button("Register"):
        if api_register(username, password, phone):
            st.session_state['logged_in'] = True
            # st.session_state['navigate_to_home'] = True  # Navigate to Home page after registration
            st.success("You are now loged in go to Home tab")
            # st.experimental_rerun()
        else:
            st.error("Registration failed. Please try a different username.")

# Home Page
elif selected == "Home" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+service['rate'] for service in services]  # Extract service names
        


        # Form with URL, Quantity, and Service
        with st.form("my_form"):
            st.markdown("""
            <style>
            div.stSelectbox > div > div > select {
                padding: 10px;  /* Increase padding */
            }
            </style>
            """, unsafe_allow_html=True)

            service = st.selectbox("Service", service_names)
            quantity = st.number_input("Quantity", min_value=100)            
            url = st.text_input("URL")
            service_rate = None
            for service_ in services:
            
                if service_["name"] == service:
                        service_id = service_["rate"]
                        break
            if service_rate is not None:
                st.text(f"Service Rate: {service_rate}")
            else:
                st.text("Select a service to see its rate.")


            submitted = st.form_submit_button("Submit")
            if submitted:
                service=service.split(',')
                service_id = None
                for service_ in services:
                    if service_["name"] == service[0]:
                        service_id = service_["service"]
                        break
                # print(service_id)

                if api_form(service_id, quantity, url):  # Call api_form and check its return value
                    st.success("Your order is placed")  # Show success message
                else:
                    st.error("Operation failed.")

        

        balance = "Your balance is $100"  # Call fetch_balance() if fetching from an API
        st.text(balance)  # Displaying the balance as text
        
       
        photo_url = 'https://audiodeepfile.s3.ap-south-1.amazonaws.com/desktopqrcode.jpeg'  # Replace with actual URL or file path
        st.image(photo_url, caption='This is your QR code for adding money')  # Displaying the photo with a caption
                
    else:
        st.error("You are not logged in. Please login to access the home page.")

