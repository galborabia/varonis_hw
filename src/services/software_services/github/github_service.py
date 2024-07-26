from interfaces.service import Service
from services.software_services.github.rules.public_repo_rule import PublicRepoRule
from services.software_services.github.rules.webhook_with_insecure_ssl import WebHookWithInsecureSSL
from github import Github, Auth


class GitHubService(Service):

    def __init__(self):
        super().__init__()
        self.rules = self._init_rules()

    def _init_rules(self):
        rules = {PublicRepoRule(),
                 WebHookWithInsecureSSL()}

        rules = {rule.get_name(): rule for rule in rules}

        return rules

    def run_analysis(self, analysis_request) -> dict:
        instance = self.create_instance(analysis_request.get('credentials'))
        detection_report = self.run_detection_rules(instance)
        fixing_report = self.run_fix_misconfiguration_rules(instance, detection_report)
        summary_report = self.create_summary_report(fixing_report)
        return summary_report

    def run_detection_rules(self, instance):
        analysis_report = {}
        for rule_name, rule in self.rules.items():
            rule_report = rule.detect_misconfiguration(instance)
            if rule_report.get('misconfiguration'):
                analysis_report[rule_name] = rule_report

        return analysis_report

    def run_fix_misconfiguration_rules(self, instance, detection_report: dict):
        fixing_report = {}
        for rule_name, rule_report in detection_report.items():
            rule = self.rules.get(rule_name)
            rule_fixing_report = rule.fix_misconfiguration(instance, rule_report)
            fixing_report[rule_name] = rule_fixing_report

        return fixing_report

    def create_instance(self, credentials: dict):
        authentication = Auth.Token(**credentials)
        instance = Github(auth=authentication)
        return instance

    def create_summary_report(self, final_report):
        print("Summary report")
        return final_report