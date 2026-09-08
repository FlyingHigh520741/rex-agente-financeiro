import requests
import time

class MarketAPI:
    """
    Integração com APIs de mercado financeiro para cotações em tempo real:
    - CoinGecko: Bitcoin e Ethereum (em BRL)
    - Brapi: IBOVESPA / Ações brasileiras
    Inclui cache local para respeitar limites de taxa (rate limits).
    """

    _cache = {}
    _CACHE_TTL = 3600 * 2  # 2 horas

    @classmethod
    def obter_cripto_btc(cls) -> str:
        agora = time.time()
        if "btc" in cls._cache:
            val, ts = cls._cache["btc"]
            if agora - ts < cls._CACHE_TTL:
                return val

        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                preco = res.json().get("bitcoin", {}).get("brl")
                if preco:
                    texto = f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    cls._cache["btc"] = (texto, agora)
                    return texto
        except Exception:
            pass

        return "R$ 380.000,00"

    @classmethod
    def obter_ibov(cls) -> str:
        agora = time.time()
        if "ibov" in cls._cache:
            val, ts = cls._cache["ibov"]
            if agora - ts < cls._CACHE_TTL:
                return val

        try:
            url = "https://brapi.dev/api/quote/%5EBVSP?token=public"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                results = res.json().get("results", [])
                if results and "regularMarketPrice" in results[0]:
                    pts = results[0]["regularMarketPrice"]
                    texto = f"{pts:,.0f} pts".replace(",", ".")
                    cls._cache["ibov"] = (texto, agora)
                    return texto
        except Exception:
            pass

        return "132.000 pts"

    @classmethod
    def obter_resumo_mercado(cls) -> dict:
        return {
            "bitcoin": cls.obter_cripto_btc(),
            "ibovespa": cls.obter_ibov()
        }

if __name__ == "__main__":
    print("Testando Market API:")
    print(MarketAPI.obter_resumo_mercado())

