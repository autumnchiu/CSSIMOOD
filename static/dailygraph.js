new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    // x-axis, will become timestamp
    labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
    datasets: [{
        //should be numeric value for emotion
        data: [-1,3,-15,2,7,26,82,172,312,433],
        // label: "North America",
        borderColor: "#4BC4AE",
        fill: false
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'A graph of your emotions'
    }
  }
});
