# donations/utils/pdf/donations/pdf_formats.py

from reportlab.lib import colors 
from reportlab.platypus import TableStyle

def create_table_style(data):
    estilo_tabla = TableStyle([
        # Encabezado
        ('SPAN', (0,0), (5,0)), 
        ('BACKGROUND', (0,0), (5,0), colors.HexColor('#5cd57c')),
        ('TEXTCOLOR', (0,0), (5,0), colors.white),

        # Encabezado secundatio
        ('BACKGROUND', (0,1), (5,1), colors.HexColor('#8effad')),
        ('TEXTCOLOR', (0,1), (5,1), colors.black),
        
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
            activity_color = colors.HexColor('#d4ffe1')
        else:
            # Color para filas impares
            activity_color = colors.HexColor('#fcffff')

        # Aplicar color a cada sección de las filas
        estilo_tabla.add('BACKGROUND', (0, i), (5, i), activity_color)

    return estilo_tabla