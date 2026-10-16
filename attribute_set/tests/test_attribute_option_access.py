# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestAttributeOptionAccess(TransactionCase):
    """The value_ref selection lists ir.model records, which only administrators can read.

    Since value_ref is no longer restricted to base.group_erp_manager, fields_get()
    computes this selection for every user opening an attribute or option view.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(cls.env, login="attribute_option_user", groups="base.group_user")

    def test_selection_model_list_as_internal_user(self):
        selection = self.env["attribute.option"].with_user(self.user)._selection_model_list()
        self.assertIn("res.partner", dict(selection))

    def test_fields_get_as_internal_user(self):
        fields = self.env["attribute.option"].with_user(self.user).fields_get(["value_ref"], ["selection"])
        self.assertIn("res.partner", dict(fields["value_ref"]["selection"]))
