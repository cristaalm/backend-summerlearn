# donations/utils/pdf/donations/export_pdf.py

from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from myApp.models import Programs
import os
from django.conf import settings
from .imageAndTitle import ImageAndTitle
from django.http import HttpResponse
from .pdf_formats import create_table_style

def export_programs_to_pdf():
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
    titulo = "Reporte de programas"
    titulo_con_imagen = ImageAndTitle(image=imagen_path, text=titulo, width=50, height=50, page_width=page_width)
    
    # Añadir el título con la imagen a los elementos
    elementos.append(titulo_con_imagen)
    elementos.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    # Definir los datos de la tabla
    data = []
    data.append(['Programas', '', '', '', ''])
    data.append(['Responsable', 'Nombre', 'Inicio', 'Fin', 'Área'])

    # Obtener los programas
    programs = Programs.objects.all()

    for program in programs:
        row = []
        
        # Programa
        if program:
            row.append(program.programs_user.name if program.programs_user.name else '') # Responsable
            row.append(program.programs_name if program.programs_name else '') # Nombre
            row.append(program.programs_start.strftime('%d/%m/%Y') if program.programs_start else '') # Inicio
            row.append(program.programs_end.strftime('%d/%m/%Y') if program.programs_end else '') # Fin
            row.append(program.programs_area.areas_name if program.programs_area.areas_name else '')

        else:
            row.extend([''] * 5)

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
    response['Content-Disposition'] = 'attachment; filename="programas.pdf"'
    response.write(pdf)
    return response