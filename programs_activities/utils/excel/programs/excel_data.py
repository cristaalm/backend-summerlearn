# programs_activities/utils/excel/programs/excel_data.py

import datetime

def write_programs_data(worksheet, row_num, program, formats):
    """
    Escribe los datos de un programa en la hoja de Excel.
    """
    row_type = 'even' if row_num % 2 == 0 else 'odd'

    # Responsable del programa
    responsable = program.programs_user.name if program.programs_user else ''
    worksheet.write(row_num, 0, responsable, formats['program'][row_type]['text'])

    # Nombre del programa
    worksheet.write(row_num, 1, program.programs_name, formats['program'][row_type]['text'])

    # Fecha de inicio
    if isinstance(program.programs_start, (datetime.date, datetime.datetime)):
        date_obj = program.programs_start
        if isinstance(program.programs_start, datetime.date) and not isinstance(program.programs_start, datetime.datetime):
            date_obj = datetime.datetime.combine(program.programs_start, datetime.datetime.min.time())
        worksheet.write_datetime(row_num, 2, date_obj, formats['program'][row_type]['date'])
    else:
        try:
            date_obj = datetime.datetime.strptime(str(program.programs_start), '%Y-%m-%d').date()
            date_obj = datetime.datetime.combine(date_obj, datetime.datetime.min.time())
            worksheet.write_datetime(row_num, 2, date_obj, formats['program'][row_type]['date'])
        except (ValueError, TypeError):
            worksheet.write(row_num, 2, program.programs_start, formats['program'][row_type]['text'])

    # Fecha de fin
    if isinstance(program.programs_end, (datetime.date, datetime.datetime)):
        date_obj = program.programs_end
        if isinstance(program.programs_end, datetime.date) and not isinstance(program.programs_end, datetime.datetime):
            date_obj = datetime.datetime.combine(program.programs_end, datetime.datetime.min.time())
        worksheet.write_datetime(row_num, 3, date_obj, formats['program'][row_type]['date'])
    else:
        try:
            date_obj = datetime.datetime.strptime(str(program.programs_end), '%Y-%m-%d').date()
            date_obj = datetime.datetime.combine(date_obj, datetime.datetime.min.time())
            worksheet.write_datetime(row_num, 3, date_obj, formats['program'][row_type]['date'])
        except (ValueError, TypeError):
            worksheet.write(row_num, 3, program.programs_end, formats['program'][row_type]['text'])

    # Area del programa

    worksheet.write(row_num, 4, program.programs_area.areas_name, formats['program'][row_type]['text'])