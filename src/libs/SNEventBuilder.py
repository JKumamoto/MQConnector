class SNEventBuilder():

    def __init__(self):
        self.source = ""
        self.event_class = ""
        self.resource = ""
        self.metric_name = ""
        self.node = ""
        self.type = ""
        self.time_of_event = ""
        self.severity = ""
        self.description = ""
        self.additional_info = ""

    def set_source(self, source_):
        self.source = source_
        return self

    def set_event_class(self, event_class_):
        self.event_class = event_class_
        return self

    def set_resource(self, resource_):
        self.resource = resource_
        return self

    def set_metric_name(self, metric_name_):
        self.metric_name = metric_name_
        return self

    def set_node(self, node_):
        self.node = node_
        return self

    def set_type(self, type_):
        self.type = type_
        return self

    def set_time_of_event(self, time_of_event_):
        self.time_of_event = time_of_event_
        return self

    def set_severity(self, severity_):
        self.severity = severity_
        return self

    def set_description(self, description_):
        self.description = description_
        return self

    def set_additional_info(self, additional_info_):
        self.additional_info = additional_info_
        return self

    @property
    def build(self):
        self.json_ = {
            "records" : [
               {
                   "source" : self.source,
                   "event_class" : self.event_class,
                   "resource" : self.resource,
                   "node" : self.node,
                   "metric_name" : self.metric_name,
                   "type" : self.type,
                   "time_of_event" : self.time_of_event,
                   "severity" : self.severity,
                   "description" : self.description,
                   "additional_info" : self.additional_info
                }
            ]
        }
        return self.json_

