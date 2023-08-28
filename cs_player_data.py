import requests

def get_cs_stats(api_key, nome_ev):
    url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={api_key}&steamid={nome_ev}"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("playerstats", {}).get("stats", [])
    else:
        return None

def create_cs_dict(stats):
    dict_to_send = {}
    dict_not_to_send = {}
    #lista che serve per prelevare unicamente i valori delle chiavi dalla chiamata effettuata a steam per cs con nomi uguali a quelli della lista
    accepted_name = [
        "total_kills", "total_time_played", "total_damage_done",
        "total_kills_headshot", "last_match_wins", "last_match_rounds",
        "last_match_kills", "last_match_deaths", "last_match_damage"
    ]
    #lista usata per prelevare valori delle chiavi alla stessa maniera di accepted_name, ma i valori qui presenti non verranno inviati, ma usati per calcolare altri valori che verranno successivamente inviati
    accepted_name_not_to_send = [
        "total_matches_won", "total_matches_played",
        "total_shots_hit", "total_shots_fired", "total_deaths"
    ]
    
    for item in stats:
        n = item.get("name")
        v = item.get("value")

        if n in accepted_name:
            dict_to_send[n] = v
        elif n in accepted_name_not_to_send:
            dict_not_to_send[n] = v
    
    dict_to_send["kd_ratio"] = calculate_ratio(dict_to_send.get("total_kills", 0), dict_not_to_send.get("total_deaths", 1))
    dict_to_send["total_wins_perc"] = calculate_percentage(dict_not_to_send.get("total_matches_won", 0), dict_not_to_send.get("total_matches_played", 1))
    dict_to_send["last_match_kd_ratio"] = calculate_ratio(dict_to_send.get("last_match_kills", 0), dict_to_send.get("last_match_deaths", 1))
    dict_to_send["accuracy_perc"] = calculate_percentage(dict_not_to_send.get("total_shots_hit", 0), dict_not_to_send.get("total_shots_fired", 1))
    
    return dict_to_send

def calculate_ratio(numerator, denominator):
    return float("{:.2f}".format(numerator / denominator))

def calculate_percentage(part, whole):
    return float("{:.1f}".format(part / whole * 100))

def process_cs_data(api_key, nome_ev):
    stats = get_cs_stats(api_key, nome_ev)
    
    if stats is None:
        return "Errore_account_non_esistente"
    
    cs_dict = create_cs_dict(stats)
    return cs_dict

