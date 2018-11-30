# coding=utf-8
import os
import time
class AppiumServer():
        def start_AppiumS(self, port, bport):
                t = "start node d:\\Appium\\node_modules\\appium\\lib\\server\\main.js --address 127.0.0.1 --port " + port + " --platform-name Android --platform-version 6.0.1 --automation-name Appium --log-level info --command-timeout 180 --session-override  -bp " + bport
                os.system(t)


if __name__ == '__main__':
    AppiumServer().start_AppiumS('4713','4724')