
# Built-in
from urllib.request import urlopen as uOpen, Request as uReq
from urllib.parse import urlsplit, urlunsplit, quote

# Third-party
from bs4 import BeautifulSoup as soup

# Local
from src.pokemon import get_poke_soup, get_next_pokemon_link, get_poke_info, check_last_page
from src.util import get_formatted_message, recreate_file

if __name__ == '__main__':
    BASE_URL  = 'https://bulbapedia.bulbagarden.net'
    END_URL   = '/wiki/%3F%3F%3F_(Pok%C3%A9mon)'
    FILE_NAME = 'pokemon_list.txt'

    recreate_file(FILE_NAME)

    with open(FILE_NAME, 'w') as f:
        next_pokemon_link = '/wiki/Bulbasaur_%28Pok%C3%A9mon%29'

        while(True):
            poke_soup = get_poke_soup(f'{BASE_URL}{next_pokemon_link}')
            if check_last_page(poke_soup):
                break
            
            poke_info = get_poke_info(poke_soup)
            message   = get_formatted_message(poke_info)

            f.write(f'{next_pokemon_link}\n{message}\n')
            print(next_pokemon_link)
            print(message)

            next_pokemon_link = get_next_pokemon_link(poke_soup)
            if (next_pokemon_link == END_URL):
                break
 
    print("\n\n########## FINISHED ##########\n\n")

