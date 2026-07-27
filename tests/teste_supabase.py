from core.supabase_client import SupabaseManager

if __name__ == "__main__":
    print("Testando conexão com o Supabase...")
    db = SupabaseManager()

    # Simulando qualquer dado para ver se salva dentro do banco
    nota_teste_entrada = [{
        "id": 999999999,
        "numero": "101",
        "serie": "1",
        "tipo": "E",
        "situacao": "Emitida",
        "chave_acesso": "35260700000000000000550010000001011000000001",
        "data_emissao": "2026-07-24T10:00:00-03:00",
        "valor_nota": 150.00,
        "fornecedor_nome": "Fulano",
        "fornecedor_documento": "000.000.000-00"
    }]
    
    nota_teste_saida = [{
        "id": 999999998,
        "numero": "102",
        "serie": "1",
        "tipo": "S",
        "situacao": "Emitida",
        "chave_acesso": "35260700000000000000550010000001021000000002",
        "data_emissao": "2026-07-24T10:00:00-03:00",
        "valor_nota": 250.00,
        "cliente_nome": "Ciclano",
        "cliente_documento": "000.000.000-00"
    }]

    # Inserindo dados ficticios dentro das tabelas
    db.salvar_notas_entrada(nota_teste_entrada)
    db.salvar_notas_saida(nota_teste_saida)
