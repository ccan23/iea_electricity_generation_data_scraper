# Import necessary libraries
import os
import csv
import requests
from pprint import pprint

# Set VERBOSE flag to True to print out information about each API request
VERBOSE = True

# Define API endpoints for getting available years, products, and countries
api_list_template = 'https://api.iea.org/mes/list/%s'

# Define API endpoint for getting monthly data for a specific country, year, month, and product
api_information_template = 'https://api.iea.org/mes/latest/month?COUNTRY=%s&YEAR=%s&MONTH=%s&PRODUCT=%s&share=true'

# Get lists of available years, products, and countries from the API
years = requests.get(api_list_template % 'YEAR').json()
products = requests.get(api_list_template % 'PRODUCT').json()
countries = requests.get(api_list_template % 'COUNTRY').json()

# Define the header row for the CSV file that will store the data
header = [
    'COUNTRY',           # Name of the country
    'CODE_TIME',         # A code that represents the month and year (e.g., JAN2010 for January 2010)
    'TIME',              # The month and year in a more human-readable format (e.g., January 2010)
    'YEAR',              # The year of the data point
    'MONTH',             # The month of the data point as a number (1-12)
    'MONTH_NAME',        # The month of the data point as a string (e.g., January)
    'PRODUCT',           # The type of energy product (e.g., Hydro, Wind, Solar)
    'VALUE',             # The amount of electricity generated in gigawatt-hours (GWh)
    'DISPLAY_ORDER',     # The order in which the products should be displayed
    'yearToDate',        # The amount of electricity generated for the current year up to the current month in GWh
    'previousYearToDate',# The amount of electricity generated for the previous year up to the current month in GWh
    'share'              # The share of the product in the total electricity generation for the country in decimal format
]

# Check if data.csv file exists
if os.path.isfile('data.csv'):
    # Check if file is empty 
    if os.stat('data.csv').st_size != 0:
        # Read CSV file and get the last line of it
        with open('data.csv', 'r') as csv_file:
            last_line = csv_file.readlines()[-1].split(',')

            # Extract the information from the last line get their index values
            index_last_year = years.index(int(last_line[3]))
            index_last_month = int(last_line[4])
            index_last_country = countries.index(last_line[0])
            index_last_product = products.index(last_line[6]) + 1
    
    else:
        # If CSV file is empty 
        index_last_year, index_last_month, index_last_country, index_last_product = 0, 1, 0, 0

# Open CSV file for writing
with open('data.csv', 'a+', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)

    # Scrape the data and write it to the CSV file
    for year in years[index_last_year:]:
        for month in range(index_last_month, 13):
            for country in countries[index_last_country:]:
                # Replace apostrophes in the country name with %27 to create a valid URL
                country = country.replace('\'', '%27')

                for product in products[index_last_product:]:
                    # Send an API request to get monthly data for the current country, year, month and product
                    response = requests.get(
                        api_information_template % (country, year, month, product)
                    )

                    # Check if the API response is OK
                    if response.ok:
                        # Parse the response JSON
                        response = response.json()

                        # Create a dictionary of the data to write to the CSV file
                        result = dict()

                        # Extract the data from the response and add it to the result dictionary
                        for key in response['latest'][0].keys():
                            result[key] = response['latest'][0][key]

                        # Add year-to-date, previous-year-to-date and share data to the result dictionary
                        result['yearToDate'] = response['yearToDate']
                        result['previousYearToDate'] = response['previousYearToDate']
                        result['share'] = response['share']

                        # Write the result dictionary to the CSV file
                        writer.writerow(result)

                        # If verbose mode is on, print the result for this month
                        if VERBOSE:
                            pprint(result, sort_dicts=False)
                            print('_________________________')
                
                index_last_product = 0
                index_last_month = 1
                index_last_country = 0

# NOTE: This code will take some time to run due to the large number of API requests that are sent.