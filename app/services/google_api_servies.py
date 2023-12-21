from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"


class GoogleService:
    """API операции с аккаунтом гугл."""

    def __init__(self, wrapper_services: Aiogoogle):
        self.wrapper_services = wrapper_services

    async def set_user_permissions(self, spreadsheetid: str) -> None:
        """Права доступа для пользователя в роли writer."""
        permissions_body = {
            "type": "user",
            "role": "writer",
            "emailAddress": settings.email,
        }
        service = await self.wrapper_services.discover("drive", "v3")
        await self.wrapper_services.as_service_account(
            service.permissions.create(
                fileId=spreadsheetid, json=permissions_body, fields="id"
            )
        )

    async def spreadsheets_create(self) -> str:
        """Создание гугл-таблицы."""
        now_date_time = datetime.now().strftime(FORMAT)
        service = await self.wrapper_services.discover("sheets", "v4")
        spreadsheet_body = {
            "properties": {
                "title": f"Отчёт на {now_date_time}",
                "locale": "ru_RU",
            },
            "sheets": [
                {
                    "properties": {
                        "sheetType": "GRID",
                        "sheetId": 0,
                        "title": "Лист1",
                        "gridProperties": {"rowCount": 100, "columnCount": 11},
                    }
                }
            ],
        }
        response = await self.wrapper_services.as_service_account(
            service.spreadsheets.create(json=spreadsheet_body)
        )
        spreadsheetid = response["spreadsheetId"]
        return spreadsheetid

    async def spreadsheets_update_value(
        self, spreadsheetid: str, projects: list
    ) -> None:
        """Запись данных в созданную таблицу."""
        now_date_time = datetime.now().strftime(FORMAT)
        service = await self.wrapper_services.discover("sheets", "v4")
        table_values = [
            ["Отчёт от", now_date_time],
            ["Топ проектов по скорости закрытия"],
            ["Название проекта", "Время сбора", "Описание"],
        ]
        for project in projects:
            completion_rate = project.close_date - project.create_date
            new_row = [
                str(project.name),
                str(completion_rate),
                str(project.description),
            ]
            table_values.append(new_row)

        update_body = {"majorDimension": "ROWS", "values": table_values}
        await self.wrapper_services.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheetid,
                range="A1:E30",
                valueInputOption="USER_ENTERED",
                json=update_body,
            )
        )
