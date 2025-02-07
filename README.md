# Gas Price Tracker

## 📌 Project Overview
Gas Price Tracker is a Python-based web scraping tool that helps users find the latest gas prices at nearby stations using Selenium and FPDF. It retrieves gas prices based on user input (City, State, or ZIP code) and generates a PDF report of the top 10 results, including station names, addresses, prices, and Google Maps links.

## 🚀 Features
- Scrapes real-time gas prices from [AAA Public Affairs Gas Information](https://cluballiance.aaa.com/public-affairs/gas-information).
- Allows users to search by City & State or ZIP code.
- Extracts the top 10 gas stations with the lowest prices.
- Generates a professional PDF report including station details and Google Maps links.

## 🛠️ Technologies Used
- Python 3
- Selenium WebDriver
- FPDF
- WebDriver Manager

## 📂 Installation & Setup
- ### Step 1: Install Dependencies
   Run the following command to install required Python packages:  
   ```pip install -r requirements.txt```
- ### Step 2: Run the Script
   To execute the program, simply run:  
   ```python tracker.py```

## 🔧 Usage Guide
1. Run the script and choose an option:
   - ```1``` for City & State search
   - ```2``` for ZIP code search
2. Enter the required location details.  
3. The script will scrape gas price data and display results in the terminal.
4. A PDF report will be created with station details and Google Maps links.
