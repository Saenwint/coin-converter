import requests

class CurrencyConverterLogic:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.currencyapi.com/v2/latest"

    def get_currencies(self, base_currency="USD"):
        """
        Получает список всех доступных валют.
        :param base_currency: Базовая валюта для получения курсов (по умолчанию USD)
        :return: Список названий валют или None в случае ошибки
        """
        try:
            url = f"{self.base_url}?apikey={self.api_key}&base_currency={base_currency}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                rates = data.get("data")  # Словарь с курсами валют
                if isinstance(rates, dict):
                    return list(rates.keys())  # Возвращаем список названий валют
                else:
                    print("Ошибка: Некорректный формат ответа API")
                    return None
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Произошла ошибка при получении списка валют: {e}")
            return None

    def get_exchange_rate(self, base_currency, target_currency):
        """
        Получает курс обмена между двумя валютами.
        :param base_currency: Базовая валюта
        :param target_currency: Целевая валюта
        :return: Курс обмена или None в случае ошибки
        """
        try:
            url = f"{self.base_url}?apikey={self.api_key}&base_currency={base_currency}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                rates = data.get("data")
                if isinstance(rates, dict) and target_currency in rates:
                    exchange_rate = rates[target_currency]
                    if isinstance(exchange_rate, (int, float)):
                        return float(exchange_rate)
                    else:
                        print(f"Ошибка: Некорректный формат курса для {target_currency}")
                        return None
                else:
                    print(f"Ошибка: Не найдена валюта {target_currency} или некорректный ответ API")
                    return None
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Произошла ошибка при запросе курса: {e}")
            return None

    def convert_currency(self, amount, base_currency, target_currency):
        """
        Конвертирует сумму из одной валюты в другую.
        :param amount: Сумма для конвертации
        :param base_currency: Базовая валюта
        :param target_currency: Целевая валюта
        :return: Результат конвертации или None в случае ошибки
        """
        exchange_rate = self.get_exchange_rate(base_currency, target_currency)
        if exchange_rate is not None:
            return amount * exchange_rate
        return None