import streamlit as st
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

# Define the function to fetch services from the API
def fetch_services():
    url = "https://dangi-olive.vercel.app/fetch-services"
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        services = response.json()
        return services
    else:
        return []

# Other function definitions (api_register, api_login, api_form) are assumed to be defined

# Initialize session state for login status and selected service category
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'selected_service_category' not in st.session_state:
    st.session_state['selected_service_category'] = "Home"

# Define categories for services
service_categories = ["Instagram Services", "YouTube Services", "Twitter Services",
                      "Facebook Services", "Telegram Services", "TikTok Services"]

# Sidebar for navigation
with st.sidebar:
    st.title("Menu")
    # Login and Register options
    if st.button("Login"):
        st.session_state['selected_service_category'] = "Login"
    if st.button("Register"):
        st.session_state['selected_service_category'] = "Register"
    
    st.title("Services")
    # Dynamically create buttons for each service category
    for category in service_categories:
        if st.button(category):
            st.session_state['selected_service_category'] = category

# Display logic based on selected category or page
if st.session_state['selected_service_category'] == "Login":
    # Include your login functionality here
    pass  # Placeholder for your login code
elif st.session_state['selected_service_category'] == "Register":
    # Include your registration functionality here
    pass  # Placeholder for your registration code
elif st.session_state['selected_service_category'] in service_categories:
    if st.session_state['logged_in']:
        selected_category = st.session_state['selected_service_category']
        services = fetch_services()
        
        # Filter services based on the selected category
        category_services = [service for service in services if selected_category.split(' ')[0].lower() in service['name'].lower()]
        
        st.title(f"{selected_category}")
        for service in category_services:
            st.markdown(f"**Service Name:** {service['name']} - **Price:** {service['rate']}")
    else:
        st.error("You are not logged in. Please login to access the services.")
else:
    st.write("Home Page or other content")

# Note: Placeholder comments should be replaced with your actual login, registration, and content display logic.
