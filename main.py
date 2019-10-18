# Built-in
import os
from urllib.request import urlopen as uOpen, Request as uReq
from urllib.parse import urlsplit, urlunsplit, quote

# Third-party
from bs4 import BeautifulSoup as soup

# Local
from src.pokemon import get_poke_soup, get_next_pokemon_link, get_formatted_message, get_poke_info

if __name__ == '__main__':
    BASE_URL  = "https://bulbapedia.bulbagarden.net/"
    FIRST_URL = "https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_%28Pok%C3%A9mon%29"
    END_URL   = "/wiki/%3F%3F%3F_(Pok%C3%A9mon)"
    FILE_NAME = "pokemon_list.txt"

    if (os.path.exists(FILE_NAME)):
        os.remove(FILE_NAME)

    f = open(FILE_NAME, "x")
    f = open(FILE_NAME, "w")

    poke_soup     = get_poke_soup(FIRST_URL)
    
    while(True):
        poke_info = get_poke_info(poke_soup)
        message   = get_formatted_message(poke_info)

        f.write(message + '\n')
        print(message)

        next_pokemon_link = get_next_pokemon_link(poke_soup)
        if (next_pokemon_link == END_URL):
            break
        
        poke_soup = get_poke_soup(BASE_URL + next_pokemon_link)

    f.close()