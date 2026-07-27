from supabase import create_client, Client
from config.settings import settings

class SupabaseManager:
    def __init__(self):
        # Valida as configurações de ambiente se estão funcionando corretamente
        settings.validate()
        
        # Inicializando o cliente oficial do Supabase
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def salvar_notas_saida(self, lista_notas: list[dict]):
        """
        Salva ou atualiza (Upsert) uma lista de notas fiscais de saída na tabela.
        """
        if not lista_notas:
            print("Nenhuma nota de saída para salvar!")
            return

        try:
            # O upsert insere novas notas ou atualiza caso o ID já exista
            resposta = self.client.table("Notas_Fiscais_Saidas_2026").upsert(lista_notas).execute()
            print(f"Foram salvas {len(lista_notas)} notas de saída com sucesso no Supabase!")
            return resposta
        except Exception as e:
            print(f"ERRO ao salvar notas de saída: {str(e)}")
            raise e

    def salvar_notas_entrada(self, lista_notas: list[dict]):
        """
        Salva ou atualiza (Upsert) uma lista de notas fiscais de entrada na tabela.
        """
        if not lista_notas:
            print("Nenhuma nota de entrada para salvar!")
            return

        try:
            resposta = self.client.table("Notas_Fiscais_Entradas_2026").upsert(lista_notas).execute()
            print(f"Foram salvas {len(lista_notas)} notas de entrada com sucesso no Supabase!")
            return resposta
        except Exception as e:
            print(f"Erro ao salvar notas de entrada: {str(e)}")
            raise e
