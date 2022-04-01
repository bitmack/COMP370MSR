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
data.to_csv("pulled_issues_10K.csv", sep=";", encoding="utf-8", index=True)

print("Finish fetching issues")  # for debugging purposes

# fetching all commits from repo
commits = repo.get_commits()
print("Total number of commits", commits.totalCount)  # for debugging purposes

# record entities for each commits into the list
commits_record = []

# record urls tree for each commit , so we can fetch sha and code size using url of each commit
commits_trees_urls = []

for c in commits:
    commit = {
        "commit_author": c.commit.author.name,
        "commit_date": c.commit.author.date,
        "commit_url": c.commit.tree.url,
    }
    url = {
        "commit_url": c.commit.tree.url,
    }
    commits_trees_urls.append(url)
    commits_record.append(commit)

# wrrite commits into csv file
data = pd.DataFrame(commits_record)
data.to_csv("pulled_commits.csv", sep=";", encoding="utf-8", index=True)
print("Finish fetching commits")  # for debugging purposes

# example https://api.github.com/repos/mozilla-mobile/fenix/git/trees/f6256a928e3af27b01dcc367077fdf2fb83400ef
# the list collects all entities of tree for each commit (Commit ->url->tree-> sha/code size)
each_commit_tree = []

# this loop interates through each commit' url
for i in commits_trees_urls:

    # the loop iterates throught each litle tree of given commit to fetch code size and path, other attribues are for debugging purposes.
    # example above
    for each_tree in i.tree:
        tr = {
            "sha": each_tree.sha,
            "path": each_tree.tree.path,
            "commit_sha": each_tree.tree.sha,
            "size": each_tree.tree.size,
        }
    each_commit_tree.append(tr)

# write data into csv file
code_size_record = pd.DataFrame(each_commit_tree)
code_size_record.to_csv("code_size.csv", sep=";", encoding="utf-8", index=True)
print("Finish fetching trees")  # for debugging purposes
