import os
import requests
from kivy.app import App
from dotenv import load_dotenv

load_dotenv()


class MyFireBase():
    API_KEY = os.getenv("API_KEY")

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        meu_aplicativo = App.get_running_app()

        if requisicao.ok:
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            link = f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}"
            req_id = requests.get(link)
            id_vendedor = req_id.json()

            link_db = f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"
            info_usuario = f'{{"avatar":"foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'

            requisicao_usuario = requests.patch(link_db, data=info_usuario)

            proximo_id_vendedor = int(id_vendedor) + 1
            info_prox_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/.json?auth={id_token}", data=info_prox_id_vendedor)

            if requisicao_usuario.ok:
                meu_aplicativo.carrega_infos_usuario()
                meu_aplicativo.mudar_tela("homepage")
        else:
            mensagem = requisicao_dic.get("error", {}).get("message", "Erro ao criar conta")
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        # CORRIGIDO: alterado "senha" para "password"
        info = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        meu_app = App.get_running_app()

        if requisicao.ok:
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_app.local_id = local_id
            meu_app.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_app.carrega_infos_usuario()
            # CORRIGIDO: adicionado argumento "homepage"
            meu_app.mudar_tela("homepage")

        else:
            mensagem = requisicao_dic.get("error", {}).get("message", "Erro ao fazer login")
            pagina_login = meu_app.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        # CORRIGIDO: "refresh_token" ajustado
        infos = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        requisicao = requests.post(link, data=infos)
        requisicao_dic = requisicao.json()
        return requisicao_dic["user_id"], requisicao_dic["id_token"]