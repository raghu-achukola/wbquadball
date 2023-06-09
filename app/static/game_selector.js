
function sanitize_film_links(film_list){
    if (typeof film_list == 'undefined') {
        return encodeURIComponent('[]')
    }
    text = encodeURIComponent('[')
    for (i = 0; i < film_list.length; i++){
        if (i != 0){
            text += encodeURIComponent(',')
        }
        text += encodeURIComponent('"')
        text += encodeURIComponent(film_list[i])
        text += encodeURIComponent('"')
        
    }
    return text + encodeURIComponent(']')
}

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
                add_to_selector(seasonSelect,x.season_id,x.season_id)
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
                add_to_selector(tournamentSelect,x.tournament_name,x._id)
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
                opt.innerHTML = `${x.team_a_name} vs ${x.team_b_name} : ${x.description_in_tournament ?? ''}`
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
        console.log(`PREP_STATSHEET TRIGGERED WITH ${val._id}. Tourney ID: ${tourney}. Season : ${season}. Team A: ${val.team_a_name} Team B: ${val.team_b_name} Film:${encodeURIComponent(val.film_sources)}`)
        button.onclick = function() { downloadStatsheet(season, val._id, tourney, val.winning_team_id, val.losing_team_id, val.team_a_name, val.team_b_name, sanitize_film_links(val.film_sources))}
    }
}

function downloadStatsheet(season_id, game_id, tournament_id, team_a_id, team_b_id, team_a_name, team_b_name,film_sources){
    console.log('Downloading Triggered')
    const a = document.createElement('a')
    a.href = `/statsheet?season_id=${season_id}&game_id=${game_id}&tournament_id=${tournament_id}&team_a_id=${team_a_id}&team_b_id=${team_b_id}&team_a_name=${team_a_name}&team_b_name=${team_b_name}&film_sources=${film_sources}`
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
        data.leagues.forEach(x => add_to_selector(leagueSelector,x.league_id,x.league_id))

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
    
