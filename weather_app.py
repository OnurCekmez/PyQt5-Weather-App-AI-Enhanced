from dotenv import load_dotenv
import os
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QWidget {
                background-color: #cce7ff;
            }
            QLabel, QPushButton {
                font-family: Arial, Helvetica, sans-serif;
                color: #333;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
                padding: 5px;
                border: 2px solid #006aff;
                border-radius: 8px;
                color: black;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
                background-color: #006aff;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #338eff;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
            }
            QLabel#description_label {
                font-size: 50px;
                color: #555;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            self.display_error("API key not found.\nCheck your .env file.")
            return
        city = self.city_input.text()
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

        try:
            response  = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                error_code = data["error"]["code"]
                match error_code:
                    case 1006:  # No matching location found
                        self.display_error("Not Found:\nCity not found")
                    case _:
                        self.display_error(f"API Error {error_code}:\n{data['error']['message']}")
            else:
                api_city = data["location"]["name"].lower()
                user_city = city.lower()
                if api_city != user_city:
                    self.display_error("Not Found:\nCity not found")
                    return
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")
                
                

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request time out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        temperature_c = data["current"]["temp_c"]
        # print(temperature_c)
        weather_id = data["current"]["condition"]["code"]
        weather_description = data["current"]["condition"]["text"]

        self.temperature_label.setStyleSheet("color: #333333; font-size: 75px;")

        self.temperature_label.setText(f"{temperature_c}℃")
        pixmap = self.get_weather_emoji(data)
        scaled_pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.emoji_label.setPixmap(scaled_pixmap)
        self.description_label.setText(weather_description)
        
    @staticmethod
    def get_weather_emoji(data):
        icon_url = "http:" + data["current"]["condition"]["icon"]
        icon_response = requests.get(icon_url)
        pixmap = QPixmap()
        pixmap.loadFromData(icon_response.content)
        return pixmap

def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()