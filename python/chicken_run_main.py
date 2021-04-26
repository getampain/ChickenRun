import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
import platform

from kiwoom_api import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        

        #현재 실행중인 환경의 비트수 
        print(platform.architecture())
        self.kiwoom = Kiwoom_api()

        #계좌상태를 보여주기 위한 택스트 박스 추가
        self.account_text = QTextEdit()
        self.account_text.setAcceptRichText(False)
        self.account_text.setReadOnly(True)
    
        #칰런 시작버튼
        self.btn_run = QPushButton("Run!", self)
        self.btn_run.clicked.connect(self.btn_run_chickenrun)

        #메인 박스
        vbox = QVBoxLayout()
        vbox.addWidget(self.account_text)
        vbox.addWidget(self.btn_run)
        vbox.addStretch()

        #사이즈 세팅
        self.setLayout(vbox)
        self.setWindowTitle("Chicken run")
        self.setGeometry(300, 300, 300, 250)

    def btn_run_chickenrun(self):
        """
            데이터 수집?
            작업?
            연결등의 작업을 진행해준다.
        """
        self.check_my_account()
        self.btn_first_my_function()

    def btn_first_my_function(self):
        #005930
        self.kiwoom.set_input_value("종목코드", "034730")
        self.kiwoom.set_input_value("조회일자", "20210419")
        self.kiwoom.set_input_value("표시구분", "1")
        self.kiwoom.send_trdata("opt10086_req", "opt10086", "0", "0101")

        self.kiwoom.event_loop.exec_()

        hello_world = self.kiwoom.received_data
        print(hello_world)
    
    def check_my_account(self):
        print("hello...")

    #config항목을 어떻게할까 예민한 데이터도 존재한다.... git ignore 예상

    #값을 바인딩해버리자 타이머같은걸로 계속 리셋하는게 어떨까?
    #이벤트 연결안하고 그냥불러와도 값이 읽히는거같은대...?
    #



if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())