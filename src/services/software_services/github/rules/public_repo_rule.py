from interfaces.rule import Rule


class PublicRepoRule(Rule):

    def __init__(self):
        super().__init__("Github Public Repository")

    def detect_misconfiguration(self, instance, *args, **kwargs) -> dict:

        detections = {}
        repositories = instance.get_user().get_repos()
        for repo in repositories:
            if not repo.private:
                print(f"Repository {repo.name} has public access")
                detections[repo.name] = True

        report_summary = {'rule': self.name,
                          'detection': detections,
                          'misconfiguration': len(detections) > 0}

        return report_summary

    def fix_misconfiguration(self,  instance, report, *args, **kwargs) -> dict:
        fixed_detections = {}

        for repo_name in report.get('detection').keys():
            repo = instance.git_repo(repo_name)
            repo.edit(private=True)
            fixed_detections[repo_name] = True
        report['fix_detection'] = fixed_detections

        return report
