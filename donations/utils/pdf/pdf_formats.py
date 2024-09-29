# donations/utils/pdf/pdf_formats.py

from reportlab.lib import colors
from reportlab.platypus import TableStyle

def create_table_style(data, total_bills, total_donations, total_excess):
    estilo_tabla = TableStyle([
        ('SPAN', (0,0), (3,0)),
        ('SPAN', (4,0), (6,0)),
        ('SPAN', (7,0), (7,1)),
        ('BACKGROUND', (0,0), (3,0), colors.HexColor('#5cd57c')),
        ('TEXTCOLOR', (0,0), (3,0), colors.white),
        ('BACKGROUND', (4,0), (6,0), colors.HexColor('#3fb5d1')),
        ('TEXTCOLOR', (4,0), (6,0), colors.white),
        ('BACKGROUND', (7,0), (7,1), colors.HexColor('#fdffa9')),
        ('TEXTCOLOR', (7,0), (7,1), colors.black),
        ('BACKGROUND', (0,1), (3,1), colors.HexColor('#8effad')),
        ('BACKGROUND', (4,1), (6,1), colors.HexColor('#86e6fe')),
        ('TEXTCOLOR', (0,1), (6,1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])

    # Estilos para la fila de totales
    total_row = len(data) - 1
    estilo_tabla.add('BACKGROUND', (0, total_row), (3, total_row), colors.HexColor('#5cd57c'))
    estilo_tabla.add('BACKGROUND', (4, total_row), (6, total_row), colors.HexColor('#3fb5d1'))
    estilo_tabla.add('BACKGROUND', (7, total_row), (7, total_row), colors.HexColor('#fdffa9'))
    estilo_tabla.add('FONTNAME', (0, total_row), (-1, total_row), 'Helvetica-Bold')
    estilo_tabla.add('TEXTCOLOR', (0, total_row), (3, total_row), colors.white)
    estilo_tabla.add('TEXTCOLOR', (4, total_row), (6, total_row), colors.white)
    estilo_tabla.add('TEXTCOLOR', (7, total_row), (7, total_row), colors.black)

    return estilo_tabla