import requests

BOT_TOKEN = '7932135408:AAFpBzgkq2ZPcrFQgMiRGf5s_633LTYvZ8Q'

def check_connection():
    print("Intentando conectar con Telegram...")  # Línea de depuración
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getMe'
    response = requests.get(url)
    if response.status_code == 200:
        print("Conexión exitosa con Telegram")
        print(response.json())
    else:
        print(f"Error al conectar con Telegram: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    check_connection()
