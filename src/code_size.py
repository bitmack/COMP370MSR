from github import Github
import pandas as pd
import json
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

# fetching all commits from repo
commits = repo.get_commits()
print("Total number of commits", commits.totalCount)  # for debugging purposes

# record urls tree for each commit , so we can fetch sha and code size using url of each commit
# example https://api.github.com/repos/mozilla-mobile/fenix/git/trees/f6256a928e3af27b01dcc367077fdf2fb83400ef
commits_trees_urls = []

for c in commits:
    url = {
        "commit_url": c.commit.tree.url,
    }
    commits_trees_urls.append(url)

each_commit_tree = []
counter = 0

# this loop iterates through each commit' url
for i in commits_trees_urls:
    link = i["commit_url"]
    if counter < 5000:  # prevents rate limit error

        i_tree = requests.get(link, auth=("ovusa", ACCESS_TOKEN))
        counter = counter + 1        

        if i_tree.status_code == 200:
            body = json.loads(i_tree.content)
           

        tree_body = body["tree"]
      
        for i in tree_body:
            subtree = {
                "tree_sha": body["sha"],
                "path": i["path"],
                "type": i["type"],
                "size": None,
            }
            try:
                subtree["size"] = i["size"]
            except:
                print("The subtree doesn't have code size field")

            each_commit_tree.append(subtree)

# writes data into csv file
code_size_record = pd.DataFrame(each_commit_tree)
code_size_record.to_csv("code_size.csv", sep=";", encoding="utf-8", index=True)