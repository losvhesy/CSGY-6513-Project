import altair as alt
from vega_datasets import data
import pandas as pd
import numpy as np


def plot_ts_clusters(integrated_data, embeddings):
    alt.data_transformers.disable_max_rows()

    cluster_selection = alt.selection_multi(fields=['cluster'])
    line_selection = alt.selection_single(fields=['state'],on='mouseover')
    color = alt.condition(cluster_selection,
                          alt.Color('cluster:N', legend=None),
                          alt.value('lightgray'))
    line_color = alt.condition(line_selection,
                          alt.Color('state:N', legend=None),
                          alt.value('lightgray'))
    line_source = integrated_data

    # line_source = line_source[line_source['state'].isin(cluster_states)]
    line = alt.Chart(line_source).mark_line(interpolate='basis').encode(
        x='date:T',
        y='cases:Q',
        color=line_color,
        opacity=alt.condition(line_selection, alt.value(0.9), alt.value(0.2))
    ).transform_filter(
        cluster_selection
    ).properties(
        width=300, height=300
    ).add_selection(
        line_selection
    )

    points_source = embeddings

    # Brush for selection
    brush = alt.selection(type='interval')

    # Scatter Plot
    points = alt.Chart(points_source).mark_point().encode(
        x='x:Q',
        y='y:Q',
        color=color,
        tooltip='state:N'
    ).properties(
        width=300, height=300
    )

    legend = alt.Chart(points_source).mark_point().encode(
        y=alt.Y('cluster:N', axis=alt.Axis(orient='right')),
        color=color
    ).add_selection(
        cluster_selection
    )
    line_legend = alt.Chart(line_source).mark_point().encode(
        y=alt.Y('state:N', axis=alt.Axis(orient='right')),
        color=line_color
    ).transform_filter(
        cluster_selection
    ).add_selection(
        line_selection
    )



    return points | legend | alt.layer(
        line #, line_selectors, line_points, line_rules, line_text
    ).properties(
        width=600, height=300
    ) | line_legend


def plot_map(integrated_data, state2fips_df, populations):
    states = alt.topo_feature(data.us_10m.url, 'states')
    map_source = integrated_data[integrated_data['date'] > '2021-03-22' ]
    map_source = pd.merge(map_source, state2fips_df, how='left',
                      left_on='state', right_on='state')
    map_source = pd.merge(map_source, populations, how='left',
                      left_on='state', right_on='state')
    map_source['cases in a million']  = 1000000 * map_source['cases'] / map_source['population']
    return alt.Chart(map_source).mark_geoshape().encode(
        shape='geo:G',
        color='cases in a million:Q',
        tooltip=['state:N', alt.Tooltip('cases in a million:Q', format='.2f')],
    ).transform_lookup(
        lookup='fip',
        from_=alt.LookupData(data=states, key='id'),
        as_='geo'
    ).properties(
        width=300,
        height=175,
    ).project(
        type='albersUsa'
    )


def generate_corr_items(state_metric_correlation, metrics):
    source_corr_matrix = []
    for row in state_metric_correlation.iterrows():
        for metric in metrics:
            for covid_metric in ['cases', 'deaths']:
                col = metric + "_" + covid_metric
                obj = {
                    "state": row[1]['state'],
                    "value": row[1][col],
                    "metric": metric.split("_")[0] + " " + covid_metric
                }
                source_corr_matrix.append(obj)
    source_corr_matrix = pd.DataFrame(source_corr_matrix)
    return source_corr_matrix


def transform_corr_log(state_metric_correlation, metrics):
    state_metric_correlation_log = state_metric_correlation.copy()
    for metric in metrics:
        for covid_metric in ['cases', 'deaths']:
            col = metric + "_" + covid_metric
            state_metric_correlation_log[col].iloc[state_metric_correlation_log[col] < 0] = 0
            state_metric_correlation_log[col] = np.log(state_metric_correlation_log[col] + 1)
    return state_metric_correlation_log


def plot_state_metric_corr(state_metric_correlation, metrics, use_log=True):
    if use_log:
        state_metric_correlation = transform_corr_log(state_metric_correlation, metrics)
    source_corr_matrix = generate_corr_items(state_metric_correlation, metrics)
    return alt.Chart(source_corr_matrix).mark_rect().encode(
        y='metric:O',
        x='state:O',
        color='value:Q'
    )


def plot_corr_map(state_metric_correlation, state2fips_df, metrics, use_log=True):
    states = alt.topo_feature(data.us_10m.url, 'states')
    if use_log:
        state_metric_correlation = transform_corr_log(state_metric_correlation, metrics)
    source_corr_matrix = generate_corr_items(state_metric_correlation, metrics)
    map_source = source_corr_matrix
    map_source = pd.merge(map_source, state2fips_df, how='left',
                          left_on='state', right_on='state')

    metrics = map_source['metric'].unique()
    input_dropdown = alt.binding_select(options=metrics)
    selection = alt.selection_single(fields=['metric'], bind=input_dropdown, name='Corr Metric')

    return alt.Chart(map_source).mark_geoshape().encode(
        shape='geo:G',
        color='value:Q',
        tooltip=['state:N', alt.Tooltip('value', format='.2f')],
    ).add_selection(
        selection
    ).transform_filter(
        selection
    ).transform_lookup(
        lookup='fip',
        from_=alt.LookupData(data=states, key='id'),
        as_='geo'
    ).properties(
        width=300,
        height=175,
    ).project(
        type='albersUsa'
    )