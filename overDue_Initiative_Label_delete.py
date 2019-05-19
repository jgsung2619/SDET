from jira import JIRA
from jira.exceptions import JIRAError
import sys

DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'
# ID = input("AD계정 : ")
# PASSWORD = input("Passwd : ")
ID = "goosung.jung"
PASSWORD = "wjdrntjd3570!"
# .txt file to description


def overDueLabeled():
    labeledList = []
    initiative_search = jira.search_issues('project=TVPLAT and labels = EPIC_OverDueDate1회', maxResults=1000)
    for key in initiative_search:
        initiative = jira.issue(key)
        labeledList.append(initiative.key)

    print("현재 Labeling된 Initiative List: "+' '.join(map(str, labeledList)))
    return labeledList

def realTimeoverDueInitiative():
    realTimeList = []
    initiative_search = jira.search_issues('filter=49494', maxResults=1000)
    for key in initiative_search:
        initiative = jira.issue(key)
        realTimeList.append(initiative.key)

    print("조치된 후 남은 Initiative List: "+' '.join(map(str, realTimeList)))
    return realTimeList

def compareList(labeledList, realTimeList):
    deltaList = []
    deltaList = list(set(labeledList) - set(realTimeList))
    print("Unlabeling할 Initiative List: "+' '.join(map(str, deltaList)))
    return deltaList

def delLabels(issue):
    issue_labels = issue.fields.labels
    print(str(issue_labels))
    issue_labels.remove('EPIC_OverDueDate1회')
    issue.update(fields={"labels": issue_labels})


if __name__ == "__main__":

    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    # issue_search_convert = jira.search_issues("labels = EPIC_OverDueDate1회", maxResults=1000)
    # Create New Jira Tickets

    labeledList = overDueLabeled()
    realTimeList = realTimeoverDueInitiative()
    deltaList = compareList(labeledList, realTimeList)

    for key in deltaList:
        initiative = jira.issue(key)
        print("############################################")
        print("대상initiative Key = " + initiative.key)
        delLabels(initiative)
