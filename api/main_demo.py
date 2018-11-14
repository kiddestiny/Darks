import flask
from flask_cors import CORS
from datetime import datetime
from sse import Publisher
import pan_demo

app = flask.Flask(__name__)
CORS(app,supports_credentials=True)
publisher = Publisher()

@app.route('/subscribe')
def subscribe():
    '''
    sse subscribe
    '''
    return flask.Response(publisher.subscribe(),
                          content_type='text/event-stream')

@app.route('/gotnewdebit')
def root():
    '''
    sse publish
    '''
    debitid = flask.request.args.get('debitid')
    # 执行逻辑
    res = pan.run(debitid=int(debitid))
    publisher.publish(res)
    return """
<html>
    <body>
        已发布 debitid: {} 通过 /subscribe 订阅消息
    </body>
</html>
""".format(debitid)

@app.route('/pushdata')
def demo():
    '''
    sse publish
    '''
    address = flask.request.args.get('address')
    gender = flask.request.args.get('gender')
    user_name = flask.request.args.get('user_name')
    res = pan.run_demo(user_name,gender,address)
    
    # 执行逻辑
    publisher.publish(res)
    return """
<html>
    <body>
        已发布 demo: {} 通过 /subscribe 订阅消息
    </body>
</html>
""".format(address)

# @app.route('/getdebitinfo')
# def getdebitinfo():
#     debitid = flask.request.args.get('debitid')
#     pan.shop_transform_one()



app.run(host='127.0.0.1',debug=True,port=8098,threaded=True)
# http://127.0.0.1:8098/pushdata?address=安徽省合肥市当涂东路与望江路交口星隆国际1栋2单元1305室&gender=男&user_name=王阿三
# /data/anaconda/bin/python /data/anaconda/bin/gunicorn -w 1 -b 127.0.0.1:8098 -n ssescreen -k gevent main:app --reload -t 500 -D --access-logfile /data/log/gunicorn_sse.log


