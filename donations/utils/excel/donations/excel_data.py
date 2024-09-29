# donations/utils/utils/excel/bils/excel_data.py

import datetime

def write_donations_data(worksheet, row_num, donations, formats):
    """
    Escribe los datos de las donaciones en la hoja de Excel.
    Retorna los valores para los totales.
    """
    total_donations = 0
    total_excess = 0

    row_type = 'even' if row_num % 2 == 0 else 'odd'

    # Donación
    if donations:
        # Responsable
        donation_responsable = donations.donations_user.name if donations.donations_user else ''
        worksheet.write(row_num, 0, donation_responsable, formats['donation'][row_type]['text'])

        # Fecha
        if isinstance(donations.donations_date, (datetime.date, datetime.datetime)):
            donation_date = donations.donations_date
            if isinstance(donations.donations_date, datetime.date) and not isinstance(donations.donations_date, datetime.datetime):
                donation_date = datetime.datetime.combine(donations.donations_date, datetime.datetime.min.time())
            worksheet.write_datetime(row_num, 1, donation_date, formats['donation'][row_type]['date'])
        else:
            try:
                donation_date = datetime.datetime.strptime(str(donations.donations_date), '%Y-%m-%d').date()
                donation_date = datetime.datetime.combine(donation_date, datetime.datetime.min.time())
                worksheet.write_datetime(row_num, 1, donation_date, formats['donation'][row_type]['date'])
            except (ValueError, TypeError):
                worksheet.write(row_num, 1, donations.donations_date, formats['donation'][row_type]['text'])

        # Concepto
        if donations.donations_concept is not None:
            worksheet.write(row_num, 2, donations.donations_concept, formats['donation'][row_type]['text'])
        else:
            worksheet.write(row_num, 2, '', formats['donation'][row_type]['text'])

        # Cantidad
        if donations.donations_quantity is not None:
            worksheet.write_number(row_num, 3, donations.donations_quantity, formats['donation'][row_type]['money'])
            total_donations += donations.donations_quantity
        else:
            worksheet.write_number(row_num, 3, 0, formats['donation'][row_type]['money'])

        # Excedente disponible
        if donations.donations_spent is not None and donations.donations_quantity is not None:
            excess_value = donations.donations_quantity - donations.donations_spent
            total_excess += excess_value
        elif donations.donations_quantity is not None:
            excess_value = donations.donations_quantity
        else:
            excess_value = 0
        worksheet.write_number(row_num, 4, excess_value, formats['excess'][row_type])  # Excedente disponible
    else:
        # Handle cases where there are no donations linked
        worksheet.write(row_num, 0, '', formats['donation'][row_type]['text'])
        worksheet.write(row_num, 1, '', formats['donation'][row_type]['text'])
        worksheet.write_number(row_num, 3, 0, formats['donation'][row_type]['money'])
        worksheet.write_number(row_num, 4, 0, formats['excess'][row_type])  # Excedente disponible

    return total_donations, total_excess
