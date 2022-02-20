import uvicorn
import typer
from typing import Optional
from mako.template import Template

app = typer.Typer()


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


    # Dependencies
    requirements = Template(filename='./src/templates/requirements.txt.mako').render()
    with open('app/requirements.txt', 'w') as file:
        file.write(requirements)

    # User auth model
    main = Template(filename='./src/templates/main.py.mako').render(user_model=user_model)
    with open('app/main.py', 'w') as file:
        file.write(main)

    # Base routes, such as the root URI
    routes_base = Template(filename='./src/templates/routes_base.py.mako').render()
    with open('app/routes/base.py', 'w') as file:
        file.write(routes_base)


@app.command(help='Run the newly generated web application using uvicorn.')
def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)



@app.command(help='Run the newly generated web application using uvicorn.')
def swap():
    routes_base = Template(filename='./src/main.py').render(something='Hello')
    with open('./main.py', 'w') as file:
        file.write(routes_base)



if __name__ == "__main__":
    app()
