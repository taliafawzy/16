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
-   Registreren  
    @app.route("/register", methods = ["GET, "POST"])  
    def register():  
    - controleert invoervakjes
    - controleert of de gebruikersnaam nog niet in gebruik is
    - controleert of het wachtwoord en de bevestiging van het wachtwoord overeenkomen
    - hasht het wachtwoord van de gebruiker
    - registreert de gebruiker in de users database
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
    - gebruiker kan recept opslaan of beoordelen door middel van een helpersfunctie
    - geeft gebruiker recepten terug die vaak zijn opgeslagen als bezochte recept ook is opgeslagen door middel van helpersfunctie          related_likes()  
    Het aangeklikte recept wordt bekeken en de gebruiker heeft ook de mogelijkheid om het recept op te slaan. Recept opslaan volgt de route van recept naar portfolio van de gebruiker. Daarnaast moet er een onderscheid worden gemaakt tussen een ingelogde en niet-ingelogde gebruiker. De gebruiker kan eventueel teruggaan naar de resultatenlijst.
-   Profielpagina bekijken  
    @app.route("/mypage", methods = ["GET", "PULL"])  
    visitMyPage():  
    - linkt gebruiker door naar profielpagina
    - toont portfolio en cookbook van gebruiker
    - gebruiker kan aangeven het recept te hebben geprobeerd en het recept beoordelen door middel van een helpersfunctie
    - gebruiker kan doorgelinkt worden naar opgeslagen recepten door op de naam van het recept te klikken  
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
    - verandert integer 'saved' met +1 in tabel portfolio in database wanneer gebruiker op  
-   def personal_rating():  
    - krijgt rating van gebruiker binnen
    - update integer 'rating' in tabel cookbook in database  
-   def common_rating():  
    - krijgt rating van gebruiker binnen
    - telt rating van gebruiker op bij 'rating' x 'people' in tabel recipe in database 
    - deelt voorgaande door 'people'+1
    - update rating op in 'rating' in tabel recipe in database
    - update 'people' in tabel recipe in database  
-   def related_likes():  
    - krijgt recept binnen wat gebruiker bezoekt
    - zoekt op in welke portfolio's dit recept voorkomt
    - maakt een set van al deze portfolio's bij elkaar met als key de recepten en als value het aantal gebruikers dat deze recepten heeft
    - sorteert deze set
    - kiest twee random recepten uit
    - geeft deze recepten weer aan gebruiker op de receptpagina

## Plugins en framwork
-   Flask framework
    (http://flask.pocoo.org/)
-   Bootstrap
-   Edamam recipe finder API
    (https://developer.edamam.com/edamam-recipe-api)
-   SQLite databases
    (https://www.sqlite.org/lang.html)
-   phpLite admin
    (https://www.phpliteadmin.org/)
-   javaScript





