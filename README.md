## Telemarketer Dashboard for Customer Discontinuation Rates

It is well known that it's much cheaper to keep current customers than acquiring new customers.

If we could calculate the likelihood of a certain customer to discontinue, we can make appropriate action to keep that customer.

**Churn-Out** is a dashboard to optimize personalized marketing by showing the best way to reduce the churn rate.

When telemarketer is connected to a customer, this app would search the customer ID within the database to show the current liklihood of termination.

Along with the current number, it shows a graph of scenarios when a certain aspect of a customer changes to another.

* For example, when a customer changes their payment method from credit card to bank transfer, the Churn Rate would decrease 15%p.*
* Therefore, the telemarketer should promote changing the payment method by providing a coupon to the customer.*

![Frontpage](/images/Frontpage.jpg)

### Data

As a sample data, we have used the data from IBM Sample Data Sets.

The data consists 21 columns, and for the dependent variable, column name "Churn" was used.

Within the "Churn" column, there are customers who has terminated the service, and those who are currently using our service.

We wanted to find out the similarity of people who quit, and then see if there are any current customers who share the same aspects with them.

### Logistic Regression

We have used LogisticRegression from sklearn to predict where each customers lies by using their categorical variables.

After we have the current churn rate, we changed each aspects to different state and calculated the new rate.

### Limitation

The data only has 7043 observations, which is too small to have a good analysis.

This project would only demonstrate the concept of how logistic regression could be used for CRM (Customer Relationship Management).

### Further steps

In an actual environment, when the telemarketer finds a customer to have a high Churn rate, we need to redirect the customer to a risk-management team.

Need to make this a machine learning process to update the model whenever the data is updated.
