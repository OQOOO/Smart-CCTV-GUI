import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# UI파일 연결
form_class = uic.loadUiType("modeSelection.ui")[0]
form_class2 = uic.loadUiType("normalMode.ui")[0]

# 모드선택화면
class ModeSelection(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.show()

		# 위젯 시그널 입력
        self.page2.clicked.connect(self.goToPage2)

	# 작동시킬 함수들 작성
    def goToPage2(self):
        self.hide()
        self.second = NormalMode()

    

 


# 화면을 띄우는데 사용되는 Class 선언2
class NormalMode(QMainWindow, form_class2) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.show()

		# 위젯 시그널 입력
        self.page1.clicked.connect(self.goToPage1)

	# 작동시킬 함수들 작성
    def goToPage1(self):
        self.hide()
        self.second = ModeSelection()

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = ModeSelection() 
    myWindow.show()
    app.exec_()