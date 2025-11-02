from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestLogNoteDeleteRestrict(TransactionCase):

    def setUp(self):
        super().setUp()
        self.mail_model = self.env['mail.message']
        self.user_demo = self.env['res.users'].create({
            'name': 'Demo User',
            'login': 'demo@test.com',
            'email': 'demo@test.com',
        })
        # Create a sample log note
        self.log_note = self.mail_model.create({
            'body': 'This is a test log note',
            'model': 'res.partner',
            'message_type': 'comment',
        })

    def test_user_cannot_delete_log_note(self):
        """Ensure normal users cannot delete log notes."""
        mail_as_demo = self.mail_model.with_user(self.user_demo)
        with self.assertRaises(UserError):
            mail_as_demo.browse(self.log_note.id).unlink()

    def test_admin_can_delete_log_note(self):
        """Ensure admin can delete log notes successfully."""
        count_before = self.mail_model.search_count([])
        self.log_note.unlink()
        count_after = self.mail_model.search_count([])
        self.assertEqual(count_before - 1, count_after)

