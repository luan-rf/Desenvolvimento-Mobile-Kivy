import os
from functools import partial
import requests
from datetime import date

from kivy.app import App
from kivy.lang import Builder

from bannervenda import BannerVenda
from bannervendedor import BannerVendedor
from botoes import *
from myfirebase import MyFireBase
from telas import *


class MainApp(App):

    unidade = None
    cliente = None
    produto = None

    def build(self):
        # Carrega a interface principal e define self.root automaticamente
        return Builder.load_file("main.kv")

    def on_start(self):
        # Definição do parâmetro do Firebase
        self.firebase = MyFireBase()


        # Carregar as fotos de clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionarvendas = self.root.ids["adicionarvendas"]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto}", on_release=partial(self.selecionar_cliente, foto))
            label = LabelButton(text=foto.replace(".png", "").capitalize(), on_release=partial(self.selecionar_cliente, foto))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)

        # Carregar as fotos de produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionarvendas = self.root.ids["adicionarvendas"]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto}", on_release=partial(self.selecionar_produto, foto))
            label = LabelButton(text=foto.replace(".png", "").capitalize(), on_release=partial(self.selecionar_produto, foto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)


        # Carregar as fotos de perfil na lista da tela MudarFoto
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_foto_perfil = self.root.ids["mudarfoto"]
        lista_fotos = pagina_foto_perfil.ids["lista_fotos_perfil"]

        # Limpa elementos antes de preencher
        lista_fotos.clear_widgets()

        for foto in arquivos:
            imagem = ImageButton(
                source=f"icones/fotos_perfil/{foto}",
                on_release=partial(self.mudar_foto_perfil, foto)
            )
            lista_fotos.add_widget(imagem)


        # Carrega a data
        pagina_adicionar_vendas = self.root.ids["adicionarvendas"]
        label_data = pagina_adicionar_vendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"


        # Carrega as informações do usuário
        self.carrega_infos_usuario()

    def carrega_infos_usuario(self):
        try:
            # Faz a leitura do refresh token do usuário
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read().strip()

            # Troca o refresh token pelas credenciais
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            # Requisita dados do usuário no Realtime Database
            link = f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            requisicao = requests.get(link)
            dados = requisicao.json()

            # GARANTIA: Se os dados não forem um dicionário (ex: retornar None, False ou mensagem de erro em String)
            if not isinstance(dados, dict):
                print(f"Atenção: Resposta inválida do Firebase para o usuário {self.local_id}. Retorno: {dados}")
                return

            # Alteração e Reload da Foto de Perfil
            avatar = dados.get("avatar", "foto1.png")
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"
            foto_perfil.reload()
            self.avatar = avatar

            # ID único
            id_vendedor = dados.get("id_vendedor", "")
            self.id_vendedor = id_vendedor

            # Total vendas
            total_vendas = dados.get("total_vendas", "0")
            self.total_vendas = total_vendas

            # Equipe
            self.equipe = dados.get("equipe", "")

            pagina_ajustes = self.root.ids["ajustespage"]
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID único: {id_vendedor}"

            pagina_home = self.root.ids["homepage"]
            lista_vendas = pagina_home.ids["lista_vendas"]
            pagina_home.ids[
                "label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]  R${total_vendas}[/b]"

            # Limpa widgets anteriores da lista para não duplicar vendas
            lista_vendas.clear_widgets()

            # Processamento e inclusão das vendas do usuário
            try:
                vendas = dados.get("vendas", {})
                self.vendas = vendas

                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(
                        cliente=venda.get("cliente", ""),
                        foto_cliente=venda.get("foto_cliente", ""),
                        produto=venda.get("produto", ""),
                        foto_produto=venda.get("foto_produto", ""),
                        data=venda.get("data", ""),
                        preco=venda.get("preco", "0"),
                        unidade=venda.get("unidade", ""),
                        quantidade=venda.get("quantidade", "0")
                    )
                    lista_vendas.add_widget(banner)
            except Exception as e:
                print(f"Erro ao carregar vendas do usuário: {e}")

            # Carrega a equipe
            equipe = dados.get("equipe", "")
            if equipe:
                lista_equipe = equipe.split(",")
                pagina_lista_vendedores = self.root.ids["listarvendedores"]
                lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]
                lista_vendedores.clear_widgets()

                for id_vendedor_equipe in lista_equipe:
                    id_limpo = id_vendedor_equipe.strip()
                    if id_limpo:
                        banner_vendedor = BannerVendedor(id_vendedor=id_limpo)
                        lista_vendedores.add_widget(banner_vendedor)

            self.mudar_tela("homepage")

        except Exception as e:
            print(f"Erro ao carregar infos do usuário: {e}")


    def mudar_foto_perfil(self, foto, *args):
        # Atualiza o avatar local e recarrega
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"
        foto_perfil.reload()

        # Envia a alteração do avatar para o Firebase
        info = f'{{"avatar": "{foto}"}}'
        requests.patch(
            f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
            data=str(info)
        )
        self.mudar_tela("ajustespage")


    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def adicionar_vendedor(self, id_vendedor_adicionar):
        # CORRIGIDO: Inclusão do auth={self.id_token}
        link = f'https://aplicacaocomkivy-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionar}"&auth={self.id_token}'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        pagina_adicionar_vendedor = self.root.ids["adicionarvendedores"]
        mensagem_adicionar_vendedor = pagina_adicionar_vendedor.ids["mensagem_outrovendedor"]

        if not requisicao_dic:
            mensagem_adicionar_vendedor.text = "Vendedor não encontrado."
            mensagem_adicionar_vendedor.color = (1, 0, 0, 1)
        else:
            equipe = self.equipe.split(",") if self.equipe else []
            if id_vendedor_adicionar in equipe:
                mensagem_adicionar_vendedor.text = "Este usuário já faz parte da sua equipe."
                mensagem_adicionar_vendedor.color = (1, 0, 0, 1)
            else:
                if self.equipe:
                    self.equipe = f"{self.equipe},{id_vendedor_adicionar}"
                else:
                    self.equipe = str(id_vendedor_adicionar)

                link = f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
                dados_equipe = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(link, data=dados_equipe)

                # CORRIGIDO: Mensagem alterada para sucesso
                mensagem_adicionar_vendedor.text = "Vendedor adicionado com sucesso!"
                mensagem_adicionar_vendedor.color = (0, 1, 0, 1)

                pagina_listar_vendedores = self.root.ids["listarvendedores"]
                lista_vendedores = pagina_listar_vendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionar)
                lista_vendedores.add_widget(banner_vendedor)



    def selecionar_cliente(self, foto, *args): # foto -> 'carrefour.png'
        # pintar de azul o texto do item que foi selecionado e pintar de branco o resto dos itens
        pagina_adicionar_vendas = self.root.ids["adicionarvendas"]
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]

        self.cliente = foto.replace(".png", "")

        # altera o atributo de color dos textos de todos os 'children' do objeto lista_clientes da página, pois somente labels possuem 'text:"
        for item in list(lista_clientes.children):
            item.color = (1,1,1,1) # branco
            try:
                texto = item.text
                texto = texto.lower()
                texto = texto + ".png"
                if foto == texto:
                    item.color = (0,207/255,219/255,1) # azul
            except:
                pass



    def selecionar_produto(self, foto, *args):  # foto -> 'carrefour.png'
        # pintar de azul o texto do item que foi selecionado e pintar de branco o resto dos itens
        pagina_adicionar_vendas = self.root.ids["adicionarvendas"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]

        self.produto = foto.replace(".png", "")

        # altera o atributo de color dos textos de todos os 'children' do objeto lista_clientes da página, pois somente labels possuem 'text:"
        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)  # branco
            try:
                texto = item.text
                texto = texto.lower()
                texto = texto + ".png"
                if foto == texto:
                    item.color = (0, 207 / 255, 219 / 255, 1)  # azul
            except:
                pass



    # 'id_tem' é o objeto labelbutton que vem do metodo on_release dos botões
    def selecionar_unidade(self, id_item, *args):
        pagina_adicionar_vendas = self.root.ids["adicionarvendas"]

        self.unidade = id_item.replace("unidades_", "")

        # pintar todos os itens de branco
        pagina_adicionar_vendas.ids["unidades_kg"].color = (1,1,1,1)
        pagina_adicionar_vendas.ids["unidades_unidades"].color = (1,1,1,1)
        pagina_adicionar_vendas.ids["unidades_litros"].color = (1,1,1,1)

        # pintar o item selecionado de azul
        pagina_adicionar_vendas.ids[id_item].color = (0, 207 / 255, 219 / 255, 1)



    def adicionar_venda(self):
        # definição das variaveis que o usuário tem no momento
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade

        # preenchimento do campo da data, preço e quantidade
        pagina_adicionar_vendas = self.root.ids["adicionarvendas"]
        data = pagina_adicionar_vendas.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionar_vendas.ids["preco_total"].text
        quantidade = pagina_adicionar_vendas.ids["quantidade_total"].text

        # tratamento em caso não tenha sido escolhido todos os campos antes de preencher a nova venda
        if not cliente:
            pagina_adicionar_vendas.ids["label_selecao_cliente"].color = (1,0,0,1)
        if not produto:
            pagina_adicionar_vendas.ids["label_selecione_produto"].color = (1,0,0,1)
        if not unidade:
            pagina_adicionar_vendas.ids["unidades_litros"].color = (1,0,0,1)
            pagina_adicionar_vendas.ids["unidades_unidades"].color = (1,0,0,1)
            pagina_adicionar_vendas.ids["unidades_kg"].color =(1,0,0,1)
        if not preco:
            pagina_adicionar_vendas.ids["label_preco"].color = (1,0,0,1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)
        if not quantidade:
            pagina_adicionar_vendas.ids["label_quantidade"].color = (1,0,0,1)
        else:
            try:
                quantidade = int(quantidade)
            except:
                pagina_adicionar_vendas.ids["label_quantidade"].color = (1,0,0,1)


        # caso esteja tudo preenchido na pagina e os tipos dos dados estejam corretos, é feita a requisição no banco
        if cliente and produto and unidade and preco and quantidade and (type(preco) == float) and (type(quantidade) == int):
            # ajuste do nome das imagens com .png
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png"

            # post no banco de dados com as informações selecionadas no formato do firebase api
            info = (f'{{"cliente": "{cliente}", "foto_cliente": "{foto_cliente}", "produto": "{produto}", '
                    f'"foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", '
                    f'"preco": "{preco}", "quantidade": "{quantidade}"}}')
            requests.post(f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}", data=info)

            # criação do banner de venda e ajuste no layout para eles aparecerem
            banner_venda = BannerVenda(cliente=cliente, foto_cliente= foto_cliente,
                                       produto=produto, foto_produto=foto_produto,
                                       data=data, preco=preco, quantidade=quantidade, unidade=unidade)
            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner_venda)

            # alteração do valor de vendas do usuário logado, pegando o valor atual, somando e fazendo patch no banco com o valor atualizado
            requisicao = requests.get(f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}")
            total_vendas = float(requisicao.json())
            total_vendas += preco
            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(f"https://aplicacaocomkivy-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}", data=info)

            # alteração do valor no label da homepage que mostra o valor de total vendas
            pagina_homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]  R${total_vendas}[/b]"

            # muda a tela para a homepage
            self.mudar_tela("homepage")



        # Depois de adicionar a venda, os itens voltam ao padrão
        self.cliente = None
        self.unidade = None
        self.produto = None

    def carregar_todas_vendas(self):
        pagina_todas_vendas = self.root.ids["todasvendas"]
        lista_vendas = pagina_todas_vendas.ids["lista_vendas"]

        # Limpa as vendas exibidas anteriormente
        lista_vendas.clear_widgets()

        # Requisição corrigida: orderBy em minúsculo e inclusão do id_token
        link = f'https://aplicacaocomkivy-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&auth={self.id_token}'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/hash.png"
        total_vendas = 0

        # Verifica se o retorno é um dicionário válido
        if isinstance(requisicao_dic, dict):
            for local_id_usuario in requisicao_dic:
                try:
                    vendas = requisicao_dic[local_id_usuario].get("vendas", {})
                    for id_venda in vendas:
                        venda = vendas[id_venda]

                        # Converte e acumula o total
                        try:
                            preco_num = float(venda["preco"])
                        except (ValueError, TypeError):
                            preco_num = 0.0

                        total_vendas += preco_num

                        # Valores e criação do banner
                        banner_venda = BannerVenda(
                            cliente=venda.get("cliente", ""),
                            foto_cliente=venda.get("foto_cliente", ""),
                            produto=venda.get("produto", ""),
                            foto_produto=venda.get("foto_produto", ""),
                            data=venda.get("data", ""),
                            preco=venda.get("preco", 0),
                            quantidade=venda.get("quantidade", 0),
                            unidade=venda.get("unidade", "")
                        )

                        # Adiciona o banner na tela
                        lista_vendas.add_widget(banner_venda)
                except Exception as e:
                    print(f"Erro ao processar vendas do usuário {local_id_usuario}: {e}")

        # Atualiza a Label com o valor total formatado
        pagina_todas_vendas.ids[
            "label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]  R${total_vendas:.2f}[/b]"

        # Redireciona para a tela
        self.mudar_tela("todasvendas")



    def sair_todas_vendas(self, id_tela):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"

        self.mudar_tela(id_tela)



    def carregar_vendas_vendedor(self, requisicao_dic, *args):
        # Definição da página de vendas de outros vendedores e da lista
        pagina_outros_vendedor = self.root.ids["vendasoutrovendedor"]
        lista_vendas = pagina_outros_vendedor.ids["lista_vendas"]

        # Limpa widgets de buscas anteriores
        lista_vendas.clear_widgets()

        # Definição do valor de total vendas
        total_vendas = requisicao_dic.get("total_vendas", "0")
        pagina_outros_vendedor.ids["label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]  R${total_vendas}[/b]"

        # Atualiza a foto de perfil do vendedor selecionado no cabeçalho
        avatar = requisicao_dic.get("avatar", "foto1.png")
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # Criação dos banners com base nas vendas do vendedor selecionado
        try:
            vendas = requisicao_dic.get("vendas", {})
            for id_venda in vendas:
                venda = vendas[id_venda]

                banner_venda = BannerVenda(
                    cliente=venda["cliente"],
                    foto_cliente=venda["foto_cliente"],
                    produto=venda["produto"],
                    foto_produto=venda["foto_produto"],
                    data=venda["data"],
                    preco=venda["preco"],
                    quantidade=venda["quantidade"],
                    unidade=venda["unidade"]
                )

                lista_vendas.add_widget(banner_venda)
        except Exception as e:
            print(f"Erro ao carregar vendas do outro vendedor: {e}")

        # Redirecionamento de telas
        self.mudar_tela("vendasoutrovendedor")


if __name__ == "__main__":
    MainApp().run()