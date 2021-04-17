import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
import platform

from kiwoom_api import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chicken run")
        self.setGeometry(300, 300, 300, 150)

        #현재 실행중인 환경의 비트수 
        print(platform.architecture())

        self.kiwoom = Kiwoom_api()
        """
        #키움 api와 연결 
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        #키움 api 로그인 실행
        self.kiwoom.dynamicCall("CommConnect()")


        #self.kiwoom.OnEventConnect.connect(self.event_connect)
        #tran이후 데이터를 받아오는 파트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
    
        btn2 = QPushButton("Check", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)
        """

   


    def btn2_clicked(self):
        total_message = ""
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            total_message += "Not connected\n"
        else:
            total_message += "connected\n"


        #self.kiwoom.SetInputValue("종목코드", "005930")
        #self.kiwoom.CommRqData("OPT10001", "OPT10001", 0, "0101")

        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005930")
        hello = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")
        print(hello) 


        #last_massage = self.kiwoom.dynamicCall('GetCommRealData(QString, QString)', "005930", 10)
        #print(last_massage)
        #self.statusBar().showMessage(total_message + str(last_massage))


    
    

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()