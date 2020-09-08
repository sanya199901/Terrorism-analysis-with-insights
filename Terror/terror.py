import pandas as pd
import dash
import dash_html_components as html
import webbrowser
from dash.dependencies import Input,Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate


# Global variables

app = dash.Dash()  # creating object of our app

def load_data():

    global df, countries, years, year_list, month, day_list, day, region, state, city, attack_type,\
world_chart_options, token

    token = 'pk.eyJ1IjoiZGVldmVzaGl6bSIsImEiOiJja2VrenI3amEwZXJtMnNwd242YW42ajJpIn0.FqsxGZu5Q5vUAjNRIq6IvA'

    

    file_name = "terror101.csv"

    df = pd.read_csv(file_name)
    pd.options.mode.chained_assignment = None

    month_dict = {'January': 1,
                  'February': 2,
                  'March': 3,
                  'April': 4,
                  'May': 5,
                  'June': 6,
                  'July': 7,
                  'August': 8,
                  'September': 9,
                  'October': 10,
                  'November': 11,
                  'December': 12}

    month = [{'label': key, 'value': value} for key, value in month_dict.items()]

    day_list = [x for x in range(1, 32)]

    day = [{'label': str(x), 'value': x} for x in day_list]

    region = [{'label': str(i), 'value': str(i)} for i in sorted(df['region_txt'].unique().tolist())]

    

    # Taking all the countries in the form of a list

    # temp_list = sorted(df["country_txt"].unique().tolist())

    # Converting that country list (temp_list) to a list of Dictionary as the in dcc.Dropdown,

    # The option argument accepts list of dictionary only

    # countries = [{'label': str(i), 'value': str(i)} for i in sorted(df["country_txt"].unique().tolist())]

    countries = df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()

    

    # state = [{'label': str(i), 'value': str(i)} for i in df['provstate'].unique().tolist()]

    state = df.groupby('country_txt')['provstate'].unique().apply(list).to_dict()

    

    # city = [{'label': str(i), 'value': str(i)} for i in df['city'].unique().tolist()]

    city = df.groupby('provstate')['city'].unique().apply(list).to_dict()

    

    attack_type = [{'label': str(i), 'value': str(i)} for i in df['attacktype1_txt'].unique().tolist()]

    

    # Creating a year_list

    year_list = sorted(df['iyear'].unique().tolist())

    # converting the year_list into a dictionary as the dcc.Slider takes a dictionary as an input in the marks argument

    years = {str(year): str(year) for year in year_list}

    

    # Global Chart tool options

    chart_dropdown_values = {

        'Terrorist Organisation': 'gname',

        'Target Nationality': 'natlty1_txt',

        'Target Type': 'targtype1_txt',

        'Type of Attack': 'attacktype1_txt',

        'Weapon Type': 'weaptype1_txt',

        'Region': 'region_txt',

        'Country Attacked': 'country_txt'

    }

    world_chart_options = [{'label': key, 'value': value} for key, value in chart_dropdown_values.items()]





def open_webbrowser():

    url = "http://127.0.0.1:8050/"  # Dash always runs the server on this ip:port address http://127.0.0.1:8050/

    webbrowser.open_new(url)


def create_app_ui():

    main_layout = html.Div(id='body', style={'fontFamily': 'Arial, Helvetica, sans-serif'}, children=[

        html.Div(id='heading', children=[

            html.H1(id='head', style={'textAlign': 'center'}, children='TERRORISM ANALYSIS AND INSIGHTS'),

            html.Br(),

            

            dcc.Tabs(id='tabs', value='Map', children=[

                dcc.Tab(label='Map Tool', id='map tool', value='Map', children=[

                    dcc.Tabs(id='subtabs', value='WorldMap', children=[

                        dcc.Tab(label='World Map', id='world map', value='WorldMap', children=[

                        ]),

                        dcc.Tab(label='India Map', id='india map', value='IndiaMap', children=[

                        ])

                    ]),

                    html.Br(),

                    html.H2(children='Map Filters', id='filter'),

                    dcc.Dropdown(id='month',

                                 options=month,

                                 placeholder='Select Month',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    dcc.Dropdown(id='day',

                                 options=day,

                                 placeholder='Select Day',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    dcc.Dropdown(id='region',

                                 options=region,

                                 placeholder='Select Region',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    dcc.Dropdown(id='country',

                                 options=[{'label': 'All', 'value': 'All'}],

                                 placeholder='Select Country',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    dcc.Dropdown(id='state',

                                 options=[{'label': 'All', 'value': 'All'}],

                                 placeholder='Select State',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    dcc.Dropdown(id='city',

                                 options=[{'label': 'All', 'value': 'All'}],

                                 placeholder='Select City',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    dcc.Dropdown(id='attack_type',

                                 options=attack_type,

                                 placeholder='Select Attack Type',  # default value

                                 style={'width': 300, 'borderRadius': '15px'},

                                 multi=True

                                 ),

                    html.Br(),

                    html.H2(children='Select the year', id='year_title'),

                    dcc.RangeSlider(id='year-slider',

                                    min=min(year_list),

                                    max=max(year_list),

                                    value=[min(year_list), max(year_list)],

                                    marks=years,  # Slider values

                                    step=None

                                    ),

                    html.Br()

                ]),

                dcc.Tab(label='Chart Tool', id='chart tool', value='Chart', children=[

                    dcc.Tabs(id='subtabs2', value='WorldChart', children=[

                        dcc.Tab(label='World Chart', id='world_chart', value='WorldChart', children=[]),

                        dcc.Tab(label='India Chart', id='india chart', value='IndiaChart')

                    ]),

                    html.Br(),

                    html.H2(id='chartFilter', children='Chart Filters'),

                    dcc.Dropdown(id='chart',

                                 options=world_chart_options,

                                 placeholder='Select an option',

                                 value='region_txt',

                                 style={'width': 300, 'borderRadius': '15px'}

                                 ),

                    html.Br(),

                    dcc.Input(id='search',

                              placeholder='Search Filter',

                              style={'width': 293, 'borderRadius': '13px', 'height': 26}

                              ),

                    html.Br(),

                    html.Br(),

                    html.H2(children='Select Year Range'),

                    dcc.RangeSlider(id='cyear_slider',

                                    min=min(year_list),

                                    max=max(year_list),

                                    value=[min(year_list), max(year_list)],

                                    marks=years,  # Slider values

                                    step=None

                                    ),

                    html.Br()

                ])

            ])

        ]),

        html.Br(),

        html.Div(id='graph', children='Graph will be shown here')

    ])

    return main_layout





@app.callback(

    Output('graph', 'children'),

    [Input('tabs', 'value'),

     Input('month', 'value'),

     Input('day', 'value'),

     Input('region', 'value'),

     Input('country', 'value'),

     Input('state', 'value'),

     Input('city', 'value'),

     Input('attack_type', 'value'),

     Input('year-slider', 'value'),

     Input('cyear_slider', 'value'),

     

     Input('chart', 'value'),

     Input('search', 'value'),

     Input('subtabs2', 'value')

     ]

)

def update_app_ui(tabs, month_value, day_value, region_value, country_value, state_value, city_value, attack_type_val,

                  year_value, cyear_value, chart_dp_values, search, subtabs2):

    fig = None

    if tabs == 'Map':

        print('Data type of month : ', str(type(month_value)))

        print('Month selected ', str(month_value))

        print('Data type of day : ', str(type(day_value)))

        print('day selected ', str(day_value))

        print('Data type of region : ', str(type(region_value)))

        print('Region selected ', str(region_value))

        print('Data type of country : ', str(type(country_value)))

        print('Country selected ', str(country_value))

        print('Data type of state : ', str(type(state_value)))

        print('State selected ', str(state_value))

        print('Data type of city : ', str(type(city_value)))

        print('city selected ', str(city_value))

        print('Data type of attack type : ', str(type(attack_type_val)))

        print('Attack type selected ', str(attack_type_val))

        print('Data type of year : ', str(type(year_value)))

        print('Year selected : ', str(year_value))

    

        # year range/year slider

        year_range = range(year_value[0], year_value[1] + 1)

        new_df = df[df['iyear'].isin(year_range)]

    

        # month filter

        if month_value == [] or month_value is None:

            pass

        else:

            if day_value == [] or day_value is None:

                new_df = new_df[new_df['imonth'].isin(month_value)]

            else:

                new_df = new_df[(new_df['imonth'].isin(month_value))

                                & (new_df['iday'].isin(day_value))]



        # region country state city filter

        if region_value == [] or region_value is None:

            pass

        else:

            if country_value == [] or country_value is None:

                new_df = new_df[new_df['region_txt'].isin(region_value)]

            else:

                if state_value == [] or state_value is None:

                    new_df = new_df[(new_df['region_txt'].isin(region_value))

                                    & (new_df['country_txt'].isin(country_value))]

                else:

                    if city_value == [] or city_value is None:

                        new_df = new_df[(new_df['region_txt'].isin(region_value))

                                        & (new_df['country_txt'].isin(country_value))

                                        & (new_df['provstate'].isin(state_value))]

                    else:

                        new_df = new_df[(new_df['region_txt'].isin(region_value))

                                        & (new_df['country_txt'].isin(country_value))

                                        & (new_df['provstate'].isin(state_value))

                                        & (new_df['city'].isin(city_value))]



        # Attack type filter

        if attack_type_val == [] or attack_type_val is None:

            pass

        else:

            new_df = new_df[new_df['attacktype1_txt'].isin(attack_type_val)]



        # You should always set the figure for blank, since this callback

        # is called once when it is drawing for first time

        figure = go.Figure()

        if new_df.shape[0]:

            pass

        else:

            new_df = pd.DataFrame(

                columns=['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',

                         'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]



        figure = px.scatter_mapbox(new_df,

                                   lat='latitude',

                                   lon='longitude',

                                   hover_data=['region_txt', 'country_txt', 'provstate', 'city',

                                               'attacktype1_txt',

                                               'nkill',

                                               'iyear'],

                                   zoom=1,

                                   color='attacktype1_txt',

                                   height=650

                                   )



        figure.update_layout(

            mapbox_style='dark',
            mapbox_accesstoken=token,
            autosize=True,
            margin=dict(l=0, r=0, b=25, t=20),
            template='plotly_dark'

        )



        fig = figure



    elif tabs == 'Chart':

        fig = None

        year_range_c = range(cyear_value[0], cyear_value[1]+1)

        chart_df = df[df['iyear'].isin(year_range_c)]

        

        if subtabs2 == 'WorldChart':

            pass

        elif subtabs2 == 'IndiaChart':

            chart_df = chart_df[(chart_df['region_txt'] == 'South Asia') & (chart_df['country_txt'] == 'India')]

        if chart_dp_values is not None and chart_df.shape[0]:

            if search is not None:

                chart_df = chart_df.groupby('iyear')[chart_dp_values].value_counts().reset_index(name='count')

                chart_df = chart_df[chart_df[chart_dp_values].str.contains(search, case=False)]

            else:

                chart_df = chart_df.groupby('iyear')[chart_dp_values].value_counts().reset_index(name='count')

        if chart_df.shape[0]:

            pass

        else:

            chart_df = pd.DataFrame(columns=['iyear', 'count', chart_dp_values])

            chart_df.iloc[0] = [0, 0, 'No Data']

        chart_fig = px.area(chart_df,

                            x='iyear',

                            y='count',

                            color=chart_dp_values,

                            template='plotly_dark'

                            )

        fig = chart_fig

        

    return dcc.Graph(figure=fig)


@app.callback(

    Output('day', 'options'),
    [Input('month', 'value')]

)

def day_options(value):

    date_list = [x for x in range(1, 32)]

    option = []

    if value:

        option = [{"label": m, "value": m} for m in date_list]

    return option

@app.callback(

    [Output('region', 'value'),
     Output('region', 'disabled'),
     Output('country', 'value'),
     Output('country', 'disabled')],
    [Input('subtabs', 'value')]

)

def update_r(sub_value):

    region_v = None

    disabled_r = False

    country_v = None

    disabled_c = False

    if sub_value == 'WorldMap':

        pass

    elif sub_value == 'IndiaMap':

        region_v = ['South Asia']

        disabled_r = True

        country_v = ['India']

        disabled_c = True

    return region_v, disabled_r, country_v, disabled_c

    



@app.callback(

    Output('country', 'options'),
    [Input('region', 'value')]

)

def country_option(r_value):

    option = []

    if r_value is None:

        raise PreventUpdate

    else:

        for var in r_value:

            if var in countries.keys():

                option.extend(countries[var])

    return [{'label': m, 'value': m} for m in option]





@app.callback(

    Output('state', 'options'),
    [Input('country', 'value')]

)

def state_option(c_value):

    option = []

    if c_value is None:

        raise PreventUpdate

    else:

        for var in c_value:

            if var in state.keys():

                option.extend(state[var])

    return [{'label': m, 'value': m} for m in option]


@app.callback(

    Output('city', 'options'),
    [Input('state', 'value')]

)

def city_option(s_value):

    option = []

    if s_value is None:

        raise PreventUpdate

    else:

        for var in s_value:

            if var in city.keys():

                option.extend(city[var])

    return [{'label': m, 'value': m} for m in option]





def main():

    # webpage of the project
    print('Welcome to the project....!')

    load_data()

    open_webbrowser()

    

    global app

    app.layout = create_app_ui()

    app.title = "Terrorism Analysis And Insights"

    app.run_server()
    app = None
    df = None

    print('Thanku for using this project...!')



if __name__ == '__main__':

    main()