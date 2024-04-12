# %%
import streamlit as st
import pandas as pd
import requests
import numpy as np

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
    my_data = [#golfers[g[0]]['id'],
               golfers[g[0]]["athlete"]["displayName"],
               golfers[g[0]]["linescores"][0]["displayValue"]]
    leaderboard.append(my_data)


# Get leaderboard from list type back in df type
df_leaderboard = pd.DataFrame(leaderboard)
headers = ["id", "golfer","score"]
headers = ["golfer","score"]
df_leaderboard.columns = headers

df_leaderboard.reset_index(drop=True)

# Change E to 0 so whole column can be changed to integers
df_leaderboard.loc[df_leaderboard["score"] == 'E', "score"] = 0

df_leaderboard.score = df_leaderboard.score.astype(int)
df_leaderboard = df_leaderboard.sort_values("score")


# %%
# Set teams as dfs
df_ta_team = pd.DataFrame(list(df_golf.iloc[0]),columns=['golfer'])
df_lu_team = pd.DataFrame(list(df_golf.iloc[1]),columns=['golfer'])
df_aj_team = pd.DataFrame(list(df_golf.iloc[2]),columns=['golfer'])
df_br_team = pd.DataFrame(list(df_golf.iloc[3]),columns=['golfer'])
df_hu_team = pd.DataFrame(list(df_golf.iloc[4]),columns=['golfer'])
df_ad_team = pd.DataFrame(list(df_golf.iloc[5]),columns=['golfer'])
df_ty_team = pd.DataFrame(list(df_golf.iloc[6]),columns=['golfer'])

# Prepopulate df column to insert scores
df_ta_team.loc[:,'score'] = 0
df_lu_team.loc[:,'score'] = 0
df_aj_team.loc[:,'score'] = 0
df_br_team.loc[:,'score'] = 0
df_hu_team.loc[:,'score'] = 0
df_ad_team.loc[:,'score'] = 0
df_ty_team.loc[:,'score'] = 0


# # %%
# df_ta_team.score = df_leaderboard.score[(df_leaderboard["golfer"] == df_ta_team["golfer"])]


# %%

all_data = []

for bruv in range(0,7):
    bruv_data = []
    golfer_list = list(df_golf.iloc[bruv])
    for g in enumerate(leaderboard):
        athlete = leaderboard[g[0]][0]
        if athlete in golfer_list:
            bruv_data.append([leaderboard[g[0]][0],leaderboard[g[0]][1]])
    all_data.append(bruv_data)



# Brute force sorting DFs
ta_data_df = pd.DataFrame(all_data[0],columns=['golfer','score'])
ta_data_df.loc[ta_data_df["score"] == 'E', "score"] = 0
ta_data_df.score = ta_data_df.score.astype(int)
ta_data_df = ta_data_df.sort_values("score")

lu_data_df = pd.DataFrame(all_data[1],columns=['golfer','score'])
lu_data_df.loc[lu_data_df["score"] == 'E', "score"] = 0
lu_data_df.score = lu_data_df.score.astype(int)
lu_data_df = lu_data_df.sort_values("score")

aj_data_df = pd.DataFrame(all_data[2],columns=['golfer','score'])
aj_data_df.loc[aj_data_df["score"] == 'E', "score"] = 0
aj_data_df.score = aj_data_df.score.astype(int)
aj_data_df = aj_data_df.sort_values("score")

br_data_df = pd.DataFrame(all_data[3],columns=['golfer','score'])
br_data_df.loc[br_data_df["score"] == 'E', "score"] = 0
br_data_df.score = br_data_df.score.astype(int)
br_data_df = br_data_df.sort_values("score")

hu_data_df = pd.DataFrame(all_data[4],columns=['golfer','score'])
hu_data_df.loc[hu_data_df["score"] == 'E', "score"] = 0
hu_data_df.score = hu_data_df.score.astype(int)
hu_data_df = hu_data_df.sort_values("score")

ad_data_df = pd.DataFrame(all_data[5],columns=['golfer','score'])
ad_data_df.loc[ad_data_df["score"] == 'E', "score"] = 0
ad_data_df.score = ad_data_df.score.astype(int)
ad_data_df = ad_data_df.sort_values("score")

ty_data_df = pd.DataFrame(all_data[6],columns=['golfer','score'])
ty_data_df.loc[ty_data_df["score"] == 'E', "score"] = 0
ty_data_df.score = ty_data_df.score.astype(int)
ty_data_df = ty_data_df.sort_values("score")


ta_total = ta_data_df.score[0:4].sum()
lu_total = lu_data_df.score[0:4].sum()
aj_total = aj_data_df.score[0:4].sum()
br_total = br_data_df.score[0:4].sum()
hu_total = hu_data_df.score[0:4].sum()
ad_total = ad_data_df.score[0:4].sum()
ty_total = ty_data_df.score[0:4].sum()

total_list = [ta_total,
              lu_total,
              aj_total,
              br_total,
              hu_total,
              ad_total,
              ty_total]


df_bruv.loc[:,'overall_score'] = 0
df_bruv.overall_score = total_list

df_bruv.overall_score = df_bruv.overall_score.astype(int)
df_bruv = df_bruv.sort_values("overall_score")

df_bruv.insert(0,'Rank', range(1,8))




# %%
st.title("STURGs MASTERS 2024")
st.write(df_bruv)

st.markdown("~strikethru text~")

st.write(ta_data_df)
st.write(lu_data_df)
st.write(aj_data_df)
st.write(br_data_df)
st.write(hu_data_df)
st.write(ad_data_df)
st.write(ty_data_df)
