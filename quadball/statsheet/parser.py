from io import BytesIO

def parse_file(file_location:str) -> list:
    """
        High level method to convert a file location into a stats json 
    """
    #TODO Inc 2: fill method with functionality
    return []

def open_file(file_location:str, location_type = None) -> BytesIO:
    """
        The output of both a BytesIO object and a S3 StreamingBody
        can be accessed by .read()

        In this increment we will keep the default functionality the
        local one
    """
    #TODO: add s3 functionality
    with open(file_location,'rb') as f: 
        return BytesIO(f.read())
    
