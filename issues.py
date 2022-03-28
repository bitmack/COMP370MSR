from github import (
    Github,
    GithubException,
    BadCredentialsException,
    UnknownObjectException,
    BadUserAgentException,
    RateLimitExceededException,
    BadAttributeException,
)
import pandas as pd
import requests
import time
from datetime import datetime
from Secret.Secret_Token import ACCESS_TOKEN

g = Github(ACCESS_TOKEN, per_page=100, retry=20)


repo = g.get_repo("mozilla-mobile/fenix")
all_issues = repo.get_issues(
    state="all", sort="created", direction="asc"
)  # object with all issues
print("Total number of issues", all_issues.totalCount)

issues_record = []
count = 0

for issue in all_issues:
    if count >= 5000:
        break
    else:
        issue = {
            "issue_id": issue.id,
            "issue_title": issue.title,
            "issue_state": issue.state,
            "issue_label": issue.labels,
            "closed_at": issue.closed_at,
            "created_at": issue.created_at,
            "locked": issue.locked,
            "issue_comments": issue.comments,
        }
        count = count + 1
    issues_record.append(issue)

data = pd.DataFrame(issues_record)
data.to_csv("pulled_issues2.csv", sep=";", encoding="utf-8", index=True)

print("the end")
