import flask
from flask_cors import CORS
from datetime import datetime
from sse import Publisher

app = flask.Flask(__name__)
CORS(app,supports_credentials=True)
publisher = Publisher()

@app.route('/subscribe')
def subscribe():
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

app.run(debug=True,port=8877,threaded=True)
