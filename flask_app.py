from flask import Flask, request
# ngrok ключ для авторизации 28qqtiZvFAOvTYzRRaBixggfsjj_5HYKTDNU1eb68AU3s2r1r

import logging
import json

app = Flask(__name__)
# run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()

# INFO:root:Request: {'session': {'message_id': 0, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': True}, 'version': '1.0', 'response': {'end_session': False, 'text': 'Привет! Купи слона!', 'buttons': [{'title': 'Не хочу.', 'hide': True}, {'title': 'Не буду.', 'hide': True}]}}
# INFO:root:Response:  {'session': {'message_id': 0, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': True}, 'version': '1.0', 'response': {'end_session': False, 'text': 'Привет! Купи слона!', 'buttons': [{'title': 'Не хочу.', 'hide': True}, {'title': 'Не буду.', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:40:00] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 0, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': True}, 'request': {'command': '', 'original_utterance': '', 'nlu': {'tokens': [], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 0, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': True}, 'version': '1.0', 'response': {'end_session': False, 'text': 'Привет! Купи слона!', 'buttons': [{'title': 'Не хочу.', 'hide': True}, {'title': 'Не буду.', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:40:22] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 1, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'request': {'command': 'не хочу', 'original_utterance': 'не хочу', 'nlu': {'tokens': ['не', 'хочу'], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 1, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'version': '1.0', 'response': {'end_session': False, 'text': "Все говорят 'не хочу', а ты купи слона!", 'buttons': [{'title': 'Не буду.', 'hide': True}, {'title': 'Отстань!', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:40:53] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 2, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'request': {'command': 'отстань', 'original_utterance': 'Отстань!', 'nlu': {'tokens': ['отстань'], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 2, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'version': '1.0', 'response': {'end_session': False, 'text': "Все говорят 'Отстань!', а ты купи слона!", 'buttons': [{'title': 'Отстань!', 'hide': True}, {'title': 'Ладно', 'url': 'https://market.yandex.ru/search?text=слон', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:42:03] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 3, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'request': {'command': 'отстань', 'original_utterance': 'Отстань!', 'nlu': {'tokens': ['отстань'], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 3, 'session_id': '689dbf67-2903-4f5c-b6c2-425006ed88d1', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'version': '1.0', 'response': {'end_session': False, 'text': "Все говорят 'Отстань!', а ты купи слона!", 'buttons': [{'title': 'Ладно', 'url': 'https://market.yandex.ru/search?text=слон', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:42:10] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 0, 'session_id': 'fe0a81f4-9f72-4d87-9904-db9a751215ae', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': True}, 'request': {'command': '', 'original_utterance': '', 'nlu': {'tokens': [], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 0, 'session_id': 'fe0a81f4-9f72-4d87-9904-db9a751215ae', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': True}, 'version': '1.0', 'response': {'end_session': False, 'text': 'Привет! Купи слона!', 'buttons': [{'title': 'Не хочу.', 'hide': True}, {'title': 'Не буду.', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:42:15] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 1, 'session_id': 'fe0a81f4-9f72-4d87-9904-db9a751215ae', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'request': {'command': 'не хочу', 'original_utterance': 'Не хочу.', 'nlu': {'tokens': ['не', 'хочу'], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 1, 'session_id': 'fe0a81f4-9f72-4d87-9904-db9a751215ae', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'version': '1.0', 'response': {'end_session': False, 'text': "Все говорят 'Не хочу.', а ты купи слона!", 'buttons': [{'title': 'Не буду.', 'hide': True}, {'title': 'Отстань!', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:42:18] "POST /post HTTP/1.1" 200 -
# INFO:root:Request: {'meta': {'locale': 'ru-RU', 'timezone': 'UTC', 'client_id': 'ru.yandex.searchplugin/7.16 (none none; android 4.4.2)', 'interfaces': {'screen': {}, 'payments': {}, 'account_linking': {}}}, 'session': {'message_id': 2, 'session_id': 'fe0a81f4-9f72-4d87-9904-db9a751215ae', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'request': {'command': 'отстань', 'original_utterance': 'Отстань!', 'nlu': {'tokens': ['отстань'], 'entities': [], 'intents': {}}, 'markup': {'dangerous_context': False}, 'type': 'SimpleUtterance'}, 'version': '1.0'}
# INFO:root:Response:  {'session': {'message_id': 2, 'session_id': 'fe0a81f4-9f72-4d87-9904-db9a751215ae', 'skill_id': 'bb0de403-6c3e-4d10-b386-b9bd056a8991', 'user': {'user_id': '8B7FE477E170609E287FAE264CA42B29260CA3A3F8C3E83414F7453890ABB23D'}, 'application': {'application_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5'}, 'user_id': '2D9578E96B203FD3F65D3F4ABE09477F2C9A3E9C68E514EA715FDFE3BEF9B1E5', 'new': False}, 'version': '1.0', 'response': {'end_session': False, 'text': "Все говорят 'Отстань!', а ты купи слона!", 'buttons': [{'title': 'Отстань!', 'hide': True}, {'title': 'Ладно', 'url': 'https://market.yandex.ru/search?text=слон', 'hide': True}]}}
# INFO:werkzeug:127.0.0.1 - - [07/May/2022 23:42:20] "POST /post HTTP/1.1" 200 -
