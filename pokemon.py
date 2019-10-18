from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uOpen, Request as uReq
from urllib.parse import urlsplit, urlunsplit, quote
import os
from pokemon_util import (
    convert_iri_url,
    get_poke_soup,
    get_next_pokemon_link,
    get_formatted_message,
    _get_formatted_message,
    _get_poke_info,
    get_poke_info
)

base_url      = "https://bulbapedia.bulbagarden.net/"
forbidden_url = "/wiki/%3F%3F%3F_(Pok%C3%A9mon)"
poke_page_url = convert_iri_url("https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pokémon)")
file_name     = "pokemon_list.txt"
poke_soup     = get_poke_soup(poke_page_url)

if (os.path.exists(file_name)):
    os.remove(file_name)

f = open(file_name, "x")
f = open(file_name, "w")

while(True):
    poke_info = get_poke_info(poke_soup)
    message   = get_formatted_message(poke_info)

    f.write(message + '\n')
    print(message)

    next_pokemon_link = get_next_pokemon_link(poke_soup)
    if (next_pokemon_link == forbidden_url):
        break
    
    poke_soup = get_poke_soup(base_url + next_pokemon_link)

f.close()