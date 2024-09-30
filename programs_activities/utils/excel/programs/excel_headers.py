# programs_activities/utils/excel/programs/excel_headers.py

def write_primary_headers(worksheet, header_secondary_programs):
    """
    Escribe los encabezados primarios en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.Worksheet): La hoja de Excel en la que se escribirán los encabezados.
    """

    # Escribir los encabezados
    worksheet.merge_range('A1:E1', 'Programas', header_secondary_programs)

def write_secondary_headers(worksheet, header_secondary_programs):
    """
    Escribe los encabezados secundarios en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.Worksheet): La hoja de Excel en la que se escribirán los encabezados.
    """
    primary_headers_programs = ["Responsable", "Nombre", "Inicio", "Fin", "Área"]

    # Escribir los encabezados
    worksheet.write_row(1, 0, primary_headers_programs, header_secondary_programs)

