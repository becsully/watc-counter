__author__ = 'bsullivan'


import csv
import ast
from pprint import pprint


def is_guest(guest):
    races = ['W', 'B', 'L', 'A', 'M', 'O']
    genders = ['M', 'F']
    if len(guest) != 3:
        return False
    else:
        if (guest[0] in races) and (guest[2] in genders):
            return True
        else:
            return False


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


def totalWATCbydate():
    date_dict = {}
    with open("WATC_diversity_data.csv", "r") as watc:
        watcreader = csv.DictReader(watc)
        for row in watcreader:
            if row["Date"] == "Date":
                pass
            else:
                if row["Date"] not in date_dict:
                    date_dict[(row["Date"])] = {"White men":0, "White women":0, "Men of color":0, "Women of color":0,
                                                "Unknown men":0,"Unknown women":0,"Total":0}
                indv_date = date_dict[(row["Date"])]
                raw_guests = row["Guest info"]
                guest_list = ast.literal_eval(raw_guests)
                for guest in guest_list:
                    if is_guest(guest):
                        indv_date["Total"] += 1
                        non_white = ['B', 'L', 'A', 'M']
                        race = guest[0]
                        gender = guest[2]
                        if guest == "W,M":
                            indv_date["White men"] += 1
                        if guest == "W,F":
                            indv_date["White women"] += 1
                        if race in non_white and gender == "M":
                            indv_date["Men of color"] += 1
                        if race in non_white and gender == "F":
                            indv_date["Women of color"] += 1
                        if guest == "O,M":
                            indv_date["Unknown men"] += 1
                        if guest == "O,F":
                            indv_date["Unknown women"] += 1
                    else:
                        pass
        watc.close()
    return date_dict



def showWATCbydate():
    date_dict = {}
    with open("WATC_diversity_data.csv", "r") as watc:
        watcreader = csv.DictReader(watc)
        for row in watcreader:
            if row["Date"] == "Date":
                pass
            else:
                if row["Origin"] == "D":
                    pass
                if row["Origin"] == "S":
                    if row["Date"] not in date_dict:
                        date_dict[(row["Date"])] = {"White men":0, "White women":0, "Men of color":0, "Women of color":0,
                                                    "Unknown men":0,"Unknown women":0,"Total":0}
                    indv_date = date_dict[(row["Date"])]
                    raw_guests = row["Guest info"]
                    guest_list = ast.literal_eval(raw_guests)
                    for guest in guest_list:
                        if is_guest(guest):
                            indv_date["Total"] += 1
                            non_white = ['B', 'L', 'A', 'M']
                            race = guest[0]
                            gender = guest[2]
                            if guest == "W,M":
                                indv_date["White men"] += 1
                            if guest == "W,F":
                                indv_date["White women"] += 1
                            if race in non_white and gender == "M":
                                indv_date["Men of color"] += 1
                            if race in non_white and gender == "F":
                                indv_date["Women of color"] += 1
                            if guest == "O,M":
                                indv_date["Unknown men"] += 1
                            if guest == "O,F":
                                indv_date["Unknown women"] += 1
                        else:
                            pass
        watc.close()
    return date_dict


pprint(showWATCbydate())