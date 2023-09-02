from unittest.mock import Mock, patch
from cruncher import NumberCruncher,NumberRequester
from pprint import pprint
import pytest

def test_number_requester_returns_a_valid_result_when_called():
    """Test that the call method returns a valid item.
    
    Given:
         A NumberRequester instance making a successful call

    Result:
        A result as a dict in the form {'result': 'SUCCESS', 'number': 13, "fact": "13 is lucky for some."}

    """
    mock_request = Mock()
    mock_request.status_code = 200
    mock_request.text = "13 is lucky for some."
    with patch('cruncher.requests.get') as mock_get:
        mock_get.return_value = mock_request
        requester = NumberRequester()
        result = requester.call()

        assert result == {'result': 'SUCCESS', 'number': 13, "fact": "13 is lucky for some."}

def test_number_requester_returns_error_result_for_non_200_response():
    """Test that the call method returns a valid item when a request fails.
    
    Given:
         A NumberRequester instance making an unsuccessful call

    Result:
        A result as a dict in the form {'result': 'FAILURE', 'error_code': 404}
    
    """
    mock_request = Mock()
    mock_request.status_code = 404
    mock_request.text = "Oop! Something has gone wrong"
    with patch('cruncher.requests.get') as mock_get:
        mock_get.return_value = mock_request
        requester = NumberRequester()
        result = requester.call()

        assert result == {'result': 'FAILURE', 'error_code': 404}


def test_number_requester_keeps_log_of_requests():
    """Test that a NumberRequester instance keeps a log of its own requests.

    Given:
        A NumberRequester is instantiated.
        The NumberRequester.call method is called 5 times at known times.

    Result:
        The NumberRequester.log attribute returns a array of five valid results. Each result
        is a serialisable dict in the form:
        {'request_number': 1, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math',
        'result': 'SUCCESS', 'number': 49}
    Ensure that you test that each dict is exactly correct - including the 'call_time'.
    """
    requester = NumberRequester()
    with patch('cruncher.requests.get') as mock_get, patch('cruncher.dt') as mock_dt:
        mock_request = Mock()
        mock_request.status_code = 200
        mock_request.text = "49 is seven squared."
        mock_get.return_value = mock_request
        
        mock_now = Mock()
        mock_now.isoformat.return_value = '2022-11-09T16:38:23.417667'
        mock_dt.now.return_value = mock_now
        
        for i in range(5):
            requester.call()
       
        expected = [
            {'request_number': 1, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 49}, {'request_number': 2, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 49}, {'request_number': 3, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 49}, {'request_number': 4, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 49}, {'request_number': 5, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math', 'result': 'SUCCESS', 'number': 49}]
        
        assert requester.log == expected

  