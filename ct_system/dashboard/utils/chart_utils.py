from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import inch
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import matplotlib
matplotlib.use('SVG')
plt.style.use('seaborn-v0_8-darkgrid')

def generate_chart(chart_configs:list):
    """
    Generate a list of charts based on the specified chart configurations.

    Parameters:
    - chart_configs (list): List of dictionaries, where each dictionary
      contains parameters specific to a chart type.

    Returns:
    - images (list): List of Image objects, each containing a chart image.
    """
    images = []

    for config in chart_configs:
        # Create a figure and axis for each chart configuration
        fig, ax = plt.subplots()  # Set facecolor to grey
        fig.patch.set_alpha(0)
        chart_type = config['type']
        kwargs = config.get('kwargs', {})

        # Determine the chart type and plot accordingly
        if chart_type == 'line':
            ax.plot(kwargs.get('x_axis', []), kwargs.get('y_axis', []), marker=kwargs.get('marker', 'o'), linestyle=kwargs.get('linestyle', '-'))
            plt.title(kwargs.get('title', ''), fontsize='xx-large', fontstyle="oblique", weight="bold")
        elif chart_type == 'pie':
            try:
                ax.pie(kwargs.get('data', []), labels=kwargs.get('labels', []), colors=kwargs.get('colors'), autopct='%1.1f%%', pctdistance=0.85)
                plt.title(kwargs.get('title', ''), fontsize='xx-large', fontstyle="oblique", weight="bold")
            except ValueError:
                plt.title('ERRO AO GERAR GRÁFICO: DADOS INSUFICIENTES', fontsize='xx-large', fontstyle="oblique", weight="bold")
        elif chart_type == 'bar':
            ax.bar(kwargs.get('labels', []), kwargs.get('data', []), color=kwargs.get('colors'))
            plt.title(kwargs.get('title', ''), fontsize='xx-large', fontstyle="oblique", weight="bold")
        elif chart_type == 'heatmap':
            sns.heatmap(kwargs.get('data', []), cbar=kwargs.get('cbar', True), cmap=kwargs.get('cmap', 'Oranges'), annot=kwargs.get('annot', False), ax=ax)
            plt.title(kwargs.get('title', ''), fontsize='xx-large', fontstyle="oblique", weight="bold")
        
        elif chart_type == 'radar':
            labels = kwargs.get('labels', [])
            data = kwargs.get('data', [])

            # Create a polar subplot explicitly
            ax = plt.subplot(111, polar=True)

            # Calculate angles for each component
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

            # The plot is circular, so we need to close the plot loop
            data = np.concatenate((data, [data[0]]))
            angles += angles[:1]

            # Plot the radar chart
            ax.fill(angles, data, color='b', alpha=0.25)
            ax.set_yticklabels([])

            # Convert angles to radians before setting the theta grids
            ax.set_thetagrids(np.array(angles[:-1]) * 180 / np.pi, labels)
            plt.title(kwargs.get('title', ''), fontsize='xx-large', fontstyle="oblique", weight="bold")
            
        elif chart_type == 'parallel':
            data = kwargs.get('data', [])
            fig = px.parallel_coordinates(data, color_continuous_scale=px.colors.diverging.Tealrose,
                                          color='budget_values', labels={"budget_values": "Orçamento", "authority_values": "Autoridade",
                                                                    "need_values": "Necessidade", "timing_values": "Timing",
                                                                    "time_to_respond_values": "Tempo de Resposta", "behavior_values": "Comportamento"},
                                          title=kwargs.get('title', ''),
                                          )
            # Convert plotly figure to matplotlib figure
            parallel_buffer = BytesIO()
            fig.write_image(parallel_buffer, format='png')
            parallel_buffer.seek(0)
            parallel_image = Image(parallel_buffer)
            parallel_image._restrictSize(5 * inch, 5 * inch)
            images.append(parallel_image)
            continue

        # Save the chart as an image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image = Image(buffer)

        # Specify the size of the image
        image._restrictSize(5 * inch, 5 * inch)

        # Clear/remove the plot to avoid interference
        plt.clf()
        plt.close()

        # Append the image to the list
        images.append(image)

    return images


