from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from core_app.models import Incident

class EditStatusViewTest(TestCase):
    def setUp(self):
        self.incident = Incident.objects.create(location="Test Location", description="Test Description", incident_type="Test Type", occur_time="2024-02-06T12:00:00Z", status="Test Status", traffic_status="Test Traffic Status", scale_impact="Test Scale Impact")

    def test_edit_status_successful(self):
        url = reverse('edit_status', args=[self.incident.id, self.incident.status])
        response = self.client.post(url, {'new_status': 'New Test Status'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.incident.refresh().status, 'New Test Status')

    def test_edit_status_incident_not_found(self):
        url = reverse('edit_status', args=[999, 'Test Status'])
        response = self.client.post(url, {'new_status': 'New Test Status'})
        self.assertEqual(response.status_code, 404)

    def test_edit_status_invalid_request_method(self):
        url = reverse('edit_status', args=[self.incident.id, self.incident.status])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

class ReportIncidentViewTest(TestCase):
    def test_report_incident_successful(self):
        url = reverse('report_incident')
        response = self.client.post(url, {'location': 'Test Location', 'description': 'Test Description', 'category': 'Test Category', 'impactScale': 'Test Impact Scale'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Incident.objects.count(), 1)

    def test_report_incident_get_request(self):
        url = reverse('report_incident')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
