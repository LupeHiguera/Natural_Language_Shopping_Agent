"""Regressions found during the UI and search audit; no live AWS calls."""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.bedrock_client import BedrockClient
from app.dynamodb_client import DynamoDBClient
from app.main import app
from app.models import ShoeProduct


@pytest.fixture
def search():
    return BedrockClient('demo', 'demo', mock_mode=True)


@pytest.mark.parametrize('query, ids', [
    ('red running shoes under $100 in size 10', ['mock-001']),
    ('black running shoes under $90', []),
    ('running shoes under $95', ['mock-001']),
    ('running shoes at most $95', ['mock-001', 'mock-004']),
    ('shoes between $90 and $100', ['mock-004']),
    ('purple shoes', []),
    ('sandals', []),
    ('shoes size 25', []),
    ('Adidas casual shoes under $80', ['mock-002']),
])
def test_demo_search_combines_constraints(search, query, ids):
    result = search.invoke_agent(query)
    assert [product['shoe_id'] for product in result['products']] == ids
    catalog = DynamoDBClient('demo', mock_mode=True)
    assert all(catalog.get_product_by_id(product['shoe_id']) == product for product in result['products'])


def test_search_generates_distinct_sessions_and_preserves_provided_session(search):
    assert search.invoke_agent('shoes')['session_id'] != search.invoke_agent('shoes')['session_id']
    assert search.invoke_agent('shoes', 'existing-session')['session_id'] == 'existing-session'


def test_bedrock_generates_required_session_and_parses_split_utf8_json():
    payload = '{"response":"A café favorite","products":[{"shoe_id":"123"}]}'.encode()
    split = payload.index('é'.encode()) + 1
    with patch('app.bedrock_client.boto3.client') as factory:
        factory.return_value.invoke_agent.return_value = {'completion': [
            {'chunk': {'bytes': payload[:split]}}, {'chunk': {'bytes': payload[split:]}}
        ]}
        search = BedrockClient('agent', 'alias')
        result = search.invoke_agent('shoes')
        assert result['agent_response'] == 'A café favorite'
        assert result['products'] == [{'shoe_id': '123'}]
        assert factory.return_value.invoke_agent.call_args.kwargs['sessionId'] == result['session_id']


def test_bedrock_plain_text_and_stream_errors(search):
    assert search._parse_response({'completion': [{'chunk': {'bytes': b'No matches today.'}}]}) == {
        'agent_response': 'No matches today.', 'products': []
    }
    with pytest.raises(RuntimeError):
        search._parse_response({'completion': [{'throttlingException': {'message': 'busy'}}]})


def test_product_filter_zero_and_inverted_bounds():
    client = TestClient(app)
    assert client.get('/api/products', params={'price_max': 0}).json()['products'] == []
    assert client.get('/api/products', params={'price_min': 100, 'price_max': 50}).status_code == 400


def test_search_length_is_bounded():
    assert TestClient(app).post('/api/search', json={'query': 'x' * 501}).status_code == 422


def test_seed_stock_alias_is_preserved():
    product = DynamoDBClient('demo', mock_mode=True).get_all_products()[0]
    product.pop('stock')
    product['in_stock'] = False
    parsed = ShoeProduct(**product)
    assert parsed.stock is False
    assert parsed.model_dump()['stock'] is False


@pytest.mark.parametrize('trace_payload', [
    [{"shoe_id": "live-001"}],
    {"products": [{"shoe_id": "live-001"}]},
])
def test_live_action_group_trace_products_are_preserved(search, trace_payload):
    import json
    response = {"completion": [
        {"trace": {"trace": {"orchestrationTrace": {"observation": {
            "actionGroupInvocationOutput": {"text": json.dumps(trace_payload)}
        }}}}},
        {"chunk": {"bytes": b'Here are the matches from the catalog.'}},
    ]}
    result = search._parse_response(response)
    assert result['products'] == [{'shoe_id': 'live-001'}]
    assert result['agent_response'] == 'Here are the matches from the catalog.'


def test_structured_completion_does_not_duplicate_trace_products(search):
    response = {"completion": [
        {"trace": {"trace": {"orchestrationTrace": {"observation": {
            "actionGroupInvocationOutput": {"text": '[{"shoe_id":"123"}]'}
        }}}}},
        {"chunk": {"bytes": b'{"response":"One pair","products":[{"shoe_id":"123"}]}'}},
    ]}
    assert search._parse_response(response)['products'] == [{'shoe_id': '123'}]


def test_upstream_single_size_records_work_with_the_size_picker():
    product = DynamoDBClient('demo', mock_mode=True).get_all_products()[0]
    product.pop('sizes')
    product['size'] = 10.5
    assert ShoeProduct(**product).sizes == [10.5]
