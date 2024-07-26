import requests


class GatWayService:

    def __init__(self, services, database, notification_service, credentials_service):
        self.services = services
        self.database = database
        self.notification_service = notification_service
        self.credentials_service = credentials_service

    def get_credentials(self, platform, organization):
        credentials = self.credentials_service.get_credentials(platform, organization)
        return credentials

    # async tasks
    def create_task(self, analysis_request):
        task_credentials = self.get_credentials(analysis_request.get('platform'),
                                                analysis_request.get('organization'))
        scan_report = self.forward_request_to_relevant_service(analysis_request, task_credentials)
        self.write_scan_report_to_db(scan_report)
        self.notify_organization_users(scan_report)
        return task_credentials

    def forward_request_to_relevant_service(self, request, credentials):
        service = self.services.get(request.get('service'))
        response = requests.post(service, data={'credentials': credentials})
        return response

    def write_scan_report_to_db(self, report):
        self.database.write_results_to_db(report)

    def notify_organization_users(self, detection_report):
        self.notification_service.send_notification(detection_report)