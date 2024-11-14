from csv_service import agregar_horas, agregar_recorrido, cargar_datos
from data_analysis_service import obtener_datos_para_barras_de_frecuencias_agrupadas_por_recorrido, obtener_datos_para_diagrama_de_areas_de_frecuencias_por_hora, obtener_datos_para_grafico_torta
from data_visualization_service import generar_diagrama_de_areas_de_frecuencias_por_hora, generar_diagrama_de_barras_de_frecuencias_agrupadas_por_recorrido, generar_grafico_torta, guardar_en_cache
from paths import images_path
import streamlit as st
from encryption_service import get_temp_path_encrypted_file, get_temp_path_file, leer_clave, desencriptar_archivo
from pdf_service import generar_informe_pdf
from streamlit_service import add_bg_from_local

def main():
    logo = 'Logo.png'
    fondo = 'Fondo2.png'
    clave_privada = leer_clave('privada')
    st.set_page_config(page_title='Temira', page_icon=logo)
    st.title("TEMIRA")
    st.image(logo, width=300)
    add_bg_from_local(fondo)
    st.markdown('# Análisis de Deteciones de Microsueños y Distracciones')
    st.markdown('### Esta aplicación permite analizar los datos de las detecciones de microsueños y distracciones realizadas por la aplicación Temira. Para ello, se debe cargar un archivo CSV con los datos de las detecciones.')
    # Boton de ayuda que despliega un texto con instrucciones para cargar el csv
    if st.button('Ayuda'):
        st.markdown('Para cargar el archivo, se debe hacer click en el botón "Cargar archivo CSV" y seleccionar el archivo correspondiente. El archivo debe tener el siguiente formato:')

    archivo_encriptado = st.file_uploader('Cargar archivo encriptado', type=['csv'])

    if archivo_encriptado is not None:
        ruta_temporal_archivo_encritado = get_temp_path_encrypted_file(archivo_encriptado)
        contenido_desencriptado = desencriptar_archivo(clave_privada, ruta_temporal_archivo_encritado)
        ruta_temporal_archivo_desencritado = get_temp_path_file(contenido_desencriptado)
        datos = cargar_datos(ruta_temporal_archivo_desencritado)

        # Mostrar la tabla de datos
        st.subheader("Datos del archivo CSV")
        st.dataframe(datos)

        # Mostrar el gráfico de torta
        st.subheader("Gráfico de Torta")
        st.markdown('Este gráfico muestra la distribución de tiempos en los que la app estaba prendida y en los que sonaba la alarma')
        datos_para_grafico_torta = obtener_datos_para_grafico_torta(datos)
        fig1 = generar_grafico_torta(datos_para_grafico_torta)
        st.pyplot(fig1)

        # Mostrar el diagrama de frecuencias por recorrido
        st.subheader("Diagrama de Frecuencias por Recorrido")
        st.markdown('Este diagrama muestra la cantidad de pausas, microsueños y distracciones por recorrido')
        datos = agregar_recorrido(datos)
        st.subheader("Dataframe con recorridos")
        st.dataframe(datos)
        x,y = obtener_datos_para_barras_de_frecuencias_agrupadas_por_recorrido(datos)
        fig2 = generar_diagrama_de_barras_de_frecuencias_agrupadas_por_recorrido(x,y)
        st.pyplot(fig2)

        # Mostrar el diagramas de frecuencias
        st.subheader("Diagramas de Frecuencias Horarias")
        st.markdown('Este diagrama muestra la cantidad de detecciones de microsueños y distracciones por hora')
        datos1 = agregar_horas(datos)
        st.subheader("Dataframe con horas")
        st.dataframe(datos1)

        datos_para_diagrama_de_frecuencias = obtener_datos_para_diagrama_de_areas_de_frecuencias_por_hora(datos)
        fig3 = generar_diagrama_de_areas_de_frecuencias_por_hora(datos_para_diagrama_de_frecuencias)

        st.pyplot(fig3)

        # Botón para generar el informe PDF
        st.title("Generar Informe PDF")
        # codigo para que mientras no ingrese el nombre del conductor no se mostrara el boton de descarga
        with st.form("NombreConductorForm"):
            nombre_conductor = ""
            nombre_conductor = st.text_input("Ingrese el nombre del conductor")
            submit_button = st.form_submit_button("OK")
    
        if submit_button and nombre_conductor:
            # Generar el informe PDF
            graficos = [fig1, fig2, fig3]
            nombre_informe = "informe de " + nombre_conductor
            archivos_cachados = guardar_en_cache(graficos)
            informe_pdf = generar_informe_pdf(archivos_cachados, nombre_conductor)
            # Descargar el archivo PDF utilizando el botón de descarga de Streamlit
            st.download_button(
                label="Descargar Informe PDF",
                data=informe_pdf,
                file_name=f"{nombre_informe}.pdf",
                mime="application/pdf"
            )


# Ejecutar la app
if __name__ == '__main__':
    main()
