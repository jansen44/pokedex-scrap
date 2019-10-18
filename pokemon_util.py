from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uOpen, Request as uReq
from urllib.parse import urlsplit, urlunsplit, quote
from operator import itemgetter
import os

def convert_iri_url (iri):
    url    = urlsplit(iri)
    url    = list(url)
    url[2] = quote(url[2])
    url    = urlunsplit(url)
    
    return url
    
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





# Legacy =================================================================================
def _get_next_pokemon_link(poke_soup):
    next_pokemon_link = poke_soup.find(id="mw-content-text").table
    next_pokemon_link = next_pokemon_link.findChildren("tr", recursive=False)[1]
    next_pokemon_link = next_pokemon_link.findChildren("td", recursive=False)[2]
    next_pokemon_link = next_pokemon_link.find("a")["href"]
    return next_pokemon_link

def _get_poke_info(poke_soup):
    info_table     = poke_soup.find(id="mw-content-text").find_all("table")[4]
    table_text_arr = info_table.text.split("\n")

    return {
        "name":   info_table.find("b").text,
        "index":  table_text_arr[13],
        "type_1": table_text_arr[47],
        "type_2": table_text_arr[49],
    }
