import pandas as pd
import matplotlib.pyplot as plt
from paths import images_path
from matplotlib.dates import DateFormatter, HourLocator



def generar_grafico_torta(data):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    # Titulos de todos los gráficos
    fig.suptitle('Gráficos de Torta', fontweight='bold', fontsize=14)

    # Gráfico de torta 1
    labels = ['Tiempo prendido', 'Tiempo apagado']
    values = [data['Tiempo prendido'], data['Tiempo apagado']]
    colors = ['#FF6F00', '#1E88E5']
    axs[0, 0].pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    axs[0, 0].axis('equal')
    axs[0, 0].set_title('Distribución de tiempos en los que la app estaba prendida')

    # Gráfico de torta 2
    labels = ['Tiempo pausado', 'Tiempo en ejecucion']
    values = [data['Tiempo pausado'], data['Tiempo en ejecucion']]
    colors = ['#FF4081', '#42A5F5']
    axs[0, 1].pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    axs[0, 1].axis('equal')
    axs[0, 1].set_title('Distribución de tiempos en los que la app estaba pausada')

    # Gráfico de torta 3
    labels = ['Tiempo detectando', 'Tiempo sin detectar']
    values = [data['Tiempo detectando'], data['Tiempo sin detectar']]
    colors = ['#FF5252', '#448AFF']
    axs[1, 0].pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    axs[1, 0].axis('equal')
    axs[1, 0].set_title('Distribución de tiempos en los que la app estaba detectando')

    # Gráfico de torta 4
    labels = ['Tiempo microsueno', 'Tiempo distraccion']
    values = [data['Tiempo microsueno'], data['Tiempo distraccion']]
    colors = ['#FF5722', '#FFC107']
    axs[1, 1].pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    axs[1, 1].axis('equal')
    axs[1, 1].set_title('Distribución de tiempos en los que sonaba la alarma')

    # Ajustar el espacio entre los gráficos
    plt.tight_layout()
    return fig

def generar_diagrama_de_barras_de_frecuencias_agrupadas_por_recorrido(x, y):
    etiquetas = ['Microsueño', 'Distracción', 'Pausa']
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, next(y), width=0.2, label=etiquetas[0])
    ax.bar(x, next(y), width=0.2, label=etiquetas[1])
    ax.bar(x + 0.2, next(y), width=0.2, label=etiquetas[2])

    ax.set_xlabel('Recorrido')
    ax.set_ylabel('Cantidad de Registros')
    ax.set_title('Frecuencias por Recorrido', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.legend()
    return fig


# Función para generar el diagrama de frecuencias
def generar_diagrama_de_areas_de_frecuencias_por_hora(data):
    frecuencia_microsuenos = data['microsuenos']
    frecuencia_distracciones = data['distracciones']
    frecuencia_pausas = data['pausas']

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Generar el gráfico
    ax.fill_between(frecuencia_microsuenos.index, frecuencia_microsuenos, alpha=0.5, label='Microsueños')
    ax.fill_between(frecuencia_distracciones.index, frecuencia_distracciones, alpha=0.5, label='Distracciones')
    ax.fill_between(frecuencia_pausas.index, frecuencia_pausas, alpha=0.5, label='Pausas')

    # Configurar el eje x
    ax.xaxis.set_major_locator(HourLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter('%H'))
    ax.set_xlabel('Hora')
    ax.set_ylabel('Cantidad de Registros')
    ax.set_title('Frecuencias por Hora', fontweight='bold', fontsize=14)
    ax.legend()
    return fig

def guardar_en_cache(graficos):
    # Guardar los gráficos en la caché
    for i, grafico in enumerate(graficos):
        grafico.savefig(f"{images_path}_grafico{i}.png")
    # devuelve una lista de las rutas de los archivos
    return [f"{images_path}_grafico{i}.png" for i in range(len(graficos))]