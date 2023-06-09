# -*- coding: utf-8 -*-
"""Copy of Copy of capstone Project: Retail.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13B8e1dgVkQNeJqLtirfweW81jBcY6Sl5

#**Retail**

![](https://www.foodnavigator-asia.com/var/wrbm_gb_food_pharma/storage/images/publications/food-beverage-nutrition/foodnavigator-asia.com/article/2018/07/02/five-key-features-that-will-shape-the-online-retail-store-of-the-future/8266733-1-eng-GB/Five-key-features-that-will-shape-the-online-retail-store-of-the-future.jpg)

#**Capstone Project: Retail**

###**Problem Statement:**


- It is a critical requirement for business to understand the value derived from a customer. RFM is a method used for analyzing customer value.
- Customer segmentation is the practice of segregating the customer base into groups of individuals based on some common characteristics such as age, gender, interests, and spending habits.
- Perform customer segmentation using RFM analysis. The resulting segments can be ordered from most valuable (highest recency, frequency, and value) to least valuable (lowest recency, frequency, and value).
- Dataset Description: This is a transnational data set which contains all the transactions that occurred between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. The company mainly sells unique and all-occasion gifts.


###**Dataset Description:**

This is a transnational data set which contains all the transactions that occurred between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. The company mainly sells unique and all-occasion gifts.


**InvoiceNo:** Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.

**StockCode:** Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.

**Description:** Product (item) name. Nominal.

**Quantity:** The quantities of each product (item) per transaction. Numeric.
InvoiceDate: Invoice Date and time. Numeric, the day and time when each transaction was generated.

**UnitPrice:** Unit price. Numeric, Product price per unit in sterling.

**CustomerID:** Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.

**Country:** Country name. Nominal, the name of the country where each customer resides.



##**Project Task: Week 1:**

###**Data Cleaning:**

**Perform a preliminary data inspection and data cleaning.**

a. Check for missing data and formulate an apt strategy to treat them.

b. Remove duplicate data records.

c. Perform descriptive analytics on the given data.

###**Data Transformation:**

**Perform cohort analysis (a cohort is a group of subjects that share a defining characteristic). Observe how a cohort behaves across time and compare it to other cohorts.**

a. Create month cohorts and analyze active customers for each cohort.

b. Analyze the retention rate of customers.


##**Project Task: Week 2**

###**Data Modeling :**

1. Build a RFM (Recency Frequency Monetary) model. Recency means the number of days since a customer made the last purchase. Frequency is the number of purchase in a given period. It could be 3 months, 6 months or 1 year. Monetary is the total amount of money a customer spent in that given period. Therefore, big spenders will be differentiated among other customers such as MVP (Minimum Viable Product) or VIP.

2. Calculate RFM metrics.

3. Build RFM Segments. Give recency, frequency, and monetary scores individually by dividing them into quartiles.

 b1.Combine three ratings to get a RFM segment (as strings).

 b2. Get the RFM score by adding up the three ratings.

 b3. Analyze the RFM segments by summarizing them and comment on the findings.

**Note:** Rate “recency" for customer who has been active more recently higher than the less recent customer, because each company wants its customers to be recent.

**Note:** Rate “frequency" and “monetary" higher, because the company wants the customer to visit more often and spend more money.




##**Project Task: Week 3**

###**Data Modeling :**

Create clusters using k-means clustering algorithm.

  a. Prepare the data for the algorithm. If the data is asymmetrically distributed, manage the skewness with appropriate transformation. Standardize the data.

 b. Decide the optimum number of clusters to be formed.

 c. Analyze these clusters and comment on the results.



##**Project Task: Week 4**
   
###**Data Reporting:**

Create a dashboard in tableau by choosing appropriate chart types and metrics useful for the business. The dashboard must entail the following:

  a. Country-wise analysis to demonstrate average spend. Use a bar chart to show the monthly figures

  b. Bar graph of top 15 products which are mostly ordered by the users to show the number of products sold

  c. Bar graph to show the count of orders vs. hours throughout the day

  d. Plot the distribution of RFM values using histogram and frequency charts

  e. Plot error (cost) vs. number of clusters selected

  f. Visualize to compare the RFM values of the clusters using heatmap

#**SOLUTION:**



##**Week 1:**

##**(A) Data Cleaning**

**(1) Reading Data and Preliminary Data Inspection**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from datetime import timedelta
from pandas import ExcelWriter

df=pd.read_excel('/content/Online Retail.xlsx')
df.head()

# Check shape of data
df.shape

# Check feature details of data
df.info()

"""- **(a) Missing values treatment:**"""

# Check missing values in data
df.isnull().sum()

#check percentage of missing value in data
df_null=round(df.isnull().sum()/len(df)*100,2)
df_null

df = df.drop('Description', axis=1)
df = df.dropna()
df.shape

"""- **(b) Remove duplicate data records:** Since our data is transactional data and it has duplicate entries for InvoiceNo and CustomerID, we will drop only those rows which are completely duplicated, not on the basis of any one particular column such as InvoiceNo or CustomerID etc."""

df = df.drop_duplicates()
df.shape

"""- **(c) Perform descriptive anaylysis on the given data:**"""

# CustomerID is 'float64', changing the datatype of CustomerId to string as Customer ID as numerical data does not make sense

df['CustomerID'] = df['CustomerID'].astype(str)

df.describe(datetime_is_numeric=True)

"""- **Quantity:** Average quantity of each product in transaction is 12.18. Also note that minimum value in Quantity column is negative. This implies that some customers had returned the product during our period of analysis.

- **InvoiceDate**: Our data has transaction between 01-12-2010 to 09-12-2011

- **UnitPrice:** Average price of each product in transactions is 3.47
"""

df.describe(include=['O'])

"""- **InvoiceNo:** Total entries in preprocessed data are 4,01,602 but transactions are 22,190. Most number of entries (count of unique products) are in Invoice No. '576339' and is 542 nos.

- **StockCode:** There are total 3684 unique products in our data and product with stock code '85123A' appears most frequently (2065 times) in our data.

- **CustomerID:** There are 4372 unique customers in our final preprocessed data. Customer with ID '17841' appears most frequently in data (7812 times)
Country: Company has customers across 37 countries. Most entries are from United Kingdom in our dataset (356726)

##**(B) Data Transformation**

  **(2) Perform Cohort Analysis**

**(a) Create month cohort of customers and analyze active customers in each cohort:**
"""

# Convert InvoiceDate into month year format
df['month_year']=df['InvoiceDate'].dt.to_period('M')
df['month_year'].nunique()

month_cohort=df.groupby('month_year')['CustomerID'].nunique()
month_cohort

plt.figure(figsize = (15,5))
sns.barplot(y= month_cohort.index, x= month_cohort.values)
plt.xlabel('Count of Customers')
plt.title('No. of Active Customers')

month_cohort-month_cohort.shift(1)

retention_rate=round(month_cohort.pct_change(periods=1)*100,2)
retention_rate

plt.figure(figsize=(10,5))
sns.barplot(y = retention_rate.index, x = retention_rate.values);

"""##**Week 2:**

**Monetary analysis:**
"""

df['amount']=df['Quantity']*df['UnitPrice']
df.head()

df_monetary=df.groupby('CustomerID').sum()['amount'].reset_index()
df_monetary

"""**Frequency Analysis:**"""

df_frequency=df.groupby('CustomerID').nunique()['InvoiceNo'].reset_index()
df_frequency

"""**Recency Analysis:**

"""

# We will fix reference date for calculating recency as last transaction day in data + 1 day
ref_day = max(df['InvoiceDate']) + timedelta(days=1)
df['days_to_last_order'] = (ref_day - df['InvoiceDate']).dt.days
df.head()

df_recency = df.groupby('CustomerID')['days_to_last_order'].min().reset_index()
df_recency

"""**Calculate RFM metrics:**"""

df_rf = pd.merge(df_recency, df_frequency,  on='CustomerID', how='inner')
df_rfm = pd.merge(df_rf, df_monetary, on='CustomerID', how='inner')
df_rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
df_rfm.head()

"""**Build RFM Segments:**"""

df_rfm['recency_labels'] = pd.cut(df_rfm['Recency'], bins=5,
                                     labels=['newest', 'newer', 'medium', 'older', 'oldest'])
df_rfm['recency_labels'].value_counts().plot(kind='barh');
df_rfm['recency_labels'].value_counts()

df_rfm['frequency_labels'] = pd.cut(df_rfm['Frequency'], bins=5, labels=['lowest', 'lower', 'medium', 'higher', 'highest'])
df_rfm['frequency_labels'].value_counts().plot(kind='barh');
df_rfm['frequency_labels'].value_counts()

df_rfm['monetary_labels'] = pd.cut(df_rfm['Monetary'], bins=5, labels=['smallest', 'smaller', 'medium', 'larger', 'largest'])
df_rfm['monetary_labels'].value_counts().plot(kind='barh');
df_rfm['monetary_labels'].value_counts()

df_rfm['rfm_segment'] = df_rfm[['recency_labels','frequency_labels','monetary_labels']].agg('-'.join, axis=1)
df_rfm.head()

"""**RFM Score:**"""

recency_dict = {'newest': 5, 'newer':4, 'medium': 3, 'older':2, 'oldest':1}
frequency_dict = {'lowest':1, 'lower':2, 'medium': 3, 'higher':4, 'highest':5}
monetary_dict = {'smallest':1, 'smaller':2, 'medium': 3, 'larger':4, 'largest':5}

df_rfm['rfm_score'] = df_rfm['recency_labels'].map(recency_dict).astype(int)+ df_rfm['frequency_labels'].map(frequency_dict).astype(int) + df_rfm['monetary_labels'].map(monetary_dict).astype(int)
df_rfm.head(10)

"""**Analyze RFM Segment and Score:**"""

df_rfm['rfm_segment'].value_counts().plot(kind='barh', figsize=(10, 5));

df_rfm['rfm_score'].value_counts().plot(kind='barh', figsize=(10, 5));

"""##**Week 3**

###**Data Modeling:**

  **1.Create clusters using k-means clustering algorithm.**

  **a. Prepare the data for the algorithm. If the data is asymmetrically distributed, manage the skewness with appropriate transformation. Standardize the data** 
"""

print(df_rfm.shape)

df_rfm.head()

plt.figure(figsize=(12,6))

for i, feature in enumerate(['Recency', 'Frequency', 'Monetary']):
    plt.subplot(2,3,i+1)
    df_rfm[feature].plot(kind='box')
    plt.subplot(2,3,i+1+3)
    df_rfm[feature].plot(kind='hist')

"""**Outliers:** Frequency and Monetary features in above data seem to have lot of outliers. Lets drop them."""

df_rfm = df_rfm[(df_rfm['Frequency']<60) & (df_rfm['Monetary']<40000)]
df_rfm.shape

plt.figure(figsize=(12,6))

for i, feature in enumerate(['Recency', 'Frequency', 'Monetary']):
    plt.subplot(2,3,i+1)
    df_rfm[feature].plot(kind='box')
    plt.subplot(2,3,i+1+3)
    df_rfm[feature].plot(kind='hist')

"""**Log Transformation:** Now since all three features have right skewed data therefore we will use log transformation of these features in our model."""

df_rfm_log_trans = pd.DataFrame()
df_rfm_log_trans['Recency'] = np.log(df_rfm['Recency'])
df_rfm_log_trans['Frequency'] = np.log(df_rfm['Frequency'])
df_rfm_log_trans['Monetary'] = np.log(df_rfm['Monetary']-df_rfm['Monetary'].min()+1)

"""**Standard Scalar Transformation:** It is extremely important to rescale the features so that they have a comparable scale."""

scaler = StandardScaler()

df_rfm_scaled = scaler.fit_transform(df_rfm_log_trans[['Recency', 'Frequency', 'Monetary']])
df_rfm_scaled

df_rfm_scaled = pd.DataFrame(df_rfm_scaled)
df_rfm_scaled.columns = ['Recency', 'Frequency', 'Monetary']
df_rfm_scaled.head()

"""
**b. Build K-Means Clustering Model and Decide the optimum number of clusters to be formed.**"""

# k-means with some arbitrary k
kmeans = KMeans(n_clusters=3, max_iter=50)
kmeans.fit(df_rfm_scaled)

kmeans.labels_

# Finding the Optimal Number of Clusters with the help of Elbow Curve/ SSD
ssd = []
range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for num_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=num_clusters, max_iter=100)
    kmeans.fit(df_rfm_scaled)
    
    ssd.append(kmeans.inertia_)
    
# plot the SSDs for each n_clusters
plt.plot(range_n_clusters,ssd);

# Creating dataframe for exporting to create visualization in tableau later
df_inertia = pd.DataFrame(list(zip(range_n_clusters, ssd)), columns=['clusters', 'intertia'])
df_inertia

# Finding the Optimal Number of Clusters with the help of Silhouette Analysis
range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]

for num_clusters in range_n_clusters:    
    kmeans = KMeans(n_clusters=num_clusters, max_iter=50)
    kmeans.fit(df_rfm_scaled)
    
    cluster_labels = kmeans.labels_
    
    silhouette_avg = silhouette_score(df_rfm_scaled, cluster_labels)
    print("For n_clusters={0}, the silhouette score is {1}".format(num_clusters, silhouette_avg))

"""We can select optimum number of clusters as 3 in our final model"""

# Final model with k=3
kmeans = KMeans(n_clusters=3, max_iter=50)
kmeans.fit(df_rfm_scaled)

"""**c. Analyze these clusters and comment on the results.**"""

# assign the label
df_rfm['Cluster_Id'] = kmeans.labels_
df_rfm.head()

# Box plot to visualize Cluster Id vs Monetary
sns.boxplot(x='Cluster_Id', y='Monetary', data=df_rfm);

# Box plot to visualize Cluster Id vs Frequency
sns.boxplot(x='Cluster_Id', y='Frequency', data=df_rfm);

# Box plot to visualize Cluster Id vs Recency
sns.boxplot(x='Cluster_Id', y='Recency', data=df_rfm);

"""##**Inference:**
**As we can observe from above boxplots that our model has nicely created 3 segements of customer with the interpretation as below:**

- Customers with Cluster Id 0 are less frequent buyers with low monetary expenditure and also they have not purchased anything in recent time and hence least important for business.
- Customers with Cluster Id 1 are the customers having Recency, Frequency and Monetary score in the medium range.
- Customers with Cluster Id 2 are the most frequent buyers, spending high amount and recently placing orders so they are the most important customers from business point of view.
"""

with pd.ExcelWriter('Output.xlsx') as writer:
  df.to_excel(writer, sheet_name='master_data', index=False)
  df_rfm.to_excel(writer, sheet_name='rfm_data', index=False)
  df_inertia.to_excel(writer, sheet_name='inertia', index=False)

product_desc = pd.read_excel("Online Retail.xlsx")
product_desc = product_desc[['StockCode', 'Description']]
product_desc = product_desc.drop_duplicates()
product_desc.to_csv('product_desc.csv', index=False)