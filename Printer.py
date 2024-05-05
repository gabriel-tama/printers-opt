class Printer:
    def __init__(self,name,a , latitude, longitude):
        self.name = name
        self.a = a
        self.latitude = latitude
        self.longitude = longitude
        self.time_spent=0
        self.item_has = []
        self.timeseries = []

    def set_time_spent(self,time_spent):
        self.time_spent = time_spent

    def set_item(self,item_has):
        self.item_has = item_has

    def set_timeseries(self):
        time_span = []
        cumulative_time = 0

        for value in self.item_has:
            time_span.append([cumulative_time, value.value])
            cumulative_time += value.value

        self.timeseries=time_span
