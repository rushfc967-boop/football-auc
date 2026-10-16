from database import init_db, add_player, count_players, count_by_position, get_conn

PLAYERS = [
    # GK (40)
    ("GK","Manuel Neuer",2.5),("GK","Alisson Becker",2.5),("GK","Thibaut Courtois",2.5),
    ("GK","Ederson Moraes",2),("GK","Jan Oblak",2),("GK","Mike Maignan",2),
    ("GK","Gianluigi Donnarumma",2.5),("GK","Emiliano Martinez",2),("GK","Marc-Andre ter Stegen",2),
    ("GK","Andre Onana",2),("GK","David Raya",1.5),("GK","Aaron Ramsdale",1.5),
    ("GK","Jordan Pickford",1.5),("GK","Edouard Mendy",1.5),("GK","Hugo Lloris",1.5),
    ("GK","Keylor Navas",1.5),("GK","Yann Sommer",1.5),("GK","Robert Sanchez",1.5),
    ("GK","Gregor Kobel",1.5),("GK","Diogo Costa",1.5),("GK","Andriy Lunin",1),
    ("GK","Kepa Arrizabalaga",1),("GK","Samir Handanovic",1),("GK","Wojciech Szczesny",1),
    ("GK","Steve Mandanda",1),("GK","Alex Meret",1),("GK","Guglielmo Vicario",1),
    ("GK","Bernd Leno",1),("GK","Alphonse Areola",1),("GK","Dean Henderson",1),
    ("GK","Nick Pope",1),("GK","Jose Sa",1),("GK","Lukas Hradecky",1),
    ("GK","Koen Casteels",1),("GK","Marco Silvestri",0.5),("GK","Pierluigi Gollini",0.5),
    ("GK","Antonio Mirante",0.5),("GK","Alex Remiro",0.5),("GK","Unai Simon",1),
    ("GK","Geronimo Rulli",0.5),

    # DEF (100)
    ("DEF","Paolo Maldini",4),("DEF","Franz Beckenbauer",3.5),("DEF","Sergio Ramos",3),
    ("DEF","Virgil van Dijk",3),("DEF","Roberto Carlos",3),("DEF","Cafu",2.5),
    ("DEF","Carles Puyol",2.5),("DEF","Gerard Pique",2),("DEF","Thiago Silva",2),
    ("DEF","Ruben Dias",3),("DEF","Antonio Rudiger",2),("DEF","Alphonso Davies",2.5),
    ("DEF","Trent Alexander-Arnold",3),("DEF","Andrew Robertson",2.5),("DEF","Kyle Walker",2),
    ("DEF","Jordi Alba",2),("DEF","Matthijs de Ligt",2.5),("DEF","Alessandro Bastoni",2),
    ("DEF","Marquinhos",2.5),("DEF","Josko Gvardiol",2),("DEF","Achraf Hakimi",2.5),
    ("DEF","Theo Hernandez",2.5),("DEF","David Alaba",2),("DEF","Milan Skriniar",2),
    ("DEF","Kalidou Koulibaly",2),("DEF","Raphael Varane",2),("DEF","Harry Maguire",1.5),
    ("DEF","John Stones",2),("DEF","William Saliba",2.5),("DEF","Gabriel Magalhaes",2),
    ("DEF","Ben White",2),("DEF","Oleksandr Zinchenko",1.5),("DEF","Kieran Tierney",1.5),
    ("DEF","Reece James",2.5),("DEF","Ben Chilwell",2),("DEF","Cesar Azpilicueta",1.5),
    ("DEF","Wesley Fofana",1.5),("DEF","Levi Colwill",1.5),("DEF","Jules Kounde",2.5),
    ("DEF","Ronald Araujo",2.5),("DEF","Andreas Christensen",1.5),("DEF","Eric Garcia",1.5),
    ("DEF","Alejandro Balde",2),("DEF","Dani Carvajal",1.5),("DEF","Ferland Mendy",1.5),
    ("DEF","Antonio Militao",2),("DEF","Nacho Fernandez",1.5),("DEF","Stefan de Vrij",1.5),
    ("DEF","Francesco Acerbi",1.5),("DEF","Giovanni Di Lorenzo",1.5),("DEF","Kim Min-jae",2),
    ("DEF","Matteo Darmian",1),("DEF","Denzel Dumfries",1.5),("DEF","Robin Gosens",1),
    ("DEF","Manuel Akanji",2),("DEF","Nathan Ake",1.5),("DEF","Joao Cancelo",2),
    ("DEF","Sergio Gomez",1),("DEF","Luke Shaw",1.5),("DEF","Lisandro Martinez",2),
    ("DEF","Victor Lindelof",1),("DEF","Aaron Wan-Bissaka",1),("DEF","Diogo Dalot",1.5),
    ("DEF","Tyrell Malacia",0.5),("DEF","Ibrahima Konate",2),("DEF","Joel Matip",1.5),
    ("DEF","Joe Gomez",1),("DEF","Kostas Tsimikas",0.5),("DEF","Cristian Romero",2),
    ("DEF","Micky van de Ven",2),("DEF","Destiny Udogie",1.5),("DEF","Emerson Royal",1),
    ("DEF","Ben Davies",0.5),("DEF","Kieran Trippier",1.5),("DEF","Sven Botman",1.5),
    ("DEF","Fabian Schar",1),("DEF","Dan Burn",0.5),("DEF","Max Kilman",1),
    ("DEF","Craig Dawson",0.5),("DEF","Kurt Zouma",0.5),("DEF","Thilo Kehrer",0.5),
    ("DEF","Emerson Palmieri",0.5),("DEF","Angelo Ogbonna",0.5),("DEF","Aaron Cresswell",0.5),
    ("DEF","Vladimir Coufal",0.5),("DEF","Ben Johnson",0.5),("DEF","Nayef Aguerd",1),
    ("DEF","Konstantinos Mavropanos",0.5),("DEF","Jean-Clair Todibo",1),("DEF","Aurelien Tchouameni",2.5),
    ("DEF","Eduardo Camavinga",2.5),("DEF","Sergio Reguilon",0.5),("DEF","Federico Dimarco",2),
    ("DEF","Alessandro Florenzi",0.5),("DEF","Davide Calabria",1),("DEF","Pierre Kalulu",1.5),
    ("DEF","Malick Thiaw",1.5),("DEF","Fikayo Tomori",2),("DEF","Alessio Romagnoli",1.5),

    # MID (90)
    ("MID","Zinedine Zidane",5),("MID","Andres Iniesta",4),("MID","Xavi Hernandez",4),
    ("MID","Kevin De Bruyne",3.5),("MID","Luka Modric",3),("MID","Steven Gerrard",3),
    ("MID","Frank Lampard",3),("MID","Paul Scholes",3),("MID","Andrea Pirlo",3.5),
    ("MID","Ronaldinho",4),("MID","Kaka",3.5),("MID","Rodri",3),
    ("MID","Jude Bellingham",3.5),("MID","Pedri",3),("MID","Frenkie de Jong",3),
    ("MID","Casemiro",2.5),("MID","Ngolo Kante",3),("MID","Toni Kroos",3),
    ("MID","Bruno Fernandes",3),("MID","Martin Odegaard",3),("MID","Federico Valverde",3),
    ("MID","Declan Rice",2.5),("MID","Enzo Fernandez",2.5),("MID","Moises Caicedo",2),
    ("MID","Alexis Mac Allister",2.5),("MID","Dominik Szoboszlai",2),("MID","Ryan Gravenberch",2),
    ("MID","Curtis Jones",1.5),("MID","Harvey Elliott",1.5),("MID","Thiago Alcantara",2),
    ("MID","Wataru Endo",1),("MID","Mason Mount",2),("MID","Kobbie Mainoo",2),
    ("MID","Christian Eriksen",1.5),("MID","Scott McTominay",1.5),("MID","Bruno Guimaraes",2.5),
    ("MID","Joelinton",2),("MID","Joe Willock",1.5),("MID","Sandro Tonali",2),
    ("MID","Ilkay Gundogan",2),("MID","Bernardo Silva",3),("MID","Phil Foden",3),
    ("MID","Matheus Nunes",1.5),("MID","Kalvin Phillips",1),("MID","Jack Grealish",2.5),
    ("MID","Jeremy Doku",2),("MID","Mateo Kovacic",2),("MID","Nicolo Barella",2.5),
    ("MID","Hakan Calhanoglu",2),("MID","Henrikh Mkhitaryan",1.5),("MID","Davide Frattesi",1.5),
    ("MID","Piotr Zielinski",1.5),("MID","Stanislav Lobotka",1.5),("MID","Andre-Frank Zambo Anguissa",1.5),
    ("MID","Fabian Ruiz",2),("MID","Sergej Milinkovic-Savic",2),("MID","Luis Alberto",1.5),
    ("MID","Nicolo Rovella",1),("MID","Manuel Locatelli",1.5),("MID","Adrien Rabiot",1.5),
    ("MID","Weston McKennie",1),("MID","Federico Chiesa",2),("MID","Paul Pogba",2),
    ("MID","Marco Verratti",2),("MID","Warren Zaire-Emery",2.5),("MID","Vitinha",2),
    ("MID","Lee Kang-in",1.5),("MID","Carlos Soler",1.5),("MID","Dani Ceballos",1.5),
    ("MID","Arda Guler",1.5),("MID","Gavi",2),("MID","Oriol Romeu",1),
    ("MID","Sergi Roberto",1),("MID","Pablo Torre",1),("MID","Fermin Lopez",1),
    ("MID","Joao Felix",2.5),("MID","Joao Palhinha",1.5),("MID","Andreas Pereira",1),
    ("MID","Youri Tielemans",2),("MID","Douglas Luiz",2),("MID","John McGinn",1.5),
    ("MID","Jacob Ramsey",1.5),("MID","Boubacar Kamara",1.5),("MID","Amadou Onana",1.5),
    ("MID","Abdoulaye Doucoure",1),("MID","Idrissa Gueye",1),("MID","James Garner",1),

    # FWD (70)
    ("FWD","Lionel Messi",5),("FWD","Cristiano Ronaldo",5),("FWD","Kylian Mbappe",5),
    ("FWD","Erling Haaland",5),("FWD","Neymar Jr",4),("FWD","Robert Lewandowski",4),
    ("FWD","Karim Benzema",3.5),("FWD","Mohamed Salah",4),("FWD","Sadio Mane",3),
    ("FWD","Vinicius Jr",4),("FWD","Thierry Henry",4),("FWD","Ronaldo Nazario",5),
    ("FWD","Wayne Rooney",3),("FWD","Zlatan Ibrahimovic",3.5),("FWD","Luis Suarez",3),
    ("FWD","Sergio Aguero",3),("FWD","Antoine Griezmann",3),("FWD","Harry Kane",4),
    ("FWD","Lautaro Martinez",3),("FWD","Victor Osimhen",3),("FWD","Rafael Leao",3),
    ("FWD","Ousmane Dembele",2.5),("FWD","Randal Kolo Muani",2),("FWD","Marco Asensio",2),
    ("FWD","Takefusa Kubo",2),("FWD","Rodrygo",3),("FWD","Endrick",2),
    ("FWD","Bukayo Saka",3.5),("FWD","Gabriel Martinelli",2.5),("FWD","Gabriel Jesus",2.5),
    ("FWD","Eddie Nketiah",1.5),("FWD","Leandro Trossard",2),("FWD","Kai Havertz",2.5),
    ("FWD","Cole Palmer",2.5),("FWD","Nicolas Jackson",2),("FWD","Raheem Sterling",2.5),
    ("FWD","Mykhailo Mudryk",2),("FWD","Christopher Nkunku",2.5),("FWD","Diogo Jota",2.5),
    ("FWD","Darwin Nunez",2.5),("FWD","Luis Diaz",3),("FWD","Cody Gakpo",2),
    ("FWD","Son Heung-min",3),("FWD","Richarlison",2),("FWD","Dejan Kulusevski",2),
    ("FWD","Brennan Johnson",1.5),("FWD","Alexander Isak",2.5),("FWD","Anthony Gordon",2),
    ("FWD","Callum Wilson",1.5),("FWD","Miguel Almiron",1.5),("FWD","Harvey Barnes",1.5),
    ("FWD","Ollie Watkins",2.5),("FWD","Leon Bailey",1.5),("FWD","Moussa Diaby",2),
    ("FWD","Jhon Duran",1.5),("FWD","Marcus Rashford",2.5),("FWD","Antony",1.5),
    ("FWD","Alejandro Garnacho",2),("FWD","Rasmus Hojlund",2.5),("FWD","Anthony Martial",1.5),
    ("FWD","Jadon Sancho",1.5),("FWD","Amad Diallo",1),("FWD","Florian Wirtz",3),
    ("FWD","Victor Boniface",2),("FWD","Serhou Guirassy",2),("FWD","Karim Adeyemi",2),
    ("FWD","Donyell Malen",1.5),("FWD","Jonathan David",2),("FWD","Viktor Gyokeres",2.5),
]

def seed():
    init_db()
    conn = get_conn()
    conn.execute("DELETE FROM players")
    conn.commit()
    conn.close()
    for pos, name, base in PLAYERS:
        add_player(name, pos, base)
    print(f"Seeded {len(PLAYERS)} players")
    print(f"Breakdown: {count_by_position()}")

if __name__ == "__main__":
    seed()
