import json
from fabric import Connection
import requests
from base64 import b64encode
from nacl import encoding, public


class Github:
    def __init__(self, username: str, token: str, repo: str) -> None:
        self.username = username
        self.token = token
        self.repo = repo
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

    def upload_secret(self, secret_name: str, secret_value: str) -> int:
        """Upload a secret to Github secrets."""
        public_key, key_id = self._get_public_key()
        encrypted_secret = self.encrypt(public_key, secret_value)
        response = requests.put(
            f'https://api.github.com/repos/{self.username}/{self.repo}/actions/secrets/{secret_name}',
            data=json.dumps(
                {
                    "encrypted_value": encrypted_secret,
                    "key_id": key_id
                }
            ),
            auth=(self.username, self.token)
        )
        return response.status_code


    def setenv(path):
        with open(path, 'r') as envfile:
            env = envfile.read()



    def secrets_dict(self, conn: Connection, ip_address: str) -> dict:
        """Returns a structured dictionary that with fields ready to upload to Github secrets."""
        id_rsa = conn.run('cat /home/ubuntu/.ssh/id_rsa', hide='both')
        return {
            "HOST": ip_address,
            "PORT": "22",
            "USERNAME": "ubuntu",
            "SSHKEY": id_rsa.stdout
        }


    def _get_public_key(self) -> tuple:
        """Return the public key from Github needed to make further requests."""
        response = requests.get(f'https://api.github.com/repos/{self.username}/{self.repo}/actions/secrets/public-key', auth=(self.username, self.token))
        content = json.loads(response.content)
        return content.get('key'), content.get('key_id')


    def encrypt(self, public_key: str, secret_value: str) -> str:
        """Encrypt a Unicode string using the public key."""
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")
