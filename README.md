# ServiceTap Backend

Backend API for **ServiceTap** — an “Uber for Services” platform that connects customers with local service providers such as plumbers, electricians, tutors, and cleaners.

This project is built with **Django**, **Django REST Framework**, **PostgreSQL**, **Redis**, **Celery**, **Gunicorn**, and **Nginx**. It provides authentication, provider profiles, service listings, bookings, and reviews, together with interactive API documentation. 

---

## Features

- JWT authentication for users
- Separate customer and provider roles
- Provider profile management
- Service categories and service listings
- Search, filtering, and ordering for services
- Booking creation and status updates
- Review system for completed bookings
- OpenAPI schema and Swagger documentation
- Celery worker and Celery Beat for background tasks
- PostgreSQL for persistent data
- Redis as Celery broker/result backend

---

## Tech Stack

- **Python 3.12**
- **Django 6**
- **Django REST Framework**
- **PostgreSQL 16**
- **Redis 7**
- **Celery 5**
- **Gunicorn**
- **Nginx**
- **Docker Compose**

---

## Project Structure

```text
uber-services-platform/
├── backend/
│   ├── bookings/
│   ├── core/
│   │   ├── settings/
│   │   ├── celery.py
│   │   └── urls.py
│   ├── reviews/
│   ├── services/
│   ├── users/
│   ├── manage.py
│   ├── gunicorn.conf.py
│   ├── requirements.txt
│   └── schema.yml
├── nginx/
│   └── default.conf
├── docker-compose.yml
├── dockerfile
├── API_DOCUMENTATION.md
└── README.md
```

---

## Main Modules

### Users
- User registration
- JWT login and token refresh
- Current authenticated user endpoint
- Provider profile update
- Provider listing

### Services
- Category listing
- Service CRUD for providers
- Public service listing with filtering, search, and ordering

### Bookings
- Customers can create bookings
- Customers and providers can view their own bookings
- Providers can update booking status
- Scheduled background task cancels expired pending bookings

### Reviews
- Public review listing and retrieval
- Customers can leave reviews for completed bookings

---

## API Endpoints

### Authentication
- `POST /api/users/register/`
- `POST /api/users/login/`
- `POST /api/users/token/refresh/`

### User Endpoints
- `GET /api/users/me/`
- `GET /api/users/providers/`
- `GET/PATCH /api/users/provider-profile/`

### Service Endpoints
- `GET /api/services/categories/`
- `GET/POST /api/services/`
- `GET/PATCH/DELETE /api/services/<id>/`

### Booking Endpoints
- `GET/POST /api/bookings/`
- `GET /api/bookings/<id>/`
- `PATCH /api/bookings/<id>/status/`

### Review Endpoints
- `GET/POST /api/reviews/`
- `GET /api/reviews/<id>/`

### API Docs
- `GET /api/schema/`
- `GET /api/docs/`

---

## Business Logic Summary

### User roles
The application uses a custom `User` model with at least two roles:
- `customer`
- `provider`

Providers can also have a profile and a verification flag.

### Services
A service belongs to a category and a provider. Services support pricing modes such as:
- fixed
- hourly
- negotiable

The service list supports filtering, search, ordering, and rating-based filtering.

### Bookings
A booking is created by a customer for a selected service. When a booking is created, the backend automatically assigns:
- the service provider
- the estimated price from the service price

### Reviews
A review can be created by a customer for a completed booking. When a review is saved, the backend automatically links the review to the relevant provider and service.

---

## Environment Variables

Create a file at:

```bash
backend/.env
```

Example:

```env
SECRET_KEY=change-me
DEBUG=False

DB_NAME=service_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

### Notes
- In Docker, the database host should be `db`.
- In Docker, the Redis host should be `redis`.
- For local development without HTTPS, keep `SECURE_SSL_REDIRECT=False`.
- Production settings are enabled in Docker by default through `DJANGO_SETTINGS_MODULE=core.settings.prod`.

---

## Running the Server with Docker on a Local Machine

There are **two important things** to fix before the project can run smoothly on localhost:

1. In `docker-compose.yml`, the services reference `Dockerfile`, but the repository file is currently named `dockerfile`.
2. `nginx/default.conf` is configured for the production Azure domain and expects existing Let’s Encrypt SSL certificates, so it is **not suitable for localhost out of the box**.

### Option A — Recommended local setup
Run the backend stack **without Nginx and Certbot**. This is the easiest way to run locally.

### Step 1: Clone the repository
```bash
git clone https://github.com/Sayid03/uber-services-platform.git
cd uber-services-platform
```

### Step 2: Create the environment file
Create `backend/.env` using the example above.

### Step 3: Start only the local services
```bash
docker compose up --build db redis web celery celery-beat
```

### Step 4: Open the API
The Django app runs on port `8000` inside the `web` container, but in the current compose file it is only exposed to other containers, not to your host machine.

So for localhost access you should add this to the `web` service in `docker-compose.yml`:

```yaml
ports:
  - "8000:8000"
```

Then restart:

```bash
docker compose up --build db redis web celery celery-beat
```

Now open:

- API root: `http://localhost:8000/api/`
- Swagger docs: `http://localhost:8000/api/docs/`
- Admin panel: `http://localhost:8000/admin/`

### Step 5: Create a superuser
In another terminal:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Running with Nginx Locally

If you want to run the full stack with Nginx locally, you need to adjust `nginx/default.conf`.

### What to change
Replace the production-only config with a simpler localhost config like this:

```nginx
server {
    listen 80;
    server_name localhost;

    client_max_body_size 20M;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This version:
- removes HTTPS requirements
- removes Let’s Encrypt certificate paths
- works for localhost over plain HTTP

Then you can run:

```bash
docker compose up --build
```

And open:

- `http://localhost/`
- `http://localhost/api/docs/`

---

## Useful Docker Commands

### Start containers
```bash
docker compose up --build
```

### Start in background
```bash
docker compose up --build -d
```

### Stop containers
```bash
docker compose down
```

### Stop and remove volumes
```bash
docker compose down -v
```

### View logs
```bash
docker compose logs -f
```

### View logs for one service
```bash
docker compose logs -f web
```

### Run migrations manually
```bash
docker compose exec web python manage.py migrate
```

### Collect static files manually
```bash
docker compose exec web python manage.py collectstatic --noinput
```

---

## Local Development Notes

- The current Docker setup uses **production settings** for the `web`, `celery`, and `celery-beat` services.
- For quick local debugging, you may prefer development settings by changing:

```yaml
environment:
  DJANGO_SETTINGS_MODULE: core.settings.prod
```

to:

```yaml
environment:
  DJANGO_SETTINGS_MODULE: core.settings.dev
```

- If you do that, update database and Redis host values accordingly if needed.
- Static files are served with WhiteNoise.
- Media files are stored in `backend/media` through the named Docker volume.

---

## Example Service Capabilities

The backend already supports several useful API behaviors:

- service search by title, description, location, and provider username
- ordering by creation date, price, title, average rating, and review count
- filtering bookings by status, service, and provider
- filtering reviews by provider, service, and rating

---

## Scheduled Tasks

Celery Beat is configured to run a recurring task that cancels expired pending bookings every 30 minutes.

---

## Documentation

Additional endpoint notes are also available in:

```text
API_DOCUMENTATION.md
```

Interactive schema and Swagger docs are available from the running server at:

```text
/api/schema/
/api/docs/
```

---

## License

This project is licensed under the **MIT License**.

---

## Suggested Future Improvements

- add an `.env.example` file to the repository
- add Docker profiles for local vs production
- provide a separate localhost Nginx config
- add seed data for categories and demo users
- add automated tests and CI checks
- document request/response examples for each endpoint
