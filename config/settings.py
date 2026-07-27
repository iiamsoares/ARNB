import os
from dotenv import load_dotenv

# Carregando as variáveis dentro do arquivo .env
load_dotenv()

class Settings:
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Bling API v3
    BLING_ACCESS_TOKEN: str = os.getenv("BLING_ACCESS_TOKEN", "")
    BLING_REFRESH_TOKEN: str = os.getenv("BLING_REFRESH_TOKEN", "")
    BLING_CLIENT_ID: str = os.getenv("BLING_CLIENT_ID", "")
    BLING_CLIENT_SECRET: str = os.getenv("BLING_CLIENT_SECRET", "")

    @classmethod
    def validate(cls):
        """Valida se as credenciais essenciais foram preenchidas corretamente."""
        if not cls.SUPABASE_URL or not cls.SUPABASE_KEY:
            raise ValueError("ERRO: SUPABASE_URL ou SUPABASE_KEY não configuradas no arquivo .env!")
        print("Configurações de ambiente carregadas corretamente!")

# Instância global de configurações
settings = Settings()
