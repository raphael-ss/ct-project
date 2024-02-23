from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import inch
import numpy as np

def generate_metrics(configs:list):
    metrics = []

    for config in configs:
        kwargs = config.get('kwargs', {})

        metric = kwargs.get('text', '') + kwargs.get('value', '') + kwargs.get('unit', '')

        metrics.append(metric)

    return metrics


