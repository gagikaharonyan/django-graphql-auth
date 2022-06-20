from graphql_auth.constants import Messages
from .testCases import RelayTestCase, DefaultTestCase


class BlockUserTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="foo@email.com", username="foo", verified=False, first_name="foo"
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True, first_name="bar"
        )
        self.user_super = self.register_user(
            email="gaa@email.com", username="gaa", verified=True, first_name="gaa", is_superuser=True,
        )

    def test_block_account(self):
        variables = {"user": self.user_super, 'user_id': self.user1.id}
        query_variables = {'user_id': self.user1.id, }
        executed = self.make_request(self.get_query(), variables, query_variables=query_variables)
        self.assertEqual(executed["success"], True)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.status.blocked)

        query_variables = {'user_id': self.user1.id, 'unblocking': False}
        executed = self.make_request(self.get_query(), variables, query_variables=query_variables)
        self.assertEqual(executed["success"], True)
        self.assertFalse(executed["unblocked"])
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.status.blocked)

    def test_block_account_with_none_superuser(self):
        variables = {"user": self.user2}
        query_variables = {'user_id': self.user1.id, }
        executed = self.make_request(self.get_query(), variables, query_variables=query_variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED)
        self.user1.refresh_from_db()
        self.assertFalse(self.user1.status.blocked)

    def test_unblock_account(self):
        variables = {"user": self.user_super}
        query_variables = {'user_id': self.user1.id, 'unblocking': True}
        executed = self.make_request(self.get_query(), variables, query_variables=query_variables)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["unblocked"])

        query_variables = {'user_id': self.user1.id, 'unblocking': True}
        executed = self.make_request(self.get_query(), variables, query_variables=query_variables)
        self.assertTrue(executed["success"])
        self.assertTrue(executed["unblocked"])


class BlockUserTestCase(BlockUserTestCaseMixin, DefaultTestCase):
    def get_query(self):
        return """
        mutation BlockUser($user_id: ID!, $unblocking: Boolean) {
            blockUser(userId: $user_id, unblocking: $unblocking)
                { success, errors, unblocked  }
        }
        """


class BlockUserRelayTestCase(BlockUserTestCaseMixin, RelayTestCase):
    def get_query(self, ):
        return """
        mutation BlockUser($user_id: ID!, $unblocking: Boolean) {
            blockUser(input:{ userId: $user_id, unblocking: $unblocking })
                { success, errors, unblocked }
        }
        """
