import requests
import datetime

def get_player_info(api_key, nome_ev):
    url = f"https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{nome_ev}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_player_info_id(api_key, nome_ev):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nome_ev}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
def get_player_matches(api_key, puuid):
    url = f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={api_key}"
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
        if rank.get("queueType") == "RANKED_TFT_DOUBLE_UP":
            return rank
    return {}

def get_match_details(api_key, match_id):
    url = f"https://europe.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def calculate_winrate(wins, losses):
    total_matches = wins + losses
    if total_matches == 0:
        return 0
    return (wins / total_matches) * 100

def process_player_data(api_key_tft, api_key_lol,nome_ev):
    
    player_info = get_player_info(api_key_tft, nome_ev)
    
    if not player_info:
        return "Errore_account_non_esistente"
    
    puuid = player_info.get('puuid')
    summoner_id = get_player_info_id(api_key_lol, nome_ev).get('id')
    
    matches = get_player_matches(api_key_tft, puuid)
    player_rank = get_player_rank(api_key_lol, summoner_id)
    
    tier = player_rank.get('tier', "Nessuno")
    rank = player_rank.get('rank', "Nessuno")
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
    
    for match_id in matches:
        match_details = get_match_details(api_key_tft, match_id)
        if not match_details:
            continue
        
        match_info = match_details.get('info')
        participants = match_info.get('participants', [])
        
        for participant in participants:
            if puuid in participant.get('puuid', ''):
                singolo = {
                    "match_id": match_details.get('metadata', {}).get('match_id'),
                    "livello": participant.get("level"),
                    "piazzamento": participant.get("placement"),
                    "giocatoriEliminati": participant.get("players_eliminated"),
                    "durata_partita": str(datetime.timedelta(seconds=participant.get('time_eliminated', 0))),
                    "unita_team": [unit.get("character_id").split("_", 1)[1] for unit in participant.get("units", [])],
                }
                
                player_data["matchs"].append(singolo)
                
                if 1 <= singolo["piazzamento"] <= 4:
                    wins += 1
                else:
                    losses += 1
    
    player_data["winrate"] = calculate_winrate(wins, losses)
    return player_data


