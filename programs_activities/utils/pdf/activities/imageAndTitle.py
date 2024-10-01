# donations/utils/pdf/donations/imageAndTitle.py

from reportlab.platypus import Flowable
from reportlab.lib import colors

class ImageAndTitle(Flowable):
    def __init__(self, image, text, width, height, page_width):
        Flowable.__init__(self)
        self.image = image
        self.text = text
        self.width = width
        self.height = height
        self.page_width = page_width

    def draw(self):
        # Calcular la posición para centrar la imagen y el texto
        total_width = self.width + self.canv.stringWidth(self.text, 'Helvetica-Bold', 16) + 10  # Espacio entre imagen y texto
        x_position = ((self.page_width - total_width) / 2) - 90  # Restar 10 para centrar

        # Dibujar un fondo blanco detrás de la imagen (rectángulo blanco)
        self.canv.setFillColor(colors.white)
        self.canv.rect(x_position, 0, self.width, self.height, fill=True, stroke=False)

        # Dibujar la imagen
        self.canv.drawImage(self.image, x_position, 0, width=self.width, height=self.height)

        # Dibujar el texto al lado derecho de la imagen en color negro
        self.canv.setFont("Helvetica-Bold", 16)
        self.canv.setFillColor(colors.black)  # Asegurar que el texto sea negro
        self.canv.drawString(x_position + self.width + 10, self.height / 2 - 5, self.text)
