from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle


class BannerVenda(GridLayout):

    def __init__(self, **kwargs):
        # 1. Remove parâmetros dinâmicos para evitar erros no Kivy
        cliente = kwargs.pop("cliente", "")
        foto_cliente = kwargs.pop("foto_cliente", "")
        produto = kwargs.pop("produto", "")
        foto_produto = kwargs.pop("foto_produto", "")
        unidade = kwargs.pop("unidade", "")
        data = kwargs.pop("data", "")
        preco = kwargs.pop("preco", 0)
        quantidade = kwargs.pop("quantidade", 0)

        # 2. Trata valores numéricos de preço
        try:
            preco_num = float(preco)
        except (ValueError, TypeError):
            preco_num = 0.0

        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = "100dp"
        self.cols = 3
        self.padding = [10, 5, 10, 5]
        self.spacing = 5

        # --- FUNDO MODERNO ESCURO (PRETO COM TRANSPARÊNCIA E BORDAS ARREDONDADAS) ---
        with self.canvas.before:
            Color(0.05, 0.08, 0.12, 0.85)  # Preto levemente azulado com 85% de opacidade
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[12, 12, 12, 12])
        self.bind(pos=self._atualizar_canvas, size=self._atualizar_canvas)

        # -------------------------------------------------------------
        # 1. COLUNA ESQUERDA (Cliente)
        # -------------------------------------------------------------
        esquerda = FloatLayout()
        esquerda_imagem = Image(
            pos_hint={"center_x": 0.5, "top": 0.95},
            size_hint=(0.8, 0.65),
            source=f"icones/fotos_clientes/{foto_cliente}" if foto_cliente else ""
        )
        esquerda_label = Label(
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "top": 0.28},
            text=str(cliente).capitalize(),
            font_size="12sp",
            bold=True,
            color=(1, 1, 1, 1)
        )
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        # -------------------------------------------------------------
        # 2. COLUNA MEIO (Produto)
        # -------------------------------------------------------------
        meio = FloatLayout()
        meio_imagem = Image(
            pos_hint={"center_x": 0.5, "top": 0.95},
            size_hint=(0.8, 0.65),
            source=f"icones/fotos_produtos/{foto_produto}" if foto_produto else ""
        )
        meio_label = Label(
            size_hint=(1, 0.25),
            pos_hint={"center_x": 0.5, "top": 0.28},
            text=str(produto).capitalize(),
            font_size="12sp",
            bold=True,
            color=(1, 1, 1, 1)
        )
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)

        # -------------------------------------------------------------
        # 3. COLUNA DIREITA (Data, Preço e Quantidade)
        # -------------------------------------------------------------
        direita = FloatLayout()

        direita_label_data = Label(
            size_hint=(1, 0.3),
            pos_hint={"x": 0, "top": 0.95},
            text=f"Data: [b]{data}[/b]",
            markup=True,
            font_size="11sp",
            halign="left",
            valign="middle",
            color=(0.8, 0.8, 0.8, 1)
        )
        direita_label_data.bind(size=direita_label_data.setter('text_size'))

        direita_label_preco = Label(
            size_hint=(1, 0.3),
            pos_hint={"x": 0, "top": 0.65},
            text=f"Preço: [color=#00DF9A][b]R${preco_num:.2f}[/b][/color]",
            markup=True,
            font_size="11sp",
            halign="left",
            valign="middle"
        )
        direita_label_preco.bind(size=direita_label_preco.setter('text_size'))

        direita_label_quantidade = Label(
            size_hint=(1, 0.3),
            pos_hint={"x": 0, "top": 0.35},
            text=f"Qtd: [b]{quantidade} {unidade}[/b]",
            markup=True,
            font_size="11sp",
            halign="left",
            valign="middle",
            color=(0.9, 0.9, 0.9, 1)
        )
        direita_label_quantidade.bind(size=direita_label_quantidade.setter('text_size'))

        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_quantidade)

        # -------------------------------------------------------------
        # Adiciona as 3 colunas ao Grid
        # -------------------------------------------------------------
        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def _atualizar_canvas(self, *args):
        """Redimensiona o fundo arredondado quando o widget altera de posição/tamanho"""
        self.rect.pos = self.pos
        self.rect.size = self.size