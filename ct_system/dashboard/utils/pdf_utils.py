from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import datetime
from reportlab.lib.units import inch
from reportlab.lib import utils
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from . import chart_utils

#xfont_path = './font/Lato-Regular.ttf'
#pdfmetrics.registerFont(TTFont('Lato', font_path))

def gen_target_analysis(chart_configs, date=datetime.datetime.now().date()):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    def on_each_page(canvas, doc):
        # Set the font
        #canvas.setFont('Lato', 16)

        # Add borders to the page
        canvas.rect(10, 10, letter[0] - 20, letter[1] - 20)

        # Add image as watermark
        logo_path = os.path.abspath('ct_system/static/img/logo_verde.png')
        logo_width = 2.5 * inch
        logo_height = 2.5 * inch
        center_x = (letter[0] - logo_width) / 2
        center_y = (letter[1] - logo_height) / 2
        canvas.setFillAlpha(0.3)
        canvas.drawImage(logo_path, center_x, center_y, width=logo_width, height=logo_height, mask='auto')
        canvas.setFillAlpha(1)

        # Add header
        title_text = f"Relatório - Análise de Público Alvo: {date}"
        canvas.drawCentredString(letter[0] / 2, letter[1] - 50, title_text)

    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=getSampleStyleSheet()['BodyText'],
        #fontName='Lato',
        fontSize=13,
    )
    pdf.build(
        [
            Paragraph("Visualizações das Distribuições, Frequências e Relações dos Dados:",
                      custom_style),
            Spacer(1, 12),
            *chart_utils.generate_chart(chart_configs=chart_configs)
        ],
        onFirstPage=on_each_page,
        onLaterPages=on_each_page
    )

    return buffer