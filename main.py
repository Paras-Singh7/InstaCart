import numpy as np
import pandas as pd
import altair as alt

aisles = pd.read_csv('aisles.csv')
departments = pd.read_csv('departments.csv')
order_products_prior = pd.read_csv('order_products__prior.csv')
order_products_train = pd.read_csv('order_products__train.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')

# Exploring data sets
aisles.head()
departments.head()
orders.head()
products.head()
order_products_prior.head()
order_products_train.head()

# Concating order prior and train
order_products = pd.concat([order_products_prior,order_products_train])
order_products.shape

# Creating test, trian, prior set
test = orders[orders['eval_set'] == 'test']
test.head()

train = orders[orders['eval_set'] == 'train']
train.head()

prior = orders[orders['eval_set'] == 'prior']
prior.head()

# Creating final data set
data = pd.merge(orders, order_products, on='order_id')
data.head()

data = pd.merge(data, products, on='product_id')
data.head()

data = pd.merge(data, aisles, on='aisle_id')
data = pd.merge(data, departments, on='department_id')
data.head()

# Explanatory data analysis
from altair import pipe, limit_rows, to_values
t = lambda data: pipe(data, limit_rows(max_rows=1000000000), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')

#How many orders, items, and users are in each eval set?
count = pd.DataFrame(orders.groupby('eval_set')['order_number'].count()) 
count['i'] = count.index
count

n = alt.Chart(count, height = 350, width = 450,title = 'Orders as per Evaluation Set').mark_bar().encode(
    x='i',
    y='order_number',
    color = alt.Color('i', legend=None)
).configure_axis(
    labelFontSize=16,
    titleFontSize=16,
    grid = False
).configure_title(fontSize=24)
n.encoding.y.title = 'Number of Orders'
n.encoding.x.title = 'Evalution set'
n

count = pd.DataFrame(data.groupby('eval_set')['order_number'].count()) 
count['i'] = count.index
count

n = alt.Chart(count, height = 350, width = 450,title = 'Orders as per Evaluation Set').mark_bar().encode(
    x='i',
    y='order_number',
    color = alt.Color('i', legend=None)
).configure_axis(
    labelFontSize=16,
    titleFontSize=16,
    grid = False
).configure_title(fontSize=24)
n.encoding.y.title = 'Number of Orders'
n.encoding.x.title = 'Evalution set'
n

count = pd.DataFrame(orders.groupby('eval_set')['user_id'].nunique())
count['i'] = count.index
count

n = alt.Chart(count, height = 350, width = 450,title = 'Number of Users').mark_bar().encode(
    x='i',
    y='user_id',
    color = alt.Color('i', legend=None)
).configure_axis(
    labelFontSize=16,
    titleFontSize=16,
    grid = False
).configure_title(fontSize=24)
n.encoding.y.title = 'Users'
n.encoding.x.title = 'Evalution set'
n

#How many users in prior appear in train? How many users in prior or train appear in test?
len(pd.Series(list(set(prior['user_id']) & set(test['user_id']))))
len(pd.Series(list(set(prior['user_id']) & set(train['user_id']))))
len(pd.Series(list(set(train['user_id']) & set(test['user_id']))))

#When are orders made?
count = pd.DataFrame(orders.groupby('order_dow')['order_number'].count()) 
count['i'] = count.index + 1
count

n = alt.Chart(count, height = 350, width = 350,title = 'Number of Orders on Each day of Week').mark_bar(size=25).encode(
    x='i',
    y='order_number'
).configure_axis(
    labelFontSize=16,
    titleFontSize=16,
    grid = False
).configure_title(fontSize=24)
n.encoding.y.title = 'Number of order'
n.encoding.x.title = 'Day of the Week'
n

count = pd.DataFrame(orders.groupby('order_hour_of_day')['order_number'].count()) 
count['i'] = count.index + 1
count.head()

n = alt.Chart(count, height = 350, width = 750,title = 'Number of Orders on Each day of Week').mark_bar(size=20).encode(
    x='i',
    y='order_number'
).configure_axis(
    labelFontSize=16,
    titleFontSize=16,
    grid = False
).configure_title(fontSize=24)
n.encoding.y.title = 'Number of order'
n.encoding.x.title = 'Day of the Week'
n

count = pd.DataFrame(orders.groupby('days_since_prior_order')['order_number'].count()) 
count['i'] = count.index + 1
count.head()

alt.Chart(count, width = 750, height = 350).mark_bar(size = 20).encode(
    alt.X("i", title = 'Date'),
    alt.Y("order_number", title='Number of Order')
).configure_axis(
    labelFontSize=16,
    titleFontSize=16,
    grid = False
).configure_title(fontSize = 24)

hourDow = orders.groupby(['order_dow', 'order_hour_of_day'])['order_number'].aggregate('count').reset_index()
hourDow

alt.Chart(hourDow, title='No of order day of week vs hour of day').mark_rect().encode(
    x = alt.X('order_hour_of_day:O', title='Hour of the Day'),
    y = alt.Y('order_dow:O', title='Day of Week'),
    color = 'order_number:Q'
).configure_axis(
    labelFontSize=16,
    titleFontSize=16
).configure_title(
    fontSize = 24
).properties(
    height = 450,
    width = 450
)

#Count of Users by Number of Prior Orders
count = pd.DataFrame(orders.groupby('user_id')['order_number'].aggregate('max').reset_index()) 
count

new = pd.DataFrame(count['order_number'].value_counts())
new['i'] = new.index
new.head()

alt.Chart(new, title='Count of users by number of prior orders').mark_bar().encode(
    alt.X('i', title = 'Number of Prior Orders'),
    alt.Y('order_number', title = 'Number of Users')
).configure_axis(
    labelFontSize = 16,
    titleFontSize = 16,
    grid = False
).configure_title(
    fontSize = 24
).properties(
    height = 400,
    width = 700
).configure_bar(
    color = '#7AAD80'
)

# Distribution of basket size
OrderSize = data.reset_index().groupby(['user_id', 'order_number'])['add_to_cart_order'].aggregate('max')
new = pd.DataFrame(OrderSize.value_counts())
new['i'] = new.index
new

alt.Chart(new, title='Count of users by number of Items in Basket').mark_bar(size = 4).encode(
    alt.X('i', title = 'Number of Items in Basket'),
    alt.Y('add_to_cart_order', title = 'Number of Users')
).configure_axis(
    labelFontSize = 16,
    titleFontSize = 16,
    grid = False
).configure_title(
    fontSize = 24
).properties(
    height = 350,
    width = 750
).configure_bar(
    color = '#FC5959'
)

# Popular Products
countProducts = pd.crosstab(data.product_name, data.eval_set)
countProducts['total'] = countProducts.prior + countProducts.train
count = countProducts.sort_values(by='total', ascending=False).head(25)
count['i'] = count.index
count.head(10)

m = alt.Chart(count, title="Count of Order of prior 25 Most Ordered Product").mark_bar(size = 7).encode(
    alt.X('i', title = 'Product Name'),
    alt.Y('prior', title = 'Count of Orders')
).properties(
    height = 350,
    width = 350
)
n = alt.Chart(count, title="Count of Order of train 25 Most Ordered Product").mark_bar(size = 7).encode(
    alt.X('i', title = 'Product Name'),
    alt.Y('train', title = 'Count of Orders')
).properties(
    height = 350,
    width = 350
)
(m|n).configure_axis(
    labelFontSize = 14,
    titleFontSize = 14,
    grid = False
).configure_title(
    fontSize = 16
)

countAisles = pd.crosstab(data.aisle, data.eval_set)
countAisles['total'] = countAisles.prior + countAisles.train
count = countAisles.sort_values(by='total', ascending=False).head(15)
count['i'] = count.index
count.head()

m = alt.Chart(count, title="Count of Order of prior 15 Most Ordered from Aisles").mark_bar(size = 10).encode(
    alt.X('i', title = 'Product Name'),
    alt.Y('prior', title = 'Count of Orders')
).properties(
    height = 350,
    width = 350
)
n = alt.Chart(count, title="Count of Order of train 15 Most Ordered from Aisles").mark_bar(size = 10).encode(
    alt.X('i', title = 'Product Name'),
    alt.Y('train', title = 'Count of Orders')
).properties(
    height = 350,
    width = 350
)
(m|n).configure_axis(
    labelFontSize = 14,
    titleFontSize = 14,
    grid = False
).configure_title(
    fontSize = 15
)

Ratio of Departments
countDepartment = pd.crosstab(data.department, data.eval_set)
countDepartment['total'] = countDepartment.prior + countDepartment.train
countDepartment['%'] = countDepartment.total / countDepartment.total.sum()
count = countDepartment.sort_values(by='total', ascending=False)
count['i'] = count.index
count.head()

p = alt.Chart(count, title='Proportion of Items Sold from Each Department').mark_point().encode(
    x=alt.X('i', title='Department Name'),
    y=alt.Y('%', title='Total Percentage')
)
t = p.mark_text(
    align='left',
    baseline='middle',
    dy=7,
    fontSize = 12
).encode(
    text='i'
)
(p+t).configure_axis(
    labelFontSize = 14,
    titleFontSize = 14,
    grid = False
).configure_title(
    fontSize = 15
).properties(
    height = 600,
    width = 600
)

# Reorder ratio by departement
count = pd.DataFrame(data.groupby('department')['reordered'].mean())
count['i'] = count.index
count.head()

alt.Chart(count).mark_bar(size = 25).encode(
    alt.X('i', title = 'Department'),
    alt.Y('reordered', title = 'Ratio')
).configure_axis(
    labelFontSize = 16,
    titleFontSize = 16,
    grid = False
).configure_title(
    fontSize = 24
).properties(
    height = 350,
	width = 150
)
   
#Reorder ratio by the hour of the day or the day of the week?
count = data.groupby(['order_dow'])['reordered'].aggregate('mean').reset_index()
count

alt.Chart(count, title='Reorder proportion on Each day of Week').mark_bar(size = 25).encode(
    alt.X('order_dow', title = 'Day of week'),
    alt.Y('reordered', title = 'Reorder Proportion')
).configure_axis(
    labelFontSize = 16,
    titleFontSize = 16,
    grid = False
).configure_title(
    fontSize = 24
).properties(
    height = 350,
    width = 300
).configure_bar(
    color = '#9CABFF'
)

count = data.groupby(['order_hour_of_day'])['reordered'].aggregate('mean').reset_index()
count.head()

alt.Chart(count, title='Reorder proportion on Each Hour of day').mark_bar(size = 20).encode(
    alt.X('order_hour_of_day', title = 'Order of day'),
    alt.Y('reordered', title = 'Reorder Proportion')
).configure_axis(
    labelFontSize = 16,
    titleFontSize = 16,
    grid = False
).configure_title(
    fontSize = 24
).properties(
    height = 350,
    width = 650
).configure_bar(
    color = '#E2A4FF'
)

reorderHourDow = data.groupby(['order_dow', 'order_hour_of_day'])['reordered'].aggregate('mean').reset_index()
reorderHourDow

alt.Chart(reorderHourDow, title='Reorder Proportion by Day of Week vs Hour of Day').mark_rect().encode(
    x = alt.X('order_hour_of_day:O', title='Hour of the Day'),
    y = alt.Y('order_dow:O', title='Day of Week'),
    color=alt.Color('reordered:Q',scale=alt.Scale(scheme='greenblue'))
).configure_axis(
    labelFontSize=16,
    titleFontSize=16
).configure_title(
    fontSize = 24
).properties(
    height = 450,
    width=150
)