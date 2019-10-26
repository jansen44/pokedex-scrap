
# Builtin
import os
import csv

def get_formatted_message(poke_info):
    category_label   = 'Categories'  if len(poke_info['categories'])  > 1 else 'Category'
    type_label       = 'Types'       if len(poke_info['types'])       > 1 else 'Type'
    ability_label    = 'Abilities'   if len(poke_info['abilities'])   > 1 else 'Ability'
    egg_group_label  = 'Egg Groups'  if len(poke_info['egg_groups'])  > 1 else 'Egg Group'
    mega_stone_label = 'Mega Stones' if len(poke_info['mega_stones']) > 1 else 'Mega Stone'
    

    return """\
########################################################################################
# Image: %s
# Index: %d
# Name: %s / %s (%s)
# %s: %s
# %s: %s
# ============================================================
# %s: \n# - %s
# ============================================================
# Gender Ratio: %s
# Catch Rate: %s
# ============================================================
# %s: %s
# Hatch Time: %s
# ============================================================
# Height: %s
# Weight: %s
# ============================================================
# %s: %s
########################################################################################
    """ % (
        poke_info['image_link'],
        poke_info['index'],
        poke_info['name'],
        poke_info['jp_name'],
        poke_info['jp_rom_name'],
        category_label,
        ' / '.join(poke_info['categories']),
        type_label,
        ' / '.join(poke_info['types']),
        ability_label,
        ' \n# - '.join(poke_info['abilities']),
        ' / '.join(poke_info['gender_ratio']) if len(poke_info['gender_ratio']) > 0 else "Genderless",
        poke_info['catch_rate'],
        egg_group_label,
        ' / '.join(poke_info['egg_groups']),
        poke_info['hatch_time'],
        ' / '.join(poke_info['height']),
        ' / '.join(poke_info['weight']),
        mega_stone_label,
        ' / '.join(poke_info['mega_stones']) if len(poke_info['mega_stones']) > 0 else '---',
    )

def recreate_file(file_name):
    if (os.path.exists(file_name)):
        os.remove(file_name)

    open(file_name, 'x')

def get_pokemon_link(poke_name):
        return f'/wiki/{poke_name.capitalize()}_%28Pok%C3%A9mon%29'

def format_to_csv(poke_info):
    return {
        'image_link':   f'=IMAGE(\"{poke_info["image_link"]}\")',
        'index':        poke_info['index'],
        'name':         poke_info['name'],
        'categories':   ' \n'.join(['- ' + p for p in poke_info['categories']]),
        'jp_name':      poke_info['jp_name'],
        'jp_rom_name':  poke_info['jp_rom_name'],
        'types':        ' \n'.join(['- ' + p for p in poke_info['types']]),
        'abilities':    ' \n'.join(['- ' + p for p in poke_info['abilities']]),
        'gender_ratio': ' \n'.join(['- ' + p for p in poke_info['gender_ratio']]),
        'catch_rate':   poke_info['catch_rate'],
        'egg_groups':   ' \n'.join(['- ' + p for p in poke_info['egg_groups']]),
        'hatch_time':   poke_info['hatch_time'],
        'height':       ' \n'.join(['- ' + p for p in poke_info['height']]),
        'weight':       ' \n'.join(['- ' + p for p in poke_info['weight']]),
        'mega_stones':  ' \n'.join(['- ' + p for p in poke_info['mega_stones']]),
    }

def append_csv(poke_info, file):
    formatted_poke = format_to_csv(poke_info)
    keys           = formatted_poke.keys()

    with open(file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writerow(formatted_poke)
   