from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('SVG')

def generate_chart(chart_type, **kwargs):
    """
    Generate a chart based on the specified chart_type and parameters.

    Parameters:
    - chart_type (str): Type of chart ('line', 'pie', 'heatmap', etc.).
    - **kwargs: Additional parameters specific to the chosen chart type.

    Returns:
    - buffer: BytesIO buffer containing the chart image.
    """
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Determine the chart type and plot accordingly
    if chart_type == 'line':
        ax.plot(kwargs['x_axis'], kwargs['y_axis'], marker=kwargs.get('marker', 'o'), linestyle=kwargs.get('linestyle', '-'))
    elif chart_type == 'pie':
        ax.pie(kwargs['data'], labels=kwargs['labels'], colors=kwargs.get('colors'), autopct='%1.1f%%', pctdistance=0.85)
    elif chart_type == 'bar':
        ax.bar(kwargs['labels'], kwargs['data'], color=kwargs.get('colors'))
    elif chart_type == 'heatmap':
        sns.heatmap(kwargs['data'], cbar=kwargs.get('cbar', True), cmap=kwargs.get('cmap', 'Oranges'), annot=kwargs.get('annot', False), ax=ax)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = Image(buffer)

    #-Especifica o tamanho da imagem
    image._restrictSize(4 * inch, 4 * inch)

    #-Limpa/remove o plot para não interferir
    plt.clf()
    plt.close()

    return image
