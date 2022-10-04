// Version 1.1
var config = {
    type: 'line',
    data: {
      labels: ["0 compradores", "1 comprador", "2 compradores", "3 compradores", "4 compradores"],
      datasets: [
        {
          label: "Periodos",
          backgroundColor: ["#0d6efd", "#0d6efd", "#0d6efd", "#0d6efd", "#0d6efd"],
          data: [0, 0, 0, 0, 0],
          pointRadius: 15,
          pointHoverRadius: 10,
          pointHitRadius: 15*5,
        }
      ]
    },
    options: {
      responsive: true,
      onHover: function(e) {
        const point = e.chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, false)
        if (point.length) e.native.target.style.cursor = 'grab'
        else e.native.target.style.cursor = 'default'
      },
      plugins: {
        dragData: {
          round: 1,
          showTooltip: true,
          onDragStart: function(e) {
            // console.log(e)
          },
          onDrag: function(e, datasetIndex, index, value) {              
            e.target.style.cursor = 'grabbing'
            // console.log(e, datasetIndex, index, value)
          },
          onDragEnd: function(e, datasetIndex, index, value) {
            e.target.style.cursor = 'default' 
            // console.log(datasetIndex, index, value)
          },
          magnet: {
            to: Math.round // to: (value) => value + 5
          }
        }
      },
      scales: {
        y: {
          max: 8,
          min: 0
        }
      }
    }
  }

const myChart = new Chart(
    document.getElementById('beliefs'),
    config
);

get_suma = () => {
    suma = 0;
    for (val of config["data"]["datasets"][0]["data"]){
        suma += val;
    }
    return suma;
}