class Service:

    def __init__(self):
        pass

    def run_analysis(self, analysis_request) -> dict:
        pass

    def run_detection_rules(self, instance) -> dict:
        pass

    def run_fix_misconfiguration_rules(self, instance, detection_report: dict):
        pass

    def create_instance(self, credentials: dict):
        pass

    def create_summary_report(self, final_report) -> dict:
        pass
