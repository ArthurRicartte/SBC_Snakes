#Informações para quem clonar o repositório: Criar um ambiente virtual:
"""
depois que baixar o python 3.9.13 vai no terminal e cola:

1 -> py -3.9 -m venv venv_sbc
1 -> .\venv_sbc\Scripts\activate
1 -> pip install -r requirements.txt
"""
from experta import KnowledgeEngine, Rule, Fact, MATCH, AS
from experta import P    # predicates (e.g. P(lambda x: x > 37.8))
from experta import OR, AND, NOT
from rich import print

#Definindo as classes que vão servir como fatos:
class Cobra(Fact):
    """
    Será o fato de entrada na memória de trabalho, pode conter as caracterísitcas físicas de uma cobra:
    Tamanho_médio = float
    local_encontrado = onde o usuário encontrou o animal = floresta, sertão (caatinga), área residencial, árvore, etc 
    eh_agressiva = (valor booleano sim ou não)
    cor = string
    padrão_corpo = string descrevendo brevemente os padrões de corpo do animal
    tem_fosseta_loreal = (Valor booleano sim ou não)
    padrão_cauda = string descrevendo a cauda do animal. ex = chocalho, cauda pontuda...
    """
    pass

class Familia(Fact):
    """
    Fato que será derivada a partir do fato Cobra(), teremos 4 famílias possíveis:
    - Viperidae: Para a Cascavel e Jararaca-da-Caatinga
    - Elapidae: Coral-verdadeira
    - Colubridae: Falsa-coral, Cobra-cipó-verde e Corre-campo
    - Boidae: Jiboia
    """
    pass

class Genero(Fact):
    """
    Fato que deriva da Família e de algumas característica da cobra, os possíveis valores são:
    - Bothrops: Jararaca-da-Caatinga 
    - Crotalus: Cascavel
    - Micrurus: Coral-verdadeira
    - Oxyrhopus: Falsa-coral
    - Boa: Jiboia
    - Philodryas: Cobra-cipó-verde e Corre-campo
    """
    pass

class Diagnostico(Fact):
    """"
    Resposta final: Gênero + informações específicas da cobra (onde foi encontrada) + Cor. Possíveis respostas:
    - Jararaca-da-Caatinga (Bothrops erythromelas)
    - Cascavel (Crotalus durissus)
    - Coral-verdadeira (Micrurus ibiboboca)
    - Falsa-coral (Oxyrhopus trigeminus / Apostolepis cearensis)
    - Jiboia (Boa constrictor)
    - Cobra-cipó-verde (Philodryas olfersii) 
    - Corre-campo (Philodryas nattereri)

    Diagnóstico tem os seguintes campos:
    - Nome do animal (Tipo um nickname)
    - Nome popular
    - Nome científico
    """
    pass


#Base de Conhecimento:
class ProcessoIdentificacao(KnowledgeEngine):
    #Regra 1: tentativa de disparar regra de saliência máxima: Caso a cobra tenha chocalho na cauda -> Cascavél (Característica muito predominante)
    @Rule(Cobra(nome=MATCH.nome, padrao_cauda="chocalho"), NOT(Diagnostico(nome=MATCH.nome)), salience=100)
    def atalho_cascavel(self, nome):
        print(f"[red][SALIENCE 100] [Regra 1][/] -> Chocalho detectado! {nome} é uma [red]Cascavel (Crotalus durissus).[/]\n") #Testando o print do rich
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Cascavel",
            nome_cientifico="Crotalus durissus"
        ))


    #Nível 1 de encadeamento: A partir de características da cobra derivamos uma família:


    #Regra 2: Família Viperidae (Jararaca e Cascavel)
    @Rule(
        Cobra(nome=MATCH.nome, tem_fosseta_loreal =True),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel1_viperidae(self, nome):
        print(f"[blue][Nível 1] [Regra 2]:[/] Fosseta loreal detectada -> [green]{nome}[/] pertence à [green]família Viperidae[/]")
        self.declare(Familia(nome=nome, familia="Viperidae"))

    #Regra 3: Família Elapidae (Coral-verdadeira)
    @Rule(
        Cobra(nome=MATCH.nome, tem_fosseta_loreal=False, padrao_corpo="aneis_completos"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel1_elapidae(self, nome):
        print(f"[blue][Nível 1] [Regra 3]:[/] Sem fosseta + Anéis completos -> [green]{nome}[/] pertence à [green]família Elapidae[/]")
        self.declare(Familia(nome=nome, familia="Elapidae"))

    #Regra 4: Família Boidae (Jiboia)
    @Rule(
        Cobra(nome=MATCH.nome, tem_fosseta_loreal=False, tamanho_medio=P(lambda t: t >= 2.0)),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel1_boidae(self, nome):
        print(f"[blue][Nível 1] [Regra 4]:[/] Sem fosseta + Porte grande (>= 2m) -> [green]{nome}[/] pertence à família [green]Boidae[/]")
        self.declare(Familia(nome=nome, familia="Boidae"))

    #Regra 5: Família Colubridae (Falsa-coral, Cobra-cipó-verde, Corre-campo)
    @Rule(
        Cobra(
            nome=MATCH.nome, 
            tem_fosseta_loreal=False, 
            tamanho_medio=P(lambda t: t < 2.0),
        ),
        NOT(Cobra(nome=MATCH.nome, padrao_corpo="aneis_completos")), #Impede de captar cobra Coral verdadeira
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel1_colubridae(self, nome):
        print(f"[blue][Nível 1] [Regra 5]:[/] Sem fosseta + Porte < 2m + Sem anéis completos -> [green]{nome}[/] pertence à família [green]Colubridae[/]")
        self.declare(Familia(nome=nome, familia="Colubridae"))


    #Nível 2 de derivação de fatos: Família() + Cobra() -> Genero():
    

    # Regra 6: Gênero Bothrops (Jararaca-da-Caatinga)
    @Rule(
        Familia(nome=MATCH.nome, familia="Viperidae"),
        Cobra(nome=MATCH.nome, padrao_corpo="triângulos"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel2_bothrops(self, nome):
        print(f"[cyan][Nível 2] [Regra 6]:[/] Viperidae + Desenhos em triângulos -> [green]{nome}[/] pertence ao gênero [green]Bothrops[/]")
        self.declare(Genero(nome=nome, genero="Bothrops"))

    # Regra 7: Gênero Micrurus (Coral-verdadeira)
    @Rule(
        Familia(nome=MATCH.nome, familia="Elapidae"),
        Cobra(nome=MATCH.nome, padrao_corpo="aneis_completos"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel2_micrurus(self, nome):
        print(f"[cyan][Nível 2] [Regra 7]:[/] Elapidae + Anéis coloridos completos -> [green]{nome}[/] pertence ao gênero [green]Micrurus[/]")
        self.declare(Genero(nome=nome, genero="Micrurus"))

    # Regra 8: Gênero Oxyrhopus (Falsa-coral)
    @Rule(
        Familia(nome=MATCH.nome, familia="Colubridae"),
        Cobra(nome=MATCH.nome, padrao_corpo="aneis_incompletos"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel2_oxyrhopus(self, nome):
        print(f"[cyan][Nível 2] [Regra 8]:[/] Colubridae + Anéis incompletos -> [green]{nome}[/] pertence ao gênero [green]Oxyrhopus[/]")
        self.declare(Genero(nome=nome, genero="Oxyrhopus"))

    # Regra 9: Gênero Philodryas (Cobra-cipó-verde e Corre-campo)
    #Cobra corre campo e Cobra cipó pertencem ao mesmo gênero
    #Solução: Utilizar o OR
    @Rule(
        Familia(nome=MATCH.nome, familia="Colubridae"),
        OR(
            Cobra(nome=MATCH.nome, cor="verde"),
            Cobra(nome=MATCH.nome, cor="marrom_amarelo")
        ),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel2_philodryas(self, nome):
        print(f"[cyan][Nível 2] [Regra 9]:[/] Colubridae + Cor verde ou marrom/amarelo -> [green]{nome}[/] pertence ao gênero [green]Philodryas[/]")
        self.declare(Genero(nome=nome, genero="Philodryas"))

    # Regra 10: Gênero Boa (Jiboia)
    @Rule(
        Familia(nome=MATCH.nome, familia="Boidae"),
        Cobra(nome=MATCH.nome, padrao_corpo="listras_largas"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel2_boa(self, nome):
        print(f"[cyan][Nível 2] [Regra 10]:[/] Boidae + Listras largas transversais -> [green]{nome}[/] pertence ao gênero [green]Boa[/]")
        self.declare(Genero(nome=nome, genero="Boa"))


    #Regras de nível 3: Genero() + Cobra() -> Diagnóstico final = Nome cobra + Nome científico


    # Regra 11: Jararaca-da-Caatinga
    @Rule(
        Genero(nome=MATCH.nome, genero="Bothrops"),
        Cobra(nome=MATCH.nome, cor="marrom_cinza"),
        OR(
            Cobra(nome=MATCH.nome, local_encontrado="floresta"),
            Cobra(nome=MATCH.nome, local_encontrado="area_urbana")
        ),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel3_jararaca(self, nome):
        print(f"[purple][Nível 3] [Regra 11]:[/] Gênero Bothrops + Marrom/Cinza + Floresta/Área Urbana -> Diagnóstico: [green]{nome}[/] é uma [green]Jararaca-da-Caatinga[/]\n")
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Jararaca-da-Caatinga",
            nome_cientifico="Bothrops erythromelas"
        ))

    # Regra 12: Coral-verdadeira
    @Rule(
        Genero(nome=MATCH.nome, genero="Micrurus"),
        Cobra(nome=MATCH.nome, padrao_cauda="curta", local_encontrado="subterraneo"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel3_coral_verdadeira(self, nome):
        print(f"[purple][Nível 3] [Regra 12]:[/] Gênero Micrurus + Cauda curta + Subterrâneo -> Diagnóstico: [green]{nome}[/] é uma [green]Coral-verdadeira[/]\n")
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Coral-verdadeira",
            nome_cientifico="Micrurus ibiboboca"
        ))

    # Regra 13: Falsa-coral
    @Rule(
        Genero(nome=MATCH.nome, genero="Oxyrhopus"),
        Cobra(nome=MATCH.nome, padrao_cauda="longa", local_encontrado="caatinga_terrestre"),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel3_falsa_coral(self, nome):
        print(f"[purple][Nível 3] [Regra 13]:[/] Gênero Oxyrhopus + Cauda longa + Caatinga Terrestre -> Diagnóstico: [green]{nome}[/] é uma [green]Falsa-coral[/]\n")
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Falsa-coral",
            nome_cientifico="Oxyrhopus trigeminus"
        ))

    # Regra 14: Cobra-cipó-verde
    @Rule(
        Genero(nome=MATCH.nome, genero="Philodryas"),
        Cobra(nome=MATCH.nome, cor="verde"),
        OR(
            Cobra(nome=MATCH.nome, local_encontrado="arvore"),
            Cobra(nome=MATCH.nome, local_encontrado="solo")
        ),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel3_cipo_verde(self, nome):
        print(f"[purple][Nível 3] [Regra 14]:[/] Gênero Philodryas + Cor verde + Árvore/Solo -> Diagnóstico: [green]{nome}[/] é uma [green]Cobra-cipó-verde[/]\n")
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Cobra-cipó-verde",
            nome_cientifico="Philodryas olfersii"
        ))

    # Regra 15: Corre-campo
    @Rule(
        Genero(nome=MATCH.nome, genero="Philodryas"),
        Cobra(nome=MATCH.nome, cor="marrom_amarelo", padrao_corpo="pontos_escuros"),
        OR(
            Cobra(nome=MATCH.nome, local_encontrado="estrada"),
            Cobra(nome=MATCH.nome, local_encontrado="lajedo"),
            Cobra(nome=MATCH.nome, local_encontrado="area_descampada")
        ),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel3_corre_campo(self, nome):
        print(f"[purple][Nível 3] [Regra 15]:[/] Gênero Philodryas + Marrom/Amarelo com pontos + Estrada/Lajedo/Descampado -> Diagnóstico: [green]{nome}[/] é uma [green] Corre-campo[/]\n")
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Corre-campo",
            nome_cientifico="Philodryas nattereri"
        ))

    # Regra 16: Jiboia
    @Rule(
        Genero(nome=MATCH.nome, genero="Boa"),
        Cobra(nome=MATCH.nome, cor="amarelada"),
        OR(
            Cobra(nome=MATCH.nome, local_encontrado="terrestre"),
            Cobra(nome=MATCH.nome, local_encontrado="arvore"),
            Cobra(nome=MATCH.nome, local_encontrado="galinheiro")
        ),
        NOT(Diagnostico(nome=MATCH.nome))
    )
    def nivel3_jiboia(self, nome):
        print(f"[purple][Nível 3] [Regra 16]:[/] Gênero Boa + Amarelada + Terrestre/Árvore/Galinheiro -> Diagnóstico: [green]{nome}[/] é uma [green] Jiboia[/]\n")
        self.declare(Diagnostico(
            nome=nome,
            nome_popular="Jiboia",
            nome_cientifico="Boa constrictor"
        ))


def main():
    #Testando tudo:
    identify = ProcessoIdentificacao()
    identify.reset()

    """"
        #Teste 1: Cascavél com saliência
        identify.declare(Cobra(nome="Jujuba", padrao_cauda="chocalho"))
    """

    """"
    # Teste 2: Jararaca-da-Caatinga
    identify.declare(Cobra(
        nome="Teste_2", 
        tem_fosseta_loreal=True, 
        padrao_corpo="triângulos", 
        cor="marrom_cinza", 
        tamanho_medio=0.54,
        local_encontrado="floresta"
    ))
    """

    """"
    # Teste 3: Coral-verdadeira (Trajeto esperado: Elapidae -> Micrurus -> Diagnóstico)
    identify.declare(Cobra(
        nome="Teste_3", 
        tem_fosseta_loreal=False, 
        padrao_corpo="aneis_completos", 
        padrao_cauda="curta", 
        local_encontrado="subterraneo",
        tamanho_medio=1.0
    ))
    """

    """"
    # Teste 4: Falsa-coral (Trajeto esperado: Colubridae -> Oxyrhopus -> Diagnóstico)
    identify.declare(Cobra(
        nome="Teste_4", 
        tem_fosseta_loreal=False, 
        padrao_corpo="aneis_incompletos", 
        padrao_cauda="longa", 
        local_encontrado="caatinga_terrestre",
        tamanho_medio=0.70
    ))
    """

    """"
    # Teste 5: Cobra-cipó-verde (Trajeto esperado: Colubridae -> Philodryas -> Diagnóstico)
    identify.declare(Cobra(
        nome="Teste_5", 
        tem_fosseta_loreal=False, 
        cor="verde", 
        padrao_corpo="uniforme", 
        local_encontrado="arvore",
        tamanho_medio=1.0
    ))
    """

    """"
    # Teste 6: Corre-campo (Trajeto esperado: Colubridae -> Philodryas -> Diagnóstico)
    identify.declare(Cobra(
        nome="Teste_6", 
        tem_fosseta_loreal=False, 
        cor="marrom_amarelo", 
        padrao_corpo="pontos_escuros", 
        local_encontrado="estrada",
        tamanho_medio=1.5
    ))
    """

    """"
    # Teste 7: Jiboia (Trajeto esperado: Boidae -> Boa -> Diagnóstico)
    identify.declare(Cobra(
        nome="Teste_7", 
        tem_fosseta_loreal=False, 
        cor="amarelada", 
        padrao_corpo="listras_largas", 
        local_encontrado="galinheiro",
        tamanho_medio=4.0
    ))
    """

    identify.run()

if __name__ == "__main__":
    main()