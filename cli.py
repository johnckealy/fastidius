import typer
import shutil
import os
import subprocess
import sys
from mako.template import Template


app = typer.Typer()



def generate_file(filename, **kwargs):
    routes_base = Template(filename=filename).render(**kwargs)
    with open(filename.replace('/src/', '/app/'), 'w') as file:
        file.write(routes_base)


@app.command(help='Create a brand new web application.')
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

    auth = typer.confirm("Add authentication?", default=True)
    if auth:
        user_model = typer.prompt("Please specify the name of your User model", default='User')
        user_model = user_model.strip().capitalize()
    models = typer.prompt("Please specify the names of the initial database models (comma separated)", default='')
    models = [model.strip().capitalize() for model in models.split(',')]



    path = os.path.dirname(os.path.abspath(__file__))
    shutil.copytree(f'{path}/src', 'app', dirs_exist_ok=True)

    generate_file(f'app/backend/main.py', alembic=True)




@app.command(help='Run the newly generated web application using uvicorn.')
def run():
    os.chdir('app')
    if not os.path.isdir('.python3.9_env'):
        subprocess.run(["virtualenv", ".python3.9_env", "-p", "python3.9"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])

    os.environ["BASE_ENVIRONMENT"] = "dev"

    subprocess.run(["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])




if __name__ == "__main__":
    app()
