from quadball.db.statsheet_converter import * 
import pytest
import os
import json
from google.protobuf.json_format import ParseDict, MessageToDict
from quadball.schema.db.stats_pb2 import Extra
from deepdiff import DeepDiff

relpath = lambda *paths: os.path.realpath(os.path.join(os.path.dirname(__file__),*paths))
EXTRA_JSON_PATH = relpath(
    '..','test_data','db','test_statsheet_converter','extras.json'
)



@pytest.fixture
def extra_data():
    with open(EXTRA_JSON_PATH) as f: 
        return json.loads(f.read())

def test_extra_extraction(extra_data):
    for test_name, test_params in extra_data.items():
        inputs, outputs = test_params['in'], test_params['out']
        actual = MessageToDict(convert_single_extra(**inputs))
        expected =  MessageToDict(ParseDict(outputs, Extra() ))
        assert actual == expected, DeepDiff(actual,expected)
