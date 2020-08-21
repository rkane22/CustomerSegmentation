import math
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import clean

colors = ['Orange', 'Blue', 'Green']

def plot_customer_spend_v_freq():
    # scatter customers by spend and frequency
    x = 'CustomerFrequency'
    y = 'CustomerSpend'
    c = clean.customerDF
    fig = px.scatter(c[(c.CustomerSpend > 0) & (c.CustomerSpend < 25000) & (c.CustomerFrequency < 100)], x=x, y=y,width=600)
    fig.update_layout(title_text="Customer Purchase Frequency vs Customer Spending")
    return fig

def plot_80_20_rule():
    c = clean.customerDF
    top_cs = c['CustomerSpend'].sort_values(ascending=False)
    label = np.append(
            np.ones(math.floor(len(top_cs.index)*0.2)), 
            np.zeros(math.ceil(len(top_cs.index)*0.8))
        )
    d = {
        'Biggest Spenders': ['Top 20%', 'Bottom 80%'],
        'Size': [len(top_cs.index) * 0.2, len(top_cs.index) * 0.8],
        'Spending': [
            top_cs[label == 1].sum(),
            top_cs[label == 0].sum()
        ]
    }
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(
        go.Bar(x=d['Biggest Spenders'], y=d['Size'], name="Group Size"),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=d['Biggest Spenders'], y=d['Spending'], name="Spending"),
        row=2, col=1
    )
    fig.update_layout(title_text="80/20 Rule, Group Spending vs Group Size")
    # fig = px.bar(d, x='Biggest Spenders', y='Size', color='Spending')
    return fig

def plot_unique_customers_per_month():
    # Analyze Shopping By Month
    invoices = clean.invoices
    Months = clean.Months
    by_Month = invoices.groupby(by="month")["CustomerID"].nunique()
    by_Month = pd.DataFrame({'Months': Months,
                            '# of Unique Customers': by_Month})
    fig = px.bar(by_Month, x=by_Month['Months'], y=by_Month['# of Unique Customers'])
    return fig

def plot_customers_per_time_of_day_per_weekday():
    df = clean.invoices
    weekdays = []
    hours = []
    num_cs = []
    total_spend = []
    for weekday in range(0, len(clean.Days)):
        for hour in clean.Hours:
            weekdays.append(clean.Days[weekday])
            hours.append(hour)
            num_cs.append(df[(df.weekday==weekday)& (df.hour == hour)]['CustomerID'].nunique())
            total_spend.append(df[(df.weekday==weekday) & (df.hour == hour)]['TotalPrice'].sum())
    
    df = pd.DataFrame({
        'Weekday': weekdays,
        'Hour': hours,
        '# of Unique Customers': num_cs,
        'Total Spent': total_spend
    })
    fig = px.line(df, x='Hour', y='# of Unique Customers', color='Weekday')
        
        # fig.add_trace(
        #     go.Scatter(df, x=df['Hour'][day], y=df['Total Spent'][day], mode='lines'),
        #     row=1, col=2
        # )
    
    # fig.update_layout(title_text="80/20 Rule, Group Spending vs Group Size")

    return fig

def plot_kmeans_sse():
    fig = px.line(
            {
                "# of K's": clean.ks, 
                "SSE": clean.sse
            },
            x="# of K's",
            y="SSE"
        )
    return fig

def plot_customer_segments_kmeans():
    clean.customerDF_NO['Groups'] = clean.customerDF_NO['Group'].apply(str)
    fig = px.scatter(clean.customerDF_NO, x='CustomerFrequency', y='CustomerSpend', color='Groups')
    return fig

def plot_customer_segment_sizes():
    groups = clean.customerDF_NO.groupby(by='Groups').count()
    df = pd.DataFrame({
        'Group': groups.index,
        'Size': groups['CustomerSpend']
    })
    fig = px.bar(df, x='Group', y='Size', color='Group')
    return fig

def plot_seasonal_customer_segments():
    groups = []
    seasonal = []
    count = []
    for g in range(0, clean.k):
        group = clean.customerDF_NO[clean.customerDF_NO.Group == g].groupby(by='SeasonalCustomer').count()
        groups.append(str(g))
        groups.append(str(g))
        seasonal.append('Seasonal')
        seasonal.append('Non-Seasonal')
        if(group.empty):
            count.append(0)
            count.append(0)
        else:
            count.append(group['CustomerID'][0])
            count.append(group['CustomerID'][1])
    
    df = pd.DataFrame({
        'Seasonal': seasonal,
        'Group': groups,
        '# of Customers': count
    })

    fig = px.bar(df, x='Seasonal', y='# of Customers', color='Group', barmode='group')
    return fig

def plot_customer_segments_weekdays():
    groups = []
    weekdays = []
    count = []
    for g in range(0, clean.k):
        group = clean.customerDF_NO[clean.customerDF_NO.Group == g].groupby(by='CustomerFavDay').count()
        for weekday in range(0, len(clean.Days)):
            groups.append(str(g))
            weekdays.append(clean.Days[weekday])
            if weekday == 5:
                count.append(0)
            else:
                count.append(group['CustomerID'][weekday])
    
    df = pd.DataFrame({
        "Customer's Favourite Weekday": weekdays,
        'Group': groups,
        '# of Customers': count
    })
    fig = px.bar(df, x="Customer's Favourite Weekday", y='# of Customers', color='Group', barmode='group')
    return fig

def plot_customers_by_country_per_month():
    return

def plot_seasonal_customer_segments_per_country():
    return