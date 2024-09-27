# myApp/excel_utils/excel_headers.py

def write_primary_headers(worksheet, header_primary_gasto, header_primary_donacion, header_primary_excedente):
    """
    Escribe los encabezados primarios en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.worksheet.Worksheet): La hoja de Excel donde se escribirán los encabezados.
    header_primary_gasto (dict): Formato para el encabezado de 'Gasto'.
    header_primary_donacion (dict): Formato para el encabezado de 'Donación'.
    header_primary_excedente (dict): Formato para el encabezado de 'Excedente disponible'.
    """
    worksheet.merge_range('A1:D1', 'Gasto', header_primary_gasto)
    worksheet.merge_range('E1:G1', 'Donación', header_primary_donacion)
    worksheet.merge_range('H1:H2', 'Excedente disponible', header_primary_excedente)

def write_secondary_headers(worksheet, header_secondary_gasto, header_secondary_donacion):
    """
    Escribe los encabezados secundarios en la hoja de Excel.

    Parameters:
    worksheet (xlsxwriter.worksheet.Worksheet): La hoja de Excel donde se escribirán los encabezados.
    header_secondary_gasto (dict): Formato para los encabezados secundarios de 'Gasto'.
    header_secondary_donacion (dict): Formato para los encabezados secundarios de 'Donación'.
    """
    second_headers_bills = ["Responsable", "Cantidad", "Concepto", "Fecha"]
    second_headers_donations = ["Responsable", "Fecha", "Cantidad"]

    worksheet.write_row(1, 0, second_headers_bills, header_secondary_gasto)
    worksheet.write_row(1, 4, second_headers_donations, header_secondary_donacion)
