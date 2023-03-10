from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
SPREADSHEETS_BODY = {
    'properties': {
        'title': f'Отчет на ', # noqa
        'locale': 'ru_RU'}, 'sheets':
            [{'properties':
                {'sheetType': 'GRID',
                 'sheetId': 0, 'title':
                     'Лист1', 'gridProperties':
                         {'rowCount': 100, 'columnCount': 11}}}]
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEETS_BODY
    spreadsheet_body['properties']['title'] += NOW_DATE_TIME
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str, wrapper_services: Aiogoogle) -> None:
    permissions_body = {
        'type': 'user', 'role': 'writer', 'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"))


async def spreadsheets_update_value(
        spreadsheet_id: str, projects: list,
        wrapper_services: Aiogoogle) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', NOW_DATE_TIME],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']]
    for res in projects:
        new_row = [res['name'], str(res['delta']), res['description']]
        table_values.append(new_row)
    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body))
