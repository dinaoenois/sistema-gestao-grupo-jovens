# Sistema de Gestão para Grupo de Jovens

MVP acadêmico desenvolvido como proposta para a disciplina de Projeto de Software. O sistema reúne informações que podem ficar espalhadas em mensagens, planilhas e anotações, facilitando a organização de um grupo de jovens.

## Funcionalidades

- Cadastro de participantes, com contato e indicação de atividade.
- Cadastro de eventos, com data, local e participantes.
- Registro de contribuições por participante e evento, com valor, vencimento e situação (pendente ou pago).
- Organização de tarefas, com responsável, evento opcional, prazo e conclusão.
- Menu com indicadores, consulta de eventos e consulta de pagamentos com totais.

Os cadastros e alterações são feitos no painel administrativo do Django. As telas de consulta exigem uma conta de equipe (`staff`); o superusuário criado na instalação já possui esse acesso. Este MVP não realiza transações financeiras: os pagamentos são registros de controle.

## Tecnologias

Python, Django 5.2, HTML e CSS. SQLite é o banco padrão, sem instalação adicional. PostgreSQL está planejado para a implantação. A interface usa CSS local e não depende de serviços externos.

## Instalação e execução local

Pré-requisito: Python 3.12 ou 3.13 instalado. Extraia o ZIP e abra um terminal na pasta `sistema-gestao-grupo-jovens` (a que contém `manage.py`).

```sh
python -m venv .venv
```

Ative o ambiente no Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

No Windows (Prompt de Comando):

```bat
.venv\Scripts\activate.bat
```

No Linux/macOS:

```sh
source .venv/bin/activate
```

Com o ambiente ativo:

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abra http://127.0.0.1:8000/ e entre com a conta criada. O painel fica em http://127.0.0.1:8000/admin/. Cadastre participantes e eventos primeiro; depois registre pagamentos e tarefas. O projeto inicia sem dados e sem senha predefinida.

Caso o PowerShell bloqueie a ativação, use o Prompt de Comando ou execute diretamente `.venv\Scripts\python.exe` no lugar de `python` nos comandos seguintes.

## Estrutura

```text
sistema-gestao-grupo-jovens/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── config/                 # Configuração, rotas, WSGI e ASGI
└── gestao/                 # Modelos, administração, consultas e testes
    ├── migrations/         # Estrutura inicial do banco
    ├── templates/gestao/   # Menu, eventos e pagamentos
    └── static/gestao/      # CSS local
```

## Verificação

```sh
python manage.py check
python manage.py test
```

Os testes verificam acesso autenticado, consultas, totalização de pagamentos, validação de valor e proteção dos vínculos financeiros.

## PostgreSQL e implantação futura

SQLite facilita a demonstração local. Na implantação, está prevista a adoção do PostgreSQL. Será necessário instalar o driver `psycopg`, substituir a configuração `DATABASES` em `config/settings.py` pelo backend `django.db.backends.postgresql` e fornecer nome do banco, usuário, senha, host e porta por variáveis de ambiente. Depois, aplique as migrações. A troca de configuração não transfere automaticamente os dados do SQLite.

O arquivo atual contém configurações de desenvolvimento. Antes de publicar a aplicação, defina uma chave secreta própria (`DJANGO_SECRET_KEY`), `DJANGO_DEBUG=0`, os domínios permitidos (`DJANGO_ALLOWED_HOSTS`, separados por vírgula), HTTPS e a entrega de arquivos estáticos. Use um servidor de aplicação apropriado; `runserver` é para desenvolvimento. Os arquivos `.env` não são carregados automaticamente.

## Publicação no GitHub

Crie um repositório público chamado **sistema-gestao-grupo-jovens** e envie os arquivos da pasta do projeto, incluindo `.gitignore` e a migração inicial. Não envie o ambiente virtual, o banco local, senhas ou dados pessoais reais. Para a apresentação acadêmica, utilize dados fictícios. A visibilidade pública do repositório disponibiliza o código; não coloca a aplicação em execução na internet.

## Limites e próximos passos

O MVP usa o administrador do Django para operações de cadastro e não possui portal dos participantes, notificações, integração de cobrança ou relatórios avançados. Próximas melhorias previstas são formulários próprios, perfis de acesso e validação com usuários do grupo.

Documentação de referência: [Django 5.2](https://docs.djangoproject.com/en/5.2/).

## Roteiro para demonstração do MVP

1. Acesse o painel administrativo com o superusuário criado na instalação.
2. Cadastre dois participantes fictícios.
3. Crie um evento e vincule os participantes.
4. Registre um pagamento pago e outro pendente.
5. Cadastre uma tarefa com responsável e prazo.
6. Consulte o menu principal, os eventos e os totais de pagamentos.
7. Marque a tarefa como concluída e confira a atualização do indicador.
