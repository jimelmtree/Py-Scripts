'''
Name: My IP Address Finder
Author: Krantz, Jim
Description: This script finds and displays the IP address of the computer and other cool information.
Date: September 14, 2023
Version: 1.5.0 (Revision 5, September 15, 2023)

Change Log:
- Version 1.5.0(Revision 5, September 15, 2023)
    Changed from tkinter GUI to PySimpleGUI
- Version 1.4.0 (Revision 5, September 15, 2023):
  - Added functions for:
  1. Copy IP to Clipboard:
     Add a button to copy the displayed IP address to the clipboard.

  2. Display Hostname:
     Along with displaying the IP address, display the hostname of the computer.

  3. Ping a Specific Device:
     Allow the user to enter an IP address and ping that specific device to check its availability.

  4. Display Network Information:
     Provide more detailed network information, such as subnet mask, default gateway, etc.

  5. Display Public IP Address:
     Fetch and display the public IP address of the network.

  6. Geolocation:
     Integrate with a service to fetch and display the geolocation (e.g., country, city) of the IP address.

  7. Network Speed Test:
     Allow the user to perform a network speed test and display the results.

- Version 1.3.0 (Revision 4, September 14, 2023):
  - Added button to scan network for other devices.
- Version 1.2.0 (Revision 3, September 14, 2023):
  - Enhanced user interface with a modern dark theme.
- Version 1.1.0 (Revision 2, September 14, 2023):
  - Added pyw for desktop functionality.
- Version 1.0.0 (Revision 1, September 14, 2023):
  - Initial release.
'''

import socket
import ipaddress
import requests
import struct
import speedtest
import threading
import PySimpleGUI as sg

# Function to display network information
def display_network_info():
    try:
        default_gateway = ".".join(ipaddress.IPv4Network("0.0.0.0/0", strict=False).exploded.split('.')[:-1]) + ".1"
        subnet_mask = socket.inet_ntoa(struct.pack('!I', 0xFFFFFFFF ^ (1 << 32 - 24) - 1))
        sg.Popup(f"Subnet Mask: {subnet_mask}\nDefault Gateway: {default_gateway}", title="Network Information")
    except Exception as e:
        sg.Popup(f"Unable to retrieve network information. Error: {str(e)}", title="Error")

# Function to display public IP address
def display_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Check for HTTP errors
        public_ip = response.json().get('ip')
        sg.Popup(f"Public IP address: {public_ip}", title="Public IP Address")
    except requests.exceptions.RequestException as e:
        sg.Popup(f"Unable to retrieve public IP address. Error: {str(e)}", title="Error")

# Function to display geolocation based on IP using ip-api.com
def display_geolocation():
    try:
        response = requests.get('http://ip-api.com/json', timeout=5)  # Set a timeout here (e.g., 5 seconds)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        geolocation_data = response.json()
        sg.Popup(f"Geolocation:\nCountry: {geolocation_data.get('country', 'N/A')}\nCity: {geolocation_data.get('city', 'N/A')}", title="Geolocation")
    except requests.exceptions.RequestException as e:
        sg.Popup(f"Unable to retrieve geolocation. Error: {str(e)}", title="Error")


# Define network speed test using speedtest-cli
def network_speed_test():
    global result_label
    try:
        # Update label to indicate the speed test is starting
        result_label.update(value="Speed test is starting...")

        # Run the speed test in a separate thread
        threading.Thread(target=run_speed_test_in_thread).start()
    except Exception as e:
        update_label_with_results(f"Unable to perform speed test. Error: {str(e)}")

# Function to run speed test in a separate thread
def run_speed_test_in_thread():
    try:
        # Run the speed test using speedtest-cli
        st = speedtest.Speedtest()
        st.get_best_server()  # Select the best server for accurate results
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps

        # Display the speed test results
        speed_test_output = f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps"
        update_label_with_results(speed_test_output)
    except Exception as e:
        update_label_with_results(f"Unable to perform speed test. Error: {str(e)}")


# Function to update the label with the final speed test results
def update_label_with_results(results):
    result_label.update(value=f"Speed Test Results:\n{results}")

# Define the GUI layout
layout = [
    [sg.Button("Run Speed Test", key="-SPEED_TEST-", size=(40, 4))],
    [sg.Button("Display Network Info", key="-NETWORK_INFO-", size=(40, 4))],
    [sg.Button("Display My Public IP", key="-PUBLIC_IP-", size=(40, 4))],
    [sg.Button("Display Geolocation", key="-GEOLOCATION-", size=(40, 4))],
    [sg.Text("", size=(50, 5), key="-RESULT-")],
]

# Create the window
window = sg.Window("Local IP Address and Device Finder", layout, finalize=True)

# Initialize result_label as a global variable
result_label = window["-RESULT-"]

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-NETWORK_INFO-":
        display_network_info()
    elif event == "-PUBLIC_IP-":
        display_public_ip()
    elif event == "-GEOLOCATION-":
        display_geolocation()
    elif event == "-SPEED_TEST-":
        network_speed_test()

# Close the window
window.close()
