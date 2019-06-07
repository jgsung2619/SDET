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

def findStatusSummaryUpdate(issue, issue_changelog):
    maxResults = issue_changelog.maxResults
    histories = issue_changelog.histories
    rawDateList = []

    for history in issue_changelog.histories:
        for item in history.items:
            if item.field == "Status Summary":
                rawDateList.append(history.created)
    rawDate = rawDateList[-1]
    print("LOG: ",rawDate)
    timeConvertor(issue,rawDate)

def timeConvertor(issue, rawDate):
    lastUpdateList = []
    lastUpdateList = rawDate.split(sep="T")
    lastUpdateString = lastUpdateList[0]
    lastUpdate = datetime.strptime(lastUpdateString, "%Y-%m-%d")
    print("LOG: ",lastUpdate)
    timeDeltaCalculator(issue,lastUpdate)

def timeDeltaCalculator(issue, lastUpdate):
    now = datetime.now()
    print("LOG: ", now)
    delta = now - lastUpdate  # 7 days, 21:21:20.939894, datetime
    dayOfDelta = delta.days  # 7, int
    print("LOG: ", dayOfDelta)
    findGroundRuleViolation(issue,dayOfDelta)

def findGroundRuleViolation(issue, delta):
    if delta > 6 :
        addLabels(issue, delta)
    elif delta <= 6 :
        print("LOG: 점검결과 OK!")

def addLabels(issue, delta):
    issue_labels = issue.fields.labels
    if delta > 13:
        try :
            issue_labels.remove('Status_Summary1회미입력')
            issue_labels.append('Status_Summary2회미입력')
            print("LOG: 1회->2회")
        except:
            issue_labels.append('Status_Summary2회미입력')
            print("LOG: 바로 2회 라벨링. 왜 1회 누락되었는지 점검해주세요!")
    elif delta > 6 & delta <= 13:
        issue_labels.append('Status_Summary1회미입력')
        print("LOG: 1회 라벨링")

    issue.update(fields={"labels": issue_labels})
    print("LOG: ", str(issue_labels))

if __name__ == "__main__" :
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    #filter=49494 : 1_webOS_5.0_Epic_OverDue_Initiative_pm
    # issue_search_convert = jira.search_issues("filter=49607", maxResults=1000, expand="changelog")
    issue_search_convert = jira.search_issues("filter=49520", maxResults=1000, expand='changelog')
    print("### status summary 업데이트 누락 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.key
        issue_assignee = issue.fields.assignee.name # initiative Owner
        issue_summary = issue.fields.summary
        issue_changelog = issue.changelog
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        findStatusSummaryUpdate(issue, issue_changelog)

    # raw = "2019-05-12T10:11:11"
    # timeConvertor(raw)
