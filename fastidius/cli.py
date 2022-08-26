import os
import sys
import typer
import subprocess

from invoke.exceptions import UnexpectedExit
from fastidius.services.create_app import AppCreator
from fastidius.services.github import Github
from fastidius.services.utils import colored_echo, connect_to_server, generate_file, ip_error, version_callback, welcome_prompt

cli = typer.Typer()

FILEPATH = f'{os.path.dirname(os.path.abspath(__file__))}'
IP_ADDRESS = os.getenv('IP_ADDRESS')



@cli.callback()
def common(ctx: typer.Context, version: bool = typer.Option(None, "--version", callback=version_callback)):
    """Facilitates printing the --version."""
    pass



@cli.command(help='Create a brand new web application.')
def create():
    """
    Create a web application. Includes a large list of prompts to guide the user through
    essential setup choices for their app.
    """
    welcome_prompt()

    app_name = typer.prompt("Please give your app a name: ", default='app')
    if os.path.isdir('app'):
        overwrite = typer.confirm(f"An app with the name '{app_name}' is already present, overwrite? ", default=True)
        if not overwrite:
            raise typer.Abort()

    backend = typer.confirm("Include a backend? ", default=True)
    if backend:
        auth = typer.confirm("Add authentication?", default=True)
        models = typer.prompt("Please specify the names of the initial database models (comma separated)", default='')
        models = [model.strip().capitalize() for model in models.split(',')]
    else:
        auth = False
        models = []

    creator = AppCreator(
        FILEPATH=FILEPATH,
        backend=backend,
        app_name=app_name,
        auth=auth,
        models=models,
    )

    if not auth:
        creator.remove_auth()

    if not backend:
        creator.remove_backend()

    typer.echo('Creating application...')
    creator.generate()

    # colored_echo(f'App creation was successful. You can now: cd {app_name}/', color='green')



@cli.command(help='For use directly after initializing a new VPS server. ')
def initialize_server(ip_address: str = typer.Option(IP_ADDRESS)):
    """Simple command to print out the necessary shell command to set up a new droplet."""
    if ip_error(ip_address):
        raise typer.Exit(code=1)
    typer.echo('[Run this command locally to set up a new Droplet]')
    colored_echo(f'ssh root@{ip_address} "bash -s" < {FILEPATH}/deploy/server_setup.sh\n')
    typer.echo('[If all went well, you should be able to ssh into the server. Do this at least '
               'once now, because the password for the newly created sudo user must be set]')
    colored_echo(f'ssh ubuntu@{ip_address}\n')



@cli.command(help='Generate a new Caddyfile and docker setup for caddy.')
def configure_caddy(ip_address: str = typer.Option(IP_ADDRESS)):
    """Talks to the server and configures the Caddy Server."""
    conn = connect_to_server(ip_address)
    try:
        conn.get('/caddy/Caddyfile', local=f'{FILEPATH}/deploy/', preserve_mode=False)
    except FileNotFoundError:
        typer.echo("No Caddyfile was found in /caddy, creating one...")
        generate_file(
            filename=f'{FILEPATH}/deploy/Caddyfile.mako',
            outfile=f'{FILEPATH}/deploy/Caddyfile',
            letsencrypt_email='example@hello.com',
            frontend_domain='example.com',
            backend_domain='api.example.com',
            app_name='app'
        )
        typer.echo('Generated a new Caddyfile into {FILEPATH}/deploy/Caddyfile')
    else:
        typer.echo('Successfully downloaded the Caddyfile from the server.')

    confirm = typer.confirm("Open the Caddyfile in vscode? ")
    if confirm:
        os.system(f'code {FILEPATH}/deploy/Caddyfile')



@cli.command(help='')
def deploy_caddy(ip_address: str = typer.Option(IP_ADDRESS)):
    conn = connect_to_server(ip_address, root=True)
    if not conn:
        raise typer.Exit('There was an issue connecting to the server.', code=1)

    try:
        conn.run('ls /caddy/', hide='both')
    except UnexpectedExit:
        conn.run('mkdir /caddy/')

    colored_echo(f"\n[WARNING] This action will overwrite /caddy/Caddyfile on the server with the "
                  "local version and send up the docker container.")
    confirm = typer.confirm(f"Are you happy with the contents of {FILEPATH}/deploy/Caddyfile? ")
    if confirm:
        conn.put( f'{FILEPATH}/deploy/Caddyfile', remote="/caddy/Caddyfile",  preserve_mode=False)
        conn.put( f'{FILEPATH}/deploy/docker-compose.yml', remote="/caddy/docker-compose.yml",  preserve_mode=False)
        typer.echo('Files uploaded. Sending up the Caddy container...')
        conn.run('cd /caddy/ && docker-compose down -v && docker-compose up --build -d', echo=True)




@cli.command(help='Set up the Github Action secrets necessary for deployment.')
def github_setup(
        github_username: str = typer.Option('', envvar='GITHUB_USERNAME'),
        github_token: str = typer.Option('',  envvar='GITHUB_TOKEN'),
        ip_address: str = typer.Option('',  envvar='IP_ADDRESS'),
        github_repo: str = typer.Option(''),
    ):
    """Sets up the Github environment by adding secrets necessary for deployment in Github Actions."""
    if not github_token or not github_username:
        raise ValueError('No github username/token found. Please set either the --github-token ' +
                         'and --github-username flags, or the GITHUB_TOKEN and GITHUB_USERNAME shell variables.')
    if not github_repo:
        github_repo = os.path.basename(os.getcwd())

    github = Github(username=github_username, token=github_token, repo=github_repo)
    conn = connect_to_server(ip_address)
    SECRETS = github.secrets_dict(conn, ip_address)
    for secret_name, secret_value in SECRETS.items():
        response_code = github.upload_secret(secret_name=secret_name, secret_value=secret_value)
        if response_code == 204:
            typer.echo(f'"{secret_name}" was successfully uploaded to Github secrets.')





if __name__ == "__main__":
    cli()
