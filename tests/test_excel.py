from core.excel_generator import ExcelGenerator
from datetime import datetime

if __name__ == "__main__":
    generator = ExcelGenerator()
    hoje = datetime.now().strftime("%Y-%m-%d")
    generator.gerar_relatorio_diario(data_alvo=hoje)

    