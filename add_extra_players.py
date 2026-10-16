from database import init_db, add_player, get_conn, count_players, count_by_position

init_db()

# ---- 1. Multiply existing bases × 5 (CR → M) ----
conn = get_conn()
conn.execute("UPDATE players SET base_price = base_price * 5")
conn.commit()
conn.close()
print("✅ Multiplied all existing bases × 5")

# ---- 2. Add more players (bases already in M) ----
EXTRA = [
    # 20 GK
    ("Lucas Chevalier","GK",10),("Mile Svilar","GK",10),("Marco Carnesecchi","GK",10),
    ("Bart Verbruggen","GK",10),("Marcin Bulka","GK",8),("Giorgi Mamardashvili","GK",10),
    ("Filip Jorgensen","GK",8),("Marco Sportiello","GK",5),("Juan Musso","GK",8),
    ("Paulo Gazzaniga","GK",5),("Marko Dmitrovic","GK",5),("Sergio Rico","GK",5),
    ("Nick Pope","GK",8),("Jose Sa","GK",8),("Lukas Hradecky","GK",8),
    ("Koen Casteels","GK",8),("Alphonse Areola","GK",5),("Bernd Leno","GK",5),
    ("Samir Handanovic","GK",5),("Alex Meret","GK",5),

    # 20 DEF
    ("Antonio Silva","DEF",10),("Leny Yoro","DEF",10),("Ousmane Diomande","DEF",10),
    ("Goncalo Inacio","DEF",10),("Castello Lukeba","DEF",10),("Milos Kerkez","DEF",10),
    ("Rayan Ait-Nouri","DEF",8),("Nuno Mendes","DEF",13),("Yann Bisseck","DEF",8),
    ("Giorgio Scalvini","DEF",8),("Nicolas Otamendi","DEF",8),("Dayot Upamecano","DEF",13),
    ("Jonathan Tah","DEF",10),("Edmond Tapsoba","DEF",10),("Nico Schlotterbeck","DEF",10),
    ("Waldemar Anton","DEF",8),("Robin Le Normand","DEF",10),("Pau Torres","DEF",10),
    ("Marc Bartra","DEF",5),("Nathan Collins","DEF",8),

    # 20 MID
    ("Martin Zubimendi","MID",13),("Mikel Merino","MID",10),("Tijjani Reijnders","MID",13),
    ("Teun Koopmeiners","MID",13),("Youssouf Fofana","MID",10),("Manuel Ugarte","MID",10),
    ("Enzo Le Fee","MID",8),("Amine Adli","MID",8),("Pape Sarr","MID",8),
    ("Seko Fofana","MID",10),("Ibrahim Sangare","MID",8),("Giacomo Raspadori","MID",10),
    ("Matias Vecino","MID",5),("Lorenzo Pellegrini","MID",10),("Bryan Cristante","MID",8),
    ("Marcel Sabitzer","MID",10),("Julian Brandt","MID",10),("Giovanni Fabbian","MID",8),
    ("Lewis Ferguson","MID",8),("Conor Gallagher","MID",10),

    # 20 FWD
    ("Ansu Fati","FWD",10),("Ferran Torres","FWD",13),("Christian Pulisic","FWD",13),
    ("Samuel Chukwueze","FWD",10),("Noah Okafor","FWD",8),("Youssoufa Moukoko","FWD",8),
    ("Paulo Dybala","FWD",13),("Lorenzo Insigne","FWD",8),("Ciro Immobile","FWD",10),
    ("Andrea Belotti","FWD",8),("Gianluca Scamacca","FWD",10),("Moise Kean","FWD",10),
    ("Sardar Azmoun","FWD",8),("Mehdi Taremi","FWD",10),("Moussa Dembele","FWD",8),
    ("Wissam Ben Yedder","FWD",8),("Alexandre Lacazette","FWD",8),("Kevin Volland","FWD",5),
    ("Jean-Philippe Mateta","FWD",8),("Odsonne Edouard","FWD",8),
]

added = 0
for name, pos, base in EXTRA:
    add_player(name, pos, base)
    added += 1

print(f"✅ Added {added} more players")
print(f"📊 Total: {count_players()}")
print(f"   {count_by_position()}")
