import calendar
from datetime import datetime

async def alert(t1_closeToClose, bool_isHighUSTodayDay_gte_ClosePreviousDay):

    strings = []
    date = datetime.today()
    dateStr = f"{date.date()}, {calendar.day_name[date.weekday()].upper()[:3]}"

    if 0.86 <= t1_closeToClose <= 3:
        if date.isoweekday() == 1:
            strings.append("- closeToOpen [<= 0%] ---> closeValReached 97%")
        else:
            strings.append("- closeToOpen [<= -0.60 // -0.39% - 0%] ---> 92% closeValReached")

    if date.isoweekday() == 3:
        if t1_closeToClose <= -1.4:
            strings.append("- closeToOpen [<= 0%] ---> 100% closeValReached")
        elif t1_closeToClose <= -1.0:
            strings.append("- closeToOpen [<= 0%] ---> 88% closeValReached")

    if date.isoweekday() == 2:
        if t1_closeToClose <= -1.4:
            strings.append("- closeToOpen [-0.4% - 0%] ---> 97% closeValReached")
        elif t1_closeToClose <= -1.0:
            strings.append("- closeToOpen [<= 0%] ---> 94% closeValReached")

    if not date.isoweekday() == 2 and not date.isoweekday() == 3:
        if t1_closeToClose <= -1.4:
            strings.append("- closeToOpen [-0.4% - 0%] ---> 97% closeValReached")

    if bool_isHighUSTodayDay_gte_ClosePreviousDay == "no" and date.isoweekday() == 1:
        strings.append("- closeToOpen [<= 0%] ---> 93% closeValReached // 90% openToHighÜber0.2 // 80% openToHighÜber0.4")

    return dateStr, strings

def formatList(strings):
    finalStr = ""

    if len(strings) > 1:
        for s in strings:
            finalStr = finalStr + s + "\n"
        finalStr = finalStr.rstrip("\n")
    else:
        finalStr = strings[0]

    return  finalStr