import time
import json
from libs.MQConnection import MQConnection
from libs.EventosMF import EventosMF

mqconn = MQConnection()
ev = EventosMF()
ev.set_url("http://0.0.0.0:5000/echo")

host = '172.17.0.2'
port = '1414'
queue_manager = 'QM1'
channel = 'DEV.APP.SVRCONN'
user = 'app'
password = 'passw0rd'

conn = '%s(%s)' % (host, port)

mqconn.Connect(queue_manager, channel, conn, user, password)

queues = list()
queues.append("DEV.QUEUE.1")
queues.append("DEV.QUEUE.2")

mqconn.OpenQueue(queues)

keep_alive = True
while keep_alive:
    try:
        msg = mqconn.MQGET()
        if msg:
            df = ev.parser(msg)
            dict_events = df.to_dict(orient='records')
            events = ev.EventFactory(dict_events)
            #ev.post(json.dumps(events))

        time.sleep(10)
    except KeyboardInterrupt:
        keep_alive = False

mqconn.CloseQueue()

mqconn.CloseConnection()

