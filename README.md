# Sistema Web em Django para Controle de Dados e Informações Internas

Este reposítório consiste num projeto de uma série de aplicações web, de interação com banco de dados, registrador de escalas, visualização e geração de métricas, entre outros,
como sistema interno de uma empresa.

## Aplicações do Projeto:

## Aplicação DBCT: 

- Dashboard com visualizações gráficas interativas de metas;
- Barra de pesquisa em tabelas para filtrar resultados;
- Possibilidade de adicionar, modificar e deletar registros de tabelas;
- Sistema de autenticação de usuário, com interações baseadas em cargo (*role-based*);
- Geração de métricas atualizadas com os dados;

## Aplicação ScaleTracker:

- Registro de Escalas numa tabela;
- Visualização da tabela com as escalas dos membros;
- Barra de pesquisa para filtrar resultados;
- Visualizações de horas ao longo da semana;
- Visualização de horas totais;

## Instalação e Configuração

1. Clone o repositório.

   '''git clone https://github.com/seu-usuario/seu-projeto.git'''

2. Caso não haja um ambiente virtual, crie um

'''cd ct-project
python -m venv venv'''

3. Ative o ambiente virtual

'''source venv/bin/activate  # ou "venv\Scripts\activate" no Windows'''

4. Instale as dependências necessárias

'''pip install -r requirements.txt'''

5. Execute o projeto 

''' python manage.py runserver '''
