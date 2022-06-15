
"""
Purpose is to create a web editable configuration file in order to dynamically run different grow environments 
from a central web location. 

Sensors must be calibrated before being able to use them in a logging controller. 

Irrigation Zones must be setup / calibrated before creating an irrigation controller.

"""

db_config = {
    user : 'growpi', 
    password : 'growpi',
    host : 'localhost',
    database : 'growpi'
    }


calibration = {
    'irrigation':{
        'sensor':{
            1 : {
                'min':0,
                'max':999999,
                }
            }, # 2, 3, 4 5
        'zone':{
            1 : {
                'shot_ml': 110,
                'secs_to_shot': 5,
                },
            2 : {
                'shot_ml': 110,
                'secs_to_shot': 5,
                },
            }
        },
    'environment':{
        'sensor':{
            1 : {
                'data_pin' : 4,
                'type' : 'temp_hum',
                'model' : 2302
                }
            }
        }
    }

config = {
    'irrigation_zones': {
        1 : {
            'name':'Ice Cream Cake',
            'sensor_ids':[],
            'dryback_wc': 50,
            'wet_wc': 70,
            },
        2 : {
            'name':'Gary Payton',
            'sensor_ids':[],
            'dryback_wc': 50,
            'wet_wc': 70,
            }
    },
    'controllers': {
        1 : {
            'name': 'Side Room',
            'type': 'Lighting Controller',
            'override_function': 'run_within',
            'args': [h for h in range(24) if h not in range(6, 22)],
            'on_code': 349635,
            'off_code': 349644,
            },
        2 : {
            'name': 'Ice Cream Cake',
            'type': 'Irrigation Controller',
            'irrigation_zone': 1,
            'override_function': 'run_when_triggered',
            'args': [calibration['irrigation']['zone'][1]['secs_to_shot']], # time to run
            'on_code': 349635,
            'off_code': 349644,
            },
        3 : {
            'name': 'Gary Payton',
            'type': 'Irrigation Controller',
            'irrigation_zone': 2,
            'override_function': 'run_when_triggered',
            'args': [calibration['irrigation']['zone'][2]['secs_to_shot']],
            'on_code': 349635,
            'off_code': 349644,
            },
        4 : {
            'name': 'Temp / Hum DS322',
            'type': 'Logging Controller',
            'override_function': 'db_log_DS322', # environment logger
            'args': [60], # run every x sec
            }
        }
    }
