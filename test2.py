import threading

class ThreadTest:
    def __init__(self):
        self.killSwitch = 1

    #########################################
    def loop(self):
        n = 0
        while True:
            if self.killSwitch:
                break
            n += 1
            print(n)
    #########################################

    def switchIpt(self):
        while True:

            self.killSwitch = int(input())
            print("" ,self.killSwitch, " <<<<<")

            if self.killSwitch == 0:
                threading.Thread(target=self.loop, args=()).start()

th = ThreadTest()
th.switchIpt()