from __future__ import division
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.font_manager import FontProperties
from pprint import pprint
import csv
import ast
from collections import Counter


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


def percent_of(num,total):
    raw_percent = num / total
    percent = round((raw_percent * 100),1)
    return percent


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
                                                "Unknown men":0, "Unknown women":0, "Total":0}
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


def date_line_graph(date_dict):
    x = []
    y_series_0 = []
    y_series_1 = []
    y_series_2 = []
    for k in sorted(date_dict):
        date = datetime.datetime.strptime(k,"%y%m%d")
        x.append(date)
        percent_0 = percent_of((date_dict[k])[0],(date_dict[k])[3])
        percent_1 = percent_of((date_dict[k])[1],(date_dict[k])[3])
        percent_2 = percent_of((date_dict[k])[2],(date_dict[k])[3])
        y_series_0.append(percent_0)
        y_series_1.append(percent_1)
        y_series_2.append(percent_2)
    print x
    print y_series_0
    print y_series_1
    print y_series_2
    dates = mdates.date2num(x)
    fig = plt.figure()
    graph = fig.add_subplot(111)
    graph.plot(dates,y_series_0,'r-o')
    graph.plot(dates,y_series_1,'b-o')
    graph.plot(dates,y_series_2,'g-o')
    graph.set_xticks(dates)
    fig.autofmt_xdate()

    plt.show()


def date_bar_graph(date_dict):
    num = range(len(date_dict))
    dates = []
    white_men = []
    white_women = []
    men_of_color = []
    women_of_color = []
    for k in sorted(date_dict):
        raw_date = datetime.datetime.strptime(k,"%y%m%d")
        date = datetime.datetime.strftime(raw_date, "%b %d")
        dates.append(date)
        percent_0 = percent_of((date_dict[k])[0],(date_dict[k])[4])
        percent_1 = percent_of((date_dict[k])[1],(date_dict[k])[4])
        percent_2 = percent_of((date_dict[k])[2],(date_dict[k])[4])
        percent_3 = percent_of((date_dict[k])[3],(date_dict[k])[4])
        white_men.append(percent_0)
        white_women.append(percent_1)
        men_of_color.append(percent_2)
        women_of_color.append(percent_3)

    september = dates.index("Sep 06")
    october = dates.index("Oct 04")

    y_wm = np.array(white_men)
    y_ww = np.array(white_women)
    y_mc = np.array(men_of_color)
    y_wc = np.array(women_of_color)

    ## swap ind for dates to plot by date: dates = mdates.date2num(x)
    ## ind = range(n)
    width = 0.8

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.yaxis.grid(True,color='white',linestyle="-")
    ax.set_xticks(([2,september+1,october+1]))
    ax.set_xticklabels(['August','September','October'])
    l = plt.axvline(x=(september-.105), color='lightgrey')
    l = plt.axvline(x=(october-.105), color='lightgrey')
    ## l = plt.axhline(y=58, color='lightgrey')
    ## l = plt.axhline(y=80, color='lightgrey')
    ax.set_xlim(-0.5,len(num)+0.5)

    p1 = plt.bar(num, y_wm, width, color=((114/255),(158/255),(206/255)), lw=0)
    p2 = plt.bar(num, y_ww, width, color=((158/255),(218/255),(229/255)), bottom=sum([y_wm]), lw=0)
    p3 = plt.bar(num, y_mc, width, color=((255/255),(187/255),(120/255)),
                 bottom=sum([y_wm, y_ww]), lw=0)
    p4 = plt.bar(num, y_wc, width, color=((255/255),(152/255),(150/255)),
                 bottom=sum([y_wm, y_ww, y_mc]), lw=0)

    plt.title('Diversity by date on WATC')
    plt.tick_params(axis='both', which='both', left='off', right='off', bottom='off', top='off')
    plt.ylabel('Percent of guests')
    plt.yticks(range(0,101,10))
    plt.legend( (p1[0], p2[0], p3[0], p4[0]), ('White Men', 'White Women',
                                       'Men of Color', 'Women of Color' ) )

    plt.show()


def watc_by_month(date_dict):
    month_by_number = {}
    month_by_percent = {}
    for key in date_dict:
        raw_date = datetime.datetime.strptime(key,"%y%m%d")
        month = datetime.datetime.strftime(raw_date, "%y%m")
        if month not in month_by_number:
            month_by_number[month] = {"White men":0, "White women":0, "Men of color":0, "Women of color":0,
                                     "Unknown men":0,"Unknown women":0,"Total":0}
        dict1 = Counter(month_by_number[month])
        dict2 = Counter(date_dict[key])
        month_Counter = dict1 + dict2
        month_by_number[month] = dict(month_Counter)
    for month in month_by_number:
        month_by_percent[month] = {"White men":0, "White women":0, "Men of color":0, "Women of color":0,
                                 "Unknown men":0,"Unknown women":0,"Total":0}
        for demographic in month_by_number[month]:
            try:
                firstnum = (month_by_number[month])[demographic]
                secondnum = (month_by_number[month])["Total"]
                percent = percent_of(firstnum,secondnum)
                (month_by_percent[month])[demographic] = percent
            except KeyError:
                pass
            month_by_percent[month].pop("Total",None)
    return month_by_percent


def old_month_bar_graph(month_dict):
    num = range(len(month_dict))
    dates = []
    white_men = []
    white_women = []
    men_of_color = []
    women_of_color = []
    percents = []
    month_names = []

    for i in range(0,101,10):
        percents.append(str(i)+"%")

    for month in sorted.month_dict:
        dates.append(month)
        raw_month = datetime.datetime.strptime(month,"%y%m")
        month_names.append(datetime.datetime.strftime(raw_month, "%B"))
        white_men.append((month_dict[month])[0])
        white_women.append((month_dict[month])[1])
        men_of_color.append((month_dict[month])[2])
        women_of_color.append((month_dict[month])[3])

    y_wm = np.array(white_men)
    y_ww = np.array(white_women)
    y_mc = np.array(men_of_color)
    y_wc = np.array(women_of_color)

    width = 0.8

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.yaxis.grid(True,color='white',linestyle="-", zorder=10)
    l = plt.axhline(y=58, color='lightgrey', zorder=0)
    l = plt.axhline(y=80, color='lightgrey', zorder=1)
    ax.set_xlim(-0.2,len(num)+0.2)
    ax.set_xticklabels(['August','September','October'])
    ax.set_yticklabels(percents)
    fontP = FontProperties()
    fontP.set_size('small')

    p1 = plt.bar(num, y_wm, width, color=((114/255),(158/255),(206/255)),
                 lw=0, zorder=2)
    p2 = plt.bar(num, y_ww, width, color=((164/255),(209/255),(230/255)),
                 bottom=sum([y_wm]), lw=0, zorder=2)
    p3 = plt.bar(num, y_mc, width, color=((250/255),(140/255),(98/255)),
                 bottom=sum([y_wm, y_ww]), lw=0, zorder=2)
    p4 = plt.bar(num, y_wc, width, color=((255/255),(187/255),(120/255)),
                 bottom=sum([y_wm, y_ww, y_mc]), lw=0, zorder=2)

    plt.tick_params(axis='both', which='both', left='off', right='off',
                    bottom='off', top='off')
    plt.yticks(range(0,101,10))
    plt.xticks(np.arange(0.4,(len(month_dict)+0.4),1))
    plt.legend( (p1[0], p2[0], p3[0], p4[0]), ('White Men', 'White Women',
               'Men of Color', 'Women of Color' ), loc='upper center',
               bbox_to_anchor=(0.5, 1.1), ncol=4, prop=fontP )

    plt.show()


def month_bar_graph(month_dict):
    num = range(len(month_dict))
    dates = []
    white_men = []
    white_women = []
    men_of_color = []
    women_of_color = []
    unknown = []
    percents = []
    month_names = []


    for i in range(0,101,10):
        percents.append(str(i)+"%")

    for month in sorted(month_dict):
        dates.append(month)
        raw_month = datetime.datetime.strptime(month,"%y%m")
        month_names.append(datetime.datetime.strftime(raw_month, "%B"))
        white_men.append((month_dict[month])["White men"])
        white_women.append((month_dict[month])["White women"])
        men_of_color.append((month_dict[month])["Men of color"])
        women_of_color.append((month_dict[month])["Women of color"])
        unknown.append((month_dict[month])["Unknown men"] + (month_dict[month])["Unknown women"])

    y_wm = np.array(white_men)
    y_ww = np.array(white_women)
    y_mc = np.array(men_of_color)
    y_wc = np.array(women_of_color)
    y_u = np.array(unknown)

    width = 0.8

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    ax1.yaxis.grid(True,color='white',linestyle="-", zorder=10)
    l = plt.axhline(y=58, color='lightgrey', zorder=0)
    l = plt.axhline(y=80, color='lightgrey', zorder=0)
    l = plt.axhline(y=91, color='lightgrey', zorder=0)
    ax1.set_xlim(-0.2,len(num))
    ax1.set_xticklabels(month_names)
    ax1.set_yticklabels(percents)
    fontP = FontProperties()
    fontP.set_size('small')

    #colors from website Tableau
    p1 = plt.bar(num, y_wm, width, color=((114/255),(158/255),(206/255)),
                 lw=0, zorder=2)
    p2 = plt.bar(num, y_ww, width, color=((164/255),(209/255),(230/255)),
                 bottom=sum([y_wm]), lw=0, zorder=2)
    p3 = plt.bar(num, y_mc, width, color=((250/255),(140/255),(98/255)),
                 bottom=sum([y_wm, y_ww]), lw=0, zorder=2)
    p4 = plt.bar(num, y_wc, width, color=((255/255),(187/255),(120/255)),
                 bottom=sum([y_wm, y_ww, y_mc]), lw=0, zorder=2)
    p5 = plt.bar(num, y_u, width, color=((133/255),(175/255),(125/255)),
                 bottom=sum([y_wm, y_ww, y_mc, y_wc]), lw=0, zorder=2)


    plt.tick_params(axis='both', which='both', left='off', right='off',
                    bottom='off', top='off')
    plt.yticks(range(0,101,10))
    plt.xticks(np.arange(0.4,(len(month_dict)+0.4),1))
    plt.legend( (p1[0], p2[0], p3[0], p4[0], p5[0]), ('White Men', 'White Women',
               'Men of Color', 'Women of Color', 'Unknown' ), loc='upper center',
               bbox_to_anchor=(0.5, 1), ncol=5, prop=fontP )

    plt.show()


def main():
    print "WELCOME TO THE WATC BY DATE GRAPHER"
    print
    while True:
        print "1. Print a bar graph (NEW) of the monthly data, with unknowns."
        print "2. Print a bar graph (OLD) of the monthly data, minus unknowns."
        print "3. Print a bar graph of the daily data. (NEEDS UPDATE)"
        print "4. Print a line graph of the daily data. (NEEDS UPDATE)"
        print "5. Quit"
        choice1, choice2 = raw_input("Choose an option 1-5: "), raw_input('Do you want "show" data or "total" data? ')
        if choice1 == "1":
            if choice2 == "show":
                month_bar_graph(watc_by_month(showWATCbydate()))
            elif choice2 == "total":
                month_bar_graph(watc_by_month(totalWATCbydate()))
            else:
                print "Invalid choice.\n"
        elif choice1 == "2":
            if choice2 == "show":
                old_month_bar_graph(watc_by_month(showWATCbydate()))
            elif choice2 == "total":
                old_month_bar_graph(watc_by_month(totalWATCbydate()))
            else:
                print "Invalid choice.\n"
        elif choice1 == "3":
            if choice2 == "show":
                date_bar_graph(showWATCbydate())
            elif choice2 == "total":
                date_bar_graph(totalWATCbydate())
            else:
                print "Invalid choice.\n"
        elif choice1 == "4":
            if choice2 == "show":
                date_line_graph(showWATCbydate())
            elif choice2 == "total":
                date_line_graph(totalWATCbydate())
            else:
                print "Invalid choice.\n"
        else:
            break


if __name__ == "__main__":
    main()