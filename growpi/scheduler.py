import time
import multiprocessing
from pyfiglet import figlet_format



class Scheduler():
    """
    days are 0-6 starting on monday
    times are military format with tuples for designating minutes. 
    ie: (7,15) = 7:15am, (14:30) = 2:30pm

    set times through initialization methods 
    ie: Scheduler(days=range(0,6), times=[7,(7,15),(7,30),8,9])
    
    times passed through initialization are parsed and standardized to tuple pairs
    ie: 7 = (7,0)

    funcs should be tuple pairs of funcs and args ie: [(range, (0,10)), (max, ([number_list],)), etc]"

    initialization scheduling not recommended, does not offer granular sheduling control.
    instead, use the .schedule method once initialized. Arguments mirror the initialization method
    """
    def __init__(self, days:list=range(0,5), times:list=[7], funcs:list=[], startup_text='python scripts', font='cosmic', p=True):
        if p:
            print(figlet_format(startup_text, font=font))
        self.today = time.localtime()
        self.jobs = list()
        self.executing = list()
        self.print_headers()
        for f in funcs:
            self.schedule(days, times, f)
        print()


    def print_headers(self):
        pad = lambda s, i: ' ' * (i - len(s))
        t = 'Current Time' 
        t += pad(t, 24)
        name = 'Process' 
        name += pad(name, 13)
        sched = 'Scheduled For'
        print(t, name, sched, sep=' | ')
        print('-'*89, end='')


    def run(self):
        while True:
            now = time.localtime()
            execute, funcs = self.time_to_run(now)
            if execute:
                for func in funcs:
                    self.reset_execution_state(func)
                    try: name = func[0].__name__
                    except: name = func[0].__class__.__name__
                    print(f'{time.strftime("%c")} | running {name}')
                    p = multiprocessing.Process(target=func[0], args=func[1], name=func[0].__name__)
                    p.daemon = True
                    p.start()
                    self.executing.append(p)

            self.check_for_reset(now)
            time.sleep(20)


    def reset_execution_state(self, func:tuple):
        self.executing = [p for p in self.executing if p.is_alive()]
        try: name = func[0].__name__
        except: name = func[0].__class__.__name__
        for p in self.executing:
            if p.name == name:
                print(f'{time.strftime("%c")} | restarting {name}')
                p.terminate()


    def schedule(self, func, args=(), days:list=range(7), times:list=[(0,0)]): #default, run daily at midnight
        name = func.__name__ + ' ' * (13 - len(func.__name__))
        print(time.strftime('%c'), f'{name}', f'days: {days}, times: {times}', sep=' | ')
        times = self.parse_times(times)
        for d in days: 
            for t in times:
                self.jobs.append([(func,args),d,t,False]) # false for execution state, resets daily


    def parse_times(self, times):
        r = list()
        for t in times:
            if isinstance(t, tuple):
                r.append(t)
            else:
                r.append((int(t),0))
        return r        


    def time_to_run(self, now):
        funcs = list()
        for i in range(len(self.jobs)):
            func, day, _time, executed = self.jobs[i]
            if not executed:
                if now.tm_wday == day:
                    if now.tm_hour == _time[0]:
                        if now.tm_min == _time[1]:
                            funcs.append(func)
                            self.jobs[i][3] = True
        if funcs:
            return True, funcs
        return False, funcs


    def check_for_reset(self, now):
        if self.today.tm_wday != now.tm_wday:
            self.today = time.localtime()
            for i in range(len(self.jobs)):
                self.jobs[i][3] = False
