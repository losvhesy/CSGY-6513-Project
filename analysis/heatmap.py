import altair as alt
import numpy as np
import pandas as pd

def retail(df):
	alt.data_transformers.disable_max_rows()
	selector = alt.selection_single(fields=['state'])

	base = alt.Chart(df, title="Chart for retail data").properties(
		width=700,
		height=500
	).add_selection(selector)

	heatmap = base.mark_rect().encode(
		x=alt.X('date:T', bin=alt.Bin(maxbins=150), axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y=alt.Y('state:N', title="State"),
		color = alt.condition(selector,
							 'retail_and_recreation_percent_change_from_baseline:Q',
							 alt.value('lightgray'),
							 scale=alt.Scale(scheme='blueorange',domain=[-70,0,45])),
		tooltip = [alt.Tooltip('state:N'),
				   alt.Tooltip('date:T'),
				   alt.Tooltip('retail_and_recreation_percent_change_from_baseline:Q',title = "percentage"),
				   alt.Tooltip('cases:Q'),alt.Tooltip('deaths:Q')]
	)

	line = base.mark_line().encode(
		x=alt.X('date:T', axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y='cases',
		color='state',tooltip = [alt.Tooltip('state:N')]
	).transform_filter(
		selector
	)

	return alt.vconcat(
		heatmap,
		line
	).resolve_scale(
		x='shared'
	)
	
	
def parks(df):
	alt.data_transformers.disable_max_rows()
	selector = alt.selection_single(fields=['state'])

	base = alt.Chart(df, title="Chart for parks data").properties(
		width=700,
		height=500
	).add_selection(selector)

	heatmap = base.mark_rect().encode(
		x=alt.X('date:T', bin=alt.Bin(maxbins=150), axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y=alt.Y('state:N', title="State"),
		color = alt.condition(selector,
							 'parks_percent_change_from_baseline:Q',
							 alt.value('lightgray'),
							 scale=alt.Scale(scheme='blueorange',domain=[-70,0,250])),
		tooltip = [alt.Tooltip('state:N'),
				   alt.Tooltip('date:T'),
				   alt.Tooltip('parks_percent_change_from_baseline:Q',title = "percentage"),
				   alt.Tooltip('cases:Q'),alt.Tooltip('deaths:Q')]
	)

	line = base.mark_line().encode(
		x=alt.X('date:T', axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y='cases',
		color='state',tooltip = [alt.Tooltip('state:N')]
	).transform_filter(
		selector
	)

	return alt.vconcat(
		heatmap,
		line
	).resolve_scale(
		x='shared'
	)
	

def transit(df):
	alt.data_transformers.disable_max_rows()
	selector = alt.selection_single(fields=['state'])

	base = alt.Chart(df, title="Chart for transit stations data").properties(
		width=700,
		height=500
	).add_selection(selector)

	heatmap = base.mark_rect().encode(
		x=alt.X('date:T', bin=alt.Bin(maxbins=150), axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y=alt.Y('state:N', title="State"),
		color = alt.condition(selector,
							 'transit_stations_percent_change_from_baseline:Q',
							 alt.value('lightgray'),
							 scale=alt.Scale(scheme='blueorange',domain=[-70,0,70])),
		tooltip = [alt.Tooltip('state:N'),
				   alt.Tooltip('date:T'),
				   alt.Tooltip('transit_stations_percent_change_from_baseline:Q',title = "percentage"),
				   alt.Tooltip('cases:Q'),alt.Tooltip('deaths:Q')]
	)

	line = base.mark_line().encode(
		x=alt.X('date:T', axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y='cases',
		color='state',tooltip = [alt.Tooltip('state:N')]
	).transform_filter(
		selector
	)

	return alt.vconcat(
		heatmap,
		line
	).resolve_scale(
		x='shared'
	)
	
def workplace(df):
	alt.data_transformers.disable_max_rows()
	selector = alt.selection_single(fields=['state'])

	base = alt.Chart(df, title="Chart for workplaces data").properties(
		width=700,
		height=500
	).add_selection(selector)

	heatmap = base.mark_rect().encode(
		x=alt.X('date:T', bin=alt.Bin(maxbins=150), axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y=alt.Y('state:N', title="State"),
		color = alt.condition(selector,
							 'workplaces_percent_change_from_baseline:Q',
							 alt.value('lightgray'),
							 scale=alt.Scale(scheme='blueorange',domain=[-80,0,70])),
		tooltip = [alt.Tooltip('state:N'),
				   alt.Tooltip('date:T'),
				   alt.Tooltip('workplaces_percent_change_from_baseline:Q',title = "percentage"),
				   alt.Tooltip('cases:Q'),alt.Tooltip('deaths:Q')]
	)

	line = base.mark_line().encode(
		x=alt.X('date:T', axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y='cases',
		color='state',tooltip = [alt.Tooltip('state:N')]
	).transform_filter(
		selector
	)

	return alt.vconcat(
		heatmap,
		line
	).resolve_scale(
		x='shared'
	)
	
def residential(df):
	alt.data_transformers.disable_max_rows()
	selector = alt.selection_single(fields=['state'])

	base = alt.Chart(df, title="Chart for residential data").properties(
		width=700,
		height=500
	).add_selection(selector)

	heatmap = base.mark_rect().encode(
		x=alt.X('date:T', bin=alt.Bin(maxbins=150), axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y=alt.Y('state:N', title="State"),
		color = alt.condition(selector,
							 'residential_percent_change_from_baseline:Q',
							 alt.value('lightgray'),
							 scale=alt.Scale(scheme='blueorange',domain=[-40,0,35])),
		tooltip = [alt.Tooltip('state:N'),
				   alt.Tooltip('date:T'),
				   alt.Tooltip('residential_percent_change_from_baseline:Q',title = "percentage"),
				   alt.Tooltip('cases:Q'),alt.Tooltip('deaths:Q')]
	)

	line = base.mark_line().encode(
		x=alt.X('date:T', axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y='cases',
		color='state',tooltip = [alt.Tooltip('state:N')]
	).transform_filter(
		selector
	)

	return alt.vconcat(
		heatmap,
		line
	).resolve_scale(
		x='shared'
	)
	
def grocery(df):
	alt.data_transformers.disable_max_rows()
	selector = alt.selection_single(fields=['state'])

	base = alt.Chart(df, title="Chart for grocery and pharmacy data").properties(
		width=700,
		height=500
	).add_selection(selector)

	heatmap = base.mark_rect().encode(
		x=alt.X('date:T', bin=alt.Bin(maxbins=150), axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y=alt.Y('state:N', title="State"),
		color = alt.condition(selector,
							 'grocery_and_pharmacy_percent_change_from_baseline:Q',
							 alt.value('lightgray'),
							 scale=alt.Scale(scheme='blueorange',domain=[-70,0,45])),
		tooltip = [alt.Tooltip('state:N'),
				   alt.Tooltip('date:T'),
				   alt.Tooltip('grocery_and_pharmacy_percent_change_from_baseline:Q',title = "percentage"),
				   alt.Tooltip('cases:Q'),alt.Tooltip('deaths:Q')]
	)

	line = base.mark_line().encode(
		x=alt.X('date:T', axis = alt.Axis(title = 'Date'.upper(), format = ("%m %Y"))),
		y='cases',
		color='state',tooltip = [alt.Tooltip('state:N')]
	).transform_filter(
		selector
	)

	return alt.vconcat(
		heatmap,
		line
	).resolve_scale(
		x='shared'
	)
	

