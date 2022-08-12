import json
from flask import Flask
from flask_sock import Sock
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

@sock.route('/connect')
def connect(ws):
    socks.append(ws)
    try:
        while True:
            receive = ws.receive()
            data = json.loads(receive)
            
            if (data['type'] == "send"):
                name = data['data']['name']
                content = data['data']['content']
                if ((len(name)>0) & (len(name)<=100) & (len(content)>0) & (len(content)<=4000)):
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
                        print("["+timestamp.strftime("%d/%m/%Y, %H:%M:%S")+"] "+name+": "+content)

                        #*Return client send
                        output = {
                            "type": "send",
                            "status": True,
                            "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                        }
                        ws.send(json.dumps(output))

                        #*Update another Client
                        for client in socks:
                            if (client != ws):
                                client.send(input)
                    except:
                        output = {
                            "type": "send",
                            "status": False,
                        }
                        ws.send(json.dumps(output))
                else:
                    output = {
                            "type": "send",
                            "status": False,
                        }
                    ws.send(json.dumps(output))
                    
            if (data['type'] == "get"):
                output = {}
                try:
                    dat = json.loads(get())
                    output = {
                        "type": "get",
                        "status": True,
                        "data": dat
                    }
                except:
                    output = {
                        "type": "get",
                        "status": False
                    }
                ws.send(json.dumps(output))
    except:
        socks.remove(ws)

app.run()