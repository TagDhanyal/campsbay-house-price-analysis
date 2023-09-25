import unittest
from lambda_function import function_handler

class TestLambdaFunction(unittest.TestCase):

    def test_lambda_handler(self):
        # Create mock event and context objects
        event = {}
        context = {}

        # Call the Lambda function handler
        result = function_handler(event, context)

        # Assert that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Assert that the result has the 'statusCode' key with value 200
        self.assertEqual(result.get('statusCode'), 200)

        # Assert that the result has the 'body' key with the expected message
        expected_message = 'Data uploaded successfully'
        self.assertEqual(result.get('body'), expected_message)

if __name__ == '__main__':
    unittest.main()