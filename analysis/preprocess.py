import json
import pandas as pd


def extract_states(data):
    states = data['state'].unique()
    return states
def preprocess_data(integrated_src_data):
    states = extract_states(integrated_src_data)
    state_df_list = []
    integrated_src_data = integrated_src_data[(integrated_src_data['date'] > '2020-03-20') & (integrated_src_data['date'] < '2021-03-24')]
    for state in states:
        state_df = integrated_src_data[integrated_src_data['state'] == state]
        state_df = pd.DataFrame(state_df)
        state_df['acc_cases'] = state_df['cases']
        state_df['acc_deaths'] = state_df['deaths']
        state_df['tmp'] = state_df.cases.shift(1,fill_value=0)
        state_df['cases'] = state_df['acc_cases'] - state_df['tmp']
        state_df['tmp'] = state_df.deaths.shift(1,fill_value=0)
        state_df['deaths'] = state_df['acc_deaths'] - state_df['tmp']
        state_df = state_df[1:]
        state_df_list.append(state_df)
    integrated_data = pd.concat(state_df_list)
    integrated_data = integrated_data[(integrated_data['date'] > '2020-03-20') & (integrated_data['date'] < '2021-03-24')]
    return integrated_data



