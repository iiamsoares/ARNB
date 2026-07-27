import argparse
from datetime import datetime
from core.etl import ETLPipeline
from core.excel_generator import ExcelGenerator

def rodar_automacao_completa(data_alvo: str = None):
    """
    Orquestra o fluxo completo da automação:
    1. Busca notas do Bling, transforma os dados e salva no Supabase (ETL).
    2. Consulta os dados atualizados no Supabase e gera o arquivo Excel em 3 abas.
    """
    if not data_alvo:
        data_alvo = datetime.now().strftime("%Y-%m-%d")

    print("\n" + "=" * 60)
    print(f"INICIANDO AUTOMAÇÃO DE RELATÓRIOS DIÁRIOS ({data_alvo})")
    print("=" * 60 + "\n")

    # 1. ETAPA DE ETL (Bling -> Supabase)
    print("ETAPA 1: Sincronizando dados do Bling com o Supabase...")
    pipeline = ETLPipeline()
    pipeline.executar_pipeline_diaria(data_inicio=data_alvo, data_fim=data_alvo)

    # 2. ETAPA DE EXCEL (Supabase -> Relatório .xlsx)
    print("\nETAPA 2: Gerando relatório consolidado em Excel...")
    excel_gen = ExcelGenerator()
    caminho_planilha = excel_gen.gerar_relatorio_diario(data_alvo=data_alvo)

    print("\n" + "=" * 60)
    print("AUTOMAÇÃO EXECUTADA COM SUCESSO DE PONTA A PONTA!")
    print(f"Planilha Gerada: {caminho_planilha}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    # Permite passar uma data específica via linha de comando, ex: python main.py --data 2026-07-24
    parser = argparse.ArgumentParser(description="Automação Bling -> Supabase -> Excel")
    parser.add_argument("--data", type=str, help="Data alvo no formato YYYY-MM-DD (Padrão: Hoje)")
    args = parser.parse_args()

    rodar_automacao_completa(data_alvo=args.data)
