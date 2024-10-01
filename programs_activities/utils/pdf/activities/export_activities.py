# donations/utils/pdf/donations/export_pdf.py

from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from myApp.models import Activities
import os
from django.conf import settings
from .imageAndTitle import ImageAndTitle
from django.http import HttpResponse
from .pdf_formats import create_table_style

def export_activities_to_pdf():
    # Crear un buffer para almacenar el PDF en memoria
    buffer = BytesIO()

    # Configurar el documento
    page_width, page_height = landscape(A4)
    # configurar formato vertical
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []

    # Cargar la imagen
    imagen_path = os.path.join(settings.MEDIA_ROOT, 'LogoPI.jpg')

    # Crear el título con el texto
    titulo = "Reporte de acvitidades"
    titulo_con_imagen = ImageAndTitle(image=imagen_path, text=titulo, width=50, height=50, page_width=page_width)
    
    # Añadir el título con la imagen a los elementos
    elementos.append(titulo_con_imagen)
    elementos.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    # Definir los datos de la tabla
    data = []
    data.append(['Actividades', '', '', '', '', ''])
    data.append(['Nombre', 'Fecha', 'Programa', 'Área', 'Voluntarios', 'Beneficiarios'])

    # Obtener las actividades
    activities = Activities.objects.all()

    for activity in activities:
        row = []
        
        # Agregar los datos de la actividad
        if activity:
            row.append(activity.activities_name if activity.activities_name else '') # Responsable
            row.append(activity.activities_date.strftime('%d/%m/%Y') if activity.activities_date else '') # Fecha
            row.append(activity.activities_program.programs_name if activity.activities_program.programs_name else '') # Programa
            row.append(activity.activities_program.programs_area.areas_name if activity.activities_program.programs_area.areas_name else '') # Área

            # TODO: Calcular el número de voluntarios
            row.append('0')
            # TODO: Calcular el número de beneficiarios
            row.append('0')

        else:
            row.extend([''] * 6)

        data.append(row)
    
    # Crear la tabla
    tabla = Table(data, repeatRows=2)
    estilo_tabla = create_table_style(data)
    tabla.setStyle(estilo_tabla)
    elementos.append(tabla)

    # Construir el documento
    doc.build(elementos)

    # Obtener el contenido del buffer
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    # creamos la respuesta HTTP para regresar el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="actividades.pdf"'
    response.write(pdf)
    return response