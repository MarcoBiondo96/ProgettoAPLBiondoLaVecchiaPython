import calendar
import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import BytesIO
from flask import send_file
import matplotlib
matplotlib.use('Agg')#Implementato per risolvere delle problematiche relative all'utilizzo dei thread.  La funzione use di Matplotlib è utilizzata per impostare il backend di rendering in Agg. In quanto possono verificarsi problemi quando più richieste HTTP vengono elaborate in contemporanea.
def salva_grafico(fig):#Viene passato il grafico e viene convertito in formato Bytes per poterla inviare tramite send_file
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()  
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')

 
def dailyuser_graph(data,graph):#Funzione che in base agli orari_lobby arrivati (rappresentano una singola prenotazione da parte di un utente) li suddivide nelle ore in cui sono state fatte
        orari_lobby_list = data["orari_lobby"]
        datanome_gioco=data["gioco"]
        x_list = list(range(24))  
        y_list = [0] * 24  
        for value in orari_lobby_list:
            hour = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').hour
            y_list[hour] += 1
        graph.plot(x_list, y_list)
        graph.set_xlabel('Orario')
        graph.set_ylabel('Utenti in lobby')
        graph.set_title(f"Numero di utenti del giorno in lobby per {datanome_gioco}")
        graph.set_xticks(x_list)
        graph.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        return salva_grafico(graph)


def monthuser_graph(data,graph):#Fa lo stesso solo che fa la suddivisione per i gironi nel mese corrente
        orari_lobby_list = data["orari_lobby"]
        datanome_gioco=data["gioco"]
        if orari_lobby_list: 
            num_giorni=calendar.monthrange(datetime.datetime.strptime(orari_lobby_list[0], '%Y-%m-%d %H:%M:%S').year, datetime.datetime.strptime(orari_lobby_list[0], '%Y-%m-%d %H:%M:%S').month)[1]#Serve a prelevare il numero di gironi presenti nel mese corrente
            
            x_list = [x + 1 for x in list(range(num_giorni))]            
            y_list = [0] * num_giorni  
            for value in orari_lobby_list:
                day = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').day
                y_list[day] += 1
            graph.plot(x_list, y_list)
            graph.set_xlabel('Orario')
            graph.set_ylabel('Utenti in lobby')
            graph.set_title(f"Numero di utenti del mese in lobby per {datanome_gioco}")
            graph.set_xticks(x_list[::2])
            graph.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            return salva_grafico(graph)
        else:
            graph.plot(0, 0)
            graph.set_title(f"Nessuna prenotazioni nel mese per: {datanome_gioco}")
            return salva_grafico(graph)

def yearuser_graph(data, graph):#Fa lo stesso solo che fa la suddivisione per i mesi dell'anno
    orari_lobby_list = data["orari_lobby"]
    datanome_gioco = data["gioco"]
    x_list = x_list = [x + 1 for x in list(range(12))]  
    y_list = [0] * 12 
    for value in orari_lobby_list:
        month = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').month
        y_list[month] += 1
    graph.plot(x_list, y_list)
    graph.set_xlabel('Mese')
    graph.set_ylabel('Utenti in lobby')
    graph.set_title(f"Numero di utenti dell'anno per {datanome_gioco}")
    graph.set_xticks(x_list)
    graph.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    return salva_grafico(graph)
    