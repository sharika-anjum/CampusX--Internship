import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash
from dash.dependencies import Input, Output

user = pd.read_csv('users.csv')
eva = pd.read_csv('evaluation.csv')
data = user.merge(eva, left_on='user_id', right_on='user_id')
gyan = pd.read_csv('gyan.csv')
myday = pd.read_csv('myday.csv')

# merging and doing the necessary stuffs
users_and_gyan = user.merge(gyan, left_on='user_id', right_on='user_id')
gyan_ka_graph = users_and_gyan['batch_id'].value_counts().reset_index()
gyan_ka_graph.rename(columns={'index': 'batch id', 'batch_id': 'total number of gyans shared'}, inplace=True)
users_and_myday = user.merge(myday, left_on='user_id', right_on='user_id')
myday_ka_graph = users_and_myday['batch_id'].value_counts().reset_index()
myday_ka_graph.rename(columns={'index': 'batch id', 'batch_id': 'total number of myday shared'}, inplace=True)
m = pd.merge(myday, user, on='user_id')
g = pd.merge(gyan, user, on='user_id')
a = m['fname'].value_counts().reset_index()
g = g['fname'].value_counts().reset_index()
consis = pd.merge(g,a,on='index')
consis['score']=consis['fname_x']+consis['fname_x']
one = pd.merge(eva,user,on= 'user_id')

# cleaning data
user['college'].replace(['Amity University kolkata'], ['Amity University,Kolkata'], inplace=True)
user['college'].replace(['Amity University Kolkata'], ['Amity University,Kolkata'], inplace=True)
user['college'].replace(['Amity University'], ['Amity University,Kolkata'], inplace=True)
user['college'].replace(['Amity University, Kolkata'], ['Amity University,Kolkata'], inplace=True)
user['college'].replace(['Amity University kolkata '], ['Amity University,Kolkata'], inplace=True)
user['college'].replace(['ACADEMY OF TECHNOLOGY'], ['Academy of Technology'], inplace=True)
user['college'].replace(['Academy Of Technology'], ['Academy of Technology'], inplace=True)
user['college'].replace(['HETC, Hoogly'], ['Hoogly Engineering And Technology College'], inplace=True)
user['college'].replace(['Calcutta institute of engineering and management'],['Calcutta Institute of Engineering and Management'], inplace=True)
user.fillna({'college': 'not known'}, inplace=True)
user['college'].replace(['Techno main salt lake'], ['Techno Main Salt Lake'], inplace=True)
user['college'].replace(['Techno Main'], ['Techno Main Salt Lake'], inplace=True)
user['college'].replace(['Future Institute Of Engineering and Management'],
                        ['Future Institute of Engineering & Management'], inplace=True)
user['college'].replace(['Future Institute Of Engineering And Management '],
                        ['Future Institute of Engineering & Management'], inplace=True)

b = user['college'].unique().size

# making new dataframe
number = user['user_id'].count()
batches = user['batch_id'].max()

count = user['college'].value_counts().reset_index()
count.rename(columns={'index': 'college', 'college': 'frequency'}, inplace=True)

# To get the participation from various colleges so far

trace1 = go.Bar(x=count['college'], y=count['frequency'])

data1 = [trace1]

layout1 = go.Layout(title='Participation from different colleges so far',
                    xaxis={'title': '', 'automargin': True},
                    yaxis={'title': 'Counts'})

fig1 = go.Figure(data=data1, layout=layout1)

# to get which batch shares the most no. of gyans
trace2 = go.Pie(labels=gyan_ka_graph['batch id'], values=gyan_ka_graph['total number of gyans shared'],
                textposition='inside', textfont_size=14)

data2 = [trace2]

layout2 = go.Layout(title='total number of gyans shared by each batch')

fig2 = go.Figure(data=data2, layout=layout2)

# to get which batch shares the most no. of gyans
trace3 = go.Pie(labels=myday_ka_graph['batch id'], values=myday_ka_graph['total number of myday shared'],
                textposition='inside', textfont_size=14)

data3 = [trace3]

layout3 = go.Layout(title='total number of myday shared by each batch')

fig3 = go.Figure(data=data3, layout=layout3)

options1 = [
    {'label': 'Batch 1', 'value': '1'},
    {'label': 'Batch 2', 'value': '2'},
    {'label': 'Batch 3', 'value': '3'}

]

options2 = [
    {'label': 'gyan shared', 'value': 'gyan'},
    {'label': 'myday shared', 'value': 'myday'},
    {'label': 'consistency', 'value': 'consistency'}

]


external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous',

    }
]

campusx = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = campusx.server
campusx.layout = html.Div([
    html.H1("Campus-X", style={'color': '#fff', 'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("No. of Batches", className='text-light'),
                    html.H4(batches, className='text-light')
                ], className='card-body')
            ], className='card bg-warning h-100 m-auto')
        ], className='col-md-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("No. of Students enrolled", className='text-light'),
                    html.H4(number, className='text-light')
                ], className='card-body')
            ], className='card bg-info h-100 m-auto')
        ], className='col-md-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("No. of different colleges", className='text-light'),
                    html.H4(b, className='text-light')
                ], className='card-body')
            ], className='card bg-success h-100 m-auto')
        ], className='col-md-4'),
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='Bar', figure=fig1)
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-12'),
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options1, value='1'),
                    dcc.Graph(id='Line')
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-12')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker1',options=options2,value='gyan'),
                    dcc.Graph(id='Bar&Line')
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-12')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='Pie1', figure=fig2)
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='Pie', figure=fig3)
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-6'),
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker4', options=options1, value='1'),
                    dcc.Graph(id='Score')
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-12')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker2', options=options1, value='1'),
                    dcc.Graph(id='Late')
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker3', options=options1, value='1'),
                    dcc.Graph(id='Win')
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-6'),
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("THANK YOU!", className='bold', style={'color': 'grey', 'text-align': 'center'}),
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-12')
    ], className='row')

], className='container')


@campusx.callback(Output('Line', 'figure'), [Input('picker', 'value')])
def update_graph(type):
    if type=='1':
        single = data[data['batch_id']==1]
        performance = single.groupby('task_id')['score'].mean().reset_index()
        return {'data': [go.Scatter(x=performance['task_id'], y=performance['score'], mode='lines + markers')],
                'layout': go.Layout(title='Batch 1 vs average performance',
                                    xaxis={'title': 'Task_id','automargin': True},
                                    yaxis={'title': 'Average'})}
    elif type=='2':
        single = data[data['batch_id']==2]
        performance = single.groupby('task_id')['score'].mean().reset_index()
        return {'data': [go.Scatter(x=performance['task_id'], y=performance['score'], mode='lines + markers')],
                'layout': go.Layout(title='Batch 2 vs average performance',
                                    xaxis={'title': 'Task_id','automargin': True},
                                    yaxis={'title': 'Average'})}
    elif type=='3':
        single = data[data['batch_id']==3]
        performance = single.groupby('task_id')['score'].mean().reset_index()
        return {'data': [go.Scatter(x=performance['task_id'], y=performance['score'], mode='lines + markers')],
                'layout': go.Layout(title='Batch 3 vs average performance',
                                    xaxis={'title': 'Task_id','automargin': True},
                                    yaxis={'title': 'Average'})}

@campusx.callback(Output('Bar&Line', 'figure'), [Input('picker1', 'value')])
def update_graph(type):
    if type=='myday':
        return {'data': [go.Bar(x=a['index'],y=a['fname'])],
                'layout': go.Layout(title='No. of mydays shared',
                xaxis={'title':'','automargin': True},
                yaxis={'title':'Count'})}
    elif type=='gyan':
        return {'data': [go.Bar(x=g['index'],y=g['fname'])],
                'layout': go.Layout(title='No. of gyans shared',
                xaxis={'title':'','automargin': True},
                yaxis={'title':'Count'})}

    elif type=='consistency':
        return {'data': [go.Scatter(x=consis['index'],y=consis['score'],
                mode='lines+markers',
                marker={'color':'#00a65a'})],
                'layout': go.Layout(title='Consistency',
                xaxis={'title':'','automargin': True},
                yaxis={'title':''})}

@campusx.callback(Output('Score', 'figure'), [Input('picker4', 'value')])
def update_graph(type):
    if type=='1':
        ev = one[one['batch_id']==1]
        ev = ev.groupby('fname')['score'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Bar(x=ev['fname'],y=ev['score'])],
                'layout': go.Layout(title='Total marks',
                xaxis={'title':'name','automargin': True},
                yaxis={'title':'Count'})}

    elif type=='2':
        ev = one[one['batch_id']==2]
        ev = ev.groupby('fname')['score'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Bar(x=ev['fname'], y=ev['score'])],
                'layout': go.Layout(title='Total marks',
                                    xaxis={'title': 'name', 'automargin': True},
                                    yaxis={'title': 'Count'})}
    else:
        ev = one[one['batch_id']==3]
        ev = ev.groupby('fname')['score'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Bar(x=ev['fname'], y=ev['score'])],
                'layout': go.Layout(title='Total marks',
                                    xaxis={'title': 'name', 'automargin': True},
                                    yaxis={'title': 'Count'})}

@campusx.callback(Output('Late', 'figure'), [Input('picker2', 'value')])
def update_graph(type):
    if type=='1':
        ev = one[one['batch_id']==1]
        late=ev.groupby('fname')['late'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Scatter(x=late['fname'],y=late['late'],mode='lines+markers',
                marker={'color':'#00a65a'})],
                'layout': go.Layout(title='No. of lates',
                xaxis={'title':'', 'automargin': True},
                yaxis={'title':'Count'})}

    elif type=='2':
        ev = one[one['batch_id']==2]
        late = ev.groupby('fname')['late'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Scatter(x=late['fname'], y=late['late'], mode='lines+markers',
                                    marker={'color': '#00a65a'})],
                'layout': go.Layout(title='No. of lates',
                                    xaxis={'title': '', 'automargin': True},
                                    yaxis={'title': 'Count'})}

    else:
        ev = one[one['batch_id']==3]
        late = ev.groupby('fname')['late'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Scatter(x=late['fname'], y=late['late'], mode='lines+markers',
                                    marker={'color': '#00a65a'})],
                'layout': go.Layout(title='No. of lates',
                                    xaxis={'title': '', 'automargin': True},
                                    yaxis={'title': 'Count'})}

@campusx.callback(Output('Win', 'figure'), [Input('picker3', 'value')])
def update_graph(type):
    if type=='1':
        r = one[one['batch_id']==1]
        win = r.groupby('fname')['winner'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Scatter(x=win['fname'],y=win['winner'],mode='lines+markers',
                marker={'color':'#00a65a'})],
                'layout': go.Layout(title='No. of Wins',
                xaxis={'title':'', 'automargin': True},
                yaxis={'title':'Count'})}

    elif type=='2':
        r = one[one['batch_id']==2]
        win = r.groupby('fname')['winner'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Scatter(x=win['fname'], y=win['winner'], mode='lines+markers',
                                    marker={'color': '#00a65a'})],
                'layout': go.Layout(title='No. of Wins',
                                    xaxis={'title': '', 'automargin': True},
                                    yaxis={'title': 'Count'})}

    else:
        r = one[one['batch_id']==3]
        win = r.groupby('fname')['winner'].sum().sort_values(ascending=False).reset_index()
        return {'data': [go.Scatter(x=win['fname'], y=win['winner'], mode='lines+markers',
                                    marker={'color': '#00a65a'})],
                'layout': go.Layout(title='No. of Wins',
                                    xaxis={'title': '', 'automargin': True},
                                    yaxis={'title': 'Count'})}


if __name__=="__main__":
    campusx.run_server(debug=False)
