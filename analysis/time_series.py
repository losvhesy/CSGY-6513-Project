import networkx as nx
import numpy as np
import pandas as pd
import random
from tslearn.clustering import KernelKMeans
from tslearn.utils import to_time_series_dataset
from .preprocess import extract_states


def extract_state_series(integrated_data):
    states = extract_states(integrated_data)
    X = []
    XV = []
    for state in states:
        array = integrated_data[integrated_data['state'] == state]
        array = array[['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
           'parks_percent_change_from_baseline',
           'transit_stations_percent_change_from_baseline',
           'workplaces_percent_change_from_baseline',
           'residential_percent_change_from_baseline', 'cases', 'deaths']]
        X.append(array)
        tmp = array.values
        tmp = tmp.flatten()
        XV.append(tmp)
    X = to_time_series_dataset(X)
    return X

def cluster_states_by_ts(X, n_clusters = 6):
    gak_km = KernelKMeans(n_clusters=n_clusters, kernel="gak")
    labels = gak_km.fit_predict(X)
    return labels

def generate_cluster_network(states, labels, n_clusters=6):
    G = nx.Graph()
    for state in states:
        G.add_node(state)
    for cluster_idx in range(n_clusters):
        cluster_state_ids = np.where(labels == cluster_idx)
        cluster_states = list(map(lambda x: states[x], cluster_state_ids[0]))
        for i in range(len(cluster_states)):
            for j in range(len(cluster_states) - i - 1):
                G.add_edge(cluster_states[i], cluster_states[j + i + 1])
        for link_cluster_idx in range(n_clusters - cluster_idx - 1):
            link_cluster_state_ids = np.where(labels == link_cluster_idx)
            link_cluster_states = list(map(lambda x: states[x], link_cluster_state_ids[0]))
            G.add_edge(cluster_states[0], link_cluster_states[0])
    for state_idx in range(len(states)):
        for link_state_idx in range(len(states) - 1 - state_idx):
            if random.random() > 0.1:
                continue
            G.add_edge(states[state_idx], states[link_state_idx])

    return G


def get_state_pos(states, labels):
    G = generate_cluster_network(states, labels)
    pos = nx.spring_layout(G)
    return pos


def get_state_embeddings(states, labels):
    pos = get_state_pos(states, labels)
    embeddings = []
    for idx, state in enumerate(states):
        row = {
            "state": state,
            "x": pos[state][0],
            "y": pos[state][1],
            "cluster": labels[idx]
        }
        embeddings.append(row)

    embeddings = pd.DataFrame(embeddings)
    return embeddings


def add_cluster_info(integrated_data, embeddings):
    state_cluster_dict = {}
    for row in embeddings.iterrows():
        state_cluster_dict[row[1]['state']] = row[1]['cluster']
    # state_cluster_dict
    integrated_data['cluster'] = integrated_data['state'].map(state_cluster_dict)
    return integrated_data
