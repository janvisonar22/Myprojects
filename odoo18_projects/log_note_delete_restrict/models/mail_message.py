from odoo import api, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def unlink(self):
        """Prevent normal users from deleting log notes."""
        for record in self:
            # Allow admins only
            if not self.env.user.has_group('base.group_system'):
                raise UserError(
                    _("You are not allowed to delete log notes. "
                      "Only Administrators can perform this action."))
            else:
                # Log audit info
                _logger.warning(
                    "Log Note ID %s deleted by %s (User ID: %s)",
                    record.id,
                    self.env.user.name,
                    self.env.user.id,
                )
        return super(MailMessage, self).unlink()

