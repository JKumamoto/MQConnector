import time
from libs.MQConnection import MQConnection

mqconn = MQConnection()

host = 'SCQTD0029CLD'
port = '5000'
queue_manager = 'SMD1041CTO'
channel = 'D1041CTO.P_OC2_DEV'
#user = 'usutivo@itau'

conn = '%s(%s)' % (host, port)

mqconn.Connect(queue_manager, channel, conn)

queues = list()
queues.append("RP.QRP.OC2.MONIT.SECA2")

mqconn.OpenQueue(queues)

while True:
    [print(i) for i in (mqconn.MQGET())]
    time.sleep(10)

mqconn.CloseQueue()

mqconn.CloseConnection()

