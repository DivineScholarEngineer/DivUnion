# DivUnion

DivUnion is a Django-powered showcase for curated technology products. The
platform now highlights a comprehensive roadmap of capabilities so visitors can
quickly understand what the marketplace offers.

## Core Platform Features

* Curated tech catalogue with detailed product pages.
* Smart search & filtering to pinpoint the right item fast.
* AI customer support that keeps the conversation going.
* Developer dashboard for role-based insights.
* Secure account creation and profile management.

## New Experience Enhancements

1. Responsive layout across mobile, tablet and desktop breakpoints.
2. Scroll-triggered animations for a polished browsing experience.
3. Built-in cookie consent management.
4. Static export friendly configuration (django-distill).
5. Operational snapshot on the dashboard for quick stats.
6. Category-driven catalogue structure.
7. Media-ready product listing cards.
8. Optional external marketplace link support (eBay, etc.).
9. Session-aware AI conversations to preserve context.
10. Role-based access control via the developer flag.

## MySQL Setup

A ready-to-run schema is available at `scripts/mysql_schema.sql`. Execute the
script against your MySQL server and provide the connection credentials via
environment variables before starting Django:

```
export DJANGO_DB_ENGINE=mysql
export MYSQL_DATABASE=divunion
export MYSQL_USER=divunion_app
export MYSQL_PASSWORD=change-me
export MYSQL_HOST=127.0.0.1  # or your host
export MYSQL_PORT=3306
```

The application automatically falls back to SQLite when these variables are not
present. Once configured, install the Python dependencies (including PyMySQL)
and run `python manage.py migrate` to finish applying Django's built-in tables.
