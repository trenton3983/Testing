# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 12:22:30 2017

@author: tjmckinx
"""

from win32com.client import Dispatch
import win32com.client
import glob
import sys


mypath = r'\\npo\coos\LNO_Validation\Validation_Data\FVL Sustaining\FVL B1\Test Plans\*\*\*FVL_B1*.xlsx'

def get_files():
    files = glob.glob(mypath)
    return files


def main():
    
    xlsx = Dispatch('Excel.Application')
    
    files_ = get_files()
    count_ = len(files_)
    print(f'Number of files: {count_}')
    
    n = 0
    
    for file in files_:
        print(file.rsplit('\\', 1)[-1])
        n+=1
        print(f'Opening file: {n}')
        wb = xlsx.Workbooks.Open(file)
        
        #ws1 = wb.Worksheets('Test Matrix')
        #ws2 = wb.Worksheets('Stressed Receiver Sensitivity')
        
        xlsx.Visible = True
        
        wait = input('"End" to abort, else press Enter to continue: ')
        if wait.lower() == 'end':
            wb.Close(True)
            xlsx.Application.Quit()
            sys.exit()
        else:
            wb.Close(True)
            xlsx.Application.Quit()


if __name__ == "__main__":


    main()