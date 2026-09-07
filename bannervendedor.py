from botoes import LabelButton, ImageButton
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
import requests
from kivy.app import App
from functools import partial


class BannerVendedor(FloatLayout):

    def __init__(self, **kwargs):
        id_vendedor = kwargs.pop("id_vendedor", "")
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = "90dp"

        with self.canvas:
            Color(rgb=(0, 0, 0, 0.2))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        meu_app = App.get_running_app()
        id_token = getattr(meu_app, "id_token", "")

        # CORRIGIDO: alterado de "?auth=" para "&auth="
        requisicao = requests.get(
            f'https://aplicacaocomkivy-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"&auth={id_token}'
        )
        requisicao_dic = requisicao.json()

        if requisicao_dic and isinstance(requisicao_dic, dict):
            lista_valores = list(requisicao_dic.values())[0]
            avatar = lista_valores.get("avatar", "foto1.png")
            total_vendas = lista_valores.get("total_vendas", "0")

            imagem = ImageButton(
                source=f"icones/fotos_perfil/{avatar}",
                pos_hint={"right": 0.3, "top": 0.9},
                size_hint=(0.25, 0.8),
                on_release=partial(meu_app.carregar_vendas_vendedor, lista_valores)
            )
            label_id = LabelButton(
                text=f"ID Vendedor: {id_vendedor}",
                pos_hint={"right": 0.9, "top": 0.9},
                size_hint=(0.5, 0.4),
                on_release=partial(meu_app.carregar_vendas_vendedor, lista_valores)
            )
            label_total_vendas = LabelButton(
                text=f"Total de Vendas: R${total_vendas}",
                pos_hint={"right": 0.9, "top": 0.5},
                size_hint=(0.5, 0.4),
                on_release=partial(meu_app.carregar_vendas_vendedor, lista_valores)
            )

            self.add_widget(imagem)
            self.add_widget(label_id)
            self.add_widget(label_total_vendas)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size