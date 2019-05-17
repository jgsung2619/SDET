# import configuration  # .py file that I store my username/password/token/server domain
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

# # .txt file to description
# f = open("D:/epic_tc.txt", 'r')
# epicDescription = f.read()
# f.close()
#
# f = open("D:/story_tc.txt", 'r')
# storyDescription = f.read()
# f.close()

def addWatchers(tc):
    jira.add_watcher(tc.id, "goosung.jung")
    jira.add_watcher(tc.id, "boyoung.cho")
    jira.add_watcher(tc.id, "ikju.kim")
    jira.add_watcher(tc.id, "jaegyo.seo")
    jira.add_watcher(tc.id, "jeonggeun.lim")
    jira.add_watcher(tc.id, "soohyun0131.lee")
    jira.add_watcher(tc.id, "sungbin.na")
    jira.add_watcher(tc.id, "wonjune.gong")
    jira.add_watcher(tc.id, "yj74.kim")

# 아래 코멘트는 본인 입맛에 맞게 수정하여 사용
def addComments(tc, assignee):

    comments = "[~" + assignee + """] Owner님. webOS4.5 MR부터 자기완결형 개발 문화 정착을 위해 SDET/개발SE에서 개발자 검증 강화 활동을 지원해 드리고 있습니다.
    주로 개발자 분들이 직접 작성하신 Test Case 리뷰 활동과 검증 활동이 주가 될 것입니다. 자세한 건 유선으로 연락드리거나 필요하면 직접 찾아뵙고 설명드리도록 하겠습니다.
    일단, 본 TC Sample을 보시고 향후 어떤 개발과제든 Initiative로 개발하실 때, EPIC과 Story에 하기 양식에 맞게 zephyr 등록하시면 됩니다.
    (해당 Initiative에도 SDET/STE 담당자가 지정되어 지원해 드릴 예정입니다.)

    *Test수행방법*
    Test수행 시 Execution클릭하시어 STEP별 Pass/Fail 판정하시고,
    이슈가 발생하면 해당 STEP 우측 comment란에 기술해 주세요. (별도 Issue Jira 생성X)
    해당 이슈를 기준으로 TC를 업데이트 해나가시는 것도 좋은 방법중 하나입니다.
    그리고 한 번 만들어진 TC는 다른 플랫폼에서도 재사용 가능하오니, 지속 modify해가면서 업데이트 활용하셔도 좋습니다.

    {panel}
    Story TC Sample : http://hlm.lge.com/issue/browse/TVDEVTC-2574
    EPIC TC Sample : http://hlm.lge.com/issue/browse/TVDEVTC-3738
    {panel}
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)

def addLink(tc, target) :
    jira.create_issue_link('is a testcase for',tc, target)

def creatJira(issue, epicTC, storyTC):
    # issue information
    issue_type = issue.fields.issuetype.name
    issue_summary = issue.fields.summary
    issue_assignee = issue.fields.assignee.name
    TC_summary = ""
    description = ""
    print('{}: {} ({})'.format(issue_type, issue_summary, issue_assignee))

    # distinguish Issue Type
    if issue_type == "Initiative":
        TC_summary = "[Initiativ_TC] " + issue_summary + " 검증 Test Case"
        description = epicTC.fields.description

    elif issue_type == "Epic":
        TC_summary = "[EPIC_TC]" + issue_summary + " 검증 Test Case"
        description = epicTC.fields.description
    else:
        TC_summary = "[Story_TC]" + issue_summary + " 검증 Test Case"
        description = storyTC.fields.description

    jira_dict_convert = {
        'project': {'key': 'TVDEVTC'},
        'summary': TC_summary,
        'assignee': {'name': issue_assignee},
        'reporter': {'name': ID},
        'issuetype': {"name": "Test"},
        'description': description,

        # 'customfield_12761': SomeCustomFieldValue
    }
    new_tc = jira.create_issue(jira_dict_convert)

    # add watchers
    addWatchers(new_tc)
    # add comments
    addComments(new_tc, issue_assignee)
    # add comments
    addLink(new_tc, issue)

def checkMyTestCase():
    for issue in jira.search_issues('reporter = currentUser() AND created >= startOfDay() AND issuetype = test ORDER BY created DESC', maxResults=10):
        print('{}: {}'.format(issue.key, issue.fields.summary))


if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    epicSampleTC = jira.issue("TVDEVTC-3738", fields='description')
    storySampleTC = jira.issue("TVDEVTC-2574", fields='description')

    issue_search_convert = jira.search_issues("filter=48947", maxResults=1000)
    print("### 검증 대상 EPIC & STORY ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        creatJira(issue,epicSampleTC,storySampleTC)
    # jira create
    print("\n### 오늘 생성한 Test Case List ###")
    checkMyTestCase()
