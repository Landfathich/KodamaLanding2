import datetime
import logging
import os
import uuid

import pytz
from gspread import Client, Spreadsheet, service_account

logger = logging.getLogger(__name__)

TABLE_ID = "1zAsg7X1S1RiGG51qMK2RiEXUWxpJ9MaYhcWGlHzc5xQ"

# Нужно вмонтировать папку kodama-secrets так:
# -v /var/lib/dokku/data/storage/kodama-secrets:/app/secrets
KEY_PATH = '/app/secrets/kodama-storage-b9df0175c688.json'


# Ссылка на таблицу: https://docs.google.com/spreadsheets/d/1zAsg7X1S1RiGG51qMK2RiEXUWxpJ9MaYhcWGlHzc5xQ/edit


def client_init_json() -> Client:
    return service_account(filename=KEY_PATH)


def get_table_by_id(client: Client, table_url: str) -> Spreadsheet:
    return client.open_by_key(table_url)


def get_worksheet_info(table: Spreadsheet) -> dict:
    worksheets = table.worksheets()
    return {
        "count": len(worksheets),
        "names": [ws.title for ws in worksheets]
    }


def insert_test_row(table: Spreadsheet, sheet_name: str) -> None:
    worksheet = table.worksheet(sheet_name)
    values = worksheet.get_all_values()
    next_row = len(values) + 1
    timezone = pytz.timezone("Europe/Moscow")
    test_data = [
        str(uuid.uuid4()), "mail", "phone", str(datetime.date.today()),
        datetime.datetime.now(timezone).time().strftime("%H:%M"),
        "курс", "имя", "коммент", "статус"
    ]
    worksheet.insert_row(test_data, index=next_row)
    logger.info(f"Добавлена строка {next_row} с тестовыми данными")


def test_insert_new_row():
    client = client_init_json()
    table = get_table_by_id(client, TABLE_ID)
    get_worksheet_info(table)
    insert_test_row(table, 'Requests')


def insert_new_row(
        mail: str,
        phone: str,
        course: str = "Не выбран",
        name: str = "",
        is_policy_accepted: str = "",
        comment: str = "",
        status: str = "Ожидает ответа"
) -> bool:
    if not os.path.exists(KEY_PATH):
        logger.error(f"❌ Файл ключа не найден: {KEY_PATH}")
        return False

    try:
        client = client_init_json()
        table = get_table_by_id(client, TABLE_ID)
        worksheet = table.worksheet("Requests")

        values = worksheet.get_all_values()
        next_row = len(values) + 1
        timezone = pytz.timezone("Europe/Moscow")

        data = [
            str(uuid.uuid4()),
            mail,
            phone,
            str(datetime.date.today()),
            datetime.datetime.now(timezone).time().strftime("%H:%M"),
            course,
            name,
            comment,
            is_policy_accepted,
            status
        ]

        worksheet.insert_row(data, index=next_row)
        logger.info(f"Добавлена строка {next_row}")
        return True

    except Exception as e:
        logger.error(f"Ошибка Google Sheets: {type(e).__name__}: {e}")
        return False
