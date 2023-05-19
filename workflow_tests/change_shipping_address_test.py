from langchain.agents import Tool, load_tools
from tests.workflow_tests.base_test import TestCase, WorkflowTester, BaseTest


class TestChangeShippingAddress(BaseTest):
    @staticmethod
    def check_order_status(order_id: str, **kwargs):
        """Returns order information as a dictionary, where order_status can be "shipped" or "not_shipped" """
        if order_id == "123":
            return {"status_code": 200, "order_id": "123", "order_status": "shipped",
                    "tracking_url": "example.com/123",
                    "shipping_address": "300 ivy street san francisco ca"}
        elif order_id == "456":
            return {"status_code": 200, "order_id": "456", "order_status": "not_shipped",
                    "tracking_url": "example.com/456",
                    "shipping_address": "301 ivy street san francisco ca"}
        else:
            return {"status_code": 400, "message": "order not found"}

    @staticmethod
    def change_shipping_address(order_id: str, new_address: str, **kwargs):
        """Changes the shipping address for unshipped orders. Requires the order_id and the new_address inputs"""
        return {"status_code": 200, "order_id": order_id, "shipping_address": new_address}

    policy = """You are an AI assistant for customer support for the company Figs which sells nurse and medical staff clothes.
When a customer requests to change their shipping address, verify the order status in the system.
If the order has not yet shipped, update the shipping address as requested and confirm with the customer that it has been updated. 
If the order has already shipped, inform them that it is not possible to change the shipping address at this stage and provide assistance on how to proceed with exchanges, by following instructions at example.com/returns.
"""

    tools = [
                Tool(
                    name="check order status",
                    func=check_order_status,
                    description="""This function checks the order status based on order_id
            Input args: order_id: non-empty str
            Output values: status_code: int, order_id: str, order_status: shipped or not shipped, 
            tracking_url: str, message: str
            """
                ),
                Tool(
                    name="change shipping address",
                    func=change_shipping_address,
                    description="""This function change the shipping address based on provided 
            order_id and new_address 
            Input args: order_id: non-empty str, new_address: non-empty str
            Output values: status_code: int, order_id: str, shipping_address: str
            """
                ),
            ]

    test_cases = [
        TestCase(test_name="change shipping address",
                 user_query="can i change my shipping address?",
                 user_context="order id is 456. the new address is 234 spear st, "
                              "san francisco",
                 expected_outcome="found order status and changed shipping address"),
        TestCase(test_name="failed changing shipping address, no order id",
                 user_query="can i change my shipping address?",
                 user_context="don't know about order id. the new address is 234 spear st, san francisco",
                 expected_outcome="cannot find the order status, failed to change shipping "
                                  "address"),
        TestCase(test_name="failed changing shipping address, shipped item",
                 user_query="can i change my shipping address?",
                 user_context="order id is 123. the new address is 234 spear st, "
                              "san francisco",
                 expected_outcome="inform user cannot change shipping address and hand off to "
                                  "agent"),
    ]


if __name__ == '__main__':
    tests = WorkflowTester(tests=[TestChangeShippingAddress()], output_dir="./test_results")
    tests.run_all_tests()
