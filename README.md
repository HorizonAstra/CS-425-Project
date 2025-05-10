# CS-425-Project
# Real-Estate Management Application  


---

## 1 · Instant demo with Docker Compose

> **Requires only Docker Desktop** (or plain Docker + Compose v2).

```bash
git clone https://github.com/<your-org>/<repo>.git
cd <repo>
docker compose up --build
```













###IGNORE


| Step | Command / Action                                                                                              | Expected                                                        |
| ---- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 0-1  | `git clone HorizonAstra/CS-425-Project`                                                                       | Source code present                                             |
| 0-2  | `cd realestate_app`                                                                                           | —                                                               |
| 0-3  | `python -m venv venv`  → `venv\Scripts\activate`                                                              | Prompt shows **(venv)**                                         |
| 0-4  | `pip install -r requirements.txt`                                                                             | No errors                                                       |
| 0-5  | Ensure Postgres is running; create role & db.                                                                 | `realestate_db` exists                                          |
| 0-6  | `set FLASK_APP=app.py`<br>`set DATABASE_URL=postgresql://realestate_user:StrongPass!@localhost/realestate_db` | —                                                               |
| 0-7  | `flask db upgrade`                                                                                            | Tables created                                                  |
| 0-8  | `flask run`                                                                                                   | Dev server @ **[http://127.0.0.1:5000](http://127.0.0.1:5000)** |




