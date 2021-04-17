from PyQt5.QAxContainer import *

class Kiwoom_api(QAxWidget):

    def __init__(self):
        super().__init__()
        self.api_connnect()

        #tran의 결과값을 받아오는 파트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)


    #api에 접근하고 로그인이 되어있지 않으면 로그인 창을 불러오는 하트
    def api_connnect(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    
        #login check
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.kiwoom.dynamicCall("CommConnect()")

    """
        해당 파트를 정의해서 범용으로 값을 가지고 올 수있도록 해야한다.
    """
    #tran의 결과값을 받아오는 함수
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")

            print(name.strip())
            print(volume.strip())
            #self.text_edit.append("종목명: " + name.strip())
            #self.text_edit.append("거래량: " + volume.strip())
    
    #tran의 값을 입력하기 위한 함수
    def set_input_value(self, value_name, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", value_name, value)
    
    """
        해당 파트를 정의해서 범용으로 값을 보낼 수 있도록 해야한다.
    """
    def send_trdata(self):
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")