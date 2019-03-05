## Telemarketer Machine Learning Dashboard

Churn-Out is a dashboard application to optimize personalized marketing by showing the best way to reduce the churn rate.

When telemarketer inputs customer ID, it shows the current liklihood of it's termination.

Along with that, it shows a table of all sorts of scenarios that change a certain aspect from TRUE to FALSE or vise versa.

Saying that the customer changes that certain aspect, it shows the change of probability of churn rate, calculated by machine learning.

### Data

As a sample data, we have used the data from [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn) which came from IBM Sample Data Sets.

Within the data, there are people that already have stoped using the service, and those who still are.

We wanted to find out the similarity of people who quit, and then see if there are any current customers who share the same aspects with them.

### Machine Learning

We have used LogisticRegression from sklearn to predict where each customers lies by using their categorical variables.

After we have the current churn rate, we changed each aspects to different state and calculated the difference.

