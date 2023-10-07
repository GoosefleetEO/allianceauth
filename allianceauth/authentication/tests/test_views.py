import json
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from allianceauth.authentication.views import task_counts
from allianceauth.tests.auth_utils import AuthUtils

MODULE_PATH = "allianceauth.authentication.views"


def jsonresponse_to_dict(response) -> dict:
    return json.loads(response.content)


@patch(MODULE_PATH + ".queued_tasks_count")
@patch(MODULE_PATH + ".active_tasks_count")
class TestRunningTasksCount(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.user = AuthUtils.create_user("bruce_wayne")

    def test_should_return_data(
        self, mock_active_tasks_count, mock_queued_tasks_count
    ):
        # given
        mock_active_tasks_count.return_value = 2
        mock_queued_tasks_count.return_value = 3
        request = self.factory.get("/")
        request.user = self.user
        # when
        response = task_counts(request)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            jsonresponse_to_dict(response), {"tasks_running": 2, "tasks_queued": 3}
        )
