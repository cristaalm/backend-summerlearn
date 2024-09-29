# donations/utils/pdf/donations/export_pdf.py

from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from myApp.models import Donations
import os
from django.conf import settings
from .imageAndTitle import ImageAndTitle
from django.http import HttpResponse
from .pdf_formats import create_table_style

def export_donations_to_pdf():
    # Crear un buffer para almacenar el PDF en memoria
    buffer = BytesIO()

    # Configurar el documento
    page_width, page_height = landscape(A4)
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elementos = []

    # Cargar la imagen
    imagen_path = os.path.join(settings.MEDIA_ROOT, 'LogoPI.jpg')

    # Crear el título con el texto
    titulo = "Reporte de donaciones"
    titulo_con_imagen = ImageAndTitle(image=imagen_path, text=titulo, width=50, height=50, page_width=page_width)
    
    # Añadir el título con la imagen a los elementos
    elementos.append(titulo_con_imagen)
    elementos.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    # Definir los datos de la tabla
    data = []
    data.append(['Donación', '', '', '', 'Excedente disponible'])
    data.append(['Responsable', 'Fecha', 'Concepto', 'Cantidad', ''])

    # Obtener las donaciones 
    donations = Donations.objects.all()

    total_donations = 0
    total_excess = 0

    for donation in donations:
        row = []
        
        # Donación
        if donation:
            row.append(donation.donations_user.name if donation.donations_user else '')
            row.append(donation.donations_date.strftime('%d/%m/%Y') if donation.donations_date else '')
            row.append(donation.donations_concept if donation.donations_concept else '')
            row.append(f"${'{:,.2f}'.format(donation.donations_quantity) if donation.donations_quantity else '0.00'}")
            excess = (donation.donations_quantity - donation.donations_spent) if donation.donations_spent is not None else donation.donations_quantity
            row.append(f"${'{:,.2f}'.format(excess)}")

            # Actualizar totales
            total_donations += donation.donations_quantity
            total_excess += excess
        else:
            row.extend([''] * 4)

        data.append(row)

    # Filas de totales
    data.append([
        'Total de donaciones', 
        '', 
        '', 
        f"${'{:,.2f}'.format(total_donations)}", 
        f"${'{:,.2f}'.format(total_excess)}"
    ])
    

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
    response['Content-Disposition'] = 'attachment; filename="reporte_donaciones.pdf"'
    response.write(pdf)
    return response