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
filterNo = input("filter number : ")


def planingComments(tc, assignee):

    comments = "[~" + assignee + """] Owner님. 본 Initiative는 이번 2019_IR2SP21 Sprint Demo 대상 항목입니다.
    하기와 같이 collab Page에 Demo 계획 수립 요청드립니다.

    *Demo취합page:* http://collab.lge.com/main/pages/viewpage.action?pageId=987499094
    *기한: ~6/13(목), 오전 10시*

    Sprint Demo의 취지는 Milestone에 명시된 산출물과 DoD를 팀장님 주관하에 Review를 진행하는 것입니다.
    현물Demo가 가능한 건은 이번 Sprint기간 내 팀장님과 일정 조율하시어 Demo진행 부탁드립니다.
    현물Demo가 어려운 구조설계/TestCase/UX시나리오 등은 업무보고 형식의 Sprint Review로 대체해 주시면 됩니다.(팀 회의, 파트 회의 활용)
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)

def delayComments(tc, assignee):

    comments = "[~" + assignee + """] Owner님! 본 Initiative는 이번 2019_IR2SP21 Sprint Demo 대상 항목입니다.
    하기와 같이 collab Page에 Demo 계획 수립이 되지 않아 코멘트드립니다.
    되도록 오늘까지 계획 수립하시어 콜랩 업데이트 부탁드립니다.

    *Demo취합page:* http://collab.lge.com/main/pages/viewpage.action?pageId=987499094
    *기한: 금일 퇴근 전*

    Sprint Demo의 취지는 Milestone에 명시된 산출물과 DoD를 팀장님 주관하에 Review를 진행하는 것입니다.
    현물Demo가 가능한 건은 이번 Sprint기간 내 팀장님과 일정 조율하시어 Demo진행 부탁드립니다.
    현물Demo가 어려운 구조설계/TestCase/UX시나리오 등은 업무보고 형식의 Sprint Review로 대체해 주시면 됩니다.(팀 회의, 파트 회의 활용)
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)

if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    issue_search_convert = jira.search_issues("filter="+ filterNo +" and (labels not in (demo:sp21, demo:skip:sp21, demo:delay:sp21) or labels is empty)", maxResults=1000) # 계획 수립 지연
    print("### 관리대상 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.key
        issue_summary = issue.fields.summary
        issue_assignee = issue.fields.assignee.name
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        planingComments(issue, issue_assignee)
        # delayComments(issue, issue_assignee)
