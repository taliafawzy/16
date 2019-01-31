# Smart Cooking
Jill Reijnders, Gijs van Scheijndel, Miro Schreinemakers & Talia Fawzy
## Samenvatting
Gebruikers kunnen via de website zoeken naar recepten met de specifieke ingrediënten die zij aanklikken.De website geeft in eerste instantie alleen de keuze uit verse producten (vlees, zuivel, vis, groente, fruit). Dit is gericht op het tegengaan van voedselverspilling. Als de verse ingrediënten zijn aangeklikt krijgt de gebruiker recepten terug en een lijst met ingrediënten die worden gecombineerd met het gekozen ingrediënt. De lijst aan ingrediënten die de gebruiker terugkrijgt bestaat uit zowel verse als houdbare producten. De gebruiker kan kijken welke ingrediënten hij/zij verder in huis heeft en kan op de ingrediënten in de lijst klikken om recepten terug te krijgen met de gekozen combinatie.
Het product laat gebruikers hun favoriete recepten opslaan die zij op hun persoonlijke pagina kunnen bekijken. Ze kunnen daar aangeven of ze het recept hebben geprobeerd en ze kunnen het recept eventueel weer verwijderen. Gebruikers worden getipt over andere recepten, doordat zij op de receptpagina krijgen te zien wat gebruikers die het bezochte recept hebben opgeslagen ook hebben opgeslagen.

## Video
https://drive.google.com/file/d/1cvC-eX3fBQI3QXp4G7nrhNMc-oOLOld-/view?usp=sharing

## Views
![](https://github.com/taliafawzy/16/blob/master/static/homepage.png)
### Databases
![](https://github.com/taliafawzy/16/blob/master/static/databases.PNG)

## Features
1. Gebruiker kunnen inloggen
2. Gebruikers kunnen registreren
3. Er wordt voor iedere geregistreerde gebruiker een cookbook en portfolio aangemaakt
4. Gebruikers kunnen uitloggen
5. Gebruikers kunnen uit een uitvouwmenu ingrediënten aanklikken
6. Gebruikers krijgen recepten met dit/deze ingrediënt(en) terug
7. Gebruikers krijgen (naast de recepten) ook andere ingrediënten te zien die vaak gecombineerd worden met het/de gekozen ingrediënt(en)
8. Gebruikers kunnen deze andere ingrediënten aanklikken en krijgen dan een niewue lijst van recepten terug
9. Gebruikers kunnen de gegeven recepten aanklikken
10. Gebruiker kunnen, mits ingelogd, een recept opslaan in hun cookbook
11. Gebruikers krijgen bij een aangeklikt recept te zien welke recepten ook zijn opgeslagen door gebruikers die getoonde recept ook in hun cookbook hebben
12. Gebruikers kunnen op hun profielpagina aangeven of een recept is geprobeerd
13. Gebruikers kunnen op hun profielpagina een recept uit hun cookbook verwijderen
14. Opgeslagen recepten worden met naam, link, 'tried' button of 'YES' en delete button in een tabel op de profielpagina getoond
15. Op de profielpagina wordt de gebruikersnaam van de gebruiker getoond en wordt bijgehouden hoeveel recepten zijn geprobeerd en opgeslagen

## Afhankelijkheden
### Databronnen
- **Recipe Puppy recipe finder**
http://www.recipepuppy.com/about/api/

### Externe Componenten
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

## Indeling repository
- Static: map voor afbeeldingen, javascript en CSS
- Templates: map voor alle html templates

## Taakverdeling
- Miro : API, homepage, JavaScript, algehele functionaliteit
- Jill : UX/UI, CSS, layout, algehele functionaliteit
- Gijs : CSS, html templates opzetten, UI, algehele functionaliteit
- Talia : database, helpersfuncties, JavaScript, algehele functionaliteit