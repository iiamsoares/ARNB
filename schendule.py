import time
import schedule
from datetime import datetime, timedelta
from main import rodar_automacao_completa

def job_diario():
    """
    Executa a automação para a data de ONTEM (pois o dia já encerrou e todas as notas foram emitidas).
    """
    data_ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"\nExecutando rotina agendada diária referente ao dia anterior ({data_ontem})...")
    rodar_automacao_completa(data_alvo=data_ontem)

if __name__ == "__main__":
    horario_agendado = "17:45"
    print("\n" + "=" * 60)
    print(f"AGENDADOR ATIVADO! A automação rodará todos os dias às {horario_agendado}.")
    print("Pressione Ctrl+C para encerrar o agendador.")
    print("=" * 60 + "\n")

    # Agenda a execução diária
    schedule.every().day.at(horario_agendado).do(job_diario)

    # Loop contínuo aguardando o horário configurado
    while True:
        schedule.run_pending()
        time.sleep(60)
