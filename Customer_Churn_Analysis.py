# Customer Churn Analysis
# Analyze customer behavior and identify patterns associated with customer churn.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PART 1: LOAD AND UNDERSTAND THE DATASET
# ============================================================

# Load the Telco Customer Churn dataset into a Pandas DataFrame.
# Replace this path with the location of the CSV file on your computer.
df = pd.read_csv("Telco-Customer-Churn.csv")

# Display the first five rows to get an initial look at the dataset.
print(df.head())

# Display the last five rows to verify that the dataset was loaded completely.
print(df.tail())

# Check the number of observations and features in the dataset.
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

# Display all column names to understand what information is available.
print("All column names:\n", df.columns)

# Check the data type of every column.
# This helps identify columns that may need to be converted before analysis.
print("Data types:\n", df.dtypes)

# Generate descriptive statistics for the numerical columns.
# This provides information such as count, mean, standard deviation,
# minimum, quartiles, and maximum values.
print("Descriptive statistics:\n", df.describe())

# Check whether the dataset contains missing values.
print("Total missing values:", df.isna().sum().sum())

# Check whether any complete rows are duplicated.
print("Duplicate rows:", df.duplicated().sum())


# ============================================================
# PART 2: DATA CLEANING
# ============================================================

# TotalCharges is stored as an object/string column instead of a numerical column.
# First, inspect its current data type and check for missing values.
print("TotalCharges data type:", df["TotalCharges"].dtype)
print("Missing values in TotalCharges:", df["TotalCharges"].isna().sum())

# Some customers have a blank string in TotalCharges.
# Replace those blank values with 0 and convert the column to float
# so that numerical calculations can be performed.
df["TotalCharges"] = df["TotalCharges"].replace(" ", 0)
df["TotalCharges"] = df["TotalCharges"].astype(float)

# Confirm that TotalCharges is now stored as a numerical column.
print("TotalCharges data type after conversion:", df["TotalCharges"].dtype)

# Check whether the conversion introduced any missing values.
print(
    "Missing values in TotalCharges after conversion:",
    df["TotalCharges"].isna().sum()
)

# customerID should uniquely identify each customer.
# Checking for duplicate IDs helps verify the uniqueness of each customer record.
print(
    "Duplicate customerID values:",
    df["customerID"].duplicated().sum()
)


# ============================================================
# PART 3: BASIC CUSTOMER ANALYSIS
# ============================================================

# Count customers by gender to understand the basic demographic distribution.
print("Male customers:", len(df[df["gender"] == "Male"]))
print("Female customers:", len(df[df["gender"] == "Female"]))

# Calculate the average number of months customers have stayed with the company.
print(f"Average customer tenure: {df['tenure'].mean():.2f} months")

# Calculate the average monthly charge across all customers.
print(f"Average monthly charge: {df['MonthlyCharges'].mean():.2f}")

# Calculate the average total charges accumulated per customer.
print(f"Average total charge: {df['TotalCharges'].mean():.2f}")


# ============================================================
# PART 4: OVERALL CHURN ANALYSIS
# ============================================================

# Separate customers who churned from those who remained.
churned_customers = df[df["Churn"] == "Yes"]
non_churned_customers = df[df["Churn"] == "No"]

# Count customers in each churn category.
churned = len(churned_customers)
non_churned = len(non_churned_customers)

print("Churned customers:", churned)
print("Customers who did not churn:", non_churned)

# Calculate the percentage of customers who churned.
total_customers = len(df)
churn_rate = (churned / total_customers) * 100

print(f"Overall churn rate: {churn_rate:.2f}%")


# ============================================================
# PART 5: IDENTIFY CHURN PATTERNS
# ============================================================

# Calculate the number of customers and churn rate for each contract type.
# Grouping the data allows us to compare customer retention across contracts.
contract_summary = df.groupby("Contract").agg(
    Customers=("customerID", "count"),
    Churned=("Churn", lambda x: (x == "Yes").sum())
)

contract_summary["ChurnRate"] = (
    contract_summary["Churned"]
    / contract_summary["Customers"]
    * 100
)

print("\nContract analysis:")
print(contract_summary)


# Compare average tenure between customers who churned and customers who stayed.
average_tenure = df.groupby("Churn")["tenure"].mean()

print("\nAverage tenure by churn status:")
print(average_tenure)


# Compare average monthly charges between customers who churned and customers who stayed.
average_monthly_charge = df.groupby("Churn")["MonthlyCharges"].mean()

print("\nAverage monthly charge by churn status:")
print(average_monthly_charge)


# Calculate the churn rate for each Internet Service category.
internet_summary = df.groupby("InternetService").agg(
    Customers=("customerID", "count"),
    Churned=("Churn", lambda x: (x == "Yes").sum())
)

internet_summary["ChurnRate"] = (
    internet_summary["Churned"]
    / internet_summary["Customers"]
    * 100
)

print("\nInternet Service analysis:")
print(internet_summary)


# Calculate the churn rate for each payment method.
payment_summary = df.groupby("PaymentMethod").agg(
    Customers=("customerID", "count"),
    Churned=("Churn", lambda x: (x == "Yes").sum())
)

payment_summary["ChurnRate"] = (
    payment_summary["Churned"]
    / payment_summary["Customers"]
    * 100
)

print("\nPayment Method analysis:")
print(payment_summary)


# ============================================================
# PART 6: TENURE GROUP ANALYSIS
# ============================================================

# Create customer tenure groups to make it easier to compare churn
# between newer and longer-term customers.
conditions = [
    (df["tenure"] >= 0) & (df["tenure"] <= 12),
    (df["tenure"] >= 13) & (df["tenure"] <= 24),
    (df["tenure"] >= 25) & (df["tenure"] <= 48),
    (df["tenure"] >= 49)
]

choices = [
    "0–12",
    "13–24",
    "25–48",
    "49+"
]

df["TenureGroup"] = np.select(
    conditions,
    choices,
    default="Unknown"
)

# Count the number of customers in each tenure group.
print("\nCustomers in each tenure group:")
print(df["TenureGroup"].value_counts().sort_index())


# Calculate the churn rate for each tenure group.
tenure_summary = df.groupby("TenureGroup").agg(
    Customers=("customerID", "count"),
    Churned=("Churn", lambda x: (x == "Yes").sum())
)

tenure_summary["ChurnRate"] = (
    tenure_summary["Churned"]
    / tenure_summary["Customers"]
    * 100
)

# Keep the groups in their natural chronological order.
tenure_order = [
    "0–12",
    "13–24",
    "25–48",
    "49+"
]

tenure_summary = tenure_summary.reindex(tenure_order)

print("\nTenure group analysis:")
print(tenure_summary)


# ============================================================
# PART 7: ADDITIONAL CUSTOMER ANALYSIS
# ============================================================

# ------------------------------------------------------------
# Compare churn rates between customers paying $100 or more
# and customers paying less than $100 per month.
# ------------------------------------------------------------

high_monthly = df[df["MonthlyCharges"] >= 100]
low_monthly = df[df["MonthlyCharges"] < 100]

high_monthly_churn_rate = (
    (high_monthly["Churn"] == "Yes").mean() * 100
)

low_monthly_churn_rate = (
    (low_monthly["Churn"] == "Yes").mean() * 100
)

print("\nMonthly charge analysis:")
print("Customers paying $100 or more:", len(high_monthly))
print(f"Churn rate for $100+ customers: {high_monthly_churn_rate:.2f}%")

print("Customers paying less than $100:", len(low_monthly))
print(
    f"Churn rate for customers below $100: "
    f"{low_monthly_churn_rate:.2f}%"
)


# ------------------------------------------------------------
# Compare churn rates between senior and non-senior customers.
# ------------------------------------------------------------

senior_customers = df[df["SeniorCitizen"] == 1]
non_senior_customers = df[df["SeniorCitizen"] == 0]

senior_churn_rate = (
    (senior_customers["Churn"] == "Yes").mean() * 100
)

non_senior_churn_rate = (
    (non_senior_customers["Churn"] == "Yes").mean() * 100
)

print("\nSenior citizen analysis:")
print("Senior citizen customers:", len(senior_customers))
print(f"Senior citizen churn rate: {senior_churn_rate:.2f}%")

print("Non-senior customers:", len(non_senior_customers))
print(f"Non-senior churn rate: {non_senior_churn_rate:.2f}%")


# ------------------------------------------------------------
# Compare churn rates across Contract and Internet Service combinations.
# ------------------------------------------------------------

# Group customers by both Contract and Internet Service.
# This allows us to examine combinations of customer characteristics
# instead of looking at each variable independently.
contract_internet_summary = df.groupby(
    ["Contract", "InternetService"]
).agg(
    Customers=("customerID", "count"),
    Churned=("Churn", lambda x: (x == "Yes").sum())
)

contract_internet_summary["ChurnRate"] = (
    contract_internet_summary["Churned"]
    / contract_internet_summary["Customers"]
    * 100
)

print("\nContract + Internet Service analysis:")
print(contract_internet_summary)


# ============================================================
# PART 8: KEY FINDINGS
# ============================================================

# Identify the contract type with the highest churn rate.
highest_contract = contract_summary["ChurnRate"].idxmax()
highest_contract_rate = contract_summary["ChurnRate"].max()

# Identify the Internet Service category with the highest churn rate.
highest_internet = internet_summary["ChurnRate"].idxmax()
highest_internet_rate = internet_summary["ChurnRate"].max()

# Identify the payment method with the highest churn rate.
highest_payment = payment_summary["ChurnRate"].idxmax()
highest_payment_rate = payment_summary["ChurnRate"].max()

# Identify the tenure group with the highest churn rate.
highest_tenure = tenure_summary["ChurnRate"].idxmax()
highest_tenure_rate = tenure_summary["ChurnRate"].max()

# Identify the Contract + Internet Service combination with the
# highest churn rate.
highest_combination = contract_internet_summary["ChurnRate"].idxmax()
highest_combination_rate = contract_internet_summary["ChurnRate"].max()

print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)

print(
    f"Overall churn rate: {churn_rate:.2f}%"
)

print(
    f"Contract type with highest churn rate: "
    f"{highest_contract} ({highest_contract_rate:.2f}%)"
)

print(
    f"Internet Service with highest churn rate: "
    f"{highest_internet} ({highest_internet_rate:.2f}%)"
)

print(
    f"Payment method with highest churn rate: "
    f"{highest_payment} ({highest_payment_rate:.2f}%)"
)

print(
    f"Tenure group with highest churn rate: "
    f"{highest_tenure} ({highest_tenure_rate:.2f}%)"
)

print(
    f"Highest Contract + Internet Service combination: "
    f"{highest_combination} ({highest_combination_rate:.2f}%)"
)

print(
    f"Churn rate for customers paying $100+: "
    f"{high_monthly_churn_rate:.2f}%"
)

print(
    f"Churn rate for customers paying below $100: "
    f"{low_monthly_churn_rate:.2f}%"
)

print(
    f"Senior citizen churn rate: "
    f"{senior_churn_rate:.2f}%"
)

print(
    f"Non-senior churn rate: "
    f"{non_senior_churn_rate:.2f}%"
)


# ============================================================
# PART 9: VISUALIZATIONS
# ============================================================

# Visualizations make it easier to communicate differences in churn
# between customer groups.


# ------------------------------------------------------------
# Churn Rate by Contract Type
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    contract_summary.index,
    contract_summary["ChurnRate"]
)

plt.title("Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(contract_summary["ChurnRate"]):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Churn Rate by Internet Service
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    internet_summary.index,
    internet_summary["ChurnRate"]
)

plt.title("Churn Rate by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(internet_summary["ChurnRate"]):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Churn Rate by Tenure Group
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    tenure_summary.index,
    tenure_summary["ChurnRate"]
)

plt.title("Churn Rate by Tenure Group")
plt.xlabel("Tenure Group")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(tenure_summary["ChurnRate"]):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Churn Rate by Payment Method
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.bar(
    payment_summary.index,
    payment_summary["ChurnRate"]
)

plt.title("Churn Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Churn Rate (%)")

plt.xticks(rotation=20)

for i, value in enumerate(payment_summary["ChurnRate"]):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Churn Rate by Contract + Internet Service
# ------------------------------------------------------------

# Convert the grouped results into a table where contract types
# are rows and Internet Service types are columns.
combination_pivot = contract_internet_summary["ChurnRate"].unstack()

combination_pivot.plot(
    kind="bar",
    figsize=(9, 5)
)

plt.title("Churn Rate by Contract and Internet Service")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=0)
plt.legend(title="Internet Service")

plt.tight_layout()
plt.show()


# ============================================================
# PART 10: CONCLUSION
# ============================================================

# Summarize the main patterns identified during the analysis.
print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)

print(
    "The analysis found that churn was highest among "
    "month-to-month customers, customers with shorter tenure, "
    "fiber optic users, and electronic check users."
)

print(
    "The highest observed churn rate was among customers with "
    "both a month-to-month contract and fiber optic service."
)

print(
    "Customers paying $100 or more per month had a churn rate "
    "of 28.30%, compared with 26.28% for customers paying below $100."
)

print(
    "Senior customers had a higher observed churn rate than "
    "non-senior customers."
)

print(
    "These results show patterns associated with customer churn, "
    "but they do not establish that these factors directly cause churn."
)