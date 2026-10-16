from database import get_conn, init_db, add_player, count_players, count_by_position

POOL = {
    "GK": [
        # Modern ELITE
        ("Gianluigi Buffon", 20), ("Lev Yashin", 22), ("Edwin van der Sar", 18),
        ("Peter Schmeichel", 18), ("Iker Casillas", 18), ("Petr Cech", 16),
        ("Oliver Kahn", 16), ("Dida", 12),
        ("Thibaut Courtois", 18), ("Alisson Becker", 17), ("Ederson Moraes", 16),
        ("Manuel Neuer", 16), ("Gianluigi Donnarumma", 16),
        ("Marc-Andre ter Stegen", 15), ("Jan Oblak", 15),
        ("Emiliano Martinez", 14), ("Mike Maignan", 14), ("Andre Onana", 13),
        ("David Raya", 13), ("Diogo Costa", 13), ("Gregor Kobel", 12),
        ("Giorgi Mamardashvili", 12), ("Yann Sommer", 12),
        ("Lucas Chevalier", 12), ("Marco Carnesecchi", 12),
        ("Aaron Ramsdale", 11), ("Jordan Pickford", 11), ("Edouard Mendy", 10),
        ("Robert Sanchez", 10), ("Bart Verbruggen", 10), ("Mile Svilar", 10),
        ("Andriy Lunin", 9), ("Kepa Arrizabalaga", 9), ("Wojciech Szczesny", 9),
        ("Guglielmo Vicario", 9), ("Bernd Leno", 9), ("Nick Pope", 9),
        ("Jose Sa", 8), ("Lukas Hradecky", 8), ("Koen Casteels", 8),
        ("Marcin Bulka", 8), ("Filip Jorgensen", 8), ("Hugo Lloris", 8),
        ("Alphonse Areola", 7), ("Dean Henderson", 7), ("Alex Meret", 7),
        ("Unai Simon", 7), ("Keylor Navas", 7),
        ("Marco Silvestri", 6), ("Alex Remiro", 6), ("Juan Musso", 6),
        ("Pierluigi Gollini", 5), ("Antonio Mirante", 5), ("Geronimo Rulli", 5),
        ("Paulo Gazzaniga", 5), ("Marko Dmitrovic", 5), ("Sergio Rico", 5),
    ],

    "DEF": [
        # Legends
        ("Franco Baresi", 22), ("Gaetano Scirea", 18), ("Fabio Cannavaro", 18),
        ("Bobby Moore", 18),
        # Elite
        ("Paolo Maldini", 25), ("Franz Beckenbauer", 22), ("Sergio Ramos", 20),
        ("Virgil van Dijk", 20), ("Roberto Carlos", 18), ("Cafu", 18),
        ("Carles Puyol", 17), ("Ruben Dias", 17), ("Trent Alexander-Arnold", 17),
        ("Gerard Pique", 15), ("Thiago Silva", 15), ("Alphonso Davies", 15),
        ("Andrew Robertson", 15), ("Antonio Rudiger", 14), ("Matthijs de Ligt", 14),
        ("Marquinhos", 14), ("Achraf Hakimi", 14), ("Theo Hernandez", 14),
        ("Kyle Walker", 13), ("Jordi Alba", 13), ("Alessandro Bastoni", 13),
        ("Josko Gvardiol", 13), ("David Alaba", 12), ("Milan Skriniar", 12),
        ("Kalidou Koulibaly", 12), ("Raphael Varane", 12), ("William Saliba", 12),
        ("Reece James", 12), ("Jules Kounde", 12), ("Ronald Araujo", 12),
        ("John Stones", 11), ("Gabriel Magalhaes", 11), ("Ben White", 11),
        ("Ben Chilwell", 11), ("Alejandro Balde", 11), ("Antonio Militao", 11),
        ("Manuel Akanji", 11), ("Joao Cancelo", 11), ("Lisandro Martinez", 11),
        ("Ibrahima Konate", 11), ("Cristian Romero", 11), ("Micky van de Ven", 11),
        ("Federico Dimarco", 11), ("Fikayo Tomori", 11), ("Marc Guehi", 11),
        ("Jarrad Branthwaite", 11), ("Riccardo Calafiori", 11), ("Antonio Silva", 11),
        ("Leny Yoro", 11), ("Ousmane Diomande", 11), ("Goncalo Inacio", 11),
        ("Castello Lukeba", 11), ("Milos Kerkez", 11), ("Dayot Upamecano", 11),
        ("Nuno Mendes", 11), ("Kim Min-jae", 10), ("Aurelien Tchouameni", 10),
        ("Eduardo Camavinga", 10), ("Jonathan Tah", 10), ("Edmond Tapsoba", 10),
        ("Nico Schlotterbeck", 10), ("Robin Le Normand", 10), ("Pau Torres", 10),
        ("Rayan Ait-Nouri", 10), ("Giorgio Scalvini", 10),
        ("Davide Calabria", 9), ("Malick Thiaw", 9), ("Alessio Romagnoli", 9),
        ("Pierre Kalulu", 9), ("Yann Bisseck", 9), ("Nicolas Otamendi", 9),
        ("Waldemar Anton", 9), ("Nathan Collins", 9),
        ("Oleksandr Zinchenko", 8), ("Kieran Tierney", 8), ("Cesar Azpilicueta", 8),
        ("Wesley Fofana", 8), ("Levi Colwill", 8), ("Andreas Christensen", 8),
        ("Eric Garcia", 8), ("Dani Carvajal", 8), ("Ferland Mendy", 8),
        ("Nacho Fernandez", 8), ("Stefan de Vrij", 8), ("Francesco Acerbi", 8),
        ("Giovanni Di Lorenzo", 8), ("Denzel Dumfries", 8), ("Nathan Ake", 8),
        ("Luke Shaw", 8), ("Diogo Dalot", 8), ("Joel Matip", 8),
        ("Destiny Udogie", 8), ("Kieran Trippier", 8), ("Sven Botman", 8),
        ("Harry Maguire", 8),
        ("Robin Gosens", 7), ("Sergio Gomez", 7), ("Victor Lindelof", 7),
        ("Aaron Wan-Bissaka", 7), ("Joe Gomez", 7), ("Emerson Royal", 7),
        ("Fabian Schar", 7), ("Max Kilman", 7), ("Nayef Aguerd", 7),
        ("Jean-Clair Todibo", 7),
        ("Tyrell Malacia", 5), ("Kostas Tsimikas", 5), ("Ben Davies", 5),
        ("Dan Burn", 5), ("Craig Dawson", 5), ("Kurt Zouma", 5),
        ("Thilo Kehrer", 5), ("Emerson Palmieri", 5), ("Angelo Ogbonna", 5),
        ("Aaron Cresswell", 5), ("Vladimir Coufal", 5), ("Ben Johnson", 5),
        ("Konstantinos Mavropanos", 5), ("Marc Bartra", 5), ("Sergio Reguilon", 5),
    ],

    "MID": [
        # Legends
        ("Michel Platini", 22), ("Lothar Matthaus", 18), ("Ruud Gullit", 18),
        # Elite
        ("Zinedine Zidane", 25), ("Andres Iniesta", 22), ("Xavi Hernandez", 22),
        ("Ronaldinho", 22), ("Kevin De Bruyne", 20), ("Andrea Pirlo", 20),
        ("Kaka", 20),
        ("Luka Modric", 17), ("Steven Gerrard", 17), ("Frank Lampard", 17),
        ("Paul Scholes", 17), ("Rodri", 17), ("Jude Bellingham", 17),
        ("Pedri", 15), ("Frenkie de Jong", 15), ("Ngolo Kante", 15),
        ("Toni Kroos", 15), ("Bruno Fernandes", 15), ("Martin Odegaard", 15),
        ("Federico Valverde", 15), ("Bernardo Silva", 15), ("Phil Foden", 15),
        ("Khvicha Kvaratskhelia", 15),
        ("Casemiro", 13), ("Declan Rice", 13), ("Enzo Fernandez", 13),
        ("Alexis Mac Allister", 13), ("Bruno Guimaraes", 13), ("Jack Grealish", 13),
        ("Nicolo Barella", 13), ("Warren Zaire-Emery", 13), ("Joao Felix", 13),
        ("Joao Neves", 13), ("Estevao Willian", 13), ("Martin Zubimendi", 13),
        ("Tijjani Reijnders", 13), ("Teun Koopmeiners", 13),
        ("Moises Caicedo", 10), ("Dominik Szoboszlai", 10), ("Ryan Gravenberch", 10),
        ("Thiago Alcantara", 10), ("Mason Mount", 10), ("Kobbie Mainoo", 10),
        ("Joelinton", 10), ("Sandro Tonali", 10), ("Ilkay Gundogan", 10),
        ("Jeremy Doku", 10), ("Mateo Kovacic", 10), ("Hakan Calhanoglu", 10),
        ("Fabian Ruiz", 10), ("Sergej Milinkovic-Savic", 10), ("Federico Chiesa", 10),
        ("Paul Pogba", 10), ("Marco Verratti", 10), ("Vitinha", 10),
        ("Gavi", 10), ("Youri Tielemans", 10), ("Douglas Luiz", 10),
        ("Nico Paz", 10), ("Morgan Gibbs-White", 10), ("Adam Wharton", 10),
        ("Franco Mastantuono", 10), ("Mikel Merino", 10), ("Youssouf Fofana", 10),
        ("Manuel Ugarte", 10), ("Seko Fofana", 10), ("Giacomo Raspadori", 10),
        ("Lorenzo Pellegrini", 10), ("Marcel Sabitzer", 10), ("Julian Brandt", 10),
        ("Conor Gallagher", 10),
        ("Curtis Jones", 8), ("Harvey Elliott", 8), ("Christian Eriksen", 8),
        ("Scott McTominay", 8), ("Joe Willock", 8), ("Matheus Nunes", 8),
        ("Henrikh Mkhitaryan", 8), ("Davide Frattesi", 8), ("Piotr Zielinski", 8),
        ("Stanislav Lobotka", 8), ("Luis Alberto", 8), ("Manuel Locatelli", 8),
        ("Adrien Rabiot", 8), ("Lee Kang-in", 8), ("Carlos Soler", 8),
        ("Dani Ceballos", 8), ("Arda Guler", 8), ("Joao Palhinha", 8),
        ("John McGinn", 8), ("Boubacar Kamara", 8), ("Amadou Onana", 8),
        ("Eberechi Eze", 8), ("Enzo Le Fee", 8), ("Amine Adli", 8),
        ("Pape Sarr", 8), ("Ibrahim Sangare", 8), ("Bryan Cristante", 8),
        ("Giovanni Fabbian", 8), ("Lewis Ferguson", 8),
    ],

    "FWD": [
        # Legends
        ("Pele", 25), ("Diego Maradona", 25), ("Ferenc Puskas", 20),
        ("Alfredo Di Stefano", 20), ("Johan Cruyff", 22), ("Eusebio", 18),
        ("Gerd Muller", 18),
        # Elite
        ("Lionel Messi", 25), ("Cristiano Ronaldo", 25), ("Kylian Mbappe", 25),
        ("Erling Haaland", 25), ("Ronaldo Nazario", 25),
        ("Neymar Jr", 22), ("Robert Lewandowski", 22), ("Mohamed Salah", 22),
        ("Karim Benzema", 20), ("Vinicius Jr", 20), ("Thierry Henry", 20),
        ("Harry Kane", 20),
        ("Sadio Mane", 17), ("Zlatan Ibrahimovic", 17), ("Bukayo Saka", 17),
        ("Wayne Rooney", 15), ("Luis Suarez", 15), ("Sergio Aguero", 15),
        ("Antoine Griezmann", 15), ("Lautaro Martinez", 15), ("Victor Osimhen", 15),
        ("Rafael Leao", 15), ("Rodrygo", 15), ("Luis Diaz", 15),
        ("Son Heung-min", 15), ("Florian Wirtz", 15), ("Lamine Yamal", 15),
        ("Jamal Musiala", 15),
        ("Ousmane Dembele", 13), ("Gabriel Martinelli", 13), ("Gabriel Jesus", 13),
        ("Kai Havertz", 13), ("Cole Palmer", 13), ("Raheem Sterling", 13),
        ("Christopher Nkunku", 13), ("Diogo Jota", 13), ("Darwin Nunez", 13),
        ("Alexander Isak", 13), ("Ollie Watkins", 13), ("Marcus Rashford", 13),
        ("Rasmus Hojlund", 13), ("Viktor Gyokeres", 13), ("Rayan Cherki", 13),
        ("Desire Doue", 13), ("Nico Williams", 13), ("Michael Olise", 13),
        ("Xavi Simons", 13), ("Ademola Lookman", 13), ("Kenan Yildiz", 13),
        ("Dusan Vlahovic", 13), ("Marcus Thuram", 13), ("Ferran Torres", 13),
        ("Christian Pulisic", 13), ("Paulo Dybala", 13),
        ("Randal Kolo Muani", 10), ("Marco Asensio", 10), ("Takefusa Kubo", 10),
        ("Endrick", 10), ("Leandro Trossard", 10), ("Nicolas Jackson", 10),
        ("Mykhailo Mudryk", 10), ("Cody Gakpo", 10), ("Richarlison", 10),
        ("Dejan Kulusevski", 10), ("Anthony Gordon", 10), ("Alejandro Garnacho", 10),
        ("Victor Boniface", 10), ("Serhou Guirassy", 10), ("Jonathan David", 10),
        ("Bradley Barcola", 10), ("Mateo Retegui", 10), ("Santiago Gimenez", 10),
        ("Benjamin Sesko", 10), ("Lois Openda", 10), ("Khicha Mbeumo", 10),
        ("Nicolas Gonzalez", 10), ("Karim Adeyemi", 10), ("Ansu Fati", 10),
        ("Samuel Chukwueze", 10), ("Ciro Immobile", 10), ("Gianluca Scamacca", 10),
        ("Moise Kean", 10), ("Mehdi Taremi", 10),
        ("Eddie Nketiah", 8), ("Donyell Malen", 8), ("Jhon Duran", 8),
        ("Callum Wilson", 8), ("Noah Okafor", 8), ("Youssoufa Moukoko", 8),
        ("Lorenzo Insigne", 8), ("Andrea Belotti", 8), ("Sardar Azmoun", 8),
        ("Moussa Dembele", 8), ("Wissam Ben Yedder", 8), ("Alexandre Lacazette", 8),
        ("Jean-Philippe Mateta", 8), ("Odsonne Edouard", 8),
        ("Kevin Volland", 5), ("Antony", 5), ("Anthony Martial", 5),
    ],
}


def seed_pool(clear_existing=True):
    init_db()
    conn = get_conn()
    if clear_existing:
        cur = conn.cursor()
        cur.execute("DELETE FROM players")
        conn.commit()
        cur.close()
    conn.close()

    total = 0
    for pos, players in POOL.items():
        for name, base_m in players:
            add_player(name, pos, float(base_m))
            total += 1
    return total
