# donations/utils/utils/excel/excel_data.py

import datetime

def write_bills_data(worksheet, row_num, bill, formats):
    """
    Escribe una fila de datos de 'Gasto' en la hoja de Excel.
    Retorna los valores para los totales.
    """
    total_bills = 0
    total_donations = 0
    total_excess = 0

    row_type = 'even' if row_num % 2 == 0 else 'odd'

    # Responsable
    responsable = bill.bills_user.name if bill.bills_user else ''
    worksheet.write(row_num, 0, responsable, formats['bill'][row_type]['text'])

    # Cantidad
    if bill.bills_amount is not None:
        worksheet.write_number(row_num, 1, bill.bills_amount, formats['bill'][row_type]['money'])
        total_bills += bill.bills_amount
    else:
        worksheet.write_number(row_num, 1, 0, formats['bill'][row_type]['money'])

    # Concepto
    concepto = bill.bills_concept if bill.bills_concept else ''
    worksheet.write(row_num, 2, concepto, formats['bill'][row_type]['text'])

    # Fecha
    if isinstance(bill.bills_date, (datetime.date, datetime.datetime)):
        date_obj = bill.bills_date
        if isinstance(bill.bills_date, datetime.date) and not isinstance(bill.bills_date, datetime.datetime):
            date_obj = datetime.datetime.combine(bill.bills_date, datetime.datetime.min.time())
        worksheet.write_datetime(row_num, 3, date_obj, formats['bill'][row_type]['date'])
    else:
        try:
            date_obj = datetime.datetime.strptime(str(bill.bills_date), '%Y-%m-%d').date()
            date_obj = datetime.datetime.combine(date_obj, datetime.datetime.min.time())
            worksheet.write_datetime(row_num, 3, date_obj, formats['bill'][row_type]['date'])
        except (ValueError, TypeError):
            worksheet.write(row_num, 3, bill.bills_date, formats['bill'][row_type]['text'])

    # Donación
    donations = bill.bills_donations
    if donations:
        # Responsable
        donation_responsable = donations.donations_user.name if donations.donations_user else ''
        worksheet.write(row_num, 4, donation_responsable, formats['donation'][row_type]['text'])

        # Fecha
        if isinstance(donations.donations_date, (datetime.date, datetime.datetime)):
            donation_date = donations.donations_date
            if isinstance(donations.donations_date, datetime.date) and not isinstance(donations.donations_date, datetime.datetime):
                donation_date = datetime.datetime.combine(donations.donations_date, datetime.datetime.min.time())
            worksheet.write_datetime(row_num, 5, donation_date, formats['donation'][row_type]['date'])
        else:
            try:
                donation_date = datetime.datetime.strptime(str(donations.donations_date), '%Y-%m-%d').date()
                donation_date = datetime.datetime.combine(donation_date, datetime.datetime.min.time())
                worksheet.write_datetime(row_num, 5, donation_date, formats['donation'][row_type]['date'])
            except (ValueError, TypeError):
                worksheet.write(row_num, 5, donations.donations_date, formats['donation'][row_type]['text'])

        # Cantidad
        if donations.donations_quantity is not None:
            worksheet.write_number(row_num, 6, donations.donations_quantity, formats['donation'][row_type]['money'])
            total_donations += donations.donations_quantity
        else:
            worksheet.write_number(row_num, 6, 0, formats['donation'][row_type]['money'])

        # Excedente disponible
        if donations.donations_spent is not None and donations.donations_quantity is not None:
            excess_value = donations.donations_quantity - donations.donations_spent
            total_excess += excess_value
        elif donations.donations_quantity is not None:
            excess_value = donations.donations_quantity
        else:
            excess_value = 0
        worksheet.write_number(row_num, 7, excess_value, formats['excess'][row_type])  # Excedente disponible
    else:
        # Handle cases where there are no donations linked
        worksheet.write(row_num, 4, '', formats['donation'][row_type]['text'])
        worksheet.write(row_num, 5, '', formats['donation'][row_type]['text'])
        worksheet.write_number(row_num, 6, 0, formats['donation'][row_type]['money'])
        worksheet.write_number(row_num, 7, 0, formats['excess'][row_type])  # Excedente disponible

    return total_bills, total_donations, total_excess
