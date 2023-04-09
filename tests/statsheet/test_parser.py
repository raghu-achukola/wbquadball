from quadball.statsheet.parser import * 
import os
from io import BytesIO
from openpyxl import load_workbook


relpath = lambda *paths: os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), *paths)
    
    )
def test_parse_file(): 
    file_name = relpath( '..','test_data','statsheet', 'TEXAS_LSQC.xlsx')

    assert parse_file(file_name) == []


def test_open_file():
    #TODO: move so all these equivalences are stored in data files
    file_name = relpath( '..','test_data','statsheet', 'hello_world.txt')
    output = open_file(file_name)

    assert type(output) == BytesIO, f'Expected object of type BytesIO, found {type(output)}'
    output_text = output.read().decode('utf-8')
    assert output_text == 'Hello world!'

def test_get_cell_group_values():
    #TODO: move so all these equivalences are stored in data files
    file_name = relpath( '..','test_data','statsheet', 'TEXAS_LSQC.xlsx')
    stream = open_file(file_name)
    sheet = load_workbook(stream).active
    output =  get_cell_group_values(sheet, 7,4)
    assert len(output) == 6
    extras, offense, end_time, result, primary, secondary = output
    assert extras is None and secondary is None 
    assert offense == 'B'
    assert end_time == '0010'
    assert result == 'GD'
    assert primary == 7  # yes an integer

