import os
import re
import sys
import json
import threading
import traceback
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    import winreg
except ImportError:
    winreg = None

APP_VERSION = "1.0.0"
GITHUB_URL = "https://github.com/GuilhermeSoaresMarciel"
DEVELOPER_NAME = "GUILHERME"
DEVELOPER_USER = "GuilhermeSoaresMarciel"

DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "STScriptManager")
DATA_FILE = os.path.join(DATA_DIR, "data.json")

THEMES = {
    "light": {
        "bg": "#f3f3f3",
        "fg": "#1e1e1e",
        "field": "#ffffff",
        "sel": "#0078d4",
        "selfg": "#ffffff",
        "btn": "#e1e1e1",
        "border": "#bdbdbd",
        "accent": "#0b5cad",
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#e6e6e6",
        "field": "#2b2b2b",
        "sel": "#3a7bd5",
        "selfg": "#ffffff",
        "btn": "#333333",
        "border": "#555555",
        "accent": "#6cb6ff",
    },
    "dracula": {
        "bg": "#282a36",
        "fg": "#f8f8f2",
        "field": "#44475a",
        "sel": "#bd93f9",
        "selfg": "#282a36",
        "btn": "#44475a",
        "border": "#6272a4",
        "accent": "#ff79c6",
    },
}

TEXTS = {
    "pt": {
        "title": "ST Script Manager",
        "search": "Buscar jogo",
        "games": "Jogos instalados",
        "info": "Informações",
        "name": "Nome",
        "appid": "App ID",
        "path": "Pasta de instalação",
        "size": "Tamanho em disco",
        "updated": "Última atualização",
        "build": "Build ID",
        "scripts": "Scripts",
        "new": "Novo script",
        "delete": "Excluir",
        "save": "Salvar script",
        "script_name": "Nome do script",
        "launch": "Abrir jogo com scripts ativos",
        "select_game": "Selecione um jogo na lista",
        "no_steam": "Steam não encontrada neste computador.",
        "script_default": "Script",
        "confirm_delete": "Excluir este script?",
        "error": "Erro",
        "script_error": "Erro no script",
        "unknown": "Desconhecido",
        "none": "Nenhum jogo encontrado",
        "theme": "Tema",
        "theme_light": "Claro",
        "theme_dark": "Escuro",
        "theme_dracula": "Dracula",
        "about_btn": "Sobre",
        "terms_btn": "Termos de uso",
        "credits_btn": "Créditos",
        "tab_about": "Sobre o app",
        "tab_terms": "Termos de uso",
        "tab_credits": "Créditos",
        "info_title": "Sobre o ST Script Manager",
        "terms_title": "Termos de uso",
        "accept": "Li e aceito os termos de uso",
        "continue": "Continuar",
        "exit": "Sair",
        "developed_by": "Desenvolvido por",
        "open_github": "Abrir GitHub",
        "version": "Versão",
    },
    "en": {
        "title": "ST Script Manager",
        "search": "Search game",
        "games": "Installed games",
        "info": "Information",
        "name": "Name",
        "appid": "App ID",
        "path": "Install folder",
        "size": "Size on disk",
        "updated": "Last updated",
        "build": "Build ID",
        "scripts": "Scripts",
        "new": "New script",
        "delete": "Delete",
        "save": "Save script",
        "script_name": "Script name",
        "launch": "Launch game with active scripts",
        "select_game": "Select a game from the list",
        "no_steam": "Steam was not found on this computer.",
        "script_default": "Script",
        "confirm_delete": "Delete this script?",
        "error": "Error",
        "script_error": "Script error",
        "unknown": "Unknown",
        "none": "No games found",
        "theme": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_dracula": "Dracula",
        "about_btn": "About",
        "terms_btn": "Terms of use",
        "credits_btn": "Credits",
        "tab_about": "About the app",
        "tab_terms": "Terms of use",
        "tab_credits": "Credits",
        "info_title": "About ST Script Manager",
        "terms_title": "Terms of use",
        "accept": "I have read and accept the terms of use",
        "continue": "Continue",
        "exit": "Exit",
        "developed_by": "Developed by",
        "open_github": "Open GitHub",
        "version": "Version",
    },
}

LONG_TEXTS = {
    "pt": {
        "about": """ST SCRIPT MANAGER

O ST Script Manager é uma ferramenta desktop criada para fins de estudo. Ela detecta automaticamente todos os jogos e aplicativos instalados na sua Steam, mostra informações detalhadas sobre cada um deles e permite que você crie, organize e controle scripts associados a cada aplicativo.

O QUE A FERRAMENTA FAZ

1. Detecta a instalação da Steam no computador e lê todas as bibliotecas configuradas, inclusive as que ficam em outros discos.
2. Lista os jogos e aplicativos instalados, com busca por nome.
3. Exibe para cada aplicativo o nome, o App ID, a pasta de instalação, o tamanho ocupado em disco, a data da última atualização e o Build ID.
4. Permite criar quantos scripts você quiser para cada aplicativo, editá-los, salvá-los e excluí-los.
5. Cada script possui uma caixa de seleção que define se ele deve ou não ser executado. Somente os scripts marcados como ativos são executados.
6. Abre o jogo pela própria ferramenta. No momento em que você usa o botão de abrir, todos os scripts ativos daquele aplicativo são iniciados e, em seguida, o jogo é lançado pela Steam.
7. Oferece três temas visuais: Claro, Escuro e Dracula.
8. Oferece interface em Português e em Inglês, escolhida ao abrir o programa.

COMO OS SCRIPTS FUNCIONAM

Os scripts são escritos em Python. Cada script é executado em uma thread própria, de modo que um script demorado ou com repetição não trava a interface nem impede a abertura do jogo. Dentro de cada script você tem acesso a três variáveis prontas:

app_id: o identificador do aplicativo na Steam.
app_name: o nome do aplicativo.
install_dir: a pasta onde o aplicativo está instalado.

Se um script gerar um erro, a ferramenta mostra uma janela com os detalhes para que você possa corrigi-lo. Os scripts são executados antes da abertura do jogo; caso o seu script dependa do processo do jogo, ele deve aguardar o processo aparecer por conta própria.

ONDE FICAM OS DADOS

Todas as configurações, o idioma, o tema, a aceitação dos termos e os scripts ficam salvos localmente, no arquivo data.json dentro da pasta STScriptManager em AppData do seu usuário. A ferramenta não envia nenhuma informação para a internet.

POR QUE ESTA FERRAMENTA EXISTE

O projeto nasceu do estudo de como a Steam organiza seus aplicativos e de como é possível automatizar tarefas ao redor deles de forma organizada e segura. O desenvolvedor é fã da Steam e criou esta ferramenta como um projeto de aprendizado e de admiração pela plataforma.""",
        "terms": """TERMOS DE USO

Última atualização: versão 1.0.0

Leia com atenção os termos abaixo antes de usar o ST Script Manager. Ao marcar a caixa de aceite ou ao continuar utilizando a ferramenta, você declara que leu, entendeu e concorda com todas as condições descritas aqui.

1. ACEITAÇÃO DOS TERMOS

1.1. O uso da ferramenta implica a aceitação integral destes termos.
1.2. Caso você não concorde com qualquer parte destes termos, você deve parar de usar a ferramenta imediatamente.
1.3. O desenvolvedor pode atualizar estes termos a qualquer momento. A continuidade do uso após uma atualização representa a aceitação da nova versão.

2. FINALIDADE DA FERRAMENTA

2.1. Esta ferramenta foi desenvolvida para fins de estudo e aprendizado.
2.2. Apesar de seu propósito educacional, trata-se de uma ferramenta poderosa: ela permite a criação de scripts, o gerenciamento desses scripts e o controle sobre os aplicativos instalados na Steam.
2.3. Justamente por ser poderosa, a ferramenta deve ser utilizada com responsabilidade, bom senso e respeito às regras das plataformas envolvidas.
2.4. O desenvolvedor é fã da Steam, e a ferramenta foi criada com admiração pela plataforma, sem qualquer pretensão de prejudicá-la, de substituí-la ou de contornar seus mecanismos de proteção.

3. CÓDIGO-FONTE DISPONÍVEL

3.1. O código-fonte da ferramenta está disponível publicamente para consulta, leitura e estudo.
3.2. A disponibilidade do código-fonte não significa liberdade para modificá-lo e redistribuí-lo. O código está disponível para que as pessoas possam aprender, entender como a ferramenta funciona e verificar que ela não coleta dados nem executa ações ocultas.
3.3. Você pode ler o código, estudá-lo e usá-lo como referência de aprendizado, respeitando os termos aqui descritos.

4. PROIBIÇÃO DE MODIFICAÇÕES NÃO OFICIAIS

4.1. Não é permitido modificar a ferramenta de forma não oficial.
4.2. Também não é permitido distribuir, publicar, vender ou compartilhar versões alteradas, recompiladas ou empacotadas da ferramenta como se fossem oficiais ou como se tivessem a aprovação do desenvolvedor.
4.3. Esta restrição existe para evitar que a ferramenta seja adulterada e usada de forma maliciosa, por exemplo com a inclusão de código que roube dados, instale programas indesejados, comprometa contas ou prejudique outras pessoas.
4.4. Somente as versões publicadas pelo desenvolvedor em seus canais oficiais, especialmente o seu perfil no GitHub, devem ser consideradas legítimas e seguras.
4.5. Sugestões de melhoria, relatos de problemas e contribuições podem ser enviados ao desenvolvedor pelo GitHub, e poderão ser incorporados à versão oficial a critério exclusivo dele.

5. USOS PERMITIDOS

5.1. Estudar o funcionamento da ferramenta e do seu código-fonte.
5.2. Gerenciar e organizar scripts pessoais para os seus próprios aplicativos instalados na Steam.
5.3. Automatizar tarefas legítimas relacionadas aos seus jogos, como organizar arquivos, fazer cópias de segurança de saves, registrar informações de uso, abrir programas auxiliares e tarefas semelhantes.
5.4. Utilizar a ferramenta em ambiente pessoal, educacional e de testes.

6. USOS PROIBIDOS

6.1. É proibido utilizar a ferramenta, ou qualquer script criado com ela, para:
a) criar, executar, distribuir ou ocultar vírus, malware, ransomware, spyware, keyloggers ou qualquer código malicioso;
b) obter vantagem desleal em jogos online, como trapaças, hacks e automações que prejudiquem outros jogadores;
c) burlar, desativar ou enganar sistemas anticheat, como o VAC, ou qualquer outro mecanismo de proteção de jogos ou da Steam;
d) acessar, copiar, alterar ou apagar dados, contas ou arquivos de terceiros sem autorização;
e) violar direitos autorais, licenças de software ou o Acordo de Assinante da Steam;
f) violar os termos de serviço de qualquer jogo, plataforma ou serviço de terceiros;
g) praticar fraude, assédio, perseguição ou qualquer atividade ilegal.
6.2. O uso proibido é de inteira responsabilidade de quem o praticar.

7. RESPONSABILIDADE SOBRE OS SCRIPTS

7.1. Os scripts são escritos e controlados por você. A ferramenta apenas os armazena e os executa conforme a sua escolha.
7.2. Você é o único responsável pelo conteúdo de cada script e por todas as consequências da sua execução.
7.3. Scripts podem executar ações poderosas no seu computador, como ler, criar, alterar e apagar arquivos e iniciar processos. Nunca execute scripts de origem desconhecida ou que você não entenda completamente.
7.4. Faça cópias de segurança dos seus dados importantes antes de executar scripts novos ou testados pela primeira vez.
7.5. Scripts recebidos de terceiros devem ser revisados com atenção antes de serem ativados.

8. DADOS E PRIVACIDADE

8.1. A ferramenta não coleta, não transmite e não vende dados pessoais.
8.2. A ferramenta não se conecta à internet por conta própria. As únicas ações externas são abrir o jogo por meio do protocolo da Steam e abrir o perfil do desenvolvedor no GitHub, quando você clica no botão correspondente.
8.3. As configurações e os scripts ficam gravados apenas no seu computador, na pasta do aplicativo dentro de AppData.
8.4. Ao remover a pasta STScriptManager de AppData, todos os dados da ferramenta são apagados.

9. MARCAS E INDEPENDÊNCIA

9.1. Steam e Valve são marcas de seus respectivos titulares.
9.2. Esta ferramenta é um projeto independente, não oficial, e não possui qualquer vínculo, patrocínio, aprovação ou afiliação com a Valve Corporation ou com a Steam.
9.3. Os nomes de jogos e aplicativos exibidos pertencem aos seus respectivos proprietários.

10. AUSÊNCIA DE GARANTIAS

10.1. A ferramenta é fornecida no estado em que se encontra, sem garantias de qualquer tipo, expressas ou implícitas.
10.2. Não há garantia de funcionamento ininterrupto, de ausência de erros, de compatibilidade com todas as versões da Steam ou do sistema operacional, nem de adequação a um objetivo específico.
10.3. A Steam pode alterar a forma como organiza seus arquivos a qualquer momento, o que pode afetar o funcionamento da ferramenta.

11. LIMITAÇÃO DE RESPONSABILIDADE

11.1. Na máxima extensão permitida pela lei aplicável, o desenvolvedor não se responsabiliza por danos diretos ou indiretos decorrentes do uso da ferramenta, incluindo perda de dados, falhas no sistema, perda de progresso em jogos, bloqueio ou suspensão de contas e prejuízos de qualquer natureza.
11.2. O desenvolvedor não se responsabiliza por scripts criados por você ou por terceiros, nem por versões da ferramenta modificadas de forma não oficial.
11.3. Penalidades aplicadas por jogos, serviços ou pela própria Steam em razão do uso indevido da ferramenta são de responsabilidade exclusiva do usuário.

12. ATUALIZAÇÕES E DISPONIBILIDADE

12.1. O desenvolvedor pode atualizar, alterar, suspender ou descontinuar a ferramenta a qualquer momento, sem aviso prévio.
12.2. Não há obrigação de oferecer suporte, correções ou novas funcionalidades.

13. ENCERRAMENTO

13.1. O direito de uso da ferramenta pode ser encerrado caso estes termos sejam descumpridos.
13.2. Em caso de descumprimento, você deve interromper o uso e excluir todas as cópias da ferramenta que estejam em seu poder.
13.3. As disposições sobre responsabilidade, ausência de garantias e propriedade permanecem válidas mesmo após o encerramento.

14. PROPRIEDADE INTELECTUAL

14.1. A autoria da ferramenta pertence ao desenvolvedor GUILHERME (GuilhermeSoaresMarciel).
14.2. É proibido remover ou alterar os créditos de autoria da ferramenta.

15. CONTATO

15.1. Dúvidas, sugestões e relatos de problemas podem ser enviados ao desenvolvedor por meio do seu perfil no GitHub: https://github.com/GuilhermeSoaresMarciel

Ao continuar, você confirma que leu e concorda com estes termos e que utilizará a ferramenta de forma ética, legal e responsável.""",
        "credits": """CRÉDITOS

Desenvolvedor: GUILHERME (GuilhermeSoaresMarciel)
GitHub: https://github.com/GuilhermeSoaresMarciel

O ST Script Manager foi criado por GUILHERME como um projeto de estudo e como uma homenagem à Steam, plataforma da qual ele é fã.

Agradecimentos à comunidade de desenvolvedores e jogadores que torna o universo dos jogos para computador tão criativo.

Steam e Valve são marcas de seus respectivos titulares. Este projeto é independente e não possui vínculo oficial com a Valve Corporation.

Para acompanhar o projeto, sugerir melhorias ou relatar problemas, visite o perfil do desenvolvedor no GitHub.""",
    },
    "en": {
        "about": """ST SCRIPT MANAGER

ST Script Manager is a desktop tool created for study purposes. It automatically detects every game and application installed on your Steam, shows detailed information about each one, and lets you create, organize and control scripts associated with each application.

WHAT THE TOOL DOES

1. Detects the Steam installation on the computer and reads every configured library, including the ones located on other drives.
2. Lists installed games and applications, with search by name.
3. Shows for each application its name, App ID, install folder, size on disk, last update date and Build ID.
4. Lets you create as many scripts as you want for each application, edit them, save them and delete them.
5. Each script has a checkbox that defines whether it should run or not. Only scripts marked as active are executed.
6. Launches the game through the tool itself. When you use the launch button, all active scripts for that application are started and then the game is launched through Steam.
7. Offers three visual themes: Light, Dark and Dracula.
8. Offers an interface in Portuguese and English, chosen when the program opens.

HOW SCRIPTS WORK

Scripts are written in Python. Each script runs in its own thread, so a long or looping script does not freeze the interface or prevent the game from opening. Inside each script you have access to three ready-made variables:

app_id: the application identifier on Steam.
app_name: the name of the application.
install_dir: the folder where the application is installed.

If a script raises an error, the tool shows a window with the details so you can fix it. Scripts run before the game opens; if your script depends on the game process, it must wait for the process to appear on its own.

WHERE DATA IS STORED

All settings, language, theme, terms acceptance and scripts are saved locally in the data.json file inside the STScriptManager folder in your user's AppData. The tool does not send any information to the internet.

WHY THIS TOOL EXISTS

The project was born from studying how Steam organizes its applications and how it is possible to automate tasks around them in an organized and safe way. The developer is a Steam fan and created this tool as a learning project and out of admiration for the platform.""",
        "terms": """TERMS OF USE

Last updated: version 1.0.0

Please read the terms below carefully before using ST Script Manager. By checking the acceptance box or by continuing to use the tool, you declare that you have read, understood and agree with all the conditions described here.

1. ACCEPTANCE OF THE TERMS

1.1. Using the tool means full acceptance of these terms.
1.2. If you do not agree with any part of these terms, you must stop using the tool immediately.
1.3. The developer may update these terms at any time. Continuing to use the tool after an update represents acceptance of the new version.

2. PURPOSE OF THE TOOL

2.1. This tool was developed for study and learning purposes.
2.2. Despite its educational purpose, it is a powerful tool: it allows the creation of scripts, the management of those scripts and control over the applications installed on Steam.
2.3. Precisely because it is powerful, the tool must be used with responsibility, good judgment and respect for the rules of the platforms involved.
2.4. The developer is a fan of Steam, and the tool was created out of admiration for the platform, with no intention of harming it, replacing it or bypassing its protection mechanisms.

3. SOURCE CODE AVAILABILITY

3.1. The source code of the tool is publicly available for viewing, reading and study.
3.2. The availability of the source code does not mean freedom to modify and redistribute it. The code is available so that people can learn, understand how the tool works and verify that it does not collect data or perform hidden actions.
3.3. You may read the code, study it and use it as a learning reference, respecting the terms described here.

4. PROHIBITION OF UNOFFICIAL MODIFICATIONS

4.1. Unofficial modifications to the tool are not permitted.
4.2. It is also not permitted to distribute, publish, sell or share altered, recompiled or repackaged versions of the tool as if they were official or approved by the developer.
4.3. This restriction exists to prevent the tool from being tampered with and used maliciously, for example by including code that steals data, installs unwanted programs, compromises accounts or harms other people.
4.4. Only versions published by the developer on his official channels, especially his GitHub profile, should be considered legitimate and safe.
4.5. Suggestions for improvement, problem reports and contributions may be sent to the developer through GitHub, and may be incorporated into the official version at his sole discretion.

5. PERMITTED USES

5.1. Studying how the tool and its source code work.
5.2. Managing and organizing personal scripts for your own applications installed on Steam.
5.3. Automating legitimate tasks related to your games, such as organizing files, backing up saves, logging usage information, opening helper programs and similar tasks.
5.4. Using the tool in personal, educational and testing environments.

6. PROHIBITED USES

6.1. It is forbidden to use the tool, or any script created with it, to:
a) create, run, distribute or hide viruses, malware, ransomware, spyware, keyloggers or any malicious code;
b) gain an unfair advantage in online games, such as cheats, hacks and automation that harm other players;
c) bypass, disable or deceive anti-cheat systems, such as VAC, or any other protection mechanism of games or Steam;
d) access, copy, change or delete data, accounts or files of third parties without authorization;
e) violate copyrights, software licenses or the Steam Subscriber Agreement;
f) violate the terms of service of any game, platform or third-party service;
g) engage in fraud, harassment, stalking or any illegal activity.
6.2. Prohibited use is the sole responsibility of whoever commits it.

7. RESPONSIBILITY FOR SCRIPTS

7.1. Scripts are written and controlled by you. The tool only stores them and runs them according to your choice.
7.2. You are solely responsible for the content of each script and for all consequences of its execution.
7.3. Scripts can perform powerful actions on your computer, such as reading, creating, changing and deleting files and starting processes. Never run scripts from unknown sources or that you do not fully understand.
7.4. Back up your important data before running new or first-time scripts.
7.5. Scripts received from third parties must be carefully reviewed before being activated.

8. DATA AND PRIVACY

8.1. The tool does not collect, transmit or sell personal data.
8.2. The tool does not connect to the internet on its own. The only external actions are launching the game through the Steam protocol and opening the developer's GitHub profile when you click the corresponding button.
8.3. Settings and scripts are stored only on your computer, in the application folder inside AppData.
8.4. By removing the STScriptManager folder from AppData, all of the tool's data is erased.

9. TRADEMARKS AND INDEPENDENCE

9.1. Steam and Valve are trademarks of their respective owners.
9.2. This tool is an independent, unofficial project and has no link, sponsorship, approval or affiliation with Valve Corporation or Steam.
9.3. The names of games and applications displayed belong to their respective owners.

10. NO WARRANTIES

10.1. The tool is provided as is, without warranties of any kind, express or implied.
10.2. There is no guarantee of uninterrupted operation, absence of errors, compatibility with all versions of Steam or the operating system, or fitness for a particular purpose.
10.3. Steam may change the way it organizes its files at any time, which may affect the operation of the tool.

11. LIMITATION OF LIABILITY

11.1. To the maximum extent permitted by applicable law, the developer is not liable for direct or indirect damages arising from the use of the tool, including data loss, system failures, loss of game progress, account blocks or suspensions and losses of any nature.
11.2. The developer is not responsible for scripts created by you or by third parties, nor for versions of the tool modified in an unofficial way.
11.3. Penalties applied by games, services or Steam itself due to misuse of the tool are the sole responsibility of the user.

12. UPDATES AND AVAILABILITY

12.1. The developer may update, change, suspend or discontinue the tool at any time without prior notice.
12.2. There is no obligation to provide support, fixes or new features.

13. TERMINATION

13.1. The right to use the tool may be terminated if these terms are violated.
13.2. In case of violation, you must stop using the tool and delete all copies in your possession.
13.3. The provisions on liability, no warranties and ownership remain valid even after termination.

14. INTELLECTUAL PROPERTY

14.1. Authorship of the tool belongs to the developer GUILHERME (GuilhermeSoaresMarciel).
14.2. Removing or altering the authorship credits of the tool is prohibited.

15. CONTACT

15.1. Questions, suggestions and problem reports may be sent to the developer through his GitHub profile: https://github.com/GuilhermeSoaresMarciel

By continuing, you confirm that you have read and agree with these terms and that you will use the tool ethically, legally and responsibly.""",
        "credits": """CREDITS

Developer: GUILHERME (GuilhermeSoaresMarciel)
GitHub: https://github.com/GuilhermeSoaresMarciel

ST Script Manager was created by GUILHERME as a study project and as a tribute to Steam, a platform he is a fan of.

Thanks to the community of developers and players that makes the world of PC gaming so creative.

Steam and Valve are trademarks of their respective owners. This project is independent and has no official link with Valve Corporation.

To follow the project, suggest improvements or report problems, visit the developer's GitHub profile.""",
    },
}


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data.setdefault("language", "en")
    data.setdefault("theme", "dark")
    data.setdefault("terms_accepted", False)
    data.setdefault("scripts", {})
    if data["theme"] not in THEMES:
        data["theme"] = "dark"
    return data


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_steam_path():
    if winreg:
        for hive, key, value in (
            (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
        ):
            try:
                with winreg.OpenKey(hive, key) as k:
                    path = winreg.QueryValueEx(k, value)[0]
                    if os.path.isdir(path):
                        return os.path.normpath(path)
            except OSError:
                continue
    for path in (
        r"C:\Program Files (x86)\Steam",
        r"C:\Program Files\Steam",
        os.path.expanduser("~/.steam/steam"),
        os.path.expanduser("~/.local/share/Steam"),
    ):
        if os.path.isdir(path):
            return os.path.normpath(path)
    return None


def get_library_folders(steam_path):
    libraries = [os.path.join(steam_path, "steamapps")]
    vdf = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
    try:
        with open(vdf, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for match in re.findall(r'"path"\s+"([^"]+)"', content):
            lib = os.path.join(match.replace("\\\\", "\\"), "steamapps")
            if os.path.isdir(lib) and os.path.normpath(lib) not in [os.path.normpath(x) for x in libraries]:
                libraries.append(lib)
    except OSError:
        pass
    return libraries


def parse_manifest(path, library):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return None
    fields = {}
    for key, value in re.findall(r'"(\w+)"\s+"([^"]*)"', content):
        fields.setdefault(key.lower(), value)
    appid = fields.get("appid")
    name = fields.get("name")
    if not appid or not name:
        return None
    if appid == "228980" or name.startswith(("Proton", "Steam Linux Runtime", "Steamworks Common")):
        return None
    installdir = fields.get("installdir", "")
    return {
        "appid": appid,
        "name": name,
        "dir": os.path.join(library, "common", installdir),
        "size": int(fields.get("sizeondisk", "0") or 0),
        "updated": int(fields.get("lastupdated", "0") or 0),
        "build": fields.get("buildid", ""),
    }


def get_games(steam_path):
    games = {}
    for library in get_library_folders(steam_path):
        try:
            files = os.listdir(library)
        except OSError:
            continue
        for file in files:
            if file.startswith("appmanifest_") and file.endswith(".acf"):
                game = parse_manifest(os.path.join(library, file), library)
                if game:
                    games[game["appid"]] = game
    return sorted(games.values(), key=lambda g: g["name"].lower())


def format_size(size):
    gb = size / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.2f} GB"
    return f"{size / (1024 ** 2):.1f} MB"


class App:
    def __init__(self):
        self.data = load_data()
        self.root = tk.Tk()
        self.root.title("ST Script Manager")
        self.lang = self.data["language"] if self.data["language"] in TEXTS else "en"
        self.games = []
        self.visible = []
        self.game = None
        self.script_index = None
        self.errors = []
        self.info_win = None
        self.th = THEMES[self.data["theme"]]
        self.apply_theme()
        self.language_screen()
        self.root.mainloop()

    def t(self, key):
        return TEXTS[self.lang][key]

    def clear(self):
        if self.info_win is not None and self.info_win.winfo_exists():
            self.info_win.destroy()
        self.info_win = None
        for child in self.root.winfo_children():
            child.destroy()

    def apply_theme(self):
        th = THEMES[self.data["theme"]]
        self.th = th
        style = ttk.Style(self.root)
        style.theme_use("clam")
        self.root.configure(bg=th["bg"])
        style.configure(
            ".",
            background=th["bg"],
            foreground=th["fg"],
            fieldbackground=th["field"],
            bordercolor=th["border"],
            lightcolor=th["border"],
            darkcolor=th["border"],
            troughcolor=th["bg"],
            focuscolor=th["bg"],
            insertcolor=th["fg"],
        )
        style.configure("TFrame", background=th["bg"])
        style.configure("TLabel", background=th["bg"], foreground=th["fg"])
        style.configure("TButton", background=th["btn"], foreground=th["fg"], bordercolor=th["border"], padding=5)
        style.map(
            "TButton",
            background=[("active", th["sel"]), ("pressed", th["sel"]), ("disabled", th["bg"])],
            foreground=[("active", th["selfg"]), ("pressed", th["selfg"]), ("disabled", th["border"])],
        )
        style.configure("TCheckbutton", background=th["bg"], foreground=th["fg"], indicatorbackground=th["field"], indicatorforeground=th["selfg"])
        style.map(
            "TCheckbutton",
            background=[("active", th["bg"])],
            indicatorcolor=[("selected", th["sel"]), ("!selected", th["field"])],
        )
        style.configure("TEntry", fieldbackground=th["field"], foreground=th["fg"], insertcolor=th["fg"], bordercolor=th["border"])
        style.configure(
            "TCombobox",
            fieldbackground=th["field"],
            background=th["btn"],
            foreground=th["fg"],
            arrowcolor=th["fg"],
            selectbackground=th["field"],
            selectforeground=th["fg"],
            bordercolor=th["border"],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", th["field"])],
            foreground=[("readonly", th["fg"])],
            selectbackground=[("readonly", th["field"])],
            selectforeground=[("readonly", th["fg"])],
        )
        style.configure("TScrollbar", background=th["btn"], troughcolor=th["bg"], arrowcolor=th["fg"], bordercolor=th["border"])
        style.map("TScrollbar", background=[("active", th["sel"])])
        style.configure("TLabelframe", background=th["bg"], bordercolor=th["border"])
        style.configure("TLabelframe.Label", background=th["bg"], foreground=th["fg"])
        style.configure("TNotebook", background=th["bg"], bordercolor=th["border"])
        style.configure("TNotebook.Tab", background=th["btn"], foreground=th["fg"], padding=(12, 6))
        style.map(
            "TNotebook.Tab",
            background=[("selected", th["sel"])],
            foreground=[("selected", th["selfg"])],
        )
        self.root.option_add("*TCombobox*Listbox.background", th["field"])
        self.root.option_add("*TCombobox*Listbox.foreground", th["fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", th["sel"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", th["selfg"])

    def language_screen(self):
        self.clear()
        self.root.geometry("380x260")
        self.root.resizable(False, False)
        frame = ttk.Frame(self.root, padding=24)
        frame.pack(expand=True, fill="both")
        ttk.Label(frame, text="Escolha o idioma / Choose language", font=("Segoe UI", 11, "bold")).pack(pady=(0, 18))
        ttk.Button(frame, text="Português", command=lambda: self.set_language("pt")).pack(fill="x", pady=4, ipady=6)
        ttk.Button(frame, text="English", command=lambda: self.set_language("en")).pack(fill="x", pady=4, ipady=6)
        link = tk.Label(
            frame,
            text=f"{DEVELOPER_NAME} - github.com/{DEVELOPER_USER}",
            bg=self.th["bg"],
            fg=self.th["accent"],
            cursor="hand2",
            font=("Segoe UI", 9, "underline"),
        )
        link.pack(side="bottom", pady=(14, 0))
        link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))

    def set_language(self, lang):
        self.lang = lang
        self.data["language"] = lang
        save_data(self.data)
        if self.data["terms_accepted"]:
            self.main_screen()
        else:
            self.terms_screen()

    def make_text(self, parent, content, height=None):
        frame = ttk.Frame(parent)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        options = {}
        if height:
            options["height"] = height
        text = tk.Text(
            frame,
            wrap="word",
            bg=self.th["field"],
            fg=self.th["fg"],
            insertbackground=self.th["fg"],
            selectbackground=self.th["sel"],
            selectforeground=self.th["selfg"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.th["border"],
            highlightcolor=self.th["border"],
            padx=12,
            pady=10,
            font=("Segoe UI", 10),
            **options,
        )
        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        text.insert("1.0", content)
        text.configure(state="disabled")
        return frame

    def terms_screen(self):
        self.clear()
        self.root.geometry("820x640")
        self.root.minsize(640, 480)
        self.root.resizable(True, True)
        self.root.title(self.t("terms_title"))
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        ttk.Label(frame, text=self.t("terms_title"), font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.make_text(frame, LONG_TEXTS[self.lang]["terms"]).grid(row=1, column=0, sticky="nsew")
        accept_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text=self.t("accept"), variable=accept_var).grid(row=2, column=0, sticky="w", pady=(10, 6))
        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, sticky="e")
        continue_button = ttk.Button(buttons, text=self.t("continue"), state="disabled", command=self.accept_terms)
        continue_button.pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text=self.t("exit"), command=self.root.destroy).pack(side="right")
        accept_var.trace_add("write", lambda *a: continue_button.configure(state="normal" if accept_var.get() else "disabled"))

    def accept_terms(self):
        self.data["terms_accepted"] = True
        save_data(self.data)
        self.main_screen()

    def open_info(self, tab_index=0):
        if self.info_win is not None and self.info_win.winfo_exists():
            self.info_win.destroy()
        win = tk.Toplevel(self.root)
        self.info_win = win
        win.title(self.t("info_title"))
        win.geometry("780x600")
        win.minsize(560, 420)
        win.configure(bg=self.th["bg"])
        win.transient(self.root)
        notebook = ttk.Notebook(win)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        about_tab = ttk.Frame(notebook, padding=8)
        about_tab.columnconfigure(0, weight=1)
        about_tab.rowconfigure(1, weight=1)
        ttk.Label(about_tab, text=f"{self.t('title')}  -  {self.t('version')} {APP_VERSION}", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.make_text(about_tab, LONG_TEXTS[self.lang]["about"]).grid(row=1, column=0, sticky="nsew")
        notebook.add(about_tab, text=self.t("tab_about"))

        terms_tab = ttk.Frame(notebook, padding=8)
        terms_tab.columnconfigure(0, weight=1)
        terms_tab.rowconfigure(0, weight=1)
        self.make_text(terms_tab, LONG_TEXTS[self.lang]["terms"]).grid(row=0, column=0, sticky="nsew")
        notebook.add(terms_tab, text=self.t("tab_terms"))

        credits_tab = ttk.Frame(notebook, padding=8)
        credits_tab.columnconfigure(0, weight=1)
        credits_tab.rowconfigure(0, weight=1)
        self.make_text(credits_tab, LONG_TEXTS[self.lang]["credits"]).grid(row=0, column=0, sticky="nsew")
        link_row = ttk.Frame(credits_tab)
        link_row.grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(link_row, text=self.t("open_github"), command=lambda: webbrowser.open(GITHUB_URL)).pack(side="left")
        notebook.add(credits_tab, text=self.t("tab_credits"))

        notebook.select(tab_index)

    def theme_labels(self):
        return [(key, self.t(f"theme_{key}")) for key in ("light", "dark", "dracula")]

    def on_theme_change(self, event=None):
        labels = self.theme_labels()
        index = self.theme_box.current()
        if index < 0:
            return
        self.data["theme"] = labels[index][0]
        save_data(self.data)
        previous = self.game["appid"] if self.game else None
        self.apply_theme()
        self.main_screen()
        if previous:
            self.reselect_game(previous)

    def reselect_game(self, appid):
        for i, g in enumerate(self.visible):
            if g["appid"] == appid:
                self.listbox.selection_clear(0, "end")
                self.listbox.selection_set(i)
                self.listbox.see(i)
                self.game = g
                self.show_info()
                self.refresh_scripts()
                return

    def main_screen(self):
        self.clear()
        self.game = None
        self.script_index = None
        self.root.title(self.t("title"))
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.resizable(True, True)
        th = self.th
        steam = find_steam_path()
        if not steam:
            messagebox.showerror(self.t("error"), self.t("no_steam"))
            self.games = []
        else:
            self.games = get_games(steam)

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        top = ttk.Frame(self.root, padding=(10, 8))
        top.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(top, text=self.t("title"), font=("Segoe UI", 13, "bold")).pack(side="left")
        ttk.Button(top, text=self.t("credits_btn"), command=lambda: self.open_info(2)).pack(side="right", padx=(6, 0))
        ttk.Button(top, text=self.t("terms_btn"), command=lambda: self.open_info(1)).pack(side="right", padx=(6, 0))
        ttk.Button(top, text=self.t("about_btn"), command=lambda: self.open_info(0)).pack(side="right", padx=(6, 0))
        labels = self.theme_labels()
        self.theme_box = ttk.Combobox(top, state="readonly", width=10, values=[label for _, label in labels])
        self.theme_box.current([key for key, _ in labels].index(self.data["theme"]))
        self.theme_box.bind("<<ComboboxSelected>>", self.on_theme_change)
        self.theme_box.pack(side="right", padx=(6, 0))
        ttk.Label(top, text=self.t("theme") + ":").pack(side="right")

        left = ttk.Frame(self.root, padding=8)
        left.grid(row=1, column=0, sticky="ns")
        ttk.Label(left, text=self.t("games"), font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.fill_games())
        ttk.Entry(left, textvariable=self.search_var).pack(fill="x", pady=6)
        list_frame = ttk.Frame(left)
        list_frame.pack(fill="both", expand=True)
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side="right", fill="y")
        self.listbox = tk.Listbox(
            list_frame,
            width=34,
            activestyle="none",
            exportselection=False,
            yscrollcommand=scroll.set,
            bg=th["field"],
            fg=th["fg"],
            selectbackground=th["sel"],
            selectforeground=th["selfg"],
            highlightthickness=1,
            highlightbackground=th["border"],
            highlightcolor=th["border"],
            relief="flat",
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_game)

        right = ttk.Frame(self.root, padding=8)
        right.grid(row=1, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(2, weight=1)

        self.info_frame = ttk.LabelFrame(right, text=self.t("info"), padding=10)
        self.info_frame.grid(row=0, column=0, sticky="ew")
        self.info_frame.columnconfigure(1, weight=1)
        self.info_labels = {}
        for i, key in enumerate(("name", "appid", "path", "size", "updated", "build")):
            ttk.Label(self.info_frame, text=self.t(key) + ":", font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="nw", padx=(0, 8), pady=1)
            label = ttk.Label(self.info_frame, text="-", wraplength=560, justify="left")
            label.grid(row=i, column=1, sticky="w", pady=1)
            self.info_labels[key] = label
        self.info_labels["name"].config(text=self.t("select_game"))

        bar = ttk.Frame(right)
        bar.grid(row=1, column=0, sticky="ew", pady=(10, 4))
        ttk.Label(bar, text=self.t("scripts"), font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(bar, text=self.t("delete"), command=self.delete_script).pack(side="right", padx=(6, 0))
        ttk.Button(bar, text=self.t("new"), command=self.new_script).pack(side="right")

        body = ttk.Frame(right)
        body.grid(row=2, column=0, sticky="nsew")
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        canvas_frame = ttk.Frame(body)
        canvas_frame.grid(row=0, column=0, sticky="ns", padx=(0, 8))
        self.canvas = tk.Canvas(canvas_frame, width=230, highlightthickness=1, highlightbackground=th["border"], bg=th["bg"])
        canvas_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=canvas_scroll.set)
        canvas_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="y", expand=True)
        self.scripts_inner = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scripts_inner, anchor="nw")
        self.scripts_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        editor = ttk.Frame(body)
        editor.grid(row=0, column=1, sticky="nsew")
        editor.columnconfigure(0, weight=1)
        editor.rowconfigure(2, weight=1)
        ttk.Label(editor, text=self.t("script_name")).grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.name_var).grid(row=1, column=0, sticky="ew", pady=(2, 6))
        text_frame = ttk.Frame(editor)
        text_frame.grid(row=2, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        self.code = tk.Text(
            text_frame,
            font=("Consolas", 10),
            undo=True,
            wrap="none",
            bg=th["field"],
            fg=th["fg"],
            insertbackground=th["fg"],
            selectbackground=th["sel"],
            selectforeground=th["selfg"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=th["border"],
            highlightcolor=th["border"],
        )
        code_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.code.yview)
        self.code.configure(yscrollcommand=code_scroll.set)
        self.code.grid(row=0, column=0, sticky="nsew")
        code_scroll.grid(row=0, column=1, sticky="ns")
        ttk.Button(editor, text=self.t("save"), command=self.save_script).grid(row=3, column=0, sticky="e", pady=(6, 0))

        ttk.Button(right, text=self.t("launch"), command=self.launch).grid(row=3, column=0, sticky="ew", pady=(10, 0), ipady=8)

        footer = ttk.Frame(self.root, padding=(10, 4, 10, 8))
        footer.grid(row=2, column=0, columnspan=2, sticky="ew")
        ttk.Label(footer, text=f"{self.t('developed_by')} {DEVELOPER_NAME} ({DEVELOPER_USER})  |  {self.t('version')} {APP_VERSION}").pack(side="left")
        link = tk.Label(footer, text="github.com/" + DEVELOPER_USER, bg=th["bg"], fg=th["accent"], cursor="hand2", font=("Segoe UI", 9, "underline"))
        link.pack(side="right")
        link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))

        self.fill_games()

    def fill_games(self):
        query = self.search_var.get().strip().lower()
        self.visible = [g for g in self.games if query in g["name"].lower()]
        self.listbox.delete(0, "end")
        for g in self.visible:
            self.listbox.insert("end", g["name"])
        if not self.visible:
            self.listbox.insert("end", self.t("none"))

    def on_select_game(self, event):
        selection = self.listbox.curselection()
        if not selection or selection[0] >= len(self.visible):
            return
        self.game = self.visible[selection[0]]
        self.script_index = None
        self.name_var.set("")
        self.code.delete("1.0", "end")
        self.show_info()
        self.refresh_scripts()

    def show_info(self):
        g = self.game
        updated = datetime.fromtimestamp(g["updated"]).strftime("%Y-%m-%d %H:%M") if g["updated"] else self.t("unknown")
        values = {
            "name": g["name"],
            "appid": g["appid"],
            "path": g["dir"],
            "size": format_size(g["size"]),
            "updated": updated,
            "build": g["build"] or self.t("unknown"),
        }
        for key, value in values.items():
            self.info_labels[key].config(text=value)

    def scripts(self):
        return self.data["scripts"].setdefault(self.game["appid"], [])

    def refresh_scripts(self):
        for child in self.scripts_inner.winfo_children():
            child.destroy()
        if not self.game:
            return
        th = self.th
        for i, script in enumerate(self.scripts()):
            row = ttk.Frame(self.scripts_inner)
            row.pack(fill="x", anchor="w", pady=1)
            var = tk.BooleanVar(value=script["enabled"])
            ttk.Checkbutton(row, variable=var, command=lambda i=i, v=var: self.toggle_script(i, v)).pack(side="left")
            selected = i == self.script_index
            label = tk.Label(
                row,
                text=script["name"],
                anchor="w",
                font=("Segoe UI", 9, "bold") if selected else ("Segoe UI", 9),
                cursor="hand2",
                bg=th["bg"],
                fg=th["accent"] if selected else th["fg"],
            )
            label.pack(side="left", fill="x", expand=True)
            label.bind("<Button-1>", lambda e, i=i: self.select_script(i))

    def toggle_script(self, index, var):
        self.scripts()[index]["enabled"] = bool(var.get())
        save_data(self.data)

    def select_script(self, index):
        self.script_index = index
        script = self.scripts()[index]
        self.name_var.set(script["name"])
        self.code.delete("1.0", "end")
        self.code.insert("1.0", script["code"])
        self.refresh_scripts()

    def new_script(self):
        if not self.game:
            return
        scripts = self.scripts()
        scripts.append({"name": f"{self.t('script_default')} {len(scripts) + 1}", "code": "", "enabled": True})
        save_data(self.data)
        self.select_script(len(scripts) - 1)

    def save_script(self):
        if not self.game or self.script_index is None:
            return
        script = self.scripts()[self.script_index]
        script["name"] = self.name_var.get().strip() or f"{self.t('script_default')} {self.script_index + 1}"
        script["code"] = self.code.get("1.0", "end-1c")
        save_data(self.data)
        self.refresh_scripts()

    def delete_script(self):
        if not self.game or self.script_index is None:
            return
        if not messagebox.askyesno(self.t("title"), self.t("confirm_delete")):
            return
        del self.scripts()[self.script_index]
        self.script_index = None
        self.name_var.set("")
        self.code.delete("1.0", "end")
        save_data(self.data)
        self.refresh_scripts()

    def run_script(self, script, game):
        env = {
            "__name__": "__script__",
            "app_id": game["appid"],
            "app_name": game["name"],
            "install_dir": game["dir"],
        }
        try:
            exec(compile(script["code"], script["name"], "exec"), env)
        except Exception:
            self.errors.append((script["name"], traceback.format_exc()))
            self.root.after(0, self.show_errors)

    def show_errors(self):
        while self.errors:
            name, trace = self.errors.pop(0)
            messagebox.showerror(f"{self.t('script_error')}: {name}", trace)

    def launch(self):
        if not self.game:
            messagebox.showinfo(self.t("title"), self.t("select_game"))
            return
        self.save_script()
        for script in self.scripts():
            if script["enabled"] and script["code"].strip():
                threading.Thread(target=self.run_script, args=(dict(script), dict(self.game)), daemon=True).start()
        url = f"steam://rungameid/{self.game['appid']}"
        if sys.platform.startswith("win"):
            os.startfile(url)
        elif sys.platform == "darwin":
            os.system(f'open "{url}"')
        else:
            os.system(f'xdg-open "{url}"')


if __name__ == "__main__":
    App()
