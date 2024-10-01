# programs_activities/utils/excel/programs/export_programs.py

import xlsxwriter
from io import BytesIO
from django.http import HttpResponse
from .excel_formats import get_formats
from .excel_headers import write_primary_headers, write_secondary_headers
from .excel_data import write_programs_data
from myApp.models import Programs

def export_programs_to_excel():
    """
    Exporta los datos de programas a un archivo de Excel y retorna la respuesta HTTP.
    """
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Programs')

    # Obtener todos los formatos necesarios
    formats_data = get_formats(workbook)
    formats = formats_data['formats']
    header_primary_program = formats_data['header_primary_program']
    header_secondary_program = formats_data['header_secundary_program']

    # Escribir los encabezados
    write_primary_headers(worksheet, header_primary_program)
    write_secondary_headers(worksheet, header_secondary_program)

    # Obtener los datos
    programs = Programs.objects.all()

    # Escribir los datos
    for row_num, program in enumerate(programs, start=2):
        write_programs_data(worksheet, row_num, program, formats)


    # Ajustes finales
    worksheet.set_column('A:A', 35)  # Responsable del programa
    worksheet.set_column('B:B', 30)  # Nombre del programa
    worksheet.set_column('C:C', 15)  # Fehca de inicio 
    worksheet.set_column('D:D', 15)  # Fecha de fin
    worksheet.set_column('E:E', 25)  # Nombre del área del programa


    workbook.close()

    # Reset the buffer's current position to the beginning
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=programas.xlsx'
    return response
