# Gourmet da Avenida

Aplicação desenvolvida em estilo **E-commerce** para facilitar o gerenciamento e interação do cliente em um negócio local.
O sistema conta com três módulos principais: **Produto, Pedido e Usuário**, além de uma área administrativa para gerenciar cadastros e operações. 

# Funcionalidades (não administrativas)

## Módulo Produto 

## Módulo Pedido

## Módulo Usuário 

# Modelagem Relacional
As tabelas não destacadas são criadas automaticamente pelo Django.

![Título](/img/relational-model.png)

# Modelagem Dimensional

## Instalação
1. Clone o repositório:
```
https://github.com/matconi/gourmet-avenida.git
```
2. Certifique-se que o Docker esteja instalado e pronto para funcionamento.
3. Abra o projeto no editor de sua preferência.
4. Configure as variáveis de ambiente, cujo exemplo se encontra na pasta env_files, ajustando-as ao seu projeto.
5. Execute o comando `docker compose up --build` se for a primeira vez que estiver subindo o projeto ou se os arquivos de configuração/variáveis de ambiente forem modificados.
6. Caso contrário, execute `docker compose up`.

## Contribuições
Contribuições são bem-vindas para aprimorar o sistema. Sinta-se à vontade para abrir issues e pull requests para sugerir melhorias, corrigir problemas ou adicionar novas funcionalidades.