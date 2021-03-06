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
from Secret.Secret_Token import ACCESS_TOKEN

g = Github(ACCESS_TOKEN, per_page=100, retry=20)

repo = g.get_repo("mozilla-mobile/fenix")
commits = repo.get_commits()
print(commits.totalCount)

commits_record = []
for c in commits:
    commit = {
        "commit_author": c.commit.author.name,
        "commit_date": c.commit.author.date,
        "commit_url": c.commit.tree.url,
    }
   
    commits_record.append(commit)


data = pd.DataFrame(commits_record)
data.to_csv("commits.csv", sep=";", encoding="utf-8", index=True)
