# import modules
from datetime import datetime

def main():
    pass


def get_data(txt_file):
    '''Takes text file as input. Returns a list 
    where each line in the file is a list of each
    space separated value.'''

    return [line.strip().split('\t') for line in open(txt_file, 'r')]


def str_to_datetime(date_string, from_format = 'date'):
    '''Takes two inputs: 1) a date in string format 
    and 2) 'from_format' indicating either 'date' 
    (date without time, default value) or 'datetime' 
    (date with time). Converts string into a datetime
    object with time of '00:00' if no time provided 
    in string, otherwise returns datetime object 
    with the provided time.'''

    if from_format == 'date':
        return datetime.strptime(date_string, "%Y-%m-%d")
    elif from_format == 'datetime':
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
    else:
        return "Argument 'from_format' must be 'date' or 'datetime'"
    
    
if __name__ == '__main__':
    main()
