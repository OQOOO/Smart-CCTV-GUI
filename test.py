import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
qPixmapVar = QPixmap()

# UI파일 연결
form_class = uic.loadUiType("untitled.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.testImg()

		# 위젯 시그널 입력
        ''' ex)
        self.Qt_Designer에서_정한_objectName값.clicked.connect(self.작동시킬함수)
        '''

	# 작동시킬 함수들 작성
    ''' ex)
    def 작동시킬함수(self):
    	print("함수작동")
        self.출력할위젯objectName값.setText(str(1))
    '''
    def testImg(self):
        img_url = 'C:\\Users\igh07\OneDrive\바탕 화면\smartCCTV\\tImg.png'
        qPixmapVar.load(img_url)
        self.imgTest.setPixmap(qPixmapVar)

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()