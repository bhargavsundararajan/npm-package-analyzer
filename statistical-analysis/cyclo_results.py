import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pickle

###################################
# EDIT THESE CONSTANTS
###################################

GROUP = "ecs260-43"
DB_PASSWORD = "wintry-churn-provost-actually"

ANALYZER_NAME = f"{GROUP}/cyclomatic"
ANALYZER_VERSION = "0.2.0"
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
#print(job_df['repo_url'])
result_df = job_df[['extra','repo_url']]
#print(result_df)
pickle.dump(result_df, open("result_cyclo.pkl","wb"))
print("Result dumped in pickle")
