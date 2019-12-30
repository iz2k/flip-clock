from wtforms import Form, StringField, IntegerField, BooleanField, HiddenField, SubmitField
from lxml import etree
from tools import str2bool



class AlarmPeriodic:
    def __init__(self):
        self.enable = False
        self.weekday = []
        for i in range(7):
            self.weekday.append(False)

    def parseForm(self, form):
        self.enable = form.alarm_period_enable.data
        self.weekday[0] = form.alarm_period_monday.data
        self.weekday[1] = form.alarm_period_tuesday.data
        self.weekday[2] = form.alarm_period_wednesday.data
        self.weekday[3] = form.alarm_period_thursday.data
        self.weekday[4] = form.alarm_period_friday.data
        self.weekday[5] = form.alarm_period_saturday.data
        self.weekday[6] = form.alarm_period_sunday.data

    def parseXML(self, xml):
        for ch in xml.getchildren():
            if ch.tag == 'enable':
                self.enable = str2bool(ch.text)
            if ch.tag == 'monday':
                self.weekday[0] = str2bool(ch.text)
            if ch.tag == 'tuesday':
                self.weekday[1] = str2bool(ch.text)
            if ch.tag == 'wednesday':
                self.weekday[2] = str2bool(ch.text)
            if ch.tag == 'thursday':
                self.weekday[3] = str2bool(ch.text)
            if ch.tag == 'friday':
                self.weekday[4] = str2bool(ch.text)
            if ch.tag == 'saturday':
                self.weekday[5] = str2bool(ch.text)
            if ch.tag == 'sunday':
                self.weekday[6] = str2bool(ch.text)


class AlarmSource:
    def __init__(self):
        self.type = ''
        self.item = ''
        self.randomize = False

    def parseForm(self, form):
        self.type = form.alarm_src_type.data
        self.item = form.alarm_src_item.data
        self.randomize = form.alarm_src_random.data

    def parseXML(self, xml):
        for ch in xml.getchildren():
            if ch.tag == 'type':
                self.type = ch.text
            if ch.tag == 'item':
                self.item = ch.text
            if ch.tag == 'randomize':
                self.randomize = str2bool(ch.text)


class AlarmVolume:
    def __init__(self):
        self.start = 50
        self.end = 50
        self.ramptime = 0

    def parseForm(self, form):
        self.start = form.alarm_vol_start.data
        self.end = form.alarm_vol_end.data
        self.ramptime = form.alarm_vol_ramptime.data

    def parseXML(self, xml):
        for ch in xml.getchildren():
            if ch.tag == 'start':
                self.start = int(ch.text)
            if ch.tag == 'end':
                self.end = int(ch.text)
            if ch.tag == 'ramptime':
                self.ramptime = int(ch.text)


class AlarmSnooze:
    def __init__(self):
        self.enable = False
        self.time = 10

    def parseForm(self, form):
        self.enable = form.alarm_snz_enable.data
        self.time = form.alarm_snz_time.data

    def parseXML(self, xml):
        for ch in xml.getchildren():
            if ch.tag == 'enable':
                self.enable = str2bool(ch.text)
            if ch.tag == 'time':
                self.time = int(ch.text)


class AlarmWeather:
    def __init__(self):
        self.enable = False
        self.greeting = ''
        self.delay = 1

    def parseForm(self, form):
        self.enable = form.alarm_wth_enable.data
        self.greeting = form.alarm_wth_greeting.data
        self.delay = form.alarm_wth_delay.data

    def parseXML(self, xml):
        for ch in xml.getchildren():
            if ch.tag == 'enable':
                self.enable = str2bool(ch.text)
            if ch.tag == 'greeting':
                self.greeting = ch.text
            if ch.tag == 'delay':
                self.delay = int(ch.text)


class Alarm:
    name = ''
    hour = 0
    minute = 0
    periodic = AlarmPeriodic()
    source = AlarmSource()
    volume = AlarmVolume()
    snooze = AlarmSnooze()
    weather = AlarmWeather()

    def __init__(self, form=None, xml=None):
        if form != None:
            self.parseForm(form)
        if xml != None:
            self.parseXML(xml)

    def parseForm(self, form):
        self.name = form.name.data
        self.hour = form.hour.data
        self.minute = form.minute.data
        self.periodic.parseForm(form)
        self.source.parseForm(form)
        self.volume.parseForm(form)
        self.snooze.parseForm(form)
        self.weather.parseForm(form)

    def parseXML(self, xml):
        for ch in xml.getchildren():
            if ch.tag == 'name':
                self.name = ch.text
            if ch.tag == 'hour':
                self.hour = int(ch.text)
            if ch.tag == 'minute':
                self.minute = int(ch.text)
            if ch.tag == 'periodic':
                self.periodic.parseXML(ch)
            if ch.tag == 'source':
                self.source.parseXML(ch)
            if ch.tag == 'volume':
                self.volume.parseXML(ch)
            if ch.tag == 'snooze':
                self.snooze.parseXML(ch)
            if ch.tag == 'weather':
                self.weather.parseXML(ch)


class AlarmForm(Form):
    name = StringField(label='Name')
    hour = IntegerField(label='Hour')
    minute = IntegerField(label='Minute')
    alarm_period_enable = BooleanField(label='Enable periodic alarm')
    alarm_period_monday = BooleanField(label='Monday')
    alarm_period_tuesday = BooleanField(label='Tuesday')
    alarm_period_wednesday = BooleanField(label='Wednesday')
    alarm_period_thursday = BooleanField(label='Thursday')
    alarm_period_friday = BooleanField(label='Friday')
    alarm_period_saturday = BooleanField(label='Saturday')
    alarm_period_sunday = BooleanField(label='Sunday')
    alarm_src_type = StringField(label='Source type')
    alarm_src_item = StringField(label='Source item')
    alarm_src_random = BooleanField(label='random')
    alarm_vol_start = IntegerField(label='Start volume (%)')
    alarm_vol_end = IntegerField(label='End volume (%)')
    alarm_vol_ramptime = IntegerField(label='Ramptime (min)')
    alarm_snz_enable = BooleanField(label='Enable snooze')
    alarm_snz_time = IntegerField(label='Snooze time (min)')
    alarm_wth_enable = BooleanField(label='Enable weather forecast')
    alarm_wth_greeting = StringField(label='Greeting')
    alarm_wth_delay = IntegerField(label='Weather delay (min)')
    idx = HiddenField()
    delete = SubmitField(label='Delete')
    update = SubmitField(label='Update')
    new = SubmitField(label='New')

    def readobject(self, alarm):
        self.name.data = alarm.name
        self.hour.data = alarm.hour
        self.minute.data = alarm.minute
        self.alarm_period_enable.data = alarm.periodic.enable
        self.alarm_period_monday.data = alarm.periodic.weekday[0]
        self.alarm_period_tuesday.data = alarm.periodic.weekday[1]
        self.alarm_period_wednesday.data = alarm.periodic.weekday[2]
        self.alarm_period_thursday.data = alarm.periodic.weekday[3]
        self.alarm_period_friday.data = alarm.periodic.weekday[4]
        self.alarm_period_saturday.data = alarm.periodic.weekday[5]
        self.alarm_period_sunday.data = alarm.periodic.weekday[6]
        self.alarm_src_type.data = alarm.source.type
        self.alarm_src_item.data = alarm.source.item
        self.alarm_src_random.data = alarm.source.randomize
        self.alarm_vol_start.data = alarm.volume.start
        self.alarm_vol_end.data = alarm.volume.end
        self.alarm_vol_ramptime.data = alarm.volume.ramptime
        self.alarm_snz_enable.data = alarm.snooze.enable
        self.alarm_snz_time.data = alarm.snooze.time
        self.alarm_wth_enable.data = alarm.weather.enable
        self.alarm_wth_greeting.data = alarm.weather.greeting
        self.alarm_wth_delay.data = alarm.weather.delay


def save_alarm_list(alarms, filename):
    # Create main element
    alist = etree.Element('alarms')
    for alarm in alarms:
        # Create alarm element
        al = etree.SubElement(alist, 'alarm')
        # Main tags
        se = etree.SubElement(al, 'name')
        se.text = alarm.name
        se = etree.SubElement(al, 'hour')
        se.text = str(alarm.hour)
        se = etree.SubElement(al, 'minute')
        se.text = str(alarm.minute)
        # Periodic tags
        periodic = etree.SubElement(al, 'periodic')
        se = etree.SubElement(periodic, 'enable')
        se.text = str(alarm.periodic.enable)
        se = etree.SubElement(periodic, 'monday')
        se.text = str(alarm.periodic.weekday[0])
        se = etree.SubElement(periodic, 'tuesday')
        se.text = str(alarm.periodic.weekday[1])
        se = etree.SubElement(periodic, 'wednesday')
        se.text = str(alarm.periodic.weekday[2])
        se = etree.SubElement(periodic, 'thursday')
        se.text = str(alarm.periodic.weekday[3])
        se = etree.SubElement(periodic, 'friday')
        se.text = str(alarm.periodic.weekday[4])
        se = etree.SubElement(periodic, 'saturday')
        se.text = str(alarm.periodic.weekday[5])
        se = etree.SubElement(periodic, 'sunday')
        se.text = str(alarm.periodic.weekday[6])
        # Source tags
        source = etree.SubElement(al, 'source')
        se = etree.SubElement(source, 'type')
        se.text = alarm.source.type
        se = etree.SubElement(source, 'item')
        se.text = alarm.source.item
        se = etree.SubElement(source, 'randomize')
        se.text = str(alarm.source.randomize)
        # Volume tags
        volume = etree.SubElement(al, 'volume')
        se = etree.SubElement(volume, 'start')
        se.text = str(alarm.volume.start)
        se = etree.SubElement(volume, 'end')
        se.text = str(alarm.volume.end)
        se = etree.SubElement(volume, 'ramptime')
        se.text = str(alarm.volume.ramptime)
        # Snooze tags
        snooze = etree.SubElement(al, 'snooze')
        se = etree.SubElement(snooze, 'enable')
        se.text = str(alarm.snooze.enable)
        se = etree.SubElement(snooze, 'time')
        se.text = str(alarm.snooze.time)
        # Weather tags
        weather = etree.SubElement(al, 'weather')
        se = etree.SubElement(weather, 'enable')
        se.text = str(alarm.weather.enable)
        se = etree.SubElement(weather, 'greeting')
        se.text = alarm.weather.greeting
        se = etree.SubElement(weather, 'delay')
        se.text = str(alarm.weather.delay)

    with open(filename, 'w', encoding='utf8') as doc:
        doc.write(etree.tostring(alist, pretty_print=True, encoding='unicode'))

def load_alarm_list(filename):
    tree = etree.parse(filename)

    # Create alarm objects from XML
    alarms = []
    for el in tree.findall('alarm'):
        alarm = Alarm(xml=el)
        alarms.append(alarm)

    # Return alarm object list
    return alarms