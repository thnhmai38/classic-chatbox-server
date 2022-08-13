import json
from flask import Flask
from flask_sock import Sock, Server
import datetime
import os

app = Flask(__name__)
sock = Sock(app)

socks = []

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
os.system('clear')
os.system('cls')
print(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
print(" ")
print("======== CHÚ GIẢI =======")
print("[->] Kết nối tới")
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
    try:
        while True:
            receive = ws.receive()
            data = json.loads(receive)
            
            if (data['type'] == "change"):
                number = find(socks, 'socket', ws)
                username = ""
                try:
                    username = data['name']
                except:
                    print("[/] Từ chối đổi tên ",ws," | Lý do: WrongFormatJSON")
                    out = {
                        'type': 'change',
                        'status': False,
                        'reason': "WrongFormatJSON"
                    }
                    return ws.send(json.dumps(out))
                if (number != None): # Xác nhận người này đã đăng ký
                    oldname = socks[number]['name']
                    if ((len(username)>0) & (len(username)<=100)):
                        if (find(socks, 'name', username) == None): # Không có ai sử dụng tên này
                            try:
                                socks[number]['name'] = username

                                timestamp = datetime.datetime.now()
                                out = {
                                    'type': 'change',
                                    'oldname': oldname,
                                    'newname': username,
                                    'timestamp': timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
                                    'status': True
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
                                        client['socket'].send(json.dumps(rec))

                            except Exception as e:
                                print("[/] LỖI KHI ĐỔI TÊN ",oldname, "(", ws , ") thành tên " , username , " | Lý do: ")
                                print(e)
                                out = {
                                    'type': 'change',
                                    'oldname': oldname,
                                    'newname': username,
                                    'status': False,
                                    'reason': "ErrorWhenChange"
                                }
                                ws.send(json.dumps(out))
                        else:
                            print("[/] Từ chối đổi tên cho ",oldname, "(", ws , ") thành tên " , username , " | Lý do: NameAlreadyUsed")
                            out = {
                                'type': 'change',
                                'oldname': oldname,
                                'newname': username,
                                'status': False,
                                'reason': "NameAlreadyUsed"
                            }
                            ws.send(json.dumps(out))
                    else: 
                        print("[/] Từ chối đổi tên cho ",oldname, "(", ws , ") thành tên " , username , " | Lý do: WrongFormatName")
                        out = {
                            'type': 'change',
                            'oldname': oldname,
                            'newname': username,
                            'status': False,
                            'reason': "WrongFormatName"
                        }
                        ws.send(json.dumps(out))
                else:
                    print("[/] Từ chối đổi tên cho " , ws , " thành tên " , username , " | Lý do: UnknownRegister")
                    out = {
                        'type': 'change',
                        'newname': username,
                        'status': False,
                        'reason': "UnknownRegister"
                    }
                    ws.send(json.dumps(out))

            if (data['type'] == "register"):
                username = ""
                try:
                    username = data['name']
                except:
                    print("[+] Từ chối đăng ký " , ws , " | Lý do: WrongFormatJSON")
                    out = {
                        'type': 'register',
                        'status': False,
                        'reason': "WrongFormatJSON"
                    }
                    return ws.send(json.dumps(out))

                if ((len(username)>0) & (len(username)<=100)):
                    if (find(socks, 'name', username) == None):
                        try:
                            reginfo = {
                                "name": username,
                                "socket": ws
                            }
                            socks.append(reginfo)

                            timestamp = datetime.datetime.now()
                            out = {
                                'type': 'register',
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
                                    client['socket'].send(json.dumps(rec))

                        except Exception as e:
                            print("[+] LỖI KHI ĐĂNG KÝ " , ws , " dưới tên " , username , " | Lý do: ")
                            print(e)
                            out = {
                                'type': 'register',
                                'name': username,
                                'status': False,
                                'reason': "ErrorWhenRegister"
                            }
                            ws.send(json.dumps(out))
                    else:
                        print("[+] Từ chối đăng ký " , ws , " dưới tên " , username , " | Lý do: NameAlreadyUsed")
                        out = {
                            'type': 'register',
                            'name': username,
                            'status': False,
                            'reason': "NameAlreadyUsed"
                        }
                        ws.send(json.dumps(out))
                else: 
                    print("[+] Từ chối đăng ký " , ws , " dưới tên " , username , " | Lý do: WrongFormatName")
                    out = {
                        'type': 'register',
                        'name': username,
                        'status': False,
                        'reason': "WrongFormatName"
                    }
                    ws.send(json.dumps(out))

            if (data['type'] == "send"):
                name = ""
                try:
                    name = data[find(socks, 'socket', ws)]['name']
                except: 
                    print("[S] Từ chối gửi tin ",ws,": " , " | Lý do: UnknownRegister")
                    output = {
                        "type": "send",
                        "status": False,
                        "reason": "UnknownRegister"
                    }
                    ws.send(json.dumps(output))

                content = ""
                try:
                    content = data['content']
                except:
                    print("[S] Từ chối gửi tin ",name," (",ws,"): " , " | Lý do: WrongFormatJSON")
                    output = {
                        "type": "send",
                        "username": name,
                        "status": False,
                        "reason":"WrongFormatJSON"
                    }
                    ws.send(json.dumps(output))

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
                            "type": "send",
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
                                client['socket'].send(json.dumps(rec))

                    except Exception as e:
                        print("[S] LỖI KHI GỬI TIN ",name," (",ws,"): " , content , " | Lý do: ")
                        print(e)
                        output = {
                            "type": "send",
                            "username": name,
                            "content": content,
                            "status": False,
                            "reason": "ErrorWhenSend"
                        }
                        ws.send(json.dumps(output))
                else:
                    print("[S] Từ chối gửi tin ",name," (",ws,"): " , content , " | Lý do: WrongFormatContent")
                    output = {
                            "type": "send",
                            "username": name,
                            "content": content,
                            "status": False,
                            "reason":"WrongFormatContent"
                        }
                    ws.send(json.dumps(output))
                    
            if (data['type'] == "get"):
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
                            "type": "get",
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
                        print("[G] LỖI KHI CUNG CẤP TOÀN BỘ TIN NHẮN, NGƯỜI ONLINE CHO ",username," (",ws,")" , " | Lý do: ")
                        print(e)
                        output = {
                            "type": "get",
                            "name": username,
                            "status": False,
                            "reason": "ErrorWhenGet"
                        }
                    ws.send(json.dumps(output))
                else:
                    print("[G] Từ chối cung cấp toàn bộ tin nhắn, người online cho ",ws," | Lý do: UnknownRegister")
                    output = {
                        "type": "get",
                        "status": False,
                        "reason": "UnknownRegister"
                    }
                    ws.send(json.dumps(output))
    except: 
        number = find(socks, 'socket', ws)
        if (number != None):
            print("[<-] Đã rời khỏi Chatbox và ngắt kết nối Socket" , socks[number]['name'] , " (" , socks[number]['socket'] , ")")
            socks.remove(socks[number])
        else:
            print("[<-] Đã ngắt kết nối Socket: " ,ws)

app.run()