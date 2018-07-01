# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import numpy as np
import pandas as pd
from dash.dependencies import Output, Input
from datetime import datetime as dt
from datetime import date
import plotly.figure_factory as ff
from textwrap import dedent
import webbrowser


#Important Declarations
use_as_index = list(range(24))

#App Initialisation
app = dash.Dash()
app.config['suppress_callback_exceptions']=True

#Data Extraction
df1 = pd.read_excel('data.xlsx', 'Daily', index_col='Date') #Total Data
df2 = pd.read_excel('data.xlsx', 'Hourly', index_col='Date') #Hourly Data
df3 = pd.read_excel('data.xlsx', 'CrA', index_col='Date') #Breakup on criterion A
df4 = pd.read_excel('data.xlsx', 'CrB', index_col='Date') #Breakup on criterion B
	
df1.index = pd.to_datetime(df1.index)

#App Structure
app.layout = html.Div(children=[

	html.Div(children=[

						html.H1(children='DASH'),
						html.H5(children='Data Visualisation Project'),

					],
			style={'textAlign':'center'}
			),

	dcc.Markdown(dedent('''
		## Some guidelines:
		- Graphs are dynamically updated as the dates are changed
		- Graphs can be zoomed in by drawing a rectangle pver the focus area
		- Graphs can be zoomed out back to the original state by double-click

		''')),

	html.Hr(),

	html.H2(children='Monthly Analysis'),

	dcc.DatePickerRange(
		id='monthly-date-picker-range',
		min_date_allowed=dt(2016, 6, 1),
		max_date_allowed=dt(2018, 7, 29),
		start_date=dt(2017, 1, 1),
		end_date=dt(2017, 12, 31)
	),

	html.Br(),
	html.Br(),

	html.Div(id='output-graph-1'), 
	html.Hr(),

	html.H2(children='Daily Analysis'),
	dcc.DatePickerSingle(id='daily-date', date=date(2017, 6, 30), display_format='DD-MM-Y'),
	
	html.Br(),
	html.Br(),
	
	html.Div(children=[dcc.Graph(id='test')], style={'width':'30%', 'display':'inline-block'}),
	html.Div(id='output-graph-2', style={'width':'70%', 'display':'inline-block', 'marginBottom':200,}),      
	
	html.Hr(),

	html.H2(children='Criterion A Breakup'),
	html.Label('Select Dates:'),

	dcc.DatePickerRange(
		id='a-date-picker-range',
		min_date_allowed=dt(2016, 6, 1),
		max_date_allowed=dt(2018, 7, 29),
		start_date=dt(2017, 1, 2),
		end_date=dt(2017, 12, 31),
		display_format='DD-MM-Y'
	),

	html.Br(),
	html.Br(),
	
	html.Div(children=[

		html.Div(children=[

			html.Div(id='output-graph-a-1'),
			html.Div(id='output-graph-a-2')

			], 
			style={'display':'inline-block', 'width':'50%'}
			),

		html.Div(children=[

			html.Div(id='output-graph-a-3'),
			html.Div(id='output-graph-a-4')

			], 
			style={'display':'inline-block', 'width':'50%'}
			),

	]), 

	html.Hr(),

	html.H2(children='Criterion B Breakup'),
	html.Label('Select Dates:'),
	
	dcc.DatePickerRange(
		id='b-date-picker-range',
		min_date_allowed=dt(2016, 6, 1),
		max_date_allowed=dt(2018, 7, 29),
		start_date=dt(2017, 1, 2),
		end_date=dt(2017, 12, 31),
		display_format='DD-MM-Y'
	),

	html.Br(),
	html.Br(),
	
	html.Div(children=[

		html.Div(children=[

			html.Div(id='output-graph-b-1'),
			html.Div(id='output-graph-b-2')

			], 
			style={'display':'inline-block', 'width':'50%'}
			),

		html.Div(children=[

			html.Div(id='output-graph-b-3'),
			html.Div(id='output-graph-b-4')

			], 
			style={'display':'inline-block', 'width':'50%'}
			),

	]),




], style={
			'margin': 10,
			'fontFamily': '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif',
			'fontSize': 15,
			'borderWidth':'1px',
			'borderStyle':'dashed',
			'padding':25,
		})

#App Functionality
@app.callback(
	Output(component_id='output-graph-1', component_property='children'),
	[Input(component_id='monthly-date-picker-range', component_property='start_date'),
	Input(component_id='monthly-date-picker-range', component_property='end_date')]
)

def update_graph_1(start_date, end_date):

	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)

	display = df1.loc[start_date:end_date]

	return dcc.Graph(
		id='monthly-graph',
		figure={
			'data': [{'x': display.index, 'y' : display['PredictedValue'], 'type': 'line', 'name': 'Predicted'},
						{'x': display.index, 'y' : display['ActualValue'], 'type': 'line', 'name': 'Actual'}
					],
			'layout' : { 'title' : 'Data between specified dates' }
		}
	)

@app.callback(
	Output(component_id='output-graph-2', component_property='children'),
	[Input(component_id='daily-date', component_property='date')]
)

def update_graph_2(daily_date):


	date = dt.strptime(daily_date, '%Y-%m-%d')
	
	date_string = date.strftime('%d/%m/%Y')


	df = df2.copy()
	df.index=df.index.strftime("%d/%m/%Y %H:%M:%S")
	display=df[df.index.str.contains(date_string)]

	return dcc.Graph(
		id='Daily-graph',
		figure={
			'data': [{'x': display.index, 'y' : display['PredictedVolume'], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display['ActualVolume'], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : 'Daily Graph' }
		}
	)

@app.callback(
	Output('test', 'figure'),
	[Input('daily-date', 'date')])

def generate_table(daily_date):											#Generating a table-friendly dataframe
	date = dt.strptime(daily_date, '%Y-%m-%d')
	date_string = date.strftime('%d/%m/%Y')
	df = df2.copy()
	df.index=df.index.strftime("%d/%m/%Y %H:%M")
	display=df[df.index.str.contains(date_string)]
	display.insert(column='abc', value=use_as_index, loc=0)
	display.insert(column='Date', value=display.index, loc=0)
	display.set_index('abc', inplace=True)
	
	new_table_figure = ff.create_table(display)
	return new_table_figure

@app.callback(
	Output(component_id='output-graph-a-1', component_property='children'),
	[Input(component_id='a-date-picker-range', component_property='start_date'),
	Input(component_id='a-date-picker-range', component_property='end_date')]
)

def update_graph_a_1(start_date, end_date):

	a_type = 'A'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = a_type+' Actual'
	predicted = a_type+' Predicted'
	title_a = 'Data for: '+a_type

	temp = df3.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='a-graph-1',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_a }
		}
	)

@app.callback(
	Output(component_id='output-graph-a-2', component_property='children'),
	[Input(component_id='a-date-picker-range', component_property='start_date'),
	Input(component_id='a-date-picker-range', component_property='end_date')]
)

def update_graph_a_2(start_date, end_date):

	a_type = 'B'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = a_type+' Actual'
	predicted = a_type+' Predicted'
	title_a = 'Data for: '+a_type

	temp = df3.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='a-graph-2',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_a }
		}
	)

@app.callback(
	Output(component_id='output-graph-a-3', component_property='children'),
	[Input(component_id='a-date-picker-range', component_property='start_date'),
	Input(component_id='a-date-picker-range', component_property='end_date')]
)

def update_graph_a_3(start_date, end_date):

	a_type = 'C'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = a_type+' Actual'
	predicted = a_type+' Predicted'
	title_a = 'Data for: '+a_type

	temp = df3.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='a-graph-3',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_a }
		}
	)

@app.callback(
	Output(component_id='output-graph-a-4', component_property='children'),
	[Input(component_id='a-date-picker-range', component_property='start_date'),
	Input(component_id='a-date-picker-range', component_property='end_date')]
)

def update_graph_a_4(start_date, end_date):

	a_type = 'D'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = a_type+' Actual'
	predicted = a_type+' Predicted'
	title_a = 'Data for: '+a_type

	temp = df3.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='a-graph-4',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_a }
		}
	)

@app.callback(
	Output(component_id='output-graph-b-1', component_property='children'),
	[Input(component_id='b-date-picker-range', component_property='start_date'),
	Input(component_id='b-date-picker-range', component_property='end_date')]
)

def update_graph_b_1(start_date, end_date):

	b_type = 'A'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = b_type+' Actual'
	predicted = b_type+' Predicted'
	title_b = 'Data for: '+b_type

	temp = df4.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='b-graph-1',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_b }
		}
	)

@app.callback(
	Output(component_id='output-graph-b-2', component_property='children'),
	[Input(component_id='b-date-picker-range', component_property='start_date'),
	Input(component_id='b-date-picker-range', component_property='end_date')]
)

def update_graph_b_2(start_date, end_date):

	b_type = 'B'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = b_type+' Actual'
	predicted = b_type+' Predicted'
	title_b = 'Data for: '+b_type

	temp = df4.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='b-graph-2',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_b }
		}
	)

@app.callback(
	Output(component_id='output-graph-b-3', component_property='children'),
	[Input(component_id='b-date-picker-range', component_property='start_date'),
	Input(component_id='b-date-picker-range', component_property='end_date')]
)

def update_graph_b_3(start_date, end_date):

	b_type = 'C'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = b_type+' Actual'
	predicted = b_type+' Predicted'
	title_b = 'Data for: '+b_type

	temp = df4.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='b-graph-3',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_b }
		}
	)

@app.callback(
	Output(component_id='output-graph-b-4', component_property='children'),
	[Input(component_id='b-date-picker-range', component_property='start_date'),
	Input(component_id='b-date-picker-range', component_property='end_date')]
)

def update_graph_b_4(start_date, end_date):

	b_type = 'D'
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)
	
	actual = b_type+' Actual'
	predicted = b_type+' Predicted'
	title_b = 'Data for: '+b_type

	temp = df4.copy()
	display = temp.loc[start_date:end_date]

	return dcc.Graph(
		id='b-graph-4',
		figure={
			'data': [{'x': display.index, 'y' : display[predicted], 'type': 'line', 'name': 'Predicted Value'},
						{'x': display.index, 'y' : display[actual], 'type': 'line', 'name': 'Actual Value'}
					],
			'layout' : { 'title' : title_b }
		}
	)

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

#Starting local server
if __name__ == '__main__':
    app.run_server(debug=True)
