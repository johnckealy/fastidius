import os
import typer
from fabric import Connection
from typing import Union
from mako.template import Template
from fastidius import __version__


def version_callback(value: bool):
    """Faciliates printing the --version."""
    if value:
        typer.echo(f"Fastidius {__version__}")
        raise typer.Exit()


def generate_file(filename: str, outfile: str = None, **kwargs) -> None:
    """Takes a Mako template file and renders the Mako logic into the file, in place."""
    routes_base = Template(filename=filename).render(**kwargs)
    if not outfile:
        outfile = filename
    with open(outfile, 'w') as file:
        file.write(routes_base)


def colored_echo(message: str, color='blue') -> None:
    """Wrapper on Typer's shell coloring."""
    COLORS = {
        'blue': typer.colors.BRIGHT_BLUE,
        'green': typer.colors.BRIGHT_GREEN,
        'red': typer.colors.BRIGHT_RED
    }
    typer.echo(typer.style(message, fg=COLORS[color]))


def welcome_prompt():
    """Prints the fastidius logo and some into text."""
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


def ip_error(ip_address: str) -> bool:
    """Check if a valid IP address has been provided."""
    if not ip_address:
        typer.echo("[ERROR] No server IP address was supplied, please include one using either --ip-address <IP ADDRESS>, "
                   "or by setting the IP_ADDRESS environment variable.")
        return True
    return False



def connect_to_server(ip_address: str, root: bool = False) -> Union[Connection, None]:
    if ip_error(ip_address):
        raise typer.Exit()

    host = 'root' if root else 'ubuntu'
    conn = Connection(
        host=f'{host}@{ip_address}',
        connect_kwargs={
            "key_filename": f"{os.getenv('HOME')}/.ssh/id_ed25519.pub",
        },
        connect_timeout=6
    )

    try:
        conn.run('ls', hide='both')
    except Exception as error:
        raise typer.Exit(f'[ERROR] Connection to the remote server was unsuccessful ({error})')

    return conn
