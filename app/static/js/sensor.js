const rpiT = document.querySelector('#rpi-temperature')

const bmeT = document.querySelector('#bme-temperature')

const dht1T = document.querySelector('#dht1-temperature')
const dht1H = document.querySelector('#dht1-humidity')
const dht1Date = document.querySelector('#dht1-date')

const dht2T = document.querySelector('#dht2-temperature')
const dht2H = document.querySelector('#dht2-humidity')
const dht2Date = document.querySelector('#dht2-date')

// const timer = 1000 * 60
const timer = 1000 * 60 * 5

const postfixBme = ['temperature', 'pressure', 'humidity', 'date']

function getElementMap(prefix) {
    const dynamicMap = new Map()
    postfixBme.forEach((p) => {
        dynamicMap.set(p, document.querySelector(`#${prefix}-${p}`))
    })
    return dynamicMap
}

function getTextContent(map, data) {
    map.forEach((v, k) => {
        if (v && k === 'date') {
            console.log('v', v)
            v.textContent = data?.created_at ? new Date(data.created_at).toLocaleString('ru') : new Date().toLocaleString('ru')
        } 
        if (data[k] && k !== 'date') {
            v.textContent = data[k]
        }
    })
}

function getSensorData(url, prefix) {
    const map = getElementMap(prefix)
    fetch(url)
        .then((response) => response.json())
        .then((res) => {
            console.log('map', map)
            getTextContent(map, res)
        })
}

var socket = io();
socket.on('connect', () => {
    // console.log(socket.id)
});
socket.on('dht_message', (data) => {
    const dht = JSON.parse(data)
    if (dht1T) {
        dht1T.textContent = dht['temperature-1']
        dht2T.textContent = dht['temperature-2']
        dht1H.textContent = dht['humidity-1']
        dht2H.textContent = dht['humidity-2']
        dht1Date.textContent = dht2Date.textContent = new Date().toLocaleString('ru')
    }
});
socket.on('bme_message', (data) => {
    const bme = JSON.parse(data)

    const map = getElementMap('bme')
    getTextContent(map, data)

    // if (bmeT) {
    //     bmeT.textContent = bme['temperature']
    //     bmeP.textContent = bme['pressure']
    //     bmeH.textContent = bme['humidity']
    //     bmeDate.textContent = new Date().toLocaleString('ru')
    // }
});


// function getBme280RpiData() {
//     fetch('/bme280Rpi')
//         .then((response) => response.json())
//         .then((jsonR) => {
//             rpiT.textContent = jsonR.temperature
//             rpiP.textContent = jsonR.pressure
//             rpiH.textContent = jsonR.humidity
//             rpiDate.textContent = new Date(jsonR.created_at).toLocaleString('ru')
//        })
// }

// function getBme280OuterData() {
//     fetch('/bme280Outer')
//         .then((response) => response.json())
//         .then((jsonR) => {
//             bmeT.textContent = jsonR.temperature
//             bmeP.textContent = jsonR.pressure
//             bmeH.textContent = jsonR.humidity
//             bmeDate.textContent = new Date(jsonR.created_at).toLocaleString('ru')
//         })
// }


function getDht22OuterData() {
    fetch('/dht22Outer')
        .then((response) => response.json())
        .then((jsonR) => {
            dht1T.textContent = jsonR.temperature1
            dht2T.textContent = jsonR.temperature2
            dht1H.textContent = jsonR.humidity1
            dht2H.textContent = jsonR.humidity2
            dht1Date.textContent = dht2Date.textContent = new Date(jsonR.created_at).toLocaleString('ru')
        })
}

function checkContent() {
    if (dht1T && !dht1T.innerText) {
        getDht22OuterData()
    }
    if (bmeT && !bmeT.innerText) {
        // getBme280OuterData()
        getSensorData('/bme280Outer', 'bme')

    } 
}

function loop() {
    setTimeout(() => {
    //   getBme280RpiData()
    getSensorData('/bme280Rpi', 'rpi')
      loop()
    }, timer)
  }
  
function init() {
    checkContent()
    if (rpiT) {
        // getBme280RpiData()
        getSensorData('/bme280Rpi', 'rpi')

        loop()
    }
}

window.onload = (e) => {
    init()
}





// apexcharts https://apexcharts.com/docs/creating-first-javascript-chart/

// var options = {
//     chart: {
//       type: 'line'
//     },
//     series: [{
//       name: 'sales',
//       data: [30,40,35,50,49,60,70,91,125]
//     }],
//     xaxis: {
//       categories: [1991,1992,1993,1994,1995,1996,1997, 1998,1999]
//     }
//   }
  
//   var chart = new ApexCharts(document.querySelector("#chart"), options);
  
//   chart.render();
