list_date = [
     {
        'dataName': "Даные на", 
        'data': 'date',
    },
]

list1 = [
    {
        'dataName': "Температура, &deg;C",
        'data': 'temperature',
    }, 
    {
        'dataName': "Влажность, %", 
        'data': 'humidity',
    }, 
]

list2 = [
     {
        'dataName': "Давление, мм.рт.ст.", 
        'data': 'pressure',
    },
]

list3 = [*list1, *list2]

list_dht = [*list_date, *list1]

list_bme = [*list_date, *list3]

prefix_list = ['rpi', 'bme', 'dht1', 'dht2']
sensors_list = ['rpi', 'dht1', 'dht2']
weather_list = ['bme']

main_menu = [
        { 'url': 'sensor.sensors', 'text': 'Датчики в доме'},   
        { 'url': 'sensor.bme280_rpi', 'text': 'BME280 RPI'},   
        { 'url': 'sensor.bme280_outer', 'text': 'BME280 внешний'},   
        { 'url': 'sensor.dht22_outer', 'text': 'DHT22 внешние'},   
        { 'url': 'sensor.bme_history', 'text': 'BME280 история'},   
    ]