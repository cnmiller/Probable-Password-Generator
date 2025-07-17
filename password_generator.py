import random
import argparse
import sys
import re
from typing import Dict, List, Set
from datetime import datetime, timedelta

COMMON_PASSWORDS: List[str] = [
    'password', '123456', 'qwerty', 'abc123', 'iloveyou',
    'admin', 'welcome', 'monkey', 'football', 'baseball'
]

TECH_DEFAULTS: List[str] = [
    'Password1', 'Welcome1', 'Letmein', 'P@ssw0rd', 'Passw0rd',
    'Admin123', 'User123', 'Guest123', 'Test123', 'Demo123',
    'Manager1', 'Super123', 'Root123', 'Login123', 'Access123',
    'Temp123', 'Default1', 'System1', 'Service1', 'Security1'
]

SYMBOLS: List[str] = ['!', '@', '#', '$', '%', '^', '&', '*']  # Ordered by real-world frequency

def get_current_years() -> List[str]:
    """Get current and previous year in both full and short format."""
    current_year = datetime.now().year
    previous_year = current_year - 1
    
    return [
        str(current_year),      # 2025
        str(previous_year),     # 2024  
        str(current_year)[2:],  # 25
        str(previous_year)[2:]  # 24
    ]

def get_valid_months(expiration_days: int = None) -> List[str]:
    """Get months that would be valid based on password expiration policy."""
    all_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December',
        'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    
    if expiration_days is None:
        return all_months
    
    # Calculate how far back we should go based on expiration
    current_date = datetime.now()
    expiration_date = current_date - timedelta(days=expiration_days)
    
    valid_months = set()
    
    # Get all months from expiration date to current date
    temp_date = expiration_date.replace(day=1)  # Start of month
    while temp_date <= current_date:
        month_name = temp_date.strftime('%B')  # Full name
        month_abbr = temp_date.strftime('%b')  # Abbreviated
        
        valid_months.add(month_name)
        valid_months.add(month_abbr)
        
        # Move to next month
        if temp_date.month == 12:
            temp_date = temp_date.replace(year=temp_date.year + 1, month=1)
        else:
            temp_date = temp_date.replace(month=temp_date.month + 1)
    
    # Return in order, filtering the full list to maintain order
    return [month for month in all_months if month in valid_months]

SEASONS: List[str] = [
    'Spring', 'Summer', 'Fall', 'Autumn', 'Winter'
]

MONTHS: List[str] = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
    'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

KEYBOARD_WALKS: List[str] = [
    'qwerty', 'asdf', 'zxcv', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
    '1234567890', '!@#$%^&*()', 'qwe123', 'asd123', 'zxc123',
    'qwer1234', 'asdf1234', '123qwe', '123asd', '1qaz2wsx',
    'qazwsx', 'wsxedc', 'rfvtgb', 'yhnujm', 'plokijuh'
]

PRO_TEAMS: Dict[str, List[str]] = {
    "new york": ["Giants", "Jets", "Yankees", "Mets", "Knicks", "Nets", "Rangers", "Islanders", "RedBulls", "CityFC", "Liberty"],
    "los angeles": ["Rams", "Chargers", "Dodgers", "Angels", "Lakers", "Clippers", "Kings", "Ducks", "Galaxy", "LAFC", "Sparks"],
    "chicago": ["Bears", "Cubs", "WhiteSox", "Bulls", "Blackhawks", "Fire", "Sky"],
    "houston": ["Texans", "Astros", "Rockets", "Dynamo", "Dash"],
    "phoenix": ["Cardinals", "Diamondbacks", "Suns", "Coyotes", "Rising", "Mercury"],
    "philadelphia": ["Eagles", "Phillies", "76ers", "Flyers", "Union"],
    "san antonio": ["Spurs"],
    "san diego": ["Padres", "Wave", "Loyal"],
    "dallas": ["Cowboys", "Rangers", "Mavericks", "Stars", "FCDallas", "Wings"],
    "san jose": ["Sharks", "Earthquakes"],
    "austin": ["AustinFC"],
    "jacksonville": ["Jaguars"],
    "san francisco": ["49ers", "Giants", "Warriors"],
    "columbus": ["BlueJackets", "Crew"],
    "indianapolis": ["Colts", "Pacers", "Fever"],
    "fort worth": ["Cowboys", "Rangers", "Mavericks", "Stars"],
    "charlotte": ["Panthers", "Hornets", "CharlotteFC"],
    "seattle": ["Seahawks", "Mariners", "Kraken", "Sounders", "Storm"],
    "denver": ["Broncos", "Rockies", "Nuggets", "Avalanche", "Rapids"],
    "washington": ["Commanders", "Nationals", "Wizards", "Capitals", "DCUnited", "Mystics"],
    "boston": ["Patriots", "RedSox", "Celtics", "Bruins", "Revolution"],
    "detroit": ["Lions", "Tigers", "Pistons", "RedWings", "CityFC"],
    "nashville": ["Titans", "Predators", "NashvilleSC"],
    "memphis": ["Grizzlies", "901FC"],
    "portland": ["TrailBlazers", "Timbers", "Thorns"],
    "oklahoma city": ["Thunder"],
    "las vegas": ["Raiders", "GoldenKnights", "Aces", "Lights"],
    "baltimore": ["Ravens", "Orioles"],
    "milwaukee": ["Bucks", "Brewers"],
    "atlanta": ["Falcons", "Braves", "Hawks", "United", "Dream"],
    "minneapolis": ["Vikings", "Twins", "Timberwolves", "Wild", "United", "Lynx"],
    "miami": ["Dolphins", "Marlins", "Heat", "Panthers", "InterMiami"],
    "tampa": ["Buccaneers", "Lightning", "Rays", "Rowdies"],
    "orlando": ["Magic", "City", "Pride"],
    "kansas city": ["Chiefs", "Royals", "Sporting"],
    "st. louis": ["Cardinals", "Blues", "CitySC"],
    "cincinnati": ["Bengals", "Reds", "FCCincinnati"],
    "cleveland": ["Browns", "Guardians", "Cavaliers"],
    "pittsburgh": ["Steelers", "Pirates", "Penguins", "Riverhounds"],
    "buffalo": ["Bills", "Sabres"],
    "sacramento": ["Kings", "Republic"],
    "raleigh": ["Hurricanes", "NCCourage"],
    "salt lake city": ["Jazz", "RealSaltLake"],
    "new orleans": ["Saints", "Pelicans"],
    "green bay": ["Packers"],
    "tampa bay": ["Buccaneers", "Lightning", "Rays", "Rowdies"],
    "st petersburg": ["Rays", "Rowdies"],
    "arlington": ["Cowboys", "Rangers"],
    "anaheim": ["Ducks", "Angels"],
    "oakland": ["Athletics"],
    "san bernardino": ["Quakes"],
    "fresno": ["FC"],
    "bakersfield": ["Condors"],
    "stockton": ["Heat"],
    "modesto": ["Nuts"],
    "santa clara": ["49ers"],
    "fremont": ["Aces"],
    "richmond": ["Kickers"],
    "norfolk": ["Tides", "Admirals"],
    "virginia beach": ["CityFC"],
    "chesapeake": ["Bayhawks"],
    "newport news": ["Shipbuilders"],
    "louisville": ["CityFC"],
    "lexington": ["Legends"],
    "birmingham": ["Legion"],
    "huntsville": ["Havoc"],
    "mobile": ["BayBears"],
    "montgomery": ["Biscuits"],
    "little rock": ["Rangers"],
    "jackson": ["Generals"],
    "shreveport": ["Mudbugs"],
    "baton rouge": ["Zydeco"],
    "lafayette": ["Drillers"],
    "lake charles": ["IcePirates"],
    "el paso": ["Locomotive", "Chihuahuas"],
    "lubbock": ["CottonKings"],
    "amarillo": ["Bulls"],
    "corpus christi": ["Hooks"],
    "beaumont": ["Drillers"],
    "mcallen": ["Thunder"],
    "brownsville": ["Charros"],
    "laredo": ["Heat"],
    "waco": ["Wizards"],
    "tyler": ["Wildcatters"],
    "abilene": ["PrairieDogs"],
    "midland": ["RockHounds"],
    "odessa": ["Jackalopes"],
    "tucson": ["Roadrunners", "SugarSkulls"],
    "mesa": ["SolarSox"],
    "chandler": ["Compadres"],
    "glendale": ["DesertDogs"],
    "scottsdale": ["Scorpions"],
    "tempe": ["Diablo"],
    "peoria": ["Javelinas"],
    "surprise": ["Saguaros"],
    "albuquerque": ["Isotopes"],
    "las cruces": ["Vaqueros"],
    "roswell": ["Invaders"],
    "santa fe": ["Fuego"],
    "colorado springs": ["Switchbacks"],
    "fort collins": ["Eagles"],
    "pueblo": ["Bulls"],
    "grand junction": ["Rockies"],
    "boise": ["Hawks"],
    "spokane": ["Chiefs"],
    "tacoma": ["Rainiers"],
    "vancouver": ["Canadians"],
    "eugene": ["Emeralds"],
    "salem": ["Volcanoes"],
    "bend": ["Elks"],
    "medford": ["Rogues"],
    "tri cities": ["Americans"],
    "yakima": ["Bears"],
    "wenatchee": ["AppleSox"],
    "everett": ["AquaSox"],
    "bellingham": ["Bells"]
}

FBS_MASCOTS: Dict[str, List[str]] = {
    "new york": ["Syracuse", "Orange", "ArmyWestPoint", "BlackKnights", "StJohns", "RedStorm", "NYU", "Violets", "Columbia", "Lions", "Fordham", "Rams"],
    "los angeles": ["USC", "Trojans", "UCLA", "Bruins", "Pepperdine", "Waves", "LoyolaMarymount", "Lions", "CalStateNorthridge", "Matadors"],
    "chicago": ["Illinois", "FightingIllini", "Northwestern", "Wildcats", "Chicago", "Maroons", "DePaul", "BlueDemons", "Loyola", "Ramblers"],
    "houston": ["Houston", "Cougars", "Rice", "Owls", "TexasAM", "Aggies", "PrairieViewAM", "Panthers", "TexasSouthern", "Tigers"],
    "phoenix": ["ArizonaState", "SunDevils", "Arizona", "Wildcats", "NorthernArizona", "Lumberjacks", "GrandCanyon", "Antelopes"],
    "philadelphia": ["Temple", "Owls", "PennState", "NittanyLions", "Penn", "Quakers", "LaSalle", "Explorers", "Drexel", "Dragons", "Villanova", "Wildcats"],
    "san antonio": ["UTSA", "Roadrunners", "StMarys", "Rattlers", "Trinity", "Tigers", "Incarnate", "Cardinals"],
    "san diego": ["SanDiegoState", "Aztecs", "SanDiego", "Toreros", "UCSD", "Tritons", "PointLoma", "SeaLions"],
    "dallas": ["SMU", "Mustangs", "TCU", "HornedFrogs", "NorthTexas", "MeanGreen", "TexasAM", "Aggies", "Baylor", "Bears", "Texas", "Longhorns"],
    "san jose": ["SanJoseState", "Spartans", "SantaClara", "Broncos", "Stanford", "Cardinal", "Berkeley", "Bears"],
    "austin": ["Texas", "Longhorns", "TexasState", "Bobcats", "StEdwards", "Hilltoppers"],
    "jacksonville": ["Florida", "Gators", "Jacksonville", "Dolphins", "FloridaState", "Seminoles", "Miami", "Hurricanes"],
    "san francisco": ["Berkeley", "GoldenBears", "Stanford", "Cardinal", "SanFrancisco", "Dons", "SaintMarys", "Gaels"],
    "columbus": ["OhioState", "Buckeyes", "Ohio", "Bobcats", "BowlingGreen", "Falcons", "Cincinnati", "Bearcats"],
    "indianapolis": ["Indiana", "Hoosiers", "Purdue", "Boilermakers", "Butler", "Bulldogs", "BallState", "Cardinals", "NotreDame", "FightingIrish"],
    "charlotte": ["Charlotte", "49ers", "WakeForest", "DemonDeacons", "NorthCarolinaState", "Wolfpack", "Duke", "BlueDevils", "NorthCarolina", "TarHeels"],
    "seattle": ["Washington", "Huskies", "WashingtonState", "Cougars", "SeattleU", "Redhawks", "Gonzaga", "Bulldogs"],
    "denver": ["Colorado", "Buffaloes", "AirForce", "Falcons", "Denver", "Pioneers", "ColoradoState", "Rams", "NorthernColorado", "Bears"],
    "washington": ["Maryland", "Terrapins", "Georgetown", "Hoyas", "GeorgeWashington", "Colonials", "AmericanU", "Eagles", "Navy", "Midshipmen"],
    "boston": ["BostonCollege", "Eagles", "Harvard", "Crimson", "BostonU", "Terriers", "Northeastern", "Huskies", "MIT", "Engineers"],
    "detroit": ["Michigan", "Wolverines", "MichiganState", "Spartans", "Detroit", "Titans", "WesternMichigan", "Broncos", "CentralMichigan", "Chippewas"],
    "nashville": ["Vanderbilt", "Commodores", "Tennessee", "Volunteers", "MiddleTennessee", "BlueRaiders", "Belmont", "Bruins"],
    "memphis": ["Memphis", "Tigers", "Mississippi", "Rebels", "MississippiState", "Bulldogs"],
    "portland": ["Oregon", "Ducks", "OregonState", "Beavers", "Portland", "Pilots", "PortlandState", "Vikings"],
    "oklahoma city": ["Oklahoma", "Sooners", "OklahomaState", "Cowboys", "Tulsa", "GoldenHurricane", "OralRoberts", "GoldenEagles"],
    "las vegas": ["UNLV", "Rebels", "Nevada", "WolfPack", "CalPoly", "Mustangs"],
    "baltimore": ["Maryland", "Terrapins", "Navy", "Midshipmen", "Towson", "Tigers", "UMBC", "Retrievers"],
    "milwaukee": ["Wisconsin", "Badgers", "Marquette", "GoldenEagles", "UWMilwaukee", "Panthers"],
    "atlanta": ["GeorgiaTech", "YellowJackets", "Georgia", "Bulldogs", "GeorgiaState", "Panthers", "Emory", "Eagles", "GeorgiaSouthern", "Eagles"],
    "minneapolis": ["Minnesota", "GoldenGophers", "StThomas", "Tommies", "Macalester", "Scots"],
    "miami": ["Miami", "Hurricanes", "FloridaInternational", "Panthers", "Florida", "Gators", "FloridaState", "Seminoles", "NovaU", "Sharks"],
    "tampa": ["SouthFlorida", "Bulls", "Florida", "Gators", "FloridaState", "Seminoles", "Stetson", "Hatters"],
    "orlando": ["CentralFlorida", "Knights", "Rollins", "Tars", "Florida", "Gators"],
    "kansas city": ["Kansas", "Jayhawks", "Missouri", "Tigers", "KansasState", "Wildcats", "Wichita", "Shockers"],
    "st. louis": ["SaintLouis", "Billikens", "Missouri", "Tigers", "WashingtonU", "Bears", "SaintLouisU", "Billikens"],
    "cincinnati": ["Cincinnati", "Bearcats", "Xavier", "Musketeers", "Miami", "RedHawks", "Dayton", "Flyers"],
    "cleveland": ["ClevelandState", "Vikings", "CaseWestern", "Spartans", "BaldwinWallace", "YellowJackets", "OhioState", "Buckeyes"],
    "pittsburgh": ["Pittsburgh", "Panthers", "PennState", "NittanyLions", "Carnegie", "Tartans", "Duquesne", "Dukes", "WestVirginia", "Mountaineers"],
    "buffalo": ["Buffalo", "Bulls", "Canisius", "GoldenGriffins", "Niagara", "PurpleEagles", "StBonaventure", "Bonnies"],
    "sacramento": ["SacramentoState", "Hornets", "UCDavis", "Aggies", "CalPoly", "Mustangs"],
    "raleigh": ["NorthCarolinaState", "Wolfpack", "NorthCarolina", "TarHeels", "Duke", "BlueDevils", "WakeForest", "DemonDeacons"],
    "salt lake city": ["Utah", "Utes", "UtahState", "Aggies", "BrighamYoung", "Cougars", "Weber", "Wildcats"],
    "new orleans": ["Tulane", "GreenWave", "NewOrleans", "Privateers", "Xavier", "GoldRush", "Dillard", "BleuDevils"],
    "green bay": ["Wisconsin", "Badgers", "WisconsinGreenBay", "Phoenix", "Marquette", "GoldenEagles"],
    "arlington": ["TexasArlington", "Mavericks", "TCU", "HornedFrogs", "SMU", "Mustangs", "Texas", "Longhorns"],
    "anaheim": ["CalStateFullerton", "Titans", "Chapman", "Panthers", "UCI", "Anteaters"],
    "fresno": ["CalStateFresno", "Bulldogs", "Fresno", "Rams"],
    "bakersfield": ["CalStateBakersfield", "Roadrunners"],
    "stockton": ["Pacific", "Tigers", "CalStateStanislaus", "Warriors"],
    "modesto": ["CalStateStanislaus", "Warriors", "ModestoJC", "Pirates"],
    "richmond": ["VirginiaCommonwealth", "Rams", "Richmond", "Spiders", "Virginia", "Cavaliers", "VirginiaTech", "Hokies"],
    "norfolk": ["OldDominion", "Monarchs", "Norfolk", "Spartans", "Hampton", "Pirates"],
    "virginia beach": ["OldDominion", "Monarchs", "Virginia", "Cavaliers", "VirginiaTech", "Hokies"],
    "louisville": ["Louisville", "Cardinals", "Kentucky", "Wildcats", "Western", "Hilltoppers"],
    "lexington": ["Kentucky", "Wildcats", "Louisville", "Cardinals", "EasternKentucky", "Colonels"],
    "birmingham": ["UAB", "Blazers", "Samford", "Bulldogs", "Alabama", "CrimsonTide", "Auburn", "Tigers"],
    "huntsville": ["AlabamaHuntsville", "Chargers", "Alabama", "CrimsonTide", "AuburnMontgomery", "Senators"],
    "mobile": ["SouthAlabama", "Jaguars", "Alabama", "CrimsonTide", "Auburn", "Tigers"],
    "montgomery": ["AlabamaState", "Hornets", "Auburn", "Tigers", "TroyU", "Trojans"],
    "little rock": ["ArkansasLittleRock", "Trojans", "Arkansas", "Razorbacks", "ArkansasState", "RedWolves"],
    "jackson": ["JacksonState", "Tigers", "Mississippi", "Rebels", "MississippiState", "Bulldogs", "Southern", "Jaguars"],
    "shreveport": ["LouisianaTech", "Bulldogs", "Centenary", "Gentlemen", "LSU", "Tigers"],
    "baton rouge": ["LSU", "Tigers", "SouthernU", "Jaguars"],
    "lafayette": ["LouisianaLafayette", "RaginCajuns", "LSU", "Tigers"],
    "el paso": ["UTEP", "Miners", "NewMexicoState", "Aggies"],
    "lubbock": ["TexasTech", "RedRaiders", "LubbockChristian", "Chaparrals"],
    "amarillo": ["WestTexasAM", "Buffs", "TexasTech", "RedRaiders"],
    "corpus christi": ["TexasAMCorpusChristi", "Islanders", "TexasAM", "Aggies"],
    "waco": ["Baylor", "Bears", "TexasState", "Bobcats"],
    "tyler": ["TexasCollege", "Steers", "LeTourneau", "YellowJackets"],
    "abilene": ["AbilenChristian", "Wildcats", "HardinSimmons", "Cowboys"],
    "midland": ["TexasPermian", "Panthers", "TexasTech", "RedRaiders"],
    "tucson": ["Arizona", "Wildcats", "ArizonaState", "SunDevils"],
    "mesa": ["ArizonaState", "SunDevils", "Arizona", "Wildcats"],
    "tempe": ["ArizonaState", "SunDevils", "Arizona", "Wildcats"],
    "albuquerque": ["NewMexico", "Lobos", "NewMexicoState", "Aggies"],
    "las cruces": ["NewMexicoState", "Aggies", "NewMexico", "Lobos"],
    "santa fe": ["NewMexicoHighlands", "Cowboys", "StJohns", "Johnnies"],
    "colorado springs": ["AirForce", "Falcons", "Colorado", "Buffaloes", "ColoradoCollege", "Tigers"],
    "fort collins": ["ColoradoState", "Rams", "Colorado", "Buffaloes"],
    "pueblo": ["ColoradoStatePueblo", "ThunderWolves", "Colorado", "Buffaloes"],
    "boise": ["BoiseState", "Broncos", "Idaho", "Vandals"],
    "spokane": ["Gonzaga", "Bulldogs", "EasternWashington", "Eagles", "Whitworth", "Pirates"],
    "tacoma": ["PugetSound", "Loggers", "Washington", "Huskies"],
    "eugene": ["Oregon", "Ducks", "OregonState", "Beavers"],
    "salem": ["Willamette", "Bearcats", "Oregon", "Ducks"],
    "bend": ["CentralOregon", "Bobcats", "Oregon", "Ducks"],
    "tri cities": ["WashingtonState", "Cougars", "Washington", "Huskies"],
    "yakima": ["CentralWashington", "Wildcats", "Washington", "Huskies"],
    "bellingham": ["WesternWashington", "Vikings", "Washington", "Huskies"],
    "fort worth": ["TCU", "HornedFrogs", "TexasWesleyan", "Rams"],
    "san bernardino": ["CalStateSanBernardino", "Coyotes", "UCRiverside", "Highlanders"],
    "santa clara": ["SantaClara", "Broncos", "Stanford", "Cardinal", "SanJoseState", "Spartans"],
    "fremont": ["OhloneCollege", "Renegades", "Berkeley", "Bears"],
    "chesapeake": ["OldDominion", "Monarchs", "Norfolk", "Spartans"],
    "newport news": ["ChristopherNewport", "Captains", "OldDominion", "Monarchs"],
    "tulsa": ["Tulsa", "GoldenHurricane", "Oklahoma", "Sooners", "OklahomaState", "Cowboys"],
    "omaha": ["Nebraska", "Cornhuskers", "Creighton", "Bluejays"],
    "wichita": ["WichitaState", "Shockers", "Kansas", "Jayhawks"],
    "des moines": ["Drake", "Bulldogs", "Iowa", "Hawkeyes", "IowaState", "Cyclones"],
    "cedar falls": ["NorthernIowa", "Panthers", "Iowa", "Hawkeyes"],
    "ames": ["IowaState", "Cyclones", "Iowa", "Hawkeyes"],
    "iowa city": ["Iowa", "Hawkeyes", "IowaState", "Cyclones"],
    "madison": ["Wisconsin", "Badgers", "Marquette", "GoldenEagles"],
    "ann arbor": ["Michigan", "Wolverines", "MichiganState", "Spartans"],
    "east lansing": ["MichiganState", "Spartans", "Michigan", "Wolverines"],
    "champaign": ["Illinois", "FightingIllini", "Northwestern", "Wildcats"],
    "evanston": ["Northwestern", "Wildcats", "Illinois", "FightingIllini"],
    "west lafayette": ["Purdue", "Boilermakers", "Indiana", "Hoosiers"],
    "bloomington": ["Indiana", "Hoosiers", "Purdue", "Boilermakers"],
    "lincoln": ["Nebraska", "Cornhuskers", "Creighton", "Bluejays"],
    "norman": ["Oklahoma", "Sooners", "OklahomaState", "Cowboys"],
    "stillwater": ["OklahomaState", "Cowboys", "Oklahoma", "Sooners"],
    "manhattan": ["KansasState", "Wildcats", "Kansas", "Jayhawks"],
    "lawrence": ["Kansas", "Jayhawks", "KansasState", "Wildcats"],
    "columbia": ["Missouri", "Tigers", "Kansas", "Jayhawks"],
    "fayetteville": ["Arkansas", "Razorbacks", "ArkansasState", "RedWolves"],
    "knoxville": ["Tennessee", "Volunteers", "Vanderbilt", "Commodores"],
    "clemson": ["Clemson", "Tigers", "SouthCarolina", "Gamecocks"],
    "athens": ["Georgia", "Bulldogs", "GeorgiaTech", "YellowJackets"],
    "gainesville": ["Florida", "Gators", "FloridaState", "Seminoles"],
    "tallahassee": ["FloridaState", "Seminoles", "Florida", "Gators"],
    "coral gables": ["Miami", "Hurricanes", "Florida", "Gators"],
    "blacksburg": ["VirginiaTech", "Hokies", "Virginia", "Cavaliers"],
    "charlottesville": ["Virginia", "Cavaliers", "VirginiaTech", "Hokies"],
    "chapel hill": ["NorthCarolina", "TarHeels", "NorthCarolinaState", "Wolfpack"],
    "durham": ["Duke", "BlueDevils", "NorthCarolina", "TarHeels"],
    "winston salem": ["WakeForest", "DemonDeacons", "NorthCarolina", "TarHeels"],
    "college station": ["TexasAM", "Aggies", "Texas", "Longhorns"],
    "tuscaloosa": ["Alabama", "CrimsonTide", "Auburn", "Tigers"],
    "auburn": ["Auburn", "Tigers", "Alabama", "CrimsonTide"],
    "starkville": ["MississippiState", "Bulldogs", "Mississippi", "Rebels"],
    "oxford": ["Mississippi", "Rebels", "MississippiState", "Bulldogs"],
    "college park": ["Maryland", "Terrapins", "Georgetown", "Hoyas"],
    "university park": ["PennState", "NittanyLions", "Pittsburgh", "Panthers"],
    "piscataway": ["Rutgers", "ScarletKnights", "Princeton", "Tigers"]
}

def leetspeak_level1(word: str) -> str:
    """Basic leetspeak: simple number substitutions."""
    if not word or not isinstance(word, str):
        return ""
    
    replacements: Dict[str, str] = {'a':'4', 'e':'3', 'i':'1', 'o':'0', 's':'5', 't':'7'}
    return ''.join(replacements.get(c.lower(), c) for c in word)

def leetspeak_level2(word: str) -> str:
    """Advanced leetspeak: more substitutions including symbols."""
    if not word or not isinstance(word, str):
        return ""
    
    replacements: Dict[str, str] = {
        'a':'@', 'e':'3', 'i':'!', 'o':'0', 's':'$', 't':'7',
        'l':'1', 'g':'9', 'b':'6', 'z':'2'
    }
    return ''.join(replacements.get(c.lower(), c) for c in word)

def leetspeak_level3(word: str) -> str:
    """Maximum leetspeak: combines level 1 and 2 with additional patterns."""
    if not word or not isinstance(word, str):
        return ""
    
    replacements: Dict[str, str] = {
        'a':'@', 'e':'3', 'i':'!', 'o':'0', 's':'$', 't':'7',
        'l':'1', 'g':'9', 'b':'6', 'z':'2', 'c':'(', 'h':'#'
    }
    result = ''.join(replacements.get(c.lower(), c) for c in word)
    # Additional transformations
    result = result.replace('ck', 'x').replace('ph', 'f')
    return result

def generate_variations(base_words: List[str], symbols_count: int = 5, expiration_days: int = None) -> Set[str]:
    """Generate password variations from base words using individual transformations only."""
    if not base_words:
        return set()
    
    # Use only the most common symbols based on user preference
    active_symbols = SYMBOLS[:symbols_count]
    # Get dynamic years
    current_years = get_current_years()
    
    variations: Set[str] = set()
    
    for word in base_words:
        if not word or not isinstance(word, str):
            continue
            
        word_lower: str = word.lower()
        word_cap: str = word.capitalize()
        word_upper: str = word.upper()
        
        # Basic variations
        base_variations = [word_lower, word_cap, word_upper]
        
        # Leetspeak variations
        leet1 = leetspeak_level1(word_lower)
        leet2 = leetspeak_level2(word_lower)
        leet3 = leetspeak_level3(word_lower)
        
        # All word forms to process
        all_forms = base_variations + [leet1, leet2, leet3]
        
        for form in all_forms:
            if not form:
                continue
                
            # Basic patterns: word + suffix + symbol
            for suffix in ['', '123', '1', '01', '1234', '12345'] + current_years:
                for symbol in active_symbols + ['']:
                    try:
                        variations.add(form + suffix + symbol)
                        if suffix:  # Avoid empty middle parts
                            variations.add(form + symbol + suffix)
                    except (TypeError, AttributeError):
                        continue
    
    return variations

def calculate_password_score(password: str, word_type: str, expiration_days: int = None) -> float:
    """Calculate likelihood score for a password based on real-world usage patterns."""
    score = 0.0
    
    # Get dynamic years for scoring
    current_years = get_current_years()
    current_year_full = current_years[0]  # e.g., "2025"
    previous_year_full = current_years[1]  # e.g., "2024"
    current_year_short = current_years[2]  # e.g., "25"
    previous_year_short = current_years[3]  # e.g., "24"
    
    # Determine password characteristics
    is_simple = not any(char in password for char in '4310579@!$#()6^&*') and not any(char.isdigit() for char in password)
    has_year = any(year in password for year in current_years)
    has_symbol = any(char in password for char in '!@#$%^&*')
    has_numbers = any(char.isdigit() for char in password)
    
    # Check if password contains valid months (if expiration is specified)
    if expiration_days is not None:
        valid_months = get_valid_months(expiration_days)
        valid_months_lower = [month.lower() for month in valid_months]
        password_lower = password.lower()
        
        contains_valid_month = any(month.lower() in password_lower for month in valid_months)
        if word_type == 'months' and not contains_valid_month:
            score -= 50.0  # Heavy penalty for expired months
    
    # New priority weighting system with leetspeak-aware custom word scoring
    if word_type == 'custom':
        # Check if this custom word has heavy leetspeak
        leet_char_count = sum(1 for char in password if char in '4310579@!$#()6^&*' and char in '4310579()')
        if leet_char_count >= 3:  # Heavy leetspeak custom words get reduced priority
            score = 160.0  # Lower than teams when heavily modified
        else:
            score = 200.0  # Normal custom word priority
    elif word_type == 'common_passwords' and is_simple:
        score = 190.0  # Common passwords with no modifications
    elif word_type == 'seasons' and has_year and not has_symbol:
        score = 180.0  # Seasons + year
    elif word_type == 'seasons' and has_year and has_symbol:
        score = 170.0  # Seasons + year + symbol  
    elif word_type == 'months' and has_year and not has_symbol:
        score = 160.0  # Months + year
    elif word_type == 'months' and has_year and has_symbol:
        score = 150.0  # Months + year + symbol
    elif word_type == 'teams':
        score = 140.0  # Sports teams, etc
    elif word_type == 'mascots':
        score = 130.0  # Mascots, etc
    else:
        score = 100.0  # Everything else (tech defaults, keyboard walks, etc)
    
    # IMPROVED CASE PATTERN SCORING (major improvement)
    if len(password) > 0:
        if password[0].isupper() and len(password) > 1 and password[1:].islower():
            score += 25.0  # Title case (Cowboys2025) - MOST COMMON
        elif password.islower():
            score += 15.0  # All lowercase - moderately common
        elif password.isupper():
            score -= 10.0  # All uppercase - MUCH LESS COMMON (penalty!)
        else:
            score += 5.0   # Mixed case patterns
    
    # OPTIMAL LENGTH SCORING (corporate password policies)
    length = len(password)
    if 8 <= length <= 10:
        score += 15.0  # Sweet spot for most corporate policies
    elif 11 <= length <= 12:
        score += 10.0  # Still good
    elif 6 <= length <= 7:
        score += 5.0   # Too short for many policies
    elif 13 <= length <= 15:
        score += 3.0   # Getting long
    else:
        score -= 8.0   # Very short or very long less common
    
    # SYMBOL FREQUENCY SCORING (based on real usage)
    if has_symbol:
        symbol_scores = {'!': 15.0, '@': 12.0, '#': 10.0, '$': 8.0, '%': 6.0, '^': 4.0, '&': 3.0, '*': 2.0}
        for symbol, symbol_score in symbol_scores.items():
            if symbol in password:
                score += symbol_score
                break  # Only count the first (most common) symbol found
    
    # POSITION-BASED SCORING (endings are most common)
    if password.endswith(('123', '1', '01', '!', '@')):
        score += 18.0  # Very common endings
    elif password.endswith(('1234', '12345', '#', '$')):
        score += 12.0  # Common endings
    elif password.endswith(('%', '^', '&', '*')):
        score += 8.0   # Less common endings
    
    # DYNAMIC YEAR PROXIMITY SCORING (current year gets highest score)
    if current_year_full in password:
        score += 25.0  # Current year full
    elif current_year_short in password:
        score += 20.0  # Current year short
    elif previous_year_full in password:
        score += 15.0  # Previous year full
    elif previous_year_short in password:
        score += 12.0  # Previous year short
    
    # LEETSPEAK PENALTY (significantly increased - much less common)
    leet_chars = set('4310579@!$#()6^&*')
    leet_count = sum(1 for char in password if char in leet_chars and char in '4310579()')
    if leet_count > 0:
        score -= (leet_count * 15.0)  # Much stronger penalty for leetspeak
    
    # Additional penalty for very heavy leetspeak modifications
    if leet_count >= 3:
        score -= 25.0  # Extra penalty for heavily modified words
    
    # COMPLEXITY PENALTIES
    symbol_count = sum(1 for char in password if char in '!@#$%^&*')
    if symbol_count > 1:
        score -= (symbol_count - 1) * 10.0  # Multiple symbols much less common
    
    # CORPORATE POLICY BONUS (common requirements)
    meets_policy = (length >= 8 and 
                   any(c.isupper() for c in password) and
                   any(c.islower() for c in password) and
                   any(c.isdigit() for c in password) and
                   any(c in '!@#$%^&*' for c in password))
    if meets_policy:
        score += 12.0  # Bonus for meeting typical corporate password policy
    
    # WORD FREQUENCY BONUS (within categories)
    word_freq_bonus = {
        'password': 10.0, 'welcome': 8.0, 'admin': 7.0, 'qwerty': 6.0,
        'spring': 8.0, 'summer': 7.0, 'winter': 6.0, 'fall': 5.0,
        'january': 6.0, 'december': 5.0, 'march': 4.0
    }
    
    base_word = ''.join(c for c in password if c.isalpha()).lower()
    if base_word in word_freq_bonus:
        score += word_freq_bonus[base_word]
    
    # SEQUENTIAL PATTERN DETECTION
    if '123' in password:
        score += 8.0   # Very common sequence
    elif '234' in password or '345' in password:
        score += 4.0   # Less common sequences
    
    # Specific pattern bonuses
    if word_type in ['seasons', 'months'] and has_year:
        score += 8.0   # Clean seasonal/monthly patterns popular
    
    # TEAM NAME BONUS - prioritize clean team patterns
    if word_type == 'teams':
        # Bonus for clean team names with simple patterns
        if has_year and len([c for c in password if c in '4310579()']) == 0:  # No leetspeak
            score += 15.0  # Clean team + year patterns are very common
        if password.endswith(('!', '@', '123', '1')):
            score += 10.0  # Common team endings
    
    if word_type == 'custom' and (has_year or password.endswith(('123', '1', '!'))):
        # Reduced bonus for custom words to prevent over-prioritization
        score += 8.0  # Reduced from 12.0
    
    return score

def generate_scored_variations(base_words: List[str], word_type: str, symbols_count: int = 5, expiration_days: int = None) -> List[tuple]:
    """Generate variations with scores for a word type."""
    if not base_words:
        return []
    
    variations = generate_variations(base_words, symbols_count, expiration_days)
    scored_variations = []
    
    for password in variations:
        score = calculate_password_score(password, word_type, expiration_days)
        scored_variations.append((password, score, word_type))
    
    return scored_variations

def validate_city_input(city: str) -> str:
    """Validate and normalize city input."""
    if not city:
        print("Error: City name cannot be empty.", file=sys.stderr)
        sys.exit(1)
    
    if not isinstance(city, str):
        print("Error: City name must be a string.", file=sys.stderr)
        sys.exit(1)
    
    city_clean = city.strip()
    if not city_clean:
        print("Error: City name cannot be only whitespace.", file=sys.stderr)
        sys.exit(1)
    
    if len(city_clean) > 100:
        print("Error: City name too long (max 100 characters).", file=sys.stderr)
        sys.exit(1)
    
    return city_clean

def parse_custom_words(words_input: str) -> List[str]:
    """Parse custom words from file path or comma-separated string."""
    if not words_input:
        return []
    
    # Check if it's a file path
    import os
    if os.path.isfile(words_input):
        try:
            with open(words_input, 'r', encoding='utf-8') as f:
                words = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        words.append(line)
                return words
        except Exception as e:
            print(f"Error reading word file '{words_input}': {e}", file=sys.stderr)
            return []
    else:
        # Treat as comma-separated string
        return [word.strip() for word in words_input.split(',') if word.strip()]

def filter_by_length(passwords: List[str], min_length: int) -> List[str]:
    """Filter passwords by minimum length."""
    if min_length <= 0:
        return passwords
    return [pwd for pwd in passwords if len(pwd) >= min_length]

def generate_passwords(city: str, custom_words: List[str] = None, min_length: int = 0, symbols_count: int = 5, expiration_days: int = None) -> List[str]:
    """Generate password candidates based on city, custom words, and length requirements."""
    city_validated = validate_city_input(city)
    city_key = city_validated.lower()
    
    teams: List[str] = PRO_TEAMS.get(city_key, [])
    mascots: List[str] = FBS_MASCOTS.get(city_key, [])
    
    # Get dynamic months based on expiration policy
    valid_months = get_valid_months(expiration_days)
    
    # Process each word list independently with scoring
    all_scored_variations: List[tuple] = []
    
    # Process each word type with appropriate scoring
    if COMMON_PASSWORDS:
        scored_vars = generate_scored_variations(COMMON_PASSWORDS, 'common_passwords', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if TECH_DEFAULTS:
        scored_vars = generate_scored_variations(TECH_DEFAULTS, 'tech_defaults', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if SEASONS:
        scored_vars = generate_scored_variations(SEASONS, 'seasons', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if valid_months:
        scored_vars = generate_scored_variations(valid_months, 'months', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if KEYBOARD_WALKS:
        scored_vars = generate_scored_variations(KEYBOARD_WALKS, 'keyboard_walks', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if teams:
        scored_vars = generate_scored_variations(teams, 'teams', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if mascots:
        scored_vars = generate_scored_variations(mascots, 'mascots', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    # Process city variations
    city_words = [city_key, city_key.title(), city_key.upper()]
    if city_words:
        scored_vars = generate_scored_variations(city_words, 'city', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    # Process custom words independently
    if custom_words:
        scored_vars = generate_scored_variations(custom_words, 'custom', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    # Sort by score (highest first) and extract passwords
    all_scored_variations.sort(key=lambda x: x[1], reverse=True)
    all_passwords = [password for password, score, word_type in all_scored_variations]
    
    if not all_passwords:
        print(f"Warning: No passwords generated for city '{city_validated}'.", file=sys.stderr)
        # Fallback to basic defaults
        fallback_words = COMMON_PASSWORDS + TECH_DEFAULTS
        scored_vars = generate_scored_variations(fallback_words, 'common_passwords', symbols_count, expiration_days)
        scored_vars.sort(key=lambda x: x[1], reverse=True)
        all_passwords = [password for password, score, word_type in scored_vars]
    
    try:
        # Filter by minimum length if specified
        if min_length > 0:
            filtered_passwords = filter_by_length(all_passwords, min_length)
            if not filtered_passwords:
                print(f"Warning: No passwords meet minimum length requirement of {min_length} characters.", file=sys.stderr)
                return all_passwords  # Return unfiltered if none meet criteria
            return filtered_passwords
        
        return all_passwords
    except Exception as e:
        print(f"Error processing password results: {e}", file=sys.stderr)
        sys.exit(1)

def generate_passwords_with_scores(city: str, custom_words: List[str] = None, min_length: int = 0, symbols_count: int = 5, expiration_days: int = None) -> List[tuple]:
    """Generate password candidates with scores for debugging."""
    city_validated = validate_city_input(city)
    city_key = city_validated.lower()
    
    teams: List[str] = PRO_TEAMS.get(city_key, [])
    mascots: List[str] = FBS_MASCOTS.get(city_key, [])
    
    # Get dynamic months based on expiration policy  
    valid_months = get_valid_months(expiration_days)
    
    # Process each word list independently with scoring
    all_scored_variations: List[tuple] = []
    
    # Process each word type with appropriate scoring
    if COMMON_PASSWORDS:
        scored_vars = generate_scored_variations(COMMON_PASSWORDS, 'common_passwords', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if TECH_DEFAULTS:
        scored_vars = generate_scored_variations(TECH_DEFAULTS, 'tech_defaults', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if SEASONS:
        scored_vars = generate_scored_variations(SEASONS, 'seasons', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if valid_months:
        scored_vars = generate_scored_variations(valid_months, 'months', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if KEYBOARD_WALKS:
        scored_vars = generate_scored_variations(KEYBOARD_WALKS, 'keyboard_walks', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if teams:
        scored_vars = generate_scored_variations(teams, 'teams', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    if mascots:
        scored_vars = generate_scored_variations(mascots, 'mascots', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    # Process city variations
    city_words = [city_key, city_key.title(), city_key.upper()]
    if city_words:
        scored_vars = generate_scored_variations(city_words, 'city', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    # Process custom words independently
    if custom_words:
        scored_vars = generate_scored_variations(custom_words, 'custom', symbols_count, expiration_days)
        all_scored_variations.extend(scored_vars)
    
    # Sort by score (highest first)
    all_scored_variations.sort(key=lambda x: x[1], reverse=True)
    
    # Filter by minimum length if specified
    if min_length > 0:
        all_scored_variations = [(pwd, score, wtype) for pwd, score, wtype in all_scored_variations if len(pwd) >= min_length]
    
    return all_scored_variations

def validate_count(count: int) -> int:
    """Validate the password count parameter."""
    if count <= 0:
        print("Error: Count must be a positive integer.", file=sys.stderr)
        sys.exit(1)
    
    if count > 100000:
        print("Error: Count too large (max 100,000).", file=sys.stderr)
        sys.exit(1)
    
    return count

def main() -> None:
    """Main function to handle command line arguments and generate passwords."""
    try:
        parser = argparse.ArgumentParser(
            description="Generate password candidates based on city and common patterns.",
            epilog="Examples:\n"
                   "  python password_generator.py 'New York' --count 50\n"
                   "  python password_generator.py 'Dallas' --words 'company,brand,server' --min-length 8\n"
                   "  python password_generator.py 'Boston' --words /path/to/wordlist.txt --output passwords.txt\n"
                   "  python password_generator.py 'Seattle' --expiration 60 --symbols 3 --output seattle_passwords.txt\n"
                   "  python password_generator.py 'Miami' --expiration 90 --words 'finance,corp' --debug",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument("city", help="City name (e.g., 'New York', 'Dallas', 'Pittsburgh')")
        parser.add_argument("--count", type=int, 
                          help="Number of passwords to show (default: all combinations, max: 100,000)")
        parser.add_argument("--output", type=str, 
                          help="Output file path to write passwords (default: stdout)")
        parser.add_argument("--words", type=str, 
                          help="Custom words to include: comma-separated list or path to word file")
        parser.add_argument("--min-length", type=int, default=0,
                          help="Minimum password length (default: no minimum)")
        parser.add_argument("--symbols", type=int, default=5,
                          help="Number of symbols to use, ordered by frequency (default: 5, max: 8)")
        parser.add_argument("--expiration", type=int, 
                          help="Password expiration in days (e.g., 60) - limits months included")
        parser.add_argument("--debug", action="store_true",
                          help="Show password scores for debugging (default: false)")
        
        args = parser.parse_args()
        
        # Validate count if provided
        generate_all = args.count is None
        validated_count = None
        if args.count is not None:
            validated_count = validate_count(args.count)
        
        # Parse custom words if provided
        custom_words = []
        if args.words:
            custom_words = parse_custom_words(args.words)
            if custom_words:
                print(f"Loaded {len(custom_words)} custom words", file=sys.stderr)
            else:
                print("No custom words loaded", file=sys.stderr)
        
        # Validate minimum length
        min_length = 0
        if args.min_length:
            if args.min_length < 0:
                print("Error: Minimum length cannot be negative.", file=sys.stderr)
                sys.exit(1)
            if args.min_length > 100:
                print("Error: Minimum length too large (max 100).", file=sys.stderr)
                sys.exit(1)
            min_length = args.min_length
        
        # Validate symbols count
        symbols_count = args.symbols
        if symbols_count < 1:
            print("Error: Symbols count must be at least 1.", file=sys.stderr)
            sys.exit(1)
        if symbols_count > 8:
            print("Error: Symbols count cannot exceed 8 (total available symbols).", file=sys.stderr)
            sys.exit(1)
        
        # Validate expiration days
        expiration_days = args.expiration
        if expiration_days is not None:
            if expiration_days < 1:
                print("Error: Expiration days must be at least 1.", file=sys.stderr)
                sys.exit(1)
            if expiration_days > 1095:  # 3 years
                print("Error: Expiration days too large (max 1095 days).", file=sys.stderr)
                sys.exit(1)
            if expiration_days:
                valid_months = get_valid_months(expiration_days)
                print(f"Using {len(valid_months)} valid months based on {expiration_days}-day expiration policy", file=sys.stderr)
        
        # Generate passwords
        all_passwords = generate_passwords(args.city, custom_words, min_length, symbols_count, expiration_days)
        
        if not all_passwords:
            print("Error: No passwords generated.", file=sys.stderr)
            sys.exit(1)
        
        # Determine how many passwords to output
        if generate_all:
            passwords_to_output = all_passwords
            print(f"Generating all {len(passwords_to_output)} password combinations", file=sys.stderr)
        else:
            sample_size = min(validated_count, len(all_passwords))
            passwords_to_output = all_passwords[:sample_size]
            print(f"Generating top {len(passwords_to_output)} passwords", file=sys.stderr)
        
        # Prepare output content
        output_lines = []
        
        if args.debug:
            # For debug mode, show scores and word types
            debug_passwords = generate_passwords_with_scores(args.city, custom_words, min_length, symbols_count, expiration_days)
            if generate_all:
                debug_data = debug_passwords
            else:
                debug_data = debug_passwords[:validated_count]
            
            for password, score, word_type in debug_data:
                output_lines.append(f"{password} (Score: {score:.1f}, Type: {word_type})")
        else:
            # Normal mode - just passwords
            output_lines = passwords_to_output
        
        # Output results (to file or stdout)
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    for line in output_lines:
                        f.write(line + '\n')
                print(f"Passwords written to {args.output}", file=sys.stderr)
            except Exception as e:
                print(f"Error writing to file '{args.output}': {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Output to stdout
            for line in output_lines:
                print(line)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
