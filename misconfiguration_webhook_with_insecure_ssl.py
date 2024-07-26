from github import Github, Auth
import os


repo_name = os.environ.get("REPO_NAME", "galborabia/varonis_hw")
github_token = os.environ.get("GITHUB_TOKEN")

hook_id = 492273059

authentication = Auth.Token(github_token)

github_instance = Github(auth=authentication)

repo = github_instance.get_repo(repo_name)

webhook = repo.get_hook(id=hook_id)

insecure_ssl = webhook.config.get('insecure_ssl') == '1'
use_secrets = webhook.config.get('secret')

print(f"Webhook {webhook.id} configuration is - {webhook.config}")

if insecure_ssl:
    webhook_config = webhook.config
    webhook_config['insecure_ssl'] = '0'
    webhook.edit(config=webhook_config, name='web')

    if webhook.config.get('insecure_ssl') == '0':
        print(f"Webhook - {webhook.id} is updated to use SSL successfully")

if not use_secrets:
    print(f"Webhook - {webhook.id} is not use secret token.")

# change webhook config for training
webhook_config = webhook.config
webhook_config['insecure_ssl'] = '1'
webhook.edit(config=webhook_config, name='web')
