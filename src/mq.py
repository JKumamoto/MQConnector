import time
from libs.MQConnection import MQConnection

mqconn = MQConnection()

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

while True:
    [print(i) for i in (mqconn.MQGET())]
    time.sleep(10)

mqconn.CloseQueue()

mqconn.CloseConnection()

