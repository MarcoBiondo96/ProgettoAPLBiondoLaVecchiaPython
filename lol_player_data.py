import requests
import datetime

def get_player_info(api_key, nome_ev):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nome_ev}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player_matches(api_key, puuid):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_player_rank(api_key, summoner_id):
    url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    response = requests.get(url)
    ranks = response.json()
    
    for rank in ranks:
        if rank.get("queueType") == "RANKED_SOLO_5x5":
            return rank
    return {}

def get_match_details(api_key, match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def calculate_kda(kills, deaths, assists):
    if deaths == 0:
        return kills + assists
    return (kills + assists) / deaths

def process_player_data(api_key, nome_ev):
    player_info = get_player_info(api_key, nome_ev)
    
    if not player_info:
        return "Errore_account_non_esistente"
    
    puuid = player_info.get('puuid')
    summoner_id = player_info.get('id')
    
    matches = get_player_matches(api_key, puuid)
    player_rank = get_player_rank(api_key, summoner_id)
    
    tier = player_rank.get('tier')
    rank = player_rank.get('rank')
    win_ranked = player_rank.get('wins', 0)
    lose_ranked = player_rank.get('losses', 0)
    
    player_data = {
        "infoplayer": {
            "nome_evocatore": nome_ev,
            "tier": tier,
            "rank": rank,
            "win_ranked": win_ranked,
            "lose_ranked": lose_ranked,
        },
        "matchs": [],
    }
    
    wins = 0
    losses = 0
    incontri = []
    
    for match_id in matches:
        match_details = get_match_details(api_key, match_id)
        
        if not match_details:
            continue
        
        singolo = {}
        info_match = match_details.get('info')
        partecipanti = info_match.get('participants', [])
        
        for partecipante in partecipanti:
            if puuid in partecipante.get('puuid', ''):
                singolo["mode"] = info_match.get('gameMode')
                singolo["match_id"] = match_details.get('metadata', {}).get('matchId')
                
                if partecipante.get('win'):
                    singolo["risultato"] = "Vittoria"
                    wins += 1
                else:
                    singolo["risultato"] = "Sconfitta"
                    losses += 1
                
                singolo["campione"] = partecipante.get('championName')
                singolo["assists"] = partecipante.get('assists')
                singolo["deaths"] = partecipante.get('deaths')
                singolo["kills"] = partecipante.get('kills')
                
                singolo["kda"] = calculate_kda(
                    partecipante.get('kills', 0),
                    partecipante.get('deaths', 0),
                    partecipante.get('assists', 0)
                )
                
                singolo["durata_partita"] = str(datetime.timedelta(seconds=partecipante.get('timePlayed', 0)))
                
                incontri.append(singolo)
    
    player_data["matchs"] = incontri
    player_data["winrate"] = calculate_winrate(wins, losses)
    return player_data

def calculate_winrate(wins, losses):
    total_matches = wins + losses
    if total_matches == 0:
        return 0
    return (wins / total_matches) * 100

