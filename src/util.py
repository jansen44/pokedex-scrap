import os

def get_formatted_message(poke_info):
    return f"""\
########################################################################################
# Index: {poke_info['core']['index']}
# Name: {poke_info['core']['name']} / {poke_info['core']['jp_name']} ({poke_info['core']['jp_rom_name']})
# Caregory: {poke_info['core']['category']}
########################################################################################
    """

def recreate_file(file_name):
    if (os.path.exists(file_name)):
        os.remove(file_name)

    open(file_name, 'x')