from datetime import datetime
import pandas as pd

def convertir_fecha(x):
    try:
        return datetime.strptime(x, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        return pd.NaT

def combinar_registros(df):
    nuevos_registros = []
    i = 0
    while i < len(df):
        if df['causa'][i] == 'pause' and i + 1 < len(df) and df['causa'][i + 1] == 'play':
            inicio_pause = df['inicio'][i]
            fin_play = df['fin'][i + 1]
            nuevos_registros.append([inicio_pause, fin_play, 'pause'])
            i += 2
        else:
            nuevos_registros.append([df['inicio'][i], df['fin'][i], df['causa'][i]])
            i += 1
    nuevo_df = pd.DataFrame(nuevos_registros, columns=['inicio', 'fin', 'causa'])
    return nuevo_df

def agregar_duracion(df):
    df['inicio'] = pd.to_datetime(df['inicio'])
    df['fin'] = pd.to_datetime(df['fin'])
    df['duracion'] = (df['fin'] - df['inicio']).dt.total_seconds()
    return df

def cargar_datos(archivo_csv):
    converters = {'inicio': convertir_fecha, 'fin': convertir_fecha}
    df = pd.read_csv(archivo_csv, converters=converters)
    # Verificar que todos los campos estén escritos correctamente
    df['causa'] = df['causa'].apply(lambda x: x.lower())
    df = df[df['causa'].isin(['microsueño', 'distraccion','on', 'off', 'pause', 'play'])]
    # Eliminar registros con irregularidades en cualquier campo o columna
    df = df.dropna()
    # Combinar registros de pausa y play
    df = combinar_registros(df)
    # Agregar duración de la alarma
    df = agregar_duracion(df)
    return df

def agregar_recorrido(df):
    recorrido = 0
    recorridos = []
    on_count = 0
    off_count = 0

    for index, row in df.iterrows():
        if row['causa'] == 'on':
            on_count += 1
            recorrido = on_count
        elif row['causa'] == 'off':
            off_count += 1
            recorrido = off_count
        recorridos.append(recorrido)

    df['recorrido'] = recorridos
    return df

def agregar_horas(df):
    # Convertir la columna "hora" en un objeto DateTime y extraer solo las horas
    df['hora'] = pd.to_datetime(df['inicio']).dt.time
    # Establecer formato
    df['hora'] = df['hora'].apply(lambda x: x.strftime('%H:%M'))
    return df