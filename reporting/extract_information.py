import re
import xlwt
from report_tool.models import Pupil,Class,School
from reporting.models import Upload, Spreadsheet_report
import django
import definitions

#this function is used for extracting information from a string input value
def extract_information(index_of_function, index_of_head, body, indexes_of_body,
                        index_of_excel_function, excel_function, value, row_x, col_x, other_info, index_of_other_info):
    function_name = ''
    head = ''
    temp = re.search('#<.*?>', unicode(value)) #if the cell contains the function which returns the data
    if temp:
        function_name = (temp.group(0).rstrip('>').lstrip('#<')) #remove > at the right and #< at the left
        index_of_function.append((row_x, col_x)) #stores the index of this function
    else:
        temp = re.findall('{{.*?}}', unicode(value)) # find all the specified fields of data
        if temp: #if yes
            for temp1 in temp: #iterating all of the fields
                temp1 = temp1.rstrip('}}').lstrip('{{') # remove tags to get attributes
                if (temp1.startswith('head:')): #if the field is the header
                    head = temp1[5:] #remove head:
                    index_of_head.append((row_x, col_x)) #stores the location of the header
                else:
                    body.append(temp1[5:]) #else the field is the body
                    indexes_of_body.append((row_x, col_x)) #stores the location of the body
            if value.startswith(":="):
                excel_function.append(value) #strores the value of the cell contain the specified excel function
                index_of_excel_function.append((row_x, col_x)) #store index of above excel function
        else:
            other_info.append(value) #store other information
            index_of_other_info.append((row_x,col_x))#store the index of other information

    return function_name, head

#function to get a list of objects containing the data
def get_list_of_object(function_name, index_of_function):
    try: #try to get the list from the function in definitions.py file
        #try to get the list of objects by executing the function in definitions.py file
        list_objects = eval('definitions.%s'%function_name)
    except :
        try:#try to get the list directly
            list_objects = eval(function_name)
        except :#return the error message
            return 'Definition of data function error at cell ' + xlwt.Utils.rowcol_to_cell(index_of_function[0][0],index_of_function[0][1]), []

    #if everything is ok, then check if the list of object is a well list
    try:
        len(list_objects)
    except :
        return 'The function you defined returns wrong result (must return a list of objects):cell ' + xlwt.Utils.rowcol_to_cell(index_of_function[0][0],index_of_function[0][1]), []

    return 'ok', list_objects
