import pandas as pd

def calcular_tiempo_total(df):
    # Obtener la fecha del primer "on" y último "off"
    primer_registro = df[df['causa'] == 'on']['inicio'].iloc[0]
    ultimo_registro = df[df['causa'] == 'off']['fin'].iloc[-1]

    # Calcular el tiempo total en segundos
    tiempo_total = (ultimo_registro - primer_registro).total_seconds()
    return tiempo_total

def calcular_tiempos_prendido_y_apagado(df, tiempo_total):
    # Filtrar los registros de encendido (on) y apagado (off)
    encendido = df[df['causa'] == 'on']
    apagado = df[df['causa'] == 'off']
    # Calcular el tiempo prendido como la suma de los tiempos entre fin on y fin off
    tiempo_prendido = 0
    for i in range(len(encendido)):
        tiempo_prendido += (apagado['fin'].iloc[i] - encendido['fin'].iloc[i]).total_seconds()
    # Calcular el tiempo apagado como el tiempo total menos el tiempo prendido
    tiempo_apagado = tiempo_total - tiempo_prendido

    return tiempo_prendido, tiempo_apagado

def calcular_tiempos_pausado_y_en_ejecucion(df, tiempo_prendido):
    # calcular tiempo pausado como la suma de las duraciones de los registros pause
    tiempo_pausado = df[df['causa'] == 'pause']['duracion'].sum()
    tiempo_en_ejecucion = tiempo_prendido - tiempo_pausado
    return tiempo_pausado, tiempo_en_ejecucion

def calcular_tiempos_detectando_somnolencia_y_sin_detectar(df, tiempo_en_ejecucion):
    tiempo_microsueno = df[df['causa'] == 'microsueño']['duracion'].sum()
    tiempo_distraccion = df[df['causa'] == 'distraccion']['duracion'].sum()
    tiempo_detectando_somnolencia = tiempo_microsueno + tiempo_distraccion
    tiempo_sin_detectar_somnolencia = tiempo_en_ejecucion - tiempo_detectando_somnolencia
    return tiempo_detectando_somnolencia, tiempo_sin_detectar_somnolencia, tiempo_microsueno, tiempo_distraccion


def obtener_datos_para_grafico_torta(datos):
    tiempo_total = calcular_tiempo_total(datos)
    tiempo_prendido, tiempo_apagado = calcular_tiempos_prendido_y_apagado(datos, tiempo_total)
    tiempo_pausado, tiempo_en_ejecucion = calcular_tiempos_pausado_y_en_ejecucion(datos, tiempo_prendido)
    tiempo_detectando, tiempo_sin_detectar, tiempo_microsueno, tiempo_distraccion = calcular_tiempos_detectando_somnolencia_y_sin_detectar(datos, tiempo_en_ejecucion)
    datos_para_grafico_torta = { 
        "Tiempo total": tiempo_total,
        "Tiempo prendido": tiempo_prendido,
        "Tiempo apagado": tiempo_apagado,
        "Tiempo pausado": tiempo_pausado,
        "Tiempo en ejecucion": tiempo_en_ejecucion,
        "Tiempo detectando": tiempo_detectando,
        "Tiempo sin detectar": tiempo_sin_detectar,
        "Tiempo microsueno": tiempo_microsueno,
        "Tiempo distraccion": tiempo_distraccion
    }
    return datos_para_grafico_torta

def obtener_datos_para_barras_de_frecuencias_agrupadas_por_recorrido(df):
    recorridos = df['recorrido'].unique()
    causas = ['microsueño', 'distraccion', 'pause']

    frecuencias = []
    for recorrido in recorridos:
        filtro_recorrido = df['recorrido'] == recorrido
        frecuencias_recorrido = []
        for causa in causas:
            filtro_causa = df['causa'] == causa
            frecuencia = df[filtro_recorrido & filtro_causa].shape[0]
            frecuencias_recorrido.append(frecuencia)
        frecuencias.append(frecuencias_recorrido)
    
    x = recorridos
    y = zip(*frecuencias)
    return x, y

def obtener_datos_para_diagrama_de_areas_de_frecuencias_por_hora(df):
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M')
    microsuenos = df[df['causa'] == 'microsueño'].copy()
    distracciones = df[df['causa'] == 'distraccion'].copy()
    pausas = df[df['causa'] == 'pause'].copy()

    # Asignar valores a la columna "fecha" utilizando loc
    microsuenos.loc[:, 'fecha'] = microsuenos['hora']
    distracciones.loc[:, 'fecha'] = distracciones['hora']
    pausas.loc[:, 'fecha'] = pausas['hora']

    # Calcular la frecuencia por hora
    frecuencia_microsuenos = microsuenos.resample('H', on='fecha').size().fillna(0)
    frecuencia_distracciones = distracciones.resample('H', on='fecha').size().fillna(0)
    frecuencia_pausas = pausas.resample('H', on='fecha').size().fillna(0)
    datos_para_diagrama_de_frecuencias = {
        'microsuenos': frecuencia_microsuenos,
        'distracciones': frecuencia_distracciones,
        'pausas': frecuencia_pausas
    }
    return datos_para_diagrama_de_frecuencias