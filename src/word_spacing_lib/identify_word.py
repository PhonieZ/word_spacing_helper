#Imports
from word_spacing_lib.core import *
import enchant








#Main Word Identification Logic
def get_possible_words(target_string):
    global MAX_WORD_LENGTH
    global WORD_OPTION_COUNT
    EN_GB_DICTIONARY=enchant.Dict("en_GB")
    possible_words=[]

    
    for current_search_end_index in range(1,len(target_string)):
        current_target_string_slice=target_string[:current_search_end_index]

        is_current_slice_word=(EN_GB_DICTIONARY.check(current_target_string_slice) == True)


        if is_current_slice_word:
            possible_words.append(current_target_string_slice)



    return(possible_words[0:(WORD_OPTION_COUNT+1)])    #Ensures That At Most WORD_OPTION_COUNT Word Options Are Provided








#Keybind Handling Functions
def construct_word_bind_info(possible_words):
    global ARROW
    global KEYBIND_WRAPPER
    final_index=0

    word_bind_info=[]
    word_bind_info_output=""

    final_index=len(possible_words)-1


    for current_word_index in range(0,len(possible_words)):
        current_word=possible_words[current_word_index]


        if current_word_index == final_index:    #If We Have Reached Final Index, Set Keybind to 0 (For Manual Selection)
            current_keybind=0

        else:
            current_keybind=current_word_index+1


        current_keybind=wrap_object(current_keybind,KEYBIND_WRAPPER)

        current_word_bind_info="{current_keybind} {ARROW} {current_word}".format(current_keybind=current_keybind,ARROW=ARROW,current_word=current_word)

        word_bind_info.append(current_word_bind_info)


    word_bind_info_output=list_to_str(word_bind_info,delimiter="\n")

    return(word_bind_info_output)




def construct_bind_prompt(BIND_LIST):
    global KEYBIND_PROMPT_WRAPPER
    global KEYBIND_WRAPPER
    bind_prompts=[]
    bind_prompt_output=""


    for current_bind_pair in BIND_LIST:  
        current_bind, current_bind_descriptor=current_bind_pair["bind"], current_bind_pair["descriptor"]
        current_bind=wrap_object(current_bind,KEYBIND_WRAPPER)

        current_bind_prompt="{prompt} {descriptor}".format(prompt=wrap_object(current_bind,KEYBIND_PROMPT_WRAPPER),descriptor=current_bind_descriptor)

        bind_prompts.append(current_bind_prompt)


    bind_prompt_output=list_to_str(bind_prompts,delimiter="\n")

    return(bind_prompt_output)




def is_key_in_bind_list(key,bind_list):
    for current_bind_pair in bind_list:
        if key == current_bind_pair["bind"]:
            return(True)
    else:
        return(False)
    



def get_descriptor_from_bind(bind,bind_list):
    for current_bind_pair in bind_list:
        if bind == current_bind_pair["bind"]:
            return(current_bind_pair["descriptor"])
    else:
        return(None)