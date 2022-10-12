import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
import time


# UI파일 연결
form_class = uic.loadUiType("untitled.ui")[0]

# 모드선택화면
class ModeSelection(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.show()
        self.k = 0
        

		# 위젯 시그널 입력
        #self.page2.clicked.connect(self.goToPage2)
        self.loopStart.clicked.connect(self.loop)
        self.loopBreak.clicked.connect(self.loopBk)

	# 작동시킬 함수들 작성
    def process(self):
        n = 1
        self.k = 0
        while True:
            print(n)
            n += 1
            if self.k == 1:
                break


    def loop(self):
        self.t = threading.Thread(target=self.process,args=())
        self.t.start()


    def loopBk(self):
        self.k = 1


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = ModeSelection() 
    myWindow.show()
    app.exec_()