from odoo.tests.common import TransactionCase

class TestFieldServiceCalendarFilter(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create two users
        self.user_1 = self.env['res.users'].create({
            'name': 'User One',
            'login': 'userone@test.com',
        })
        self.user_2 = self.env['res.users'].create({
            'name': 'User Two',
            'login': 'usertwo@test.com',
        })

        # Create two test tasks
        self.task_1 = self.env['fieldservice.task'].create({
            'name': 'Repair Job 1',
            'user_id': self.user_1.id,
        })
        self.task_2 = self.env['fieldservice.task'].create({
            'name': 'Repair Job 2',
            'user_id': self.user_2.id,
        })

    def test_filter_assigned_to_user(self):
        """Test filtering by Assigned To (user_id)"""
        tasks_user1 = self.env['fieldservice.task'].search([('user_id', '=', self.user_1.id)])
        self.assertIn(self.task_1, tasks_user1)
        self.assertNotIn(self.task_2, tasks_user1)

    def test_filter_assigned_to_multiple_users(self):
        """Test filtering by multiple users"""
        tasks = self.env['fieldservice.task'].search([('user_id', 'in', [self.user_1.id, self.user_2.id])])
        self.assertIn(self.task_1, tasks)
        self.assertIn(self.task_2, tasks)

    def test_no_filter_shows_all(self):
        """Test when no filter is applied"""
        all_tasks = self.env['fieldservice.task'].search([])
        self.assertIn(self.task_1, all_tasks)
        self.assertIn(self.task_2, all_tasks)
