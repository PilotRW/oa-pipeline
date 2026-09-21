import unittest

from app.services.keepa_batch_policy import effective_batch_limit


class KeepaBatchPolicyTests(unittest.TestCase):
    def test_limit_respects_tokens_plan_and_request(self):
        self.assertEqual(
            10,
            effective_batch_limit(
                100,
                tokens_left=20,
                token_cost_per_item=2,
                configured_limit=50,
            ),
        )

    def test_limit_is_zero_without_enough_tokens(self):
        self.assertEqual(
            0,
            effective_batch_limit(
                10,
                tokens_left=1,
                token_cost_per_item=3,
                configured_limit=100,
            ),
        )

    def test_negative_tokens_are_treated_as_zero(self):
        self.assertEqual(
            0,
            effective_batch_limit(
                10,
                tokens_left=-1,
                token_cost_per_item=1,
                configured_limit=100,
            ),
        )


if __name__ == "__main__":
    unittest.main()
