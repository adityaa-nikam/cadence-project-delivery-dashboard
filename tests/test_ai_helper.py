import unittest
from unittest.mock import patch

from ai_helper import parse_update
from mock_data import MILESTONES, PROJECTS


class UpdateTransformationTests(unittest.TestCase):
    def setUp(self):
        self.project = next(project for project in PROJECTS if project.id == "orion")
        self.milestones = [milestone for milestone in MILESTONES if milestone.project_id == self.project.id]

    @patch("ai_helper._get_api_key", return_value="")
    def test_parser_returns_unknown_when_no_api_key(self, mock_key):
        """Without API key, parser returns fallback with error."""
        result = parse_update(
            "Maya says Firewall Access Approval is still stuck because IT has not approved access. Jake will follow up tomorrow.",
            self.milestones,
        )

        self.assertEqual(result["affected_milestone"], "Unknown")
        self.assertIsNone(result["new_status"])
        self.assertIn("...", result["summary"])
        self.assertIsNotNone(result["error"])
        self.assertIn("API_KEY not set", result["error"])

    @patch("ai_helper._get_api_key", return_value="")
    def test_parser_handles_offline_fallback(self, mock_key):
        """Parser handles text gracefully when offline."""
        result = parse_update(
            "good news, Fleet API Integration is finally done — Jake pushed the last commit yesterday.",
            self.milestones,
        )

        self.assertEqual(result["affected_milestone"], "Unknown")
        self.assertIsNone(result["new_status"])
        self.assertIn("...", result["summary"])
        self.assertIsNotNone(result["error"])


if __name__ == "__main__":
    unittest.main()