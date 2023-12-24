Chart.register({
    id: 'pt-BR',
    options: {
        date: {
            months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            weekdays: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']
        }
    }
});
// Fetch data from Django backend (you can use Django template tags to embed the data)
var labels = [{% for contract in contracts %}"{{ contract.date|date:'Y-m-d' }}",{% endfor %}];
var data = [{% for contract in contracts %}{{ contract.total_value }},{% endfor %}];

console.log(labels)
console.log(data)

// Use Chart.js to create a line chart
var ctx = document.getElementById('lineChart').getContext('2d');
var lineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Total Contract Values',
            data: data,
            fill: true,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    tooltipFormat: 'YYYY-MM-DD',
                }
            },
            y: {
                beginAtZero: true
            }
        }
    },
    plugins: {
        legend: {
            display: true,
            position: 'top'
        }
    },
    locale: 'pt-BR' // Set the locale to Portuguese
       
});