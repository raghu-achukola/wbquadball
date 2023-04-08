import quadball.schema.statsheet.statsheet_pb2 as stsh
import os
from io import BytesIO
import json 
from google.protobuf.json_format import ParseDict

data_path = os.path.realpath(
    os.path.join(
    os.path.dirname(__file__),
    '..','test_data', 'schema','statsheet','statsheet_possession.json'
    )
)
                 

def test_statsheet_possession():
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """
    with open(data_path) as f: 
        json_data = json.loads(f.read())
    ssp = stsh.StatSheetPossession()
    for i, obj in enumerate(json_data):
        try: 
            ParseDict(obj,ssp)
        except Exception as e: 
            assert False, f"Parse exception occured at index {i}: {e}"
    assert True
    
    