#Imports
from word_spacing_lib.core import *
from word_spacing_lib import identify_word








#Main Word Selection Loop
target_string=None

possible_words=[]
compiled_word_list=[]

error_message=""
#TBD, Just Refactor This Whole File Next Time You Touch This Project


target_string=get_target_string(root_directory=os.path.dirname(__file__))
compiled_word_list_index=0

while True:
    if target_string == "":    #Exit Condition 1, Whole String Has Been Compiled Into Word List
        output_string(root_directory=os.path.dirname(__file__),output_string=list_to_str(compiled_word_list,delimiter=" "))
        clear_console()
        break

    ui_elements=[]








    #Initial Data Collection And UI Construction
    final_compiled_word_list_index=len(compiled_word_list)-1
    if final_compiled_word_list_index < 0:
        final_compiled_word_list_index=0

    slice_end_index=MAX_WORD_LENGTH
    
    if MAX_WORD_LENGTH > (len(target_string)-1):
        slice_end_index=len(target_string)
    


    current_target_string_slice=target_string[:slice_end_index]

    possible_words=identify_word.get_possible_words(current_target_string_slice)
    possible_words.reverse()
    possible_words.append(MANUAL_SELECTION_LABEL)


    possible_words_binds_info=identify_word.construct_word_bind_info(possible_words)


    bind_prompts=identify_word.construct_bind_prompt(BIND_LIST)


    text_preview=list_to_str(compiled_word_list[:(compiled_word_list_index+1)],delimiter=" ")



    ui_elements.append({"header": "Current Sequence:", "content": current_target_string_slice, "delimiter": "\n"})
    ui_elements.append({"header": "Next Possible Words:", "content": possible_words_binds_info, "delimiter": "\n"})
    ui_elements.append({"header": None, "content": bind_prompts, "delimiter": None})


    if error_message != "":    #If There Is An Error, Add It To The UI Elements
        error_message_output="ERROR: {error_message}".format(error_message=error_message)
        ui_elements.append({"header": None, "content": wrap_object(error_message_output,ERROR_COLOUR_WRAPPER), "delimiter": None})
        error_message=""

    
    ui_elements.append({"header": "Text Preview:", "content": text_preview, "delimiter": "\n"})








    #Displaying The UI
    ui_output=ui_elements_to_str(ui_elements,delimiter="\n\n")
    clear_console()
    dump(ui_output,padding=2)



    




    #User Input Collection, Error Handling And Data Processing
    key_pressed=get_keypress()["key_pressed"]


    try:
        is_key_pressed_valid_num=(int(key_pressed) in range(0,len(possible_words)))
    except ValueError:
        is_key_pressed_valid_num=False

    is_key_pressed_in_bind_list=identify_word.is_key_in_bind_list(key=key_pressed,bind_list=BIND_LIST)










    #Keybind Handling
    key_pressed_descriptor=identify_word.get_descriptor_from_bind(key_pressed,BIND_LIST)

    if (is_key_pressed_in_bind_list) and (key_pressed_descriptor == "Exit"):
        fatal_error(compiled_words=list_to_str(compiled_word_list,delimiter=" "))



    elif (is_key_pressed_in_bind_list) and (key_pressed_descriptor == "Undo"):
        compiled_word_list_index-=1

        if (compiled_word_list_index < 0) and (compiled_word_list == []):
            compiled_word_list_index+=1

            error_message="There Is Nothing To Undo"

        else:
            target_string=compiled_word_list[compiled_word_list_index+1]+target_string

            if compiled_word_list_index < 0:    #Resets All Data (Otherwise Bad Things Happen)
                compiled_word_list_index=0      #TBD Fix Undo And Redo Seeking (Errors At Ends of Range)
                compiled_word_list=[]           #TBD Also get Rid Of Clamps

        



    elif (is_key_pressed_in_bind_list) and (key_pressed_descriptor == "Redo"):
        compiled_word_list_index+=1

        if compiled_word_list_index > final_compiled_word_list_index:
            compiled_word_list_index-=1
            error_message="There Is Nothing To Redo"

        else:
            target_string=target_string[len(compiled_word_list[compiled_word_list_index]):]








    #Number Keybind Handling
    elif is_key_pressed_valid_num:
        key_pressed=int(key_pressed)
        selected_word_index=key_pressed-1


        if key_pressed == 0:
            selected_word=input("Manual Selection:")
            selected_word=standardise_case(selected_word)

            selection_in_target_string=selected_word == target_string[:len(selected_word)]

            if not selection_in_target_string:
                error_message="Manual Selection Not In Text"
                selected_word=""

        else:
            selected_word=possible_words[selected_word_index]


        if selected_word != "":

            if compiled_word_list_index == final_compiled_word_list_index:
                compiled_word_list.append(selected_word)

            else:
                compiled_word_list[compiled_word_list_index+1]=selected_word
                compiled_word_list=compiled_word_list[:compiled_word_list_index+2]    #Removes All Elements After The Newly Added Element (If There Are Any), So You Cannot Modify The Target Strign With Redo



            if len(compiled_word_list) != 1:    #So If compiled_word_list_index=0 And compiled_word_list_index=["Word"], Index Doesn't Become 1
                compiled_word_list_index+=1      

            start_index=len(selected_word)
            target_string=target_string[start_index:]








    #Error Handling
    else:
        pass    #Just Ignore Anything Else