import pandas as pd
import numpy as np
import dash
from dash import html, dcc
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Carga de Datos...
hechos_homicidios = pd.read_parquet("dataset_limpio/hechos_homicidios.parquet")
victimas_homicidios = pd.read_parquet("dataset_limpio/victimas_homicidios.parquet")
hechos_lesiones = pd.read_parquet("dataset_limpio/hechos_lesiones.parquet")
victimas_lesiones = pd.read_parquet("dataset_limpio/victimas_lesiones.parquet")

def create_header():
    return html.Div(children = [
        html.H1(className = 'row', children = 'SINIESTROS VIALES EN LA CIUDAD DE BUENOS AIRES', style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

        html.Div(children = ''' "Dash": MARCO DE WEB PARA LOS DATOS DE SINIESTROS VIALES PROVINCIA DE BUENOS AIRES''')
    ]
)

# MENU DESPLEGABLE PARA ELEGIR LAS COLUMNAS DE LOS DATAFRAMES "hechos_homicidios" Y "victimas_homicidios"...

def create_layout_01():
    columnas_deseadas = ['NUMERO_DE_VICTIMAS', 'AÑO', 'MES', 'FRANJA_HORARIA', 'COMUNA', 'VICTIMA', 'ACUSADO']
    return html.Div([
        html.H3('Estudio del dataframe: hechos_homicidios', style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Dropdown(
            id='columna-selector-1',
            options=[
                {'label': columna, 'value': columna} for columna in columnas_deseadas
            ],
            value='AÑO',  # Valor predeterminado
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='plot-1'
        )
    ]
)

def create_layout_02():
    columnas_deseadas = ['AÑO', 'MES', 'ROL', 'VEHICULO_DE_VICTIMA', 'SEXO', 'EDAD']
    return html.Div([
        html.H3('Estudio del dataframe: victimas_homicidios', style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Dropdown(
            id='columna-selector-2',
            options=[
                {'label': columna, 'value': columna} for columna in columnas_deseadas
            ],
            value='AÑO',  # Valor predeterminado
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='plot-2'
        )
    ]
)

# MENU DESPLEGABLE PARA ELEGIR LAS COLUMNAS DE LOS DATAFRAMES "hechos_lesionados" Y "victimas_lesionados"...

def create_layout_03():
    columnas_deseadas = ['NUMERO_DE_VICTIMAS', 'AÑO', 'MES', 'DIA', 'FRANJA_HORARIA', 'COMUNA', 'VICTIMA', 'ACUSADO', 'GRAVEDAD', 'VEHICULO_SINIESTRO']
    return html.Div([
        html.H3('Estudio del dataframe: hechos_lesiones', style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Dropdown(
            id='columna-selector-3',
            options=[
                {'label': columna, 'value': columna} for columna in columnas_deseadas
            ],
            value='AÑO',  # Valor predeterminado
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='plot-3'
        )
    ]
)

def create_layout_04():
    columnas_deseadas = ['AÑO', 'MES', 'DIA', 'ROL', 'VEHICULO_DE_VICTIMA', 'SEXO', 'EDAD_VICTIMA', 'GRAVEDAD']
    return html.Div([
        html.H3('Estudio del dataframe: victimas_homicidios', style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Dropdown(
            id='columna-selector-4',
            options=[
                {'label': columna, 'value': columna} for columna in columnas_deseadas
            ],
            value='AÑO',  # Valor predeterminado
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='plot-4'
        )
    ]
)

# CREACIÓN DE LOS GRAFICOS PARA LOS DATAFRAMES "hechos_homicidios" y "victimas_homicidios"...

def update_graph(df, selected_column, fig_size=(800, 600)):

    # Calcular la frecuencia de cada valor en la columna seleccionada
    freq_values = df[selected_column].value_counts()

    # Crear un gráfico de barras con colores diferentes y etiquetas
    fig = px.bar(
        x=freq_values.index,
        y=freq_values.values,
        color=freq_values.index,
        labels={'x': f'Valores de {selected_column}', 'y': 'Frecuencia'},
        title=f'Frecuencia de valores en la columna {selected_column}'
    )

    # Agregar texto en la cima de cada barra
    fig.update_traces(text=freq_values.values, textposition='outside')

    # Ajustar el tamaño del gráfico
    fig.update_layout(width=fig_size[0], height=fig_size[1])

    return fig

# FUNCIONES PARA CALCULAR Y GRAFICAR LOS KPIs...

def create_kpis():
    return html.Div([
            html.H3('Estudio de los KPIs', style={'text-align': 'center', 'margin-bottom': '20px'}),
            dcc.Dropdown(
                id='kpi-selector',
                options=[
                    {'label': 'KPI 01', 'value': 'KPI_01'},
                    {'label': 'KPI 02', 'value': 'KPI_02'},
                    {'label': 'KPI 03', 'value': 'KPI_03'},
                    {'label': 'KPI 04', 'value': 'KPI_04'},
                    {'label': 'KPI 05', 'value': 'KPI_05'}
                ],
                value='KPI_01',  # Valor predeterminado
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='plot-kpi'), html.Div(id='kpi-info')
        ])

# KPI NUMERO 01:

def kpi_01(tasa_primer_semestre, tasa_segundo_semestre, porcentaje_reduccion):
    return html.Div([
            html.H3("KPI Nº 01: Reducir en un 10% la tasa de homicidios en siniestros viales de los últimos seis meses, en CABA, en comparación con la tasa de homicidios en siniestros viales del semestre anterior."),
            html.P(f"Tasa de homicidios en siniestros viales para el primer semestre de 2021: {tasa_primer_semestre}"),
            html.P(f"Tasa de homicidios en siniestros viales para el segundo semestre de 2021: {tasa_segundo_semestre}"),
            html.P(f"Porcentaje de reducción entre el primer y segundo semestre de 2021: {porcentaje_reduccion:.2f}%"),
            html.P("CONCLUSIONES FINALES DEL PRIMER KPI:"),
            html.P("En el primer KPI se calculó la tasa de homicidios del primer y segundo semestre del año 2021 en la Ciudad Autónoma de Buenos Aires. Luego, se calculó el porcentaje de reducción del segundo semestre en comparación al primer semestre, dando un valor del 22.2% de reducción."),
    ])

# KPI NUMERO 02:

def kpi_02(count_accidentes_2020_motos, count_accidentes_2021_motos, kpi_motos):
    return html.Div([
            html.H3("KPI Nº 02: Reducir en un 7% la cantidad de accidentes mortales de motociclistas en el último año, en CABA, respecto al año anterior."),
            html.P(f"Cantidad de accidentes en moto en el año 2020: {count_accidentes_2020_motos}"),
            html.P(f"Cantidad de accidentes en moto en el año 2021: {count_accidentes_2021_motos}"),
            html.P(f"Porcentaje de reducción en accidentes de motociclistas: {kpi_motos:.2f}%"),
            html.P("CONCLUSIONES FINALES DEL SEGUNDO KPI:"),
            html.P("En la segunda KPI se calculó la cantidad de accidentes mortales de motociclistas en siniestros viales entre el año 2021 y el año 2020 en la Ciudad Autónoma de Buenos Aires. Luego, se calculó el cambio en los valores de accidentes mortales en moto usando la fórmula citada, dando un valor definitivo del -73.8% en comparación al 2020, es decir que los accidentes por moto aumentaron un 73.8%. Esto muestra que no se produjo una reducción en el porcentaje de accidentes por motocicleta según la consigna."),
    ])

# KPI NUMERO 03:

def kpi_03(count_accidentes_ultimos_seis_meses_2020_autos, count_accidentes_primeros_seis_meses_2021_autos, kpi_autos):
    return html.Div([
            html.H3("KPI Nº 03: Reducir en un 15% la tasa de MORTALIDAD en siniestros viales producidos por AUTOS en los últimos seis meses, en CABA, en comparación con la tasa de MORTALIDAD en siniestros viales de AUTOS del semestre anterior."),
            html.P(f"Cantidad de accidentes en auto en los últimos seis meses de 2020: {count_accidentes_ultimos_seis_meses_2020_autos}"),
            html.P(f"Cantidad de accidentes en auto en los primeros seis meses de 2021: {count_accidentes_primeros_seis_meses_2021_autos}"),
            html.P(f"Porcentaje de reducción en la tasa de mortalidad de siniestros viales de autos: {kpi_autos:.2f}%"),
            html.P("CONCLUSIONES FINALES DEL TERCER KPI:"),
            html.P("En el tercer KPI se calculó la cantidad de accidentes mortales de autos en siniestros viales entre el año 2021 y el año 2020 en la Ciudad Autónoma de Buenos Aires. Luego, se calculó el cambio en los valores de accidentes mortales en auto, dando un valor definitivo del 37.50% en comparación al 2020, es decir que los accidentes por auto tuvieron variaciones entre los citados años. Esto muestra que se produjo una reducción en el porcentaje de accidentes por autos."),
    ])

# KPI NUMERO 04:

def kpi_04(count_datos_SINIESTROS_2020, count_datos_SINIESTROS_2021, kpi_lesiones):
    return html.Div([
            html.H3("KPI Nº 04: Reducir un 8% la tasa de LESIONES en siniestros viales producidos POR EL PERSONAL CON 30 AÑOS DE EDAD entre el año 2020 y el año 2021 en la provincia de Buenos Aires."),
            html.P(f"Cantidad de accidentes por lesiones del personal de 30 años en el año 2020: {count_datos_SINIESTROS_2020}"),
            html.P(f"Cantidad de accidentes por lesiones del personal de 30 años en el año 2021: {count_datos_SINIESTROS_2021}"),
            html.P(f"Porcentaje de reducción en la tasa de lesiones al personal de 30 años: {kpi_lesiones:.2f}%"),
            html.P("CONCLUSIONES FINALES DEL CUARTO KPI:"),
            html.P("En el cuarto KPI se calculó la cantidad de accidentes por lesiones del personal de 30 años de edad entre el año 2021 y el año 2020 en la Ciudad Autónoma de Buenos Aires. Luego, se calculó el cambio en los valores de accidentes por lesiones usando la fórmula citada, dando un valor definitivo del 1.79% en comparación al 2020, es decir que los accidentes por lesiones tuvieron una reducción del 1.79%. Esto muestra que se produjo una disminución en el porcentaje de accidentes por lesiones al personal de 30 años de edad. SIN EMBARGO, ESTO MUESTRA QUE NO SE CUMPLIÓ CON EL KPI PLANTEADO."),
    ])

# KPI NUMERO 05:

def kpi_05(count_accidentes_ultimos_seis_meses_2020_comuna01, count_accidentes_primeros_seis_meses_2021_comuna01, kpi_lesiones_comuna01):
    return html.Div([
            html.H3("KPI Nº 05: Reducir un 13% la tasa de LESIONES en siniestros viales producidos en la COMUNA 01 en los últimos seis meses, en CABA, en comparación con la tasa de MORTALIDAD en siniestros viales de AUTOS del semestre anterior."),
            html.P(f"Cantidad de accidentes por lesiones en la COMUNA 01 en los últimos seis meses de 2020: {count_accidentes_ultimos_seis_meses_2020_comuna01}"),
            html.P(f"Cantidad de accidentes por lesiones en la COMUNA 01 en los primeros seis meses de 2021: {count_accidentes_primeros_seis_meses_2021_comuna01}"),
            html.P(f"Porcentaje de reducción en la tasa de lesiones en la COMUNA 01: {kpi_lesiones_comuna01:.2f}%"),
            html.P("CONCLUSIONES FINALES DEL QUINTO KPI:"),
            html.P("En el quinto KPI se calculó la cantidad de accidentes por lesiones en la COMUNA 01 entre el año 2021 y el año 2020 en la Ciudad Autónoma de Buenos Aires. Luego, se calculó el cambio en los valores de accidentes por lesiones en la COMUNA 01, dando un valor definitivo del -14.75% en comparación al 2020, es decir que los accidentes por lesiones en la COMUNA 01 tuvieron un aumento del 14.75%. Esto muestra que NO se produjo una disminución en el porcentaje de accidentes por lesiones en la COMUNA 01 Y POR LO TANTO NO SE CUMPLE CON EL KPI PLANTEADO."),
    ])
