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


def scopingComments(tc, assignee):

    comments = "[~" + assignee + "]owner님. 본 설계 리뷰 대상 Initiative는 현재 Inprogress상태이나 Archi Jira는 아직 Scoping단계입니다." + """
    Archi Jira 일정 가이드에 따라 Review 준비하시어 조속히 [~sunjung87.hwang]선임님께 Review 요청 부탁드립니다.

    [~sunjung87.hwang]선임님.
    본 Archi Jira의 설계 리뷰 진척되도록 도움 요청드립니다.

    CC: [~gold.keum]책임님, [~boyoung.cho]책임님, [~changwook.im]책임님.
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)

def dueEmptyComments(archi, assignee):

    comments = "[~" + assignee + """] Owner님. Archi Jira 완료 계획 수립하시어 Due Date도 기입 부탁드립니다.
    Initiative 장단기 과제 분류에 따라 Release Sprint 최소 1개 or 2개 Sprint 이전까지 Archi Jira가 완료되셔야 합니다.

    [~sunjung87.hwang]선임님.
    본 Archi Jira의 설계 리뷰 가이드 지원 요청드립니다.
    """
    jira.add_comment(archi.id, comments, visibility=None, is_internal=False)

def statusSummaryComments(initiative, assignee):

    comments = "[~" + assignee + """] Owner님. 4/29~5/3주차 Status Summary 업데이트 부탁드립니다.

    {panel: title=Ground Rule: 주단위 Status Summary 업데이트}
    Approved단계 이후부터는 주단위 Status Summary Update가 필요합니다.
    일정 기간 공수 투입없는 개발 대기 기간이 있으신 경우, Status Summary란에 개발 시작 일정을 명시해 주시기 바랍니다.
    {panel}
    """
    jira.add_comment(initiative.id, comments, visibility=None, is_internal=False)

    # jira.update(fields={'customfield_10100': "[5/7] 4/29~5/3주차 Status Summary 업데이트 필요\n" + status_summary)

def statusSummaryUpdate(issue, status_summary):
    if(status_summary == Null){
    
    }



if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    issue_search_convert = jira.search_issues("filter=48941", maxResults=100)
    print("### 관리대상 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.id
        issue_summary = issue.fields.summary
        issue_assignee = issue.fields.assignee.name
        issue_statusSummary = issue.fields.customfield_15710
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        statusSummaryComments(issue, issue_assignee,issue_statusSummary)
        statusSummaryUpdate(issue, issue_statusSummary)
