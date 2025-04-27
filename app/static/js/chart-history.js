// apexcharts https://apexcharts.com/docs/creating-first-javascript-chart/

const params = [
  ['#chartT', 'temperature', 'температура', ['#1d531c', '#3ba639']],
  ['#chartH', 'humidity', 'влажность', ['#1b4a79', '#3392f1']],
  ['#chartP', 'pressure', 'давление', ['#6e3889', '#cc66ff']],
]

async function getHistoryData() {
  const response = await fetch('/json_history')
  const res = await response.json()
  return res
}

function getChartDataFromDbData(arr, parameter) {
  const categoriesValues = []
  const minValues = []
  const maxValues = []
  
  arr.map((item) => {
    const date = new Date(item.date).toLocaleDateString('ru')
    categoriesValues.push(date)
    minValues.push(item[`min_${parameter}`])
    const edge = parameter !== 'pressure' ? 100 : 800
    const maxV = item[`max_${parameter}`] >= edge ? item[`min_${parameter}`] : item[`max_${parameter}`]
    maxValues.push(maxV)
  })
  return {categoriesValues, minValues, maxValues}
}

function getOptionsForChart(dbData, parameter, title, colors) {
  const {categoriesValues, minValues, maxValues } = getChartDataFromDbData(dbData, parameter)
  const titleText = title.toUpperCase()
  const names = [`мин ${title}`, `макс ${title}`]

  return {
    title: {
      text: titleText,
      align: 'center',
      style: {
        fontSize: '20px',
        fontFamily: 'system-ui, sans-serif',  
        color: colors[1],
      }
    },
    chart: {
      type: 'line',
      height: 350,
      toolbar: {
        tools: {
          download: false,
          selection: false,
          zoom: false,
          zoomin: false,
          zoomout: false,
          pan: false,
          reset: false,
        },
      },
      zoom: {
        enabled: false,
      },
    },
    series: [
      {
        name: names[0],
        data: minValues,
        color: colors[0],
      },
      {
        name: names[1],
        data: maxValues,
        color: colors[1],
      },
    ],
    stroke: {
      dashArray: [0, 4],
    },
    xaxis: {
      categories: categoriesValues,
    },
    legend: {
      labels: {
        colors: ['#b2b0b0', '#b2b0b0']
      },
      markers: {
        strokeWidth: 0,
        offsetX: '-2px',
      }
    },
  }
}

function renderChart(dbData, selector, parameter, title, colors) {
  const options = getOptionsForChart(dbData, parameter, title, colors)
  const chart = new ApexCharts(document.querySelector(selector), options)
  chart.render()
}

const res = await getHistoryData()

function initCharts() {
  params.forEach(param => renderChart(res, ...param))
}

initCharts()


