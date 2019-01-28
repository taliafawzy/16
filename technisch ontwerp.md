# Technisch ontwerp
## Controllers
-   Inloggen
    @app.route("/login", methods = ["GET", "POST"])
    def login():
    - controleert invoervakjes
    - controleert username
    - controleert wachtwoord
    - logt gebruiker in
    - zorgt ervoor dat gebruiker ingelogd blijft totdat hij/zij uitlogt
    - redirect naar de homepage
    Als de gebruiker zich inlogt komt hij weer op de homepagina terecht met aangepaste functies
    om uit te loggen en naar de eigen pagina te gaan. Er zijn verschillende routes naar de
    inlogpagina: vanaf de homepagina, de resultatenlijst en de receptpagina.
-   Uitloggen
    @app.route("/logout", methods = ["POST"])
    def logout():
    - zorgt ervoor dat gebruiker niet meer wordt onthouden = logt gebruiker uit
    - redirect naar de hompage
    Als de gebruiker zich inlogt komt hij weer op de homepagina terecht met aangepaste functies om uit te loggen en naar de eigen pagina te gaan. Er zijn verschillende routes naar de inlogpagina: vanaf de homepagina, de resultatenlijst en de receptpagina.
-   Checken van invoervakjes registreerpagina
    @app.route("/checkname", methods = ["GET"])
    def checkname():
    - krijgt een JSON request binnen via register.js
    - haalt de resultaten op van het 'username' invoervak op de registreerpagina
    - controleert de userdata database of er de username al in gebruik is of niet
    - als de username in gebruik is, stuurt de functie de line 'username already exists' terug naar register.js welke het toont op register.html
    - als de username niet in gebruik is, stuurt de functie de line 'username does not exist yet' terug naar register.js welke het toont op register.html
-   Registreren
    @app.route("/register", methods = ["GET, "POST"])
    def register():
    - controleert of de gebruikersnaam nog niet in gebruik is
    - hasht het wachtwoord van de gebruiker
    - registreert de gebruiker in de userdata database
    - maakt portfolio aan voor de gebruiker
    - maakt cookbook aan voor de gebruiker
    - logt gebruiker in
    - zorgt ervoor dat gebruiker ingelogd blijft totdat hij/zij uitlogt
    - redirect naar de homepage
    Als de gebruiker nog geen account heeft zal hij/zij zich eerst moeten registreren als er gebruik wilt worden gemaakt van bepaalde functies. De registreerknop is te zien vanaf de homepagina, de resultatenlijst en de receptpagina. Er zijn dus verschillende routes naar de pagina waar de gebruiker zich kan registreren. Als de gebruiker zich succesvol registreert wordt hij/zij naar de homepagina verwezen. Op het moment dat een gebruiker zich registreert, wordt hij/zij opgeslagen in het gebruikersbestand en worden er in de back-end een portfolio en cookbook voor deze gebruiker aangemaakt waarin opgeslagen recepten worden geregistreerd.
-   Recept opzoeken
    @app.route("/homepage", methods = ["GET", "POST"])
    def searchRecipe():
    - registreert keuze van gebruiker
    - roept getResults() helpersfunctie op om naar recepten met dit ingrediënt/deze ingrediënten te zoeken
    - geeft lijst van recepten terug aan gebruiker op een andere HTML pagina
    - geeft gebruiker opties om te kiezen uit andere ingrediënten die vaak worden gebruikt in combinatie met ingrediënt(en) naar keuze
    - als gebruiker hieruit dan iets kiest, wordt de getResults() functie weer opgeroepen
    Deze functie roept de getResults() helpersfunctie op, op het moment dat de gebruiker een ingrediënt aanklikt.
-   Recept bekijken
    @app.route("/recipe", methods = ["GET", "POST"])
    def visitRecipe():
    - registreert verzoek van gebruiker
    - linkt gebruiker door naar receptpagina
    - gebruiker kan recept opslaan door middel van een helpersfunctie
    - geeft gebruiker recepten terug die vaak zijn opgeslagen als bezochte recept ook is opgeslagen door middel van helpersfunctie related_likes()
    Het aangeklikte recept wordt bekeken en de gebruiker heeft ook de mogelijkheid om het recept op te slaan. Recept opslaan volgt de route van recept naar portfolio van de gebruiker. Daarnaast moet er een onderscheid worden gemaakt tussen een ingelogde en niet-ingelogde gebruiker. De gebruiker kan eventueel teruggaan naar de resultatenlijst.
-   Profielpagina bekijken
    @app.route("/mypage", methods = ["GET", "PULL"])
    visitMyPage():
    - linkt gebruiker door naar profielpagina
    - toont portfolio en cookbook van gebruiker
    - gebruiker kan aangeven het recept te hebben geprobeerd en het recept verwijderen door middel van een helpersfunctie
    - gebruiker kan doorgelinkt worden naar opgeslagen recepten door op de url van het recept te klikken
    De gebruiker kan via de homepagina, resultatenlijst en receptpagina doorklikken naar zijn/haar eigen persoonlijke pagina. Dit kan alleen wanneer er is ingelogd.

## Views
Schetsen van website in powerpoint. De volgende pagina's zijn nodig:
-   homepage.html
-   login.html
-   register.html
-   results.html
-   recipe.html
-   mypage.html
### Databases
![](https://github.com/taliafawzy/16/blob/master/databases.PNG)

## Models/helpers
-   def apology():
    - stuurt bericht naar de gebruiker met daarin wat er precies mis is gegaan
    Het geeft aan wanneer er een excuus naar de gebruiker moet worden gestuurd als er iets mis gaat. Bijvoorbeeld door het niet of verkeerd invullen van een veld.
-   def login_required():
    - zorgt ervoor dat gebruikers die niet zijn ingelogd niet zomaar in een 'mypage' omgeving terecht kunnen komen
    - herleidt gebruikers dan naar de login pagina
-   def getResults():
    - zoekt in database naar recepten met ingevoerde ingrediënt(en)
    - geeft resultatenlijst terug op basis van ingevoerde ingrediënt(en)
    - geeft gebruiker opties om te kiezen uit andere ingrediënten die vaak worden gebruikt in combinatie met ingrediënt(en) naar keuze
    Functie die recepten zoekt naar aanleiding van de aangevinkte trefwoorden. Deze functie geeft ingrediënten terug waar de gebruiker uit kan kiezen.
-   def tried_recipe():
    - verandert integer 'tried' met +1 in tabel portfolio in database wanneer gebruiker op de 'Tried' button drukt
    - verandert boolean 'tried' van False naar True in tabel cookbook in database wanneer gebruiker op de 'Tried' button drukt
    Wordt aangeroepen wanneer gebruiker aangeeft het recept te hebben geprobeerd.
-   def save_recipe()
    - slaat recept op in tabel cookbook in database wanneer gebruiker op de 'save recipe' button drukt
    - verandert integer 'saved' met +1 in tabel portfolio in database wanneer gebruiker op de 'save recipe' button drukt
-   def delete_recipe():
    - verwijdert recept uit tabel cookbook in database wanneer gebruiker op de 'delete recipe' button drukt
    - verandert integer 'saved' met -1 in tabel portfolio in database wanneer gebruiker op de 'delete recipe' button drukt
-   def related_recipes():
    - krijgt recept binnen wat gebruiker bezoekt
    - zoekt op in welke portfolio's dit recept voorkomt
    - maakt een set van al deze portfolio's bij elkaar met als key de recepten en als value het aantal gebruikers dat deze recepten heeft
    - sorteert deze set
    - kiest twee random recepten uit indien mogelijk. Anders wordt er maar één recept getoond of helemaal geen recepten.
    - geeft deze recepten weer aan gebruiker op de receptpagina
-   def checklist()
    - leest de ingredientslist csv in en zorgt ervoor dat ingrediënten worden onderverdeeld in bepaalde categorieën

## Plugins en framwork
- **Bootstrap**
https://getbootstrap.com/
- **phpLiteAdmin**
https://www.phpliteadmin.org/
- **Flask**
http://flask.pocoo.org/
- **SQLite Databases**
https://www.sqlite.org/index.html
- **jQuery**
https://jquery.com/
- **Recipe Puppy recipe finder**
http://www.recipepuppy.com/about/api/
- **JavaScript**
https://www.javascript.com/





