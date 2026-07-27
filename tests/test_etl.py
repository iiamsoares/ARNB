from core.etl import ETLPipeline
from datetime import datetime

if __name__ == "__main__":
    print("Testando Pipeline ETL completo.")
    pipeline = ETLPipeline()
    
    # Testa para a data de hoje
    hoje = datetime.now().strftime("%Y-%m-%d")
    pipeline.executar_pipeline_diaria(data_inicio=hoje, data_fim=hoje)
