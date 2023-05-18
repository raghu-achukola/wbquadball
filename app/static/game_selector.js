
function reset_select(selectObject){
    var i, L = selectObject.options.length - 1;
    for(i = L; i >= 1; i--) {   // i >=1 so it leaves the "last" aka "first" object the blank state
        selectObject.remove(i);
    }
}

function load_seasons(all_data, value){
    console.log(`LOAD_SEASONS TRIGGERED WITH ${value}`)
    var seasonSelectorDiv = document.getElementById('season_selector')
    var seasonSelect = document.getElementById('seasons')
    reset_select(seasonSelect)
    if (value === ''){
        seasonSelect.value = ''
        seasonSelectorDiv.setAttribute('style', "visibility: hidden")
    }
    else{
        seasonSelectorDiv.setAttribute('style', "")
        var seasons = all_data.seasons
        seasons.forEach(x => {
            if (x.league_id === value){
                add_to_selector(seasonSelect,x.display_name,x.season_id)
            }
        })
    }
    seasonSelect.dispatchEvent(new Event('change'))
}

function load_tournaments(all_data, value){
    
    var tournamentSelectorDiv = document.getElementById('tournament_selector')
    var tournamentSelect = document.getElementById('tournaments')
    reset_select(tournamentSelect)
    if (value === ''){
        tournamentSelect.value = ''
        tournamentSelectorDiv.setAttribute('style', "visibility: hidden")
    }
    else{
        tournamentSelectorDiv.setAttribute('style', "")
        var tournaments = all_data.tournaments
        tournaments.forEach(x => {
            if (x.season_id === value){
                add_to_selector(tournamentSelect,x.display_name,x._id)
            }
        })

    }
    tournamentSelect.dispatchEvent(new Event('change'))
}

function load_games(all_data,value){
    var gameSelectorDiv = document.getElementById('game_selector')
    var gameSelect = document.getElementById('games')
    reset_select(gameSelect)
    if (value === ''){
        gameSelectorDiv.setAttribute('style', "visibility: hidden")
    }
    else{
        gameSelectorDiv.setAttribute('style', "")
        var games = all_data.games
        games.forEach(x => {
            if(x.tournament_id === value){
                add_to_selector(gameSelect,x.display_name, x._id)
            }
        })

    }
}



function add_to_selector(selector,objectName, objectID){
    var opt = document.createElement('option');
    opt.value = objectID
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
        data.leagues.forEach(x => add_to_selector(leagueSelector,x.display_name,x.display_name))

        leagueSelector.addEventListener(
            'change',
            function() { load_seasons(data,this.value); },
            false
        );

        seasonSelector.addEventListener(
            'change',
            function() { load_tournaments(data,this.value); },
            false
        );

        tournamentSelector.addEventListener(
            'change',
            function() { load_games(data,this.value); },
            false
        );

        

        
    }
)
    
