from database import init_db, add_player, get_conn, count_players, count_by_position

EXTRA_PLAYERS = [
    # FWD - Current superstars
    ("FWD","Lamine Yamal",3),
    ("FWD","Rayan Cherki",2.5),
    ("FWD","Desire Doue",2.5),
    ("FWD","Nico Williams",2.5),
    ("FWD","Bradley Barcola",2),
    ("FWD","Jamal Musiala",3),
    ("FWD","Michael Olise",2.5),
    ("FWD","Xavi Simons",2.5),
    ("FWD","Khicha Mbeumo",2),
    ("FWD","Marcus Thuram",2.5),
    ("FWD","Mateo Retegui",2),
    ("FWD","Ademola Lookman",2.5),
    ("FWD","Kenan Yildiz",2.5),
    ("FWD","Dusan Vlahovic",2.5),
    ("FWD","Santiago Gimenez",2),
    ("FWD","Nicolas Gonzalez",2),
    ("FWD","Benjamin Sesko",2),
    ("FWD","Lois Openda",2),
    ("FWD","Rasmus Kristensen",1.5),
    ("FWD","Cody Gakpo",2),  # already hai, dedupe skip hoga

    # MID - Current stars
    ("MID","Joao Neves",2.5),
    ("MID","Nico Paz",2),
    ("MID","Kendry Paez",1.5),
    ("MID","Claudio Echeverri",1.5),
    ("MID","Franco Mastantuono",2),
    ("MID","Estevao Willian",2.5),
    ("MID","Lucas Paqueta",2.5),
    ("MID","Bruno Guimaraes",2.5),  # already hai
    ("MID","Morgan Gibbs-White",2),
    ("MID","Eberechi Eze",2.5),
    ("MID","Adam Wharton",2),
    ("MID","Kobbie Mainoo",2),  # already hai
    ("MID","Aleksandar Pavlovic",2),
    ("MID","Angelo Stiller",2),
    ("MID","Hugo Larsson",1.5),
    ("MID","Archie Gray",1.5),
    ("MID","Lucas Bergvall",1.5),
    ("MID","Sarr Pape Matar",1.5),
    ("MID","Manu Kone",2),
    ("MID","Khvicha Kvaratskhelia",3),

    # DEF - Current stars
    ("DEF","Marc Guehi",2),
    ("DEF","Jarrad Branthwaite",2),
    ("DEF","Riccardo Calafiori",2),
    ("DEF","Pau Cubarsi",2.5),
    ("DEF","Leny Yoro",2),
    ("DEF","Antonio Silva",2),
    ("DEF","Goncalo Inacio",2),
    ("DEF","Ousmane Diomande",2),
    ("DEF","Castello Lukeba",2),
    ("DEF","Yann Bisseck",1.5),
    ("DEF","Milos Kerkez",2),
    ("DEF","Rayan Ait-Nouri",1.5),
    ("DEF","Alejandro Garnacho",2),  # already hai
    ("DEF","Nuno Mendes",2.5),
    ("DEF","Vitinho",1.5),
    ("DEF","Valentin Barco",1.5),

    # GK - Current
    ("GK","Lucas Chevalier",1.5),
    ("GK","Giorgio Scalvini",1.5),
    ("GK","Mile Svilar",1.5),
    ("GK","Marco Carnesecchi",1.5),
    ("GK","Bart Verbruggen",1.5),
]

def add_extra():
    init_db()
    conn = get_conn()
    existing = set(r[0] for r in conn.execute("SELECT name FROM players").fetchall())
    conn.close()

    added = 0
    skipped = 0
    for pos, name, base in EXTRA_PLAYERS:
        if name in existing:
            skipped += 1
            continue
        add_player(name, pos, base)
        added += 1
        existing.add(name)

    print(f"✅ Added {added} new players")
    print(f"⏭️ Skipped {skipped} duplicates")
    print(f"📊 Total pool: {count_players()}")
    print(f"   Breakdown: {count_by_position()}")

if __name__ == "__main__":
    add_extra()
