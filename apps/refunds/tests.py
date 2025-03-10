from django.test import TestCase
from django.contrib.auth.models import User
from apps.refunds.models import RefundRequest
from datetime import date
from django.core import mail


class RefundRequestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.refund = RefundRequest.objects.create(
            user=self.user,
            order_number="ORD12345",
            order_date=date.today(),
            first_name="John",
            last_name="Doe",
            phone_number="123456789",
            email="john.doe@example.com",
            country="USA",
            address="123 Main St",
            postal_code="12345",
            city="New York",
            products="Laptop",
            reason="Defective item",
            bank_name="Bank of America",
            account_type="private",
            iban="GB29NWBK60161331926819",
            iban_verified=False,
            status="pending",
        )

    def test_create_refund_request(self):
        """Checks that the refund request is created correctly"""
        self.assertEqual(RefundRequest.objects.count(), 1)
        self.assertEqual(self.refund.order_number, "ORD12345")
        self.assertEqual(self.refund.status, "pending")

    def test_refund_list_view(self):
        """Checks that the refund list is loaded for an authorized user"""
        response = self.client.get("/refunds/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ORD12345")

    def test_refund_detail_view(self):
        """Verifies that the detailed return page is loaded"""
        response = self.client.get(f"/refunds/{self.refund.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Defective item")

    def test_create_refund_view(self):
        """Checks the creation of a new return request through the form"""
        response = self.client.post(
            "/refunds/create/",
            {
                "order_number": "ORD67890",
                "order_date": "2025-01-01",
                "first_name": "Alice",
                "last_name": "Smith",
                "phone_number": "987654321",
                "email": "alice.smith@example.com",
                "country": "Canada",
                "address": "456 Another St",
                "postal_code": "54321",
                "city": "Toronto",
                "products": "Smartphone",
                "reason": "Wrong item received",
                "bank_name": "Royal Bank",
                "account_type": "private",
                "iban": "DE89370400440532013000",
            },
        )
        self.assertEqual(response.status_code, 302)  # Pending redirect
        self.assertTrue(RefundRequest.objects.filter(order_number="ORD67890").exists())

    def test_unauthorized_access_redirect(self):
        """Checks that an unauthorized user cannot see the list of returns"""
        self.client.logout()
        response = self.client.get("/refunds/")
        self.assertEqual(
            response.status_code, 302
        )  # There should be a redirect to login

    def test_iban_validation_api(self):
        """Checks IBAN validation API"""
        response = self.client.get("/api/validate-iban/?iban=GB29NWBK60161331926819")
        self.assertEqual(response.status_code, 200)
        self.assertIn("valid", response.json())

    def test_email_sent_on_status_change(self):
        """Check that the email is sent when the request status changes"""
        self.refund.status = "approved"
        self.refund.save()

        # Check that 1 email has appeared in the mailbox
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Updating the status of the return", mail.outbox[0].subject)
        self.assertIn("approved", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, ["john.doe@example.com"])

    def test_no_email_sent_if_status_not_changed(self):
        """Check that the email is NOT sent if the request status has not changed"""
        self.refund.save()
        self.assertEqual(len(mail.outbox), 0)

    def test_email_sent_on_rejection(self):
        """Verify that an email is sent when a request is rejected"""
        self.refund.status = "rejected"
        self.refund.save()

        # Check that 1 email has appeared in the mailbox
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Updating the status of the return", mail.outbox[0].subject)
        self.assertIn("rejected", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, ["john.doe@example.com"])
