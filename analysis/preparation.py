import json
import pandas as pd


def load_state_info(fips_path="./state2fips.json", population_path="./state_populations.csv"):
    with open(fips_path) as fp:
        state2fips = json.load(fp)

    state2fips_df = []
    for key in state2fips:
        obj = {
            "state": key,
            "fip": int(state2fips[key])
        }
        state2fips_df.append(obj)
    state2fips_df = pd.DataFrame(state2fips_df)
    populations = pd.read_csv(population_path)
    populations.columns = ['state', 'population']
    return state2fips_df, populations
