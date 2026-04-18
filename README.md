# Gender Classify API

A lightweight REST API that predicts gender from a name using the [Genderize.io](https://genderize.io) API, with additional processing and confidence scoring.

## Endpoint

```
GET /api/classify?name={name}
```

### Success response

```json
{
  "status": "success",
  "data": {
    "name": "James",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-18T10:00:00Z"
  }
}
```

### Error response

```json
{ "status": "error", "message": "<error message>" }
```

## Status codes

| Code | Reason |
|------|--------|
| 200 | Success or no prediction available |
| 400 | Missing or empty `name` |
| 422 | `name` is not a string |
| 502 | Genderize API unreachable |

## Logic

- `sample_size` is Genderize's `count`, renamed
- `is_confident` is `true` only when `probability >= 0.7` **and** `sample_size >= 100`
- `processed_at` is generated fresh per request in UTC ISO 8601

## Setup

**Python**
```bash
pip install flask requests
python app.py
```

**Node.js**
```bash
npm install express node-fetch
node index.js
```

Server runs on `http://localhost:5000`. CORS is open (`*`).