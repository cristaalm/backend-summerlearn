# activitys_activities/utils/excel/activities/excel_formats.py

def get_formats(workbook):
    """
    Devuelve los formatos necesarios para el archivo de Excel.

    Parameters:
    workbook (xlsxwriter.Workbook): El libro de Excel en el que se escribirán los datos.

    Returns:
    dict: Un diccionario con los formatos necesarios.
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
    colors = ['#d4ffe1', '#fcffff']
    
    header_primary_activity = workbook.add_format({
        **base_header_primary,
        'bg_color': '#5cd57c'
    })

    header_secundary_activity = workbook.add_format({
        **base_header_secondary,
        'bg_color': '#8effad'
    })

    # Create cell formats with background colors
    formats = {
        'activity': {
            'even': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[0]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[0]}),
            },
            'odd': {
                'text': workbook.add_format({**base_cell_text, 'bg_color': colors[1]}),
                'date': workbook.add_format({**base_cell_date, 'bg_color': colors[1]}),
            },
            'footer': {
                'text': workbook.add_format({**base_footer_primary, 'text_wrap': True, 'bg_color': '#5cd57c'}),
            }
        }
    }

    return {
        'formats': formats,
        'header_primary_activity': header_primary_activity,
        'header_secundary_activity': header_secundary_activity
    }
