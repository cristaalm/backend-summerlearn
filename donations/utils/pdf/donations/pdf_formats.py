# donations/utils/pdf/donations/pdf_formats.py

from reportlab.lib import colors 
from reportlab.platypus import TableStyle

def create_table_style(data):
    estilo_tabla = TableStyle([
        ('SPAN', (0,0), (3,0)),
        ('SPAN', (4,0), (4,1)),
        ('BACKGROUND', (0,0), (3,0), colors.HexColor('#3fb5d1')),
        ('TEXTCOLOR', (0,0), (3,0), colors.white),
        ('BACKGROUND', (4,0), (4,1), colors.HexColor('#fdffa9')),
        ('TEXTCOLOR', (4,0), (4,1), colors.black),
        ('BACKGROUND', (0,1), (3,1), colors.HexColor('#86e6fe')),
        ('TEXTCOLOR', (0,1), (3,1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    # Estilos para alternar colores en las filas de datos
    for i in range(2, len(data) - 1):  # Excluyendo las filas de encabezado y de totales
        if i % 2 == 0:
            # Color para filas pares
            donacion_color = colors.HexColor('#e0f7fa')
            excedente_color = colors.HexColor('#fff9c4')
        else:
            # Color para filas impares
            donacion_color = colors.HexColor('#fcffff')
            excedente_color = colors.HexColor('#fcffff')

        # Aplicar color a cada sección de las filas
        estilo_tabla.add('BACKGROUND', (0, i), (3, i), donacion_color)
        estilo_tabla.add('BACKGROUND', (4, i), (4, i), excedente_color)

    # Estilos para la fila de totales
    total_row = len(data) - 1
    estilo_tabla.add('BACKGROUND', (0, total_row), (3, total_row), colors.HexColor('#3fb5d1'))
    estilo_tabla.add('BACKGROUND', (4, total_row), (4, total_row), colors.HexColor('#fdffa9'))
    estilo_tabla.add('FONTNAME', (0, total_row), (-1, total_row), 'Helvetica-Bold')
    estilo_tabla.add('TEXTCOLOR', (0, total_row), (3, total_row), colors.white)
    estilo_tabla.add('TEXTCOLOR', (4, total_row), (4, total_row), colors.black)
    
    # Fusionar las celdas 4 y 5 de donaciones
    estilo_tabla.add('SPAN', (0, total_row), (2, total_row))

    return estilo_tabla