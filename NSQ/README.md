# NSQ

Flask app for NSQ.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python server.py
```

Open `http://127.0.0.1:5000`.

## Deploy on Vercel

Vercel can detect `server.py` because it exports a Flask `app` instance.

Set these environment variables in Vercel if you use email or sessions:

- `SECRET_KEY`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `MAIL_ACCOUNTS` optional, format `email1:password1;email2:password2`

SQLite data on Vercel is temporary. For a real deployed app, replace it with a hosted database.
