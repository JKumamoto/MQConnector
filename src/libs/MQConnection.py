import pymqi
from libs.Logger import Logger

class MQConnection():
    
    def __init__(self):
        self.qmgr = None
        self.md = pymqi.MD()
        self.gmo = pymqi.GMO()
        self.gmo.Options = self.gmo.Options | pymqi.CMQC.MQGMO_NO_PROPERTIES | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        self.queues = list()

        self.log = Logger()

    def Connect(self, queue_manager, channel, conn, user, password=None):
        self.log.info("Abrindo Conexao com o MQ")
        try:
            self.qmgr = pymqi.connect(queue_manager, channel, conn, user, password)
        except pymqi.MQMIError as e:
            raise
        self.log.info("Conexao aberta com sucesso")

        return self
    
    def CloseConnection(self):
        self.log.info("Fechando Conexao com o MQ")
        try:
            self.qmgr.disconnect()
        except pymqi.MQMIError as e:
            raise

        self.log.info("Conexao fechada com sucesso")
        return self

    def OpenQueue(self, queues):
        self.log.info("Abrindo filas")
        try:
            for q in queues:
                self.queues.append(pymqi.Queue(self.qmgr, q))
        except pymqi.MQMIError as e:
            raise

        self.log.info("Fila aberta com sucesso")
        return self

    def CloseQueue(self):
        self.log.info("Abrindo Conexao com o MQ")
        try:
            for q in self.queues:
                q.close()
        except pymqi.MQMIError as e:
            raise

        return self

    def MQGET(self):
        self.log.info("MQGET")
        messages = list()
        for q in self.queues:
            try:
                messages.append(q.get(None, self.md, self.gmo))

                self.md.MsgId = pymqi.CMQC.MQMI_NONE
                self.md.CorrelId = pymqi.CMQC.MQCI_NONE
                self.md.GroupId = pymqi.CMQC.MQGI_NONE
            except pymqi.MQMIError as e:
                if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                    # No messages, that's OK, we can ignore it.
                    self.log.info("no messages")
                    pass
                else:
                    # Some other error condition.
                    raise

        return messages

