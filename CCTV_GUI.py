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
        self.maskRateList = []

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

    # 폰트 설정 함수
    def textSet(self, font, size, color, text):
        textSet = f'''
            <html><head/><body><p><span style="
            font-family:{font}; 
            font-size:{size}pt; 
            color:{color};
            ">{str(text)}</span></p></body></html>'''
        return textSet

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
                self.maskRateList.clear()
                break

            # 마스크 유무 변수 받기
            self.maskWearNum = random.randint(0, 10) # <<<<<<< 마스크 착용자 수 할당
            self.maskNotWearNum = random.randint(0, 10) # <<<<<<< 마스크 미착용자 수 할당

            # 마스크 착용, 미착용자 수 출력             #글씨체, 크기, 색, 내용
            self.maskWearersLabel.setText(self.textSet('Malgun Gothic', 13, '#00ff7f', self.maskWearNum))
            self.maskNotWearersLabel.setText(self.textSet('Malgun Gothic', 13, '#ff5454', self.maskNotWearNum))
            
            # 마스크 착용률 출력
            ## 인원 수 계산
            totalPeopleNum = self.maskWearNum + self.maskNotWearNum
            ## 인원이 있다면
            if totalPeopleNum:
                self.maskWearRate = int(self.maskWearNum / (totalPeopleNum) * 100)
                ## 비율이 x% 이상일 때
                if 70 <= self.maskWearRate:
                    self.maskRateLabel.setText(self.textSet('Malgun Gothic', 17, '#00ff7f', str(self.maskWearRate) + '%'))
                elif 50 <= self.maskWearRate < 70:
                    self.maskRateLabel.setText(self.textSet('Malgun Gothic', 17, '#ffff7f', str(self.maskWearRate) + '%'))
                else:
                    self.maskRateLabel.setText(self.textSet('Malgun Gothic', 17, '#ff5454', str(self.maskWearRate) + '%'))
            else:
                self.maskWearRate = 100
                self.maskRateLabel.setText(self.textSet('Malgun Gothic', 13, 'white', "인원 없음"))

            # N분 평균 착용자 수
            self.maskRateList.append(self.maskWearRate)
            maskWearAverage = int(sum(self.maskRateList)/len(self.maskRateList))
            self.maskWearAverageLabel.setText(self.textSet('Malgun Gothic', 17, 'white', str(maskWearAverage) + '%'))

            if len(self.maskRateList) == 60:
                self.maskRateList.pop(0)
                           
            time.sleep(0.5)

    def normalMode(self):
        self.killSwitch = 0
        self.mode_Select_Widget.hide()
        self.normal_Mode_Widget.show()
        self.pLabel.show()
        threading.Thread(target=self.normalProcess,args=()).start()
        threading.Thread(target=self.camera,args=()).start()
    ## */ ###############################################################

    ## /* 경계모드 #######################################################
    def guardProcess(self):
        while True:
            if self.killSwitch:
                break
            self.movement = random.randint(0, 1) # <<<<<<< 움직임 여부 할당
            
            if self.movement == True:
                self.movementLabel.setText(self.textSet('Malgun Gothic', 16, '#ff5454', '움직임 감지!!!'))
            else:
                self.movementLabel.setText(self.textSet('Malgun Gothic', 16, '#00ff7f', '움직임 없음'))

            time.sleep(1)

    def guardMode(self):
        self.killSwitch = 0
        self.mode_Select_Widget.hide()
        self.guard_Mode_Widget.show()
        self.pLabel.show()
        threading.Thread(target=self.guardProcess,args=()).start()
        threading.Thread(target=self.camera,args=()).start()
    ## */ ###############################################################

    def camera(self):
        while True:
            if self.killSwitch:
                break
            pixmap = QPixmap('test1.jpg')
            pixmap = pixmap.scaledToWidth(700)
            self.pLabel.setPixmap(pixmap)
            time.sleep(1)
            pixmap = QPixmap('test2.jpg')
            pixmap = pixmap.scaledToWidth(700)
            self.pLabel.setPixmap(pixmap)
            time.sleep(1)
            pixmap = QPixmap('test3.png')
            pixmap = pixmap.scaledToWidth(700)
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