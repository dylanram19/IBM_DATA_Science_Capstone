#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np


# In[2]:


df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)


# In[3]:


# Calculate percentage of each missiing value for columns
df.isnull().sum()/df.count()*100


# In[4]:


# identify which columns are numerical or categorical
df.dtypes


# In[6]:


# Apply value_counts() on column LaunchSite
df['LaunchSite'].value_counts()


# In[7]:


# Apply value counts on orbit column
df['Orbit'].value_counts()


# In[34]:


#Use method value_counts() on Outcome to determine the number of landing_outcomes then assign to a variable landing_outcomes
landing_outcomes = df['Outcome'].value_counts();


# In[13]:


#True Ocean means the mission outcome was successfully landed to a specific region of the ocean while False Ocean means 
#the mission outcome was unsuccessfully landed to a specific region of the ocean. #True RTLS means the mission outcome 
#was successfully landed to a ground pad False RTLS means the mission outcome was unsuccessfully landed to a ground pad.
#True ASDS means the mission outcome was successfully landed to a drone ship False ASDS means the mission outcome was 
#unsuccessfully landed to a drone ship. None ASDS and None None these represent a failure to land.
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)


# In[14]:


# Create a set of outcomes where second landing was unsuccesful

bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes


# In[25]:


#  Create a list using Outcomes where landing_class = 0 if bad_outcome landing_class = 1 otherwise

landing_class=[]
for i in df['Outcome']:
    if i in bad_outcomes:
        landing_class.append(0)
    else: landing_class.append(1)


# In[26]:


df['Class']=landing_class
df[['Class']].head(8)


# In[27]:


df.head(5)


# In[28]:


# determinen success rate

df["Class"].mean()


# In[29]:


df.to_csv("dataset_part_2.csv", index=False)


# In[ ]:




