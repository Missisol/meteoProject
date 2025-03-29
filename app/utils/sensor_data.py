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