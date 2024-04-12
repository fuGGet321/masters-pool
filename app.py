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
headers = ["Player","Score"]
df_leaderboard.columns = headers

df_leaderboard.reset_index(drop=True)

# Change E to 0 so whole column can be changed to integers
df_leaderboard.loc[df_leaderboard["Score"] == 'E', "Score"] = 0

df_leaderboard.Score = df_leaderboard.Score.astype(int)
df_leaderboard = df_leaderboard.sort_values("Score")


# %%
# Set teams as dfs
df_ta_team = pd.DataFrame(list(df_golf.iloc[0]),columns=['Golfer'])
df_lu_team = pd.DataFrame(list(df_golf.iloc[1]),columns=['Golfer'])
df_aj_team = pd.DataFrame(list(df_golf.iloc[2]),columns=['Golfer'])
df_br_team = pd.DataFrame(list(df_golf.iloc[3]),columns=['Golfer'])
df_hu_team = pd.DataFrame(list(df_golf.iloc[4]),columns=['Golfer'])
df_ad_team = pd.DataFrame(list(df_golf.iloc[5]),columns=['Golfer'])
df_ty_team = pd.DataFrame(list(df_golf.iloc[6]),columns=['Golfer'])

# Prepopulate df column to insert scores
df_ta_team.loc[:,'Score'] = 0
df_lu_team.loc[:,'Score'] = 0
df_aj_team.loc[:,'Score'] = 0
df_br_team.loc[:,'Score'] = 0
df_hu_team.loc[:,'Score'] = 0
df_ad_team.loc[:,'Score'] = 0
df_ty_team.loc[:,'Score'] = 0


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
ta_data_df = pd.DataFrame(all_data[0],columns=['Golfer','Score'])
ta_data_df.loc[ta_data_df["Score"] == 'E', "Score"] = 0
ta_data_df.Score = ta_data_df.Score.astype(int)
ta_data_df = ta_data_df.sort_values("Score")


lu_data_df = pd.DataFrame(all_data[1],columns=['Golfer','Score'])
lu_data_df.loc[lu_data_df["Score"] == 'E', "Score"] = 0
lu_data_df.Score = lu_data_df.Score.astype(int)
lu_data_df = lu_data_df.sort_values("Score")


aj_data_df = pd.DataFrame(all_data[2],columns=['Golfer','Score'])
aj_data_df.loc[aj_data_df["Score"] == 'E', "Score"] = 0
aj_data_df.Score = aj_data_df.Score.astype(int)
aj_data_df = aj_data_df.sort_values("Score")


br_data_df = pd.DataFrame(all_data[3],columns=['Golfer','Score'])
br_data_df.loc[br_data_df["Score"] == 'E', "Score"] = 0
br_data_df.Score = br_data_df.Score.astype(int)
br_data_df = br_data_df.sort_values("Score")


hu_data_df = pd.DataFrame(all_data[4],columns=['Golfer','Score'])
hu_data_df.loc[hu_data_df["Score"] == 'E', "Score"] = 0
hu_data_df.Score = hu_data_df.Score.astype(int)
hu_data_df = hu_data_df.sort_values("Score")


ad_data_df = pd.DataFrame(all_data[5],columns=['Golfer','Score'])
ad_data_df.loc[ad_data_df["Score"] == 'E', "Score"] = 0
ad_data_df.Score = ad_data_df.Score.astype(int)
ad_data_df = ad_data_df.sort_values("Score")


ty_data_df = pd.DataFrame(all_data[6],columns=['Golfer','Score'])
ty_data_df.loc[ty_data_df["Score"] == 'E', "Score"] = 0
ty_data_df.Score = ty_data_df.Score.astype(int)
ty_data_df = ty_data_df.sort_values("Score")




ta_total = ta_data_df.Score[0:4].sum()
lu_total = lu_data_df.Score[0:4].sum()
aj_total = aj_data_df.Score[0:4].sum()
br_total = br_data_df.Score[0:4].sum()
hu_total = hu_data_df.Score[0:4].sum()
ad_total = ad_data_df.Score[0:4].sum()
ty_total = ty_data_df.Score[0:4].sum()

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
df_bruv.columns = ['Rank', 'Bruv', 'Score']


def strike_last_two(val):
    return ["background-color: grey"]

last_two = pd.IndexSlice[df_bruv.index[0:2],:]
df_bruv_styled = df_bruv.style.applymap(strike_last_two, subset=last_two)


# Add a + in front of over par scores
ta_data_df['Score'] = ta_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
lu_data_df['Score'] = lu_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
aj_data_df['Score'] = aj_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
br_data_df['Score'] = br_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
hu_data_df['Score'] = hu_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
ad_data_df['Score'] = ad_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
ty_data_df['Score'] = ty_data_df['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)

# Replace 0s with Es
ta_data_df.loc[ta_data_df["Score"] == 0, "Score"] = 'E'
lu_data_df.loc[lu_data_df["Score"] == 0, "Score"] = 'E'
aj_data_df.loc[aj_data_df["Score"] == 0, "Score"] = 'E'
br_data_df.loc[br_data_df["Score"] == 0, "Score"] = 'E'
hu_data_df.loc[hu_data_df["Score"] == 0, "Score"] = 'E'
ad_data_df.loc[ad_data_df["Score"] == 0, "Score"] = 'E'
ty_data_df.loc[ty_data_df["Score"] == 0, "Score"] = 'E'




# %%
st.title("STURGs MASTERS 2024")
# st.write(df_bruv)
st.write("---")
st.write("OVERALL SCORE")
st.write(df_bruv.to_html(index=False), unsafe_allow_html=True)
st.write("---")

# st.markdown("~strikethru text~")

st.markdown(f"**Team Taylor: {ta_total}**")
st.write(ta_data_df.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Lucas: {lu_total}**")
st.write(lu_data_df.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team AJ: {aj_total}**")
st.write(aj_data_df.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Brendan: {br_total}**")
st.write(br_data_df.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Hugh: {hu_total}**")
st.write(hu_data_df.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Adam: {ad_total}**")
st.write(ad_data_df.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Tyler: {ty_total}**")
st.write(ty_data_df.to_html(index=False), unsafe_allow_html=True)
