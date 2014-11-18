__author__ = 'bsullivan'


from __future__ import division
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.font_manager import FontProperties
from pprint import pprint


def totalWATCbydate():
    date_dict = {}
    watc = open("WATC.txt", "r")
    while True:
        raw_line = watc.readline()
        if "\n" not in raw_line:
            break
        else:
            raw_line = raw_line[:-1]
            line = raw_line.split("-")
            if line[0] not in date_dict:
                indv_date = date_dict[(line[0])] = [0,0,0,0,0]
            line_length = len(line) - 1
            indv_date[4] += int(line[5])
    ##guest analysis
            for i in range(line_length,5,-1):
                guest = line[i]
                if guest == "W,M":
                    indv_date[0] += 1
                elif guest == "W,F":
                    indv_date[1] += 1
                elif guest[2] == "M":
                    indv_date[2] += 1
                elif guest[2] == "F":
                    indv_date[3] += 1
    return date_dict


def showWATCbydate():
    date_dict = {}
    watc = open("WATC.txt", "r")
    while True:
        raw_line = watc.readline()
        if "\n" not in raw_line:
            break
        else:
            raw_line = raw_line[:-1]
            line = raw_line.split("-")
            if line[0] not in date_dict:
                indv_date = date_dict[(line[0])] = [0,0,0,0,0,0]
            if line[3] == "S":
                line_length = len(line) - 1
                indv_date[5] += int(line[5])
                for i in range(line_length,5,-1):
                    guest = line[i]
                    if guest == "W,M":
                        indv_date[0] += 1
                    elif guest == "W,F":
                        indv_date[1] += 1
                    elif guest[0] == "O":
                        indv_date[4] += 1
                    elif guest[2] == "M":
                        indv_date[2] += 1
                    elif guest[2] == "F":
                        indv_date[3] += 1
            else: pass
    return date_dict


def Percent(num,total):
    raw_percent = num / total
    percent = round((raw_percent * 100),1)
    return percent


def DateLineGraph(date_dict):
    x = []
    y_series_0 = []
    y_series_1 = []
    y_series_2 = []
    for k in sorted(date_dict):
        date = datetime.datetime.strptime(k,"%y%m%d")
        x.append(date)
        percent_0 = Percent((date_dict[k])[0],(date_dict[k])[3])
        percent_1 = Percent((date_dict[k])[1],(date_dict[k])[3])
        percent_2 = Percent((date_dict[k])[2],(date_dict[k])[3])
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


def DateBarGraph(date_dict):
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
        percent_0 = Percent((date_dict[k])[0],(date_dict[k])[4])
        percent_1 = Percent((date_dict[k])[1],(date_dict[k])[4])
        percent_2 = Percent((date_dict[k])[2],(date_dict[k])[4])
        percent_3 = Percent((date_dict[k])[3],(date_dict[k])[4])
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

def WatcByMonth(date_dict):
    month_dict_num = {}
    month_dict_percent = {}
    for key in date_dict:
        raw_date = datetime.datetime.strptime(key,"%y%m%d")
        month = datetime.datetime.strftime(raw_date, "%m%y")
        if month not in month_dict_num:
            month_dict_num[month] = [0,0,0,0,0,0]
        list1 = month_dict_num[month]
        list2 = [(date_dict[key])[0], (date_dict[key])[1], (date_dict[key])[2],
                 (date_dict[key])[3], (date_dict[key])[4], (date_dict[key])[5]]
        month_dict_num[month] = [x + y for x, y in zip(list1, list2)]
    for key in month_dict_num:
        percent_0 = Percent((month_dict_num[key])[0],(month_dict_num[key])[5])
        percent_1 = Percent((month_dict_num[key])[1],(month_dict_num[key])[5])
        percent_2 = Percent((month_dict_num[key])[2],(month_dict_num[key])[5])
        percent_3 = Percent((month_dict_num[key])[3],(month_dict_num[key])[5])
        percent_4 = Percent((month_dict_num[key])[4],(month_dict_num[key])[5])
        month_dict_percent[key] = [percent_0, percent_1, percent_2, percent_3, percent_4]
    return month_dict_percent



def MonthBarGraph(month_dict):
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
        raw_month = datetime.datetime.strptime(month,"%m%y")
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



def MonthBarGraphTest(month_dict):
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
        raw_month = datetime.datetime.strptime(month,"%m%y")
        month_names.append(datetime.datetime.strftime(raw_month, "%B"))
        white_men.append((month_dict[month])[0])
        white_women.append((month_dict[month])[1])
        men_of_color.append((month_dict[month])[2])
        women_of_color.append((month_dict[month])[3])
        unknown.append((month_dict[month])[4])

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



print WatcShowByDate()
date_dict = WatcByMonth(WatcShowByDate())
pprint(date_dict)
print MonthBarGraphTest(date_dict)