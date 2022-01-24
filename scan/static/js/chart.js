$(function() {
    console.log("ready func")

    let attrdata  = $("#chartData").attr('data-chart');

    let data2 = '{' + JSON.parse(attrdata) + '}'
 let dataset = JSON.parse(data2)

    let chartData = dataset["c_data"];
	let chartLabels = dataset["labels"];
     console.log("chart data is:", chartData);
     console.log("chart lables is:", chartLabels);
     drawChart(chartData, chartLabels);
})



function drawChart(chartData, chartLabels)
{
    const ctx = document.getElementById('myChart').getContext('2d');

    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartLabels,
            datasets: [{
                data: chartData,
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            }],
            labels: chartLabels
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



