__author__ = 'bsullivan'


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
            new_guest = raw_input("Enter the new race/gender. ")
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
        if new_origin == "S" or s_or_d == "D":
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


print update_producer()