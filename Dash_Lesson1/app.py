import dash
from dash import html, dcc, dash_table, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df=pd.read_csv('data/dummy_data_leads.csv')
#datos acumulados
df.sort_values(by=['Day', 'Dates', 'Fuente'])
df['CantiAcum']=df.groupby(['Fuente'])['conteo'].transform(lambda x:x.cumsum())

#listas para filtrar
fuentes_l=df.Fuente.unique()
continente_l=df.Continente.unique()


#iniciar app dash
app=dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

#funciones cde graficos

def barras_continentes():
    df_agregado=df.groupby('Continente')['conteo'].sum().reset_index()
    fig=px.bar(
        df_agregado,
        x='Continente',
        y='conteo',
        color='Continente' 

    )
    return fig

#grafico scatter

def scatter_plot():
    df_acum=df.groupby(['Day', 'Fuente'])['CantiAcum'].sum().reset_index(name='acumulado')
    fig=px.scatter(
        df_acum,
        x='Day',
        y='acumulado',
        color='Fuente',
        size='acumulado'
    )
    return fig

#tabla de redes sociales
def table_socialmedia():
    table_class = "h5 text-body text-nowrap"
    facebook = html.Span(
        [html.I(className="fa-brands fa-facebook"), " facebook"], className=table_class
    )
    twitter = html.Span(
        [html.I(className="fa-brands fa-twitter"), " twitter"], className=table_class
    )
    tiktok = html.Span(
        [html.I(className="fa-brands fa-tiktok"), " tiktok"], className=table_class
    )
    df_table=pd.DataFrame(
        {
            facebook:[],
            twitter:[],
            tiktok:[]



        }

    )
    return dbc.Table.from_dataframe(df_table, bordered=False, hover=True)




#iniciar layout
app.layout=dbc.Container( [
        html.H1('Leads Marketing',
                style={
                    'textAlign':'center',
                    'color':'#f07167'
                }
                ),
        dbc.Row([
            dbc.Col([
                html.H1('Barras por Continente', style={
                    'textAlign':'center',
                    'color':'black'
                }),
            dcc.Dropdown(id='filtro_fuentes',
                         
                         options=[{
                            'label':fuente, 'value':fuente
                         } for fuente in fuentes_l]
                         ),


                dcc.Graph(id='nombre_id_barras',
                         figure=barras_continentes() 
                       
                          )

            ]),

            dbc.Col([
                html.H1('Scatter por Fuente', style={
                    'textAlign':'center',
                    'color':'black'
                }),
                dcc.Dropdown(id='continente_filtrar',
                             options=[{
                                 'label':continente, 'value':continente

                             } for continente in continente_l]
                             
                             ),

                dcc.Graph(id='nombre_id_scatter',
                          figure=scatter_plot()
                          )

            ])



        ]),
        dbc.Row(

                dbc.Col([
                    html.Div([table_socialmedia()])

                ])
        )
        



],
style={
    'backgroundColor':'#f8f9fa',

}

)


@app.callback(
        Output('nombre_id_barras', 'figure'),
        Input('filtro_fuentes', 'value')
)
def barras_continentes(fuente_id):
    df_filtrado=df[df['Fuente']==fuente_id]
    df_agregado=df_filtrado.groupby('Continente')['conteo'].sum().reset_index()
    fig=px.bar(
        df_agregado,
        x='Continente',
        y='conteo',
        color='Continente' 

    )
    fig.layout.paper_bgcolor='#f8f9fa'
    fig.layout.plot_bgcolor='#f8f9fa'
    return fig

@app.callback(
    Output('nombre_id_scatter','figure'),
    Input('continente_filtrar','value')
)
def scatter_plot(continente_id):
    df_filtrar=df[df['Continente']==continente_id]
    df_acum=df_filtrar.groupby(['Day', 'Fuente'])['CantiAcum'].sum().reset_index(name='acumulado')
    fig=px.scatter(
        df_acum,
        x='Day',
        y='acumulado',
        color='Fuente',
        size='acumulado'
    )
    fig.layout.paper_bgcolor='#f8f9fa'
    fig.layout.plot_bgcolor='#f8f9fa'

    return fig



if __name__=='__main__':
    app.run_server(debug=True)