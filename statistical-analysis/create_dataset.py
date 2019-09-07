import pandas as pd
from functools import reduce

cyclo = pd.read_pickle("result_cyclo.pkl")
lag = pd.read_pickle("result_lag.pkl")
depth = pd.read_pickle("result_depth.pkl")
dict = {}

def create_depth_df(row):
    if row['repo_url'] not in dict.keys():
        dict[row['repo_url']] = {'loc': 'none', 'cyclo': 'none', 'depth': row['extra']['depth'], 'lag': 'none'}

depth.apply(create_depth_df, axis = 1)


for key in lag:
    dict[key]['lag'] = lag[key].days


def create_cyclo_df(row):
    dict[row['repo_url']]['loc'] = row['extra']['LOC']
    dict[row['repo_url']]['cyclo'] = row['extra']['Cyclomatic']

cyclo.apply(create_cyclo_df, axis = 1)

pop_keys = []
for key in dict:
    repo = dict[key]
    if repo['loc'] == 'none' or repo['cyclo'] == 'none' or repo['depth'] == 'none' or repo['lag'] == 'none':
        pop_keys.append(key)

for pop_key in pop_keys:
    dict.pop(pop_key, None)

repos = []
locs = []
cycs = []
deps = []
lags = []
for repo in dict:
    if dict[repo]['depth'] >= 2:
        repos.append(repo)
        locs.append(dict[repo]['loc'])
        cycs.append(dict[repo]['cyclo'])
        deps.append(dict[repo]['depth'])
        lags.append(dict[repo]['lag'])

final_df = pd.DataFrame({'repository': repos, 'lines_of_code': locs, 'cyclomatic_complexity': cycs, 'tlag': lags, 'deps_depth': deps})
print(final_df)
final_df.to_csv("npm_repo_data.csv")
