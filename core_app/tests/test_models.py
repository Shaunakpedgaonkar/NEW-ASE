from django.test import TestCase
from core_app.models import Incident, User, Image

class IncidentModelTest(TestCase):
    def test_incident_creation(self):
        incident = Incident.objects.create(
            location="Test Location",
            description="Test Description",
            incident_type="Test Type",
            occur_time="2024-02-06T12:00:00Z",
            status="Test Status",
            traffic_status="Test Traffic Status",
            scale_impact="Test Scale Impact",
            extrainfo={"additional_info": "Test Additional Info"}
        )
        self.assertEqual(incident.location, "Test Location")

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            email="tests@example.com",
            password="testpassword",
            role="Test Role"
        )

        self.assertEqual(user.email, "tests@example.com")

class ImageModelTest(TestCase):
    def test_image_creation(self):
        image = Image.objects.create(
            image="test_upload.jpeg"
        )

        self.assertEqual(image.image, "test_upload.jpeg")


# How to run
# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py test core_app.tests
# python3 manage.py test core_app.tests --keepdb  # store the test db