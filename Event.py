from InputConverter import *
from FileHandler import *
import sys


class Event:

    TIME_ZONE = 'Europe/Warsaw'
    # EVENTS = []

    def __init__(self, row):

        self.class_title = InputConverter.get_class_title_from(row)
        self.week_day = InputConverter.get_week_day_from(row)
        self.start_time = InputConverter.get_start_time_from(row)
        self.end_time = InputConverter.get_end_time_from(row)
        self.weeks = InputConverter.get_weeks_from(row)
        self.class_type = InputConverter.get_class_type_from(row)
        self.location = InputConverter.get_location_from(row)
        self.teacher = InputConverter.get_teacher_from(row)

    def append_to_ics(self, day, output):
        with open(output, 'a') as output_file:
            output_file.write('\n')
            self.return_ics_event(day, output_file)

    def return_ics_event(self, day, output=sys.stdout):

        buffer = '\n'.join([
            'BEGIN:VEVENT',
            'DTSTART;TZID={}:{}T{}00'.format(self.TIME_ZONE, day.strftime('%Y%m%d'), self.start_time),
            'DTEND;TZID={}:{}T{}00'.format(self.TIME_ZONE, day.strftime('%Y%m%d'), self.end_time),
            'SUMMARY:{}'.format(self.class_title),
            'DESCRIPTION: Prowadzący: {}; Rodzaj zajęć: {}'.format(self.teacher, self.class_type),
            'LOCATION:{}'.format(self.location),
            'TRANSP:OPAQUE',
            'END:VEVENT',
        ])

        output.write(buffer)

    @staticmethod
    def collect_events_for_group(schedule, group):
        try:
            class_set = []
            for _class in schedule[:len(schedule)-1]:
                if _class[InputConverter.group_column()] == group:
                    if _class[InputConverter.class_title_column()] == '':
                        continue
                    else:
                        class_set.append(Event(_class))
                        # Event.EVENTS.append(Event(_class))
            return class_set
        except Exception as e:
            print('Unpredicted exception while collecting events: {}'.format(e))


