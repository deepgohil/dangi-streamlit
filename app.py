import streamlit as st
from streamlit_option_menu import option_menu  
import requests


MY_BALANCE=0
MY_USERNAME=""
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

def add_money(username, transaction_id, amount):
    # Endpoint for adding money
    url = "https://dangi-olive.vercel.app/add-money"
    
    # Payload to be sent in the POST request
    payload = {
        "username": username,
        "transactionId": transaction_id,
        "amount": amount
    }
    
    # Headers to indicate JSON content
    headers = {'Content-Type': 'application/json'}
    
    # Sending the POST request
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the new balance from the response
        new_balance = response.json().get('new_balance', '0')
        
        # Update session state with the new balance
        st.session_state['balance'] = new_balance
        
        # Optionally, display a success message with the new balance
        st.success(f"Money added successfully. New balance: ${new_balance}")
    else:
        # If the request failed, display an error message
        st.error("Failed to add money. Please try again.")

def fetch_services():
    # API endpoint for fetching services
    url = "https://dangi-olive.vercel.app/fetch-services"
    
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


def update_balance(username):
    # Endpoint for fetching balance
    url = f"https://dangi-olive.vercel.app/fetch-balance?username={username}"

    try:
        # Send GET request to the endpoint
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract balance from the response
            response_data = response.json()
            balance = response_data.get('balance', '0')

            # Update session state with the new balance
            st.session_state['balance'] = balance

            # Optionally, return balance if you want to use it immediately
            return balance
        else:
            st.error("Failed to fetch balance. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")





# Function to handle registration
def api_register(username, password, phone):
    # API endpoint
    url = "https://dangi-olive.vercel.app/register"
    
    # Headers and payload
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    payload = {"username": username, "password": password, "phone": phone}
    
    # Making the POST request
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Assuming successful registration returns a 200 status code
        response_data = response.json()
        print(username)
        if 'balance' in response_data:
            st.session_state['balance'] = response_data['balance']
            st.session_state['username'] = response_data['username']
            print(f"New Balance: {st.session_state['balance']}")
        return True
    else:
        # Registration failed
        return False

    
def api_login(username, password):
    # API endpoint for login
    url = "https://dangi-olive.vercel.app/token"
    
    # Headers and payload
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        # Fill in as required by your API
        'username': username,
        'password': password,
    }
    
    # Making the POST request
    response = requests.post(url, data=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the access token and other details from the response
        response_data = response.json()
        access_token = response_data.get('access_token')
        balance = response_data.get('balance')
        
        # Update session state
        st.session_state['access_token'] = access_token
        st.session_state['username'] = username
        st.session_state['balance'] = balance
        
        return True
    # Login failed
    return False


def api_form(username, quantity, url,price):
    api_url = "https://dangi-olive.vercel.app/create-order"  
    if float(st.session_state['balance']) < 5:
                st.error("Your balance is less thanPlease add funds.")
                return
    # Assuming 'username' is the service ID for the sake of this example. Adjust accordingly.
    params = {
        'service_id': username,
        'quantity': quantity,
        'link': url
    }
    print(price)
    try:
        # Sending the GET request to the /create-order endpoint
        response = requests.get(api_url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Assuming the response body contains JSON
            response_data = response.json()
            
            # You might want to do something with the response data, e.g., displaying the order details
            st.success(f"Order created successfully: order ID is {response_data['order']['order_id']}")
            
            # Optionally, return the response data if you want to use it further
            return response_data
        else:
            # Handle responses with error status codes
            st.error(f"Failed to create order. Status code: {response.status_code}")
    except Exception as e:
        # Handle any errors that occur during the request sending process
        st.error(f"An error occurred: {str(e)}")


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'navigate_to_home' not in st.session_state:
    st.session_state['navigate_to_home'] = False

# Sidebar for navigation
with st.sidebar:
    selected = option_menu("boostallsocials", ["Login", "Register", "Home","Instagram Services","YouTube Services","Twitter Services","Facebook Services","Telegram Services","TikTok Services","Add money"], 
                           icons=['house', 'book', 'gear', 'camera', 'film', 'twitter','tablet', 'send', 'music-note','piggy-bank'], menu_icon="instagram", default_index=2)

# Login Page
if selected == "Login":
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if api_login(username, password):
            st.session_state['logged_in'] = True
            # st.session_state['navigate_to_home'] = True  # Navigate to Home page after login
            st.success("You are now loged in go to Home tab (Just to check you are human 🤖)")
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
            st.success("You are now loged in go to Home tab (Just to check you are human 🤖)")
            # st.experimental_rerun()
        else:
            st.error("Registration failed. Please try a different username.")

# Home Page
elif selected == "Home" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        st.text(f"Username: {st.session_state.get('username', '')}")
        st.text(f"Balance: {st.session_state.get('balance', '0')}")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  


        categories = {'Instagram': [], 'YouTube': [], 'Twitter': [],'Facebook':[],'Telegram':[],'TikTok':[]}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
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
            st.success(service)
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
                price = None
                
                for service_ in services:
                    if service_["name"] == service[0]:
                        service_id = service_["service"]
                        price = float(service_["rate"])*1.20
                        break
                # print(service_id)

                if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                    st.success("Your order is placed")  # Show success message
                else:
                    st.error("Operation failed.")

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")

elif selected == "Instagram Services" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
        categories = {'Instagram': []}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
       

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")
elif selected == "YouTube Services" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
        categories = {'YouTube': []}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
       

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")
elif selected == "Twitter Services" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
        categories = {'Twitter': []}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
       

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")
elif selected == "Facebook Services" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
        categories = {'Facebook': []}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
       

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")
elif selected == "Telegram Services" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
        categories = {'Telegram': []}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
       

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")


elif selected == "TikTok Services" or st.session_state['navigate_to_home']:
    if st.session_state['logged_in']:
        st.session_state['navigate_to_home'] = False  # Reset navigation flag
        st.title("Welcome ")
        services = fetch_services()
        service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
        categories = {'TikTok': []}
        for service in services:
            for category in categories:
                if category.lower() in service['name'].lower():
                    categories[category].append(service)
       

        for category, services in categories.items():
            if services:  # Only create a form if there are services in the category
                with st.form(f"{category}_form"):
                    st.subheader(f"{category} Services")
                    service_names = [service['name']+", Price "+str(float(service['rate'])*1.20) for service in services]  
                    selected_service = st.selectbox(f"Select a {category} Service", service_names, key=f"{category}_service")
                    st.success(selected_service)
                    quantity = st.number_input("Quantity", min_value=100, key=f"{category}_quantity")
                    url = st.text_input("URL", key=f"{category}_url")

                    # Find the ID of the selected service
                    selected_service_id = next((service['service'] for service in services if service['name'] == selected_service), None)

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        # Extract service ID from the selected service option
                        selected_service_details = selected_service.split(', Price ')
                        service_name = selected_service_details[0]
                        service_id = next((service['service'] for service in services if service['name'] == service_name), None)
                        price = next((float(service['rate'])*1.20 for service in services if service['name'] == service_name), None)
                        
                        if service_id:
                            if api_form(service_id, quantity, url,price):  # Call api_form and check its return value
                                st.success("Your order is placed")  # Show success message
                            else:
                                st.error("Operation failed.")


       
    else:
        st.error("You are not logged in. Please login to access the home page.(click on top right corner)")

if selected == "Add money":
    if st.session_state.get('logged_in', False):
        username = st.session_state.get('username', '')

        st.title("Add Money to Your Account")
        st.text(f"Current Balance: {st.session_state.get('balance', '0')}")

        # Input for Transaction ID
        transaction_id = st.text_input("Transaction ID")

        # Input for Amount
        amount = st.number_input("Amount", min_value=20)

        # Submit Button
        if st.button("Add Money"):
            # Call the add_money function with inputs
            add_money(username, transaction_id, amount)
    else:
        st.error("You are not logged in. Please login to access the Add Money page.")

    # HTML payment page logic
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            .payment-container {
                background-color: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            h1 {
                color: #333;
            }
            input[type="number"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .pay-button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .pay-button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="payment-container">
            <h1>Pay Now</h1>
            <input type="number" id="amount" placeholder="Enter amount in Rs" min="1" step="1">
            <button class="pay-button" onclick="initiatePayment()">Pay Now</button>
        </div>

        <script>
            function initiatePayment() {
                var amount = document.getElementById('amount').value;
                if (!amount || amount <= 0) {
                    alert("Please enter a valid amount.");
                    return;
                }

                // Replace '1234567890' with the actual phone number you want to receive payments to
                var phoneNumber = '1234567890';
                
                // Construct the UPI link with the phone number
                var upiLink = `upi://pay?pa=${phoneNumber}@upi&pn=Recipient%20Name&am=${amount}.00&cu=INR&tn=Payment%20for%20Service`;
                
                // Attempt to open the UPI link
                window.location.href = upiLink;

                // Set a timeout to check if the payment was successful
                setTimeout(function() {
                    var paymentSuccessful = confirm("Was the payment successful?");

                }, 5000); // Wait for 5 seconds before asking
            }
        </script>
    </body>
    </html>
    """

    # Display the HTML code within Streamlit
    st.components.v1.html(html_code, height=600)
                    