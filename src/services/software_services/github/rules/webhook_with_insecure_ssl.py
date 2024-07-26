from interfaces.rule import Rule


class WebHookWithInsecureSSL(Rule):

    def __init__(self):
        super().__init__("WebHook with Insecure SSL")

    def detect_misconfiguration(self, instance, *args, **kwargs) -> dict:

        detections = {}
        repositories = instance.get_user().get_repos()
        for repo in repositories:
            repo_misconfigured_webhook = []
            webhooks = repo.get_hooks()
            for webhook in webhooks:
                insecure_ssl = webhook.config.get('insecure_ssl') == '1'
                if insecure_ssl:
                    repo_misconfigured_webhook.append(webhook.id)
                    print(f"Repo {repo.name} has insecure ssl to Webhook {webhook.id}")
                    detections[repo.name] = repo_misconfigured_webhook

        report_summary = {'rule': self.name,
                          'detection': detections,
                          'misconfiguration': len(detections) > 0}

        return report_summary

    def fix_misconfiguration(self, instance, report, *args, **kwargs):
        fix_detections = {}
        for repo_name, webhooks in report.get('detection').items():
            repo = instance.git_repo(repo_name)
            fixed_webhooks = []
            for webhook_id in webhooks:
                webhook = repo.get_hook(id=webhook_id)
                webhook_config = webhook.config
                webhook_config['insecure_ssl'] = '0'
                webhook.edit(config=webhook_config, name='web')
                fixed_webhooks.append(webhook_id)
            fix_detections[repo.name] = fixed_webhooks

        report['fix_detection'] = fix_detections
