


function load_seasons(all_data, value){
    if (value === ''){
        document.getElementById('season_selector').setAttribute('style', "visibility: hidden")
    }
    else{
        var seasonSelectorDiv = document.getElementById('season_selector')
        var seasonSelect = document.getElementById('seasons')
        seasonSelectorDiv.setAttribute('style', "")
        var seasons = all_data.seasons
        seasons.forEach(x => add_to_selector(seasonSelect,x))

    }
}

function load_tournaments(all_data, value){
    if (value === ''){
        document.getElementById('tournament_selector').setAttribute('style', "visibility: hidden")
    }
    else{
        var tournamentSelectorDiv = document.getElementById('tournament_selector')
        var tournamentSelect = document.getElementById('tournaments')
        tournamentSelectorDiv.setAttribute('style', "")
        var tournaments = all_data.tournaments
        tournaments.forEach(x => add_to_selector(tournamentSelect,x))

    }
}

function load_games(all_data,value){
    if (value === ''){
        document.getElementById('game_selector').setAttribute('style', "visibility: hidden")
    }
    else{
        var gameSelectorDiv = document.getElementById('game_selector')
        var gameSelect = document.getElementById('games')
        gameSelectorDiv.setAttribute('style', "")
        var games = all_data.games
        games.forEach(x => add_to_selector(gameSelect,x))

    }
}



function add_to_selector(selector,objectName){
    var opt = document.createElement('option');
    opt.value = objectName
    opt.innerHTML = objectName
    selector.appendChild(opt)
}



fetch('/all').then(x => x.json()).then(
    data => {
        console.log(data)
        var leagueSelector = document.getElementById('leagues');
        var seasonSelector = document.getElementById('seasons');
        var tournamentSelector = document.getElementById('tournaments');
        var game_selector = document.getElementById('games');
        data.leagues.forEach(x => add_to_selector(leagueSelector,x))

        leagueSelector.addEventListener(
            'change',
            function() { load_seasons(data,this.id); },
            false
        );

        seasonSelector.addEventListener(
            'change',
            function() { load_tournaments(data,this.id); },
            false
        );

        tournamentSelector.addEventListener(
            'change',
            function() { load_games(data,this.id); },
            false
        );

        

        
    }
)
    
