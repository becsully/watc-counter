# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:59:37 2014

@author: bsullivan
"""

from __future__ import division
from datetime import datetime,date
import csv
import ast
from pprint import pprint


# these four functions are test/error handling for the CreateElement function.
def is_number(num,things):
    try:
        int(num)
    except ValueError:
        return False
    num = int(num)
    if things == "guests":
        if num <= 10:
            return True
        elif num > 10:
            sure = raw_input("That's a lot! Are you sure? Y/N: ")
            if sure == "Y":
                return True
            else:
                return False
    elif things == "elements":
        if num > 5 and num < 12:
            return True
        elif num <= 5 or num >= 12:
            sure = raw_input("That's a weird number. Are you sure? Y/N: ")
            if sure == "Y":
                return True
            else:
                return False
    elif things == "shows":
        if 7 > num:
            return True
        elif 7 <= num:
            sure = raw_input("That's a lot! Are you sure? Y/N: ")
            if sure == "Y":
                return True
            else:
                return False


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


def is_slug(slug):
    if "-" in slug:
        return False
    else:
        return True

        
def is_date(raw_date,reason):
    if reason == "entry":
        start = date(2013, 9, 21)
    elif reason == "fixing":
        start = earliestshow()
    end = date.today()
    try:
        raw_date2 = datetime.strptime(raw_date,"%y%m%d")
    except ValueError:
        return False
    raw_date2 = datetime.strptime(raw_date,"%y%m%d")
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
        

# intermediate function for the EnterShows ability.
def create_element(date, position_in_show):    
    element = [date, str(position_in_show)] #assigns date and position in show
    
    #slug with error handling:
    slug_bool = False
    while slug_bool == False:
        slug = raw_input('Type the slug of this story: ')
        if is_slug(slug):
            element.append(slug)
            slug_bool = True
        else: 
            print "TRY AGAIN: Remove the dashes from the slug title."
            slug_bool = False
    
    #Show or Desk with error handling
    sd_bool = False
    while sd_bool == False:
        s_or_d = raw_input('Is this show or desk produced? S/D ')
        if s_or_d == "S" or s_or_d == "D":
            element.append(s_or_d)
            sd_bool = True
        else: 
            print "TRY AGAIN: Enter only S or D."
            sd_bool = False
    
    #Producer/Reporter R,G with error handling
    prrg_bool = False
    while prrg_bool == False:
        rep_prod = raw_input('Enter producer/reporter race,gender (eg W,F): ')
        if is_guest(rep_prod):
            element.append(rep_prod)
            prrg_bool = True
        else:
            print "TRY AGAIN: W,B,L,A,M,O and M,F only."
            prrg_bool = False
    
    #Number of guests with error handling
    num_of_guests = 0
    num_bool = False
    while num_bool == False:
        num = raw_input('How many people are quoted? ')
        if is_number(num,"guests"):
            element.append(num)
            num_of_guests = int(num)
            num_bool = True
        else:
            print "TRY AGAIN: Must be an integer/reasonable number."
            num_bool = False
    
    guest_list = []
    
    for i in range(num_of_guests):
        guest_bool = False
        while guest_bool == False:
            guest = raw_input('Enter source race and gender (eg: W,F or B,M): ')
            if is_guest(guest):
                guest_list.append(guest)
                guest_bool = True
            else:
                print "TRY AGAIN: W,B,L,A,M,O and M,F only."
                guest_bool = False

    element.append(guest_list)
    
    with open('WATC_Diversity_data.csv','a') as watc_csv:
        watc_writer = csv.writer(watc_csv, lineterminator="\n", quoting=csv.QUOTE_ALL)
        watc_writer.writerow(element)
        watc_csv.close()
        
    return element


# intermediate function for the EnterShows ability.
def create_show(date):
    num_bool = False
    while num_bool == False:
        num = raw_input('How many elements in the show this day? ')
        if is_number(num,"elements"):
            show_length = int(num)
            num_bool = True
        else:
            print "TRY AGAIN: Must be an integer/reasonable number."
            num_bool = False
    show = []
    for i in range(show_length):
        element = create_element(date, i)
        show.append(element)
    return show


# run this for data entry
def enter_shows():
    num_bool = False
    while num_bool == False:
        num = raw_input("How many shows will you enter today? ")
        if is_number(num,"shows"):
            amount = int(num)
            num_bool = True
        else:
            print "TRY AGAIN: Must be an integer/reasonable number."
            num_bool = False
    entry = []
    for i in range(amount):
        date_bool = False
        while date_bool == False:
            date = raw_input("Type the date of the show you'd like to add. YYMMDD ")
            if is_date(date,"entry"):
                entry.append(create_show(date))
                date_bool = True
            else:
                print "TRY AGAIN: Use the format YYMMDD."
                date_bool = False
    return entry


# collects the results and returns a dictionary.
def watc_allguests():
    count = {'Total': 0, 'W': 0, 'B': 0, 'L': 0, 'A': 0, 'M': 0, 'O': 0, 'Men': 0, 'Women': 0}
    with open('WATC_Diversity_data.csv','r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            if row['Date'] == "Date":
                pass
            else:
                count['Total'] += int(row['Guest number'])
                raw_guests = row['Guest info']
                if raw_guests == "":
                    pass
                else:
                    guest_list = ast.literal_eval(raw_guests)
                    for guest in guest_list:
                        if is_guest(guest):
                            race = guest[0]
                            gender = guest[2]
                            count[race] += 1
                            if gender == "M":
                                count['Men'] += 1
                            if gender == "F":
                                count['Women'] += 1
                            if guest in count:
                                count[guest] += 1
                            else:
                                count[guest] = 1
                        else:
                            pass
        watc_csv.close()
    return count


# collects the results and returns a dictionary (show guests only).
def watc_showguests():
    count = {'Total': 0, 'W': 0, 'B': 0, 'L': 0, 'A': 0, 'M': 0, 'O': 0, 'Men': 0, 'Women': 0}
    with open('WATC_Diversity_data.csv','r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            if row["Date"] == "Date":
                pass
            if row["Origin"] == "S":
                count['Total'] += int(row['Guest number'])
                raw_guests = row['Guest info']
                if raw_guests == "":
                    pass
                else:
                    guest_list = ast.literal_eval(raw_guests)
                    for guest in guest_list:
                        if is_guest(guest):
                            race = guest[0]
                            gender = guest[2]
                            count[race] += 1
                            if gender == "M":
                                count['Men'] += 1
                            if gender == "F":
                                count['Women'] += 1
                            if guest in count:
                                count[guest] += 1
                            else:
                                count[guest] = 1
                        else:
                            pass
            else:
                pass
        watc_csv.close()
    return count


#turns awkward num into nice round percent
def percent(num, total):
    raw_percent = num / total
    perc = round((raw_percent * 100), 1)
    return perc


#this will nicely format a given dictionary of results.
def formatter(watcdict):
    total = watcdict['Total']
    men = watcdict['Men']
    women = watcdict['Women']
    white = watcdict['W']
    black = watcdict['B']
    latino = watcdict['L']
    asian = watcdict['A']
    middle = watcdict['M']
    other = watcdict['O']
    wbl = "White: %g | Black: %g | Middle Eastern: %g" % (white, black, middle)
    amo = "Asian: %g | Latino: %g | Other/Unknown: %g" % (asian, latino, other)
    mw = "Men: %g (%g%%) | Women: %g (%g%%)"  % (men, percent(men, total), women, percent(women, total))
    print "#" + ("There were " + str(total) + " total guests on WATC.").center(50) + "#"
    print "# " + "-" * 48 + " #"
    print "#" + ("ETHNIC BREAKDOWN").center(50) + "#"
    print "#" + (wbl).center(50) + "#"
    print "#" + (amo).center(50) + "#"
    print "# " + "-" * 48 + " #"
    print "#" + ("GENDER BREAKDOWN").center(50)+ "#"
    print "#" + (mw).center(50) + "#"
    print "# " + "-" * 48 + " #"
    print "#" + ("White men made up " + str(percent(watcdict['W,M'], total)) + "% of guests.").center(50) + "#"
    print "#" + (str(percent(white, total)) + "% of guests were white.").center(50) + "#"


#This just prints the formatter.
def printer(choice):
    if choice == "total":
        descriptor = "(incl. reporter pieces)"
        chosen_dict = watc_allguests()
    elif choice == "show":
        descriptor = "(show-booked guests only)"
        chosen_dict = watc_showguests()
    early_date = date.strftime(earliestshow(), "%B %d, %Y")
    latest_date = date.strftime(latestshow(), "%B %d, %Y")
    print "#" * 52
    print "#" + ("WATC diversity " + descriptor).center(50) + "#"
    print "#" + (early_date + " through " + latest_date).center(50) + "#"
    formatter(chosen_dict)
    print "#" * 52


#This backs up the main data file.
def backup():
    original = open('WATC_Diversity_data.csv','r')
    reader = csv.reader(original)
    backup_file = open('WATC_backup.csv','w')
    writer = csv.writer(backup_file, lineterminator="\n")
    for row in reader:
        writer.writerow(row)
    original.close()
    backup_file.close()
    print "Backup complete!"


def earliestshow():
    date_list = []
    with open('WATC_Diversity_data.csv','r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            raw_date = row["Date"]
            raw_date2 = datetime.strptime(raw_date,"%y%m%d")
            show_date = raw_date2.date()
            date_list.append(show_date)
    date_list.sort()
    return date_list[0]


def latestshow():
    date_list = []
    with open('WATC_Diversity_data.csv','r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            raw_date = row["Date"]
            raw_date2 = datetime.strptime(raw_date,"%y%m%d")
            show_date = raw_date2.date()
            date_list.append(show_date)
    date_list.sort(reverse=True)
    return date_list[0]


def fix_something():
    date_bool = False
    while date_bool == False:
        raw_date = raw_input("What date are we talking here? (YYMMDD): ")
        if is_date(raw_date,"fixing"):
            date_bool = True
        else:
            print "YYMMDD please, and make sure it's a date you've already entered."
            date_bool = False
    print "OK! Which story do you want to fix?"
    count = 0
    with open('WATC_Diversity_data.csv','r') as watc_csv:
        watc_reader = csv.DictReader(watc_csv)
        for row in watc_reader:
            if row["Date"] != raw_date:
                pass
            elif row["Date"] == raw_date:
                count += 1
                print str(count) + ". " + row["Slug"]
        watc_csv.close()


## WATC Counter basic interactive program
print """
Welcome to the WATC Counter!
What would you like to do?"""

keep_going = True
selection = 0
while keep_going:
    print """
    1. Enter show(s)
    2. Print the total show data
    3. Print the show-only data (no desk pieces)
    4. What's the earliest show in the list?
    5. What's the latest show in the list?
    6. Fix something
    7. Back up the list
    8. Quit
    """
    selection = int(raw_input("Please choose (1-8): "))
    if selection == 1 or 2 or 3 or 4 or 5 or 6 or 7:
        if selection == 1:
            enter_shows()
        elif selection == 2:
            printer("total")
        elif selection == 3:
            printer("show")
        elif selection == 4:
            print earliestshow()
        elif selection == 5:
            print latestshow()
        elif selection == 6:
            fix_something()
        elif selection == 7:
            backup()
        keep_going = True
    if selection == 8:
        keep_going = False
        
