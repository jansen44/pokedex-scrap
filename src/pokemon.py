
import os

from urllib.request import urlopen as uOpen, Request as uReq
from bs4 import BeautifulSoup as soup
from operator import itemgetter

def get_poke_soup(link):
    uClient         = uReq(link, headers={"User-Agent": "Magic Browser"})
    uCon            = uOpen(uClient)
    poke_page_html  = uCon.read()
    uCon.close()
    
    poke_page_soup = soup(poke_page_html, "html.parser")
    return poke_page_soup

def get_formatted_message(poke_info):
    return """
########################################################################################
# Index: %d
# Name: %s / %s (%s)
# Caregory: %s
########################################################################################
    """ % ( poke_info["index"],       \
            poke_info["name"],        \
            poke_info["jp_name"],     \
            poke_info["jp_rom_name"], \
            poke_info["category"] )

def _get_formatted_message(poke_info):
    return """
########################################################################################
# Index: %s
# Name: %s
########################################################################################
    """ % ( poke_info["index"],       \
            poke_info["name"],        \
        )

def get_next_pokemon_link(poke_soup):
    return poke_soup                                \
            .find(id="mw-content-text").table       \
            .findChildren("tr", recursive=False)[1] \
            .findChildren("td", recursive=False)[2] \
            .find("a")["href"]

def get_poke_info(poke_soup):
    core_info_getter = itemgetter("name", "category", "jp_name", "jp_rom_name", "index")

    name,        \
    category,    \
    jp_name,     \
    jp_rom_name, \
    index = core_info_getter(get_core_poke_info(poke_soup))
    
    return {
        "name":        name,
        "category":    category,
        "jp_name":     jp_name,
        "jp_rom_name": jp_rom_name,
        "index":       index
    }
    

# Name, category, index, jp/name
def get_core_poke_info(poke_soup):
    info_table = poke_soup                      \
                    .find(id="mw-content-text") \
                    .find_all("table", recursive=False)[1]

    base_info_container = info_table.tr.td \
                            .table.tr


    info_container = base_info_container.td \
                        .table.tr           \
                        .find_all("td", recursive=False)
    
    poke_index  = base_info_container.th.find("a").text
    name        = info_container[0].big.text
    category    = info_container[0].a.text
    jp_name     = info_container[1].span.text
    jp_rom_name = info_container[1].i.text

    return {
        "name":        name,
        "category":    category,
        "jp_name":     jp_name,
        "jp_rom_name": jp_rom_name,
        "index":       int(poke_index.replace('#', ''))
    }
