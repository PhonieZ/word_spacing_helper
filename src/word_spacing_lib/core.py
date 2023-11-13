#Imports
import os
import sys
import keyboard








#Constants
MAX_WORD_LENGTH=45      #Determines How Long An Identified Word Can Be At Most
WORD_OPTION_COUNT=9    #Determines How Many Possible Words Will Be Identified At Most

BIND_LIST=[
              {"bind": "esc", "descriptor": "Exit"},    #What Key Exits The Application
              {"bind": "-", "descriptor": "Undo"},      #What Key Lets You Undo
              {"bind": "=", "descriptor": "Redo"}       #What Key Lets You Redo
          ]
KEYBIND_WRAPPER={"prefix": "[", "suffix": "]"}     #The prefix And suffix Is Wrapped Around The Keybind When Printed As A String

ERROR_COLOUR_WRAPPER={"prefix": "\033[0;31m\033[7m", "suffix": "\033[0m"}    #When The prefix And suffix Is Wrapped Around A String, It Has An Error Colour

ARROW="==>"                                                     #String Representation Of An Arrow Used In Terminal
MANUAL_SELECTION_LABEL="Manual Selection"                       #Label Used For Manual Word Selection
KEYBIND_PROMPT_WRAPPER={"prefix": "Press ", "suffix": " To"}    #Used To Form Sentence Like 'Press [esc] To Exit'

WORKING_FOLDER="working_folder"    #Name Of Folder Where Input And Output Files Are Stored
OUTPUT_FILE="output.txt"           #Name Of Output File In WORKING_FOLDER
INPUT_FILE="input.txt"             #Name Of Input File In WORKING_FOLDER

DEFAULT_CASE="upper"    #Input upper For Uppercase, lower For Lowercase








#Generalised Helper Functions
def wrap_object(object,WRAPPER):
    string="{prefix}{string}{suffix}".format(prefix=WRAPPER["prefix"],string=str(object),suffix=WRAPPER["suffix"])

    return(string)




def standardise_case(string):
    global DEFAULT_CASE
    global ERROR_COLOUR_WRAPPER

    if DEFAULT_CASE == "upper":
        string=string.upper()

    elif DEFAULT_CASE == "lower":
        string=string.lower()

    else:
        print(wrap_object("DEFAULT_CASE Value Invalid",WRAPPER=ERROR_COLOUR_WRAPPER))    #Just A Warning, No Point In Crashing Just Because Of This

    return(string)    
  







#File Input And Output Handling
def get_target_string(root_directory):
    global WORKING_FOLDER
    global INPUT_FILE
    input_file_pointer=None
    target_string=""



    input_file_directory=os.path.join(root_directory,WORKING_FOLDER)

    if not(os.path.exists(input_file_directory)):    #Creates Working Folder If It Doesn't Exist
        os.makedirs(input_file_directory)

    input_file_directory=os.path.join(input_file_directory,INPUT_FILE)

    try:
        input_file_pointer=open(input_file_directory,"r",encoding="utf-8")
        target_string=input_file_pointer.read()
        input_file_pointer.close()
        
    except FileNotFoundError:
        input_file_pointer=open(input_file_directory,"x",encoding="utf-8")
        target_string=""
        input_file_pointer.close()
        
    if target_string == "":    
        fatal_error(error_message="input.txt Is Blank")   

    

    target_string=target_string.replace("\n","")
    target_string=target_string.replace(" ","")
    target_string=standardise_case(target_string)

    
    if target_string == "":
        return(None)
    else:
        return(target_string)
    



def output_string(output_string,root_directory):
    global WORKING_FOLDER
    global OUTPUT_FILE
    output_file_pointer=None



    OUTPUT_FILE_DIRECTORY=os.path.join(root_directory,WORKING_FOLDER,OUTPUT_FILE)

    output_file_pointer=open(OUTPUT_FILE_DIRECTORY,"w",encoding="utf-8")
    output_file_pointer.write(output_string)
    output_file_pointer.close()
        







#Terminal Output Handling
def dump(object,is_top_padding=True,is_bottom_padding=True,padding=8):
    output_string=""



    if is_top_padding:
        output_string+="\n"*padding


    if type(object) is dict:
        for key,value in object.items():
            if type(value) is list:
                value=list_to_str(value,delimiter="  ")

            output_string+="{key}: {value}".format(key=str(key),value=str(value))
            output_string+="\n"


        output_string=output_string[:-1]    #To Ensure The Bottom Padding Is padding Lines Of Blank Exactly

    else:                                   #Incase A Dict Isn't Inputted
        output_string+=str(object)


    if is_bottom_padding:
        output_string+="\n"*padding
        output_string=output_string[:-1]    #To Ensure The Bottom Padding Is padding Lines Of Blank Exactly

    

    print(output_string)


def list_to_str(list,delimiter=", "):    #Delimiter Determines What List Elements Are Seperated By
    output_string=""


    for current_element in list:
        output_string+="{current_element}{delimiter}".format(current_element=current_element,delimiter=delimiter)


    return(output_string[:-(len(delimiter))])




def ui_elements_to_str(ui_elements,delimiter="\n"):
    output=""

    for current_ui_element in ui_elements:
        ui_element_construction_order=[
                                          current_ui_element["header"],
                                          current_ui_element["delimiter"],
                                          current_ui_element["content"],
                                          delimiter
                                      ]

        for current_part in ui_element_construction_order:
            if not(current_part is None):
                output+=current_part

    output=output[:-len(ui_element_construction_order[-1])]

    return(output)




def clear_console():
    os.system("cls||clear")    #cls Is For Windows, clear Is For Unix Systems, || Is Magic




def fatal_error(error_message=None):
    clear_console()

    if not(error_message is None):
        input(wrap_object(error_message,ERROR_COLOUR_WRAPPER))


    sys.exit()

    






#Terminal Input Handling
def get_keypress():
    input_event=None
    is_key_pressed=False
    key_pressed=""



    input_event=keyboard.read_event()

    #TBD, Run Checks For If Window Is In Focus (As Keyboard Presses Are Always Captured) For Both Mac And Windows

    is_key_pressed=(input_event.event_type == keyboard.KEY_DOWN)
    if is_key_pressed:
        key_pressed=input_event.name

    return({"key_pressed": key_pressed})