# -*- coding: utf-8 -*-
import logging
logging.basicConfig(
                  level    = logging.INFO,
                  format='%(asctime)s-%(levelname)s-%(message)s',
                  datefmt  = '%y-%m-%d %H:%M',
                  filename = 'info.log',
                  filemode = 'a',unicode='utf-8'
                  )
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)



