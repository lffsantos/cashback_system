# Sistema de Cashback

Sistema para cadastro de revendedor e cashback


# Descrição da Solução



## Como desenvolver?

Criar/Ativar o ambiente virtual. 
- [Criando ambientes virtuais](https://docs.python.org/pt-br/3/tutorial/venv.html)


 Instale as dependências
> pip install -r requirements.txt

 Rodas as migrações
 > make migrate
 
Carregando dados
> make loaddata

Executar
> make development


## Testes:
> make test

## Descrição da API - REST:
[Documentação da API](https://documenter.getpostman.com/view/998888/T1LJm9QG?version=latest)

## API DEMO - EndPoints
https://cashback-dealer.herokuapp.com/api/dealer/  
https://cashback-dealer.herokuapp.com/login/  
https://cashback-dealer.herokuapp.com/api/purchase/  
https://cashback-dealer.herokuapp.com/api/acumulated-cashback/  

