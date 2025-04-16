from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import City, IDC, Host, HostStat, HostPasswordHistory
from unittest.mock import patch


class HostMgrTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="testuser", password="123456")
        self.token = Token.objects.create(user=self.user)
        self.client.defaults['HTTP_AUTHORIZATION'] = f"Token {self.token.key}"

        self.city = City.objects.create(name="Shanghai")
        self.idc = IDC.objects.create(name="IDC-A", city=self.city)
        self.host = Host.objects.create(
            hostname="host1",
            ip="127.0.0.1",
            root_password="oldpassword",
            idc=self.idc
        )

    def test_create_city(self):
        res = self.client.post("/api/cities/", {"name": "Beijing"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(City.objects.count(), 2)

    def test_update_host(self):
        res = self.client.patch(
            f"/api/hosts/{self.host.id}/",
            content_type="application/json",
            data='{"hostname": "updated-host"}'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Host.objects.get(id=self.host.id).hostname, "updated-host")

    def test_ping_host(self):
        with patch("subprocess.run") as mocked_ping:
            mocked_ping.return_value.returncode = 0
            res = self.client.get(f"/api/ping/{self.host.id}/")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()['reachable'], True)

    def test_password_rotation_task(self):
        from .tasks import rotate_root_passwords
        rotate_root_passwords()
        self.host.refresh_from_db()
        self.assertNotEqual(self.host.root_password, "oldpassword")
        self.assertEqual(HostPasswordHistory.objects.filter(host=self.host).count(), 1)
        self.assertEqual(
            HostPasswordHistory.objects.filter(host=self.host)[0].root_password,
            "oldpassword"
        )

    def test_daily_host_stats(self):
        from .tasks import daily_host_stats
        daily_host_stats()

        stats = HostStat.objects.all()
        self.assertEqual(stats.count(), 1)

        stat1 = HostStat.objects.get(idc=self.idc)
        self.assertEqual(stat1.city, self.city)
        self.assertEqual(stat1.count, 1)

    def test_request_duration_header(self):
        res = self.client.get("/api/hosts/")
        self.assertIn("X-Request-Duration", res.headers)
