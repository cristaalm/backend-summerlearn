# doantions/excel_utils/excel_formats.py

def get_formats(workbook):
    """
    Define and return various Excel formats for headers, cells, and footers.

    Args:
        workbook (xlsxwriter.Workbook): The workbook object to which formats will be added.

    Returns:
        dict: A dictionary containing the defined formats.
    """
    # Base format dictionaries
    base_header_primary = {
        'bold': True,
        'font_color': 'white',
        'font_size': 14,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    }

    base_header_secondary = {
        'bold': True,
        'font_color': 'black',
        'border': 1,
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True  # Habilita el ajuste de texto en encabezados secundarios
    }

    base_cell_text = {
        'font_color': 'black',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True  # Habilita el ajuste de texto
    }

    base_cell_money = {
        'num_format': '$#,##0.00',
        'font_color': 'black',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    }

    base_cell_date = {
        'num_format': 'dd/mm/yyyy',
        'font_color': 'black',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    }

    base_footer_primary = {
        'bold': True,
        'font_color': 'white',
        'font_size': 14,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    }

    # Define background colors
    colors = ['#d4ffe1', '#d5f6ff', '#feffdd', '#fcffff']

    # Create header primary formats with background colors
    header_primary_gasto = workbook.add_format({
        **base_header_primary,
        'bg_color': '#5cd57c'
    })
    header_primary_donacion = workbook.add_format({
        **base_header_primary,
        'bg_color': '#3fb5d1'
    })
    header_primary_excedente = workbook.add_format({
        **base_header_primary,
        'bg_color': '#fdffa9',
        'font_color': 'black',
        'bold': False,
        'text_wrap': True
    })

    # Create header secondary formats with background colors
    header_secondary_gasto = workbook.add_format({
        **base_header_secondary,
        'bg_color': '#8effad'
    })
    header_secondary_donacion = workbook.add_format({
        **base_header_secondary,
        'bg_color': '#86e6fe'
    })

    # Create cell formats with background colors
    formats = {
        'bill': {
            'even': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[0]}),
                'money': workbook.add_format({**base_cell_money, 'bg_color': colors[0]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[0]}),
            },
            'odd': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[3]}),
                'money': workbook.add_format({**base_cell_money, 'bg_color': colors[3]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[3]}),
            },
            'footer': {
                'text': workbook.add_format({**base_footer_primary, 'text_wrap': True, 'bg_color': '#5cd57c'}),
                'money': workbook.add_format({**base_footer_primary, 'num_format': '$#,##0.00', 'bg_color': '#5cd57c'}),
            }
        },
        'donation': {
            'even': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[1]}),
                'money': workbook.add_format({**base_cell_money, 'bg_color': colors[1]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[1]}),
            },
            'odd': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[3]}),
                'money': workbook.add_format({**base_cell_money, 'bg_color': colors[3]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[3]}),
            },
            'footer': {
                'text': workbook.add_format({**base_footer_primary, 'text_wrap': True, 'bg_color': '#3fb5d1'}),
                'money': workbook.add_format({**base_footer_primary, 'num_format': '$#,##0.00', 'bg_color': '#3fb5d1'}), 
            } 
        },
        'excess': {
            'even': workbook.add_format({**base_cell_money, 'bg_color': colors[2]}),
            'odd': workbook.add_format({**base_cell_money, 'bg_color': colors[3]}),
            'footer': workbook.add_format({**base_footer_primary, 'num_format': '$#,##0.00', 'bg_color': '#fdffa9', 'font_color': 'black'})
        }
    }

    return {
        'formats': formats,
        'header_primary_gasto': header_primary_gasto,
        'header_primary_donacion': header_primary_donacion,
        'header_primary_excedente': header_primary_excedente,
        'header_secondary_gasto': header_secondary_gasto,
        'header_secondary_donacion': header_secondary_donacion
    }
