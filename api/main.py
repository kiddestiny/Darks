import flask
from flask_cors import CORS
from datetime import datetime
from sse import Publisher
import pan

app = flask.Flask(__name__)
CORS(app,supports_credentials=True)
publisher = Publisher()

@app.route('/subscribe')
def subscribe():
    # 调用pan 查询geo信息和构造json输出
    # pan.run()
    # pan.gotnewdebit()
    # exit()
    print("......................")
    return flask.Response(publisher.subscribe(),
                          content_type='text/event-stream')

@app.route('/gotnewdebit')
def root():
    # ip = flask.request.remote_addr
    # publisher.publish('New visit from {} at {}!'.format(ip, datetime.now()))
    debitid = flask.request.args.get('debitid')
    publisher.publish(debitid)
    return """
<html>
    <body>
        已发布 debitid: {} 通过 /subscribe 订阅消息
    </body>
</html>
""".format(debitid)

app.run(host='192.168.0.74',debug=True,port=8080,threaded=True)
