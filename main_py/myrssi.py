from bluepy.btle import Scanner
import pymysql

db=pymysql.connect(host="localhost", user="root", passwd="1234", db='memberdb')

cur = db.cursor()
cur.execute("select address from member")

# member 테이블에 저장되어있는 기기의 mac주소를 가져옴
result=cur.fetchall()

def distance_measure():
    scanner = Scanner()
    
    while True:
        i=0
        print("------------searching-----------")
        devices = scanner.scan(1.0)
        
        # 주변의 기기 신호를 가져와서 db에 저장이 되어있는 mac 주소인지 판단
        for device in devices:
             #if device.addr == "a4:cf:12:58:cf:36":
             if len(result)==i:
                 i=0
             
             # 회원가입 되어있는 mac 주소이고 가까운거리에 있는지 판단
             if device.addr == result[i][0]:   
                if device.rssi >= -50:
                    print("nearby ok")
                    print("rssi = {}".format(device.rssi))
                    break
                
                else:
                    print("so far")
                    print("rssi = {}".format(device.rssi))
                    devices = scanner.scan(1.0)
                    continue
             i=i+1
             
        if len(result)==i:
            i=0
        else:
            if device.addr == result[i][0]:
                return result[i][0] # 연결시도할 기기의 mac주소 리턴
                break
       
        
