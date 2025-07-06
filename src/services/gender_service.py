import os
import requests

class GenderService:
    def __init__(self, api: str = "genderize"):
        self.api = api.lower()
        self.token = None

        if self.api == "genderapi":
            self.token = os.getenv("GENDERAPI_TOKEN")
            if not self.token:
                raise ValueError("Variável de ambiente GENDERAPI_TOKEN não configurada")
            self.api_url = "https://genderapi.io/api/"
        elif self.api == "gender-api.com":
            self.token = os.getenv("GENDER_API_TOKEN")
            if not self.token:
                raise ValueError("Variável de ambiente GENDER_API_TOKEN não configurada")
            self.api_url = "https://gender-api.com/get"
        else:
            # genderize.io
            self.api_url = "https://api.genderize.io"

    def inferir_genero(self, nome: str) -> str:
        nome = nome.strip()
        if not nome:
            return "desconhecido"

        try:
            if self.api == "genderize":
                return self._usar_genderize(nome)
            elif self.api == "genderapi":
                return self._usar_genderapi(nome)
            elif self.api == "gender-api.com":
                return self._usar_gender_api_com(nome)
            else:
                return "desconhecido"
        except requests.RequestException:
            return "desconhecido"

    def _usar_genderize(self, nome: str) -> str:
        params = {"name": nome}
        resp = requests.get(self.api_url, params=params, timeout=5)
        if resp.status_code == 200:
            dados = resp.json()
            return dados.get("gender", "desconhecido")
        return "desconhecido"

    def _usar_genderapi(self, nome: str) -> str:
        params = {"name": nome, "key": self.token}
        resp = requests.get(self.api_url, params=params, timeout=5)
        if resp.status_code == 200:
            dados = resp.json()
            gender = dados.get("gender")
            if gender:
                return gender
        return "desconhecido"

    def _usar_gender_api_com(self, nome: str) -> str:
        params = {"name": nome, "key": self.token}
        resp = requests.get(self.api_url, params=params, timeout=5)
        if resp.status_code == 200:
            dados = resp.json()
            gender = dados.get("gender")
            if gender:
                return gender
        return "desconhecido"
