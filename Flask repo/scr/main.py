from github import Github
import pandas as pd
import requests
import json

# from Secret.Secret_Token import ACCESS_TOKEN  # authentication token from Github
ACCESS_TOKEN = " "
# using PyGithub library
g = Github(ACCESS_TOKEN, per_page=100, retry=20)

# fetch a repo as an object
repo = g.get_repo("pallets/flask")
# https://github.com/pallets/flask

# fetch all issues as an object
all_issues = repo.get_issues(state="all", sort="created", direction="asc")  # object with all issues
print("Total number of issues", all_issues.totalCount)  # for debugging purposes

issues_record = []
# count value below limits number of issues
count = 0
for issue in all_issues:
    if count > 10000 and issue.pull_request is not None:
        break
    else:
        issue = {
            "issue_id": issue.id,
            "issue_title": issue.title,
            "issue_state": issue.state,
            "issue_assignees": issue.assignees,
            "nummber_assignees":len(issue.assignees),
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
data.to_csv("issues_flask.csv", sep=";", encoding="utf-8", index=True)



# fetching commits from repo
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

# write commits into csv file
data = pd.DataFrame(commits_record)
data.to_csv("commits.csv", sep=";", encoding="utf-8", index=True)

each_commit_tree = []
code_sizeS = []
counter = 0
# this loop interates through each commit' url
for i in commits_trees_urls:
#     link = i["commit_url"]
#     if counter < 5000:  # prevents rate limit error
#         print("Count is", counter)

#         final_sum = 0

#         i_tree = requests.get(link, auth=("ovusa", ACCESS_TOKEN))

#         counter = counter + 1
#         if i_tree.status_code == 200:
#             body = json.loads(i_tree.content)

#             comit_size = {
#                 "tree_sha": body["sha"],
#                 "size": None,
#             }

#         var1 = body["tree"]
#         print("Length of the tree", len(var1))
#         for i in var1:

#             try:
#                 final_sum = final_sum + i["size"]
#             except:
#                 print("this subtree doesnt have code")

#     comit_size["size"] = final_sum
#     each_commit_tree.append(comit_size)

# # writes data into csv file
# code_size_record = pd.DataFrame(each_commit_tree)
# code_size_record.to_csv("commit_size.csv", sep=";", encoding="utf-8", index=True)
# print("Finish fetching trees")  # for debugging purposes
