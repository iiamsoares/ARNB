import requests
import base64
from config.settings import settings

def trocar_code_por_token(code: str):
    url = "https://api.bling.com.br/v3/oauth/token"
    
    # Prepara a autenticação Basic Auth (client_id:client_secret em base64)
    credential = f"{settings.BLING_CLIENT_ID}:{settings.BLING_CLIENT_SECRET}"
    basic_auth = base64.b64encode(credential.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code
    }
    
    print("⏳ Solicitando tokens ao Bling...")
    resposta = requests.post(url, headers=headers, data=data)
    
    if resposta.status_code == 200:
        json_resp = resposta.json()
        print("\n🎉 TOKENS GERADOS COM SUCESSO!\n")
        print(f"BLING_ACCESS_TOKEN=\"{json_resp.get('access_token')}\"")
        print(f"BLING_REFRESH_TOKEN=\"{json_resp.get('refresh_token')}\"")
        print("\nCopie e cole os valores acima no seu arquivo .env!")
    else:
        print(f"❌ Erro ao gerar tokens ({resposta.status_code}): {resposta.text}")

if __name__ == "__main__":
    # Cole aqui o código 'code' retornado na URL do navegador
    code_do_navegador = input("Cole o parâmetro 'code' retornado na URL do navegador: ").strip()
    if code_do_navegador:
        trocar_code_por_token(code_do_navegador)
    else:
        print("Nenhum código informado.")
