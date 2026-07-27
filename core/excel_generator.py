import os
import pandas as pd
from datetime import datetime
from supabase import Client
from config.settings import settings
from supabase import create_client

class ExcelGenerator:
    def __init__(self):
        settings.validate()
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.output_dir = "relatorios_excel"
        
        # Garante que a pasta de saída existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def buscar_dados_dia(self, data_alvo: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Consulta as notas fiscais de Saída e Entrada no Supabase filtradas pela data de emissão.
        :param data_alvo: Data no formato 'YYYY-MM-DD'
        """
        inicio_dia = f"{data_alvo}T00:00:00-03:00"
        fim_dia = f"{data_alvo}T23:59:59-03:00"

        # Query Saídas
        resp_saidas = self.supabase.table("Notas_Fiscais_Saidas_2026") \
            .select("*") \
            .gte("data_emissao", inicio_dia) \
            .lte("data_emissao", fim_dia) \
            .execute()
        
        # Query Entradas
        resp_entradas = self.supabase.table("Notas_Fiscais_Entradas_2026") \
            .select("*") \
            .gte("data_emissao", inicio_dia) \
            .lte("data_emissao", fim_dia) \
            .execute()

        df_saidas = pd.DataFrame(resp_saidas.data) if resp_saidas.data else pd.DataFrame()
        df_entradas = pd.DataFrame(resp_entradas.data) if resp_entradas.data else pd.DataFrame()

        return df_saidas, df_entradas

    def gerar_relatorio_diario(self, data_alvo: str = None) -> str:
        """
        Gera a planilha .xlsx no diretório relatorios_excel/ dividida em 3 abas.
        """
        if not data_alvo:
            data_alvo = datetime.now().strftime("%Y-%m-%d")

        print(f"\nGerando relatório em Excel para a data: {data_alvo}...")
        df_saidas, df_entradas = self.buscar_dados_dia(data_alvo)

        # -------------------------------------------------------------
        # 1. ABA 1: RESUMO EXECUTIVO
        # -------------------------------------------------------------
        qtd_saidas = len(df_saidas)
        val_saidas = float(df_saidas["valor_nota"].sum()) if not df_saidas.empty and "valor_nota" in df_saidas else 0.0

        qtd_entradas = len(df_entradas)
        val_entradas = float(df_entradas["valor_nota"].sum()) if not df_entradas.empty and "valor_nota" in df_entradas else 0.0

        faturamento_liquido = val_saidas - val_entradas

        dados_resumo = [
            {"Métrica": "Quantidade de Vendas (Saídas)", "Valor": qtd_saidas},
            {"Métrica": "Valor Total de Vendas (R$)", "Valor": f"R$ {val_saidas:,.2f}"},
            {"Métrica": "Quantidade de Devoluções/Entradas", "Valor": qtd_entradas},
            {"Métrica": "Valor Total de Devoluções/Entradas (R$)", "Valor": f"R$ {val_entradas:,.2f}"},
            {"Métrica": "Faturamento Líquido do Dia (R$)", "Valor": f"R$ {faturamento_liquido:,.2f}"}
        ]
        df_resumo = pd.DataFrame(dados_resumo)

        # -------------------------------------------------------------
        # 2. SELEÇÃO E RENOMEAÇÃO DE COLUNAS DAS ABAS DE DETALHES
        # -------------------------------------------------------------
        colunas_renomear_saida = {
            "numero": "Número NF",
            "serie": "Série",
            "situacao": "Situação",
            "data_emissao": "Data Emissão",
            "cliente_nome": "Cliente",
            "cliente_documento": "CPF/CNPJ Cliente",
            "valor_nota": "Valor Nota (R$)",
            "valor_frete": "Frete (R$)",
            "valor_desconto": "Desconto (R$)",
            "chave_acesso": "Chave NFe"
        }

        colunas_renomear_entrada = {
            "numero": "Número NF",
            "serie": "Série",
            "situacao": "Situação",
            "data_emissao": "Data Emissão",
            "fornecedor_nome": "Fornecedor / Origem",
            "fornecedor_documento": "CPF/CNPJ Fornecedor",
            "valor_nota": "Valor Nota (R$)",
            "valor_frete": "Frete (R$)",
            "valor_desconto": "Desconto (R$)",
            "chave_acesso": "Chave NFe"
        }

        if not df_saidas.empty:
            cols_existentes = [c for c in colunas_renomear_saida.keys() if c in df_saidas.columns]
            df_saidas = df_saidas[cols_existentes].rename(columns=colunas_renomear_saida)

        if not df_entradas.empty:
            cols_existentes = [c for c in colunas_renomear_entrada.keys() if c in df_entradas.columns]
            df_entradas = df_entradas[cols_existentes].rename(columns=colunas_renomear_entrada)

        # -------------------------------------------------------------
        # 3. GRAVAÇÃO DAS 3 ABAS NO EXCEL
        # -------------------------------------------------------------
        nome_arquivo = f"Vendas_Diarias_{data_alvo.replace('-', '_')}.xlsx"
        caminho_completo = os.path.join(self.output_dir, nome_arquivo)

        with pd.ExcelWriter(caminho_completo, engine="openpyxl") as writer:
            df_resumo.to_excel(writer, sheet_name="Resumo Geral", index=False)
            df_saidas.to_excel(writer, sheet_name="NF-e de Saída", index=False)
            df_entradas.to_excel(writer, sheet_name="NF-e de Entrada", index=False)

        print(f"Relatório Excel gerado com sucesso: {caminho_completo}")
        return caminho_completo
