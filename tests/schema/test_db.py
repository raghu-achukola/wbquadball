
import json 
import os
from quadball.schema.db.stats_pb2 import * 
from google.protobuf.json_format import ParseDict


relpath = lambda *paths : os.path.relpath(
        os.path.join(
            os.path.dirname(__file__), *paths
        )
    )
data_path = relpath(
        '..','test_data', 'schema','db','stats.json'
    )

                 

def test_db_possession():
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """
    with open(data_path) as f: 
        json_data = json.loads(f.read())
    ssp = Possession()
    for i, obj in enumerate(json_data):
        try: 
            ParseDict(obj,ssp)
        except Exception as e: 
            assert False, f"Parse exception occured at index {i}: {e}"
    assert True
    
    