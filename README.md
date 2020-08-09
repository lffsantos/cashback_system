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


## Descrição da API - REST:
[Documentação da API](http://localhost:8000/doc/)
#### Criar Revendedor(a)

Para criar o revendedor é necessário informar os campos obrigatórios:  
- cpf
- email
- password
- name


```shell
curl --request POST \
  --url http://localhost:8000/api/dealer/ \
  --header 'content-type: application/json' \
  --data '{
	"cpf": "15350946056",
	"email": "aprovado@example.com",
	"password": "123456",
	"name": "Cpf Aprovado"
}'
```


#### Fazer Login (Autenticação)


```shell
curl --request POST \
  --url http://localhost:8000/login/ \
  --header 'content-type: application/json' \
  --data '{
	"email": "aprovado@example.com",
	"password": "123456"
}'

```


#### Cadastrar Compras

Para Cadastrar as compras é preciso estar informar o token de autenticação.

É necessário informar os campos obrigatórios:  
- purchase_code
- value
- purchase_at
- cpf

O cpf informado deve ser o mesmo do revendedor autenticado

```shell
curl --request POST \
  --url http://localhost:8000/api/purchase/ \
  --header 'authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFwcm92YWRvQGV4YW1wbGUuY29tIiwiZXhwIjoxNTk3NTUwNDgwLCJlbWFpbCI6ImFwcm92YWRvQGV4YW1wbGUuY29tIiwib3JpZ19pYXQiOjE1OTY5NDU2ODB9.N162E-OB4hGiIAi-Zvh_VVp8Qhq3pSa0eJrpZGqPJe8' \
  --header 'content-type: application/json' \
  --data '{
  "purchase_code": "code 1",
  "value": 900,
  "purchase_at": "2020-08-08",
  "cpf": "15350946056"
}'
```


### Listar Compras

Lista de compras do usuário autenticado.


```shell
curl --request GET \
  --url http://localhost:8000/api/purchase/ \
  --header 'authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFwcm92YWRvQGV4YW1wbGUuY29tIiwiZXhwIjoxNTk3NTUwNDgwLCJlbWFpbCI6ImFwcm92YWRvQGV4YW1wbGUuY29tIiwib3JpZ19pYXQiOjE1OTY5NDU2ODB9.N162E-OB4hGiIAi-Zvh_VVp8Qhq3pSa0eJrpZGqPJe8'
  ```
  
### Cashback Acumulado

Retorna o cashback acumulado, chamando uma api externa.

```shell
curl --request GET \
  --url http://localhost:8000/api/acumulated-cashback/ \
  --header 'authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3RlQGV4YW1wbGUuY29tIiwiZXhwIjoxNTk3NTQ0NTY1LCJlbWFpbCI6InRlc3RlQGV4YW1wbGUuY29tIiwib3JpZ19pYXQiOjE1OTY5Mzk3NjV9.X6oo0I65mKyOlQRjWrbCI04misxF96PeL2G_Lnop8qA'
```

