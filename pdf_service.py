from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from paths import temp_pdfs_path
import os

def generar_informe_pdf(rutas_imagenes, nombre_conductor):
    # Crear el documento PDF
    #nombre del conductor - fecha
    pdf_filename = f"informe_{nombre_conductor}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    pdf_path = os.path.join(temp_pdfs_path, pdf_filename)
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    story = []

    # Estilo del documento
    styles = getSampleStyleSheet()

    # Encabezado con logo a la derecha, título "TEMIRA" en el medio y fecha a la izquierda
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    header = [
        [
            Image('Logo.png', width=50, height=50, hAlign='RIGHT'),
            Paragraph("TEMIRA", styles["Heading1"]),
            Paragraph(f"Fecha: {fecha}", styles["Normal"])
        ]
    ]
    story.append(Table(header, colWidths=[2 * inch, 2 * inch, 2 * inch], rowHeights=0.5 * inch, hAlign='CENTER'))


    # Título principal debajo del encabezado 1 cm de espacio
    story.append(Spacer(1, 12))
    title = Paragraph(f"Análisis de Deteciones de Microsueños y Distracciones de {nombre_conductor}", styles["Title"])
    story.append(title)

    # Gráfico de torta
    # titulo del gráfico de torta centrado al medio
    imagen_grafico = Image(rutas_imagenes[0], width=550, height=500)
    story.append(imagen_grafico)

    # Diagrama de frecuencias por recorrido
    imagen_diagrama = Image(rutas_imagenes[1], width=550, height=500)
    story.append(imagen_diagrama)

    # Diagramas de frecuencias
    imagen_diagramas = Image(rutas_imagenes[2], width=550, height=500)
    story.append(imagen_diagramas)

    # Construir el documento PDF
    pdf.build(story)

    # Leer el archivo PDF generado y devolver los bytes
    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()

    return pdf_bytes