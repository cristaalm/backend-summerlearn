# programs_activities/utils/excel/activities/export_activitys.py

import xlsxwriter
from io import BytesIO
from django.http import HttpResponse
from .excel_formats import get_formats
from .excel_headers import write_primary_headers, write_secondary_headers
from .excel_data import write_activities_data
from myApp.models import Activities

def export_activities_to_excel():
    """
    Exporta los datos de actividades a un archivo de Excel y retorna la respuesta HTTP.

    Returns:
    HttpResponse: La respuesta HTTP con el archivo de Excel.
    """
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Activities')

    # Obtener todos los formatos necesarios
    formats_data = get_formats(workbook)
    formats = formats_data['formats']
    header_primary_activity = formats_data['header_primary_activity']
    header_secondary_activity = formats_data['header_secundary_activity']

    # Escribir los encabezados
    write_primary_headers(worksheet, header_primary_activity)
    write_secondary_headers(worksheet, header_secondary_activity)

    # Obtener los datos
    activities = Activities.objects.all()

    # Escribir los datos
    for row_num, activity in enumerate(activities, start=2):
        write_activities_data(worksheet, row_num, activity, formats)


    # Ajustes finales
    worksheet.set_column('A:A', 25)  # Nombre de la actividad
    worksheet.set_column('B:B', 15)  # Fecha de la actividad
    worksheet.set_column('C:C', 25)  # Nombre del programa
    worksheet.set_column('D:D', 25)  # Nombre del area
    worksheet.set_column('E:E', 20)  # Numero de voluntarios
    worksheet.set_column('F:F', 20)  # Numero de beneficiarios


    workbook.close()

    # Reset the buffer's current position to the beginning
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=actividades.xlsx'
    return response
