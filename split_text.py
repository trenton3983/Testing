# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:17:37 2017

@author: tjmckinx
"""

text = r'C:\ProgramData\Oracle\Java\javapath;C:\Program Files (x86)\Common Files\Intel\Shared Libraries\redist\ia32\mpirt;C:\Program Files (x86)\Common Files\Intel\Shared Libraries\redist\ia32\compiler;C:\Python27\Lib\site-packages\PyQt4;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;C:\Program Files (x86)\IVI Foundation\IVI\bin;C:\Program Files\IVI Foundation\IVI\bin;C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\;C:\Program Files\IVI Foundation\VISA\Win64\Bin\;C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin;F:\TortoiseSVN\bin;C:\gtk\bin;C:\Program Files (x86)\GTK2-Runtime\bin;%systemroot%\System32\WindowsPowerShell\v1.0\;C:\Users\ammonk\Desktop\Gtk+ Bundle\bin;C:\Python27;C:\Python27\Scripts;%systemroot%\System32\WindowsPowerShell\v1.0'
new_text = text.split(';')
print(new_text)