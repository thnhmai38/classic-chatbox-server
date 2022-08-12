import json
from flask import Flask
from flask_sock import Sock, Server
import datetime

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

@sock.route('/')
def connect(ws: Server):
    print("[->] Kết nối Socket mới: " + ws)
    try:
        while True:
            receive = ws.receive()
            data = json.loads(receive)
            
            if (data['type'] == "register"):
                try:
                    username = data['name']
                    if ((len(name)>0) & (len(name)<=100)):
                        try:
                            if (find(socks, 'name', username) == None):
                                reginfo = {
                                    "name": username,
                                    "socket": ws
                                }
                                socks.append(reginfo)
                                print("[+] Đã đăng ký " + ws + " dưới tên " + username)
                                out = {
                                    'type': 'register',
                                    'name': username,
                                    'status': True
                                }
                                ws.send(out)
                            else:
                                print("[+] Từ chối đăng ký " + ws + " dưới tên " + username + " | Lý do: NameAlreadyUsed")
                                out = {
                                    'type': 'register',
                                    'name': username,
                                    'status': False,
                                    'reason': "NameAlreadyUsed"
                                }
                                ws.send(out)
                        except Exception as e:
                            print("[+] LỖI KHI ĐĂNG KÝ " + ws + " dưới tên " + username + " | Lý do: "+e)
                            out = {
                                'type': 'register',
                                'name': username,
                                'status': False,
                                'reason': "ErrorWhenRegister"
                            }
                            ws.send(out)
                    else: 
                        print("[+] Từ chối đăng ký " + ws + " dưới tên " + username + " | Lý do: WrongFormatName")
                        out = {
                            'type': 'register',
                            'name': username,
                            'status': False,
                            'reason': "WrongFormatName"
                        }
                        ws.send(out)
                except:
                    print("[+] Từ chối đăng ký " + ws + " dưới tên " + username + " | Lý do: WrongFormatJSON")
                    out = {
                        'type': 'register',
                        'name': username,
                        'status': False,
                        'reason': "WrongFormatJSON"
                    }
                    ws.send(out)


            if (data['type'] == "send"):
                try:
                    name = data[find(socks, 'socket', ws)]['name']
                    try:
                        content = data['content']
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
                                print("[S] ["+timestamp.strftime("%d/%m/%Y, %H:%M:%S")+"] Đã gửi tin: "+name+ " ("+ws+"): "+ content)

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
                                input = {
                                    "type": "receive",
                                    "name": name,
                                    "content": content,
                                    "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                                }   
                                for client in socks:
                                    if (client['ws'] != ws):
                                        client['ws'].send(input)
                            except Exception as e:
                                print("[S] LỖI KHI GỬI TIN "+username+" ("+ws+"): " + content + " | Lý do: " + e)
                                output = {
                                    "type": "send",
                                    "username": username,
                                    "content": content,
                                    "status": False,
                                    "reason": "ErrorWhenSend"
                                }
                                ws.send(json.dumps(output))
                        else:
                            print("[S] Từ chối gửi tin "+username+" ("+ws+"): " + content + " | Lý do: WrongFormatContent")
                            output = {
                                    "type": "send",
                                    "username": username,
                                    "content": content,
                                    "status": False,
                                    "reason":"WrongFormatContent"
                                }
                            ws.send(json.dumps(output))
                    except:
                        print("[S] Từ chối gửi tin "+username+" ("+ws+"): " + " | Lý do: WrongFormatJSON")
                        output = {
                            "type": "send",
                            "username": username,
                            "status": False,
                            "reason":"WrongFormatJSON"
                        }
                        ws.send(json.dumps(output))
                except: 
                    print("[S] Từ chối gửi tin "+ws+": " + " | Lý do: UnknownRegister")
                    output = {
                        "type": "send",
                        "status": False,
                        "reason": "UnknownRegister"
                    }
                    ws.send(json.dumps(output))
                    
            if (data['type'] == "get"):
                number = find(socks, 'ws', ws)
                if (number != None):
                    output = {}
                    try:
                        print("[G] Cung cấp toàn bộ tin nhắn cho "+username+" ("+ws+")")
                        dat = json.loads(get())
                        output = {
                            "type": "get",
                            "status": True,
                            "name": socks[number]['name'],
                            "data": dat
                        }
                    except Exception as e:
                        print("[G] LỖI KHI CUNG CẤP TOÀN BỘ TIN NHẮN CHO "+username+" ("+ws+")" + " | Lý do: " + e)
                        output = {
                            "type": "get",
                            "status": False,
                            "reason": "ErrorWhenGet"
                        }
                    ws.send(json.dumps(output))
                else:
                    print("[G] Từ chối cung cấp toàn bộ tin nhắn cho "+ws+" | Lý do: UnknownRegister")
                    output = {
                        "type": "get",
                        "status": False,
                        "reason": "UnknownRegister"
                    }
                    ws.send(json.dumps(output))
    except: 
        number = find(socks, 'ws', ws)
        if (number != None):
            print("[<-] " + socks[number]['name'] + " (" + socks[number]['ws'] + ") đã rời khỏi Chatbox và ngắt kết nối")
            socks.remove(find(socks, 'ws', ws))
        else:
            print("[<-] " +ws+ "đã ngắt kết nối")

app.run()