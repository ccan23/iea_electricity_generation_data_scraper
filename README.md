# IEA Electricity Generation Data Scraper

Collected data: [kaggle.com](https://www.kaggle.com/datasets/ccanb23/iea-monthly-electricity-statistics)

This Python script retrieves monthly energy data for a specific country, year, month, and product from the International Energy Agency (IEA) API and stores it in a CSV file. The script makes API requests to get available years, products, and countries, and uses this information to loop through all possible combinations of country, year, month, and product. The retrieved data includes the amount of electricity generated in gigawatt-hours (GWh), the share of the product in the total electricity generation for the country, and other related information. The script uses the CSV file to store the data and appends the new data to the existing data if the file already exists. This script is released under the MIT License.

## Requirements
* Python 3.x
* `requests` library

## Getting Started
To get started, clone the repository and run the script in a Python environment. The script will automatically create a new CSV file if one does not already exist. If a file does exist, the script will pick up where it left off to avoid duplicating data.

1. Clone the repo:
```sh
git clone https://github.com/ccan23/iea_electricity_generation_data_scraper.git
```

2. Navigate to the project directory:
```sh
cd iea_electricity_generation_data_scraper
```

3. Install the required libraries:
```sh
pip install -r requirements.txt
```

## Usage
```sh
python3 iea_scraper.py
```

The script sends API requests to get monthly electricity generation data for all available countries, products, and years. It stores this data in a CSV file named "data.csv" with the following columns:

* **COUNTRY**: Name of the country
* **CODE_TIME**: A code that represents the month and year (e.g., JAN2010 for January 2010)
* **TIME**: The month and year in a more human-readable format (e.g., January 2010)
* **YEAR**: The year of the data point
* **MONTH**: The month of the data point as a number (1-12)
* **MONTH_NAME**: The month of the data point as a string (e.g., January)
* **PRODUCT**: The type of energy product (e.g., Hydro, Wind, Solar)
* **VALUE**: The amount of electricity generated in gigawatt-hours (GWh)
* **DISPLAY_ORDER**: The order in which the products should be displayed
* **yearToDate**: The amount of electricity generated for the current year up to the current month in GWh
* **previousYearToDate**: The amount of electricity generated for the previous year up to the current month in GWh
* **share**: The share of the product in the total electricity generation for the country in decimal format

By default, the script is in verbose mode and will print out information about each API request. To turn off verbose mode, set VERBOSE to False in the script.

## Note
This script may take some time to run due to the large number of API requests that are sent.

## Code Explanation with Details
This code is a Python script that scrapes monthly electricity generation data for different countries and products from the International Energy Agency (IEA) API and stores the data in a CSV file.

The script first imports the necessary libraries including os, csv, requests, and pprint. It also sets the VERBOSE flag to True which will print out information about each API request.

Then it defines API endpoints for getting available years, products, and countries, as well as an API endpoint for getting monthly data for a specific country, year, month, and product.

Next, it sends requests to the API to get lists of available years, products, and countries and stores them in the variables years, products, and countries, respectively.

It defines the header row for the CSV file that will store the data and checks if the data.csv file exists. If the file exists and is not empty, it reads the CSV file and gets the last line of it. It then extracts the information from the last line and gets their index values. If the CSV file is empty, it sets the index_last_year, index_last_month, index_last_country, and index_last_product variables to 0, 1, 0, and 0, respectively.

It then opens the data.csv file for writing and iterates through each year, month, country, and product to send an API request to get monthly data for the current country, year, month, and product. It replaces apostrophes in the country name with %27 to create a valid URL. If the API response is OK, it parses the response JSON and creates a dictionary of the data to write to the CSV file. It extracts the data from the response and adds it to the result dictionary. It also adds year-to-date, previous-year-to-date, and share data to the result dictionary. It then writes the result dictionary to the CSV file. If verbose mode is on, it prints the result for this month.

Finally, it sets some variables to 0 to start iterating from the beginning for the next run.

## License
This script is licensed under the MIT license. See LICENSE file for more details.
