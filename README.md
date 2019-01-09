# Eventex

Sistema de eventos

## Como desenvolver?

1. Clone o repositório
2. Crie um virtualenv com python 3.6
3. Ative seu virtualenv
4. Instale as dependencias
5. Configure a instâcia com o .env
6. Execute os testes

```console
git clone git@github.com:marcusgabrields/eventex.git wttd
cd wttd
python -m virtualenv .wttd
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer deploy
1. Crie uma instâcia no heroku.
2. Envie as configurações para o heroku.
3. Defina uma SECRET_KEY segura para instâcia
4. Defina DEBUG=Fasle
5. Configure o servço de email.
6. Envie o código para o heroku

```console
heroku create minha instacia
heroku config:push
heroku config:set SECRET_KEY=`python contrib secret_gen.py`
heroku config:set DEBUG=False
# configuro o email
git push heroku master --force
```