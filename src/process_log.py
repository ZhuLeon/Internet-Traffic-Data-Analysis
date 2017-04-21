import sys
import re
import operator
import datetime


def process_log():
    # TODO: bug with utf-8 encoding when reading in line 27617 but now error on line 2401515
    with open(sys.argv[1]) as inlog:

        # Initialize
        db_host = dict()
        db_resources = dict()
        db_hours = dict()
        db_tracking = dict()
        db_blocked = list()
        interval_time = datetime.datetime.strptime("29/Jun/1995:23:58:01 -0400", "%d/%b/%Y:%H:%M:%S %z")

        # DEBUG
        line_count = 1

        # Iterate through each line in file
        for line in inlog:
            # Parse each line using Regex
            # TODO: Put in some error checking for all this regex
            # try:
            host = re.search('(^.*)(?:\s-\s-)', line).group(1)
            timestamp = re.search(('(([0-9])|([0-2][0-9])|([3][0-1]))/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}'
                                   ':([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]'
                                   '\s(?:\+|-)(?:\d{4})'), line).group()
            request = re.search('\".*\"', line).group()
            if request.find(" HTTP/") != -1 and request.find(" HTTPS/") != -1:
                resource = re.search('(/[^\s\"]*)', request).group(1)
            elif request.find(" HTTP/") > 0 or request.find(" HTTPS/") > 0:
                resource = re.search('(?:GET[\s]|POST[\s]|HEAD[\s])(.*)(?:\sHTTP)', request).group(1)
            response = re.search('(?:\"\s)(\d{3})', line).group(1)
            bytes_amt = re.search('(?:\"\s\d{3}\s)([0-9-]*)', line).group(1)
            # except:
            #    print(line_count)

            if bytes_amt == "-":
                bytes_amt = "0"

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
            compare_time = datetime.datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
            diff = compare_time - interval_time
            # Check the current time is greater than the time(key) and the difference is less than 60 seconds
            if compare_time >= interval_time and diff <= datetime.timedelta(seconds=60) and interval_time in db_hours:
                db_hours[interval_time] += 1
            # If the difference is greater than 60 seconds create a new time(key)
            elif compare_time > interval_time and diff > datetime.timedelta(seconds=60):
                interval_time = compare_time
                db_hours[interval_time] = 1
            else:
                print("NOT SUPPOSED TO HAPPEN. EVER. \t@line: ", end="")
                print(line_count)

            # Feature 4 logic
            # If 3 attempts has been tracked begin blocking for 5 minutes
            if host in db_tracking and len(db_tracking[host]) == 3:
                blocked_diff = compare_time - db_tracking[host][2]
                if blocked_diff <= datetime.timedelta(minutes=5):
                    db_blocked.append(line)
                else:
                    del db_tracking[host]

            # If successful login is made within 20 seconds of first attempt
            if response == "200" and host in db_tracking and len(db_tracking[host]) != 3:
                del db_tracking[host]
            # If failed to login for the first time
            elif response != "200" and host not in db_tracking:
                db_tracking[host] = [compare_time]
            # If failed to login and have previously attempted to login and limit has not been reached
            elif resource != "200" and host in db_tracking and len(db_tracking[host]) != 3:
                failed_diff = compare_time - db_tracking[host][0]

                # If failed login is within the 20 second limit add to tracking
                if failed_diff <= datetime.timedelta(seconds=20):
                    db_tracking[host].append(compare_time)
                # If failed login is outside the 20 second limit restart tracking
                elif failed_diff > datetime.timedelta(seconds=20) :
                    del db_tracking[host]
                    db_tracking[host] = [compare_time]

            line_count += 1
        sorted_host = sorted(db_host.items(), key=operator.itemgetter(1), reverse=True)
        sorted_resource = sorted(db_resources.items(), key=operator.itemgetter(1), reverse=True)
        sorted_hours = sorted(db_hours.items(), key=operator.itemgetter(1), reverse=True)

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
            outfile.write(str(sorted_hours[row][0].strftime("%d/%b/%Y:%H:%M:%S %z")) + ',')
            outfile.write(str(sorted_hours[row][1]) + '\n')

    with open(sys.argv[5], 'w+') as outfile:
        for item in db_blocked:
            outfile.write(item)

process_log()

# Pycharm script parameters:
# "./log_input/log.txt" "./log_output/host.txt" "./log_output/resource.txt" "./log_output/hours.txt" "./log_output/blocked.txt"

__author__ = "Leon Zhu"