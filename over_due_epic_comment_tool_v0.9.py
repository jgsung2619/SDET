import jira# import configuration  # .py file that I store my username/password/token/server domain
import sys
import os
import copy

# for Jira control
from jira import JIRA
from jira.exceptions import JIRAError

DevTracker = 'http://hlm.lge.com/issue'
QTracker = 'http://hlm.lge.com/qi'
ID = input("AD계정 : ")
PASSWORD = input("Passwd : ")

def dueOverComments(issue, initiative, initiative_owner, epic_owner, epicDict):

    epicURL = ""
    for key, value in epicDict.items():
        epicURL += "http://hlm.lge.com/issue/browse/" + key + " (EPIC Owner: [~"+value+"])\n"

    comments = "[~" + initiative_owner + "] Owner님." + """하기 Epic의 Due Date이 오늘이거나 지났습니다.
    EPIC Link 공유드리오니 완료여부 or 일정 Update 부탁드립니다.\n""" + epicURL
    jira.add_comment(issue.id, comments, visibility=None, is_internal=False)

def addLabels(issue):
    issue_labels = issue.fields.labels
    print(str(issue_labels))


    # if "EPIC_OverDueDate1회" not in issue_labels:
    #     issue_labels.append('EPIC_OverDueDate1회')
    # elif "EPIC_OverDueDate1회" in issue_labels:
    #     issue_labels.remove("EPIC_OverDueDate1회")
    #     issue_labels.append('EPIC_OverDueDate2회')
    # elif "EPIC_OverDueDate2회" in issue_labels:
    #     issue_labels.remove("EPIC_OverDueDate2회")
    #     issue_labels.append('EPIC_OverDueDate3회')
    issue_labels.append('EPIC_OverDueDate1회')
    issue.update(fields={"labels": issue_labels})


def findEpic(issue, initiative, initiative_owner):
    epicDict = {}
    #filter=48073 : 1_webOS_5.0_Epic_OverDue
    epic_search_convert = jira.search_issues('filter=48073 and issueFunction in linkedIssuesOf("key='+initiative+'")', maxResults=100)
    # epic_search_convert = jira.search_issues('filter=49518 and issueFunction in linkedIssuesOf("key='+initiative+'")', maxResults=100) #Test
    for key in epic_search_convert:
        epic = jira.issue(key)
        epic_key = epic.key
        epic_owner = ""
        try:
            epic_owner = epic.fields.assignee.name
        except:
            print("EPIC Owner 없음")
            epic_owner = initiative_owner
            pass
        epicDict[epic_key] = epic_owner

    print("overDueEPIC List: "+' '.join(map(str, epicDict)))
    dueOverComments(issue, initiative, initiative_owner, epic_owner, epicDict)

if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    #filter=49494 : 1_webOS_5.0_Epic_OverDue_Initiative_pm
    issue_search_convert = jira.search_issues("filter=49494", maxResults=100)
    # issue_search_convert = jira.search_issues("filter=49520", maxResults=100)
    print("### Over Due EPIC관리 필요 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.key
        issue_assignee = issue.fields.assignee.name # initiative Owner
        issue_summary = issue.fields.summary
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        findEpic(issue, issue_key, issue_assignee)
        addLabels(issue)
