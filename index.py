from flask import Flask, request, make_response, render_template
import json
import datetime

app = Flask(__name__)

@app.route("/send/", methods=['GET'])
def send():
    name = request.args['name']
    content = request.args['content']
    response = make_response()
    if ((len(name)>0) & (len(name)<=100) & (len(content)>0) & (len(content)<=4000)):
        try:
            #*Read old data 
            file = open("data.json", encoding='utf_8')
            if (file.read().rstrip()==''):
                up = open("data.json", mode='w', encoding='utf_8')
                up.write('[]')
                up.close()
            file.close()
            file = open("data.json", encoding='utf_8')
            msg = json.loads(file.read().rstrip())
            file.close()

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

            #*Return client
            ject = {
                "sent" : True,
                "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S")
            }
        except:
            ject = {
                'sent':False
            }
    else: 
        ject = {
            'sent':False
        }
    response.set_data(json.dumps(ject))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/get/", methods=['GET'])
def getslash():
    response = make_response()
    ject = {}
    try:
        file = open("data.json", encoding='utf_8')
        if (file.read().rstrip()==''):
            up = open("data.json", mode='w', encoding='utf_8')
            up.write('[]')
            up.close()
        file.close()
        file = open("data.json", encoding='utf_8')
        data = json.loads(file.read().rstrip())
        file.close()
        ject = {
            "got" : True,
            "data" : data
        }
    except:
        ject = {"got" : False}
    response.set_data(json.dumps(ject))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def index():
    return render_template('main.html') #Thanks https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists

app.run()