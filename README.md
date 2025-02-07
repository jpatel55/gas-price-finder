# Gas Price Tracker

A Python-based web scraping tool that helps users find the cheapest gas prices at nearby stations at that current moment. It retrieves gas prices based on user input (City, State, or ZIP code) and generates a PDF report of the top 10 results, including station names, addresses, prices, and Google Maps links.

## Features
- Scrapes real-time gas prices from [AAA Public Affairs Gas Information](https://cluballiance.aaa.com/public-affairs/gas-information).
- Allows users to search by City & State or ZIP code.
- Extracts the top 10 gas stations with the lowest prices.
- Generates a professional PDF report including station details and Google Maps links.

## Prerequisites
- Python 3.x
- Required libraries: ```fpdf2```, ```selenium```, ```webdriver-manager```

## Usage
- Install the required dependencies using the following command:  
  ```pip install -r requirements.txt```
- Run the script:  
  ```python tracker.py```
