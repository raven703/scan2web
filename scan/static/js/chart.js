$(function () {

    console.log('TEST from chart.js');
console.log("chartdata2 chart.js", chartData2);
    drawChart();

})

function drawChart()
{
    const ctx = document.getElementById('myChart').getContext('2d');
    console.log(ctx)
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartLabels2,
            datasets: [{
                data: chartData2,
            }],
            labels: ['a', 'b']
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}



