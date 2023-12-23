from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"


class GoogleService:
    """API операции с аккаунтом гугл."""

    def __init__(self, wrapper_service: Aiogoogle):
        self.wrapper_service = wrapper_service

    async def set_user_permissions(self, spreadsheet_id: str) -> None:
        """Права доступа для пользователя в роли writer."""
        permissions_body = {
            "type": "user",
            "role": "writer",
            "emailAddress": settings.email,
        }
        service = await self.wrapper_service.discover("drive", "v3")
        await self.wrapper_service.as_service_account(
            service.permissions.create(
                fileId=spreadsheet_id, json=permissions_body, fields="id"
            )
        )

    async def spreadsheets_create(self) -> str:
        """Создание гугл-таблицы."""
        now_date_time = datetime.now().strftime(FORMAT)
        service = await self.wrapper_service.discover("sheets", "v4")
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
        response = await self.wrapper_service.as_service_account(
            service.spreadsheets.create(json=spreadsheet_body)
        )
        spreadsheet_id = response["spreadsheetId"]
        return spreadsheet_id

    async def spreadsheets_update_value(
        self, spreadsheet_id: str, projects: list
    ) -> None:
        """Запись данных в созданную таблицу."""
        now_date_time = datetime.now().strftime(FORMAT)
        service = await self.wrapper_service.discover("sheets", "v4")
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
        await self.wrapper_service.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range="A1:E30",
                valueInputOption="USER_ENTERED",
                json=update_body,
            )
        )
