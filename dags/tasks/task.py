import jinja2
import requests

BOOTSTRAP_STATIC_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"


def initialize_template_environment(searchpath):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    return templateEnv


def call_api(bootstrap_static_url):
    payload = {}
    headers = {}
    response = requests.request(
        "GET", bootstrap_static_url, headers=headers, data=payload
    )
    return response


def transform_teams(response):
    teams_json_format = response.json()["teams"]
    data = [
        {"id": team["id"], "name": team["name"], "short_name": team["short_name"]}
        for team in teams_json_format
    ]
    return data


def transform_players(response):
    players_json_format = response.json()["elements"]
    data = [
        {
            "id": player["id"],
            "first_name": player["first_name"],
            "second_name": player["second_name"],
            "web_name": player["web_name"],
            "position": player["element_type"],
            "team_id": player["team"],
        }
        for player in players_json_format
    ]
    return data


def transform_datetime(response):
    data = [
        fixture["kickoff_time"] for fixture in response.json() if fixture["finished"]
    ]
    return data


def transform_games_results(response):
    games_results = []
    for fixture in response.json():
        if fixture["finished"]:
            games_results.append(fixture)

    data = [
        {
            "id": game["id"],
            "kickoff_time": game["kickoff_time"],
            "team_a": game["team_a"],
            "team_h": game["team_h"],
            "team_a_score": game["team_a_score"],
            "team_h_score": game["team_h_score"],
        }
        for game in games_results
    ]
    return data


def render_template(**kwargs):
    static_response = call_api(BOOTSTRAP_STATIC_URL)
    fixtures_response = call_api(FIXTURES_URL)

    if kwargs["transformation_entity"] == "teams":
        data = transform_teams(static_response)
    elif kwargs["transformation_entity"] == "players":
        data = transform_players(static_response)
    elif kwargs["transformation_entity"] == "datetime":
        data = transform_datetime(fixtures_response)
    elif kwargs["transformation_entity"] == "games_results":
        data = transform_games_results(fixtures_response)

    templateEnv = initialize_template_environment(searchpath=kwargs["searchpath"])
    template = templateEnv.get_template(kwargs["template_path"])
    outputText = template.render(data=data)

    with open(kwargs["rendered_sql"], "w") as output_file:
        output_file.write(outputText)
