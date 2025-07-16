# 🌤️ PyQt5 Weather App

A lightweight and user-friendly desktop weather application built with **Python** and **PyQt5**.  
Fetch real-time weather information for any city using the **WeatherAPI**.

---

## 📖 About
This project was created as a learning exercise to explore PyQt5 GUI development and API integrations in Python.  
It aims to demonstrate clean code practices, API handling, and user-friendly desktop applications.

---

## ✨ Features
- 🖥️ Beautiful PyQt5 GUI
- 🌐 Fetches live weather data
- 🌡️ Displays temperature, description, and weather icon
- 🔑 Secure API key management using `.env`
- 📦 Lightweight and easy to run

---

## 📸 Screenshots

Here’s how the app looks:

![App Screenshot](screenshot/app_ui.png)

---

## 🚀 Getting Started

### 📥 Clone the Repository
```bash
git clone https://github.com/your-username/pyqt5-weather-app.git
cd pyqt5-weather-app
```

### 📦 Install Dependencies
Make sure you have Python 3.7+ installed. Then run:
```bash
pip install -r requirements.txt
```

---

## 📜 Requirements.txt
These are the Python packages required to run the app:
```
PyQt5==5.15.11
python-dotenv==1.1.1
requests==2.32.4
```

---

## 🔑 .env Example
Create a `.env` file in the project root with the following content:
```
WEATHER_API_KEY=your_api_key_here
```
💡 You can get a free API key from [WeatherAPI](https://www.weatherapi.com/)

---

## ▶️ Run the Application
After setting up everything, run:
```bash
python weather_app.py
```

---

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🙌 Credits
- [PyQt5](https://pypi.org/project/PyQt5/)
- [WeatherAPI](https://www.weatherapi.com/)
