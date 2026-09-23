# 🐍 SBC_SNAKES - Sistema Baseado em Conhecimento para Identificação de Serpentes do Nordeste brasileiro

Primeiro mini-projeto da disciplina de **Sistemas Baseados em Conhecimento (SBC)**.

Desenvolvido por: `Arthur Ricartte` e `Felipe Rodrigues`

O objetivo do nosso projeto é desenvolver um motor de inferência utilizando a biblioteca `experta` do Python para identificar 7 espécies de serpentes encontradas no nordeste do Brasil. O sistema utiliza uma base de conhecimento pautada em **regras (If-Then)** com encadeamento em 3 níveis e estratégias de resolução de conflitos (`salience` e `NOT`).

---

## 📌 Descrição do Domínio

O domínio do sistema abrange a identificação taxonômica de serpentes do nordeste brasileiro a partir de observações físicas e comportamentais do animal. Abaixo, listamos todas os atributos que levamos em consideração para classificar as serpentes:

- Tamanho médio
- Habitat natural
- Cor da pele
- Padrão de cor no corpo
- Fosseta Loreal (valor booleano)
- Padrão da cauda


O processo de inferência é estruturado em **3 níveis de encadeamento**:
- **Nível 1 (Entrada $\rightarrow$ Cobra):** Identifica a família biológica a partir dos atributos sobre a cobra.
   -  Possíveis resultados: (*Viperidae*, *Elapidae*, *Boidae* ou *Colubridae*).
- **Nível 2 (Família $\rightarrow$ Gênero):** Por meio da Família e de outras características da cobra, identificamos o gênero.
   -  Possíveis resultados: (*Bothrops*, *Micrurus*, *Oxyrhopus*, *Philodryas* ou *Boa*).
- **Nível 3 (Gênero $\rightarrow$ Espécie):** Emite o diagnóstico final identificando o nome popular, nome científico e se tem peçonha.


> **Regra de Exceção:** O sistema conta com uma regra prioritária (`salience=100`) para a **Cascavel**, que identifica o chocalho na cauda e gera o diagnóstico direto. Sem precisar passar por todos os níveis de derivação.

---

## 📚 Base de Conhecimento acerca do domínio escolhido:
### 1. Família Viperidae
* **Jararaca-da-Caatinga (*Bothrops erythromelas*)**
  * **Gênero:** *Bothrops*
  * **Tamanho Médio:** 54 cm
  * **Habitat:** Áreas florestadas e áreas urbanas
  * **Cor/Padrão:** Marrom com malha cinza e desenhos em formato de triângulos pretos/castanhos
  * **Fosseta Loreal?:** Sim
  * **Tem peçonha?:** Sim

* **Cascavel (*Crotalus durissus*)**
  * **Gênero:** *Crotalus*
  * **Tamanho Médio:** Até 1,80 m
  * **Habitat:** Ambientes terrestres na Caatinga
  * **Cor/Padrão:** Cinza com malha cinza mais clara
  * **Fosseta Loreal?:** Sim
  * **Cauda:** Presença de chocalho (guizo)
  * **Tem peçonha?:** Sim

### 2. Família Elapidae
* **Coral-verdadeira (*Micrurus ibiboboca*)**
  * **Gênero:** *Micrurus*
  * **Tamanho Médio:** Pelo menos 1,0 m
  * **Habitat:** Subterrâneo (embaixo da terra, sob folhas/troncos)
  * **Cor/Padrão:** Anéis coloridos (vermelho, preto, branco/amarelo) que circundam todo o corpo
  * **Fosseta Loreal?:** Não
  * **Cauda:** Curta
  * * **Tem peçonha?:** Sim
      
### 3. Família Colubridae (ou Dipsadidae)
* **Falsa-coral (*Oxyrhopus trigeminus*)**
  * **Gênero:** *Oxyrhopus*
  * **Tamanho Médio:** Até 70 cm
  * **Habitat:** Ambientes terrestres na Caatinga
  * **Cor/Padrão:** Preto, vermelho e branco com anéis incompletos (não circundam a barriga)
  * **Fosseta Loreal?:** Não
  * **Cauda:** Longa
  * **Tem peçonha?:** Não

* **Cobra-cipó-verde (*Philodryas olfersii*)**
  * **Gênero:** *Philodryas*
  * **Tamanho Médio:** Até 1,0 m
  * **Habitat:** Árvores (folhas/galhos) e solo
  * **Cor/Padrão:** Verde uniforme
  * **Fosseta Loreal?:** Não
  * **Cauda:** Comum
  * **Tem peçonha?:** Não

* **Corre-campo (*Philodryas nattereri*)**
  * **Gênero:** *Philodryas*
  * **Tamanho Médio:** Até 1,5 m
  * **Habitat:** Estradas, lajedos e áreas descampadas da Caatinga
  * **Cor/Padrão:** Tom marrom com amarelo e pontinhos escuros pelo corpo
  * **Fosseta Loreal?:** Não
  * **Cauda:** Comum
  * **Tem peçonha?:** Não

### 4. Família Boidae
* **Jiboia (*Boa constrictor*)**
  * **Gênero:** *Boa*
  * **Tamanho Médio:** Pode chegar a 4,0 m
  * **Habitat:** Terrestre, árvores e galinheiros
  * **Cor/Padrão:** Amarelada com listras largas transversais castanhas
  * **Fosseta Loreal?:** Não
  * **Cauda:** Listras transversais nítidas
  * **Tem peçonha?:** Não

---

## 📜 Regras em Linguagem Natural

### Regra de Exceção (Saliência Máxima)
1. **[Atalho de Saliência - Cascavel]:** **SE** a cobra possui chocalho na cauda e **NÃO** possui diagnóstico final, **ENTÃO** cobra é uma **Cascavel (*Crotalus durissus*)**.

### Nível 1: Derivação de Famílias
2. **[Nível 1 - Viperidae]:** **SE** a cobra possui fosseta loreal e **NÃO** possui diagnóstico final, **ENTÃO** pertence à família **Viperidae**.
3. **[Nível 1 - Elapidae]:** **SE** a cobra não possui fosseta loreal, possui anéis completos no corpo e **NÃO** possui diagnóstico final, **ENTÃO** pertence à família **Elapidae**.
4. **[Nível 1 - Boidae]:** **SE** a cobra não possui fosseta loreal, possui tamanho médio maior ou igual a 2 metros e **NÃO** possui diagnóstico final, **ENTÃO** pertence à família **Boidae**.
5. **[Nível 1 - Colubridae]:** **SE** a cobra não possui fosseta loreal, tem tamanho menor que 2 metros, **NÃO** possui anéis completos e **NÃO** possui diagnóstico final, **ENTÃO** pertence à família **Colubridae**.

### Nível 2: Derivação de Gêneros
6. **[Nível 2 - Bothrops]:** **SE** a família é Viperidae, o padrão de corpo é em triângulos e **NÃO** possui diagnóstico final, **ENTÃO** pertence ao gênero **Bothrops**.
7. **[Nível 2 - Micrurus]:** **SE** a família é Elapidae, o padrão de corpo é de anéis completos e **NÃO** possui diagnóstico final, **ENTÃO** pertence ao gênero **Micrurus**.
8. **[Nível 2 - Oxyrhopus]:** **SE** a família é Colubridae, o padrão de corpo é de anéis incompletos e **NÃO** possui diagnóstico final, **ENTÃO** pertence ao gênero **Oxyrhopus**.
9. **[Nível 2 - Philodryas]:** **SE** a família é Colubridae, a cor é verde **OU** marrom-amarelada e **NÃO** possui diagnóstico final, **ENTÃO** pertence ao gênero **Philodryas**.
10. **[Nível 2 - Boa]:** **SE** a família é Boidae, o padrão de corpo é de listras largas e **NÃO** possui diagnóstico final, **ENTÃO** pertence ao gênero **Boa**.

### Nível 3: Diagnóstico Final
11. **[Nível 3 - Jararaca]:** **SE** o gênero é Bothrops, a cor é marrom com cinza, o local encontrado é floresta **OU** área urbana e **NÃO** possui diagnóstico final, **ENTÃO** é uma **Jararaca-da-Caatinga (*Bothrops erythromelas*)**.
12. **[Nível 3 - Coral-verdadeira]:** **SE** o gênero é Micrurus, a cauda é curta, o local encontrado é subterrâneo e **NÃO** possui diagnóstico final, **ENTÃO** é uma **Coral-verdadeira (*Micrurus ibiboboca*)**.
13. **[Nível 3 - Falsa-coral]:** **SE** o gênero é Oxyrhopus, a cauda é longa, o local encontrado é caatinga terrestre e **NÃO** possui diagnóstico final, **ENTÃO** é uma **Falsa-coral (*Oxyrhopus trigeminus*)**.
14. **[Nível 3 - Cobra-cipó-verde]:** **SE** o gênero é Philodryas, a cor é verde, o local encontrado é árvore **OU** solo e **NÃO** possui diagnóstico final, **ENTÃO** é uma **Cobra-cipó-verde (*Philodryas olfersii*)**.
15. **[Nível 3 - Corre-campo]:** **SE** o gênero é Philodryas, a cor é marrom-amarela com pontos escuros, o local encontrado é estrada, lajedo **OU** descampado e **NÃO** possui diagnóstico final, **ENTÃO** é uma **Corre-campo (*Philodryas nattereri*)**.
16. **[Nível 3 - Jiboia]:** **SE** o gênero é Boa, a cor é amarelada, o local encontrado é terrestre, árvore **OU** galinheiro e **NÃO** possui diagnóstico final, **ENTÃO** é uma **Jiboia (*Boa constrictor*)**.

---

## 🧪 Casos de Teste

### Caso de Teste 1: Atalho por Saliência (Cascavel)
* **Entrada:** `Cobra(nome="T1", tem_fosseta_loreal=True, padrao_cauda="chocalho")`
* **Cadeia Esperada:** Disparo imediato da Regra 1 via `salience=100`.
* **Saída:** Diagnóstico: **Cascavel (*Crotalus durissus*)**

### Caso de Teste 2: Encadeamento Completo (Jararaca)
* **Entrada:** `Cobra(nome="T2", tem_fosseta_loreal=True, padrao_corpo="triângulos", cor="marrom_cinza", local_encontrado="floresta", tamanho_medio=0.54)`
* **Cadeia Esperada:**
  1. Nível 1: Dispara Regra 2 $\rightarrow$ Declara `Familia(familia="Viperidae")`
  2. Nível 2: Dispara Regra 6 $\rightarrow$ Declara `Genero(genero="Bothrops")`
  3. Nível 3: Dispara Regra 11 $\rightarrow$ Diagnóstico final
* **Saída:** Diagnóstico: **Jararaca-da-Caatinga (*Bothrops erythromelas*)**

### Caso de Teste 3: Negação Lógica e Resolução por Desempate (Cobra-cipó-verde)
* **Entrada:** `Cobra(nome="T3", tem_fosseta_loreal=False, cor="verde", padrao_corpo="uniforme", local_encontrado="arvore", tamanho_medio=1.0)`
* **Cadeia Esperada:**
  1. Nível 1: Dispara Regra 5 (valida `NOT(Cobra(padrao_corpo="aneis_completos"))`) $\rightarrow$ Declara `Familia(familia="Colubridae")`
  2. Nível 2: Dispara Regra 9 $\rightarrow$ Declara `Genero(genero="Philodryas")`
  3. Nível 3: Dispara Regra 14 $\rightarrow$ Diagnóstico final
* **Saída:** Diagnóstico: **Cobra-cipó-verde (*Philodryas olfersii*)**

---

## 🚀 Como Executar

1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv_sbc
   .\venv_sbc\Scripts\activate
