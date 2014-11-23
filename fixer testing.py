__author__ = 'bsullivan'


from pprint import pprint
from tempfile import NamedTemporaryFile
import shutil
import csv
from datetime import datetime, date
import ast


def earliestshow():
    date_list = []
    with open('WATC_Diversity_data.csv', 'r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            raw_date = row["Date"]
            raw_date2 = datetime.strptime(raw_date, "%y%m%d")
            show_date = raw_date2.date()
            date_list.append(show_date)
    date_list.sort()
    return date_list[0]


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


def is_date(raw_date, reason):
    if reason == "entry":
        start = date(2013, 9, 21)
    elif reason == "fixing":
        start = earliestshow()
    end = date.today()
    try:
        raw_date2 = datetime.strptime(raw_date, "%y%m%d")
    except ValueError:
        return False
    raw_date2 = datetime.strptime(raw_date, "%y%m%d")
    show_date = raw_date2.date()
    if len(raw_date) != 6:
        return False
    else:
        if ( start <= show_date <= end ):
            if show_date.weekday() == 5 or show_date.weekday() == 6:
                return True
            else:
                return False
        else:
            return False


def update_guestinfo(original):
    print "OK, here's the original guest list: "
    count = 0
    new_guestlist = original
    for guest in original:
        count += 1
        print str(count) + ". " + guest
    if count != 1:
        guestbool = False
        while guestbool == False:
            choicechoice = raw_input("How many guests need fixing? ")
            try:
                int(choicechoice)
            except ValueError:
                print "Try again with an integer!"
            times = int(choicechoice)
            if times <= count:
                guestbool = True
            elif times > count:
                print "Must be less than the amount of guests."
                guestbool = False
    elif count == 1:
        times = 1
    for time in range(times):
        choice_bool = False
        while choice_bool == False:
            raw_choice = raw_input("Select the guest to fix. ")
            try:
                int(raw_choice)
            except ValueError:
                print "Must be an integer!"
            choice = int(raw_choice) - 1
            if choice in range(count):
                choice_bool = True
            else:
                print "Number must be one of these guests."
                choice_bool = False
        newbool = False
        while newbool == False:
            new_guest = raw_input("What should the new guest be? ")
            if is_guest(new_guest):
                newbool = True
            else:
                print "TRY AGAIN: W,B,L,A,M,O and M,F only."
        new_guestlist[choice] = new_guest
    return new_guestlist


def update_guestnumber(original_guests):
    original = len(original_guests)
    print "So you once thought there were " + str(original) + " guests in this story."
    guestbool = False
    while guestbool == False:
        new_num = raw_input("How many guests are there actually? ")
        try:
            int(new_num)
        except ValueError:
            print "Try again with an integer!"
        if new_num == original:
            print "This is the same as the original."
        else:
            new_total = int(new_num)
            guestbool = True
    new_guestlist = original_guests
    if new_total < original:
        num_to_cut = original - new_total
        count = 0
        for i in range(num_to_cut):
            print "Which of these guests should be eliminated?"
            for guest in new_guestlist:
                count += 1
                print str(count) + ". " + guest
            newbool = False
            while newbool == False:
                eliminate_choice = raw_input("Which guest should we remove? ")
                try:
                    int(eliminate_choice)
                except ValueError:
                    print "Try again with an integer!"
                eliminate = int(eliminate_choice)
                if 0 < eliminate <= original:
                    newbool = True
            eliminate_index = eliminate - 1
            new_guestlist.pop(eliminate_index)
            count = 0
    if new_total > original:
        num_to_add = new_total - original
        for i in range(num_to_add):
            guest_bool = False
            while guest_bool == False:
                guest = raw_input('Enter source race and gender (eg: W,F or B,M): ')
                if is_guest(guest):
                    new_guestlist.append(guest)
                    guest_bool = True
                else:
                    print "TRY AGAIN: W,B,L,A,M,O and M,F only."
                    guest_bool = False
    return new_guestlist


def update_origin(original):
    if original == "D":
        descriptor = "desk-produced"
    elif original == "S":
        descriptor = "show-produced"
    print "OK. This story was originally classified as " + descriptor + "."
    sd_bool = False
    while sd_bool == False:
        new_origin = raw_input('Is this show or desk produced? S/D ')
        if new_origin == "S" or new_origin == "D":
            sd_bool = True
        else:
            print "TRY AGAIN: Enter only S or D."
            sd_bool = False
    return new_origin


def update_producer():
    prod_bool = False
    while prod_bool == False:
        new_prod = raw_input('Enter producer/reporter race and gender (eg: W,F or B,M): ')
        if is_guest(new_prod):
            return new_prod
            prod_bool = True
        else:
            print "TRY AGAIN: W,B,L,A,M,O and M,F only."
            prod_bool = False


# allows for line-by-line fixing.
def fix_something():
    headers = ['Date','Order','Slug','Origin','Producer','Guest number','Guest info']

    date_bool = False
    while date_bool == False:
        raw_date = raw_input("What date are we talking here? (YYMMDD): ")
        if is_date(raw_date, "fixing"):
            date_bool = True
        else:
            print "YYMMDD please, and make sure it's a date you've already entered."
            date_bool = False

    print "OK! Here were the stories that day."
    count = 0
    sluglist = []
    with open('WATC_testing.csv', 'r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            if row["Date"] != raw_date:
                pass
            elif row["Date"] == raw_date:
                count += 1
                print str(count) + ". " + row["Slug"]
                sluglist.append(row["Slug"])
        watc_csv.close()

    choice_bool = False
    while choice_bool == False:
        raw_choice = raw_input("Which story needs fixing? ")
        try:
            int(raw_choice)
        except ValueError:
            print "Must be an integer!"
        choice = int(raw_choice) - 1
        if choice in range(count):
            choice_bool = True
        else:
            print "Number must be one of the elements on the show."
            choice_bool = False
    story = sluglist[choice]

    with open('WATC_testing.csv', 'r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            if row["Slug"] == story and row["Date"] == raw_date:
                selection = row
        watc_csv.close()

    selection["Guest info"] = ast.literal_eval(selection["Guest info"])

    print "Here's the info:"
    pprint(selection)

    keep_going = True
    while keep_going:
        choice_bool2 = False
        while choice_bool2 == False:
            choice = raw_input("Which of these things needs fixing? (Pick Guest number to add/remove guests.) ")
            if choice in selection:
                choice_bool2 = True
            else:
                print "Type one of the descriptors."
                choice_bool2 = False

        if choice == "Guest info":
            replacement = update_guestinfo(selection["Guest info"])
        elif choice == "Guest number":
            replacement = update_guestnumber(selection["Guest info"])
            replacement2 = len(replacement)
        elif choice == "Slug":
            newslug = raw_input("What's the new slug? ")
            replacement = newslug.upper()
        elif choice == "Origin":
            replacement = update_origin(selection["Origin"])
        elif choice == "Producer":
            replacement = update_producer()
        if choice == "Guest number":
            selection["Guest info"] = replacement
            selection["Guest number"] = replacement2
        else:
            selection[choice] = replacement
        keep_choice = raw_input("More fixes to make? Y/N: ")
        if keep_choice == "N":
            keep_going = False
        else:
            keep_going = True

        new_row = []
        for category in headers:
            new_row.append(selection[category])

        replace_data(new_row)


def replace_data(newrow):
    filename = 'WATC_testing.csv'
    tempfile = NamedTemporaryFile(delete=False)

    with open(filename, 'rb') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            if row == []:
                pass
            if row[0] == newrow[0] and row[1] == newrow[1]:
                print "OLD: " + row
                print "NEW: " + newrow
                print "*" * 5
                writer.writerow(newrow)
            else:
                writer.writerow(row)

    shutil.move(tempfile.name, filename)

    print "DONE!!!!"


test_row = ["140525","5","JEFF GOLDBLUM'S JAZZ SHOW","S","W,M","6","['W,M', 'W,M', 'W,M', 'W,M', 'O,M', 'W,F']"]
testing_tmpfile(test_row)