from urllib.request import urlopen as uOpen, Request as uReq
from bs4 import BeautifulSoup as soup, NavigableString

uClient         = uReq('https://bulbapedia.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_that_are_part_of_a_three-stage_evolutionary_line&pagefrom=Raichu+%28Pok%C3%A9mon%29#mw-pages', headers={'User-Agent': 'Magic Browser'})
uCon            = uOpen(uClient, None, 5)
poke_page_html  = uCon.read()
uCon.close()

ps = soup(poke_page_html, 'html.parser')
ps = ps.find(attrs={'id': 'mw-content-text'}).find('div', attrs={'class': 'mw-category'})


with open('d.txt', 'a') as f:
    ps = ps.find_all('a')
    ps = [p.text.replace(' (Pokémon)', '\n') for p in ps]
    for p in ps:
        f.write(p)
