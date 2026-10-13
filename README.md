# User Management System

A full-stack User Management application. The Angular frontend lets you list, search, add, edit and delete users. The FastAPI backend exposes a REST API and stores the data in MySQL.

Author: Sahil Sadashiv Gaikwad

## Features

- List all users in a table (cards on mobile screens)
- Add a new user, edit an existing user, delete a user (with a confirmation prompt)
- Search by name or email
- Validation on the form (Angular) and on the API (Pydantic), plus MySQL constraints
- Duplicate email protection (API returns `409`, the form shows the message)
- Clear success and error messages
- Responsive layout for desktop and mobile
- Configuration through environment variables (`.env`)

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Angular (standalone components, `HttpClient`, routing) |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| Database | MySQL 8, accessed with PyMySQL and parameterized queries |

Tested with: Python 3.14.8, MySQL 8.0.46, Node.js 24.21.0, Angular CLI 22.2.2, npm 11.19.0, Windows 64-bit

## Project structure

```
user-management/
├── backend/
│   ├── main.py            # creates the app, CORS, error handler
│   ├── database.py        # MySQL connection (reads .env)
│   ├── schemas.py         # Pydantic validation models
│   ├── models.py          # SQL functions (parameterized queries)
│   ├── routes/
│   │   └── users.py       # the 5 API endpoints
│   ├── test_db.py         # checks the database connection
│   ├── test_schemas.py    # checks validation rules
│   ├── test_crud.py       # checks the SQL functions
│   ├── requirements.txt
│   └── .env.example
├── database/
│   └── schema.sql         # creates the database and users table
├── frontend/
│   └── user-management-ui/
│       └── src/app/
│           ├── components/
│           │   ├── user-list/
│           │   └── user-form/
│           ├── models/user.model.ts
│           ├── services/user.service.ts
│           └── app.routes.ts
└── screenshots/
    ├── API/                       # Swagger UI evidence (GET, POST, PUT, DELETE)
        ├── GET/
        ├── POST/
        ├── PUT/
        └── DELETE/
    └── frontend/                  # Angular screens
        ├── user-list component/
        ├── add-edit screenshot/
        ├── laptop responsive/
        └── mobile responsive/
```

## Prerequisites

- Python 3.10 or newer
- MySQL Server 8 (and optionally MySQL Workbench)
- Node.js and npm
- Angular CLI: `npm install -g @angular/cli`

## 1. Database setup

1. Start MySQL and run the script `database/schema.sql`. In MySQL Workbench: open the file and execute it. From a terminal:

   ```bash
   mysql -u root -p < database/schema.sql
   ```

   This creates the database `fresher_assignment` and the `users` table.

2. Create a MySQL user for the application (replace the password):

   ```sql
   CREATE USER 'fresher_app'@'localhost' IDENTIFIED BY 'your_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON fresher_assignment.* TO 'fresher_app'@'localhost';
   ```

   You can also use an existing MySQL user that has access to `fresher_assignment`.

## 2. Backend setup

From the project root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```

On macOS or Linux, activate with `source venv/bin/activate` instead.

### Configuration

Copy the example file and fill in your own values:

```powershell
copy .env.example .env             # Windows  (macOS/Linux: cp .env.example .env)
```

| Variable | Meaning | Example |
|---|---|---|
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `fresher_app` |
| `DB_PASSWORD` | Password of that user | `your_password` |
| `DB_NAME` | Database name | `fresher_assignment` |
| `CORS_ORIGINS` | Allowed frontend addresses, comma separated (optional) | `http://localhost:4200,http://127.0.0.1:4200` |

The `.env` file holds secrets and is not committed to Git.

### Run the backend

```powershell
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI (interactive API docs): http://127.0.0.1:8000/docs

### Optional checks

```powershell
python test_db.py        # prints "Connected OK"
python test_schemas.py   # validation rules
python test_crud.py      # SQL functions (uses a temporary test user)
```

## 3. Frontend setup

In a second terminal, with the backend running:

```powershell
cd frontend/user-management-ui
npm install
ng serve
```

Open http://localhost:4200. The app redirects to the user list at `/users`.

The API address is set in `src/app/services/user.service.ts` (`baseUrl`, default `http://localhost:8000/api/users`).

## API endpoints

| Method | URL | Purpose | Success | Errors |
|---|---|---|---|---|
| POST | `/api/users` | Create a user | 201 | 409 duplicate email, 422 invalid data |
| GET | `/api/users` | List users (optional `?search=`) | 200 | |
| GET | `/api/users/{user_id}` | Get one user | 200 | 404 not found |
| PUT | `/api/users/{user_id}` | Update a user (full replace) | 200 | 404, 409, 422 |
| DELETE | `/api/users/{user_id}` | Delete a user | 200 | 404 |

Example request body for `POST /api/users`:

```json
{
  "first_name": "Rahul",
  "last_name": "Sharma",
  "email": "rahul.sharma@example.com",
  "phone": "9876543210",
  "gender": "Male",
  "date_of_birth": "2002-05-15",
  "department": "Engineering",
  "designation": "Junior Developer",
  "status": "Active"
}
```

## Validation rules

| Field | Rule |
|---|---|
| `first_name`, `last_name` | Required, 1 to 100 characters |
| `email` | Required, valid format, unique, up to 255 characters |
| `phone` | Optional, 10 to 15 digits, optional leading `+` |
| `gender` | Optional: `Male`, `Female` or `Other` |
| `date_of_birth` | Optional, a valid date, not in the future |
| `department`, `designation` | Optional, up to 100 characters |
| `status` | `Active` or `Inactive` (default `Active`) |

Invalid data returns `422`, a duplicate email returns `409`, and an unknown user returns `404`. Unexpected database errors return a generic `500` message while the details are written to the server log.


## Security notes

- All SQL uses parameterized queries (`%s` placeholders), which prevents SQL injection.
- The application connects with a MySQL user that can only read and write rows in one database.
- Passwords and settings live in `.env`, which is ignored by Git.

## Screenshots and testing evidence

## Screenshots and testing evidence

- `screenshots/API/`: Swagger UI tests of each endpoint (`GET`, `POST`, `PUT`, `DELETE`), including 404, 409 and 422 cases
- `screenshots/frontend/user-list component/`: the user list
- `screenshots/frontend/add-edit screenshot/`: add and edit forms, validation messages, duplicate email message
- `screenshots/frontend/laptop responsive/` and `screenshots/frontend/mobile responsive/`: desktop and mobile layouts


## Troubleshooting

| Problem | Fix |
|---|---|
| `Access denied for user` | The `DB_USER` or `DB_PASSWORD` in `.env` is wrong |
| `Unknown database` | Run `database/schema.sql` first |
| `Can't connect to MySQL server` | Start the MySQL service and check `DB_HOST` and `DB_PORT` |
| Red CORS error in the browser console | Add the Angular address to `CORS_ORIGINS` in `.env` and restart the backend |
| The list shows "Could not load users" | The backend is not running on port 8000 |
| PowerShell blocks `Activate.ps1` | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once |


