class Assertions:
    @staticmethod
    def assert_success_response(response, expected_status=200):
        response_body = response.json()
        assert response.status_code == expected_status
        assert response_body["success"] is True
        return response_body

    @staticmethod
    def assert_error_response(response, expected_status, expected_message):
        response_body = response.json()
        assert response.status_code == expected_status
        assert response_body["success"] is False
        assert response_body["message"] == expected_message
        return response_body

    @staticmethod
    def assert_access_token_received(response):
        response_body = Assertions.assert_success_response(response)
        assert response_body.get("accessToken")
        return response_body

    @staticmethod
    def assert_order_number_received(response):
        response_body = Assertions.assert_success_response(response)
        assert response_body["order"]["number"] > 0
        return response_body

    @staticmethod
    def assert_status_code(response, expected_status):
        assert response.status_code == expected_status
