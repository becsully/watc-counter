__author__ = 'bsullivan'

import csv


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


def should_i_replace(element):
    print element
    choice = raw_input("Replace this producer race/gender? Y/N: ")
    if choice == "Y":
        return True
    elif choice == "N":
        return False


def replace(original):
    headers = ["Date","Order","Slug","Origin","Producer","Guest number","Guest info"]
    prrg_bool = False
    while prrg_bool == False:
        rep_prod = raw_input('Enter replacement race,gender (eg W,F): ')
        if is_guest(rep_prod):
            prrg_bool = True
        else:
            print "TRY AGAIN: W,B,L,A,M,O and M,F only."
            prrg_bool = False
    with open('WATC_Diversity_data.csv','r') as original_watc:
        watc_reader = csv.DictReader(original_watc)
        for row in watc_reader:
            if row["Producer"] != original:
                with open('WATC_Diversity_data_new.csv','a') as replace_watc:
                    watc_writer = csv.DictWriter(replace_watc, fieldnames=headers)
                    watc_writer.writerow(row)
                    replace_watc.close()
            elif row["Producer"] == original:
                if should_i_replace(row):
                    row_dict = row
                    row_dict["Producer"] = rep_prod
                    with open('WATC_Diversity_data_new.csv','a') as replace_watc:
                        watc_writer = csv.DictWriter(replace_watc, fieldnames=headers)
                        watc_writer.writerow(row_dict)
                        replace_watc.close()
                else:
                    with open('WATC_Diversity_data_new.csv','a') as replace_watc:
                        watc_writer = csv.DictWriter(replace_watc, fieldnames=headers)
                        watc_writer.writerow(row)
                        replace_watc.close()
        original_watc.close()


replace("L,F")