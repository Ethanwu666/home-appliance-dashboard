import dash_bootstrap_components as dbc
from dash import dcc, html

def create_layout(df):
    top_bar = dbc.Navbar(
        dbc.Container([
            dbc.Row([
   
    dbc.Col(html.Div(), width=True),
    dbc.Col(
        dcc.Input(
            id='top-search',
            type='text',
            placeholder='Search products and parts',
            style={'width': '420px', 'padding': '8px', 'borderRadius': '6px'}
        ),
        width='auto'
    )
], align='center', justify='between')

        ]),
        color='#c6daf7',
        dark=False,
        className='top-navbar'
    )

    # Product selector 
    product_options = [{'label': r, 'value': v} for r, v in zip(df['title'].str.slice(0,80), df['asin'])]

    # Main product display 
    product_area = dbc.Container([
        dbc.Row([
            dbc.Col([
                # : image 
                html.Div([
                    html.Div(id='no-regret-badge', style={'fontWeight': '700', 'color': '#e94e1b', 'fontSize': '18px', 'marginBottom': '6px'}),
                    html.Div(id='product-image', children=[
                        # placeholder image box
                        html.Div("Image", style={
                            'width': '360px', 'height': '360px', 'border': '1px solid #ddd', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center', 'backgroundColor': '#fff'
                        })
                    ]),
                ], style={'textAlign': 'center'})
            ], width=5),

            dbc.Col([
                # Right: title, price, competitor buttons
                html.H3(id='product-title', style={'marginTop': '10px'}),
                html.Div(id='product-sub', style={'color': '#666', 'marginBottom': '12px'}),
                html.H2(id='product-price', style={'color': '#1f77b4', 'marginTop': '6px'}),
                html.Div(id='product-savings', style={'color': '#1f77b4', 'fontWeight': '600', 'marginBottom': '10px'}),
                html.Div(id='comp-buttons', children=[
                    dbc.Button(id='comp-official', children="Official Website", color='warning', outline=True, className='me-2', style={'margin':'6px'}),
                    dbc.Button(id='comp-jd', children="JD.com", color='secondary', outline=True, className='me-2', style={'margin':'6px'}),
                    dbc.Button(id='comp-suning', children="Suning", color='secondary', outline=True, className='me-2', style={'margin':'6px'}),
                    dbc.Button(id='comp-tmall', children="Tmall Official", color='secondary', outline=True, className='me-2', style={'margin':'6px'})
                ]),
                html.Br(),
                # small selector and hidden store for asin
                dcc.Dropdown(id='product-selector', options=product_options, placeholder='Or pick a product...', style={'width':'100%'}),
            ], width=7)
        ], align='center', className='product-row')
    ], fluid=True)

    # Lower area with charts and KPIs: price trend (B,C), KPIs (D), comment histogram (E), radar (F)
    charts_area = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5("Price Trends", style={'marginTop': '6px'}),
                dcc.Graph(id='price-line-chart', config={'displayModeBar': False}),
                html.Div(id='promotion-calendar-placeholder', style={'fontSize':'12px','color':'#666','marginTop':'6px'})
            ], width=8),

            dbc.Col([
                html.H5("Key KPIs"),
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div("Lowest:", style={'fontSize':'14px','color':'#fff'}),
                            html.H4(id='kpi-lowest', style={'color':'#fff', 'marginTop':'6px'})
                        ], style={'backgroundColor':'#f26a21', 'padding':'10px', 'borderRadius':'8px', 'textAlign':'center', 'marginBottom':'8px'}),
                        html.Div([
                            html.Div("Average:", style={'fontSize':'13px'}),
                            html.H5(id='kpi-avg', style={'marginTop':'6px'})
                        ], style={'backgroundColor':'#e6eef8', 'padding':'10px', 'borderRadius':'8px', 'textAlign':'center', 'marginBottom':'8px'}),
                        html.Div([
                            html.Div("Volatility:", style={'fontSize':'13px'}),
                            html.H6(id='kpi-vol', style={'marginTop':'6px'})
                        ], style={'backgroundColor':'#f7f7f7', 'padding':'10px', 'borderRadius':'8px', 'textAlign':'center', 'marginBottom':'8px'}),
                        html.Div([
                            html.Div("Return Rate:", style={'fontSize':'13px'}),
                            html.H6(id='kpi-return', style={'marginTop':'6px'})
                        ], style={'backgroundColor':'#f7f7f7', 'padding':'10px', 'borderRadius':'8px', 'textAlign':'center'})
                    ])
                ], style={'border':'none', 'boxShadow':'none'})
            ], width=4)
        ], className='charts-row', align='start'),

        dbc.Row([
            dbc.Col([
                html.H5("Review Topics"),
                dcc.Graph(id='sentiment-histogram', config={'displayModeBar': False})
            ], width=6),

            dbc.Col([
                html.H5("Risk Radar"),
                dcc.Graph(id='risk-radar', config={'displayModeBar': False})
            ], width=6)
        ], align='start', style={'marginTop':'18px'}),
    ], fluid=True)

    # Combine all parts
    page = html.Div([
        top_bar,
        html.Br(),
        html.Div(children=[
            product_area,
            html.Hr(),
            charts_area
        ], style={'width': '95%', 'margin': '0 auto'})
    ])

    return page
