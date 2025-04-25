// apexcharts https://apexcharts.com/docs/creating-first-javascript-chart/


async function getHistoryData() {
  const response = await fetch('/json_history')
  const res = await response.json()
  return res
}

function getChartDataFromDbData(arr, parameter) {
  const categoriesValues = []
  const minValues = []
  const maxValues = []
  let names = []
  
  arr.map((item) => {
    const date = new Date(item.date).toLocaleDateString('ru')
    categoriesValues.push(date)
    minValues.push(item[`min_${parameter}`])
    const edge = parameter !== 'pressure' ? 100 : 800
    const maxV = item[`max_${parameter}`] >= edge ? item[`min_${parameter}`] : item[`max_${parameter}`]
    maxValues.push(maxV)
    names = [`min_${parameter}`, `max_${parameter}`]
  })
  return {categoriesValues, minValues, maxValues, names}
}

function getOptionsForChart(dbData, parameter) {
  const {categoriesValues, minValues, maxValues, names } = getChartDataFromDbData(dbData, parameter)

  return {
    chart: {
      type: 'line'
    },
    series: [
      {
      name: names[0],
      data: minValues
    },
      {
      name: names[1],
      data: maxValues
    },
  ],
    xaxis: {
      categories: categoriesValues
    }
  }
}

function renderChart(selector, parameter, dbData) {
  const options = getOptionsForChart(dbData, parameter)
  const chart = new ApexCharts(document.querySelector(selector), options)
  chart.render()
}

const res = await getHistoryData()

renderChart('#chartT', 'temperature', res)
renderChart('#chartH', 'humidity', res)
renderChart('#chartP', 'pressure', res)


