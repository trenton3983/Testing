# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 10:14:11 2017

@author: tjmckinx
"""

import pyautogui
import time
from numpy import random
import datetime

start_time = datetime.datetime.now()

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

print(f'Start Time: {start_time}')
print(f'Cursor Position: {pyautogui.position()}')
print(f'Screen Resolution: {pyautogui.size()}')

activities = ['Defecating',
              'Eating',
              'Urinating',
              'None Yo Biznus',
              'Predisposed',
              'Indisposed',
              'Collating',
              'In the lab',
              'Elsewhere, obviously',
              'Indeterminate',
              'Determinate',
              'Heterogeneous',
              'Homogeneous']

try:
    while True:
            #pyautogui.moveRel(100, 0, duration=0.25)
            #pyautogui.moveRel(-100, 0, duration=0.25)
            print(f'Current Status: {activities[random.randint(0, 12)]}')
            pyautogui.click()
            time.sleep(59)
except KeyboardInterrupt:
    print('Returned, clearly!')
    print(f'Elapsed Time: {datetime.datetime.now() - start_time}')
    print('Done')
