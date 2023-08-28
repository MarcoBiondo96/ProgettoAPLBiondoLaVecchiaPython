from flask import Flask ,request
import requests
import datetime
import sys
import matplotlib.pyplot as plt
import json
import graph_fun
import tft_player_data
import lol_player_data
import cs_player_data
import config

app=Flask("Apl")#Creazione di un'istanza dell'applicazione Flask fa da server
api_lol=config.LOL_API_KEY#Prelevazione dal file config delle api key relative alle 2 case video ludiche (quella della riot va aggionata ogni 24 ore all'interno del file config.py)
api_steam=config.STEAM_API_KEY
api_tft=config.TFT_API_KEY
@app.route('/graph', methods=['POST'])#Route che permete di ricevere una richiesta di un tipologia di grafico e lo restituisce
def graph():   
    data =json.loads(request.data)#lettura dati dal post
    fig, graph = plt.subplots()
    if(data["tipologia"]=="dailyuser"):#in base alla tipolgia viene richiamato un grafico da generare
        return graph_fun.dailyuser_graph(data,graph)
    elif(data["tipologia"]=="monthuser"):
        return graph_fun.monthuser_graph(data,graph)
    elif(data["tipologia"]=="yearuser"):
        return graph_fun.yearuser_graph(data,graph)

@app.route('/tft/<nome_ev>')#Route che permete di ricevere un richiesta tramite il metodo get , restituisce i dati relativi ad un utente specificato dal parametro del get
def richiesta_tft(nome_ev):
    return tft_player_data.process_player_data(api_tft, api_lol,nome_ev)

@app.route('/lol/<nome_ev>')
def richiesta_lol(nome_ev):
    return lol_player_data.process_player_data(api_lol, nome_ev)
    
@app.route('/processlogin/<nome_ev>')
def dict_cs_creation(nome_ev):
    return cs_player_data.process_cs_data(api_steam, nome_ev)
    
if __name__== '__main__':
    app.run(debug=True)
