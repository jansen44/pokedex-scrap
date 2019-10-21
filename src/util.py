import os

def get_formatted_message(poke_info):
    type_label    = 'Types' if len(poke_info['types']) > 1 else 'Type'
    ability_label = 'Abilities' if len(poke_info['abilities']) > 1 else 'Ability'
    
    return """\
########################################################################################
# Index: %d
# Name: %s / %s (%s)
# Category: %s
# %s: %s
# %s: \n# - %s
########################################################################################
    """ % (
        poke_info['core']['index'],
        poke_info['core']['name'],
        poke_info['core']['jp_name'],
        poke_info['core']['jp_rom_name'],
        poke_info['core']['category'],
        type_label,
        ' / '.join(poke_info['types']),
        ability_label,
        ' \n# - '.join(poke_info['abilities'])
    )

def recreate_file(file_name):
    if (os.path.exists(file_name)):
        os.remove(file_name)

    open(file_name, 'x')