from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import datetime
import chart_utils

def gen_target_analysis(chart_params, date=datetime.datetime.now().date()):
    """ Resumo:

    Args:
        chart_params (dict): Dictionary containing parameters for the chart function.
        date (date, optional): Data de hoje (datetime.now). Defaults to datetime.datetime.now().date().

    Returns:
        buffer: Retorna o buffer com o PDF
    """

    #-Cria um buffer para retornar o PDF
    buffer = BytesIO()

    #-Cria o PDF
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    #-Define os estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    body_style = styles['BodyText']

    left_aligned_style = ParagraphStyle(
        'LeftAligned', parent=body_style, alignment=0, fontSize=11
    )
    subtitle_style = ParagraphStyle('Subtitle', parent=title_style, fontSize=12)

    title = f"Relatório - Análise de Público Alvo: {date}"

    #-Cria o gráfico
    chart = chart_utils.generate_chart(**chart_params)

    #-Adiciona o título, texto e outros componentes
    pdf_title = Paragraph(title, title_style)

    body_text = Paragraph(
        "Porcentagem do faturamento anual por cada setor: Tecnologia, Construção Civil e Consultoria:",
        left_aligned_style
    )

    subtitle = Paragraph("- CT Junior -", subtitle_style)

    #-Adiciona uma margem
    margin = Spacer(1, 12)

    #-Constrói o PDF
    pdf.build([pdf_title, subtitle, body_text, margin, chart])

    #-Retorna o buffer com o PDF
    return buffer



'''
def gen_target_analysis(data, labels, colors=None, date=datetime.datetime.now().date()):
    """ Resumo:

    Args:
        data (iterable): iterável com os dados para plotar
        labels (iterable): iterável com os rótulos dos dados
        colors (list, optional): lista com as cores para cada dado [#xxxxxx]. Defaults to None.
        date (date, optional): data de hoje (datetime.now). Defaults to datetime.datetime.now().date().

    Returns:
        buffer: retorna o buffer com o PDF
    """
    
    #-Cria um buffer para retornar o PDF
    buffer = BytesIO()

    #-Cria o PDF
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    #-Define os estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    body_style = styles['BodyText']
    
    
    left_aligned_style = ParagraphStyle(
        'LeftAligned', parent=body_style, alignment=0,fontSize=11
    )
    subtitle_style = ParagraphStyle('Subtitle', parent=title_style, fontSize=12)

    title = f"Relatório - Análise de Público Alvo: {date.date()}"

    #-Cria o gráfico
    chart = chart_utils.pie_chart(data=data, labels=labels, colors=colors)

    #-Adiciona o título, texto e outros componentes
    pdf_title = Paragraph(title, title_style)
    
    body_text = Paragraph(
        "Porcentagem do faturamento anual por cada setor: Tecnologia, Construção Civil e Consultoria:",
        left_aligned_style
    )

    subtitle = Paragraph("- CT Junior -", subtitle_style)
    
    #bullet_points = ListFlowable([
    #    ListItem(Paragraph(f"Percebemos que o maior faturamente pertence à diretoria de {max}.", left_aligned_style)),
    #], bulletType='bullet', start='circle')

    #-Adiciona uma margem
    margin = Spacer(1, 12)

    #-Constrói o PDF
    pdf.build([pdf_title, subtitle, body_text, margin, chart])

    #-Retorna o buffer com o PDF
    return buffer
'''