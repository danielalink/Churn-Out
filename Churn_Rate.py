import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")
import io

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


def ML_model():
    #########Importing libraries##########


    ########Bring in the DATA!###########

    telcom = pd.read_csv("dataset/Telemarker.csv")

    #######Data Cleaning Process#########

    #Replacing spaces with null values in total charges column
    telcom['TotalCharges'] = telcom["TotalCharges"].replace(" ",np.nan)

    #Dropping null values from total charges column which contain 0.16%
    telcom = telcom[telcom["TotalCharges"].notnull()]
    telcom = telcom.reset_index()[telcom.columns]

    #convert to float type
    telcom["TotalCharges"] = telcom["TotalCharges"].astype(float)
    telcom["MonthlyCharges"] = telcom["MonthlyCharges"].astype(float)

    #replace 'No phone service' to No
    telcom["MultipleLines"] = telcom["MultipleLines"].replace("No phone service","No")

    #replace 'No internet service' to No for the following columns
    replace_cols = [ 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport','StreamingTV', 'StreamingMovies']

    for i in replace_cols : 
        telcom[i]  = telcom[i].replace({'No internet service' : 'No'})

    #Separating catagorical and numerical columns
    Id_col     = ['customerID']
    target_col = ["Churn"]
    cat_cols   = telcom.nunique()[telcom.nunique() < 6].keys().tolist()
    cat_cols   = [x for x in cat_cols if x not in target_col]
    num_cols   = [x for x in telcom.columns if x not in cat_cols + target_col + Id_col]

    #Binary columns with 2 values
    bin_cols   = telcom.nunique()[telcom.nunique() == 2].keys().tolist()

    # #Columns more than 2 values
    multi_cols = [i for i in cat_cols if i not in bin_cols]

    # #Label encoding Binary columns
    le = LabelEncoder()
    for i in bin_cols :
        telcom[i] = le.fit_transform(telcom[i])
        
    # #Duplicating columns for multi value columns
    telcom = pd.get_dummies(data = telcom,columns = multi_cols)

    # #Scaling Numerical columns
    std = StandardScaler()
    scaled = std.fit_transform(telcom[num_cols])
    scaled = pd.DataFrame(scaled,columns=num_cols)

    # #dropping original values merging scaled values for numerical columns
    telcom = telcom.drop(columns = num_cols,axis = 1)
    telcom = telcom.merge(scaled,left_index=True,right_index=True,how = "left")

    ######Model Building######

    # splitting train and test data 
    train,test = train_test_split(telcom,test_size = .20 ,random_state = 42)
        
    ##seperating dependent and independent variables
    cols    = [i for i in telcom.columns if i not in Id_col + target_col]
    X_train = train[cols]
    y_train = train[target_col]
    X_test  = test[cols]
    y_test  = test[target_col]

    # Logistic Regression
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    coefficient = classifier.coef_

    telcom1 = telcom.drop(["Churn"],axis = 1)
    df = telcom1.set_index("customerID")

    column_names = list(df.columns.values)

    return classifier, df


classifier,df = ML_model()

#Calculate Original Churn Rate
def calculate(array):
    result = round(100*classifier.predict_proba(array)[0][1],2)
    if result >= 0:
        return result
    else:
        return 0

def change_to_YN(value):
    if value == 0:
        return("N")
    if value == 1:
        return("Y")


#Calculate Original %

def origin_prob(customerID):
    output = calculate(df.loc[[customerID]])
    return(output)
    

def compare_scenario(customerID):
    _input = df.loc[[customerID]]
    columns = df.columns.drop(["gender","tenure","SeniorCitizen","Dependents","Partner"])

    scenario = {}
    for i in range(20):
        _input = df.loc[[customerID]]
        _input.iloc[:,i] = 1-_input.iloc[:,i]
        scenario[columns[i]+" ("+change_to_YN(_input.iloc[:,i].values[0])+")"] = round(calculate(_input),2)
    # print(scenario)
    return scenario

