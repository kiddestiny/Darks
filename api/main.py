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
    pan.run()
    publisher.publish(debitid)
    return """
<html>
    <body>
        已发布 debitid: {} 通过 /subscribe 订阅消息
    </body>
</html>
""".format(debitid)

app.run(host='127.0.0.1',debug=True,port=8098,threaded=True)
