# -*- coding: GB2312 -*-
from File import file
import re
yc =file().read_TKT()
print yc

for i in range(0,yc.__len__()):
    print re.findall('[0-9]{10}',yc[i].strip('\n'))[0]
    print re.findall('\|(.*)', yc[i].strip('\n'))[0]



