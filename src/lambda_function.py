import requests
from bs4 import BeautifulSoup
import json

def marcar_presenca(usuario,senha):
    print(f'Marcando presenca para o user {usuario}...')
    base_url = 'https://interage.fei.org.br/secureserver/portal/'
    presenca_page = 'https://interage.fei.org.br/secureserver/portal/graduacao/sala-dos-professores/aulas/presenca'

    payload_login = {
        '__RequestVerificationToken': None,
        'Usuario': usuario,
        'Senha': senha
    }

    payload_presenca = {
        'chave':None,
        'consideracao':''
    }

    with requests.Session() as sess:
        fei_login = sess.get(base_url)
        soup = BeautifulSoup(fei_login.content.decode(),features="html.parser")
        input_hidden = soup.select_one('input[name="__RequestVerificationToken"]')
        input_hidden_value = input_hidden.attrs['value']
        payload_login['__RequestVerificationToken'] = input_hidden_value
        login_response = sess.post(base_url,json=payload_login)
        assert login_response.status_code == 200
        presenca_response = sess.get('https://interage.fei.org.br/secureserver/portal/graduacao/sala-dos-professores/aulas/presenca')
        soup = BeautifulSoup(presenca_response.content.decode(),features="html.parser")
        keys = [input_hidden.attrs['value'] for input_hidden in soup.select('input[type="hidden"]')]
        print(f'Total de {len(keys)} para marcar presenca')
        for index,key in enumerate(keys):
            print(f'Marcando presenca para chave {index}: {key}')
            payload_presenca['chave'] = key
            token = sess.cookies.get('__token_pg')
            print(f'Token resgatado: {token}')
            sess.headers['Authorization'] = f'Bearer {token}'
            marcar_presenca_response = sess.post(presenca_page,json=payload_presenca)
            print('Solicitacao de marcar presenca enviada! Validando status code')
            assert marcar_presenca_response.status_code == 200
            print(f'Presenca enviada com sucesso!')
            print()
        return len(keys)

def lambda_handler(event, context):
    if 'usuarios' in event:
        for auth in event['usuarios']:
            total_presencas = marcar_presenca(auth['usuario'],auth['senha'])
            
        return {
            'statusCode': 200,
            'body': json.dumps('Presenca marcada para todos usuarios com sucesso!')
        }
    return {
            'statusCode': 400,
            'body': json.dumps('usuario e senha devem ser fornecidos!')
    }
    

    
