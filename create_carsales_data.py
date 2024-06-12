# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:34:28 2024

@author: Gebruiker
"""

import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate stores
stores = [f'Store_{i+1}' for i in range(69)]

# Define the car models and their categories
models = {
    'Model_1': {'type': 'Class-A', 'fuels': ['Petrol', 'Diesel'], 'price_range': (15000, 20000), 'base_profit_margin': 0.10},
    'Model_2': {'type': 'Class-A', 'fuels': ['Electric'], 'price_range': (18000, 23000), 'base_profit_margin': 0.12},
    'Model_3': {'type': 'Class-B', 'fuels': ['Petrol', 'Diesel'], 'price_range': (20000, 25000), 'base_profit_margin': 0.11},
    'Model_4': {'type': 'Class-B', 'fuels': ['Petrol', 'Diesel'], 'price_range': (20000, 25000), 'base_profit_margin': 0.11},
    'Model_5': {'type': 'Class-B', 'fuels': ['Hybrid'], 'price_range': (23000, 28000), 'base_profit_margin': 0.13},
    'Model_6': {'type': 'Class-B', 'fuels': ['Electric'], 'price_range': (24000, 29000), 'base_profit_margin': 0.14},
    'Model_7': {'type': 'Class-C', 'fuels': ['Petrol', 'Diesel', 'Hybrid'], 'price_range': (30000, 40000), 'base_profit_margin': 0.15},
    'Model_8': {'type': 'Class-C', 'fuels': ['Electric'], 'price_range': (35000, 45000), 'base_profit_margin': 0.16},
    'Model_9': {'type': 'SUV', 'fuels': ['Petrol', 'Diesel', 'Hybrid'], 'price_range': (35000, 45000), 'base_profit_margin': 0.14},
    'Model_10': {'type': 'SUV', 'fuels': ['Petrol', 'Diesel', 'Hybrid'], 'price_range': (35000, 45000), 'base_profit_margin': 0.14},
    'Model_11': {'type': 'SUV', 'fuels': ['Electric'], 'price_range': (40000, 50000), 'base_profit_margin': 0.18}
}

# Generate countries and their populations
countries = {
    'Germany': 40000000,
    'France': 36000000,
    'Italy': 34000000,
    'Spain': 24000000,
    'Netherlands': 15000000,
    'Belgium': 11500000,
    'Sweden': 10300000,
    'Denmark': 5800000,
    'Norway': 5400000,
    'Finland': 5500000,
    'Poland': 38000000,
    'Austria': 8900000,
    'Switzerland': 8600000,
    'Portugal': 10200000,
    'Czech Republic': 10600000,
    'Greece': 10700000,
    'Hungary': 9700000,
    'Ireland': 5000000,
    'Croatia': 4100000,
    'Slovakia': 5400000
}

# Generate dates for the last 4 years
dates = pd.date_range(start='2019-01-01', end='2023-12-31', freq='M')

# Create an empty DataFrame to hold the sales data
data = []

# Function to introduce seasonality
def get_seasonal_sales(month):
    if (month in [12, 1, 2]):  # Winter
        return np.random.randint(1, 3)
    elif (month in [6, 7, 8]):  # Summer
        return np.random.randint(3, 6)
    else:  # Other months
        return np.random.randint(0, 2)

# Function to introduce yearly variability
def get_yearly_sales(year, fuel):
    fuel_factors = {
        'Petrol': {2019: 1.0, 2020: 0.8, 2021: 1.0, 2022: 0.9, 2023: 1.1},
        'Diesel': {2019: 1.0, 2020: 0.7, 2021: 0.8, 2022: 0.8, 2023: 0.6},
        'Hybrid': {2019: 1.0, 2020: 0.9, 2021: 1.1, 2022: 1.2, 2023: 1.3},
        'Electric': {2019: 1.0, 2020: 1.1, 2021: 1.3, 2022: 1.5, 2023: 1.9}
    }
    return fuel_factors[fuel].get(year, 1.0)

# Function to introduce monthly variability in profit margins
def get_monthly_profit_margin(month):
    monthly_margin_factors = {
        1: 1.00, 2: 1.02, 3: 1.03, 4: 1.05, 5: 1.04, 6: 1.06,
        7: 1.07, 8: 1.05, 9: 1.04, 10: 1.03, 11: 1.02, 12: 1.01
    }
    return monthly_margin_factors.get(month, 1.0)

# Function to introduce yearly variability in profit margins
def get_yearly_profit_margin(year):
    yearly_margin_factors = {
        2019: 1.0,
        2020: 0.95,
        2021: 1.05,
        2022: 1.1,
        2023: 1.15
    }
    return yearly_margin_factors.get(year, 1.0)

for store in stores:
    for model, details in models.items():
        for fuel in details['fuels']:
            for date in dates:
                # Adjust sales based on model popularity, seasonality, and yearly and fuel source variability
                base_sales = np.random.randint(0, 50) if 'Electric' in fuel else np.random.randint(0, 100)
                seasonal_sales = get_seasonal_sales(date.month)
                yearly_sales_factor = get_yearly_sales(date.year, fuel)
                sales = (base_sales + seasonal_sales) * yearly_sales_factor
                
                # Introduce variation in prices
                price = np.random.uniform(*details['price_range'])
                sales_eur = sales * price
                
                # Calculate profit margin
                base_margin = details['base_profit_margin']
                monthly_margin_factor = get_monthly_profit_margin(date.month)
                yearly_margin_factor = get_yearly_profit_margin(date.year)
                profit_margin = base_margin * monthly_margin_factor * yearly_margin_factor
                profit = sales_eur * profit_margin
                
                # Randomly assign a country to the store
                country = np.random.choice(list(countries.keys()))
                
                # Scale sales by the population of the country
                population_factor = countries[country] / 1000000  # Example scaling factor
                sales *= population_factor
                sales_eur *= population_factor
                profit *= population_factor
                
                data.append([store, model, details['type'], fuel, date, sales, country, sales_eur, profit_margin, profit])

# Create the DataFrame
df = pd.DataFrame(data, columns=['Store', 'Model', 'ModelType', 'FuelSource', 'Date', 'Sales', 'Country', 'SalesEUR', 'ProfitMargin', 'Profit'])

# Save to CSV (optional)
df.to_csv('car_sales_data.csv', index=False)


