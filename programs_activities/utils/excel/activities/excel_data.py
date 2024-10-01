# programs_activities/utils/excel/activities/excel_data.py

import datetime

def write_activities_data(worksheet, row_num, activity, formats):
    """
    Escribe los datos de una actividad en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.Worksheet): La hoja de Excel en la que se escribirán los datos.
    row_num (int): El número de la fila en la que se escribirán los datos.
    activity (Activities): La instancia de la actividad a escribir.
    formats (dict): Un diccionario con los formatos necesarios.

    Returns:
    None
    """
    row_type = 'even' if row_num % 2 == 0 else 'odd'

    # Nombre de la actividad
    activity_name = activity.activities_name if activity.activities_name else ''
    worksheet.write(row_num, 0, activity_name, formats['activity'][row_type]['text'])

    # Fecha de la actividad
    if isinstance(activity.activities_date, (datetime.date, datetime.datetime)):
        date_obj = activity.activities_date
        if isinstance(activity.activities_date, datetime.date) and not isinstance(activity.activities_date, datetime.datetime):
            date_obj = datetime.datetime.combine(activity.activities_date, datetime.datetime.min.time())
        worksheet.write_datetime(row_num, 1, date_obj, formats['activity'][row_type]['date'])
    else:
        try:
            date_obj = datetime.datetime.strptime(str(activity.activities_date), '%Y-%m-%d').date()
            date_obj = datetime.datetime.combine(date_obj, datetime.datetime.min.time())
            worksheet.write_datetime(row_num, 1, date_obj, formats['activity'][row_type]['date'])
        except (ValueError, TypeError):
            worksheet.write(row_num, 1, activity.activities_date, formats['activity'][row_type]['text'])

    # Programa de la actividad
    worksheet.write(row_num, 2, activity.activities_program.programs_name, formats['activity'][row_type]['text'])

    # Area de la actividad
    worksheet.write(row_num, 3, activity.activities_program.programs_area.areas_name, formats['activity'][row_type]['text'])

    # Voluntarios de la actividad
    # TODO: Calcular el número de voluntarios
    worksheet.write(row_num, 4, 0, formats['activity'][row_type]['text'])

    # Beneficiarios de la actividad
    # TODO: Calcular el número de beneficiarios
    worksheet.write(row_num, 5, 0, formats['activity'][row_type]['text'])