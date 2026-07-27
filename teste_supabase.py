from core.supabase_client import SupabaseManager

if __name__ == "__main__":
    print("🚀 Testando conexão com o Supabase...")
    db = SupabaseManager()

    # Dados simulados de teste para nota de saída
    nota_teste = [{
        "id": 999999999,
        "numero": "101",
        "serie": "1",
        "tipo": "S",
        "situacao": "Emitida",
        "chave_acesso": "35260700000000000000550010000001011000000001",
        "data_emissao": "2026-07-24T10:00:00-03:00",
        "valor_nota": 150.00,
        "cliente_nome": "Cliente Teste",
        "cliente_documento": "000.000.000-00"
    }]

    # Inserir no Supabase
    db.salvar_notas_saida(nota_teste)
