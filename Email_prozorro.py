import schedule  # для запуска в определенное время
import smtplib   # для работы с почтой
from time import sleep
from email.mime.text import MIMEText  # Для работы с кириллицей
from Config_for_email import PASSWORD, EMAIL
from Create_HTML import append_HTML


def send_email():
    append_HTML()
    # Адрес электронной почты, которая будет отправлять сообщение
    sender = EMAIL

    # Адрес электронной почты, на который вы хотите отправить сообщение
    recipient = EMAIL

    # Это пароль для созданного приложения в почте
    password = PASSWORD

    # Создаем обьект SMTP (сервер, порт)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # Шифрованный обмен по TLC
    server.starttls()

    try:
        # Открывает и записываем страничку в - template
        with open("index.html", encoding='utf-8') as file:
            template = file.read()
    except IOError:
        return "The template"

    try:
        # Логинимся (Почта и пароль отправителя)
        server.login(sender, password)

        # Передаем сообщение
        msg = MIMEText(template, "html")
        # Доп. заголовки
        msg["From"] = sender
        msg["To"] = recipient
        # Задаем тему сообщения
        msg["Subject"] = "Тестовая тема"
        # Отправляем сообщение (Кто отправляет, кому, сообщение)
        server.sendmail(sender, recipient, msg.as_string())

        return "Сообщение успешно отправлено"
    except Exception as ex:
        return f"{ex}\nПроверьте свой логин или пароль!"


def main():
    # Задаем время
    schedule.every().day.at("15:06").do(send_email)

    while True:
        # Запуск
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
