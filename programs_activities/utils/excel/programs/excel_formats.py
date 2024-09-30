# programs_activities/utils/excel/programs/excel_formats.py

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
        'align': 'center',
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
    colors = ['#d5f6ff', '#fcffff']
    
    header_primary_program = workbook.add_format({
        **base_header_primary,
        'bg_color': '#3fb5d1'
    })

    header_secundary_program = workbook.add_format({
        **base_header_secondary,
        'bg_color': '#86e6fe'
    })

    # Create cell formats with background colors
    formats = {
        'program': {
            'even': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[0]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[0]}),
            },
            'odd': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[1]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[1]}),
            },
            'footer': {
                'text': workbook.add_format({**base_footer_primary, 'text_wrap': True, 'bg_color': '#3fb5d1'}),
            }
        }
    }

    return {
        'formats': formats,
        'header_primary_program': header_primary_program,
        'header_secundary_program': header_secundary_program
    }
