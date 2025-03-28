box0 = [
     {
        'dataName': "Даные на", 
        'id': 'date',
    },
]

box1 = [
    {
        'dataName': "Температура, &deg;C",
        'id': 'temperature',
    }, 
    {
        'dataName': "Влажность, %", 
        'id': 'humidity',
    }, 
]

box2 = [
     {
        'dataName': "Давление, мм.рт.ст.", 
        'id': 'pressure',
    },
]

box3 = [*box1, *box2]

box4 = [*box0, *box1]

box5 = [*box0, *box3]

gauge1 = [
    'temperature',
    'humidity',
]

gauge2 = ['pressure']

gauge3 = [*gauge1, *gauge2]

data_list =  [
    { 
        'box': box1,
    },
    {
        'gauge': gauge1,
    },
]


bme_data_list =  [
    { 
        'box': box3,
    },
    {
        'gauge': gauge3,
    },
]
