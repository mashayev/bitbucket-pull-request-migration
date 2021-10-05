import os
import sys
import time
import click

from github import Github
from github import GithubException
import requests

github_client = Github(os.getenv("GITHUB_TOKEN"))
repository = sys.argv[1]
github_org_name = sys.argv[2]
bitbucket_org_name = sys.argv[3]
total_pull_requests = sys.argv[4]

def github_create_issue():
    repo = github_client.get_repo(f"{github_org_name}/{repository}")
    while True:
        try:
            time.sleep(1)
            tmp = repo.create_issue(title="Temp issue", body="lol")
            pr_info_from_bb = bitbucket_get_pull_request(repository, tmp.number)
        except GithubException as error:
            print("sleeping for 20s due to", error)
            time.sleep(20)
        else:
            break
    while True:
        try:
            # issue = repo.create_issue(title=pr_info_from_bb["title"], body=pr_info_from_bb["description"])
            time.sleep(1)
            tmp.edit(state="closed", title=pr_info_from_bb["title"], body=pr_info_from_bb["description"])
        except GithubException as error:
            print("sleeping for 20s due to", error)
            time.sleep(20)
        else:
            break
    return tmp.number


def bitbucket_get_pull_request(repo: str, pr_id: int):
    pull_request = requests.get(
        f"https://api.bitbucket.org/2.0/repositories/{bitbucket_org_name}/{repo}/pullrequests/{pr_id}",
        auth=(os.getenv("BITBUCKET_USER"), os.getenv("BITBUCKET_TOKEN")))
    body = pull_request.json()
    if body["merge_commit"] is not None:
        source_commit = body["merge_commit"]["hash"]
    else:
        source_commit = body["source"]["commit"]["hash"]
    source_branch = body["source"]["branch"]["name"]

    if body["destination"]["commit"] is None:
        dest_commit = body["destination"]["branch"]["name"]
    else:
        dest_commit = body["destination"]["commit"]["hash"]
    dest_branch = body["destination"]["branch"]["name"]

    diff_link = f"https://github.com/{github_org_name}/{repo}/compare/{dest_commit}...{source_commit}"
    if body["author"] is None:
        author = "Deleted"
    else:
        author = body["author"]["display_name"]
    reviewers = ", ".join([x["display_name"] for x in body["reviewers"]])
    approvers = ", ".join([x["user"]["display_name"] for x in body["participants"] if x['approved']])

    description = "\n" + "\n".join(
        [line for line in body["description"].replace("{: data-inline-card='' }", "").replace("\u200c", "").replace("\n\n", "\n").replace(f"https://bitbucket.org/{bitbucket_org_name}/{repo}/pull-requests/", f"https://github.com/{github_org_name}/{repo}/issues/").splitlines()])
    closed_on = body["updated_on"]

    description = f"""[Full Diff]({diff_link})
**Author:** {author}
**Reviewers:** {reviewers}
**Approvers:** {approvers}
**Source Branch:** [{source_branch}](https://github.com/{github_org_name}/{repo}/tree/{source_branch})
**Destination Branch:** [{dest_branch}](https://github.com/{github_org_name}/{repo}/tree/{dest_branch})
**Closed On:** {closed_on}
**Status:** {body['state']}
{description}
"""

    return {
        "title": body["title"].title(),
        "description": description
    }


with click.progressbar(length=int(total_pull_requests), label='Migrating issues') as bar:
    while True:
        issue_id = github_create_issue()
        bar.update(1, issue_id)
