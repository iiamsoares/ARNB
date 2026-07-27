import json
from core.bling_client import BlingClient
from datetime import datetime
if __name__ == "__main__":
    print("Testando conexão com a API v3 do Bling...")
    bling = BlingClient()
    # Data de hoje para teste (YYYY-MM-DD)
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # !. Listando as notas de hoje
    notas_saida = bling.buscar_notas_fiscais(data_inicio=hoje, data_fim=hoje, tipo_nota=1)
    
    print("\n--- Resultado do Teste ---")
    if notas_saida:
        primeira_nota = notas_saida[0]
        id_nota = primeira_nota.get("id")
        print(f"\nPuxando detalhes completos da Nota ID:{id_nota}")

    # 2. Listando o detalhe por ID da Nota Fiscal
        print(f"\n---Detalhes da Nota Fiscal {id_nota}---")
        detalhes_nota = bling.obter_detalhes_notas_fiscais(id_nota)
        print(json.dumps(detalhes_nota, indent=4, ensure_ascii=False))
    else:
        print("Nenhuma nota emitida hoje até o momento.")