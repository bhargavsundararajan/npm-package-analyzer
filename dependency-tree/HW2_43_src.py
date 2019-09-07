#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Result Analyzer

import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

###################################
# EDIT THESE CONSTANTS
###################################

GROUP = "ecs260-43"
DB_PASSWORD = "wintry-churn-provost-actually"

ANALYZER_NAME = "r2c/js-dependencies"
ANALYZER_VERSION = "1.0.3"
CORPUS_NAME = "r2c-1000-monthly"

###################################
# END EDIT SECTION
###################################

# Canonical SQL query to get job-specific results back.
JOB_QUERY = """
SELECT * 
FROM   result, 
       commit_corpus,
       commit_metadata
WHERE  result.commit_hash = commit_corpus.commit_hash
       AND result.commit_hash = commit_metadata.commit_hash
       AND analyzer_name = %(analyzer_name)s 
       AND analyzer_version = %(analyzer_version)s
       AND corpus_name = %(corpus_name)s
"""

QUERY_PARAMS = {
    "corpus_name": CORPUS_NAME,
    "analyzer_name": ANALYZER_NAME,
    "analyzer_version": ANALYZER_VERSION
}

# Connect to PostgreSQL host and query for job-specific results
engine = create_engine(f'postgresql://notebook_user:{DB_PASSWORD}@{GROUP}-db.massive.ret2.co/postgres')
job_df = pd.read_sql(JOB_QUERY, engine, params=QUERY_PARAMS)

# Print pandas dataframe to stdout for debugging
print("Raw job dataframe:")
print(job_df[1:10])


# In[ ]:


#write dataframe to csv
file_name = r'C:\Users\bharg\Downloads\result_and_metadata.csv'
job_df.to_csv(file_name)


# In[ ]:


#read from csv
import pandas as pd

data = pd.read_csv(r'C:\Users\bharg\Downloads\result_and_metadata.csv')


# In[ ]:


#Prepare new dataframe with only relevant information
from ast import literal_eval

deps = []
vers = []
urls = []
times = []

for index, row in data.iterrows():
    try:
        extra = literal_eval(row[11])
    except:
        print("Error converting")
        break
    
    try:
        dep = extra['name']
    except:
        continue
        
    try:
        ver = extra['resolvedVersion']
    except:
        ver = extra['specifiedVersion']
    
    try:
        url = row[13]
    except:
        continue
    
    try:
        time = row[16]
    except:
        continue
    
    deps.append(dep)
    vers.append(ver)
    urls.append(url)
    times.append(time)
    

print(vers)


# In[132]:


#convert string to datetime
from datetime import datetime

dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in times]


# In[ ]:


#Create the required dataframe
df_data = pd.DataFrame({'Dependencies': deps, 'Versions': vers, 'Package_URL': urls, 'Committed_at': dates})
print(df_data)


# In[134]:


#save dataframe to local disk
df_data.to_pickle(r"C:\Bhargav files\MS\UC Davis\Courses\ECS 260 - Software Engineering\HW2\data.pkl")


# In[ ]:


#Function for comparing two dependency versions
def ver_check(ver1, ver2):
    lis1 = ver1.split('.')
    lis2 = ver2.split('.')
    for i in range(0,3):
        x = int(lis1[i])
        y = int(lis2[i])
        if x > y:
            return 1
        elif y > x:
            return -1
    return 0


# In[ ]:


#function for normalizing a version to standard form
def red_str(str):
    flag = 0
    s_lis = []
    for c in str:
        try:
            temp = int(c)
        except:
            if flag == 1:
                flag = -1
            continue
        if flag == 0 or flag == 1:
            s_lis.append(c)
            flag = 1
        elif flag == -1:
            break
    if len(s_lis) == 0:
        return '1'
    return ''.join(s_lis)
        

def normalize_ver(ver):
    lis = ver.split('.')
    for i in range(0, len(lis)):
        try:
            temp = int(lis[i])
        except:
            if i == 0:
                if len(lis[i]) > 5:
                    lis[i] = '1'
                    continue
                lis[i] = red_str(lis[i])
                i = i - 1
                continue
            else:
                lis[i] = '0'
                continue
    for i in range(0, 3 - len(lis)):
        lis.append('0')
    ver = '.'.join(lis[0:3])
    return ver


# In[135]:


#Read data from file and apply version normalization
df_data = pd.read_pickle(r"C:\Bhargav files\MS\UC Davis\Courses\ECS 260 - Software Engineering\HW2\data.pkl")
df_data['Versions'] = df_data['Versions'].apply(normalize_ver)


# In[ ]:


#Calculate the first commit date for latest version of each dependency

import pandas as pd
#df_data = pd.read_pickle(r"C:\Bhargav files\MS\UC Davis\Courses\ECS 260 - Software Engineering\HW2\data.pkl")
deps_dict = {}
def update_deps_dict(row):
    if row['Dependencies'] in deps_dict:
        ver_cmp = ver_check(deps_dict[row["Dependencies"]]["version"], row["Versions"])
        if  ver_cmp == 0:
            if deps_dict[row["Dependencies"]]["time"] > row["Committed_at"]:
                deps_dict[row["Dependencies"]]["time"] = row["Committed_at"]
        elif ver_cmp == -1:
            deps_dict[row["Dependencies"]]["version"] = row["Versions"]
            deps_dict[row["Dependencies"]]["time"] = row["Committed_at"]
    else:
        deps_dict.update({row["Dependencies"] : {"version": row["Versions"], "time": row["Committed_at"]}})
df_data.apply(update_deps_dict, axis = 1)


# In[139]:


#calculate the first commit of lastest version of dependencies of each package

packs_dict = {}
def update_packs_dict(row):
    if row['Package_URL'] in packs_dict:
        if row['Dependencies'] in packs_dict[row['Package_URL']]:
            ver_cmp = ver_check(packs_dict[row["Package_URL"]][row["Dependencies"]]["version"], row["Versions"])
            if ver_cmp == 0:
                if packs_dict[row["Package_URL"]][row["Dependencies"]]["time"] > row["Committed_at"]:
                    packs_dict[row["Package_URL"]][row["Dependencies"]]["time"] = row["Committed_at"]
            elif ver_cmp == -1:
                packs_dict[row["Package_URL"]][row["Dependencies"]]["version"] = row["Versions"]
                packs_dict[row["Package_URL"]][row["Dependencies"]]["time"] = row["Committed_at"]
        else:
            packs_dict[row['Package_URL']].update({row["Dependencies"] : {"version": row["Versions"], "time": row["Committed_at"]}})
    else:
        packs_dict.update({row['Package_URL']: {row["Dependencies"]: {"version": row["Versions"], "time": row["Committed_at"]}}})
def pack_func(pack):
    pack.apply(update_packs_dict, axis = 1)
df_data.groupby(["Package_URL","Dependencies"]).apply(pack_func)


# In[140]:


#store first commit data to disk
import pickle
pickle.dump(deps_dict, open(r"C:\Bhargav files\MS\UC Davis\Courses\ECS 260 - Software Engineering\HW2\deps_dict.pkl",'wb'))
pickle.dump(packs_dict, open(r"C:\Bhargav files\MS\UC Davis\Courses\ECS 260 - Software Engineering\HW2\packs_dict.pkl",'wb'))


# In[141]:


#calculate time lag by finding difference between latest available version and the package dependency version

results = {}
for pack in packs_dict:
    max_diff = None
    for dep in packs_dict[pack]:
        diff = deps_dict[dep]['time'] - packs_dict[pack][dep]['time']
        if max_diff == None:
            max_diff = diff
        elif diff > max_diff:
            max_diff = diff
    results.update({pack: max_diff})


# In[145]:


#store results to disk
pickle.dump(results, open(r"C:\Bhargav files\MS\UC Davis\Courses\ECS 260 - Software Engineering\HW2\results.pkl",'wb'))


# In[150]:


#extract the results to a dataframe
pack = []
tlag = []
for result in results:
    pack.append(result)
    days = results[result].days 
    tlag.append(days)


# In[222]:


#Identify top 10 laggiest packages
result_dt = pd.DataFrame({"Package": pack, "TLag" : tlag})
def fix_neg(lag):
    if lag < 0:
        return 0
    else:
        return lag
result_dt['TLag'] = result_dt['TLag'].apply(fix_neg)
result_dt = result_dt.sort_values(by = 'TLag', ascending = False)
result_dt = result_dt.reset_index(drop = True)
result_dt.head(10)


# In[215]:


#plot frequency distribution of lag for each package
bins= [0,500,1000,1500,2000,2500]
plt.hist(result_dt.TLag, bins=bins, edgecolor="k")
plt.xticks(bins)
plt.xlabel('TLag (days)')
plt.ylabel('Frequency')
plt.show()

