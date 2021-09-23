docker build -t migration .

export GITHUB_TOKEN=<Add your GITHUB_TOKEN>
export BITBUCKET_USER=<Add your BITBUCKET_USER>
export BITBUCKET_TOKEN=<Add your BITBUCKET_TOKEN>


docker run -e GITHUB_TOKEN -e BITBUCKET_USER -e BITBUCKET_TOKEN --rm -it migration python migrate.py "$1"
