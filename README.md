# Customer Churn Analysis

## Project Overview

This project analyzes customer behavior and identifies patterns associated with customer churn using the Telco Customer Churn dataset.

## Objectives

- Understand the structure and characteristics of the dataset.
- Clean and prepare the data for analysis.
- Calculate the overall customer churn rate.
- Compare churn rates across different customer groups.
- Identify patterns associated with higher and lower churn rates.
- Visualize the main findings using charts.

## Dataset

The dataset contains **7,043 customers** and **21 columns**

It includes information such as:

- Customer demographics
- Tenure
- Phone and internet services
- Contract type
- Payment method
- Monthly charges
- Total charges
- Churn status

## Data Cleaning

The main data preparation steps included:

- Checking for missing values.
- Checking for duplicate rows.
- Checking for duplicate customer IDs.
- Replacing blank values in `TotalCharges` with 0.
- Converting `TotalCharges` from string to numerical data.

## Analysis

The project analyzes churn patterns based on:

- Contract type
- Internet service
- Payment method
- Tenure groups
- Monthly charges
- Senior citizen status
- Contract and internet service combinations

## Key Findings

- The overall churn rate was **26.54%**.
- Month-to-month customers had a churn rate of **42.71%**.
- Fiber optic customers had a churn rate of **41.89%**.
- Customers using electronic checks had a churn rate of **45.29%**.
- Customers with 0–12 months of tenure had a churn rate of **47.44%**.
- The month-to-month + fiber optic combination had a churn rate of **54.61%**.
- Customers paying $100 or more per month had a churn rate of **28.30%**.
- Senior citizen customers had a churn rate of **41.68%**.

These results describe patterns in this dataset and do not by themselves establish that any particular factor causes customer churn.

## Visualizations

The project includes visualizations showing:

- Churn Rate by Contract Type
- Churn Rate by Internet Service
- Churn Rate by Tenure Group
- Churn Rate by Payment Method
- Churn Rate by Contract and Internet Service

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib

## How to Run

1. Clone or download this repository.
2. Make sure Python is installed.
3. Install the required libraries:

```bash
pip install -r requirements.txt
