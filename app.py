# %%
import streamlit as st
import pandas as pd
import requests
import numpy as np
from math import isnan

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
    round_set = [rd[1]["value"] for rd in enumerate(g[1]["linescores"]) if "value" in rd[1]]

    # Change thru to F if round is completed, or CUT if didn't make cut
    if golfers[g[0]]["status"]["hole"] == 18 and golfers[g[0]]["status"]["displayValue"] == 'CUT':
        thru = 'CUT'
    elif golfers[g[0]]["status"]["hole"] == 18:
        thru = 'F'
    else:
        thru = golfers[g[0]]["status"]["hole"]

    my_data = [#golfers[g[0]]['id'],
               golfers[g[0]]["athlete"]["displayName"],
               golfers[g[0]]["score"]["displayValue"],
               thru]
    for r in round_set:
        my_data.append(int(r))
    leaderboard.append(my_data)

# %%

# # Get leaderboard from list type back in df type
df_leaderboard = pd.DataFrame(leaderboard)
headers = ["Player","Score", "Thru", "R1", "R2", "R3"]
df_leaderboard.columns = headers

# # Add Round Score placeholders
# df_leaderboard.loc[:,['R1','R2','R3','R4']] = 0

df_leaderboard.reset_index(drop=True)

# # Change E to 0 so whole column can be changed to integers
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


# %%

all_data = []
for bruv in range(0,7):
    bruv_data = []
    golfer_list = list(df_golf.iloc[bruv])
    for g in enumerate(leaderboard):
        athlete = leaderboard[g[0]][0]
        if athlete in golfer_list:
            stat_line = [x for x in leaderboard[g[0]]]
            bruv_data.append(stat_line)
    all_data.append(bruv_data)

# Create header list based on rounds played
bruv_heads = ["Golfer", "Score", "Thru"]
for r in range(len(leaderboard[0]) - len(bruv_heads)):
    r_head = f"R{r+1}"
    bruv_heads.append(r_head)



# Brute force sorting DFs
# Weird slicing operation came from https://stackoverflow.com/questions/43596579/how-to-use-pandas-stylers-for-coloring-an-entire-row-based-on-a-given-column
ta_data_df = pd.DataFrame(all_data[0], columns=bruv_heads)
ta_data_df.loc[ta_data_df["Score"] == 'E', "Score"] = 0
ta_data_df.loc[pd.isna(ta_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
ta_data_df.Score = ta_data_df.Score.astype(int)
ta_data_df.iloc[:,-3:] = ta_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
ta_data_df = ta_data_df.sort_values("Score")

last_two = ta_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
ta_data_s = ta_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)

# %%

lu_data_df = pd.DataFrame(all_data[1],columns=bruv_heads)
lu_data_df.loc[lu_data_df["Score"] == 'E', "Score"] = 0
lu_data_df.loc[pd.isna(lu_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
lu_data_df.Score = lu_data_df.Score.astype(int)
lu_data_df.iloc[:,-3:] = lu_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
lu_data_df = lu_data_df.sort_values("Score")

last_two = lu_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
lu_data_s = lu_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)



aj_data_df = pd.DataFrame(all_data[2],columns=bruv_heads)
aj_data_df.loc[aj_data_df["Score"] == 'E', "Score"] = 0
aj_data_df.loc[pd.isna(aj_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
aj_data_df.Score = aj_data_df.Score.astype(int)
aj_data_df.iloc[:,-3:] = aj_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
aj_data_df = aj_data_df.sort_values("Score")

last_two = aj_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
aj_data_s = aj_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)



br_data_df = pd.DataFrame(all_data[3],columns=bruv_heads)
br_data_df.loc[br_data_df["Score"] == 'E', "Score"] = 0
br_data_df.loc[pd.isna(br_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
br_data_df.Score = br_data_df.Score.astype(int)
br_data_df.iloc[:,-3:] = br_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
br_data_df = br_data_df.sort_values("Score")

last_two = br_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
br_data_s = br_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)



hu_data_df = pd.DataFrame(all_data[4],columns=bruv_heads)
hu_data_df.loc[hu_data_df["Score"] == 'E', "Score"] = 0
hu_data_df.loc[pd.isna(hu_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
hu_data_df.Score = hu_data_df.Score.astype(int)
hu_data_df.iloc[:,-3:] = hu_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
hu_data_df = hu_data_df.sort_values("Score")

last_two = hu_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
hu_data_s = hu_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)



ad_data_df = pd.DataFrame(all_data[5],columns=bruv_heads)
ad_data_df.loc[ad_data_df["Score"] == 'E', "Score"] = 0
ad_data_df.loc[pd.isna(ad_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
ad_data_df.Score = ad_data_df.Score.astype(int)
ad_data_df.iloc[:,-3:] = ad_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
ad_data_df = ad_data_df.sort_values("Score")

last_two = ad_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
ad_data_s = ad_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)



ty_data_df = pd.DataFrame(all_data[6],columns=bruv_heads)
ty_data_df.loc[ty_data_df["Score"] == 'E', "Score"] = 0
ty_data_df.loc[pd.isna(ty_data_df["R3"]), "R3"] = 80 # Replace cut scores w 80
ty_data_df.Score = ty_data_df.Score.astype(int)
ty_data_df.iloc[:,-3:] = ty_data_df.iloc[:,-3:].astype(int) # Change rd scores to ints
ty_data_df = ty_data_df.sort_values("Score")

last_two = ty_data_df.tail(2)
slice_ = pd.IndexSlice[last_two.index, last_two.columns]
ty_data_s = ty_data_df.style.set_properties(**{'background-color': 'grey'}, subset=slice_)


# %%

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

# Stylize positive and Even scores in overall table
df_bruv['Score'] = df_bruv['Score'].apply(lambda x: str(f"+{x}") if x > 0 else x)
df_bruv.loc[df_bruv["Score"] == 0, "Score"] = 'E'


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
# Ops to post to webapp!
st.title("STURGs MASTERS 2024")
# st.write(df_bruv)
st.write("---")
st.write("OVERALL SCORE")
st.write(df_bruv.to_html(index=False), unsafe_allow_html=True)
st.write("---")

st.markdown(f"**Team Taylor: {ta_total}**")
st.write(ta_data_s.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Lucas: {lu_total}**")
st.write(lu_data_s.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team AJ: {aj_total}**")
st.write(aj_data_s.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Brendan: {br_total}**")
st.write(br_data_s.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Hugh: {hu_total}**")
st.write(hu_data_s.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Adam: {ad_total}**")
st.write(ad_data_s.to_html(index=False), unsafe_allow_html=True)

st.write("")
st.write("")
st.write(f"**Team Tyler: {ty_total}**")
st.write(ty_data_s.to_html(index=False), unsafe_allow_html=True)
