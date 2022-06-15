#from scheduler import Scheduler
import time.sleep
import os
import multiprocessing
from controllers import Factory
import config


if __name__ == '__main__':
    
    controllers = list()
    for id in config.config['controllers']:
        controller = config.config['controllers'][id]
        c = Factory.new(controller['type'], controller.get('on_code'), controller.get('off_code'))
        controllers.append(c(*controller['args']))

    ##exhaustFan(12*60, 12*60, 7, 19) #potential as a light controller
    #controllers = [
    #    #growLight(12*6, 12*60, 22, 6),
    #    Factory.new('exhaustFan')(5, 10, 9, 18),#run_min, every_x_min, start_hr, stop_hr
    #    Factory.new('growLight')([h for h in range(24) if h not in range(6, 22)]) #set all hours not in range(stop, start)
    #]

    while True:# busy loop to check in on processes
        for controller in controllers:
            if not controller.p.is_alive():
                controller.restart()
            else:
                time.sleep(1)
        
    
        

    
