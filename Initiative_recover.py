

import json  # .py file that I store my username/password/token/server domain
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


def findEPIClist(initiative):
    nowEpic = []
    initiativeKey = initiative.key
    epic_search = jira.search_issues('issuetype= EPIC and issueFunction in linkedIssuesOf("key=' + initiativeKey + '")', maxResults=1000)
    for key in epic_search:
        epicKey = jira.issue(key)
        nowEpic.append(epicKey.key)

    print("현재 Link된 EPIC List: "+' '.join(map(str, nowEpic)))
    compareEPIC(initiative, nowEpic, initiativeKey)


def compareEPIC(initiative, nowEpic, initiativeKey):
    priorEpic = []
    omitEpic = []
    # with open('myobj.json', 'rb') as f:
    #     root = json.load(f)

    # json_file = open('D:/initiative_DB_filterID_KeyListOnly_48233_2019-05-07T12-46-00.json').read()
    # json_data = json.loads(json_file)
    with open('D:/initiative_DB_filterID_KeyListOnly_45402_2019-05-07T12-31-00.json', 'rb') as json_file:
        json_data = json.loads(json_file.read())
    for k in json_data['issues']:
            if k['Initiative Key'] == initiativeKey:
                priorEpic = k["URL"]["EPIC_LINK"]["TOTAL"]["Total"]["keys"]
            elif k['Initiative Key'] != initiativeKey: continue

    print("기존에 Link된 EPIC List: "+' '.join(map(str, priorEpic)))
    omitEpic = list(set(priorEpic) - set(nowEpic))
    print("#Link되어야 할 EPIC List: "+' '.join(map(str, omitEpic)))
    try:
        for e in omitEpic:
            addLink(e, initiative)
    except:
        print("error발생")
        pass


def addLink(epic, initiative):
    jira.create_issue_link('is published by', epic, initiative)


if __name__ == "__main__":

    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    issue_search_convert = jira.search_issues("filter=45402", maxResults=1000)
    # Create New Jira Tickets

    for key in issue_search_convert:
        initiative = jira.issue(key)
        print("############################################")
        print("대상initiative Key = " + initiative.key)
        findEPIClist(initiative)
