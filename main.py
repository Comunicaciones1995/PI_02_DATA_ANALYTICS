# IMPORTACIÓN DE LIBRERIAS...
import pandas as pd
import dash
from dash import html, dcc, callback, Output, Input, dash_table
import funciones

# CARGA DE DATOS...
hechos_homicidios = pd.read_parquet("dataset_limpio/hechos_homicidios.parquet")
victimas_homicidios = pd.read_parquet("dataset_limpio/victimas_homicidios.parquet")
hechos_lesiones = pd.read_parquet("dataset_limpio/hechos_lesiones.parquet")
victimas_lesiones = pd.read_parquet("dataset_limpio/victimas_lesiones.parquet")

# INICIALIZAR LA APLICACIÓN Dash...
app = dash.Dash(__name__)

# App LAYOUT...
def create_layout():
    return html.Div(style={'backgroundColor': '#FFC0CB'}, children=[
        funciones.create_header(),
        funciones.create_layout_01(),
        funciones.create_layout_02(),
        funciones.create_layout_03(),
        funciones.create_layout_04(),
        funciones.create_kpis()
    ])

#--------------------------------------------------------------------------------------------------------------------------------

# FUNCIÓN PARA CALCULAR EL PRIMER KPI:
poblacion_total = 3120612

def calcular_kpi(hechos_homicidios, poblacion_total):
    primer_semestre = hechos_homicidios[(hechos_homicidios['AÑO'] == 2021) & (hechos_homicidios['MES'] >= 1) & (hechos_homicidios['MES'] <= 6)]
    segundo_semestre = hechos_homicidios[(hechos_homicidios['AÑO'] == 2021) & (hechos_homicidios['MES'] >= 7) & (hechos_homicidios['MES'] <= 12)]

    cantidad_primer_semestre = primer_semestre['ID'].count()
    cantidad_segundo_semestre = segundo_semestre['ID'].count()

    tasa_primer_semestre = (cantidad_primer_semestre / poblacion_total) * 100000
    tasa_segundo_semestre = (cantidad_segundo_semestre / poblacion_total) * 100000

    diferencia_tasas = tasa_primer_semestre - tasa_segundo_semestre
    porcentaje_reduccion = (diferencia_tasas / tasa_primer_semestre) * 100

    return tasa_primer_semestre, tasa_segundo_semestre, diferencia_tasas, porcentaje_reduccion

# FUNCIÓN PARA CALCULAR EL SEGUNDO KPI:
df_datos_MOTOS_2021 = hechos_homicidios[hechos_homicidios['AÑO'] == 2021]
df_datos_MOTOS_2020 = hechos_homicidios[hechos_homicidios['AÑO'] == 2020]

def calcular_kpi_accidentes_motos(df_datos_MOTOS_2020, df_datos_MOTOS_2021):
    count_accidentes_2020 = len(df_datos_MOTOS_2020[df_datos_MOTOS_2020['VICTIMA'] == 'MOTO'])
    count_accidentes_2021 = len(df_datos_MOTOS_2021[df_datos_MOTOS_2021['VICTIMA'] == 'MOTO'])

    if count_accidentes_2020 != 0:
        kpi_motos = ((count_accidentes_2020 - count_accidentes_2021) / count_accidentes_2020) * 100
    else:
        kpi_motos = None

    return count_accidentes_2020, count_accidentes_2021, kpi_motos

# FUNCIÓN PARA CALCULAR EL TERCER KPI:
df_datos_AUTO_2020 = hechos_homicidios[(hechos_homicidios['AÑO'] == 2020)]
df_datos_AUTO_2021 = hechos_homicidios[(hechos_homicidios['AÑO'] == 2021)]

def calcular_kpi_accidentes_autos(df_datos_AUTO_2020, df_datos_AUTO_2021):
    # Filtrar los últimos seis meses del año 2020 y los primeros seis meses del año 2021
    df_datos_AUTO_ultimos_seis_meses_2020 = df_datos_AUTO_2020[(df_datos_AUTO_2020['MES'] >= 7)]
    df_datos_AUTO_primeros_seis_meses_2021 = df_datos_AUTO_2021[(df_datos_AUTO_2021['MES'] <= 6)]

    # Contar la cantidad de valores "AUTO" en la columna 'VICTIMA' para los últimos seis meses del año 2020
    count_accidentes_ultimos_seis_meses_2020 = len(df_datos_AUTO_ultimos_seis_meses_2020[df_datos_AUTO_ultimos_seis_meses_2020['VICTIMA'] == 'AUTO'])

    # Contar la cantidad de valores "AUTO" en la columna 'VICTIMA' para los primeros seis meses del año 2021
    count_accidentes_primeros_seis_meses_2021 = len(df_datos_AUTO_primeros_seis_meses_2021[df_datos_AUTO_primeros_seis_meses_2021['VICTIMA'] == 'AUTO'])

    # Calcular el KPI
    if count_accidentes_ultimos_seis_meses_2020 != 0:
        kpi_autos = ((count_accidentes_ultimos_seis_meses_2020 - count_accidentes_primeros_seis_meses_2021) / count_accidentes_ultimos_seis_meses_2020) * 100
    else:
        kpi_autos = None

    return count_accidentes_ultimos_seis_meses_2020, count_accidentes_primeros_seis_meses_2021, kpi_autos

# FUNCIÓN PARA CALCULAR EL CUARTO KPI:
df_datos_SIN = victimas_lesiones[(victimas_lesiones['EDAD_VICTIMA'] == 30)]

def calcular_kpi_lesiones_personal_30_anos(df_datos_SIN):
    # Filtrar los últimos seis meses del año 2020 y los primeros seis meses del año 2021
    df_datos_SINIESTROS_2020 = df_datos_SIN[(df_datos_SIN['AÑO'] == 2020) & (df_datos_SIN['MES'] >= 7)]
    df_datos_SINIESTROS_2021 = df_datos_SIN[(df_datos_SIN['AÑO'] == 2021) & (df_datos_SIN['MES'] <= 6)]

    # Contar la cantidad de accidentes por lesiones del personal de 30 años en el año 2020
    count_datos_SINIESTROS_2020 = len(df_datos_SINIESTROS_2020)

    # Contar la cantidad de accidentes por lesiones del personal de 30 años en el año 2021
    count_datos_SINIESTROS_2021 = len(df_datos_SINIESTROS_2021)

    # Calcular el KPI
    if count_datos_SINIESTROS_2020 != 0:
        kpi_lesiones = ((count_datos_SINIESTROS_2020 - count_datos_SINIESTROS_2021) / count_datos_SINIESTROS_2020) * 100
    else:
        kpi_lesiones = None

    return count_datos_SINIESTROS_2020, count_datos_SINIESTROS_2021, kpi_lesiones

# FUNCIÓN PARA CALCULAR EL QUINTO KPI:
def calcular_kpi_lesiones_comuna01(hechos_lesiones):
    # Filtrar los últimos seis meses del año 2020 y los primeros seis meses del año 2021
    df_datos_COMUNA01_ultimos_seis_meses_2020 = hechos_lesiones[(hechos_lesiones['MES'] >= 7) & (hechos_lesiones['AÑO'] == 2020) & (hechos_lesiones['COMUNA'] == 1)]
    df_datos_COMUNA01_primeros_seis_meses_2021 = hechos_lesiones[(hechos_lesiones['MES'] <= 6) & (hechos_lesiones['AÑO'] == 2021) & (hechos_lesiones['COMUNA'] == 1)]

    # Contar la cantidad de accidentes por lesiones en la COMUNA 01 en los últimos seis meses del año 2020
    count_accidentes_ultimos_seis_meses_2020 = len(df_datos_COMUNA01_ultimos_seis_meses_2020)

    # Contar la cantidad de accidentes por lesiones en la COMUNA 01 en los primeros seis meses del año 2021
    count_accidentes_primeros_seis_meses_2021 = len(df_datos_COMUNA01_primeros_seis_meses_2021)

    # Calcular el KPI
    if count_accidentes_ultimos_seis_meses_2020 != 0:
        kpi_lesiones_comuna01 = ((count_accidentes_ultimos_seis_meses_2020 - count_accidentes_primeros_seis_meses_2021) / count_accidentes_ultimos_seis_meses_2020) * 100
    else:
        kpi_lesiones_comuna01 = None

    return count_accidentes_ultimos_seis_meses_2020, count_accidentes_primeros_seis_meses_2021, kpi_lesiones_comuna01

#------------------------------------------------------------------------------------------------------------------------------

# CALLBACK para actualizar el gráfico según el KPI seleccionado
@app.callback(
    [Output('kpi-info', 'children'),
     Output('plot-kpi', 'figure')],
    [Input('kpi-selector', 'value')]
)
def selector_kpi(selected_kpi):
    figure = None
    kpi_info = None

    if selected_kpi == 'KPI_01':
        tasa_primer_semestre, tasa_segundo_semestre, _, porcentaje_reduccion = calcular_kpi(hechos_homicidios, poblacion_total)
        kpi_info = funciones.kpi_01(tasa_primer_semestre, tasa_segundo_semestre, porcentaje_reduccion)

        figure = {
            'data': [
                {'x': ['Primer Semestre', 'Segundo Semestre'], 'y': [tasa_primer_semestre, tasa_segundo_semestre], 'type': 'bar', 'name': 'Tasa de homicidios'}
            ],
            'layout': {
                'title': 'Tasa de homicidios en siniestros viales por semestre (2021)',
                'xaxis': {'title': 'Semestre'},
                'yaxis': {'title': 'Tasa de homicidios por 100,000 habitantes'},
                'barmode': 'group',
            }
        }
    elif selected_kpi == 'KPI_02':
        count_accidentes_2020_motos, count_accidentes_2021_motos, kpi_motos = calcular_kpi_accidentes_motos(df_datos_MOTOS_2020, df_datos_MOTOS_2021)
        kpi_info = funciones.kpi_02(count_accidentes_2020_motos, count_accidentes_2021_motos, kpi_motos)

        figure = {
            'data': [
                {'x': ['2020', '2021'], 'y': [count_accidentes_2020_motos, count_accidentes_2021_motos], 'type': 'bar', 'name': 'Accidentes de MOTOS'}
            ],
            'layout': {
                'title': 'Accidentes de motos por año',
                'xaxis': {'title': 'Año'},
                'yaxis': {'title': 'Número de accidentes'},
                'barmode': 'group',
            }
        }
    elif selected_kpi == 'KPI_03':
        count_accidentes_ultimos_seis_meses_2020_autos, count_accidentes_primeros_seis_meses_2021_autos, kpi_autos = calcular_kpi_accidentes_autos(df_datos_AUTO_2020, df_datos_AUTO_2021)
        kpi_info = funciones.kpi_03(count_accidentes_ultimos_seis_meses_2020_autos, count_accidentes_primeros_seis_meses_2021_autos, kpi_autos)

        figure = {
            'data': [
                {'x': ['2020', '2021'], 'y': [count_accidentes_ultimos_seis_meses_2020_autos, count_accidentes_primeros_seis_meses_2021_autos], 'type': 'bar', 'name': 'Accidentes de AUTOS'}
            ],
            'layout': {
                'title': 'Accidentes de autos por año',
                'xaxis': {'title': 'Año'},
                'yaxis': {'title': 'Número de accidentes'},
                'barmode': 'group',
            }
        }
    elif selected_kpi == 'KPI_04':
        count_datos_SINIESTROS_2020, count_datos_SINIESTROS_2021, kpi_lesiones = calcular_kpi_lesiones_personal_30_anos(df_datos_SIN)
        kpi_info = funciones.kpi_04(count_datos_SINIESTROS_2020, count_datos_SINIESTROS_2021, kpi_lesiones)

        figure = {
            'data': [
                {'x': ['2020', '2021'], 'y': [count_datos_SINIESTROS_2020, count_datos_SINIESTROS_2021], 'type': 'bar', 'name': 'Accidentes de motos'}
            ],
            'layout': {
                'title': 'Accidentes de autos por año',
                'xaxis': {'title': 'Año'},
                'yaxis': {'title': 'Número de accidentes'},
                'barmode': 'group',
            }
        }        
    elif selected_kpi == 'KPI_05':
        count_accidentes_ultimos_seis_meses_2020_comuna01, count_accidentes_primeros_seis_meses_2021_comuna01, kpi_lesiones_comuna01 = calcular_kpi_lesiones_comuna01(hechos_lesiones)
        kpi_info = funciones.kpi_05(count_accidentes_ultimos_seis_meses_2020_comuna01, count_accidentes_primeros_seis_meses_2021_comuna01, kpi_lesiones_comuna01)

        figure = {
            'data': [
                {'x': ['últimos 6 meses del 2020', 'primeros 6 meses del 2021'], 'y': [count_accidentes_ultimos_seis_meses_2020_comuna01, count_accidentes_primeros_seis_meses_2021_comuna01], 'type': 'bar', 'name': 'Accidentes de motos'}
            ],
            'layout': {
                'title': 'Accidentes de autos por año',
                'xaxis': {'title': 'Año'},
                'yaxis': {'title': 'Número de accidentes'},
                'barmode': 'group',
            }
        }
    return kpi_info, figure

#-------------------------------------------------------------------------------------------------------------------------------

# CALLBACK para actualizar el gráfico según el DataFrame y la columna seleccionados
@app.callback(
    Output('plot-1', 'figure'),
    [Input('columna-selector-1', 'value')]
)
def update_graph_1(selected_column):
    return funciones.update_graph(hechos_homicidios, selected_column, fig_size=(1500, 800))

# CALLBACK para actualizar el gráfico según el DataFrame y la columna seleccionados
@app.callback(
    Output('plot-2', 'figure'),
    [Input('columna-selector-2', 'value')]
)
def update_graph_2(selected_column):
    return funciones.update_graph(victimas_homicidios, selected_column, fig_size=(1500, 800))

# CALLBACK para actualizar el gráfico según el DataFrame y la columna seleccionados
@app.callback(
    Output('plot-3', 'figure'),
    [Input('columna-selector-3', 'value')]
)
def update_graph_3(selected_column):
    return funciones.update_graph(hechos_lesiones, selected_column, fig_size=(1500, 800))

# CALLBACK para actualizar el gráfico según el DataFrame y la columna seleccionados
@app.callback(
    Output('plot-4', 'figure'),
    [Input('columna-selector-4', 'value')]
)
def update_graph_4(selected_column):
    return funciones.update_graph(victimas_lesiones, selected_column, fig_size=(1500, 800))

# ASIGNA EL DISEÑO A LA APLICACIÓN...
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port=8050, debug=True, threaded=True, use_reloader=False)
