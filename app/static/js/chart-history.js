// apexcharts https://apexcharts.com/docs/creating-first-javascript-chart/

const params = [
  ['#chartT', 'temperature', 'температура', ['#1d531c', '#3ba639']],
  ['#chartH', 'humidity', 'влажность', ['#1b4a79', '#3392f1']],
  ['#chartP', 'pressure', 'давление', ['#6e3889', '#cc66ff']],
]
const charts = []

function setupForm() {

  const buttonResetEl = document.querySelector('#button-reset')
  buttonResetEl.addEventListener('click', () => {
    getHistoryData()
  })
}

function initForm() {
  setupForm()
  const formEl = document.querySelector('#history-form')
  formEl.addEventListener('submit', (e) => {
      e.preventDefault()

      const params = `start=${formEl.start_date.value}&end=${formEl.end_date.value}`
      const arr =  getHistoryData(params)
      charts.forEach(chart => chart.updateSeries())
  })
}


async function getHistoryData(params) {
  const url = params ? `/json_history?${params}` : '/json_history'
  const response = await fetch(url)
  const res = await response.json()
  updateCharts(res.toReversed())
}

function getChartDataFromDbData(arr, parameter, title) {
  const minValues = []
  const maxValues = []
  
  arr.map((item, idx) => {
    const date = new Date(item.date).toLocaleDateString('ru')
    minValues.push({x: date, y: item[`min_${parameter}`]})
    const edge = parameter !== 'pressure' ? 100 : 800
    const maxV = item[`max_${parameter}`] >= edge ? item[`min_${parameter}`] : item[`max_${parameter}`]
    maxValues.push({x: date, y: maxV})
  })
  const names = [`мин ${title}`, `макс ${title}`]

  return { minValues, maxValues, names }
}

function getSeriesData(dbData, param) {
  const [ _, parameter, title, colors ] = param
  const { minValues, maxValues, names } = getChartDataFromDbData(dbData, parameter, title)
  
  return [
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
  ]
}

function getOptionsForChart(title, colors) {
  const titleText = title.toUpperCase()

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
    series: [],
    stroke: {
      dashArray: [0, 4],
    },
    xaxis: {
      type: 'category',
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

function renderChart(selector, _, title, colors) {
  const options = getOptionsForChart(title, colors)
  const chart = new ApexCharts(document.querySelector(selector), options)
  charts.push(chart)
  chart.render()
}

function initCharts() {
  params.forEach(param => renderChart(...param))
}

function updateCharts(res) {
  params.forEach((param, idx) => {
    const series = getSeriesData(res, param )
    charts[idx].updateSeries(series)
  })
}

async function initHistoryCharts() {
  initCharts()
  initForm()
  getHistoryData()
}

initHistoryCharts()

