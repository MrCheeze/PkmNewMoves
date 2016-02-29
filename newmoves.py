from bs4 import BeautifulSoup
import urllib2
from urllib2 import quote, unquote

pokemon_num = ["001", "002", "003", "004", "005", "006", "007", "008", "009","010","011", "012", "013", "014", "015", "016", "017", "018", "019", "020","021", "022", "023", "024", "025", "026", "027", "028", "029", "030","031", "032", "033", "034", "035", "036", "037", "038", "039", "040","041", "042", "043", "044", "045", "046", "047", "048", "049", "050","051", "052", "053", "054", "055", "056", "057", "058", "059", "060","061", "062", "063", "064", "065", "066", "067", "068", "069", "070","071", "072", "073", "074", "075", "076", "077", "078", "079", "080","081", "082", "083", "084", "085", "086", "087", "088", "089", "090","091", "092", "093", "094", "095", "096", "097", "098", "099", "100","101", "102", "103", "104", "105", "106", "107", "108", "109", "110","111", "112", "113", "114", "115", "116", "117", "118", "119", "120","121", "122", "123", "124", "125", "126", "127", "128", "129", "130","131", "132", "133", "134", "135", "136", "137", "138", "139", "140","141", "142", "143", "144", "145", "146", "147", "148", "149", "150","151"]


#pokemon_num = ["010"]

pokemon_name = ["Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash","Nidoran-f","Nidorina","Nidoqueen","Nidoran-m","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetch'd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr. Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew"]


url_gen1 = "http://serebii.net/pokedex/"
url_gen6 = "http://serebii.net/pokedex-xy/"

url_end = ".shtml"


def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_headers = row.find_all('th')
        if table_headers:
            results.append([headers.get_text() for headers in table_headers])

        table_data = row.find_all('td')[0:2]
        if table_data:
            results.append([data.get_text() for data in table_data])
    return results

def check_table(table):
   """ Checks to see if the table holds moves """

   table_headers = table.find_all('th', {"class" : "attheader" })
   #print(table_headers)
   if(table_headers != []): # For some reason the stats do not have headers...
       return True
   return False

for s in pokemon_num:

    wiki_gen1 = url_gen1 + s + url_end
    page_gen1 = urllib2.urlopen(wiki_gen1)
    wiki_gen6 = url_gen6 + s + url_end
    page_gen6 = urllib2.urlopen(wiki_gen6)

    soup1 = BeautifulSoup(page_gen1, "lxml")
    soup6 = BeautifulSoup(page_gen6, "lxml")
    #print(soup)

    try:
        table1 = soup1.findAll('table', { "class" : "dextable" })
        table6 = soup6.findAll('table', { "class" : "dextable" })

        gen1_start = 5
        gen1_end = 7 # starting tables for moves in RBY
        gen6_start = 6
        gen6_end = 10 # Starting table for moves in ORAS/XY

        rby_tables = []
        oras_tables = []

        kk=gen1_start

        #print(len(table1))
        #print(len(table6))

        while(kk<len(table1)):
            if(check_table(table1[kk])):
                rby_tables.append(table1[kk].find_all('tr'))    
            kk=kk+1

        kk=gen6_start
        #print("check tables")
        while(kk<len(table6)):
            if(check_table(table6[kk])):
                oras_tables.append(table6[kk].find_all('tr'))    
            kk=kk+1
        #print(len(oras_tables))


    except AttributeError as e:
        raise ValueError("No valid table found")

    rby_moves = [parse_rows(rby_tables[0])[::2]]
    oras_moves = [parse_rows(oras_tables[0])[::2]]
    kk=0
    for ii in rby_tables[1:]:
        rby_moves.append(parse_rows(ii)[::2])

    for ii in oras_tables[1:]:
        oras_moves.append(parse_rows(ii)[::2])

    #print("")
    #print(rby_moves)
    #print("")

    #    for ii in rby_moves:
    #        for jj in ii:
    #            print("\t".join(jj))

    #    for ii in oras_moves:
    #        for jj in ii:
    #            print("\t".join(jj))

    move_list_rby = []
    move_list_oras = []

    for ii in rby_moves:
        for jj in ii[1:]:
            temp = quote((jj[-1].encode('utf-8'))).title()
            if((len(temp) < 20) and not("Lv." in temp) and not("\n" in temp) ):
                move_list_rby.append(temp)
    for ii in oras_moves:
        for jj in ii[1:]:
            if(quote(jj[-1].encode('utf-8'))==''):
                temp = quote((jj[0].encode('utf-8'))).title()
                if((len(temp) < 20) and not("Lv." in temp) and not("\n" in temp) ):
                    move_list_oras.append(temp)
            else:
                temp = quote((jj[-1].encode('utf-8'))).title()
                if((len(temp) < 20) and not("Lv." in temp) and not("\n" in temp) ):
                    move_list_oras.append(temp)
        
    #print(move_list_oras)
    #print("")

    set_rby = set(move_list_rby)
    set_oras = set(move_list_oras)

    #print(set_rby)
    #print(set_oras)

    set_new_moves = sorted(set_rby-set_oras)

    #print("")
    #print(set_new_moves)

    print("")
    print(s + " " + pokemon_name[int(s)-1] + ":")
    for ii in set_new_moves:
        print(unquote(ii).decode('utf-8'))
