import requests
import time
from datetime import datetime

class BancoCentralAPI:
    """
    Cliente de integração com a API pública do Banco Central do Brasil (SGS - Sistema Gerenciador de Séries Temporais).
    Séries utilizadas:
    - 432: Meta Selic definida pelo Copom (% a.a.)
    - 433: IPCA - Variação mensal (%)
    - 1: Taxa de câmbio - Livre - Dólar americano (venda)
    """
    
    BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
    
    _cache = {}
    _CACHE_TTL = 3600 * 6  # Cache de 6 horas em segundos

    @classmethod
    def _obter_dado_serie(cls, codigo_serie: int, fallback_val: str) -> str:
        agora = time.time()
        if codigo_serie in cls._cache:
            dado_cached, timestamp = cls._cache[codigo_serie]
            if agora - timestamp < cls._CACHE_TTL:
                return dado_cached

        try:
            url = cls.BASE_URL.format(codigo=codigo_serie)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                dados = response.json()
                if dados and len(dados) > 0:
                    valor = dados[0].get("valor", fallback_val)
                    cls._cache[codigo_serie] = (valor, agora)
                    return valor
        except Exception:
            pass

        return fallback_val

    @classmethod
    def obter_selic(cls) -> str:
        """Retorna a taxa Selic Meta (% a.a.)."""
        return cls._obter_dado_serie(432, "10.50")

    @classmethod
    def obter_ipca_mensal(cls) -> str:
        """Retorna a última variação mensal do IPCA (%)."""
        return cls._obter_dado_serie(433, "0.38")

    @classmethod
    def obter_dolar(cls) -> str:
        """Retorna a cotação oficial do Dólar PTAX (R$)."""
        return cls._obter_dado_serie(1, "5.60")

    @classmethod
    def obter_resumo_indicadores(cls) -> dict:
        """Retorna dicionário compilado com os principais indicadores econômicos."""
        return {
            "selic": f"{cls.obter_selic()}% a.a.",
            "ipca": f"{cls.obter_ipca_mensal()}% (mês)",
            "dolar": f"R$ {float(cls.obter_dolar().replace(',', '.')):.2f}" if cls.obter_dolar() else "R$ 5.60"
        }

if __name__ == "__main__":
    print("Testando BCB API:")
    print(BancoCentralAPI.obter_resumo_indicadores())

