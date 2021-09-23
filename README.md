# bitbucket-pull-request-migration
Bitbucket pull requests migration to GitHub issues

##### Run this command to start the migration
- Clone the repostiry to your local env
- Change run.sh export variables according to your environment
```bash
export GITHUB_TOKEN=<Add your GITHUB_TOKEN>
export BITBUCKET_USER=<Add your BITBUCKET_USER>
export BITBUCKET_TOKEN=<Add your BITBUCKET_TOKEN>
```
- Run the migration script with proper arguments
```bash
./run.sh <repository_name> <github_org_name> <bitbucket_org_name> <total_pull_requests>
```
##### In the new Github repositry it should create issue with the below inforamtion:
```txt
Full Diff - <Here it will create a link to the diff between master and destination branch>
Author: <Name>
Reviewers: <Reviewers name 1>, <Reviewers name 2>
Approvers: <Approvers name 1>, <Approvers name 1>
Source Branch: <Branch name>
Destination Branch: master
Closed On: 2021-09-19T08:47:04.149338+00:00
Status: MERGED / OPEN

added <PR title / description>
```
