__author__ = 'bsullivan'


import csv


def watc_allguests():
    count = {'Total': 0, 'W': 0, 'B': 0, 'L': 0, 'A': 0, 'M': 0, 'O': 0, 'Men': 0, 'Women': 0}
    with open('WATC_diversity_data.csv','r') as watc_csv:
        watc_reader = csv.reader(watc_csv)
        for row in watc_reader:
            if row[0] == "Date":
                pass
            else:
                count['Total'] += int(row[5])
                raw_guests = row[6]
                if raw_guests == "":
                    pass
                else:
                    guest_list = raw_guests.split('/')
                    for guest in guest_list:
                        count[(guest[0])] += 1
                        if guest[2] == "M":
                            count['Men'] += 1
                        if guest[2] == "W":
                            count['Women'] += 1
                        if guest in count:
                            count[guest] += 1
                        else:
                            count[guest] = 1
        watc_csv.close()
    return count


def watc_showguests():
    count = {'Total': 0, 'W': 0, 'B': 0, 'L': 0, 'A': 0, 'M': 0, 'O': 0, 'Men': 0, 'Women': 0}
    with open('WATC_diversity_data.csv','r') as watc_csv:
        watc_reader = csv.reader(watc_csv)
        for row in watc_reader:
            if row[0] == "Date":
                pass
            if row[3] == "S":
                count['Total'] += int(row[5])
                raw_guests = row[6]
                guest_list = raw_guests.split('/')
                for guest in guest_list:
                    count[(guest[0])] += 1
                    if guest[2] == "M":
                        count['Men'] += 1
                    if guest[2] == "W":
                        count['Women'] += 1
                    if guest in count:
                        count[guest] += 1
                    else:
                        count[guest] = 1
            else:
                pass
        watc_csv.close()
    return count


print watc_allguests()
print watc_showguests()