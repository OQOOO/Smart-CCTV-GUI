import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication # 종료버튼용
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

import threading
import random
import time

from test import ModeSelection


# UI파일 연결
form_class = uic.loadUiType("cctv.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # 초기 화면 설정
        self.normal_Mode_Widget.hide()
        self.guard_Mode_Widget.hide()

        # 변수 선언
        self.killSwitch = 0 # 반복문 제어용 변수
        self.maskWearNum = 0 # 마스크 쓴사람
        self.maskNotWearNum = 0 # 마스크 안쓴사람
        self.movement = False # 움직임 변수
        
        # 버튼 시그널
        ## 모드선택화면 위젯 시그널
        self.normal_Mode_Button.clicked.connect(self.normalMode) # 일반모드
        self.guard_Mode_Button.clicked.connect(self.guardMode)

        ## 일반모드 위젯 시그널
        self.mode_Select_Button.clicked.connect(self.modeSelect)

        ## 경계모드 위젯 시그널
        self.mode_Select_Button_2.clicked.connect(self.modeSelect)
        
        ## 종료버튼
        self.endButton.clicked.connect(self.modeSelect)
        self.endButton.clicked.connect(QCoreApplication.instance().quit)


	# 작동시킬 함수들 작성
    ''' ex)
    def 작동시킬함수(self):
        self.출력할위젯objectName값.setText(str(1))
    '''

    ## 모드선택. 반복문 중단 역할도 함
    def modeSelect(self):
        self.killSwitch = 1
        self.normal_Mode_Widget.hide()
        self.guard_Mode_Widget.hide()
        self.mode_Select_Widget.show()

    ## /* 일반모드 #######################################################

    def normalProcess(self):
        while True:
            # 마스크 유무 변수 받기
            self.maskWearNum = random.randint(0, 15)
            self.maskNotWearNum = random.randint(0, 15)

            # 텍스트 출력
            self.maskWearersLabel.setText(f'''
            <html><head/><body><p><span style="
            font-family:'Malgun Gothic'; 
            font-size:13pt; 
            color:#00ff7f;
            ">{str(self.maskWearNum)}</span></p></body></html>''')
            self.maskNotWearersLabel.setText(f'''
            <html><head/><body><p><span style="
            font-family:'Malgun Gothic'; 
            font-size:13pt; 
            color:#ff0000;
            ">{str(self.maskNotWearNum)}</span></p></body></html>''')
            
            time.sleep(1)
            if self.killSwitch:
                break

    def normalMode(self):
        self.killSwitch = 0
        self.mode_Select_Widget.hide()
        self.normal_Mode_Widget.show()

        self.nt = threading.Thread(target=self.normalProcess,args=())
        self.nt.start()

            # ↑ 숫자형일 경우 {str(self.변수명)} 형태로 삽입

    ## */ #######################################################

    ## /* 경계모드 #######################################################

    def guardProcess(self):
        while True:
            self.movement = random.randint(0, 1) # 움직임 변수 받기
            time.sleep(1)
            
            if self.movement == True:
                self.movementLabel.setText('''
                <html><head/><body><p><span style="
                font-family:'Malgun Gothic'; 
                font-size:16pt; 
                color:#ff0000;
                ">움직임 감지!!!</span></p></body></html>''')
            else:
                self.movementLabel.setText('''
                <html><head/><body><p><span style="
                font-family:'Malgun Gothic'; 
                font-size:16pt; 
                color:#00ff7f;
                ">움직임 없음</span></p></body></html>''')
        
            if self.killSwitch:
                break

    def guardMode(self):
        self.killSwitch = 0
        self.mode_Select_Widget.hide()
        self.guard_Mode_Widget.show()
        self.gt = threading.Thread(target=self.guardProcess,args=())
        self.gt.start()

    ## */ #######################################################

if __name__ == "__main__" :
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()