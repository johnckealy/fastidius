from click import echo
import typer
import shutil
import os
import subprocess
import sys
from mako.template import Template
from fastidius import __version__
from fabric import Connection
from invoke.exceptions import UnexpectedExit


cli = typer.Typer()
FILEPATH = f'{os.path.dirname(os.path.abspath(__file__))}/fastidius'


def version_callback(value: bool):
    """Faciliates printing the --version."""
    if value:
        typer.echo(f"Fastidius {__version__}")
        raise typer.Exit()


@cli.callback()
def common(ctx: typer.Context, version: bool = typer.Option(None, "--version", callback=version_callback)):
    """Faciliates printing the --version."""
    pass


def colored_echo(message, color='blue'):
    COLORS = {
        'blue': typer.colors.BRIGHT_BLUE
    }
    typer.echo(typer.style(message, fg=COLORS[color]))


def generate_file(filename, outfile=None, **kwargs):
    routes_base = Template(filename=filename).render(**kwargs)
    if not outfile:
        outfile = filename
    with open(outfile, 'w') as file:
        file.write(routes_base)


def connect_to_server(ip_address: str, root=False):
    host = 'root' if root else 'ubuntu'
    return Connection(
        host=f'{host}@{ip_address}',
        connect_kwargs={
            "key_filename": f"{os.getenv('HOME')}/.ssh/id_ed25519.pub",
        }
    )


@cli.command(help='Create a brand new web application.')
def create():
    typer.echo(
        """


            ______              __   _      __ _
           / ____/____ _ _____ / /_ (_)____/ /(_)____   __  __ _____
          / /_   / __ `// ___// __// // __  // // __ \ / / / // ___/
         / __/  / /_/ /(__  )/ /_ / // /_/ // // /_/ // /_/ /(__  )
        /_/     \__,_//____/ \__//_/ \__,_//_/ \____/ \__,_//____/

        """
    )
    typer.echo(
        typer.style("fastidius needs a few settings before generating your app.\n ", fg=typer.colors.GREEN, bold=True)
    )

    app_name = typer.prompt("Please give your app a name: ", default='app')
    auth = typer.confirm("Add authentication?", default=True)
    if auth:
        user_model = typer.prompt("Please specify the name of your User model", default='User')
        user_model = user_model.strip().capitalize()
    models = typer.prompt("Please specify the names of the initial database models (comma separated)", default='')
    models = [model.strip().capitalize() for model in models.split(',')]

    shutil.copytree(f'{FILEPATH}/app_template', app_name, dirs_exist_ok=True)

    generate_file(f'{app_name}/backend/main.py', alembic=True)



@cli.command(help='Experimental command. Connect to a remote server and run a basic setup script on it.')
def initialize_server(ip_address: str, use_fabric=None):
    """
    Experimental command. The main logic is still buggy so not in use, so the command just print the required shell command.
    """
    if use_fabric:
        conn = connect_to_server(root=True)
        with open(f'{FILEPATH}/deploy/server_setup.sh', 'r') as script:
            conn.run(script.read(), warn=True)
    else:
        typer.echo('Run this command to set up a new Droplet.')
        typer.echo(
            typer.style(f'\n\nssh root@{ip_address} "bash -s" < {FILEPATH}/deploy/server_setup.sh\n', fg=typer.colors.BRIGHT_BLUE)
        )


@cli.command(help='Generate a new Caddyfile and docker setup for caddy.')
def configure_caddy(ip_address: str = typer.Option(...)):
    conn = connect_to_server(ip_address=ip_address)

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
    os.system(f'code {FILEPATH}/deploy/Caddyfile')



@cli.command(help='')
def deploy_caddy(ip_address: str = typer.Option(...)):
    conn = connect_to_server(ip_address=ip_address, root=True)
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
