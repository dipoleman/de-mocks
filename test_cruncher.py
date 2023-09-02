from unittest.mock import Mock, patch
from cruncher import NumberCruncher,NumberRequester
from pprint import pprint
import pytest

def test_number_cruncher_likes_even_numbers():
    """Test that the crunch method saves number facts for even numbers.
    
    Given:
         A Number cruncher instance getting an even result for its "crunch" method (eg 42)

    Result:
        Method returns "Yum! 42"
        The tummy attribute contains a dict such as {'number': 42, "fact": "42 is the meaning of life."}
    
    """
    with patch.object(NumberRequester, 'call') as mock_call:
        mock_call.return_value = {
            'result': 'SUCCESS',
            'number': 42,
            'fact': '42 is the meaning of life.'
        }
        cruncher = NumberCruncher(size_of_tummy=3)
        result = cruncher.crunch()
        tum = cruncher.tummy()
        
    assert result == "Yum! 42"
    assert tum == [{'number': 42, "fact": "42 is the meaning of life."}]


def test_number_cruncher_hates_odd_numbers():
    """Test that the crunch method rejects number facts for odd numbers.
    
    Given:
         A Number cruncher instance getting an odd result for its "crunch" method eg 13

    Result:
        Method returns "Yuk! 13"
        The tummy attribute is unchanged.
    
    """
    with patch.object(NumberRequester, 'call') as mock_call:
        mock_call.return_value = {
            'result': 'SUCCESS',
            'number': 13,
            'fact': '13 is the New meaning of life.'
        }
        cruncher = NumberCruncher(size_of_tummy=3)
        tum_pre_munch = cruncher.tummy()
        result = cruncher.crunch()
        tum_post_munch = cruncher.tummy()

    assert result == "Yuk! 13"
    assert tum_post_munch == tum_pre_munch


def test_number_cruncher_discards_oldest_item_when_tummy_full():
    """Test that the crunch method maintains a maximum number of facts.
    
    Given:
         A Number cruncher instance with tummy size 3 having 3 items in tummy getting 
         an even result for its "crunch" method, eg 24.

    Result:
        Method deletes oldest result from tummy (eg 42)
        Method returns "Burp! 42"
        The tummy attribute contains 24 but not 42.
    
    """
    with patch.object(NumberRequester, 'call') as mock_call:
        cruncher = NumberCruncher(size_of_tummy=2)
        mock_call.return_value = {
            'result': 'SUCCESS',
            'number': 42,
            'fact': '42 is the meaning of life.'
        }
        result = cruncher.crunch()
        mock_call.return_value = {
            'result': 'SUCCESS',
            'number': 24,
            'fact': '24 is highly composite.'
        }
        result = cruncher.crunch()
        mock_call.return_value = {
            'result': 'SUCCESS',
            'number': 2,
            'fact': 'lowest prime.'
        }
        result = cruncher.crunch()
        tum = cruncher.tummy()
        
    assert result == "Burp! 42"
    assert 24 in [food['number'] for food in tum]
    assert 42 not in [food['number'] for food in tum]

def test_number_cruncher_raises_runtime_error_if_invalid_number_request():
    """Test that there is a runtime error if NumberRequester response is
        invalid

        Given:
            A NumberCruncher instance, receiving an invalid NumberRequester
            response (eg an AttributeError)

        Result: 
            Raises RuntimeError
    """
    with patch.object(NumberRequester, 'call') as mock_call:
        cruncher = NumberCruncher(size_of_tummy=2)
        mock_call.return_value = {
            'result': 'SUCCESS',
            'number': 'forty two',
            'fact': '42 is the meaning of life.'
        }
        with pytest.raises(RuntimeError,match='Unexpected error'):
            cruncher.crunch()
