# Custody Management

This project provides a web interface for managing NFTs &  wallets and interacting with the Custodial API. Users can create wallets, view wallet information, manage NFTs, and perform various NFT operations.

## Prerequisites

- Python 3 or higher
- Flask
- Requests
- Your preferred web browser

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/radia2/custody-mgmt.git
   cd arianee-custody-management

2. **Set up a virtual environment:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
```
3. **Install the required packages**
    ```bash
    pip install -r requirements.txt
    ```
## Usage
1. **Set the environment variable for Flask:**
   ```bash
   export FLASK_APP=app.py
   ```
2. **Run the flask app**
   ```bash
   flask run
   ```
3. **Access the application**
   Open your web browser and go to http://127.0.0.1:5000

## Features
You will find the different features listed in this miro: 
<img width="784" alt="Screenshot 2024-06-12 at 11 50 25" src="https://github.com/user-attachments/assets/c9d64434-c632-4892-921c-1bfad6fec3d2">

- Create Wallet: Create new wallets.
- Get Wallet Information: Retrieve wallet information.
- Get Owned NFTs: Fetch and display NFTs owned by the wallet.
- Claim NFT: Claim an NFT using a provided link.
- Transfer NFT: Transfer an NFT to another address.
- Create Transfer Link: Generate a link to transfer NFTs.
- Create Proof Link: Generate a proof link for NFTs.

## Structure
- app.py: Main application file containing Flask routes.
- custody.py: Contains functions to interact with the Custodial API.
- jwtGen.py: Contains functions to generate JWT tokens.
- templates/: Directory containing HTML templates.
- static/: Directory containing static files like CSS and JS.
















