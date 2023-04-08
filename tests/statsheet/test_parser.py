from quadball.statsheet.parser import * 
import os
from io import BytesIO


relpath = lambda *paths: os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), *paths)
    
    )
def test_parse_file(): 
    file_name = relpath( '..','test_data','statsheet', 'TEXAS_LSQC.xlsx')

    assert parse_file(file_name) == []


def test_open_file():
    file_name = relpath( '..','test_data','statsheet', 'hello_world.txt')
    output = open_file(file_name)

    assert type(output) == BytesIO, f'Expected object of type BytesIO, found {type(output)}'
    output_text = output.read().decode('utf-8')
    assert output_text == 'Hello world!'