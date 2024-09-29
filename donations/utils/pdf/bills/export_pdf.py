# donations/utils/pdf/bills/export_pdf.py

from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from myApp.models import Bills, Donations
import os
from django.conf import settings
from .imageAndTitle import ImageAndTitle
from django.http import HttpResponse
from .pdf_formats import create_table_style

def export_bills_to_pdf():
    # Crear un buffer para almacenar el PDF en memoria
    buffer = BytesIO()

    # Configurar el documento
    page_width, page_height = landscape(A4)
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elementos = []

    # Cargar la imagen
    imagen_path = os.path.join(settings.MEDIA_ROOT, 'LogoPI.jpg')

    # Crear el título con el texto
    titulo = "Reporte de gastos"
    titulo_con_imagen = ImageAndTitle(image=imagen_path, text=titulo, width=50, height=50, page_width=page_width)
    
    # Añadir el título con la imagen a los elementos
    elementos.append(titulo_con_imagen)
    elementos.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    # Definir los datos de la tabla
    data = []
    data.append(['Gasto', 'Gasto', 'Gasto', 'Gasto', 'Donación', 'Donación', 'Donación', 'Excedente disponible'])
    data.append(["Responsable", "Cantidad", "Concepto", "Fecha", "Responsable", "Fecha", "Cantidad", ""])

    # Obtener los datos
    bills = Bills.objects.all().select_related(
        'bills_donations',
        'bills_user',
        'bills_donations__donations_user'
    )

    total_bills = 0
    total_donations = 0
    total_excess = 0

    for bill in bills:
        row = []
        # Gasto
        row.append(bill.bills_user.name if bill.bills_user else '')
        row.append(f"${'{:,.2f}'.format(bill.bills_amount) if bill.bills_amount else '0.00'}")
        row.append(bill.bills_concept if bill.bills_concept else '')
        row.append(bill.bills_date.strftime('%d/%m/%Y') if bill.bills_date else '')

        # Donación
        donations = bill.bills_donations
        if donations:
            row.append(donations.donations_user.name if donations.donations_user else '')
            row.append(donations.donations_date.strftime('%d/%m/%Y') if donations.donations_date else '')
            row.append(f"${'{:,.2f}'.format(donations.donations_quantity) if donations.donations_quantity else '0.00'}")
            excess = (donations.donations_quantity - donations.donations_spent) if donations.donations_spent is not None else donations.donations_quantity
            row.append(f"${'{:,.2f}'.format(excess)}")

            # Actualizar totales
            total_bills += bill.bills_amount if bill.bills_amount else 0
        else:
            row.extend(['', '', '$0.00', '$0.00'])
            total_bills += bill.bills_amount if bill.bills_amount else 0

        data.append(row)

    # Calculamos por aparte el total de donaciones y el excedente
    donations = Donations.objects.all()
    for donation in donations:
        total_donations += donation.donations_quantity
        total_excess += (donation.donations_quantity - donation.donations_spent) if donation.donations_spent is not None else donation.donations_quantity

    # Filas de totales
    data.append([
        'Total de gastos', 
        f"${'{:,.2f}'.format(total_bills)}", 
        '', 
        '', 
        'Total de donaciones', 
        'Total de donaciones',
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
    response['Content-Disposition'] = 'attachment; filename="reporte_gastos.pdf"'
    response.write(pdf)
    return response