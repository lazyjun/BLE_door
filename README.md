하드웨어 구성
- 아두이노 ESP32 → 출입인증 장비
- Raspberry Pi 3 Model B+ → 출입제어 장비
- 라즈베리파이에 bluepy 라이브러리 설치 필요

```python
For Python 3, you may need to use pip3:
$ sudo apt-get install python3-pip libglib2.0-dev
$ sudo pip3 install bluepy
```
- 라즈베리파이에 DB 구축을 위해 mariaDB 설치

```python
$ sudo apt-get install mariadb-server
```

- 라즈베리파이에 DB 연동을 위해 pymysql 모듈 설치 필요

```python
$ sudo pip3 install pymysql
```

실행파일
main_py 안에 ble_communication.py를 실행하면 된다.
