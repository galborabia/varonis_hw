from github import Github, Auth
import os
import time

repo_name = "galborabia/varonis_hw"

github_token = os.environ.get("GITHUB_TOKEN")

authentication = Auth.Token(github_token)


github_instance = Github(auth=authentication)

repo = github_instance.get_repo(repo_name)
print(f"Repository {repo.name}, private settings is set to - {repo.private}")

if not repo.private:
    repo.edit(private=True)
    if repo.private:
        print(f"Repository {repo.name} updated to be private repository successfully")


# Change back to public for training, sleep because it's raise error that it's already edit
time.sleep(2)
repo.edit(private=False)