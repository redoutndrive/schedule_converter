from InputConverter import *
from FileHandler import *


class Event:

    TIME_ZONE = 'Europe/Warsaw'
    EVENTS = []

    def __init__(self, row):

        self.class_title = InputConverter.get_class_title_from(row)
        self.week_day = InputConverter.get_week_day_from(row)
        self.start_time = InputConverter.get_start_time_from(row)
        self.end_time = InputConverter.get_end_time_from(row)
        self.weeks = ''
        self.class_type = InputConverter.get_class_type_from(row)
        self.location = InputConverter.get_location_from(row)
        self.teacher = InputConverter.get_teacher_from(row)

    def append_to_ics(self, file_name, day):

        output_file = open(file_name, 'a')
        output_file.write('BEGIN:VEVENT\n')
        output_file.write('DTSTART;TZID=' + self.TIME_ZONE + ':' + day.strftime('%Y%m%d') + 'T' + self.start_time + '00\n')
        output_file.write('DTEND;TZID=' + self.TIME_ZONE + ':' + day.strftime('%Y%m%d') + 'T' + self.end_time + '00\n')
        output_file.write('SUMMARY:' + self.class_title + '\n')
        output_file.write('DESCRIPTION: Prowadzący: ' + self.teacher + '\n')
        output_file.write('LOCATION:' + self.location + '\n')
        output_file.write('TRANSP:OPAQUE\n')
        output_file.write('END:VEVENT\n\n')
        output_file.close()

    # test method
    def preview_ics_output(self, day):

        print('BEGIN:VEVENT')
        print('DTSTART;TZID={}:{}T{}00'.format(self.TIME_ZONE, day.strftime('%Y%m%d'), self.start_time))
        print('DTEND;TZID={}:{}T{}00'.format(self.TIME_ZONE, day.strftime('%Y%m%d'), self.end_time))
        print('SUMMARY:{}'.format(self.class_title))
        print('DESCRIPTION: Prowadzący: {}; Rodzaj zajęć: {}'.format(self.teacher, self.class_type))
        print('LOCATION:{}'.format(self.location))
        print('TRANSP:OPAQUE')
        print('END:VEVENT')

    @staticmethod
    def collect_events_for_group(schedule, group):
        try:
            for _class in schedule[:len(schedule)-1]:
                if _class[InputConverter.group_column()] == group:
                    if _class[InputConverter.class_title_column()] == '':
                        continue
                    else:
                        Event.EVENTS.append(Event(_class))
        except Exception as e:
            print('Unpredicted exception while collecting events: {}'.format(e))


class Group:

    @staticmethod
    def get_groups(rows):
        counter = 1

        try:
            # using set to store unique values only
            groups = set([])

            for row in rows[1:len(rows) - 1]:
                if row[InputConverter.group_column()] == '':
                    continue
                groups.add(row[InputConverter.group_column()])
                counter += 1

            # Kicking out empty space element from groups
            # if '' in groups:
            #     groups.remove('')

            print('{} unique groups found'.format(len(groups)))
            return sorted(groups)

        except IndexError:
            print('Oops. Trying to read white spaces after table. IndexError in row:', counter)
            sys.exit(0)
        except TypeError:
            print('get_groups method in \'Groups\' tried to read non-existing file or file with unexpected structure.')
            sys.exit(0)
        except Exception as e:
            print('Unexpected type of exception: "{}" occurred in get_groups method.'.format(e))
            sys.exit(0)

