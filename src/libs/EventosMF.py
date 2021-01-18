import pandas as pd
from datetime import datetime, timezone
from requests import request
from libs.SNEventBuilder import SNEventBuilder

class EventosMF():

    def __init__(self):
        self.authorization = ""
        self.method = "POST"
        self.headers = {
                'Content-Type': 'application/json',
                'cache-control': 'no-cache',
                'charset': 'utf-8',
                'Authorization': self.authorization
                }

    def set_url(self, url_):
        self.url = url_
        return self

    def post(self, payload):
        response = request(self.method, self.url, data=payload, headers=self.headers)
        return response

    def parser(self, msg):
        x = [None] * len(msg)
        for i in range(len(msg)):
            x[i] = msg[i].split(";")

        df = pd.DataFrame(x, columns=['Visao', 'Severity', 'Status', 'Data', 'Sysplex', 'Sistema', 'Origem',
                                        'TRecurso', 'Recurso', 'Grupo', 'Help', 'MsgID', 'Texto'])

        df['date_gmt'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        return df

    def EventFactory(self, dict_events):
        list_events = list()

        for record in range(len(dict_events)):
            summary = []
            identifier = []
            if dict_events[record]['Grupo'] == "Mainview":
                summary = dict_events[record]['Origem'] + '-' + dict_events[record]['TRecurso'] + '-' + dict_events[record]['MsgID'] + '-' + dict_events[record]['Texto']
                identifier = dict_events[record]['Sistema'] + '.' + dict_events[record]['Origem'] + '.' + dict_events[record]['Recurso'] + '.' + dict_events[record]['MsgID'] + '.' + dict_events[record]['Visao']
            else:
                summary = dict_events[record]['Origem'] + '-' + dict_events[record]['TRecurso'] + '-' + dict_events[record]['Texto']
                identifier = dict_events[record]['Sistema'] + '.' + dict_events[record]['Origem'] + '.' + dict_events[record]['Recurso'] + '.' + dict_events[record]['MsgID']

            sn_records_gen = SNEventBuilder()
            sn_records_gen.set_source("ETL Eventos Mainframe")\
                          .set_resource(dict_events[record]["Recurso"])\
                          .set_metric_name(dict_events[record]["Help"])\
                          .set_node(dict_events[record]["Sistema"])\
                          .set_type(dict_events[record]["Grupo"])\
                          .set_time_of_event(dict_events[record]["date_gmt"])\
                          .set_severity(dict_events[record]["Severity"])\
                          .set_description(summary)\
                          .set_additional_info('{"identifier":"' + identifier + '", "netcool_severity":"' +
                                                dict_events[record]["Severity"] +
                                                '", "agent": "ETL Eventos Mainframe", "last_occurence": "' +
                                                dict_events[record]["date_gmt"] + '", "alert_group": "' +
                                                dict_events[record]["Grupo"] + '", "Resumo": "' + summary +
                                                '", "alert_key": "' + dict_events[record]["TRecurso"] +':' +
                                                dict_events[record]["Recurso"] + ':' +
                                                dict_events[record]["Sysplex"] + '", "MFVisao": "' +
                                                dict_events[record]["Visao"] + '", "node_alias": "' +
                                                dict_events[record]["Sistema"] + '", "kbc01": "' +
                                                dict_events[record]["Help"] + '", "kbc03": "' +
                                                dict_events[record]["Recurso"] + '", "kbc02": "' +
                                                dict_events[record]["Origem"] + '"}')

            list_events.append(sn_records_gen.build)

        return list_events

