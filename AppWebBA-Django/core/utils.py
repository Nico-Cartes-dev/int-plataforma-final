from zeep import Client
from datetime import datetime
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def get_exchange_clp_usd():
    #* Check cache first
    cache_key = f"usd_clp_{datetime.now().strftime('%Y-%m-%d')}"
    exchange_rate = cache.get(cache_key)
    if exchange_rate:
        return exchange_rate

    try:
        # SOAP client for Banco Central de Chile
        wsdl_url = "https://si3.bcentral.cl/SieteWS/SieteWS.asmx?WSDL"
        client = Client(wsdl_url)
        # arreglar esta parte del code 
        series_id = "F073.TCO.PRE.Z.D"  # Dólar observado
        date = datetime.now().strftime("%Y-%m-%d")

        #* Replace with your actual API credentials
        username = "nicolas cartes"  
        password = "Duoc_2025_123"  

        #* Call the API
        response = client.service.GetSeriesData(
            user=username,
            password=password,
            series=series_id,
            startDate=date,
            endDate=date
        )

        #* Extract the exchange rate
        if response and hasattr(response, 'Series') and response.Series.Obs:
            exchange_rate = float(response.Series.Obs[0].value)
            cache.set(cache_key, exchange_rate, timeout=86400)  
            return exchange_rate
        else:
            logger.error("No exchange rate data found for today")
            return None
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
        return None