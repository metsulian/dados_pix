from src.utils.api_requests import get_data

from src.config import API_URL

data = get_data(API_URL)
print(data)