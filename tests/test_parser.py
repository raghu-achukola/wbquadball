from quadball.statsheet.parser import * 
import os

def test_parse_file(): 
    file_name = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'test_data', 'TEXAS_LSQC.xlsx'))
    print(file_name)
    assert parse_file(file_name) == []