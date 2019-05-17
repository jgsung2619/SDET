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


def planingComments(tc, assignee):

    comments = "[~" + assignee + """] Owner님! 본 Initiative는 이번 2019_IR2SP19 Sprint Demo 대상 항목입니다.
    하기와 같이 collab Page에 Demo 계획 수립 요청드립니다.
    부디 일정 준수 부탁드립니다.

    *Demo취합page:* http://collab.lge.com/main/pages/viewpage.action?pageId=955662722
    *기한: ~5/16(목), 오전 10시*

    Sprint Demo의 취지는 Milestone에 명시된 산출물과 DoD를 팀장님 주관하에 Review를 진행하는 것입니다.
    현물Demo가 가능한 건은 이번 Sprint기간 내 팀장님과 일정 조율하시어 Demo진행 부탁드립니다.
    현물Demo가 어려운 구조설계/TestCase/UX시나리오 등은 업무보고 형식의 Sprint Review로 대체해 주시면 됩니다.(팀 회의, 파트 회의 활용)
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)

def dueEmptyComments(tc, assignee):

    comments = "[~" + assignee + """] Owner님. Archi Jira 완료 계획 수립하시어 Due Date도 기입 부탁드립니다.
    Initiative 장단기 과제 분류에 따라 Release Sprint 최소 1개 or 2개 Sprint 이전까지 Archi Jira가 완료되셔야 합니다.

    [~sunjung87.hwang]선임님.
    본 Archi Jira의 설계 리뷰 가이드 지원 요청드립니다.
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)

if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    issue_search_convert = jira.search_issues("filter=49413", maxResults=100)
    print("### 관리대상 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.id
        issue_summary = issue.fields.summary
        issue_assignee = issue.fields.assignee.name
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        planingComments(issue, issue_assignee)
