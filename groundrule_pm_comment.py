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


def overdueComments(tc, assignee):

    comments = "[~" + assignee + "]owner님. 본 설계 리뷰 대상 Initiative는 현재 Inprogress상태이나 Archi Jira의 Status는 아직 준비단계(Scoping, Review)입니다." + """
    Archi Jira 일정 가이드에 따라 조속히 [~sunjung87.hwang]선임님께 Archi Jira 리뷰 요청하시어 본 Archi JIRA 역시 In Progress로 진입 요청드립니다.

    [~sunjung87.hwang]선임님.
    본 Archi Jira의 설계 리뷰 진척되도록 도움 요청드립니다.
    """
    jira.add_comment(tc.id, comments, visibility=None, is_internal=False)


if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    issue_search_convert = jira.search_issues("key=TVPLAT-19005", maxResults=100)
    print("### 관리대상 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.id
        issue_summary = issue.fields.summary
        issue_assignee = issue.fields.assignee.name
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        overdueComments(issue, issue_assignee)
