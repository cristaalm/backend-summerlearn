# donations/utils/utils/excel/donations/export_bills.py

import xlsxwriter
from io import BytesIO
from django.http import HttpResponse
from .excel_formats import get_formats
from .excel_headers import write_primary_headers, write_secondary_headers
from .excel_data import write_donations_data
from myApp.models import Donations
import logging

logger = logging.getLogger(__name__)

def export_donations_to_excel():
    """
    Genera un archivo Excel con los datos de Donations y retorna una respuesta HTTP.
    """
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Donations') # Nombre de la hoja

    # Obtener todos los formatos necesarios
    formats_data = get_formats(workbook)
    formats = formats_data['formats']
    header_primary_donacion = formats_data['header_primary_donacion']
    header_primary_excedente = formats_data['header_primary_excedente']
    header_secondary_donacion = formats_data['header_secondary_donacion']

    # Escribir los encabezados
    write_primary_headers(worksheet, header_primary_donacion, header_primary_excedente)
    write_secondary_headers(worksheet, header_secondary_donacion)

    # Inicializar totales
    total_donations = 0
    total_excess = 0

    # Obtener los datos
    donations = Donations.objects.all().select_related('donations_user')

    # Escribir los datos
    for row_num, donation in enumerate(donations, start=2):
        donations_totals = write_donations_data(worksheet, row_num, donation, formats)
        total_donations += donations_totals[0]
        total_excess += donations_totals[1]

    # Escribir los totales
    total_rows = row_num + 1  # Asumiendo que al menos hay una fila de datos

    # Total de donaciones
    worksheet.merge_range(f'A{total_rows+1}:C{total_rows+1}', 'Total de donaciones', formats['donation']['footer']['text'])
    worksheet.write_number(total_rows, 3, total_donations, formats['donation']['footer']['money'])

    # Total de excedentes
    worksheet.write(total_rows, 4, total_excess, formats['excess']['footer'])

    # Ajustes finales
    worksheet.set_column('A:A', 35)  # Responsable de Gasto
    worksheet.set_column('B:B', 12)  # Fecha de Gasto
    worksheet.set_column('C:C', 30)  # Concepto de Gasto
    worksheet.set_column('D:D', 20)  # Cantidad de Gasto
    worksheet.set_column('E:E', 20)  # Excedente disponible


    workbook.close()

    # Reset the buffer's current position to the beginning
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=donations.xlsx'
    return response
