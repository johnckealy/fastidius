import shutil
import os

from fastidius.services.utils import generate_file


class AppCreator:

    def __init__(self, app_name: str, FILEPATH: str, include_backend: bool, auth: bool, models: list) -> None:
        self.app_name = app_name
        self.include_backend = include_backend
        self.auth = auth
        self.models = models
        self.FILEPATH = FILEPATH

        # Copy the app directory over from the templates.
        shutil.copytree(f'{self.FILEPATH}/app_template', self.app_name, dirs_exist_ok=True)

    def generate(self):
        generate_file(f'{self.app_name}/docker-compose.yml', include_backend=self.include_backend, app_name=self.app_name)
        generate_file(f'{self.app_name}/README.md', include_backend=self.include_backend, app_name=self.app_name)
        generate_file(
            f'{self.app_name}/.github/workflows/test_and_deploy.yml',
            app_name=self.app_name,
            host='${{ secrets.HOST }}',
            username='${{ secrets.USERNAME }}',
            port='${{ secrets.PORT }}',
            ssh_key='${{ secrets.SSHKEY }}',
        )

        self.generate_frontend()

        if self.include_backend:
            self.generate_backend()

    def generate_frontend(self):
        generate_file(f'{self.app_name}/frontend/quasar.conf.js', include_backend=self.include_backend)
        generate_file(f'{self.app_name}/frontend/package.json', app_name=self.app_name, include_backend=self.include_backend)
        generate_file(f'{self.app_name}/frontend/src/layouts/MainLayout.vue', app_name=self.app_name, auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/pages/Index.vue', app_name=self.app_name, auth=self.auth)
        generate_file(f'{self.app_name}/frontend/src/store/index.js', auth=self.auth)

    def generate_backend(self):
        generate_file(f'{self.app_name}/backend/main.py', alembic=True)
        generate_file(f'{self.app_name}/backend/requirements.txt', app_name=self.app_name, auth=self.auth)

    def remove_backend(self):
        os.remove(f'{self.app_name}/frontend/src/boot/axios.js')
        os.remove(f'{self.app_name}/frontend/src/components/LoginForm.vue')
