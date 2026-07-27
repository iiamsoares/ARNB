from datetime import datetime
from core.bling_client import BlingClient
from core.supabase_client import SupabaseManager

class ETLPipeline:
    def __init__(self):
        self.bling = BlingClient()
        self.supabase = SupabaseManager()

    def _transformar_nota(self, detalhe_nota: dict, tipo: str) -> dict:
        """
        Mapeia e transforma o JSON retornado pelo Bling no formato exato da tabela do Supabase.
        :param detalhe_nota: Dicionário vindo de GET /nfe/{id}
        :param tipo: 'S' para Saída ou 'E' para Entrada
        """
        contato = detalhe_nota.get("contato", {})
        
        # Mapeamento dos campos principais
        nota_formatada = {
            "id": detalhe_nota.get("id"),
            "numero": str(detalhe_nota.get("numero", "")),
            "serie": str(detalhe_nota.get("serie", "")),
            "tipo": tipo,
            # Aplique mudanca de int para str 6 -> Emitida
            "situacao": str(detalhe_nota.get("situacao", "")) if detalhe_nota.get("situacao") == '6' else "Emitida",
            "chave_acesso": detalhe_nota.get("chaveAcesso"),
            "data_emissao": detalhe_nota.get("dataEmissao"),
            "data_operacao": detalhe_nota.get("dataOperacao"),
            # Busca o valor da nota (testa valorNota ou total)
            "valor_nota": float(detalhe_nota.get("valorNota") or detalhe_nota.get("total") or 0.0),
            "valor_frete": float(detalhe_nota.get("valorFrete") or 0.0),
            "valor_desconto": float(detalhe_nota.get("valorDesconto") or 0.0),
        }

        # Separa os dados de Contato entre Cliente (Saídas) e Fornecedor (Entradas)
        if tipo == "S":
            nota_formatada["cliente_nome"] = contato.get("nome", "")
            nota_formatada["cliente_documento"] = contato.get("numeroDocumento", "")
        else:
            nota_formatada["fornecedor_nome"] = contato.get("nome", "")
            nota_formatada["fornecedor_documento"] = contato.get("numeroDocumento", "")

        return nota_formatada

    def executar_pipeline_diaria(self, data_inicio: str = None, data_fim: str = None):
        """
        Executa a extração do Bling, transformação e carga no Supabase.
        Se nenhuma data for informada, utiliza a data de hoje.
        """
        if not data_inicio:
            data_inicio = datetime.now().strftime("%Y-%m-%d")
        if not data_fim:
            data_fim = data_inicio

        print(f"\nIniciando Pipeline ETL para o período: {data_inicio} até {data_fim}\n")

        # -------------------------------------------------------------
        # 1. PROCESSAR NOTAS DE SAÍDA (VENDAS) - tipo_nota = 1
        # -------------------------------------------------------------
        notas_saida_resumo = self.bling.buscar_notas_fiscais(data_inicio, data_fim, tipo_nota=1)
        notas_saida_transformadas = []

        for resumo in notas_saida_resumo:
            id_nota = resumo.get("id")
            if id_nota:
                print(f"Detalhando e transformando NF de Saída ID: {id_nota}...")
                detalhe = self.bling.obter_detalhes_notas_fiscais(id_nota)
                if detalhe:
                    nota_pronta = self._transformar_nota(detalhe, tipo="S")
                    notas_saida_transformadas.append(nota_pronta)

        if notas_saida_transformadas:
            print(f"\nSalvando {len(notas_saida_transformadas)} notas de saída no Supabase...")
            self.supabase.salvar_notas_saida(notas_saida_transformadas)
        else:
            print("Nenhuma nota de saída para salvar no período.")

        # -------------------------------------------------------------
        # 2. PROCESSAR NOTAS DE ENTRADA (COMPRAS/DEVOLUÇÕES) - tipo_nota = 0
        # -------------------------------------------------------------
        notas_entrada_resumo = self.bling.buscar_notas_fiscais(data_inicio, data_fim, tipo_nota=0)
        notas_entrada_transformadas = []

        for resumo in notas_entrada_resumo:
            id_nota = resumo.get("id")
            if id_nota:
                print(f"Detalhando e transformando NF de Entrada ID: {id_nota}...")
                detalhe = self.bling.obter_detalhes_notas_fiscais(id_nota)
                if detalhe:
                    nota_pronta = self._transformar_nota(detalhe, tipo="E")
                    notas_entrada_transformadas.append(nota_pronta)

        if notas_entrada_transformadas:
            print(f"\nSalvando {len(notas_entrada_transformadas)} notas de entrada no Supabase...")
            self.supabase.salvar_notas_entrada(notas_entrada_transformadas)
        else:
            print("Nenhuma nota de entrada para salvar no período.")

        print("\nPipeline ETL concluído com sucesso!")
