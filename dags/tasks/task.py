import jinja2
import requests

BOOTSTRAP_STATIC_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


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


def render_template(**kwargs):
    response = call_api(BOOTSTRAP_STATIC_URL)
    data = transform_teams(response)

    templateEnv = initialize_template_environment(searchpath=kwargs["searchpath"])
    template = templateEnv.get_template(kwargs["template_path"])
    outputText = template.render(data=data)

    with open(kwargs["rendered_sql"], "w") as output_file:
        output_file.write(outputText)
