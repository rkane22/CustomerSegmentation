import pandas as pd
import numpy as np

invoices = pd.read_csv('../customer_segmentation.csv', encoding = "latin-1")

invoices = invoices[["CustomerID", "StockCode", "Description", "Quantity", "UnitPrice", "Country", "InvoiceDate", "InvoiceNo"]]

# get rid of unknown customer for now
invoices = invoices.dropna(subset=['CustomerID'])
# calculate total spent per invoice
invoices["TotalPrice"] = invoices["Quantity"] * invoices["UnitPrice"]

from datetime import datetime
# clean the date
invoices["InvoiceDate"] = pd.to_datetime(invoices["InvoiceDate"])
# month
invoices["month"] = [d.month for d in invoices["InvoiceDate"]]
# hour in day
invoices["hour"] = [d.hour for d in invoices["InvoiceDate"]]
# weekday
invoices["weekday"] = [d.weekday() for d in invoices["InvoiceDate"]]

invoices["Country"] = invoices["Country"].apply(lambda x: "U.K." if x == "United Kingdom" else "Other")

# List of customers by ID
customers = invoices.groupby(by="CustomerID")
customer_spent = customers["TotalPrice"].sum()
customer_invoices = customers["InvoiceNo"].agg("nunique")
s_months = invoices[invoices.month >= 9].groupby(by="CustomerID").count()["month"]
a_months = invoices.groupby(by="CustomerID").count()["month"]
customer_seasonal = s_months.divide(a_months, fill_value=0) > 0.9
customer_from_uk = customers["Country"].agg(lambda x:x.value_counts().index[0]) == "U.K."
customer_hour =  customers["hour"].agg(lambda x:x.value_counts().index[0])
customer_day =  customers["weekday"].agg(lambda x:x.value_counts().index[0])

customerDF = pd.DataFrame(
    {
        'CustomerID': customer_spent.index,
        'CustomerSpend': customer_spent,
        'CustomerFrequency': customer_invoices,
        'SeasonalCustomer': customer_seasonal,
        'CustomerFromUK': customer_from_uk,
        'CustomerFavHour': customer_hour,
        'CustomerFavDay': customer_day
    }
)

from scipy.stats import zscore


# standardize values
customerDF_Std = customerDF.copy(deep=True)
customerDF_Std['CustomerSpend'] = zscore(customerDF["CustomerSpend"])
customerDF_Std['CustomerFrequency'] = zscore(customerDF["CustomerFrequency"])

customerDF_NO = customerDF_Std[
    (np.abs(customerDF_Std.CustomerSpend) < 3)
    & (np.abs(customerDF_Std.CustomerFrequency) < 3)
]

from sklearn.cluster import KMeans

x = 'CustomerFrequency'
y = 'CustomerSpend'
df = pd.DataFrame({x: customerDF_NO[x], 
                   y: customerDF_NO[y]})

sse = []
# determine the best value for k (1-10)
ks = range(1, 10)
for k in ks:
    km = KMeans(n_clusters=k)
    km.fit(df)
    sse.append(km.inertia_)

# elbow method determines 3
k = 3
km=KMeans(n_clusters=k)
labels = km.fit_predict(df)
customerDF_NO['Group'] = labels

group_size = []
for g in range(0, k):
    group_size.append(len(customerDF_NO[customerDF_NO.Group == g]))

Months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
Days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
Hours = range(6, 21)

num_cs = len(customerDF_NO.index)