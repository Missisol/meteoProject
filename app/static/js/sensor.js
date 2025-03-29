const rpiT = document.querySelector('#rpi-temperature')
const rpiP = document.querySelector('#rpi-pressure')
const rpiH = document.querySelector('#rpi-humidity')
const rpiDate = document.querySelector('#rpi-date')

const dhtT1 = document.querySelector('#dht1-temperature')
const dhtH1 = document.querySelector('#dht1-humidity')
const dhtT2 = document.querySelector('#dht2-temperature')
const dhtH2 = document.querySelector('#dht2-humidity')
const dht1Date = document.querySelector('#dht1-date')
const dht2Date = document.querySelector('#dht2-date')

const bmeT = document.querySelector('#bme-temperature')
const bmeP = document.querySelector('#bme-pressure')
const bmeH = document.querySelector('#bme-humidity')
const bmeDate = document.querySelector('#bme-date')


const timer = 1000 * 60
// const timer = 1000 * 60 * 5


var socket = io();
socket.on('connect', () => {
    // console.log(socket.id)
});
socket.on('dht_message', (data) => {
    const dht = JSON.parse(data)
    dhtT1.textContent = dht['temperature-1']
    dhtT2.textContent = dht['temperature-2']
    dhtH1.textContent = dht['humidity-1']
    dhtH2.textContent = dht['humidity-2']
    dht1Date.textContent = dht2Date.textContent = new Date().toLocaleString('ru')
});
socket.on('bme_message', (data) => {
    const bme = JSON.parse(data)
    bmeT.textContent = bme['temperature']
    bmeP.textContent = bme['pressure']
    bmeH.textContent = bme['humidity']
    bmeDate.textContent = new Date().toLocaleString('ru')
});


function updateSensorReadings() {
    fetch('/sensorReadings')
        .then((response) => response.json())
        .then((jsonR) => {
            rpiT.textContent = jsonR.temperature
            rpiP.textContent = jsonR.pressure
            rpiH.textContent = jsonR.humidity
            rpiDate.textContent = new Date(jsonR.created_at).toLocaleString('ru')
        })
}

function getBme280OuterData() {
    fetch('/bme280Outer')
        .then((response) => response.json())
        .then((jsonR) => {
            bmeT.textContent = jsonR.temperature
            bmeP.textContent = jsonR.pressure
            bmeH.textContent = jsonR.humidity
            bmeDate.textContent = new Date(jsonR.created_at).toLocaleString('ru')
        })
}

function getDht22OuterData() {
    fetch('/dht22Outer')
        .then((response) => response.json())
        .then((jsonR) => {
            dhtT1.textContent = jsonR.temperature1
            dhtT2.textContent = jsonR.temperature2
            dhtH1.textContent = jsonR.humidity1
            dhtH2.textContent = jsonR.humidity2
            dht1Date.textContent = dht2Date.textContent = new Date(jsonR.created_at).toLocaleString('ru')
        })
}

function checkContent() {
    if (!dhtT1.innerText) {
        getDht22OuterData()
    }
    if (!bmeT.innerText) {
        getBme280OuterData()
    } 
}


function loop() {
    setTimeout(() => {
      updateSensorReadings()
      loop()
    }, timer)
  }
  

  checkContent()
  updateSensorReadings()
  loop()


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
