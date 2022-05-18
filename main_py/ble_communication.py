from bluepy import btle
from bluepy.btle import Scanner
from datetime import datetime
import myrssi
import pymysql

value = [0]*30

db=pymysql.connect(host="localhost", user="root", passwd="1234", db='memberdb')

cur = db.cursor()

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global mystr
        mystr = data
        
        value.pop(0)
        value.append(data[0])
        
# 기기와의 신호세기 측정 및 기기의 mac주소를 전달받음
address = myrssi.distance_measure()
  
# Initialisation
#address = "a4:cf:12:58:cf:36" # Esp32 address
service_uuid = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
char_uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

while True:

    try:
        p = btle.Peripheral(address)
        p.setDelegate(MyDelegate())
        break
        
    except:
        continue

# Setup to turn notifications
svc = p.getServiceByUUID(service_uuid)
ch = svc.getCharacteristics(char_uuid)[0]

"""
setup_data for bluepy noification-
"""

setup_data = b"\x01\x00" 
p.writeCharacteristic(ch.valHandle + 1, setup_data) 

ch_data = p.readCharacteristic(ch.valHandle + 1) 

cur.execute("select pw from member where address = %s",address)
result=cur.fetchall()

cur.execute("select name from member where address = %s",address)
name = cur.fetchall()
print("=== 안녕하세요. "+name[0][0]+" 님 ===",)

while True:
    if p.waitForNotifications(0.5):
        
        if mystr==b'Input PW':
        
            while True:
            
                pw=input("PIN 번호: ")
                
                if pw==result[0][0]:
                    now = datetime.now()
                    now = now.strftime("%Y-%m-%d %H:%M")
                    
                    # 저장되어 있는 mac 주소에 맞는 이름과 기기 주소를 가져옴
                    cur.execute("select name,address from member where address = %s",address)
                    result=cur.fetchall()
                    
                    # PIN번호를 알맞게 입력하면 문이 열리고 출입관리db에 이름,주소,현재시간을 저장하여 관
                    cur.execute("insert into manage values(%s,%s,%s)",(result[0][0],result[0][1],now))
                    db.commit()
                    db.close()
                    print("----------DOOR OPEN----------")
                    break
                    
                else:
                    print("잘못 입력하셨습니다. 다시 입력해주세요.")
            break

