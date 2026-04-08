# API Documentation

## Authentication
- POST /api/users/register/
- POST /api/users/login/
- POST /api/users/token/refresh/

## User Endpoints
- GET /api/users/me/
- GET /api/users/providers/
- GET/PATCH /api/users/provider-profile/

## Service Endpoints
- GET /api/services/categories/
- GET/POST /api/services/
- GET/PATCH/DELETE /api/services/<id>/

## Booking Endpoints
- GET/POST /api/bookings/
- GET /api/bookings/<id>/
- PATCH /api/bookings/<id>/status/

## Review Endpoints
- GET/POST /api/reviews/
- GET /api/reviews/<id>/