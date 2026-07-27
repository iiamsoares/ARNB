import requests
import time
from config .settings import settings

class BlingClient:
    def __init__(self):
        self.base_url = "https://api.bling.com.br/Api/v3"
        self.access_token = settings.BLING_ACCESS_TOKEN
        self.refresh_token = settings.BLING_REFRESH_TOKEN
        self.client_id = settings.BLING_CLIENT_ID
        self.client_secret = settings.BLING_CLIENT_SECRET


    def _get_headers(self) -> dict:
        """
        Retorna os cabecalhos de requisicao exigidos pela documentacao da API do Bling v3.
        """
        return{
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }

    def renovar_token(self) -> bool:
        """
        Caso o Access Token expire, o script tenta utilizar o Refresh Token para obter um novo yoken válidado.
        """
        url = f"{self.base_url}/oauth/token"
        
        # O Bling v3 aceita as credencias do app via Auth Basic ou dados de formulário

        payload ={
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        try:
            resposta = requests.post(
                url,
                data=payload,
                auth=(self.client_id, self.client_secret)
            )
            if resposta.status_code == 200:
                dados = resposta.json()
                self.access_token = dados.get("access_token", self.access_token)
                print("Token do Bling renovado com sucesso!")
                return True
            else:
                print(f"Erro ao renovar token do Bling: {{resposta.status_code}}: {resposta.text}")
                return False
        except Exception as e:
            print(f"Exceção ao renovar token do Bling: {e}")
            return False

    def buscar_notas_fiscais(self, data_inicio: str , data_fim: str, tipo_nota: int = 1) -> list[dict]:
        """
        Busca Notas Fiscais no Bling com paginação. 
        parametro data_fim: Data final para busca (formato: YYYY-MM-DD).
        parametro tipo_nota: Tipo de nota fiscal a ser buscada (1: Notas Fiscais de Saída, 2: Notas Fiscais de Entrada).
        retorno: Lista de notas fiscais encontradas.
        """
        url = f"{self.base_url}/nfe"
        todas_notas = []
        pagina = 1
        limite = 100
        print(f"Buscando Notas Fiscais no Bling ({'Saída' if tipo_nota == 1 else 'Entrada'}) de {data_inicio} até {data_fim}...")
        while True:
            params = {
                "dataEmissaoInicial": f"{data_inicio} 00:00:00",
                "dataEmissaoFinal": f"{data_fim} 23:59:59",
                "tipo": tipo_nota,
                "pagina": pagina,
                "limite": limite
            }
            resposta = requests.get(url, headers=self._get_headers(), params=params)
            # Caso o token tenha expirado (401), tenta renovar e refaz a requisição
            if resposta.status_code == 401:
                if self.renovar_token():
                    resposta = requests.get(url, headers=self._get_headers(), params=params)
                else:
                    print("Falha na renovação de token. Interrompendo busca.")
                    break
            if resposta.status_code == 200:
                dados = resposta.json()
                notas_pagina = dados.get("data", [])
                
                if not notas_pagina:
                    break  # Fim das páginas
                
                todas_notas.extend(notas_pagina)
                print(f"Página {pagina}: {len(notas_pagina)} notas encontradas.")
                
                pagina += 1
                time.sleep(0.3)  # Respeita o rate limit da API do Bling
            else:
                print(f"Erro ao consultar notas ({resposta.status_code}): {resposta.text}")
                break
        print(f"Total de {len(todas_notas)} notas encontradas para o período.")
        return todas_notas

    def obter_detalhes_notas_fiscais(self, id_nota: int) -> dict:
        """
        Buscar detalhes completos de uma Nota Fiscal específica pelo ID dela.
        Retorna o dicionário contendo detalhes da nota fiscal: Valor Total, frete, clientes e itens
        se a nota não for encontrada retorna um dicionário vazio.
        """
        url = f"{self.base_url}/nfe/{id_nota}"
        resposta = requests.get(url, headers=self._get_headers())
        # Caso o token expire;
        if resposta.status_code == 401:
            if self.renovar_token():
                resposta = requests.get(url, headers=self._get_headers())

        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get("data", {})
        else:
            print(f"Erro ao consultar detalhes da nota {{id_nota}}: {{resposta.status_code}}: {resposta.text}")
            return {}           