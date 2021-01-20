import time
from libs.MQConnection import MQConnection
from libs.EventosMF import EventosMF

mqconn = MQConnection()
ev = EventosMF()
ev.set_url("https://dev94674.service-now.com/api/global/em/jsonv2")

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
            ev.post(events)

        time.sleep(30)
    except KeyboardInterrupt: 
        keep_alive = False

mqconn.CloseQueue()

mqconn.CloseConnection()
