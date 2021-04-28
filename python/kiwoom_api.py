from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import json

class Kiwoom_api(QAxWidget):

    def __init__(self):
        super().__init__()
        self.api_connnect()
        self.json_reader()
        self.received_data = []
        self.before_tr_name = ""

        #tran의 결과값, event를 받아오는 파트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        self.event_loop = QEventLoop()

    
    #데이터 형식
    def json_reader(self):
        with open('./config/req_data.json', encoding='UTF8') as json_file:
            json_data = json.load(json_file)
            json_string = json_data["req_list"]
            self.req_list = json_data

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
    def receive_trdata(self, screen_no, tr_name, tr_code, recordname, prev_next, data_len, err_code, msg1, msg2):
        try:
            data_list = self.req_list["req_list"][tr_name]["list"]
            #첫번째 tr시작을 판단하기 위한 변수
            #첫번째 시작인경우 값을 비우고 채울준비를 한다.
            if tr_name != self.before_tr_name:
                self.before_tr_name = tr_name
                self.received_data = []


            return_dictionary = {}
            for data in data_list:
                data = data.strip()
                temp_value = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", tr_code, "", tr_name, 0, data)
                return_dictionary[data] = temp_value.strip()

            #none tpye check
            #print(return_dictionary)
            self.received_data.append(return_dictionary)

            print("hello " + str(prev_next) + " : " + str(return_dictionary))
            self.event_loop.exit()

            if prev_next != "0":
                self.send_trdata(tr_name, tr_code, prev_next, "0101")




        except Exception as e:
            error_json = {"result" : "JSON LIST가 없습니다."}
            print('list 없는 항목의 응답값입니다.', error_json)
            self.received_data = data
            self.event_loop.exit()



    """
        해당 파트를 정의해서 범용으로 값을 보낼 수 있도록 해야한다.
        tr_name : 사용자 구분명
        tr_code : tr 이름
        prev_next : 연속조회 여부
        screen_num : 화면번호
    """
    #tran의 데이터를 보내주는 함수
    def send_trdata(self, tr_name, tr_code, prev_next, screen_num):
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", tr_name, tr_code, int(prev_next), screen_num)

    #tran의 값을 입력하기 위한 함수
    def set_input_value(self, value_name, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", value_name, value)

    #자신의 계좌 상태를 확인하기 위한 함수
    def get_my_account(self):

        #self.set_input_value("계좌번호", "")
        #opt10085 계좌 수익률
        print(12345)

        """
            이름,
            코드,
            연속조회여부,
            화면번호
        """
        #self.kiwoom.send_trdata("opt10085_req", "opt10085", "0", "0101")

    #종목 코드, 일자를 통해 정보를 받아오는 함수
    def get_cop_info(self, cop_code, date_string):

        self.set_input_value("종목코드", cop_code)
        self.set_input_value("조회일자", date_string)
        self.set_input_value("표시구분", "1")
        self.send_trdata("opt10086_req", "opt10086", "0", "0101")
        self.event_loop.exec_()

