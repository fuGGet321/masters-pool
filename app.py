# %%
import streamlit as st
import pandas as pd
import requests

# %%
# Read drafted teams
df_teams = pd.read_csv('masters-2024-teams.csv')

# %%
bruv_list = list(df_teams['Unnamed: 0']) # Name of bruv with team AS LIST
df_bruv = df_teams.iloc[:,0:1] # Name of bruv with team AS DF
df_golf = df_teams.iloc[:,1:] # golfers on bruv's team


# %%
# Pull the field list off espn
# https://stackoverflow.com/questions/62840794/pulling-real-time-data-using-espn-api

url = 'https://site.web.api.espn.com/apis/site/v2/sports/golf/leaderboard?league=pga'
r = requests.get(url)

data = r.json()

# Field list from competitors dict key
golfers = data["events"][0]["competitions"][0]["competitors"]
athlete = golfers[0]["athlete"]["displayName"]
score = golfers[0]["linescores"][0]["displayValue"]


# %%
leaderboard = []
for g in enumerate(golfers):
    my_data = [golfers[g[0]]['id'],
               golfers[g[0]]["athlete"]["displayName"],
               golfers[g[0]]["linescores"][0]["displayValue"]]
    leaderboard.append(my_data)


# %%
tay_golf_list = list(df_golf.iloc[0])
tay_data = []
for g in enumerate(leaderboard):
    athlete = leaderboard[g[0]][1]
    if athlete in tay_golf_list:
        tay_data.append([leaderboard[g[0]][1],leaderboard[g[0]][2]])

tay_data_df = pd.DataFrame(tay_data)


# %%
lu_golf_list = list(df_golf.iloc[1])
lu_data = []
for g in enumerate(leaderboard):
    athlete = leaderboard[g[0]][1]
    if athlete in lu_golf_list:
        lu_data.append([leaderboard[g[0]][1],leaderboard[g[0]][2]])

lu_data_df = pd.DataFrame(lu_data)


# %%
st.title("STURGs MASTERS 2024")
st.write(tay_data_df)
st.write(lu_data_df)