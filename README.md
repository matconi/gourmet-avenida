# Gourmet da Avenida

Aplicação desenvolvida em estilo **E-commerce** para facilitar o gerenciamento e interação do cliente em um negócio local.
O sistema conta com três módulos principais: **Produto, Pedido e Usuário**, além de uma área administrativa para gerenciar cadastros e operações. 

# Funcionalidades (não administrativas)

## Módulo Produto 
- Visualizar produtos na vitrine.
- Visualizar produto e suas variações.
- Adicionar ao carrinho.
- Visualizar carrinho.
- Limpar ou remover um item do carrinho.

### Vatagens
- O cliente pode rapidamente encontrar os produtos e verificar sua disponibilidade.

## Módulo Pedido
- Realizar pedido(reservar).
- Visualizar pedidos.

### Vatagens
- O cliente pode reservar seus produtos e acompanhar o status do pedido, bem como visualizar o histórico de pedidos.

## Módulo Usuário
- Criar conta.
- Fazer login com a conta ou pelo Google.
- Visualizar e editar perfil.
- Visualizar contas sociais conectadas.
- Alterar senha pelo perfil ou por email.
- Visualizar favoritos.

### Vatagens
- Ao entrar pelo Google, o usuário pode acessar com um único clique sem se procupar em lembrar de senhas.
- A home traz os produtos mais vendidos, mais recentes e recomendados baseado nos mais comprados pelo cliente, além de mostrar a conta para usuários autorizados.
- Os favoritos facilitam ainda mais a encontrar os produtos mais queridos e estão acessíveis em qualquer página pela navegação principal.

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