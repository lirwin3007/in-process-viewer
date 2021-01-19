from github import Github

# using username and password
gh = Github("user", "password")

# or using an access token
#gh = Github("access_token")

# Github Enterprise with custom hostname
#gh = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")
