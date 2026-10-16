from database import init_db, add_player, get_conn, count_players, count_by_position

# ============================================================
# Option B: 1 GK + 4 DEF + 3 MID + 3 FWD
# GK: 30, DEF: 100, MID: 80, FWD: 80 = 290 total
# ============================================================

PLAYERS = {
    "GK": [
        ("Manuel Neuer", 2.5), ("Alisson Becker", 2.5), ("Thibaut Courtois", 2.5),
        ("Ederson Moraes", 2), ("Jan Oblak", 2), ("Mike Maignan", 2),
        ("Gianluigi Donnarumma", 2.5), ("Emiliano Martinez", 2), ("Marc-Andre ter Stegen", 2),
        ("Andre Onana", 2), ("David Raya", 1.5), ("Aaron Ramsdale", 1.5),
        ("Jordan Pickford", 1.5), ("Edouard Mendy", 1.5), ("Hugo Lloris", 1.5),
        ("Keylor Navas", 1.5), ("Yann Sommer", 1.5), ("Robert Sanchez", 1.5),
        ("Gregor Kobel", 1.5), ("Diogo Costa", 1.5), ("Andriy Lunin", 1),
        ("Kepa Arrizabalaga", 1), ("Samir Handanovic", 1), ("Wojciech Szczesny", 1),
        ("Steve Mandanda", 1), ("Alex Meret", 1), ("Guglielmo Vicario", 1),
        ("Bernd Leno", 1), ("Alphonse Areola", 1), ("Dean Henderson", 1),
    ],

    "DEF": [
        ("Paolo Maldini", 4), ("Franz Beckenbauer", 3.5), ("Sergio Ramos", 3),
        ("Virgil van Dijk", 3), ("Roberto Carlos", 3), ("Cafu", 2.5),
        ("Carles Puyol", 2.5), ("Gerard Pique", 2), ("Thiago Silva", 2),
        ("Ruben Dias", 3), ("Antonio Rudiger", 2), ("Alphonso Davies", 2.5),
        ("Trent Alexander-Arnold", 3), ("Andrew Robertson", 2.5), ("Kyle Walker", 2),
        ("Jordi Alba", 2), ("Matthijs de Ligt", 2.5), ("Alessandro Bastoni", 2),
        ("Marquinhos", 2.5), ("Josko Gvardiol", 2), ("Achraf Hakimi", 2.5),
        ("Theo Hernandez", 2.5), ("David Alaba", 2), ("Milan Skriniar", 2),
        ("Kalidou Koulibaly", 2), ("Raphael Varane", 2), ("Harry Maguire", 1.5),
        ("John Stones", 2), ("William Saliba", 2.5), ("Gabriel Magalhaes", 2),
        ("Ben White", 2), ("Oleksandr Zinchenko", 1.5), ("Kieran Tierney", 1.5),
        ("Reece James", 2.5), ("Ben Chilwell", 2), ("Cesar Azpilicueta", 1.5),
        ("Wesley Fofana", 1.5), ("Levi Colwill", 1.5), ("Jules Kounde", 2.5),
        ("Ronald Araujo", 2.5), ("Andreas Christensen", 1.5), ("Eric Garcia", 1.5),
        ("Alejandro Balde", 2), ("Dani Carvajal", 1.5), ("Ferland Mendy", 1.5),
        ("Antonio Militao", 2), ("Nacho Fernandez", 1.5), ("Stefan de Vrij", 1.5),
        ("Francesco Acerbi", 1.5), ("Giovanni Di Lorenzo", 1.5), ("Kim Min-jae", 2),
        ("Matteo Darmian", 1), ("Denzel Dumfries", 1.5), ("Robin Gosens", 1),
        ("Manuel Akanji", 2), ("Nathan Ake", 1.5), ("Joao Cancelo", 2),
        ("Sergio Gomez", 1), ("Luke Shaw", 1.5), ("Lisandro Martinez", 2),
        ("Victor Lindelof", 1), ("Aaron Wan-Bissaka", 1), ("Diogo Dalot", 1.5),
        ("Tyrell Malacia", 0.5), ("Ibrahima Konate", 2), ("Joel Matip", 1.5),
        ("Joe Gomez", 1), ("Kostas Tsimikas", 0.5), ("Cristian Romero", 2),
        ("Micky van de Ven", 2), ("Destiny Udogie", 1.5), ("Emerson Royal", 1),
        ("Ben Davies", 0.5), ("Kieran Trippier", 1.5), ("Sven Botman", 1.5),
        ("Fabian Schar", 1), ("Dan Burn", 0.5), ("Max Kilman", 1),
        ("Craig Dawson", 0.5), ("Kurt Zouma", 0.5), ("Thilo Kehrer", 0.5),
        ("Emerson Palmieri", 0.5), ("Angelo Ogbonna", 0.5), ("Aaron Cresswell", 0.5),
        ("Vladimir Coufal", 0.5), ("Ben Johnson", 0.5), ("Nayef Aguerd", 1),
        ("Konstantinos Mavropanos", 0.5), ("Jean-Clair Todibo", 1),
        ("Aurelien Tchouameni", 2.5), ("Eduardo Camavinga", 2.5), ("Sergio Reguilon", 0.5),
        ("Federico Dimarco", 2), ("Davide Calabria", 1), ("Pierre Kalulu", 1.5),
        ("Malick Thiaw", 1.5), ("Fikayo Tomori", 2), ("Alessio Romagnoli", 1.5),
        ("Marc Guehi", 2), ("Jarrad Branthwaite", 2), ("Riccardo Calafiori", 2),
    ],

    "MID": [
        ("Zinedine Zidane", 5), ("Andres Iniesta", 4), ("Xavi Hernandez", 4),
        ("Kevin De Bruyne", 3.5), ("Luka Modric", 3), ("Steven Gerrard", 3),
        ("Frank Lampard", 3), ("Paul Scholes", 3), ("Andrea Pirlo", 3.5),
        ("Ronaldinho", 4), ("Kaka", 3.5), ("Rodri", 3),
        ("Jude Bellingham", 3.5), ("Pedri", 3), ("Frenkie de Jong", 3),
        ("Casemiro", 2.5), ("Ngolo Kante", 3), ("Toni Kroos", 3),
        ("Bruno Fernandes", 3), ("Martin Odegaard", 3), ("Federico Valverde", 3),
        ("Declan Rice", 2.5), ("Enzo Fernandez", 2.5), ("Moises Caicedo", 2),
        ("Alexis Mac Allister", 2.5), ("Dominik Szoboszlai", 2), ("Ryan Gravenberch", 2),
        ("Curtis Jones", 1.5), ("Harvey Elliott", 1.5), ("Thiago Alcantara", 2),
        ("Wataru Endo", 1), ("Mason Mount", 2), ("Kobbie Mainoo", 2),
        ("Christian Eriksen", 1.5), ("Scott McTominay", 1.5), ("Bruno Guimaraes", 2.5),
        ("Joelinton", 2), ("Joe Willock", 1.5), ("Sandro Tonali", 2),
        ("Ilkay Gundogan", 2), ("Bernardo Silva", 3), ("Phil Foden", 3),
        ("Matheus Nunes", 1.5), ("Kalvin Phillips", 1), ("Jack Grealish", 2.5),
        ("Jeremy Doku", 2), ("Mateo Kovacic", 2), ("Nicolo Barella", 2.5),
        ("Hakan Calhanoglu", 2), ("Henrikh Mkhitaryan", 1.5), ("Davide Frattesi", 1.5),
        ("Piotr Zielinski", 1.5), ("Stanislav Lobotka", 1.5), ("Fabian Ruiz", 2),
        ("Sergej Milinkovic-Savic", 2), ("Luis Alberto", 1.5), ("Nicolo Rovella", 1),
        ("Manuel Locatelli", 1.5), ("Adrien Rabiot", 1.5), ("Weston McKennie", 1),
        ("Federico Chiesa", 2), ("Paul Pogba", 2), ("Marco Verratti", 2),
        ("Warren Zaire-Emery", 2.5), ("Vitinha", 2), ("Lee Kang-in", 1.5),
        ("Carlos Soler", 1.5), ("Dani Ceballos", 1.5), ("Arda Guler", 1.5),
        ("Gavi", 2), ("Oriol Romeu", 1), ("Joao Felix", 2.5),
        ("Joao Palhinha", 1.5), ("Youri Tielemans", 2), ("Douglas Luiz", 2),
        ("John McGinn", 1.5), ("Boubacar Kamara", 1.5), ("Amadou Onana", 1.5),
        ("Joao Neves", 2.5), ("Nico Paz", 2), ("Khvicha Kvaratskhelia", 3),
        ("Morgan Gibbs-White", 2), ("Eberechi Eze", 2.5), ("Adam Wharton", 2),
        ("Estevao Willian", 2.5), ("Franco Mastantuono", 2),
    ],

    "FWD": [
        ("Lionel Messi", 5), ("Cristiano Ronaldo", 5), ("Kylian Mbappe", 5),
        ("Erling Haaland", 5), ("Neymar Jr", 4), ("Robert Lewandowski", 4),
        ("Karim Benzema", 3.5), ("Mohamed Salah", 4), ("Sadio Mane", 3),
        ("Vinicius Jr", 4), ("Thierry Henry", 4), ("Ronaldo Nazario", 5),
        ("Wayne Rooney", 3), ("Zlatan Ibrahimovic", 3.5), ("Luis Suarez", 3),
        ("Sergio Aguero", 3), ("Antoine Griezmann", 3), ("Harry Kane", 4),
        ("Lautaro Martinez", 3), ("Victor Osimhen", 3), ("Rafael Leao", 3),
        ("Ousmane Dembele", 2.5), ("Randal Kolo Muani", 2), ("Marco Asensio", 2),
        ("Takefusa Kubo", 2), ("Rodrygo", 3), ("Endrick", 2),
        ("Bukayo Saka", 3.5), ("Gabriel Martinelli", 2.5), ("Gabriel Jesus", 2.5),
        ("Eddie Nketiah", 1.5), ("Leandro Trossard", 2), ("Kai Havertz", 2.5),
        ("Cole Palmer", 2.5), ("Nicolas Jackson", 2), ("Raheem Sterling", 2.5),
        ("Mykhailo Mudryk", 2), ("Christopher Nkunku", 2.5), ("Diogo Jota", 2.5),
        ("Darwin Nunez", 2.5), ("Luis Diaz", 3), ("Cody Gakpo", 2),
        ("Son Heung-min", 3), ("Richarlison", 2), ("Dejan Kulusevski", 2),
        ("Alexander Isak", 2.5), ("Anthony Gordon", 2), ("Ollie Watkins", 2.5),
        ("Marcus Rashford", 2.5), ("Alejandro Garnacho", 2), ("Rasmus Hojlund", 2.5),
        ("Florian Wirtz", 3), ("Victor Boniface", 2), ("Serhou Guirassy", 2),
        ("Jonathan David", 2), ("Viktor Gyokeres", 2.5), ("Lamine Yamal", 3),
        ("Rayan Cherki", 2.5), ("Desire Doue", 2.5), ("Nico Williams", 2.5),
        ("Bradley Barcola", 2), ("Jamal Musiala", 3), ("Michael Olise", 2.5),
        ("Xavi Simons", 2.5), ("Mateo Retegui", 2), ("Ademola Lookman", 2.5),
        ("Kenan Yildiz", 2.5), ("Dusan Vlahovic", 2.5), ("Santiago Gimenez", 2),
        ("Benjamin Sesko", 2), ("Lois Openda", 2), ("Marcus Thuram", 2.5),
        ("Khicha Mbeumo", 2), ("Nicolas Gonzalez", 2), ("Karim Adeyemi", 2),
        ("Donyell Malen", 1.5), ("Jhon Duran", 1.5), ("Callum Wilson", 1.5),
    ],
}


def rebuild():
    init_db()
    conn = get_conn()
    conn.execute("DELETE FROM players")
    conn.commit()
    conn.close()

    total = 0
    for pos, lst in PLAYERS.items():
        for name, base in lst:
            add_player(name, pos, base)
            total += 1

    print(f"✅ Rebuilt pool: {total} players")
    print(f"   Breakdown: {count_by_position()}")


if __name__ == "__main__":
    rebuild()
