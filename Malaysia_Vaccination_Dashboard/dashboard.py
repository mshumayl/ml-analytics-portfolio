# %%
%%time 
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, datetime

#Get CSVs from CITF GitHub
url1 = 'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv'
url2 = 'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv'
url3 = 'https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/static/population.csv'

res1 = requests.get(url1, allow_redirects=True)
with open('vax_state.csv','wb') as file:
    file.write(res1.content)
vax_state_df = pd.read_csv('vax_state.csv')

res2 = requests.get(url2, allow_redirects=True)
with open('vax_malaysia.csv','wb') as file:
    file.write(res2.content)
vax_malaysia_df = pd.read_csv('vax_malaysia.csv')

res3 = requests.get(url3, allow_redirects=True)
with open('population.csv', 'wb') as file:
    file.write(res3.content)
population = pd.read_csv('population.csv')

#Convert date format
vax_malaysia_df['date'] = pd.to_datetime(vax_malaysia_df['date'])
vax_state_df['date'] = pd.to_datetime(vax_state_df['date'])

#Population
# population = pd.read_csv('Malaysia_Population_18yo.csv')
# population["state"].replace({"perlis": "Perlis", 
#                        "kedah": "Kedah",
#                        "penang": "Pulau Pinang",
#                        "perak": "Perak",
#                        "selangor": "Selangor",
#                        "kl": "W.P. Kuala Lumpur",
#                        "putrajaya": "W.P. Putrajaya",
#                        "ns": "Negeri Sembilan",
#                        "melaka": "Melaka",
#                        "kelantan": "Kelantan",
#                        "terengganu": "Terengganu",
#                        "pahang": "Pahang",
#                        "johor": "Johor",
#                        "sabah": "Sabah",
#                        "labuan": "W.P. Labuan",
#                        "sarawak": "Sarawak"
#                        }, inplace=True)
population_states = pd.DataFrame(population).drop(['idxs', 'pop_18', 'pop_60'], axis=1)[1:]
population_malaysia = pd.DataFrame(population).drop(['idxs', 'pop_18', 'pop_60'], axis=1)[:1]


#Merge population into DataFrame
vax_state_df = pd.merge(population_states, vax_state_df, on="state")

#Calculate percentage using population
vax_state_df['percentage_fully_vaccinated'] = vax_state_df["dose2_cumul"] / vax_state_df['pop'] * 100

#Group by date
vax_state_groupbydate = vax_state_df.groupby(['date', 'state'])["percentage_fully_vaccinated"].sum()
vax_state_groupbydate_df = pd.DataFrame(vax_state_groupbydate)


#Key analytics
total_first_dose_malaysia = vax_malaysia_df['dose1_daily'].sum()
total_second_dose_malaysia = vax_malaysia_df['dose2_daily'].sum()
pct_fully_vax_malaysia = total_second_dose_malaysia / population_malaysia['pop'].sum()*100


#Group by state
vax_state_groupbystate_df = vax_state_df.groupby('state', as_index=False).agg(
    {
        'dose1_daily': 'sum',
        'dose2_daily': 'sum',
        'total_daily': 'sum',
        'percentage_fully_vaccinated': 'max'
    }
)

#Key percentages
pct_fully_vax_johor = vax_state_groupbystate_df['percentage_fully_vaccinated'][0] * 100
pct_fully_vax_kedah = vax_state_groupbystate_df['percentage_fully_vaccinated'][1] * 100
pct_fully_vax_kelantan = vax_state_groupbystate_df['percentage_fully_vaccinated'][2] * 100
pct_fully_vax_melaka = vax_state_groupbystate_df['percentage_fully_vaccinated'][3] * 100
pct_fully_vax_ns = vax_state_groupbystate_df['percentage_fully_vaccinated'][4] * 100
pct_fully_vax_pahang = vax_state_groupbystate_df['percentage_fully_vaccinated'][5] * 100
pct_fully_vax_perak = vax_state_groupbystate_df['percentage_fully_vaccinated'][6] * 100
pct_fully_vax_perlis = vax_state_groupbystate_df['percentage_fully_vaccinated'][7] * 100
pct_fully_vax_penang = vax_state_groupbystate_df['percentage_fully_vaccinated'][8] * 100
pct_fully_vax_sabah = vax_state_groupbystate_df['percentage_fully_vaccinated'][9] * 100
pct_fully_vax_sarawak = vax_state_groupbystate_df['percentage_fully_vaccinated'][10] * 100
pct_fully_vax_selangor = vax_state_groupbystate_df['percentage_fully_vaccinated'][11] * 100
pct_fully_vax_terengganu = vax_state_groupbystate_df['percentage_fully_vaccinated'][12] * 100
pct_fully_vax_kl = vax_state_groupbystate_df['percentage_fully_vaccinated'][13] * 100
pct_fully_vax_labuan = vax_state_groupbystate_df['percentage_fully_vaccinated'][14] * 100
pct_fully_vax_putrajaya = vax_state_groupbystate_df['percentage_fully_vaccinated'][15] * 100

#Line chart
states_line_data = vax_state_groupbydate_df.reset_index().to_dict('records')

johor_line_data = pd.DataFrame(states_line_data[0:-1:16])
kedah_line_data = pd.DataFrame(states_line_data[1:-1:16])
kelantan_line_data = pd.DataFrame(states_line_data[2:-1:16])
melaka_line_data = pd.DataFrame(states_line_data[3:-1:16])
ns_line_data = pd.DataFrame(states_line_data[4:-1:16])
pahang_line_data = pd.DataFrame(states_line_data[5:-1:16])
perak_line_data = pd.DataFrame(states_line_data[6:-1:16])
perlis_line_data = pd.DataFrame(states_line_data[7:-1:16])
penang_line_data = pd.DataFrame(states_line_data[8:-1:16])
sabah_line_data = pd.DataFrame(states_line_data[9:-1:16])
sarawak_line_data = pd.DataFrame(states_line_data[10:-1:16])
selangor_line_data = pd.DataFrame(states_line_data[11:-1:16])
terengganu_line_data = pd.DataFrame(states_line_data[12:-1:16])
kl_line_data = pd.DataFrame(states_line_data[13:-1:16])
labuan_line_data = pd.DataFrame(states_line_data[14:-1:16])
putrajaya_line_data = pd.DataFrame(states_line_data[15:-1:16]).append(states_line_data[-1], ignore_index=True)


#Template for Plotly subplots
large_rockwell_template = dict(
    layout=go.Layout(title_font=dict(family="Rockwell", size=24))
)


#Create subplot
fig = make_subplots(
    rows = 15, cols = 10,
    specs=[
            [    None, None, None, None, None, None, None, None, None, None],
            [    {"type": "scatter", "rowspan":8, "colspan":7}, None, None, None, None, None, None, None, None, None,],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    None, None, None, None, None, None, None, None, None, None],
            [    {"type": "indicator"}, None, {"type": "indicator"}, None, {"type": "indicator"}, None, None, None, None, None],
          ]
)

#Figures
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_first_dose_malaysia,
        title="Jumlah Dos Pertama",
        title_font_family="Rockwell"
    ),
    row=15, col=1
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_second_dose_malaysia,
        title="Jumlah Dos Kedua",
        title_font_family="Rockwell"
    ),
    row=15, col=3
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=pct_fully_vax_malaysia,
        title="% Divaksin Penuh (2 Dos)",
        title_font_family="Rockwell"
    ),
    row=15, col=5
)

#Line chart elements (by state)
fig.add_trace(
    go.Scatter(
        x=johor_line_data['date'].tolist(),
        y=johor_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Johor'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=kedah_line_data['date'].tolist(),
        y=kedah_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Kedah'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=kelantan_line_data['date'].tolist(),
        y=kelantan_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Kelantan'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=kl_line_data['date'].tolist(),
        y=kl_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='W.P. Kuala Lumpur'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=labuan_line_data['date'].tolist(),
        y=labuan_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='W.P. Labuan'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=melaka_line_data['date'].tolist(),
        y=melaka_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Melaka'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=ns_line_data['date'].tolist(),
        y=ns_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Negeri Sembilan'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=pahang_line_data['date'].tolist(),
        y=pahang_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Pahang'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=penang_line_data['date'].tolist(),
        y=penang_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Pulau Pinang'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=perak_line_data['date'].tolist(),
        y=perak_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Perak'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=perlis_line_data['date'].tolist(),
        y=perlis_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Perlis'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=putrajaya_line_data['date'].tolist(),
        y=putrajaya_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Putrajaya'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=sabah_line_data['date'].tolist(),
        y=sabah_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Sabah'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=sarawak_line_data['date'].tolist(),
        y=sarawak_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Sarawak'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=selangor_line_data['date'].tolist(),
        y=selangor_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Selangor'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=terengganu_line_data['date'].tolist(),
        y=terengganu_line_data['percentage_fully_vaccinated'].tolist(),
        mode='lines',
        name='Terengganu'
    ),
    row=2, col=1
)

#Fixed scale
fig.update_yaxes(range=[0, 100])

#Set black background
fig.update_layout(template='plotly_dark')

#Subplot title
fig.update_layout(
    title={
        'text': "Perkembangan Vaksinasi Negara",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    title_font_family='Rockwell',
    title_font_size=50)

#Legend
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.9,
    xanchor="right",
    x=0.99
))

#Figure titles
fig.update_layout(
    yaxis_title="% Divaksin Penuh (2 Dos)",
    xaxis_title="Tarikh",
    legend_title="*Klik dua kali untuk memilih negeri:",
    font=dict(
        family="Rockwell",
        size=16,
    )
)


# fig.update_layout(title="Perkembangan Vaksinasi Negara",
#                   template=large_rockwell_template)

# fig.add_trace(
#     go.Scatter(
#         x=vax_state_df['date'].tolist(),
#         y=vax_state_df['dose2_cumul'].tolist(),
#         mode='markers',
#         name='Scatter'
#     ),
#     row=1, col=2
# )

#Output
fig.write_html('index.html', auto_open=True)

 # %%

# FOR BARPLOT LATEST CUMULATIVE
# pct_barplot_data = pd.DataFrame(pejadah)


















# %%
