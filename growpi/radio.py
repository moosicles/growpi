import os.system, time.sleep

def codesend(code, retry=3):
    path = '/var/www/html/rfoutlet'
    for i in range(retry):
        os.system(f'{path}/codesend {code}')
        time.sleep(1)
