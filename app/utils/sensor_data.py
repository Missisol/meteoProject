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
    { 'text': 'Таблицы', 'nested': [
        { 'url': 'sensor.bme_history', 'text': 'BME280 история'},
        { 'url': 'sensor.bme280_outer', 'text': 'BME280 внешний'},   
        { 'url': 'sensor.dht22_outer', 'text': 'DHT22 внешние'},   
        { 'url': 'sensor.bme280_rpi', 'text': 'BME280 RPI'},   
    ]},   
]

bme_rpi_table = {
    'th': ['id', 'created at (utc)', 'temperature', 'humidity', 'pressure'],
    'td': ['id', 'created_at', 'temperature', 'humidity', 'pressure']
}

bme_outer_table = {
    'th': ['id', 'created at (utc)', 'date (utc)', 'temperature', 'humidity', 'pressure'],
    'td': ['id', 'created_at', 'date', 'temperature', 'humidity', 'pressure']
}

dht_outer_table = {
    'th': ['id', 'created at (utc)', 'temperature 1', 'humidity 1', 'temperature 2', 'humidity 2'],
    'td': ['id', 'created_at', 'temperature1', 'humidity1', 'temperature2', 'humidity2']
}

history_table = {
    'th': ['id', 'date', 'min temperature', 'max temperature', 'min humidity', 'max humidity', 'min pressure', 'max pressure'],
    'td': ['id', 'date', 'min_temperature', 'max_temperature', 'min_humidity', 'max_humidity', 'min_pressure', 'max_pressure']
}

theme_switcher = [
    { 'value': 'light', 'pressed': 'false', 'icon': 'sun' },
    { 'value': 'light dark', 'pressed': 'false', 'text': 'Авто' },
    { 'value': 'dark', 'pressed': 'false', 'icon': 'moon' },
]

form_buttons = [
    { 'type': 'submit', 'id': 'button-submit', 'value': 'Задать период', 'class': 'button' },
    { 'type': 'reset', 'id': 'button-reset', 'value': 'Очистить', 'class': 'button' },
]
