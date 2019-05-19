from jira import JIRA
from jira.exceptions import JIRAError
import sys
from datetime import datetime, timedelta

DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'
# ID = input("AD계정 : ")
# PASSWORD = input("Passwd : ")
ID = "goosung.jung"
PASSWORD = "wjdrntjd3570!"
# .txt file to description

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

def findStatusSummaryUpdate(issue_changelog):
    maxResults = issue_changelog.maxResults
    histories = issue_changelog.histories
    rawDateList = []

    for history in issue_changelog.histories:
        for item in history.items:
            if item.field == "Status Summary":
                rawDateList.append(history.created)
    rawDate = rawDateList[-2]
    print(rawDate)
    timeConvertor(rawDate)


if __name__ == "__main__" :
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    #filter=49494 : 1_webOS_5.0_Epic_OverDue_Initiative_pm
    issue_search_convert = jira.search_issues("key=TVPLAT-19005", maxResults=1000, expand="changelog")
    # issue_search_convert = jira.search_issues("filter=49520", maxResults=100)
    print("### status summary 업데이트 누락 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.key
        issue_assignee = issue.fields.assignee.name # initiative Owner
        issue_summary = issue.fields.summary
        issue_changelog = issue.changelog
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        findStatusSummaryUpdate(issue_changelog)

    # raw = "2019-05-12T10:11:11"
    # timeConvertor(raw)
