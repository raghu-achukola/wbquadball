
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
    
    console.log(`LOAD_TOURNEYS TRIGGERED WITH ${value}`)
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
    console.log(`LOAD_GAMES TRIGGERED WITH ${value}`)
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
                // Custom code for this to store the entirety of the option
                var opt = document.createElement('option');
                opt.value =JSON.stringify(x)
                opt.innerHTML = x.display_name
                gameSelect.appendChild(opt)
            }
        })

    }
    gameSelect.dispatchEvent(new Event('change'))
}

function prep_statsheet(value, tourney, season){
    var button = document.getElementById('download_button')
    if (value === ''){
        button.setAttribute('style', "visibility: hidden")
        console.log('PREP_STATSHEET TRIGGERED WITH EMPTY value')
    }
    else{
        button.setAttribute('style', "")

        val = JSON.parse(value)
        console.log(val)
        console.log(`PREP_STATSHEET TRIGGERED WITH ${val._id}. Tourney ID: ${tourney}. Season : ${season}. Team A: ${val.team_a} Team B: ${val.team_b}`)
        button.onclick = function() { downloadStatsheet(season, val._id, tourney, val.team_a, val.team_b, val.team_a, val.team_b)}
    }
}

function downloadStatsheet(season_id, game_id, tournament_id, team_a_id, team_b_id, team_a_name, team_b_name){
    console.log('Downloading Triggered')
    const a = document.createElement('a')
    a.href = `/statsheet?season_id=${season_id}&game_id=${game_id}&tournament_id=${tournament_id}&team_a_id=${team_a_id}&team_b_id=${team_b_id}&team_a_name=${team_a_name}&team_b_name=${team_b_name}`
    a.download = `${team_a_name}_${team_b_name}.xlsx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
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
        var gameSelector = document.getElementById('games');
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

        gameSelector.addEventListener(
            'change',
            function() { prep_statsheet(this.value, tournamentSelector.value, seasonSelector.value); },
            false
        );

        
        

        
    }
)
    
