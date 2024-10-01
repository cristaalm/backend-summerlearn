# programs_activities/utils/excel/activities/excel_headers.py

def write_primary_headers(worksheet, header_secondary_activities):
    """
    Escribe los encabezados primarios en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.Worksheet): La hoja de Excel en la que se escribirán los encabezados.
    header_secondary_activities (xlsxwriter.Format): El formato a aplicar a los encabezados secundarios.

    Returns:
    None
    """

    # Escribir los encabezados
    worksheet.merge_range('A1:F1', 'Actividades', header_secondary_activities)

def write_secondary_headers(worksheet, header_secondary_activities):
    """
    Escribe los encabezados secundarios en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.Worksheet): La hoja de Excel en la que se escribirán los encabezados.
    header_secondary_activities (xlsxwriter.Format): El formato a aplicar a los encabezados secundarios.

    Returns:
    None
    """
    #                                 A         B        C         D                 E                   F
    primary_headers_activities = ["Nombre", "Fecha", "Programa", "Área", "Voluntarios suscritos", "Beneficiarios suscritos"]

    # Escribir los encabezados
    worksheet.write_row(1, 0, primary_headers_activities, header_secondary_activities)

