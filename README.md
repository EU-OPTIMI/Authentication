# Auth Service

Session-based authentication service built with Django + DRF. Provides login/logout/profile endpoints and an HTML login page for redirects.

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
```

Environment (`.env`):
```
SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://localhost:8001
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:8001
SESSION_COOKIE_NAME=sessionid
```

## Users
- Create a superuser: `python manage.py createsuperuser`
- Admin UI: log in at `http://localhost:8001/admin/` to create regular users.

## Endpoints
- `POST /api/auth/login/` – Session login (username/email + password)
- `POST /api/auth/logout/` – Session logout
- `GET /api/auth/me/` – Profile (requires session)
- `GET /api/auth/login-page/?next=<return_url>` – HTML login page for redirects

## Example: login + profile with curl
```bash
# 1) Get a CSRF cookie
curl -s -c cookies.txt http://localhost:8001/api/auth/login-page/ >/dev/null

# 2) Extract csrftoken
CSRF=$(awk '$6=="csrftoken"{print $7}' cookies.txt | tail -n1)

# 3) Login (replace creds)
curl -i -b cookies.txt -c cookies.txt \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -X POST http://localhost:8001/api/auth/login/ \
  -d '{"username":"youruser","password":"yourpass"}'

# 4) Profile (should return 200 + JSON)
curl -i -b cookies.txt http://localhost:8001/api/auth/me/
```

## Integrate from another service (e.g., on :8000)
- Base: `http://localhost:8001`
- Send cookies with `credentials: 'include'` (frontend) or forward `sessionid` server-side.
- Auth check: call `/api/auth/me/`. On 403, redirect to `/api/auth/login-page/?next=<original_url>`.
- Login/logout POSTs must include `X-CSRFToken` from the `csrftoken` cookie.
