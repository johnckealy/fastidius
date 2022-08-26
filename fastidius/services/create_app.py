import shutil
import os

from fastidius.services.utils import generate_file


class AppCreator:

    def __init__(self, app_name: str, FILEPATH: str, backend: bool, auth: bool, models: list) -> None:
        self.app_name = app_name
        self.backend = backend
        self.auth = auth
        self.models = models
        self.FILEPATH = FILEPATH

        # Copy the app directory over from the templates.
        shutil.copytree(f'{self.FILEPATH}/app_template', self.app_name, dirs_exist_ok=True)

    def generate(self):
        generate_file(f'{self.app_name}/docker-compose.yml', backend=self.backend, app_name=self.app_name)
        generate_file(f'{self.app_name}/README.md', backend=self.backend, app_name=self.app_name)
        generate_file(
            f'{self.app_name}/.github/workflows/test_and_deploy.yml',
            app_name=self.app_name,
            host='${{ secrets.HOST }}',
            username='${{ secrets.USERNAME }}',
            port='${{ secrets.PORT }}',
            ssh_key='${{ secrets.SSHKEY }}',
        )

        self.generate_frontend()

        # TODO: either implement or remove SQL capability
        self.remove_sqlalchemy()

        if self.backend:
            self.generate_backend()

    def generate_frontend(self):
        generate_file(f'{self.app_name}/frontend/quasar.conf.js', backend=self.backend)
        generate_file(f'{self.app_name}/frontend/package.json', app_name=self.app_name, backend=self.backend)
        generate_file(f'{self.app_name}/frontend/src/layouts/MainLayout.vue', app_name=self.app_name, auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/pages/Index.vue', app_name=self.app_name, auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/pages/Dashboard.vue', auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/store/index.js', auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/router/routes.js', auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/router/index.js', auth=self.auth)

    def generate_backend(self):
        generate_file(f'{self.app_name}/backend/main.py', auth=self.auth, alembic=True)
        generate_file(f'{self.app_name}/backend/db.py', auth=self.auth)
        generate_file(f'{self.app_name}/backend/core/settings/prod.py', app_name=self.app_name)
        generate_file(f'{self.app_name}/backend/core/settings/dev.py', app_name=self.app_name)
        generate_file(f'{self.app_name}/backend/core/settings/test.py', app_name=self.app_name)
        generate_file(f'{self.app_name}/frontend/src/router/routes.js', auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/router/index.js', auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/store/index.js', auth=self.auth)
        generate_file(f'{self.app_name}/backend/requirements.txt', app_name=self.app_name, auth=self.auth, backend=self.backend)

    def remove_backend(self):
        os.remove(f'{self.app_name}/frontend/src/boot/axios.js')

    def remove_auth(self):
        os.remove(f'{self.app_name}/backend/models/user.py')
        os.remove(f'{self.app_name}/backend/core/auth.py')
        os.remove(f'{self.app_name}/backend/api/endpoints/user_endpoints.py')
        os.remove(f'{self.app_name}/frontend/src/components/LoginForm.vue')
        os.remove(f'{self.app_name}/frontend/src/pages/Login.vue')
        os.remove(f'{self.app_name}/frontend/src/pages/Register.vue')
        os.remove(f'{self.app_name}/frontend/src/pages/RegisteredSuccessfully.vue')

    def remove_sqlalchemy(self):
        os.remove(f'{self.app_name}/backend/core/auth-sqlalchemy.py')
        os.remove(f'{self.app_name}/backend/db-sqlalchemy.py')
        os.remove(f'{self.app_name}/backend/main-sqlalchemy.py')
