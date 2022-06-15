import multiprocessing
import time.sleep
import config
import mysql.connector
import sensors
from radio import codesend


class Controller():


    def __init__(self):
        self._run = self.run_for_every
        self.state = 'off'

    def restart(self):
        self.p = multiprocessing.Process(target=self._run, args=self.args, kwargs=self.kwargs)
        self.p.daemon = True
        self.p.start()


    def run(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.restart()
            

    def run_for_every(self, run_min:int=1, every_x_min:int=2, run_hours:list=range(23)):
        # switch to run hours as a list as run_within function does
        run_for = run_min * 60
        every_x = every_x_min * 60
        
        def run():
            self.on(); self.state = 'on';
            time.sleep(run_for)
            self.off(); self.state = 'off';
            time.sleep(every_x - run_for)

        while True:
            cur_hr = time.localtime().tm_hour
            if start_hr < stop_hr:#regular day time schedule
                if start_hr <= cur_hr and cur_hr < stop_hr:
                    run()
                else:
                    time.sleep(60)
            else:#overnight schedule
                if start_hr <= cur_hr or cur_hr < stop_hr:
                    run()
                else:
                    time.sleep(60)


    def run_within(self, hours:list=range(7,19)):
        while True:
            cur_hr = time.localtime().tm_hour
            if cur_hr in hours and self.state == 'off':
                self.on()
                self.state = 'on'
            elif cur_hr not in hours and self.state == 'on':
                self.off()
                self.state = 'off'
            else:
                time.sleep(60)


    def run_when_triggered(self, run_for):
        self.run_now = False
        while True:
            if self.run_now():



class exhaustFan(Controller):

    """ def on & off functions in controller factory """
    def __init__(self, *args, **kwargs):
        Controller.__init__(self)
        self.run(*args, **kwargs)

        

class growLight(Controller):

    """ def on & off functions in controller factory """
    def __init__(self, *args, **kwargs):
        Controller.__init__(self)
        self._run = self.run_within
        self.run(*args)

    

class waterPump(Controller):

    """ def on & off functions in controller factory """
    def __init__(self, *args, **kwargs):
        Controller.__init__(self)
        self._run = self.run_when_triggered # rethink, needs to integrate with zones
        self.run(*args)



class Logger(Controller):

    def __init__(self, env_sensors:list, water_sensors:list):

        controller.__init__(self)
        self._run = log

        self.env_sensors = env_sensors
        self.water_sensors =  water_sensors

        scripts = ['''CREATE TABLE environment (sensor_id VARCHAR(5),
                                                temp FLOAT(4,1),
                                                hum FLOAT(3,1),
                                                vpd FLOAT(2,1),
                                                time ''', # default now datetime stamp
                   '''CREATE TABLE water_content (sensor_id VARCHAR(5),
                                                  zone_id VARCHAR(5),
                                                  water_content FLOAT(3,1),
                                                  time ''']# default now datetime stamp

        with mysql.connector.connect(**config.db_config) as conn:
            curs = conn.cursor()
            for s in scripts:
                try:
                    curs.execute(s)
                    conn.commit()
                except Exception as e:
                    if not 'duplicate' in str(e):
                        raise e


    def log(self, every_x:int=60):
        while True:
            # thread pool executor for multiple sensors?
            self.environment()
            self.water_content()
            time.sleep(every_x)


    def environment(self, sensor_id):

        def calc_vpd(temp, hum):
            pass

        sensor = config.calibration['environment']['sensor'][sensor_id]
        temp, hum = temp_hum(sensor_model = sensor['model'], 
                             data_pin = sensor['data_pin'])
        vpd = calc_vpd(temp, hum)
        with mysql.connector.connect(**config.db_config) as conn:
            curs = conn.cursor()
            curs.execute('''INSERT INTO environment (sensor_id, temp, hum, vpd) 
                            VALUES (%s, %s, %s, %s)''',
                         (sensor_id, temp, hum, vpd))
            conn.commit()


    def water_content(self, sensor_id):
        sensor = config.calibration['irrigation']['sensor'][sensor_id]
        wc = sensors.water_content(data_pin = sensor['data_pin'])
        with mysql.connector.connect(**config.db_config) as conn:
            curs = conn.cursor()
            curs.execute('''INSERT INTO water_content (sensor_id, zone_id, water_content) 
                            VALUES (%s, %s, %s)''',
                         (sensor_id, sensor['zone_id'], wc))
            conn.commit()






class Factory:

    def new(controller_type:str, on:int, off:int):
        controllers = {
            'Exhaust Fan Controller':exhaustFan,
            'Lighting Controller':growLight,
            'Irrigation Controller': waterPump,
            }
        controller = controllers[controller_type]
        controller.on = lambda: codesend(on)
        controller.off = lambda: codesend(off)
        return controller
