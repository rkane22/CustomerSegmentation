import plot

fig1 = plot.plot_customer_spend_v_freq()
fig2 = plot.plot_80_20_rule()
fig3 = plot.plot_unique_customers_per_month()
fig4 = plot.plot_customers_per_time_of_day_per_weekday()
fig5 = plot.plot_kmeans_sse()
fig6 = plot.plot_customer_segments_kmeans()
fig7 = plot.plot_customer_segment_sizes()
fig8 = plot.plot_seasonal_customer_segments()
fig9 = plot.plot_customer_segments_weekdays()

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Customer Segmentation'),
    html.Div(children=[
        html.Div(children=[
            dcc.Markdown('''
            ## The Problem
    
            Identify different groups of customers from a dataset based on some features.

            Create suitable features by performing the data science pipeline 
            (Exploratory Data Analysis, Data Cleaning, Feature Engineering, etc...).
            '''),
        ]),
        html.Div(children=[
            dcc.Markdown('''
            ## The Dataset
            https://www.kaggle.com/sergeymedvedev/customer_segmentation

            The dataset is a collection of invoices from an online ecommerce store.
            
            * Columns:
                - Invoice Number
                - Stock Code
                - Description
                - Quantity
                - Invoice Date
                - Unit Price
                - Customer ID
                - Country

            * Summary:
                - 4,373 identified customers
                - 3,600 unique products
                - 22,190 invoices
            '''),
        ]),

        html.Div(children=[    
            html.Div(children=[
                dcc.Markdown('''
                ## Grouping Customers by Spending Behavior

                Types of spending behavior:
                * Customer’s total spend
                * Number of purchases
                * Recency of purchases

                A customers **total spend** is the total amount of money spend by the customer at the store. 
                A customer that makes very large purchases is obviously a valuable customer, but if those purchases are very infrequent
                or in the case the customer only made one large purchase, that customer is not as valuable as a customer that makes 
                frequent purchases. That is why spending behavior takes into account the number of purchases a customer makes.

                In this case we will not use the recency of a customer's purchases to evaluate them because of the limited time frame of this dataset.

                The following graph visualizes the relationship between a customer's spend and their purchase frequency. The further right a customer 
                is means they make frequent purchases and the further up they are means they spend more money per purchase. Thus the most valuable customers 
                appear more up and to the right.
                '''),
                dcc.Graph(
                    id='Customer Spending',
                    figure=fig1
                ),
            ],style={'width': '49%', 'display': 'inline-block'}),
            html.Div(children=[
                dcc.Markdown(''' 
                ###### 80/20 Rule

                The 80/20 rule is a common rule applied to the topic of customer segmentation. It means that the top 20 percent of customers 
                (by total money spent) account for 80 percent of all revenue. I applied it to this dataset and found it very close to true. 
                '''),
                dcc.Graph(
                    id='80/20 Rule',
                    figure=fig2
                ),
            ],style={'width': '49%', 'display': 'inline-block'})
        ]),

        html.Div(children=[
            dcc.Markdown('''
            ## Time of Year

            This dataset only contains purchases made in 2011, but it covers the entire year. I noticed that there were more customers 
            shopping at the end of the year than any other time. There is a seasonal bump from september to December in the total number of
            customers buying products. This is the bigger reason that I did not choose recency of purchases to be a feature, because most 
            customers would be considered recent buyers when in reality most of them only came to buy during the end of the year.
            '''),
            dcc.Graph(
                id='Unique Customers by Time of Year',
                figure=fig3
            ),
        ]),

        html.Div(children=[
            dcc.Markdown('''
            ## Time of Day/Week

            I analyzed the same metric for each hour on each of the days of the week and found that there were similar peak hours 
            for total customers making purchases every day (Except for Saturday when I assume the store is not open). Thursday has the most
            and Sunday has the least. 
            '''),
            dcc.Graph(
                id='Unique Customers by Time of Day for Each Weekday',
                figure=fig4
            ),
        ]),

        html.Div(children=[
            dcc.Markdown('''
            ## Customer Segments by KMeans Clustering

            I used KMeans clustering to group the customers into teirs of value. I used what is called the "elbow method" to determine the optimal
            number for k. The elbow method is simply to graph the SSE for each k which produces a line that looks somewhat like an arm, and pick the k
            that would be the elbow for that arm. In this case k = 3 was the best value.
            '''),
            dcc.Graph(
                id='KMeans SSE Walk',
                figure=fig5
            ),
            dcc.Markdown('''
            This shows the 3 clusters of customers based on their standardized values for spend and purchase frequency. Group 2 customers are
            the highest value customers, Group 1 are the mid-value customers, and Group 0 are the low-value customers.
            '''),
            dcc.Graph(
                id='KMeans Customer Segments',
                figure=fig6
            ),
            dcc.Markdown('''
            This graph shows the relative size of each of the groups. 
            '''),
            dcc.Graph(
                id='Customer Segment Sizes',
                figure=fig7
            )
        ]),

        html.Div(children=[
            dcc.Markdown('''
            ## Seasonal Customers
            '''),
            dcc.Markdown('''
            I defined a "seasonal" customer to be one that does 90 percent of their shopping in the last 4 months of the year (Sept-Dec). 
            After splitting the customers into seasonal and non-seasonal customers, I broke down those groups by customer value and found 
            that almost all of the seasonal customers are low value customers. This makes sense because low value customers buy less frequently
            and if they are making 90 percent of their purchases at the end of the year they are not likely to be purchasing frequently relative 
            to customers that make purchases all year.
            '''),
             dcc.Graph(
                id='Customer Segments by Season',
                figure=fig8
            ),
        ]),

        html.Div(children=[
            dcc.Markdown('''
            ## Customers for each Weekday
            I defined a customers "favourite" day by the day in which the customer made the most purchases out of the week. The reasoning behind this 
            is that it would probably be the customer's most likely day to shop in he future. I then broke down the customers by value on each of their 
            favourite days. There is a bump on thursdays in high value customers over the other days, and customers of all types shop less on friday 
            and sunday. 
            '''),
            dcc.Graph(
                id='Customer Segments by Weekday',
                figure=fig9
            )
        ]),

        html.Div(children=[
            dcc.Markdown('''
            ## Insights
            The store can focus on retaining its high value and mid value customers.

            The store could promote holidays or events outside of the end of year season to low-value, seasonal, customers. This could lead 
            to them purchasing more frequently and becoming mid-value customers.

            Lastly, The store could have weekend promotions to encourage customers to shop on friday or Sunday since those are the days when the 
            customers shop the least.
            ''')
        ])
    ], style={'marginLeft': '10%', 'marginRight': '20%', 'marginBottom': '40%', 'marginTop': '5%'}),    
    
], style={'margin': '10%'})

if __name__ == '__main__':
    app.run_server(debug=True)