import requests
from config.config import OPENAQ_API_KEY

def fetch_latest_pm25(limit=1000):
    """
    Fetches the latest PM2.5 measurements from OpenAQ.
    """
    url = "https://api.openaq.org/v3/parameters/2/latest"
    headers = {
        "X-API-Key": OPENAQ_API_KEY
    }
    params = {
        "limit": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return []
