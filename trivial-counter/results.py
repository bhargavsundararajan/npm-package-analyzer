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

ANALYZER_NAME = f"{GROUP}/trivial"
ANALYZER_VERSION = "0.0.3"
CORPUS_NAME = "r2c-1000"

###################################
# END EDIT SECTION
###################################

# Canonical SQL query to get job-specific results back.
JOB_QUERY = """
SELECT *
FROM   result,
       commit_corpus
WHERE  result.commit_hash = commit_corpus.commit_hash
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
#print("Raw job dataframe:")
#print(job_df[0])

# Helper method to compute % whitespace from the num_whitespace and size fields in our 'extra' column
total = 0
trivial = 0
def checkTrivial(row):
    global total	
    total += 1
    if row.extra["LOC"] <= 35 and row.extra["Cyclomatic"] <= 10:
        global trivial
        trivial += 1
        return 1
    # Avoid 'division by zero' exceptions.
    return 0

# Add 'percent_whitespace' column
job_df['Trivial'] = job_df.apply(checkTrivial, axis=1)

percentage = (trivial/total)*100
print("Percent of trivial packages:")
print(percentage)	
print(trivial)
print(total)

# Create a histogram of our data using the `percent_whitespace` column
#job_df.hist(column="percent_whitespace", bins=100)
#plt.show()
