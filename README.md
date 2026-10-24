# ST Script Manager

**🇧🇷 Português** | [🇺🇸 English](#english)

Ferramenta desktop para Windows, feita em Python, que detecta os jogos instalados na sua Steam e permite criar, organizar e controlar scripts para cada um deles. Desenvolvida para fins de estudo.

## Recursos

- Detecta automaticamente a Steam e todas as bibliotecas configuradas, inclusive em outros discos
- Lista os jogos instalados, com busca por nome
- Mostra nome, App ID, pasta de instalação, tamanho em disco, última atualização e Build ID
- Criação, edição e exclusão de scripts separados para cada jogo
- Checkbox em cada script para definir se ele deve ser executado ou não
- Botão para abrir o jogo pela ferramenta, executando antes apenas os scripts ativos
- Três temas: Claro, Escuro e Dracula
- Interface em Português e English, escolhida ao abrir o programa
- Termos de uso, descrição do app e créditos dentro da própria ferramenta

## Como usar

1. Abra o programa e escolha o idioma.
2. Leia e aceite os termos de uso (apenas na primeira vez).
3. Selecione um jogo na lista da esquerda.
4. Clique em **Novo script**, escreva o código e clique em **Salvar script**.
5. Marque ou desmarque o checkbox de cada script para ativá-lo ou desativá-lo.
6. Clique em **Abrir jogo com scripts ativos**.

## Scripts

Os scripts são escritos em Python e cada um roda em sua própria thread, sem travar a interface. Dentro do script existem três variáveis prontas:

| Variável | Descrição |
|---|---|
| `app_id` | Identificador do jogo na Steam |
| `app_name` | Nome do jogo |
| `install_dir` | Pasta onde o jogo está instalado |

Exemplo:

```python
import os

with open(os.path.join(install_dir, "log.txt"), "a") as f:
    f.write(app_name + "\n")
```

Os scripts são executados antes de o jogo abrir. Se o seu script depende do processo do jogo, ele deve aguardar esse processo aparecer por conta própria.

## Executando

Requisitos: Windows e Python 3.9 ou superior. Não há dependências externas.

```
python st_script_manager.py
```

## Gerando o .exe

```
pip install pyinstaller
pyinstaller --onefile --noconsole --name "ST Script Manager" st_script_manager.py
```

O executável será criado na pasta `dist`.

## Dados salvos

Idioma, tema, aceitação dos termos e scripts ficam em `%APPDATA%\STScriptManager\data.json`. A ferramenta não coleta nem envia dados para a internet.

## Termos de uso

Esta ferramenta foi desenvolvida para fins de estudo e é poderosa: permite criar scripts, gerenciá-los e controlar aplicativos instalados na Steam. Apesar de o código-fonte estar disponível, **não são permitidas modificações não oficiais**, para evitar que a ferramenta seja usada de forma maliciosa. O texto completo está dentro do programa, no botão **Termos de uso**.

## Aviso

Projeto independente e não oficial, sem qualquer vínculo com a Valve Corporation ou com a Steam. Steam e Valve são marcas de seus respectivos titulares.

## Créditos

Desenvolvido por **GUILHERME** ([GuilhermeSoaresMarciel](https://github.com/GuilhermeSoaresMarciel)), fã da Steam.

---

## English

Desktop tool for Windows, written in Python, that detects the games installed on your Steam and lets you create, organize and control scripts for each one of them. Built for study purposes.

### Features

- Automatically detects Steam and every configured library, including other drives
- Lists installed games, with search by name
- Shows name, App ID, install folder, size on disk, last update and Build ID
- Create, edit and delete separate scripts for each game
- A checkbox on each script defines whether it should run or not
- Button to launch the game through the tool, running only the active scripts first
- Three themes: Light, Dark and Dracula
- Interface in Português and English, chosen when the program opens
- Terms of use, app description and credits inside the tool itself

### How to use

1. Open the program and choose the language.
2. Read and accept the terms of use (first run only).
3. Select a game from the list on the left.
4. Click **New script**, write your code and click **Save script**.
5. Check or uncheck each script's checkbox to enable or disable it.
6. Click **Launch game with active scripts**.

### Scripts

Scripts are written in Python and each one runs in its own thread without freezing the interface. Three ready-made variables are available inside a script:

| Variable | Description |
|---|---|
| `app_id` | The game's identifier on Steam |
| `app_name` | The game's name |
| `install_dir` | Folder where the game is installed |

Example:

```python
import os

with open(os.path.join(install_dir, "log.txt"), "a") as f:
    f.write(app_name + "\n")
```

Scripts run before the game opens. If your script depends on the game process, it must wait for that process to appear on its own.

### Running

Requirements: Windows and Python 3.9 or newer. No external dependencies.

```
python st_script_manager.py
```

### Building the .exe

```
pip install pyinstaller
pyinstaller --onefile --noconsole --name "ST Script Manager" st_script_manager.py
```

The executable will be created in the `dist` folder.

### Saved data

Language, theme, terms acceptance and scripts are stored in `%APPDATA%\STScriptManager\data.json`. The tool does not collect or send any data to the internet.

### Terms of use

This tool was developed for study purposes and is powerful: it allows creating scripts, managing them and controlling applications installed on Steam. Although the source code is available, **unofficial modifications are not permitted**, to prevent the tool from being used maliciously. The full text is inside the program, under the **Terms of use** button.

### Disclaimer

Independent, unofficial project with no link to Valve Corporation or Steam. Steam and Valve are trademarks of their respective owners.

### Credits

Developed by **GUILHERME** ([GuilhermeSoaresMarciel](https://github.com/GuilhermeSoaresMarciel)), a Steam fan.
