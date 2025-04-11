# -*- coding: utf-8 -*-
"""Quantium Data preparation and customer analytics

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PlM9IC4i4FVj6C1EqUacYcOPioUF280g
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

purchase_data = pd.read_csv('/content/QVI_purchase_behaviour.csv')

transaction_data = pd.read_excel('/content/QVI_transaction_data.xlsx')

purchase_data.head()

purchase_data.shape

purchase_data.columns

purchase_data.info()

purchase_data.describe()

purchase_data.isnull().sum()

transaction_data.head()

transaction_data['DATE'].head()

transaction_data.shape

transaction_data.columns

transaction_data.info()

transaction_data.describe()

"""1. Data Cleaning & Preparation:"""

transaction_data.isnull().sum()

purchase_data.duplicated().sum()

transaction_data.duplicated().sum()

transaction_data.drop_duplicates(inplace=True)

transaction_data.duplicated().sum()

#checking for outliers - purchase data
plt.figure(figsize=(8, 5))
sns.boxplot(data=purchase_data)
plt.title('Outlier Check - Purchase Data')
plt.show()

#Outlier check - Transaction Data
plt.figure(figsize=(10, 7))
sns.boxplot(data=transaction_data)
plt.title('Outlier Check - Transaction Data')
plt.show()

purchase_data.dtypes

transaction_data.dtypes

purchase_data['PREMIUM_CUSTOMER'] = purchase_data['PREMIUM_CUSTOMER'].astype('category')
purchase_data['LIFESTAGE'] = purchase_data['LIFESTAGE'].astype('category')

#purchase_data.dtypes

"""* Outliers: Found in customer and transaction data, but they were ID columns, so no action needed.  
* Duplicates: One duplicate transaction was found and removed — a minor anomaly.  
* Date Formatting: Fixed the date column, converting it from an integer format to a proper datetime format.  
* Feature Engineering: Successfully extracted Brand and Pack Size from product descriptions.  
* Insight: The data is now clean and ready for analysis — no major issues were found.  
"""

merged_data = pd.merge(transaction_data, purchase_data, on='LYLTY_CARD_NBR')
merged_data.head()

merged_data.info()

merged_data.describe()

merged_data.shape

merged_data['price_per_unit'] = merged_data['TOT_SALES'] / merged_data['PROD_QTY']
merged_data['price_per_unit'].describe()

"""2. Sales Analysis:"""

#univariate analysis
plt.figure(figsize=(10, 7))
sns.histplot(merged_data['TOT_SALES'], bins = 30, kde=True)
plt.title('Distribution of Total Sales')
plt.show()

plt.figure(figsize=(10,7))
sns.histplot(merged_data[merged_data['TOT_SALES'] <=25]['TOT_SALES'], bins=30, kde=True)
plt.title('Distribution of Total Sales 0-30')
plt.show()

merged_data[merged_data['TOT_SALES'] <= 21.62]['TOT_SALES'].value_counts().sort_values(ascending=False)

# Grouping data by product and summing total sales
product_sales = merged_data.groupby('PROD_NAME')['TOT_SALES'].sum().sort_values(ascending=False).head(15)

# Visualizing the top 10 products by total sales
plt.figure(figsize=(12, 9))
sns.barplot(x=product_sales.index, y=product_sales.values)
plt.title('Top 15 Products by Total Sales')
plt.xlabel('Product Name')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()

"""* Total Sales Distribution: Right-skewed, indicating that most sales come from lower-priced products.  
* Price Range Insight: Majority of sales fall in the ₹7–₹10 range; sales beyond ₹15 are minimal.  
* Top-Selling Products: "Dorito Corn Chips" emerged as the most purchased item, followed by several other well-performing products.  
* Recommendation: Introduce more product varieties in the ₹7–₹10 range, as that’s the sweet spot for customer spending.

3. Customer Analysis:
"""

x = merged_data.groupby('LIFESTAGE')['TOT_SALES'].sum().sort_values(ascending=False).reset_index()

#total sales vs lifestage
plt.figure(figsize=(8, 5))
sns.barplot(x='LIFESTAGE', y='TOT_SALES', data=x, errorbar=None)
plt.title('Total Sales by Lifestage')
plt.xlabel('Lifestage')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()

#total sales vs. premium customer
premium_sales = merged_data.groupby('PREMIUM_CUSTOMER')['TOT_SALES'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x='PREMIUM_CUSTOMER', y='TOT_SALES', data=premium_sales, errorbar=None, palette="viridis")  # Change palette
plt.title('Total Sales by Customer Affluence', fontsize=14, fontweight='bold')
plt.xlabel('Customer Type', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add a subtle grid
plt.show()

"""1. Lifestage Analysis:

* Top Spend Group: Older Singles/Couples contribute the highest sales.  
* Lowest Spend Group: New Families and Mid-age Singles/Couples spend the least.  
* Recommendation: Tailor promotional offers and product variety towards older customer segments.  

2. Premium vs. Budget:  
* Premium customers make lower sales contributions compared to budget customers.  
* Recommendation: Incentivize premium customers with loyalty programs or targeted discounts to boost their engagement.

4. Store Performance:
"""

#total sales vs. store number
store_sales = merged_data.groupby('STORE_NBR')['TOT_SALES'].sum().sort_values(ascending=False).reset_index().head(20)

plt.figure(figsize=(8, 5))
sns.barplot(x='STORE_NBR', y='TOT_SALES', data=store_sales, errorbar=None)
plt.title('Total Sales by Store Number')
plt.xlabel('Store Number')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()

"""* Top Performing Store: Store 226 had the highest sales, with several others closely following.  
* Sales Consistency: Sales remain fairly steady across months, with a slight dip in February.  
* Recommendation: Investigate Store 226's practices and replicate its strategies in underperforming stores.

5. Purchase Behavior:
"""

transaction_data['DATE'] = pd.to_datetime(transaction_data['DATE'], origin='1899-12-30', unit='D')

print(transaction_data['DATE'].head())
print(transaction_data['DATE'].dtype)

transaction_data['MONTH_YEAR'] = transaction_data['DATE'].dt.to_period('M')
monthly_sales = transaction_data.groupby('MONTH_YEAR')['TOT_SALES'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x='MONTH_YEAR', y='TOT_SALES', data=monthly_sales, errorbar=None)
plt.xticks(rotation=45)
plt.title('Total Sales by Month')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Convert MONTH_YEAR to string for better visualization
transaction_data['MONTH_YEAR'] = transaction_data['DATE'].dt.to_period('M').astype(str)

# Aggregate total sales by month
monthly_sales = transaction_data.groupby('MONTH_YEAR')['TOT_SALES'].sum().reset_index()

# Plot Line Chart
plt.figure(figsize=(10, 5))
sns.lineplot(x='MONTH_YEAR', y='TOT_SALES', data=monthly_sales, marker='o', color='blue', label="Total Sales")

# Highlight December peak
plt.axvline(x=monthly_sales[monthly_sales['MONTH_YEAR'].str.endswith('-12')].index[-1], linestyle='dashed', color='red', label="December Peak")

# Formatting
plt.xticks(rotation=45)
plt.xlabel("Month-Year")
plt.ylabel("Total Sales")
plt.title("Total Sales Trends by Month")
plt.legend()
plt.show()

#total sales vs. product quantity
qty_sales = merged_data.groupby('PROD_QTY')['TOT_SALES'].sum().reset_index()

# Plotting
plt.figure(figsize=(8, 5))
sns.barplot(x='PROD_QTY', y='TOT_SALES', data=qty_sales, errorbar=None)
plt.title('Total Sales by Product Quantity')
plt.xlabel('Product Quantity')
plt.ylabel('Total Sales')
plt.show()

"""* Product Quantity: Most customers purchase two units at a time; single-item purchases account for a smaller share.  
* Recommendation: Consider bundling offers or discounts for multi-pack purchases to further encourage larger buys.
"""

#total spend per customer
total_spend = merged_data.groupby('LYLTY_CARD_NBR')['TOT_SALES'].sum().reset_index()
total_spend.columns = ['Customer_ID', 'Total_Spend']
total_spend.sort_values(by='Total_Spend', ascending = False).head()

#average spend per transaction
avg_spend=merged_data.groupby('TXN_ID')['TOT_SALES'].mean().reset_index()
avg_spend.columns = ['Transaction_ID', 'Average_Spend']
avg_spend.sort_values(by='Average_Spend', ascending = False).head()

#transaction per customer
transaction_count = merged_data.groupby('LYLTY_CARD_NBR')['TXN_ID'].nunique().reset_index()
transaction_count.columns = ['Customer_ID', 'Transaction_Count']
transaction_count.sort_values(by='Transaction_Count', ascending = False).head().reset_index()

#avg product quantity per transaction
avg_qty = merged_data.groupby('TXN_ID')['PROD_QTY'].mean().reset_index()
avg_qty.columns = ['Transaction_ID', 'Average_Quantity']
avg_qty.head()

"""Feature Engineering"""

merged_data['BRAND'] = merged_data['PROD_NAME'].apply(lambda x: x.split()[0])

import re
merged_data['PACK_SIZE'] = merged_data['PROD_NAME'].apply(lambda x: re.search(r'\d+g', x).group() if re.search(r'\d+g', x) else 'Unknown')

#merged_data.head()

"""Customer Segmentation"""

# Total spend per customer
total_spend = merged_data.groupby('LYLTY_CARD_NBR')['TOT_SALES'].sum().reset_index()
total_spend.columns = ['Customer_ID', 'Total_Spend']


total_spend['Spending_Category'] = pd.qcut(total_spend['Total_Spend'],
                                          q=[0, 0.25, 0.75, 1.0],
                                          labels=['Low Spender', 'Mid Spender', 'High Spender'])


total_spend.head()

# Purchase frequency per customer
purchase_freq = merged_data.groupby('LYLTY_CARD_NBR')['TXN_ID'].nunique().reset_index()
purchase_freq.columns = ['Customer_ID', 'Purchase_Frequency']

purchase_freq['Frequency_Category'] = pd.qcut(purchase_freq['Purchase_Frequency'],
                                                 q=[0, 0.5, 0.75, 1.0],
                                                 labels=['Occasional Buyer', 'Regular Buyer', 'Frequent Buyer'],
                                                 duplicates='drop')


purchase_freq.head()

# Visualize Spend Category Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='Spending_Category', data=total_spend, hue='Spending_Category', legend=False, palette='viridis')
plt.title('Distribution of Spend Categories')
plt.xlabel('Spend Category')
plt.ylabel('Number of Customers')
plt.show()

# Visualize Frequency Category Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='Frequency_Category', data=purchase_freq, hue='Frequency_Category', legend=False, palette='magma')
plt.title('Distribution of Purchase Frequency Categories')
plt.xlabel('Frequency Category')
plt.ylabel('Number of Customers')
plt.show()

"""1. Spending Patterns:

* Mid-level spenders dominate the customer base.  
* High spenders are a smaller but important segment.  
* Recommendation: Offer exclusive deals or early access to new products for high spenders to maintain their loyalty.  

2. Buying Frequency:  
* Occasional buyers form the largest segment; frequent buyers are relatively few.
* Recommendation: Engage occasional buyers with personalized discounts or reminders to increase their purchase frequency.

7. Brand Preference:
"""

# Dictionary to fix brand names
brand_fixes = {
    'Burger': 'Unknown',
    'French': 'Unknown',
    'Old': 'Old El Paso',
    'Grain': 'Grain Waves',
    'Red': 'Red Rock Deli',
    'Infzns': 'Infuzions',
    'GrnWves': 'Grain Waves Plus',
    'Snbts': 'Sunbites'
}

merged_data['BRAND'] = merged_data['BRAND'].replace(brand_fixes)

brand_sales = merged_data.groupby('BRAND')['TOT_SALES'].sum().reset_index().sort_values(by='TOT_SALES', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='BRAND', y='TOT_SALES', data=brand_sales, hue='BRAND', dodge=False, legend=False, palette='rocket')
plt.title('Total Sales by Brand')
plt.xticks(rotation=90)
plt.xlabel('Brand')
plt.ylabel('Total Sales')
plt.show()

import matplotlib.pyplot as plt

# Group by LIFESTAGE and PREMIUM_CUSTOMER and sum total sales (explicitly set observed=False to remove warning)
segment_sales = merged_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'], observed=False)['TOT_SALES'].sum().reset_index()

# Convert categorical columns to string before combining them
segment_sales['LABEL'] = segment_sales['LIFESTAGE'].astype(str) + " - " + segment_sales['PREMIUM_CUSTOMER'].astype(str)

# Extract labels and values
labels = segment_sales['LABEL']
sizes = segment_sales['TOT_SALES']

# Create Pie Chart
plt.figure(figsize=(12, 12))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Customer Segmentation by Life Stage & Spending Type")
plt.show()

"""* Top Brands: "Kettle" is the most popular brand, followed by Smiths and Doritos.  
* Brand Anomalies: Fixed misclassified brand names like "Grain Waves" and "Old El Paso".  
* Recommendation: Increase visibility and shelf space for top-performing brands and phase out underperforming ones.

8. Pack Size Preference:
"""

# Total sales by pack size
pack_sales = merged_data.groupby('PACK_SIZE')['TOT_SALES'].sum().reset_index()

# Sort by pack size for better visualization
pack_sales = pack_sales.sort_values(by='PACK_SIZE')

# Visualize total sales by pack size
plt.figure(figsize=(10, 6))
sns.barplot(x='PACK_SIZE', y='TOT_SALES', data=pack_sales,hue='PACK_SIZE', legend=False, palette='magma')
plt.title('Total Sales by Pack Size')
plt.xlabel('Pack Size (grams)')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

"""* Insight: 175g packs are the most preferred, suggesting this size balances value and price well for customers.
* Recommendation: Ensure ample stock of 175g packs and explore similar sizing strategies for new product launches.

**Strategic Recommendations:**

* Drive sales growth by doubling down on popular price ranges and pack sizes.  
* Boost engagement with occasional buyers through personalized offers and loyalty incentives.  
* Tailor marketing and product selection toward high-spending customer segments (Older Singles/Couples, Retirees).  
* Investigate successful store practices and replicate them across underperforming locations.
"""

