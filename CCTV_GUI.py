import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication # 종료버튼용
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

import threading
import time
import random # 임시 표시용

from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QMovie


# UI파일 연결
form_class = uic.loadUiType("CCTV_GUI.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 초기 화면 설정
        self.normal_Mode_Widget.hide()
        self.guard_Mode_Widget.hide()
        self.pLabel.hide()

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
    ## 모드선택. 반복문 중단 역할도 함
    def modeSelect(self):
        self.killSwitch = 1
        self.normal_Mode_Widget.hide()
        self.guard_Mode_Widget.hide()
        self.pLabel.hide()
        self.mode_Select_Widget.show()

    ## /* 일반모드 #######################################################
    def normalProcess(self):
        while True:
            if self.killSwitch:
                break

            # 마스크 유무 변수 받기
            self.maskWearNum = random.randint(0, 15) # <<<<<<< 마스크 착용자 수 할당
            self.maskNotWearNum = random.randint(0, 15) # <<<<<<< 마스크 미착용자 수 할당

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
            color:#ff5454;
            ">{str(self.maskNotWearNum)}</span></p></body></html>''')
            
            time.sleep(1)

    def normalMode(self):
        self.killSwitch = 0
        self.mode_Select_Widget.hide()
        self.normal_Mode_Widget.show()
        self.pLabel.show()
        self.nt = threading.Thread(target=self.normalProcess,args=())
        self.nt.start()
        threading.Thread(target=self.camera,args=()).start()
    ## */ ###############################################################

    ## /* 경계모드 #######################################################
    def guardProcess(self):
        while True:
            if self.killSwitch:
                break
            self.movement = random.randint(0, 1) # <<<<<<< 움직임 여부 할당
            
            if self.movement == True:
                self.movementLabel.setText('''
                <html><head/><body><p><span style="
                font-family:'Malgun Gothic'; 
                font-size:16pt; 
                color:#ff5454;
                ">움직임 감지!!!</span></p></body></html>''')
            else:
                self.movementLabel.setText('''
                <html><head/><body><p><span style="
                font-family:'Malgun Gothic'; 
                font-size:16pt; 
                color:#00ff7f;
                ">움직임 없음</span></p></body></html>''')

            time.sleep(1)

    def guardMode(self):
        self.killSwitch = 0
        self.mode_Select_Widget.hide()
        self.guard_Mode_Widget.show()
        self.pLabel.show()
        self.gt = threading.Thread(target=self.guardProcess,args=())
        self.gt.start()
        threading.Thread(target=self.camera,args=()).start()
    ## */ ###############################################################
    def camera(self):
        while True:
            if self.killSwitch:
                break
            pixmap = QPixmap('test1.jpg')
            pixmap = pixmap.scaledToWidth(500)
            self.pLabel.setPixmap(pixmap)
            time.sleep(1)
            pixmap = QPixmap('test2.jpg')
            pixmap = pixmap.scaledToWidth(500)
            self.pLabel.setPixmap(pixmap)
            time.sleep(1)
            pixmap = QPixmap('test3.png')
            pixmap = pixmap.scaledToWidth(500)
            self.pLabel.setPixmap(pixmap)
            time.sleep(1)


if __name__ == "__main__" :
    app = QApplication(sys.argv)

    app.setStyle("Fusion") # GUI 외관
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