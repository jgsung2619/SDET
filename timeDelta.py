from datetime import datetime, timedelta


def timeConvertor(rawDate):
    lastUpdateList = rawDate.split(sep="T")
    lastUpdateString = lastUpdateList[0]
    lastUpdate = datetime.strptime(lastUpdateString, "%Y-%m-%d")
    print(lastUpdate)
    timeDeltaCalculator(lastUpdate)

def timeDeltaCalculator(lastUpdate):
    now = datetime.now()
    print(now)
    delta = now - lastUpdate  # 7 days, 21:21:20.939894, datetime
    dayOfDelta = delta.days  # 7, int
    print(dayOfDelta)
    findGroundRuleViolation(dayOfDelta)

def findGroundRuleViolation(delta):
    if delta > 7 :
        print("addLabels")
    elif delta <= 7 :
        print("OK")

if __name__ == "__main__" :
    raw = "2019-05-12T10:11:11"
    timeConvertor(raw)
