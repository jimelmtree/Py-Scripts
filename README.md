# Py-Scripts
# Local IP Address and Device Finder

This Python script provides a GUI using PySimpleGUI to retrieve network-related information such as the IP address, network information, public IP address, geolocation, and network speed test results.

## Features

- Display network information (subnet mask and default gateway).
- Display public IP address.
- Display geolocation based on IP using [ip-api.com](http://ip-api.com/).
- Run a network speed test using `speedtest-cli`.

## Prerequisites

- Python 3.11.5
- Required Python packages:
  - `PySimpleGUI`
  - `speedtest-cli`

  You can install the necessary packages using pip:
  ```bash
  pip install PySimpleGUI speedtest-cli

Usage
1. Clone or download this repository.

2. Navigate to the project directory:
cd Local-IP-Address-and-Device-Finder

3. Run the script:
python main.py

4. The GUI will open, and you can click the appropriate buttons to access different functionalities (network information, public IP, geolocation, or speed test).


   Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch for your feature: git checkout -b feature-name.
Make changes and commit: git commit -m 'Description of changes'.
Push to the branch: git push origin feature-name.
Submit a pull request.

Acknowledgments
Thanks to the creators and maintainers of PySimpleGUI and speedtest-cli for their excellent work.
Feel free to reach out if you have any questions, suggestions, or feedback!

