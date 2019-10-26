
# Builtin
import csv

# Local
from src.pokemon import get_poke_soup, get_next_pokemon_link, get_poke_info, check_last_page
from src.util import get_formatted_message, recreate_file, get_pokemon_link, append_csv

if __name__ == '__main__':
    BASE_URL  = 'https://bulbapedia.bulbagarden.net'
    END_URL   = '/wiki/%3F%3F%3F_(Pok%C3%A9mon)'
    FILE_NAME = 'pokemon_list.txt'
    CSV_NAME  = 'pokemon.csv'
    CURRENT_KEYS = [
        'image_link', 
        'index', 
        'name', 
        'categories', 
        'jp_name', 
        'jp_rom_name', 
        'types', 
        'abilities', 
        'gender_ratio', 
        'catch_rate', 
        'egg_groups', 
        'hatch_time', 
        'height', 
        'weight', 
        'mega_stones'
    ]

    recreate_file(FILE_NAME)
    recreate_file(CSV_NAME)

    with open(CSV_NAME, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CURRENT_KEYS)
        writer.writeheader()

    with open(FILE_NAME, 'w') as f:
        next_pokemon_link = get_pokemon_link('Bulbasaur')

        while(next_pokemon_link != END_URL):
            poke_soup = get_poke_soup(f'{BASE_URL}{next_pokemon_link}')
            if check_last_page(poke_soup):
                break

            poke_info = get_poke_info(poke_soup)
            message   = get_formatted_message(poke_info)
            append_csv(poke_info, CSV_NAME)

            f.write(f'{next_pokemon_link}\n{message}\n')
            
            print(next_pokemon_link)
            print(message)

            next_pokemon_link = get_next_pokemon_link(poke_soup)


        print("\n\n########## FINISHED ##########\n\n")
    