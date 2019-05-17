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

def tcComments(issue, assignee):

    comments = "[~" + assignee + """] Owner님. 본 TestCase 활용하시어 본인의 EPIC/Story검증이 필요합니다.
    [RMS 7161] Smart STB Controller(SSC) webOS 4.5 적용 Delivery가 다음주 금요일(5/24)로 예정되어 있습니다.
    하위 EPIC과 Story의 TC 검증 결과 없이는 Initiative Delivery가 불가능하오니 Test Case 작성하시어 개발자 검증 진행 부탁드립니다.
    만약 검증이 불필요한 Story이거나 기존 TC로 검증이 가능한 경우라면 회신 부탁드립니다.
    EPIC TC로 Story검증이 모두 가능한 건지요?

    CC: [~jinyoung76.choi]책임님"""
    jira.add_comment(issue.id, comments, visibility=None, is_internal=False)


if __name__ == "__main__":
    # jira Handle open
    jira = JIRA(DevTracker, basic_auth=(ID, PASSWORD))
    issue_search_convert = jira.search_issues("key in (TVDEVTC-11349,TVDEVTC-7197,TVDEVTC-7198,TVDEVTC-7199,TVDEVTC-7200)", maxResults=100)
    print("### 관리대상 이니셔티브 ###")
    # Create New Jira Tickets
    for key in issue_search_convert:
        issue = jira.issue(key)
        issue_key = issue.id
        issue_summary = issue.fields.summary
        issue_assignee = issue.fields.assignee.name
        print('{} : {} ({})'.format(issue_key, issue_summary, issue_assignee))
        tcComments(issue, issue_assignee)
