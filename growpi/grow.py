#from scheduler import Scheduler
import time
import os
import multiprocessing
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
            

    def run_for_every(self, run_min:int=1, every_x_min:int=2, start_hr:int=7, stop_hr:int=19):
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


class exhaustFan(Controller):


    def __init__(self, *args, **kwargs):
        Controller.__init__(self)
        self.run(*args, **kwargs)

        
    def on(self):
        codesend(349491)


    def off(self):
        codesend(349500)



class growLight(Controller):


    def __init__(self, *args, **kwargs):
        Controller.__init__(self)
        self._run = self.run_within
        self.run(*args)

    
    def on(self):
        codesend(349635)


    def off(self):
        codesend(349644)



if __name__ == '__main__':
    
    #exhaustFan(12*60, 12*60, 7, 19) #potential as a light controller
    controllers = [
        #growLight(12*6, 12*60, 22, 6),
        exhaustFan(5, 10, 9, 18),#run_min, every_x_min, start_hr, stop_hr
        growLight([h for h in range(24) if h not in range(6, 22)]) #set all hours not in range(stop, start)
    ]
    
    while True:# busy loop to check in on processes
        for controller in controllers:
            if not controller.p.is_alive():
                controller.restart()
            else:
                time.sleep(1)
        
    
        

    
