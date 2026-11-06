"""Atualiza data.json (Série A e Premier League) pela API football-data.org.
Série B e Libertadores continuam manuais: edite data.json à mão."""
import json, os, sys, unicodedata, urllib.request
from datetime import date

KEY = os.environ.get("FOOTBALL_DATA_KEY", "")
TARGETS = {"Série A": "BSA", "Premier League": "PL"}
FORM_NEWEST_LAST = True  # confira na 1ª execução: o último caractere deve ser o jogo mais recente
RULES = [("athletico","Athletico-PR"),("paranaense","Athletico-PR"),("mineiro","Atlético-MG"),("bragantino","Bragantino"),
 ("flamengo","Flamengo"),("palmeiras","Palmeiras"),("cruzeiro","Cruzeiro"),("fluminense","Fluminense"),("bahia","Bahia"),
 ("santos","Santos"),("sao paulo","São Paulo"),("botafogo","Botafogo"),("coritiba","Coritiba"),("vasco","Vasco"),
 ("mirassol","Mirassol"),("vitoria","Vitória"),("internacional","Internacional"),("corinthians","Corinthians"),
 ("gremio","Grêmio"),("remo","Remo"),("chapecoense","Chapecoense"),
 ("arsenal","Arsenal"),("manchester city","Man City"),("manchester united","Man United"),("brighton","Brighton"),
 ("chelsea","Chelsea"),("liverpool","Liverpool"),("brentford","Brentford"),("everton","Everton"),("bournemouth","Bournemouth"),
 ("tottenham","Tottenham"),("aston villa","Aston Villa"),("leeds","Leeds"),("hull","Hull"),("newcastle","Newcastle"),
 ("ipswich","Ipswich"),("fulham","Fulham"),("coventry","Coventry"),("crystal palace","Crystal Palace"),
 ("nottingham","Forest"),("sunderland","Sunderland")]

def norm(t):
    return unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().lower()

def name(team):
    for raw in (team.get("name",""), team.get("shortName","")):
        n = norm(raw)
        for k, v in RULES:
            if k in n:
                return v
    return team.get("shortName") or team.get("name")

def fetch(code):
    req = urllib.request.Request(f"https://api.football-data.org/v4/competitions/{code}/standings",
                                 headers={"X-Auth-Token": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def form_str(f):
    if not f: return ""
    m = {"W": "V", "D": "E", "L": "D"}
    s = "".join(m.get(c, "") for c in f.replace(",", ""))
    s = s if FORM_NEWEST_LAST else s[::-1]
    return s[-5:]

def main():
    if not KEY:
        sys.exit("Defina FOOTBALL_DATA_KEY")
    path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    data = json.load(open(path, encoding="utf-8"))
    for league, code in TARGETS.items():
        table = next(s["table"] for s in fetch(code)["standings"] if s["type"] == "TOTAL")
        if len(table) != 20:
            sys.exit(f"{league}: tabela inesperada ({len(table)} times)")
        old = {t[0]: t for t in data["leagues"][league]["teams"]}
        teams = []
        for r in table:
            n = name(r["team"])
            row = [n, r["points"], r["playedGames"], r["won"], r["draw"], r["lost"], r["goalDifference"]]
            if data["leagues"][league].get("form"):
                prev = old.get(n, [])
                row.append(form_str(r.get("form")) or (prev[7] if len(prev) > 7 else ""))
            teams.append(row)
        L = data["leagues"][league]
        L["teams"] = teams
        L["upd"] = date.today().strftime("%d/%m/%Y")
        if league == "Premier League":
            L["sub"] = f"Premier League 2026/27 · {max(t[2] for t in teams)} rodadas disputadas"
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("data.json atualizado")

if __name__ == "__main__":
    main()
