## Running and using this project

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to [http://localhost:8004/docs/](http://localhost:8004/docs/) to view the docs for API or to [http://localhost:5556](http://localhost:5556) to view the Flower dashboard for Celery tasks.

## API methods

### POST /new_client/

Accepts object like

```json
{
  "phone_number": 0,
  "tag": "string",
  "timezone": 0
}
```

Returns object like

```json
{
  "phone_number": 0,
  "tag": "string",
  "timezone": 0,
  "id": 0,
  "operator": 0
}
```

### PUT /client/{client_id}

Accepts path parameter client_id and query parameters: phone_number, tag, timezone.

Returns object like

```json
{
  "phone_number": 0,
  "tag": "string",
  "timezone": 0,
  "id": 0,
  "operator": 0
}
```

### DELETE /client/{client_id}

Accepts path parameter client_id.

Returns object

```json
"Success"
```

### POST /new_mailing_list/

Accepts object like

```json
{
  "start_time": 0,
  "text": "string",
  "filter": "string",
  "finish_time": 0
}
```

Returns object like

```json
{
  "start_time": 0,
  "text": "string",
  "filter": "string",
  "finish_time": 0,
  "id": 0,
  "task_id": "string"
}
```

### PUT /mailing_list/{mailing_list_id}

Accepts path parameter mailing_list_id and query parameters: start_time, text, filter, finish_time.

Returns object like

```json
{
  "start_time": 0,
  "text": "string",
  "filter": "string",
  "finish_time": 0,
  "id": 0,
  "task_id": "string"
}
```

### DELETE /mailing_list/{mailing_list_id}

Accepts path parameter mailing_list_id.

Returns object

```json
"Success"
```

### GET /message_stats/

Returns all message objects like

```json
[
  {
    "id": 0,
    "send_time": 0,
    "sent": true,
    "mailing_id": 0,
    "client_id": 0
  }
]
```

### GET /mailing_stats/

Returns all mailing_list objects and amount of messages for each of them like.

```json
[
  {
    "start_time": 0,
    "text": "string",
    "filter": "string",
    "finish_time": 0,
    "id": 0,
    "task_id": "string",
    "amount_of_messages": 0
  }
]
```

### GET /mailing_stats/{mailing_id}

Returns message objects for specified mailing_id passed as path parameter.

```json
[
  {
    "start_time": 0,
    "text": "string",
    "filter": "string",
    "finish_time": 0,
    "id": 0,
    "task_id": "string",
    "amount_of_messages": 0
  }
]
```
