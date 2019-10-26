
# Built-in
from urllib.request import urlopen as uOpen, Request as uReq

# Third-party
from bs4 import BeautifulSoup as soup

# Local
from src.util import recreate_file

# Core Functions ===================================================================================
def get_poke_soup(link):
    uClient         = uReq(link, headers={'User-Agent': 'Magic Browser'})
    uCon            = uOpen(uClient)
    poke_page_html  = uCon.read()
    uCon.close()
    
    return soup(poke_page_html, 'html.parser')

def check_last_page(poke_soup):
    return poke_soup.find(id='mw-content-text').table.a['href'] == "/wiki/File:BulbaShadow.png"

def get_poke_info(poke_soup):
    info_table = poke_soup                      \
                    .find(id='mw-content-text') \
                    .find_all('table', recursive=False)[1]

    core          = get_core_poke_info(info_table)
    types         = get_poke_types(info_table)
    abilities     = get_poke_abilities(info_table)
    gender_ratios = get_poke_gender_ratio(info_table)
    catch_rate    = get_poke_catch_ratio(info_table)
    egg_groups    = get_poke_egg_group(info_table)
    hatch_time    = get_poke_hatch_time(info_table)
    height        = get_poke_height(info_table)
    weight        = get_poke_weight(info_table)
    mega_stones   = get_poke_megastones(info_table)
    
    return {
        'image_link':   core[0],
        'index':        core[1],
        'name':         core[2],
        'categories':   core[3],
        'jp_name':      core[4],
        'jp_rom_name':  core[5],
        'types':        types,
        'abilities':    abilities,
        'gender_ratio': gender_ratios,
        'catch_rate':   catch_rate,
        'egg_groups':   egg_groups,
        'hatch_time':   hatch_time,
        'height':       height,
        'weight':       weight,
        'mega_stones':  mega_stones
    }

# Data Extraction Functions ===========================================================================
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
 
def get_core_poke_info(info_table):
    base_info_container = info_table.tr.td.table.tr

    info_container = base_info_container.td.table.tr      \
                        .find_all('td', recursive=False)
    
    category = info_container[0].a.find_all('span')
    categories = [cat.text for cat in category]
    
    if len(categories) > 1:
        categories = list(filter(lambda cat: cat.find('Pokémon') == -1, categories))
        categories = list(map(lambda cat: cat + ' Pokémon', categories))
    
    image_link = 'https:' + info_table.img['src']
    
    return (
        image_link,                                                  # image_link
        int(base_info_container.th.find('a').text.replace('#', '')), # index
        info_container[0].big.text,                                  # name
        categories,                                                  # category
        info_container[1].span.text,                                 # jp_name
        info_container[1].i.text                                     # jp_rom_name
    )
    
def get_poke_types(info_table):
    types = info_table.find_all('tr', recursive=False)[1]          \
                      .table.find('td', attrs={'style': None}) \
                      .find_all('a')
    
    return [t.text for t in types if t.text != 'Unknown']

def get_poke_abilities(info_table):
    ability_title = info_table.find('a', attrs={'title': 'Ability'})
    abilities = []

    for parent in ability_title.parents:        
        if parent.name == 'td':
            abilities_container = parent.table.find_all('td')
            
            for td in abilities_container:
                if not td.has_attr('style') or (not 'display: none' in td['style']):
                    ability = td.find('a').text

                    hidden_ability_container = td.find('small')
                    if  hidden_ability_container != None:
                        ability += f' ({hidden_ability_container.text.strip()})'

                    abilities.append(ability)
            break
    
    
    return abilities

def get_poke_gender_ratio(info_table):
    gender_ratio_titles = info_table.find('a', attrs={'title': 'List of Pokémon by gender ratio'})
    ratios = []

    for parent in gender_ratio_titles.parents:        
        if parent.name == 'td':
            ratios_container = parent.table.find_all('td')
            
            for td in ratios_container:
                unformatted_ratio = td.find('a')
                if not td.has_attr('style') and unformatted_ratio != None:
                    unformatted_ratio = td.find('a').text
                    ratios = list(map(lambda r: r.strip(), unformatted_ratio.split(',')))

            break
    return ratios

def get_poke_catch_ratio(info_table):
    catch_ratio_titles = info_table.find('a', attrs={'title': 'Catch rate'})
    ratio = ""
    
    for parent in catch_ratio_titles.parents:        
        if parent.name == 'td':
            ratio = parent.table.td.text.strip()
            break
    return ratio

def get_poke_egg_group(info_table):
    egg_group_link = info_table.find('a', attrs={'title': 'Egg Group'})
    groups = []
    
    for parent in egg_group_link.parents:
        if parent.name == 'td':
            egg_groups = parent.table.find_all('span')
            
            for egg_group in egg_groups:
                groups.append(egg_group.text)
                
            break
    
    return groups

def get_poke_hatch_time(info_table):
    hatch_time_link = info_table.find('a', attrs={'title': 'Egg cycle'})

    for parent in hatch_time_link.parents:
        if parent.name == 'td':
            hatch_time = parent.table.td.text.strip()

            hatch_time_formatted = hatch_time.split('Egg')
            if len(hatch_time_formatted) > 1:
                hatch_time = ' (Egg'.join(hatch_time_formatted)
                hatch_time += ')'
                
            return hatch_time

def get_poke_height(info_table):
    height_link = info_table.find('a', attrs={'title': 'List of Pokémon by height'})
    heights = []
    
    for parent in height_link.parents:
        if parent.name == 'td':
            height_container = parent.table.find('tr', attrs={'style': None})
            
            for height in height_container.find_all('td'):
                heights.append(height.text.strip())
            
            break
    
    return heights

def get_poke_weight(info_table):
    weight_link = info_table.find('a', attrs={'title': 'Weight'})
    weights = []
    
    for parent in weight_link.parents:
        if parent.name == 'td':
            weight_container = parent.table.find('tr', attrs={'style': None})
            
            for weight in weight_container.find_all('td'):
                weights.append(weight.text.strip())
            
            break
    
    return weights

def get_poke_megastones(info_table):
    mega_stone = info_table.find_all('a', attrs={'title': 'Mega Stone'})
    mega_stone = list(filter(lambda ms: ms['href'] != '/wiki/Mega_Stone', mega_stone))

    return list(map(lambda ms: ms.text, mega_stone)) if len(mega_stone) > 0 else []
