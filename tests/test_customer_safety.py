import unittest

from components.update_feed import customer_safe_updates
from mock_data import MILESTONES, UPDATES


class CustomerSafetyTests(unittest.TestCase):
    def test_customer_feed_excludes_updates_linked_to_internal_milestones(self):
        project_id = "orion"
        visible_titles = {
            milestone.title
            for milestone in MILESTONES
            if milestone.project_id == project_id and not milestone.internal_only
        }
        project_updates = [update for update in UPDATES if update.project_id == project_id]

        filtered = customer_safe_updates(project_updates, visible_titles)

        self.assertTrue(filtered)
        self.assertTrue(all(update.affected_milestone in visible_titles for update in filtered))


if __name__ == "__main__":
    unittest.main()
