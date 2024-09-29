# donations/utils/utils/excel/export_bills.py

import xlsxwriter
from io import BytesIO
from django.http import HttpResponse
from .excel_formats import get_formats
from .excel_headers import write_primary_headers, write_secondary_headers
from .excel_data import write_bills_data
from myApp.models import Bills
import logging

logger = logging.getLogger(__name__)

def export_bills_to_excel():
    """
    Genera un archivo Excel con los datos de Bills y retorna una respuesta HTTP.
    """
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Bills')

    # Obtener todos los formatos necesarios
    formats_data = get_formats(workbook)
    formats = formats_data['formats']
    header_primary_gasto = formats_data['header_primary_gasto']
    header_primary_donacion = formats_data['header_primary_donacion']
    header_primary_excedente = formats_data['header_primary_excedente']
    header_secondary_gasto = formats_data['header_secondary_gasto']
    header_secondary_donacion = formats_data['header_secondary_donacion']

    # Escribir los encabezados
    write_primary_headers(worksheet, header_primary_gasto, header_primary_donacion, header_primary_excedente)
    write_secondary_headers(worksheet, header_secondary_gasto, header_secondary_donacion)

    # Inicializar totales
    total_bills = 0
    total_donations = 0
    total_excess = 0

    # Obtener los datos
    bills = Bills.objects.all().select_related(
        'bills_donations',
        'bills_user',
        'bills_donations__donations_user'
    )

    # Escribir los datos
    for row_num, bill in enumerate(bills, start=2):
        bills_totals = write_bills_data(worksheet, row_num, bill, formats)
        total_bills += bills_totals[0]
        total_donations += bills_totals[1]
        total_excess += bills_totals[2]

    # Escribir los totales
    total_rows = row_num + 1  # Asumiendo que al menos hay una fila de datos

    # Total de gastos
    worksheet.write(total_rows, 0, 'Total de gastos', formats['bill']['footer']['text'])
    worksheet.write_number(total_rows, 1, total_bills, formats['bill']['footer']['money'])
    worksheet.write(total_rows, 2, '', formats['bill']['footer']['text'])
    worksheet.write(total_rows, 3, '', formats['bill']['footer']['text'])

    # Total de donaciones
    worksheet.merge_range(f'E{total_rows+1}:F{total_rows+1}', 'Total de donaciones', formats['donation']['footer']['text'])
    worksheet.write_number(total_rows, 6, total_donations, formats['donation']['footer']['money'])

    # Total de excedentes
    worksheet.write(total_rows, 7, total_excess, formats['excess']['footer'])

    # Ajustes finales
    worksheet.set_column('A:A', 35)  # Responsable de Gasto
    worksheet.set_column('B:B', 22)  # Cantidad de Gasto
    worksheet.set_column('C:C', 30)  # Concepto de Gasto (ajustado para texto largo)
    worksheet.set_column('D:D', 15)  # Fecha de Gasto
    worksheet.set_column('E:E', 35)  # Responsable de Donación
    worksheet.set_column('F:F', 15)  # Fecha de Donación
    worksheet.set_column('G:G', 22)  # Cantidad de Donación
    worksheet.set_column('H:H', 22)  # Excedente disponible

    # Opcional: Establecer una altura mínima para las filas
    worksheet.set_default_row(20)  # Ajusta según tus necesidades

    workbook.close()

    # Reset the buffer's current position to the beginning
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=bills.xlsx'
    return response
