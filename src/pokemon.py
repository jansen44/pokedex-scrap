
# Built-in
from urllib.request import urlopen as uOpen, Request as uReq

# Third-party
from bs4 import BeautifulSoup as soup

# Local
from src.util import recreate_file

def get_poke_soup(link):
    uClient         = uReq(link, headers={'User-Agent': 'Magic Browser'})
    uCon            = uOpen(uClient)
    poke_page_html  = uCon.read()
    uCon.close()
    return soup(poke_page_html, 'html.parser')

def get_next_pokemon_link(poke_soup):
    npl = poke_soup.find(id='mw-content-text').table
    try:
        npl = npl.findChildren('tr', recursive=False)[1]    \
                 .findChildren('td', recursive=False)[2]
    except IndexError:
        npl = npl.findChildren('tr', recursive=False)[0]    \
                 .findChildren('td', recursive=False)[2]
    finally:
        return npl.find('a')['href']            
        

def get_poke_info(poke_soup):
    core = get_core_poke_info(poke_soup)
    
    return {
        'core': {
            'index':       core[0],
            'name':        core[1],
            'category':    core[2],
            'jp_name':     core[3],
            'jp_rom_name': core[4]
        }
    }
    

# Name, category, index, jp/name
def get_core_poke_info(poke_soup):
    info_table = poke_soup                      \
                    .find(id='mw-content-text') \
                    .find_all('table', recursive=False)[1]

    base_info_container = info_table.tr.td \
                            .table.tr


    info_container = base_info_container.td \
                        .table.tr           \
                        .find_all('td', recursive=False)
    
    return (
        int(base_info_container.th.find('a').text.replace('#', '')), # index

        info_container[0].big.text,                                  # name
        info_container[0].a.text,                                    # category
        info_container[1].span.text,                                 # jp_name
        info_container[1].i.text                                     # jp_rom_name
    )
