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
from . import chart_utils, metric_utils
from reportlab.platypus import ListItem

#-testing:
font_path = 'dashboard/utils/font/Lato-Regular.ttf'
#-official:
#font_path = 'ct_system/dashboard/utils/font/Lato-Regular.ttf'
pdfmetrics.registerFont(TTFont('Lato', font_path))

def gen_target_analysis(chart_configs, date=datetime.datetime.now().date()):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    def on_each_page(canvas, doc):
        canvas.setFont('Lato', 16)

        canvas.rect(10, 10, letter[0] - 20, letter[1] - 20)
        #-testing:
        logo_path = 'ct_system/static/img/logo_verde.png'
        #-official:
        #logo_path = 'ct_system/ct_system/static/img/logo_verde.png'
        logo_width = 2.5 * inch
        logo_height = 2.5 * inch
        center_x = (letter[0] - logo_width) / 2
        center_y = (letter[1] - logo_height) / 2
        canvas.setFillAlpha(0.3)
        canvas.drawImage(logo_path, center_x, center_y, width=logo_width, height=logo_height, mask='auto')
        canvas.setFillAlpha(1)

        title_text = f"Relatório - Análise de Público Alvo: {date}"
        canvas.drawCentredString(letter[0] / 2, letter[1] - 50, title_text)

    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=getSampleStyleSheet()['BodyText'],
        fontName='Lato',
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

def gen_funnel_analysis(chart_configs, metric_configs, date=datetime.datetime.now().date()):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    def on_each_page(canvas, doc):
        canvas.setFont('Lato', 16)

        canvas.rect(10, 10, letter[0] - 20, letter[1] - 20)
        #-testing:
        logo_path = 'ct_system/static/img/logo_verde.png'
        #-official:
        #logo_path = 'ct_system/ct_system/static/img/logo_verde.png'
        logo_width = 2.5 * inch
        logo_height = 2.5 * inch
        center_x = (letter[0] - logo_width) / 2
        center_y = (letter[1] - logo_height) / 2
        canvas.setFillAlpha(0.3)
        canvas.drawImage(logo_path, center_x, center_y, width=logo_width, height=logo_height, mask='auto')
        canvas.setFillAlpha(1)

        title_text = f"Relatório - Análise de Funil de Vendas: {date}"
        canvas.drawCentredString(letter[0] / 2, letter[1] - 50, title_text)


    # Assuming metric_utils.generate_metrics() returns a list of strings
    metric_strings = metric_utils.generate_metrics(configs=metric_configs)

    # Create a list of Paragraph objects with bullet points
    paragraphs = list()
    
    for metric_str in metric_strings:
        if metric_str[-1] == ';':
            paragraphs.append([Paragraph(f'&bull; {metric_str}', getSampleStyleSheet()['BodyText'])])
        elif metric_str[-1] == ':':
            paragraphs.append([Spacer(1,6),Paragraph(f'{metric_str}', getSampleStyleSheet()['Heading3']),Spacer(1, 6)])
        else:
            paragraphs.append([Spacer(1,3),Paragraph(f'{metric_str}', getSampleStyleSheet()['Normal']),Spacer(1, 3)])
        

    # Add content to the document
    content = [ 
        Paragraph("Métricas Gerais e Relativas:", getSampleStyleSheet()['Heading2']),
        *[phrase for sublist in paragraphs for phrase in sublist],
        Spacer(1, 12),
        Paragraph("Visualizações das Distribuições, Frequências e Relações dos Dados:", getSampleStyleSheet()['Heading2']),
        Spacer(1, 12),
        *chart_utils.generate_chart(chart_configs=chart_configs)
    ]
    
    pdf.build(
        content,
        onFirstPage=on_each_page,
        onLaterPages=on_each_page
    )

    return buffer