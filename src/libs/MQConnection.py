import pymqi
from libs.Logger import Logger

class MQConnection():
    
    def __init__(self):
        self.qmgr = None
        self.md = pymqi.MD()
        self.gmo = pymqi.GMO()
        self.gmo.Options = self.gmo.Options | pymqi.CMQC.MQGMO_NO_PROPERTIES | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        self.queues = list()

        self.logger = Logger()

    def Connect(self, queue_manager, channel, conn, user=None, password=None):
        self.logger.log("INFO", __name__, "Abrindo Conexao com o MQ")
        try:
            self.qmgr = pymqi.connect(queue_manager, channel, conn, user, password)
        except pymqi.MQMIError as e:
            self.logger.log("CRITICAL", __name__, f'Comp: {e.comp}, Reason {e.reason}')
            raise
            
        self.logger.log("INFO", __name__, "Conexao aberta com sucesso")

        return self
    
    def CloseConnection(self):
        self.logger.log("INFO", __name__, "Fechando Conexao com o MQ")
        try:
            self.qmgr.disconnect()
        except pymqi.MQMIError as e:
            self.logger.log("CRITICAL", __name__, f'Comp: {e.comp}, Reason {e.reason}')
            raise

        self.logger.log("INFO", __name__, "Conexao fechada com sucesso")
        return self

    def OpenQueue(self, queues):
        self.logger.log("INFO", __name__, "Abrindo filas")
        try:
            for q in queues:
                self.queues.append(pymqi.Queue(self.qmgr, q))
        except pymqi.MQMIError as e:
            self.logger.log("CRITICAL", __name__, f'Comp: {e.comp}, Reason {e.reason}')
            raise

        self.logger.log("INFO", __name__, "Fila aberta com sucesso")
        return self

    def CloseQueue(self):
        self.logger.log("INFO", __name__, "Abrindo Conexao com o MQ")
        try:
            for q in self.queues:
                q.close()
        except pymqi.MQMIError as e:
            self.logger.log("CRITICAL", __name__, f'Comp: {e.comp}, Reason {e.reason}')
            raise

        return self

    def MQGET(self):
        self.logger.log("INFO", __name__, "MQGET")
        messages = list()
        for q in self.queues:
            try:
                msg = q.get(None, self.md, self.gmo).decode('utf8')
                self.logger.log("INFO", __name__, f'Mensagem do MQ: {msg}')
                messages.append(msg)

                self.md.MsgId = pymqi.CMQC.MQMI_NONE
                self.md.CorrelId = pymqi.CMQC.MQCI_NONE
                self.md.GroupId = pymqi.CMQC.MQGI_NONE
            except pymqi.MQMIError as e:
                if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                    # No messages, that's OK, we can ignore it.
                    self.logger.log("INFO", __name__, "No Messages")
                    pass
                else:
                    # Some other error condition.
                    self.logger.log("CRITICAL", __name__, f'Comp: {e.comp}, Reason {e.reason}')
                    raise

        return messages

