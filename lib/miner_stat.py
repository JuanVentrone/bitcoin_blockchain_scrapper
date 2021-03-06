import urllib, json
import os
import requests
import pandas as pd
import math
import numpy as np
import math
from bs4 import BeautifulSoup
import configparser


# If You are using Collab, coment init_cof() Fun, and if name---- and use the class

# class html_class:
#     # Default Classes, but before run it, check all the class in the page

#     height_link = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk'
#     div_table = 'hnfgic-0 enzKJw'
#     left_column_table = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP sc-1n72lkw-0 ebXUGH'
#     right_column_table = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC'
#     miner_name = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk'


# class dir_:
#     # Path where is locate the last data & Path save new one
#     data_crudo = 'data/data_crudo.csv'
#     uni_data = 'data/uni_data/'


def init_conf():
  read_config = configparser.ConfigParser(allow_no_value=True)
  conf_dir = os.path.join(os.path.realpath(''), 'conf.ini')
  read_config.read( conf_dir )
  class html_class:
        # Default Classes, but before run it, check all the class in the page
        height_link = read_config.get('HTMl_Class', 'height_link')
        div_table = read_config.get('HTMl_Class', 'div_table')
        left_column_table = read_config.get('HTMl_Class', 'left_column_table')
        right_column_table = read_config.get('HTMl_Class', 'right_column_table')
        miner_name = read_config.get('HTMl_Class', 'miner_name')
  class dir_:
        # Path where is locate the last data & Path save new one
        data_crudo = read_config.get('Dir', 'data_crudo')
        uni_data = read_config.get('Dir', 'uni_data' )
  return html_class, dir_

def pool_pie():
    # Español
    # Una estimación de la distribución de hashrate entre los mayores grupos mineros.
    # Basado en un porcentaje de los Bloques Minado por cada Pool
    # English
    # An estimation of hashrate distribution amongst the largest mining pools.
    # Based on a percentage of the blocks mined for each Pool
    url_pool= "https://api.blockchain.info/pools?timespan=7days"
    r = requests.get(url_pool)
    datos_json = r.json()
    datos_json
    datos_pool = pd.DataFrame(datos_json.items(), columns=['Pool', 'Block_Founds'])
    n_bf = sum( datos_pool["Block_Founds"] )
    datos_pool["BF_Percent"] = datos_pool["Block_Founds"] / n_bf
    return ( datos_pool, n_bf )

def blockchain_stats():
    # Español
    # Informacion En estadistica del Blockchain
    # English 
    # Info Blockchain Stats
    url_pool = "https://api.blockchain.info/stats"
    r = requests.get( url_pool )
    datos_varios = r.json() 
    return datos_varios

def block_scrapper_pages( n_pages_1, n_range_block ):
    # Español
    # Escrapea https://www.blockchain.com/btc/blocks Extae valores de cada Bloque
    # Englisg
    # Scrapper https://www.blockchain.com/btc/blocks Get Values from each Block
    if type(n_pages_1) == tuple:  n_pages_1 = range( n_pages_1[ 0 ], n_pages_1[ -1 ] )
    if type(n_pages_1) == int:    n_pages_1 = range( 0, n_pages_1 )
    data_temp=[]
    data_error=[]
    g=0   
    for i in n_pages_1:
            
        if (( type(n_pages_1) == tuple ) + ( type(n_pages_1) == range ) == 1):
            print("Escrapeando pagina: ", i )
            url_pages = "https://www.blockchain.com/btc/blocks?page=" + str(i)
        else:
            print("escrapeando pagina: ",i+1)
            url_pages = "https://www.blockchain.com/btc/blocks?page=" + str( i+1 )
            

        try:
            url_pages = requests.get( url_pages )
            if url_pages.status_code == 200:
                print( "BLoques buscados: ", n_range_block )
                # Scrapping the mean Page --- Escrapeo la pagina principal
                sopa = BeautifulSoup( url_pages.text, "html5lib" )                     

                links = sopa.find_all( "a" ,attrs = {"class": html_class.height_link })
                links_blocks = [ link.get("href") for link in links ]  
                # Scrapping each block-page --- Escrapeo cada pagina del bloque
                if type(n_range_block) == range:
                    block_links = finding_blocks( n_range_block, links_blocks,links )
                else:
                    block_links,n_range_block = normal_blocks( n_range_block, links_blocks )
                
                for b in block_links:
                    pagina_url = requests.get( b )
                    if pagina_url.status_code == 200:
                        
                        lista_h = []
                        lista_q = []
                        datos_temporal = {}
                        s = BeautifulSoup( pagina_url.text, "html5lib" )
                        p = s.find("div", attrs={'class': 'hnfgic-0 enzKJw'})
                    
                        h = p.find_all("span", attrs= {'class': html_class.left_column_table })
                        q = p.find_all("span", attrs= {'class': html_class.right_column_table })
                        
                        lista_q = [q[c].get_text() for c in range(len(q))]
                        lista_h = [h[d].get_text() for d in range(len(h))]            
                        lista_h.remove( 'Miner' )
                        lista_q.pop(10)
                                    
                        for e in range(len( lista_q )):
                            datos_temporal[lista_h[e]] = lista_q[e]
                                                                
                        miner_wallet_link = p.find( "a", attrs={ 'class': html_class.miner_name})
                        datos_temporal["Miner Name"] = miner_wallet_link.get_text()
                        datos_temporal["URL Miner"] = miner_wallet_link.get("href")
                        
                        g = graph_bar(g)

                        data_temp.append( datos_temporal )
                        
        except Exception as e:
            print(str(e))
            if (( type(n_pages_1) == tuple ) + ( type(n_pages_1) == range ) == 1 ):
                print("no se encontro la URL:", i )
                data_error.append(i)
            else:
                print("no se encontro la URL:", i+1 )
                data_error.append( i+1 )
            pass
    if data_temp==[]: data_temp = [None]
    return data_temp,data_error

def normal_blocks(n_range_block,links_blocks):
    block_links=[]
    contador=0            
    
    if n_range_block>50:
        n_range_block -=50
        c = 50
    else:
        c = n_range_block

    for a in range(c):
        block_links.append( "https://www.blockchain.com" + str( links_blocks[contador] ))
        contador +=3
    return (block_links,
            n_range_block)


def finding_blocks( n_range_block,
                    links_blocks,
                    links ):

    block_links = []
    bloques = []
    contador = 0
    for a in range(50):
        if int(links[contador].get_text()) in n_range_block:
            block_links.append("https://www.blockchain.com" + links_blocks[contador])
        bloques.append(links[contador].get_text())
        contador +=3

    print("Rango de bloques en la pagina: ",min( bloques ), "-", max( bloques ))

    return block_links

def scrapper_update():
    
    # Español:
    # Ejecuta si la tabla esta actualizada o no, para escoger que se debe scrappear
    # Esta funcion debe ejecutarse despues de tener una data Hecha solo sirve para actualizar
    # English
    # Run if the table is updated or not, to choose what should be scrapped
    # This function must be executed after having information. It is only used to update
    
    stats = blockchain_stats()
    n_range_block = stats.get("n_blocks_total")

    if os.path.exists(dir_.data_crudo):

        data_old = pd.read_csv( dir_.data_crudo )
        print("diferencias de bloques ", n_range_block, max( data_old["Height"] ))
        n_range_block = n_range_block - max( data_old["Height"] )
        print( n_range_block )
        # Verificando si la Tabla esta Actualizada
        # Checking if the Table is Updated

        if n_range_block == 0: 
            return print("Los datos estan actualizados al ultimo Bloque Minado :" + str(n_range_block) )  
        
        n_pages = math.ceil( n_range_block / 50 )
        # Iniciando el scrapper 
        # Scrapper Innit
        df, dr = block_scrapper_pages ( n_pages, n_range_block )
        
        if dr == []:
              df_suma = pipe_data(data_old, df)
        else:
            df_new = last_scrpapping( df, dr, n_range_block )      
            df_suma = pipe_data(data_old, df_new)
        df_suma.to_csv( dir_.data_crudo )
    else:
        print("No se puede ejecutar todo el scrappeo, tomaria mucho tiempo puedes ejecutar la Func: scrapper_partitions ",
            " donde puedes particionar el scrapper")
    return print("Funcion scrapper_update Completa")
    
def scrapper_partitions(page_init,n_times):
    # Español:
    # Ejecuta si la tabla esta actualizada o no, para escoger que se debe scrappear
    # page_init: Es el valor donde quieres que empiece el Scrapper
    # n_times: es la posicion final que deseas que termine el Scrappeo
    # Ejemplo: si n_pages_1 empieza en 1000 y n_pages_2 es 200, Scrappea desde el 1000 hasta el 1200
    # English
    # Run if the table is updated or not, to choose what should be scrapper
    # page_init: Is the value pages that you want to start it.
    # n_times: the final position you want the Scrapped, means to end of it
    # Example: if n_pages_1 starts at 1000 and n_pages_2 is 200,maake a Scrappring from 1000 to 1200

        stats = blockchain_stats()
        n_range_block = stats.get("n_blocks_total")
       

        n_pages_1 = (page_init, page_init + n_times )
        n_range_block = n_range_block - (page_init * 50)

        df, dr = block_scrapper_pages( n_pages_1, n_range_block )
        df_new = last_scrpapping(df, dr, n_range_block)
        df_new.to_csv( dir_.uni_data +"data_" + str(page_init) + "_" + str(page_init + n_times) + ".csv")
        
        s = input("¿Desea unir todas las los datos particionados? SI: Presione cualquier tecla")
        if s != "":
            uni_table( dir_.uni_data )
            print("La data sea creado satisfactoriamente")
            return

        return print("EL Scrappeo se efectuo exitosamente: ", page_init, "-" ,page_init + n_times)

def last_scrpapping(df, dr, n_range_block):

    # Español:
    # Procesado Final para luego guardar el Scrapper

    # English:
    # Final Scrapper Procces

        df_new = pd.DataFrame(df)
        df_2, dr_2 = block_scrapper_pages(dr, n_range_block)
        if dr_2 != []: print("Analizar que ocurre con las paginas:", dr_2)
        if df_2 != [None]:
            df_new_2 = pd.DataFrame(df_2)
            df_new = df_new.append(df_new_2)
        # df_new.drop(df_new.columns[df_new.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        return df_new

def scrapper_lost_block():

    # Español:
    # Scrappea los bloques que no fueron scrappeandos anteriormente, Los bloques y el rango de las paginas donde deben estar.
   
    # English
    # Scrap blocks that were not scrapped before, get rank list
       
        data = pd.read_csv("data/rang_lost_blocks.csv")
        data.drop( data.columns[data.columns.str.contains('unnamed',case = False)], axis = 1, inplace = True )
        data = data.astype('int64')
        data_temp = pd.DataFrame()

        for i in range(len(data)):
            
            n_pages_1 = range( data["Ini Page"][i], data["Final Page"][i] )
            n_range_block = range(data["I block"][i],data["F block"][i]+1)
            df, dr = block_scrapper_pages(n_pages_1, n_range_block)
            
            if df != [None]: 
                if dr != []:
                    df = last_scrpapping(df, dr, n_range_block)
                else:
                    df = pd.DataFrame(df)
                data_temp = data_temp.append(df)
            
        
        if "Height" in data_temp:
            
            data_temp["Height"] = data_temp["Height"].astype(int)
            data_temp = data_temp.sort_values( by=['Height'], ascending=False )
            data_temp = data_temp.drop_duplicates("Height")
            if 'Unnamed: 0' in data_temp: data_temp.drop( data_temp.columns[data_temp.columns.str.contains('unnamed',case = False)], axis = 1, inplace = True )
            data_temp.dropna(subset=["Height"], inplace=True)
            data_temp.to_csv("data/uni_data/find_block" + str(n_range_block) + ".csv")
            print("Proceso Exitosamente Finalizado")
            
            

        else:
            print("No se encontro ninguno de los bloques buscados")
                
def graph_bar(g):

    graph = [" / "," - "," \ "," | "]
    if g == 3:
        print( "\r", graph[g], end='' )
        g=0
    else:
        print( "\r", graph[g], end='' )
        g+=1
    return g

def n_block():
    stats = blockchain_stats()
    return stats.get("n_blocks_total")


def rango_b(a, b, i,
            block_f, lista_height):

    while a == lista_height[i]:
        if a == b:
            return print("Finalizo la Busqueda de Bloques no escrapeados")
        a += 1
        i += 1
    block_f.append([a, lista_height[i]])

    return rango_b(lista_height[i], b,
                   i,  block_f, lista_height)

def process(block_f):

    page_url_list = []
    total = n_block()
    for i in block_f:

        a = math.ceil(((total - i[0]) / 50) + 2)
        b = math.ceil(((total - i[1]) / 50) - 1)
        page_url_list.append(
            {"Ini Page": b, "Final Page": a, "I block": i[0], "F block": i[1]})

    return page_url_list

def find_lost_block():

    data = read_data()
    data["Height"] = data["Height"].astype(int)
    lista_height = list(data["Height"])
    lista_height.sort()
    a = min(lista_height)
    b = max(lista_height)
    print(a, b)
    block_f = []
    i = 0
    rango_b(a, b, i,
            block_f, lista_height)

    if block_f == []:
        return print("La data tiene todos los bloques", len(data), "-", max(data["Height"]))
    df = process(block_f)
    df_error_pages = pd.DataFrame(df)
    df_error_pages.to_csv("data/rang_lost_blocks.csv")

    # Continue to Scrap the page?

    # r=str(input("El Proceso se realizo exitosamente!,¿Desea Scrappear los Bloques Faltantes,?,Presione cualquier tecla"))
    # if r!="": scrapper_lost_block()

def uni_table(direc):
    
    g = 0
    data = pd.DataFrame()
    director = []
    dir_tables = os.listdir(direc)
    for dir in dir_tables:
        if not dir.startswith('.'):
          director.append(dir)
    if director != []:
      for i in director:   
          try:
              data_temp = pd.read_csv(str( direc + i ))
              data = data.append(data_temp)
              g = graph_bar(g)
          except:
              print("No se pudo concatenar:", str( direc + i ))
              pass
              
    return data

def read_data():

    data = pd.read_csv( dir_.data_crudo )
    if 'Unnamed: 0' in data:
        data.drop(data.columns[data.columns.str.contains(
            'unnamed', case=False)], axis=1, inplace=True)
    return data

def concat_partition_data():

    # Concatena todos los datos que estan particionados.
    # Para luego unificarlos con la Data principal
    #
    # Concatenates all the data that are partitioned.
    # Then concattenate with the main data

    data_old = read_data()
    data_new = uni_table( dir_.uni_data )

    if not data_new.empty:
      data_new = pipe_data(data_old, data_new)
      data_new.to_csv("data/partition_manual_data_crudo.csv")
      print("Guardado data/partition_data_crudo.csv")

    else:
      return print("La Lista esta Vacia")

def concat_lost_block():
    # Concatena todos los datos faltantes ya escrappeados
    # con la data principal
    # Concatenate all missing and scrapped data with the main data
    data_old = read_data()
    data_new = uni_table("data/uni_data/")
    if not data_new.empty:
        data_new = pipe_data(data_old, data_new)
        data_new.to_csv( dir_.data_crudo )
        print("Guardado en blockchain data/data_crudo.csv")
    else:
        return print("La Lista esta Vacia")

def partition_lost_bock():

    data = pd.read_csv("data/rang_lost_blocks.csv")
    x = int(len(data) / 12)

    lista = []
    for i in range(x):
        lista.append([i*x, i*x+x])

    for i in lista:
        data_temp = data[i[0]: i[1]]
        data_temp.to_csv(
            "data/lost_blocks/"+str(i[0])+"_"+str(i[1])+".csv")

def coy_file():
    import shutil
    from datetime import date
    shutil.copyfile("data/data_crudo.csv",
                    "data/data_update_"+str(date.today())+".csv")
    print("Data Actualizada")

def pipe_data(data_old, data_new):
    data_new = data_old.append(data_new)
    data_new.dropna(subset=["Height"], inplace=True)
    data_new["Height"] = data_new["Height"].astype(int)
    data_new = data_new.drop_duplicates("Height")
    data_new = data_new.sort_values(by=['Height'], ascending=False)
    if 'Unnamed: 0' in data_new:
        data_new.drop(data_new.columns[data_new.columns.str.contains(
                'unnamed', case=False)], axis=1, inplace=True)
    return data_new

def init_update():
    scrapper_update()
    find_lost_block()
    if os.path.exists("data/rang_lost_blocks.csv"):
        scrapper_lost_block()
        concat_lost_block()
        os.remove("data/rang_lost_blocks.csv")
        find_lost_block()
    if os.path.exists("data/rang_lost_blocks.csv"):
        return print("ADVERTENCIA: puede haber algun error en la da data_crudo.csv, por favor chequear")
    else:
        coy_file()
        return print("Actualizado Por favor revisar")



if __name__ == "__main__":
    html_class, dir_ = init_conf()

# Codigo Creado por Juan Vicente Ventrone
# github.com/JuanVentrone
# Creating Code by Juan Vicente Venctrone
