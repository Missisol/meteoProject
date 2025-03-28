const rpiT = document.querySelector('#rpi-t')
const rpiP = document.querySelector('#rpi-p')
const rpiH = document.querySelector('#rpi-h')
const rpiDate = document.querySelector('#rpi-date')

const dhtLoading = document.querySelector('#dht-loading')
const dhtT1 = document.querySelector('#dht1-t')
const dhtH1 = document.querySelector('#dht1-h')
const dhtT2 = document.querySelector('#dht2-t')
const dhtH2 = document.querySelector('#dht2-h')
const dhtDate = document.querySelector('#dht-date')

const bmeT = document.querySelector('#bme-t')
const bmeP = document.querySelector('#bme-p')
const bmeH = document.querySelector('#bme-h')
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
    dhtDate.textContent = Date.now()
});
socket.on('bme_message', (data) => {
    const bme = JSON.parse(data)
    bmeT.textContent = bme['temperature']
    bmeP.textContent = bme['pressure']
    bmeH.textContent = bme['humidity']
    bmeDate.textContent = Date.now()
});


function updateSensorReadings() {
    fetch('/sensorReadings')
        .then((response) => response.json())
        .then((jsonR) => {
            rpiT.textContent = jsonR.temperature
            rpiP.textContent = jsonR.pressure
            rpiH.textContent = jsonR.humidity
            rpiDate.textContent = jsonR.created_at
        })
}

function getBme280OuterData() {
    fetch('/bme280Outer')
        .then((response) => response.json())
        .then((jsonR) => {
            bmeT.textContent = jsonR.temperature
            bmeP.textContent = jsonR.pressure
            bmeH.textContent = jsonR.humidity
            bmeDate.textContent = jsonR.created_at
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
            dhtDate.textContent = jsonR.created_at
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
