FROM python:3.9

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли залежностей та встановлюємо їх
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект в контейнер
COPY . .

# Вказуємо порт, який буде відкритий в контейнері
EXPOSE 8000

# Запускаємо додаток
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]