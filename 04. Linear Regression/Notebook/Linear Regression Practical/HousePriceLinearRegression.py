#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis:
# 1. Understanding the data
#    a. df.shape - rows and column number
#    b. df.head() - check to give 5 rows
#    c. df.columns - what all columns
#    d. df.info() - column name, dtypes
#    e. df.describe() - summary satistics
#    f. df.isnull().sum() - check for missing 
#    g. df.column_name.value_counts() - check the number of each unique data under column
#    h. df.duplicated.sum() - Check for duplication
#    i. df.plot(kind = 'box') - Check for outlier
#    j. df.corr() - Correlation
# 
# 2. Visualization (univariate and bivariate) (Descriptive Analytics - what is happening in the past):
# 
#    Univariate
#    a. Histogram
#    b. Pie chart
#    c. Box plot
#    
#    Bivariate:
#    a. Scatter Plot
#    b. Bar Plot
#    c. Pair Plot
# 
# # Data Preprocessing:
# 1. Handling Missing values
# 2. Handling Outlier values
# 3. Remove Noisy data
# 4. Dropping unwanted columns
# 5. Dropping Duplicates
# 6. Encoding of Categorical data
# 7. Feature scaling on Numerical data(Standardisation/ Normalisation)
# 8. Feature Engineering
# 9. Feature Selection
# 
# # Split the data
# 1. Train and Test Spilt
# 
# # Model
# 1. Model on Train  data
# 2. Finetune the Model
# 3. Finalize the Model
# 
# # Predict the result
# 1. Predict the Train
# 2. Predict the Test
# 
# # Evalution
# 1. Evaluation of Train data (Error Metrics)
# 2. Evaluation of Test data
# 
# # Comparison
# 1. Compare the train and test results based on that take the decision to iterate the step from Data preprocessing
# 
# # Deploy the Model
# # End Point
# 
# # Monitoring
# 
# # Retraining (on sufficient interval)

# In[321]:


# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score

from sklearn.feature_selection import SelectKBest, f_regression
pd.options.display.float_format = '{:.2f}'.format


# In[ ]:


#Outlier - Standard scaler - persisted


# In[4]:


# Load the data
data = pd.read_csv('housing_prices_dataset.csv')


# In[5]:


data


# # Understanding the data

# In[7]:


data.columns


# In[8]:


data.dtypes


# In[9]:


data.shape


# In[10]:


data.info()


# In[11]:


data.describe()


# In[12]:


# IPL Team Owner

# 2 Players

# 1st Player
# Batting Average = 60
# STD             = 50

# 2nd Player
# Batting Average = 40
# STD             = 5

# Player 1 = 10 - 110
# Player 2 = 35 - 45


# In[13]:


# Row Duplication
data.duplicated().sum()


# In[14]:


data.isnull().sum()


# In[ ]:





# In[15]:


data.drop(columns = ['Price','Size']).plot(kind = 'box')


# In[16]:


num_col = data.select_dtypes(include='number').columns


# In[17]:


for col in num_col:
    print(col)
    sns.boxplot(data[col])
    plt.show()


# In[18]:


data.head()


# In[19]:


data['Bedrooms'].plot(kind = 'box')


# In[20]:


sns.boxplot(data['Bedrooms'])


# In[21]:


data[num_col].corr()


# In[22]:


sns.heatmap(data[num_col].corr(), annot = True)


# In[23]:


# EDA


# In[24]:


data['Size'].hist(bins = 100)


# In[ ]:





# In[25]:


# 2,5,6,8,10,20,40
# 2-5  - 2
# 6-8  - 2
# 9-11 - 1
# 12-14 - 0
# 15-17 - 0
# 18-20  - 1
# 21-23



# 37-40 - 1


# In[26]:


#Bivariate
sns.pairplot(data[num_col])


# In[27]:


data['Bedrooms'].value_counts()


# In[28]:


data['Bedrooms'].value_counts().plot(kind = 'pie')


# In[29]:


data.groupby('Bedrooms').Price.mean()


# In[30]:


data.groupby('Bedrooms').Price.mean().plot(kind = 'bar')


# In[31]:


data.groupby('Bathrooms').Price.mean().plot(kind = 'bar')


# In[32]:


data.groupby(['Bedrooms','Neighborhood','Bathrooms']).Price.mean().to_csv('result.csv')


# In[33]:


plt.scatter(data['Bedrooms'], data['Price'])
plt.savefig('bathrooms_price_scatter.png')


# In[34]:


sns.scatterplot(x = data['Size'], y = data['Price'], hue=data['Bedrooms'], size=data['Bathrooms'])
plt.savefig('bathrooms_bedrooms_size_price_scatter.png')


# # Pre-Processing

# In[36]:


data.isna().sum()


# In[37]:


data.shape


# 1. Impute the Bedrooms with mode
# 2. Impute the Bathrooms with respect to Bedrooms 
# 3. Drop the rows with null HasGarage

# In[39]:


data['Bedrooms'].mode()[0]


# In[40]:


data['Bedrooms'].mean()


# In[41]:


data['Bedrooms'].fillna(data['Bedrooms'].mode()[0], inplace = True)
data['Bathrooms'].fillna(data['Bathrooms'].mode()[0], inplace = True)
data['HasGarage'].fillna(data['HasGarage'].mode()[0], inplace = True)


# 1
# 1
# 1
# 2
# 2
# 2
# 3
# 3
# 3
# 
# Mode = 1,2,3 
# 
# Mean  = can be only one
# Median  = can be only one
# Mode = can be one or more than one
# 
# Mean = may or may not be inside the data
# Median = May or may not be inside the data
# Mode = Will be inside the data
# 
# 
# 1,2,3,4,5 = 3
# 1,2,3,4  = 2.5
# 

# In[43]:


data['Bedrooms'].mode()


# In[44]:


data.isna().sum()


# In[45]:


data[data['Size']>9000]


# In[46]:


data = data[data['Size']<9000]


# In[47]:


sns.pairplot(data)


# In[48]:


data[num_col].corr()


# In[49]:


data


# In[50]:


data['HouseAge'] = 2024 - data['YearBuilt'] 


# In[51]:


data['HouseAge']


# In[52]:


data.drop(columns = 'YearBuilt', inplace = True)


# In[53]:


num_col = data.select_dtypes(include = 'number').columns


# In[54]:


data[num_col].corr()


# In[55]:


data.head()


# In[56]:


data['LuxuryRating'].value_counts()


# In[57]:


mapping = {'Low':1, 'Medium':2, 'High':3}


# In[58]:


data['LuxuryRating'] = data['LuxuryRating'].map(mapping)


# In[59]:


data.head()


# In[60]:


data['Neighborhood'].value_counts()


# In[61]:


#OneHot Encoding

data = pd.get_dummies(data, columns=['Neighborhood'],dtype='int' )


# In[62]:


data


# In[ ]:





# # Scaling

# In[130]:


scaling = StandardScaler()


# In[134]:


X = data.drop(columns='Price')


# In[136]:


X.columns


# In[138]:


scaled_features = X.columns


# In[140]:


data[scaled_features] = scaling.fit_transform(data[scaled_features])


# In[142]:


data


# In[144]:


data.corr()


# In[150]:


X = data.drop(columns = 'Price')
y = data['Price']


# # Data Split

# In[154]:


train_X, test_X, train_y, test_y = train_test_split(X,y, test_size=0.3, random_state=31)


# # Model

# In[157]:


model = LinearRegression()


# In[159]:


model.fit(train_X, train_y)


# In[161]:


model.coef_


# In[169]:


pd.Series(model.coef_, index = X.columns).plot(kind = 'bar')


# In[171]:


model.intercept_


# # Prediction

# In[174]:


train_pred = model.predict(train_X)
test_pred = model.predict(test_X)


# # Evaluation

# In[323]:


def evaluate(actual, pred, source):
    print(source)
    print("MSE")
    print(mean_squared_error(actual, pred))
    print("RMSE")
    print(np.sqrt(mean_squared_error(actual, pred)))
    print("MAPE")
    print(mean_absolute_percentage_error(actual, pred)) 
    print("R2 score")
    print(r2_score(actual, pred)) 
    return [mean_squared_error(actual, pred), np.sqrt(mean_squared_error(actual, pred)), r2_score(actual, pred), mean_absolute_percentage_error(actual, pred)]


# In[325]:


train_result = evaluate(train_y, train_pred, 'TRAIN DATA RESULT')
test_result = evaluate(test_y, test_pred, 'TEST DATA RESULT')


# In[223]:


train_result


# In[225]:


test_result


# In[227]:


res = [train_result] + [test_result]


# In[229]:


res


# In[231]:


pd.DataFrame(res, columns=['MSE','RMSE','MAPE'], index = ['Train', 'Test'])


# In[242]:


X.shape


# # Feature Selection

# In[244]:


select_k_best = SelectKBest(f_regression, k= 5 )


# In[246]:


X_select = select_k_best.fit_transform(X,y)


# In[251]:


select_k_best.get_support()


# In[253]:


X.columns


# In[257]:


selected_feature_names = X.columns[select_k_best.get_support()]


# In[259]:


selected_feature_names


# In[ ]:





# In[ ]:





# In[ ]:





# # Model After Feature Selection

# In[ ]:





# In[282]:


X = X[selected_feature_names]


# In[284]:


X = X[selected_feature_names]
y = data['Price']


# # Data Split

# In[287]:


train_X, test_X, train_y, test_y = train_test_split(X,y, test_size=0.3, random_state=31)


# # Model

# In[327]:


train_X.shape


# In[329]:


model = LinearRegression()


# In[331]:


model.fit(train_X, train_y)


# In[333]:


model.coef_


# In[335]:


pd.Series(model.coef_, index = X.columns).plot(kind = 'bar')


# In[337]:


model.intercept_


# # Prediction

# In[340]:


train_pred = model.predict(train_X)
test_pred = model.predict(test_X)


# # Evaluation

# In[345]:


def evaluate(actual, pred, source):
    print(source)
    print("MSE")
    print(mean_squared_error(actual, pred))
    print("RMSE")
    print(np.sqrt(mean_squared_error(actual, pred)))
    print("MAPE")
    print(mean_absolute_percentage_error(actual, pred)) 
    print("R2 score")
    print(r2_score(actual, pred)) 
    return [mean_squared_error(actual, pred), np.sqrt(mean_squared_error(actual, pred)), r2_score(actual, pred), mean_absolute_percentage_error(actual, pred)]


# In[347]:


train_result = evaluate(train_y, train_pred, 'TRAIN DATA RESULT')
test_result = evaluate(test_y, test_pred, 'TEST DATA RESULT')


# In[349]:


train_result


# In[351]:


test_result


# In[353]:


res = [train_result] + [test_result]


# In[355]:


res


# In[357]:


pd.DataFrame(res, columns=['MSE','RMSE','R2 Score','MAPE'], index = ['Train', 'Test'])


# In[ ]:





# In[ ]:




