import json
from flask import Flask
from flask_sock import Sock, Server
import datetime
import os
import threading
import platform

app = Flask(__name__)
sock = Sock(app)

socks = []
allsocks = []
ping_delay = 5

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
def ClientOfflineDetect():
    leaveList = []
    output = {
        "type" : "ping",
        "timeout" : ping_delay
    }
    for client in allsocks:
        try:
            client['socket'].send(json.dumps(output))
        except:
            if (client['name'] == None):
                print("[<-] Đã ngắt kết nối Socket: " ,client['socket'])
                allsocks.remove(client)
            else:
                socks.remove(client)
                try: 
                    client['socket'].close() 
                except: pass
                timestamp = datetime.datetime.now()
                print("[<-] Đã rời khỏi Chatbox và ngắt kết nối Socket" , client['name'] , " (" , client['socket'] , ")")
                leaveList.append({
                    'name': client['name'],
                    'timestamp': timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                })
                allsocks.remove(client)

    for leave in leaveList:
        rec = {
            "type": "receive",
            "datatype": "leave",
            "name": leave['name'],
            "timestamp": leave['timestamp']
        }   
        for client in socks:
            try: 
                client['socket'].send(json.dumps(rec)) 
            except Exception as e: 
                print("[=] Không gửi được thông tin rời khỏi Server của ", leave['name'], " cho ", client['socket']," | Lý do: ", repr(e))


def get():
    file = open("data.json", encoding='utf_8')
    if (file.read().rstrip()==''):
        up = open("data.json", mode='w', encoding='utf_8')
        up.write('[]')
        up.close()
    file.close()
    file = open("data.json", encoding='utf_8')
    output = file.read().rstrip()
    file.close()
    return output
def find(list: list, name: str , thing):
    dem = -1
    for x in list:
        dem = dem + 1
        if (x[name] == thing):
            return dem
    return None
# Hàm này sẽ tìm thing trong [list].name, trả về None nếu không tìm thấy

if (platform.system() == "Linux" or platform.system() == "Darwin"): os.system('clear')
elif (platform.system() == "Windows"): os.system('cls')

print(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
print(" ")
print("======== CHÚ GIẢI =======")
print("[->] Kết nối tới")
print("[>] Dữ liệu Client gửi")
print("[=] Chung")
print("[+] Đăng ký Biệt danh")
print("[S] Tin nhắn gửi đi")
print("[G] Fetch Tất cả tin nhắn")
print("[/] Thay đổi Biệt danh")
print("[<-] Ngắt kết nối")
print("=========================")
print(" ")

@sock.route('/')
def connect(ws: Server):
    print("[->] Kết nối Socket mới: ", ws)
    allsocks.append({
        'name': None,
        'socket': ws
    })

    while True:
        receive = ""
        try:
            receive = ws.receive()
            print("[>]", ws, ":", receive)
        except:
            break
        
        isRightFormatJSON = False
        data = {}
        try:
            data = json.loads(receive)
            isRightFormatJSON = True
        except:
            print("[=] Từ chối Thực thi yêu cầu cho ",ws," | Lý do: WrongFormatJSON")
            out = {
                'status': False,
                'reason': "WrongFormatJSON"
            }
            ws.send(json.dumps(out))
        if (isRightFormatJSON == True):

            if (data['type'] == "name"):
                try:
                    username = data['name']
                except:
                    print("[=] Từ chối Thực thi yêu cầu Name cho ",ws," | Lý do: NotEnoughKey")
                    return ws.send(json.dumps({
                        'type' : data['type'],
                        'status': False,
                        "reason":"NotEnoughKey",
                        "need":"name"
                    }))
                    
                number = find(socks, 'socket', ws)
                if (number != None): #* Thay đổi tên
                    oldname = socks[number]['name']
                    if ((len(username)>0) & (len(username)<=100)):
                        if (find(socks, 'name', username) == None): # Không có ai sử dụng tên này
                            try:
                                socks[number]['name'] = username
                                allsocks[find(allsocks, 'socket', ws)] = socks[number]
    
                                timestamp = datetime.datetime.now()
                                out = {
                                    'type': data['type'],
                                    'action': 'change',
                                    'oldname': oldname,
                                    'newname': username,
                                    'status': True,
                                    'timestamp': timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                                }
                                ws.send(json.dumps(out))
                                print("[/] Đã thay đổi tên của ",oldname," (",ws ,") thành " ,username)
    
                                #* Send to Other Client
                                rec = {
                                    "type": "receive",
                                    "datatype": "change",
                                    "oldname": oldname,
                                    "newname": username,
                                    "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                                }
                                for client in socks:
                                    if (client['socket'] != ws):
                                        try: 
                                            client['socket'].send(json.dumps(rec)) 
                                        except Exception as e: 
                                            print("[=] Không gửi được thông tin change của ", username, " cho ", client['socket']," | Lý do: ", repr(e))
                            except Exception as e:
                                print("[/] LỖI KHI ĐỔI TÊN ",oldname, "(", ws , ") thành tên " , username , " | Lý do: ", repr(e))
                                out = {
                                    'type': data['type'],
                                    'action': 'change',
                                    'oldname': oldname,
                                    'newname': username,
                                    'status': False,
                                    'reason': "ErrorWhenChange",
                                    "error": repr(e)
                                }
                                ws.send(json.dumps(out))
                        else:
                            print("[/] Từ chối đổi tên cho ",oldname, "(", ws , ") thành tên " , username , " | Lý do: NameAlreadyUsed")
                            out = {
                                'type': data['type'],
                                'action': 'change',
                                'oldname': oldname,
                                'newname': username,
                                'status': False,
                                'reason': "NameAlreadyUsed"
                            }
                            ws.send(json.dumps(out))
                    else: 
                        print("[/] Từ chối đổi tên cho ",oldname, "(", ws , ") thành tên " , username , " | Lý do: WrongFormatName")
                        out = {
                            'type': data['type'],
                            'action':'change',
                            'oldname': oldname,
                            'newname': username,
                            'status': False,
                            'reason': "WrongFormatName"
                        }
                        ws.send(json.dumps(out))
                else: #*Đăng ký tên
                    if ((len(username)>0) & (len(username)<=100)):
                        if (find(socks, 'name', username) == None):
                            try:
                                reginfo = {
                                    "name": username,
                                    "socket": ws
                                }
                                socks.append(reginfo)
                                allsocks[find(allsocks, 'socket', ws)] = reginfo

                                timestamp = datetime.datetime.now()
                                out = {
                                    'type': data['type'],
                                    'action':'register',
                                    'name': username,
                                    'status': True,
                                    'timestamp': timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                                }
                                ws.send(json.dumps(out))
                                print("[+] Đã đăng ký " , ws , " dưới tên " , username)

                                #* Send to Other Client 
                                rec = {
                                    "type": "receive",
                                    "datatype": "register",
                                    "name": username,
                                    "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                                }   
                                for client in socks:
                                    if (client['socket'] != ws):
                                        try: 
                                            client['socket'].send(json.dumps(rec)) 
                                        except Exception as e: 
                                            print("[=] Không gửi được thông tin register của ", username, " cho ", client['socket']," | Lý do: ", repr(e))
                            except Exception as e:
                                print("[+] LỖI KHI ĐĂNG KÝ " , ws , " dưới tên " , username , " | Lý do: ", repr(e))
                                out = {
                                    'type': data['type'],
                                    'action':'register',
                                    'name': username,
                                    'status': False,
                                    'reason': "ErrorWhenRegister",
                                    "error": repr(e)
                                }
                                ws.send(json.dumps(out))
                        else:
                            print("[+] Từ chối đăng ký " , ws , " dưới tên " , username , " | Lý do: NameAlreadyUsed")
                            out = {
                                'type': data['type'],
                                'action':'register',
                                'name': username,
                                'status': False,
                                'reason': "NameAlreadyUsed"
                            }
                            ws.send(json.dumps(out))
                    else: 
                        print("[+] Từ chối đăng ký " , ws , " dưới tên " , username , " | Lý do: WrongFormatName")
                        out = {
                            'type': data['type'],
                            'action': 'register',
                            'name': username,
                            'status': False,
                            'reason': "WrongFormatName"
                        }
                        ws.send(json.dumps(out))

            elif (data['type'] == "send"):
                try:
                    content = data['content']
                except:
                    print("[S] Từ chối Thực thi yêu cầu Send cho ",ws," | Lý do: NotEnoughKey")
                    return ws.send(json.dumps({
                        'type' : data['type'],
                        'status': False,
                        "reason":"NotEnoughKey",
                        "need": "content"
                    }))
                name = ""
                try:
                    name = socks[find(socks, 'socket', ws)]['name']
                except: 
                    print("[S] Từ chối gửi tin ",ws,": ", content , " | Lý do: UnknownRegister")
                    output = {
                        "type": data['type'],
                        "status": False,
                        "reason": "UnknownRegister"
                    }
                    return ws.send(json.dumps(output))

                if ((len(content)>0) & (len(content)<=4000)):
                    try:
                        #*Read old data 
                        msg = json.loads(get())

                        #*Package data to Python list
                        timestamp = datetime.datetime.now()
                        input = {
                            "name": name,
                            "content": content,
                            "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                        }   
                        msg.append(input)

                        #*Save chat
                        file = open('data.json', mode = 'w', encoding='utf_8')
                        file.write(json.dumps(msg))
                        file.close()
                        print("[S] Đã gửi tin: ",name, " (",ws,"): ", content)

                        #*Return client send
                        output = {
                            "type": data['type'],
                            "name": name,
                            "content": content,
                            "status": True,
                            "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                        }
                        ws.send(json.dumps(output))

                        #*Update another Client
                        rec = {
                            "type": "receive",
                            "datatype": "message",
                            "name": name,
                            "content": content,
                            "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                        }   
                        for client in socks:
                            if (client['socket'] != ws):
                                try: 
                                    client['socket'].send(json.dumps(rec)) 
                                except Exception as e: 
                                    print("[=] Không gửi được thông tin message của ", username, " cho ", client['socket']," | Lý do: ", repr(e))
                    except Exception as e:
                        print("[S] LỖI KHI GỬI TIN ",name," (",ws,"): " , content , " | Lý do: ", repr(e))
                        output = {
                            "type": data['type'],
                            "username": name,
                            "content": content,
                            "status": False,
                            "reason": "ErrorWhenSend",
                            "error": repr(e)
                        }
                        ws.send(json.dumps(output))
                else:
                    print("[S] Từ chối gửi tin ",name," (",ws,"): " , content , " | Lý do: WrongFormatContent")
                    output = {
                            "type": data['type'],
                            "username": name,
                            "content": content,
                            "status": False,
                            "reason":"WrongFormatContent"
                        }
                    ws.send(json.dumps(output))

            elif (data['type'] == "get"):
                number = find(socks, 'socket', ws)
                if (number != None):
                    username = socks[number]['name']
                    output = {}
                    online = []
                    try:
                        for client in socks:
                            online.append(client['name'])
                        timestamp = datetime.datetime.now()
                        dat = json.loads(get())
                        output = {
                            "type": data['type'],
                            "status": True,
                            "name": username,
                            'timestamp': timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
                            'data': {
                                "message": dat,
                                "online": online
                            }
                        }
                        print("[G] Đã cung cấp toàn bộ tin nhắn, người online cho ",username," (",ws,")")
                    except Exception as e:
                        print("[G] LỖI KHI CUNG CẤP TOÀN BỘ TIN NHẮN, NGƯỜI ONLINE CHO ",username," (",ws,")" , " | Lý do: ", repr(e))
                        output = {
                            "type": data['type'],
                            "name": username,
                            "status": False,
                            "reason": "ErrorWhenGet",
                            "error": repr(e)
                        }
                    ws.send(json.dumps(output))
                else:
                    print("[G] Từ chối cung cấp toàn bộ tin nhắn, người online cho ",ws," | Lý do: UnknownRegister")
                    output = {
                        "type": data['type'],
                        "status": False,
                        "reason": "UnknownRegister"
                    }
                    ws.send(json.dumps(output))
    
            else: 
                output = {
                    "type": None,
                    "status": False,
                    "reason": "UnknownType"
                }
                ws.send(json.dumps(output))
                print("[=] Từ chối Thực thi yêu cầu cho ",ws," | Lý do: UnknownType")
    # Về elif: https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/

set_interval(ClientOfflineDetect, ping_delay)
app.run()