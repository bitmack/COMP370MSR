from github import Github
import pandas as pd
import requests
from Secret.Secret_Token import ACCESS_TOKEN  # authentication token from Github

# using PyGithub library
g = Github(ACCESS_TOKEN, per_page=100, retry=20)

# fetch a repo with all info as an object
repo = g.get_repo("mozilla-mobile/fenix")

# fetch all issues as an object
all_issues = repo.get_issues(
    state="all", sort="created", direction="asc"
)  # object with all issues
print(
    "Total number of issues", all_issues.totalCount
)  # the statment mostly for debugging purposes

# fetching issues' entotites into the list
issues_record = []
# coutn value below  limits number of issues
count = 0
for issue in all_issues:
    if count >= 10000 and issue.pull_request is not None:
        break
    else:
        issue = {
            "issue_id": issue.id,
            "issue_title": issue.title,
            "issue_state": issue.state,
            "issue_assignees": issue.assignees,
            "issue_label": issue.labels,
            "closed_at": issue.closed_at,
            "created_at": issue.created_at,
            "locked": issue.locked,
            "issue_comments": issue.comments,
        }
        count = count + 1
        # append record to a list
    issues_record.append(issue)


data = pd.DataFrame(issues_record)
data.to_csv("issues_10K.csv", sep=";", encoding="utf-8", index=True)

