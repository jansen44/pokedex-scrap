import os

def get_formatted_message(poke_info):
    type_label = 'Types' if len(poke_info['types']) > 1 else 'Type'

    return """\
########################################################################################
# Index: %d
# Name: %s / %s (%s)
# Caregory: %s
# %s: %s
########################################################################################
    """ % (
        poke_info['core']['index'],
        poke_info['core']['name'],
        poke_info['core']['jp_name'],
        poke_info['core']['jp_rom_name'],
        poke_info['core']['category'],
        type_label,
        ' / '.join(poke_info['types'])
    )

def recreate_file(file_name):
    if (os.path.exists(file_name)):
        os.remove(file_name)

    open(file_name, 'x')