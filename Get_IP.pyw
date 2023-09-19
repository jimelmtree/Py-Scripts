'''
Name: My IP Address Finder
Author: Krantz, Jim
Description: This script finds and displays the IP address of the computer and other cool information.
Date: September 14, 2023
Version: 1.4.0 (Revision 5, September 15, 2023)

Change Log:
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
import tkinter as tk
from tkinter import ttk
import ipaddress
import requests
import pyperclip
import os
import struct
import subprocess
import threading

# Function to display a simple 3D effect using color shading
def apply_3d_effect(widget):
    widget.config(borderwidth=2, relief="groove")

# Function to create a simple fade-in animation
def fade_in(widget, duration=500):
    alpha = 0.0

    def fade():
        nonlocal alpha
        alpha += 0.1
        widget.config(fg='systemWindowBody', bg='black', font=("Helvetica", 18), relief="ridge")
        widget.after(duration, fade)

        if alpha >= 1.0:
            alpha = 1.0
            return

        widget.attributes("-alpha", alpha)

    fade()

# Function to create a slide-in animation
def slide_in(widget, duration=500, start_x=-500, end_x=0):
    widget.place(x=start_x, y=100)

    def slide():
        nonlocal start_x
        start_x += 10
        widget.place(x=start_x, y=100)
        widget.after(duration, slide)

        if start_x >= end_x:
            start_x = end_x
            return

    slide()

# Define network speed test using fast.com
def network_speed_test():
    try:
        # Update label to indicate the speed test is starting
        result_label.config(text="Speed test is starting...")

        # Run the speed test in a separate thread to allow for updating the UI
        threading.Thread(target=run_speed_test_in_thread).start()
    except Exception as e:
        result_label.config(text=f"Unable to perform speed test. Error: {str(e)}")


# Function to run speed test in a separate thread
def run_speed_test_in_thread():
    try:
        result = subprocess.run(["fast"], capture_output=True, text=True)
        speed_test_output = result.stdout.strip()
        update_label_with_results(speed_test_output)
    except Exception as e:
        update_label_with_results(f"Unable to perform speed test. Error: {str(e)}")

# Function to update the label with the final speed test results
def update_label_with_results(results):
    result_label.config(text=f"Speed Test Results:\n{results}")

    # Optionally, you can add a delay before clearing the label
    # app.after(5000, clear_label)

# Define the display_ip function here
def display_ip():
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        result_label.config(text=f"Your computer's IP address is: {ip_address}")

        # Add the IP to clipboard button
        copy_ip_button.pack(pady=10)

        # Display hostname
        hostname_label.config(text=f"Hostname: {host_name}")
        hostname_label.pack(pady=10)

    except Exception as e:
        result_label.config(text=f"Unable to retrieve the IP address. Error: {str(e)}")

# Function to copy the IP address to clipboard
def copy_ip_to_clipboard():
    ip_address = result_label.cget("text").split(": ")[1]
    pyperclip.copy(ip_address)
    print("IP address copied to clipboard.")

# Function to display network information
def display_network_info():
    try:
        default_gateway = ".".join(ipaddress.IPv4Network("0.0.0.0/0", strict=False).exploded.split('.')[:-1]) + ".1"
        subnet_mask = socket.inet_ntoa(struct.pack('!I', 0xFFFFFFFF ^ (1 << 32 - 24) - 1))
        result_label.config(text=f"Subnet Mask: {subnet_mask}\nDefault Gateway: {default_gateway}")
    except Exception as e:
        result_label.config(text=f"Unable to retrieve network information. Error: {str(e)}")

# Function to display public IP address
def display_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Check for HTTP errors
        public_ip = response.json().get('ip')
        result_label.config(text=f"Public IP address: {public_ip}")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Unable to retrieve public IP address. Error: {str(e)}")

# Function to display geolocation based on IP using ip-api.com
def display_geolocation():
    try:
        response = requests.get('http://ip-api.com/json', timeout=5)  # Set a timeout here (e.g., 5 seconds)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        geolocation_data = response.json()
        result_label.config(text=f"Geolocation:\nCountry: {geolocation_data.get('country', 'N/A')}\nCity: {geolocation_data.get('city', 'N/A')}")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Unable to retrieve geolocation. Error: {str(e)}")

# Function to ping a specific IP address
def ping_ip():
    try:
        ip_to_ping = ip_to_ping_entry.get()
        response = os.system(f"ping {ip_to_ping}")
        if response == 0:
            result_label.config(text=f"Ping successful to {ip_to_ping}")
        else:
            result_label.config(text=f"Ping unsuccessful to {ip_to_ping}")
    except Exception as e:
        result_label.config(text=f"Unable to ping. Error: {str(e)}")

# Define the display_network_devices function here
def display_network_devices():
    try:
        subnet_to_scan = ipaddress.IPv4Network("192.168.1.0/24")
        devices = find_devices_on_network(subnet_to_scan)

        if devices:
            result_label.config(text="Devices found on the network:")
            for device in devices:
                result_label.config(text=result_label.cget("text") + f"\nIP Address: {device[0]}, Hostname: {socket.getfqdn(device[1])}")
        else:
            result_label.config(text="No devices found on the network.")
    except Exception as e:
        result_label.config(text=f"Unable to scan the network. Error: {str(e)}")

# Define the find_devices_on_network function here
def find_devices_on_network(subnet):
    devices = []

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(0.1)
            for host in subnet.hosts():
                host_ip = str(host)
                try:
                    sock.sendto(b'Ping', (host_ip, 1))
                    data, addr = sock.recvfrom(1024)
                    devices.append((host_ip, addr[0]))
                except socket.timeout:
                    pass

    except Exception as e:
        print(f"Error: {e}")

    return devices

# Create the main application window
app = tk.Tk()
app.title("Local IP Address and Device Finder")

# Create a custom style for buttons
style = ttk.Style()
style.configure("DarkTheme.TButton",
                foreground="green",
                background="#333333",
                borderwidth=3,
                relief="ridge",
                font=("Helvetica", 18))

# Create and configure widgets
app.configure(bg="#333333")

speed_test_button = ttk.Button(app, text="Run Speed Test", command=network_speed_test, style="DarkTheme.TButton")
speed_test_button.pack(pady=10)
header_label = tk.Label(app, text="Local IP Address and Device Finder", font=("Helvetica Bold", 18), foreground="green", bg="#333333")
result_label = tk.Label(app, text="", font=("Helvetica", 18), foreground="green", bg="#333333")
hostname_label = tk.Label(app, text="", font=("Helvetica", 18), foreground="green", bg="#333333")
ip_to_ping_label = tk.Label(app, text="Enter IP to Ping:", font=("Helvetica", 14), foreground="green", bg="#333333")
ip_to_ping_entry = tk.Entry(app, font=("Helvetica", 14), width=20)
ping_button = ttk.Button(app, text="Ping IP", command=ping_ip, style="DarkTheme.TButton")
network_info_button = ttk.Button(app, text="Display Network Info", command=display_network_info, style="DarkTheme.TButton")
public_ip_button = ttk.Button(app, text="Display Public IP", command=display_public_ip, style="DarkTheme.TButton")
geolocation_button = ttk.Button(app, text="Display Geolocation", command=display_geolocation, style="DarkTheme.TButton")
scan_network_button = ttk.Button(app, text="Scan Network", command=display_network_devices, style="DarkTheme.TButton")
copy_ip_button = ttk.Button(app, text="Copy IP to Clipboard", command=copy_ip_to_clipboard, style="DarkTheme.TButton")

header_label.pack(pady=20)
ping_button.pack(pady=10)
ip_to_ping_label.pack(pady=5)
ip_to_ping_entry.pack(pady=5)
network_info_button.pack(pady=10)
public_ip_button.pack(pady=10)
geolocation_button.pack(pady=10)
scan_network_button.pack(pady=10)
result_label.pack()

app.mainloop()
