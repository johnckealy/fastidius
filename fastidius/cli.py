import os
import sys
import typer
import shutil
import subprocess

from invoke.exceptions import UnexpectedExit
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

    # Copy the app directory over from the templates.
    shutil.copytree(f'{FILEPATH}/app_template', app_name, dirs_exist_ok=True)

    include_backend = typer.confirm("Include a backend? ", default=False)
    # auth = typer.confirm("Add authentication?", default=True)
    # if auth:
    #     user_model = typer.prompt("Please specify the name of your User model", default='User')
    #     user_model = user_model.strip().capitalize()
    # models = typer.prompt("Please specify the names of the initial database models (comma separated)", default='')
    # models = [model.strip().capitalize() for model in models.split(',')]


    generate_file(f'{app_name}/backend/main.py', alembic=True)
    generate_file(f'{app_name}/docker-compose.yml', include_backend=include_backend, app_name=app_name)
    generate_file(f'{app_name}/README.md', include_backend=include_backend, app_name=app_name)
    generate_file(
        f'{app_name}/.github/workflows/test_and_deploy.yml',
        app_name=app_name,
        host='${{ secrets.HOST }}',
        username='${{ secrets.USERNAME }}',
        port='${{ secrets.PORT }}',
        ssh_key='${{ secrets.SSHKEY }}',
    )
    colored_echo(f'App creation was successful. You can now: cd {app_name}/', color='green')



@cli.command(help='For use directly after initializing a new VPS server. ')
def initialize_server(ip_address: str = typer.Option(IP_ADDRESS)):
    """Simple command to print out the necessary shell command to set up a new droplet."""
    if ip_error(ip_address):
        raise typer.Exit(code=1)
    typer.echo('Run this command to set up a new Droplet.')
    colored_echo(f'\n\nssh root@{ip_address} "bash -s" < {FILEPATH}/deploy/server_setup.sh\n')
    typer.echo('If all went well, you should be able to ssh into the server. Do this at least '
               'once now, because the password newly created sudo user must be set.')
    colored_echo(f'\nssh ubuntu@{ip_address}')



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
            LETSENCRYPT_EMAIL='example@hello.com',
            ORIGIN_DOMAIN='example.com',
            API_DOMAIN='api.example.com'
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
                  "local version and send up the docker container.\n")
    confirm = typer.confirm(f"\nAre you happy with the contents of {FILEPATH}/deploy/Caddyfile? \n")
    if confirm:
        conn.put( f'{FILEPATH}/deploy/Caddyfile', remote="/caddy/Caddyfile",  preserve_mode=False)
        conn.put( f'{FILEPATH}/deploy/docker-compose.yml', remote="/caddy/docker-compose.yml",  preserve_mode=False)
        conn.run('cd /caddy/ && docker-compose up --build -d', echo=True)



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




@cli.command(help='')
def deploy(path: str, ip_address: str = typer.Option(IP_ADDRESS)):
    conn = connect_to_server(ip_address)



@cli.command(help='Run the newly generated web application using uvicorn.')
def run():
    os.chdir('app')
    if not os.path.isdir('.python3.9_env'):
        subprocess.run(["virtualenv", ".python3.9_env", "-p", "python3.9"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
    os.environ["BASE_ENVIRONMENT"] = "dev"
    subprocess.run(["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])



if __name__ == "__main__":
    cli()
