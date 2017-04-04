# Leon Zhu

import sys
import re
import operator
import datetime

def process_log():
    with open(sys.argv[1], encoding="utf-8") as inlog:

        # Initialize
        db_host = dict()
        db_resources = dict()
        db_hours = dict()
        interval_time = datetime.datetime.strptime("29/Jun/1995:23:58:01", "%d/%b/%Y:%H:%M:%S")

        # DEBUG
        line_count = 1

        # Iterate through each line in file
        for line in inlog:
            # Parse each line using Regex
            # ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', line).group()
            print(line_count)
            host = re.search('(^.*)(?:\s-\s-)', line).group(1)
            timestamp = re.search(('(([0-9])|([0-2][0-9])|([3][0-1]))/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}'
                                   '(:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]'
                                   '\s(?:\+|-)(?:\d{4}|\d{3})'), line).group()
            in_date = re.search(('(([0-9])|([0-2][0-9])|([3][0-1]))/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}'
                                 '(:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]'), timestamp).group()
            request = re.search('\".*\"', line).group()
            resource = re.search('(/[^\s]+)(?:[^\S\x0a\x0d])|(/(?:[^\S\x0a\x0d]))|(/[^\s\"]+\.[^0-9\"]+)|(/\")', request).group(1)
            # TODO: FIX BUG AT line 41013: https://regex101.com/r/6W9cL1/6
            response = re.search('(?:\"\s)(\d{3})', line).group(1)
            bytes_amt = re.search('(?:\s\d{3}\s)([0-9-]*)', line).group(1)

            if bytes_amt == '-':
                bytes_amt = 0

            # Feature 1 logic
            if host in db_host:
                db_host[host] += 1
            else:
                db_host[host] = 1

            # Feature 2 logic
            if host in db_resources:
                db_resources[resource] += int(bytes_amt)
            else:
                db_resources[resource] = int(bytes_amt)

            # Feature 3 logic
            compare_time = datetime.datetime.strptime(in_date, "%d/%b/%Y:%H:%M:%S")
            diff = compare_time - interval_time
            if compare_time >= interval_time and diff <= datetime.timedelta(seconds=60) and interval_time in db_hours:
                db_hours[interval_time] += 1
            elif compare_time > interval_time and diff > datetime.timedelta(seconds=60):
                interval_time = compare_time
                db_hours[interval_time] = 1
            else:
                print("NOT SUPPOSED TO HAPPEN. EVER. \t@line: ", end="")
                print(line_count)

            line_count += 1
        sorted_host = sorted(db_host.items(), key=operator.itemgetter(1), reverse=True)
        sorted_resource = sorted(db_resources.items(), key=operator.itemgetter(1), reverse=True)
        sorted_hours = sorted(db_hours.items(), key=operator.itemgetter(1), reverse=True)
        # print(host)
        # print(timestamp)
        # print(request)
        # print(response)
        # print(bytes_amt)
        # print(db_host)
        # test = datetime.datetime.strptime("01/Jul/1995:00:01:02", "%d/%b/%Y:%H:%M:%S")
        # print(db_hours)
        # print(sorted_host)
        # print(sorted_resource)
        # print(sorted_hours)

    with open(sys.argv[2], 'w+') as outfile:
        for row in range(10):
            outfile.write(str(sorted_host[row][0]) + ',')
            outfile.write(str(sorted_host[row][1]) + '\n')

    with open(sys.argv[3], 'w+') as outfile:
        for row in range(10):
            outfile.write(str(sorted_resource[row][0]) + ',')
            outfile.write(str(sorted_resource[row][1]) + '\n')

    with open(sys.argv[4], 'w+') as outfile:
        for row in range(10):
            outfile.write(str(sorted_hours[row][0]) + ',')
            outfile.write(str(sorted_hours[row][1]) + '\n')

process_log()