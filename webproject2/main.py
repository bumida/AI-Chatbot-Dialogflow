#flask 패키지에서 FLASK를 임포트
import json
import os
from flask import Flask, request, render_template, make_response, redirect, url_for
from google.cloud import dialogflow as dfw
from google.api_core.exceptions import InvalidArgument
from flask_ngrok import run_with_ngrok
from collections import OrderedDict


#FLASK 객체 app을 선언
from statsmodels.graphics.tukeyplot import results

app = Flask(__name__)
run_with_ngrok(app)
@app.route('/', methods=['GET','POST'])
def index_page_landing():
    print('들어옴')
    if request.method == "POST":
        pass
    else:
        print('들어옴2')
        dialog = conversation_chatbot()
        return render_template('chat.html', context=dialog)

#terminal에서 대화형 챗봇 흉내내기
def conversation_chatbot():
    keys = []
    values = []
    print('들어옴3')
    #requestText = request.args.get['item_id']
    #print(requestText)
    print('들어옴4')
    requestText = input("request text : ")
    respText = ""
    while(requestText != 'quit'):
        respText = chatbot_request(requestText)
        keys.append(requestText) #request text
        values.append(respText) #response text

        #requestText = request.form['item_id']
        requestText = input("request text : ")

    dialog = OrderedDict({key:val for key, val in zip(keys, values)})
    print(dialog)
    return dialog

def chatbot_request(txtInput):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'web-project-tx9a-8a11ea23176c.json'

    DIALOGFLOW_PROJECT_ID = 'web-project-tx9a'
    DIALOGFLOW_LANGUAGE_CODE = 'ko'
    SESSION_ID = 'mine'


    text_to_be_analyzed = txtInput

    session_client = dfw.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dfw.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dfw.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    print("Query Text : ", response.query_result.query_text)
    print("Detected intent : ", response.query_result.intent.display_name)
    print("Detected intent confidence : ", response.query_result.intent_detection_confidence)
    print("Fulfillment text : ", response.query_result.fulfillment_text) #<----

    return response.query_result.fulfillment_text

# route()를 사용해 웹페이지와 해당 페이지에서 작동할 함수를 매칭
@app.route('/index')
def hello_world():

    return render_template('index.html')


@app.route('/chat')
def chat_world():

    return render_template('renewal_index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    return make_response(json.dumps(results()))

def results():
    req = request.get_json(force=True)
    print(req)
    queryText = req.get("queryResult").get("queryText")
    print(queryText)


    respText = {
        "fulfillmentMessages":[
            {
                "text":{
                    "text":[
                        "This is a response from webhook!!!"
                    ]
                }
            }


        ]
    }
    return respText



#test
@app.route('/test')
def test():
    color = 'red'
    colors = ['red', 'green', 'blue']
    blogger = {'name': 'jvvp', 'eloc':'songpa'}

    return render_template('test.html', d1=color, d2=colors, d3=blogger)



# 모듈명이 main일 때만 실행하도록 조건문을 추가
if __name__ == '__main__':

    app.run()
