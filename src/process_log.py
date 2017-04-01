# Leon Zhu

import sys
import re
import operator

def process_log():
    with open(sys.argv[1], encoding="utf-8") as inlog:
        db_host = dict()
        db_resources = dict()
        # count = 0
        # line = inlog.readline()
        # print(line)
        for line in inlog:
            # print(count)
            # count = count + 1
            # ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', line).group()
            host = re.search('(^.*)(?:\s-\s-)', line).group(1)
            timestamp = re.search(('(([0-9])|([0-2][0-9])|([3][0-1]))/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}'
                             '(:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]'
                            '\s(?:\+|-)(?:\d{4}|\d{3})'), line).group()
            request = re.search('\".*\"', line).group()
            resource = re.search('(/[^\s]+)(?:[^\S\x0a\x0d])|(/(?:[^\S\x0a\x0d]))|(/[^\s\"]+\.[^0-9\"]+)', request).group(1)
            response = re.search('(?:\"\s)(\d{3})', line).group(1)
            bytes_amt = re.search('(?:\s\d{3}\s)([0-9-]*)', line).group(1)

            if bytes_amt == '-':
                bytes_amt = 0
            if host in db_host:
                db_host[host] = db_host[host]+1
            else:
                db_host[host] = 1
            if host in db_resources:
                db_resources[resource] = db_resources[resource] + int(bytes_amt)
            else:
                db_resources[resource]=int(bytes_amt)
        sorted_host = sorted(db_host.items(), key=operator.itemgetter(1), reverse=True)
        sorted_resource = sorted(db_resources.items(), key=operator.itemgetter(1), reverse=True)
        # print(host)
        # print(timestamp)
        # print(request)
        # print(response)
        # print(bytes_amt)
        # print(db_host)
        # print(sorted_host)
        # print(sorted_resource)

    with open(sys.argv[2], 'w+') as outfile:
        for row in range(10):
            outfile.write(str(sorted_host[row][0]) + ',')
            outfile.write(str(sorted_host[row][1]) + '\n')

    with open(sys.argv[3], 'w+') as outfile:
        for row in range(10):
            outfile.write(str(sorted_resource[row][0]) + ',')
            outfile.write(str(sorted_resource[row][1]) + '\n')


process_log()