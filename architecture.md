# Deejiar Architecture Document

## 1. Overview
Deejiar is a mobile travel journaling app that maps places through their signature products rather than generic ratings. It shows creative, tech-savvy travelers (aged 20-35) exactly what to order at each location. Think "Lonely Planet for the Instagram Generation" — curated locations across US, Taiwan, Singapore, and Japan with product-focused views highlighting what makes each place special.

---
## 2. System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                 │
├─────────────┬─────────────────┬─────────────┬───────────────────┤
│   iOS App   │     Web App     │    Admin    │   Landing Page    │
│ (Capacitor) │      (Vue)      │ (Datacenter)│     (Framer)      │
│             │                 │             │                   │
│ deejiar://  │ app.deejiar.com │    /admin   │  deejiar.com      │
└──────┬──────┴────────┬────────┴──────┬──────┴─────────┬─────────┘
       │               │               │                │
       └───────────────┴───────┬───────┴────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       nginx         │
                    │   (reverse proxy)   │
                    │                     │
                    │ • SSL termination   │
                    │ • Route /api → 8000 │
                    │ • Static serving    │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    FastAPI      │  │   Static/CDN    │  │    Supabase     │
│    Backend      │  │     Assets      │  │   (Direct)      │
│                 │  │                 │  │                 │
│ • Auth routes   │  │ • Map JSON      │  │ • Auth (client) │
│ • Map data      │  │ • Images        │  │ • Realtime      │
│ • Search        │  │ • Fonts         │  │                 │
│ • Webhooks      │  │                 │  │                 │
│                 │  │                 │  │                 │
│ Port: 8000      │  │ /cdn/*          │  │                 │
└────────┬────────┘  └─────────────────┘  └────────┬────────┘
         │                                         │
         └─────────────────┬───────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │      Supabase        │
                │                      │
                │ • PostgreSQL DB      │
                │ • Auth service       │
                │ • Row Level Security │
                │ • Storage (future)   │
                └──────────────────────┘
```
---
## 3. Tech Stack

| Layer        | Technology                | Version    |
|--------------|---------------------------|------------|
| **Frontend** | Vue                       | 3.5.25     |
| **Mobile**   | Capacitor                 | 7.4.2      |
| **Backend**  | FastAPI                   | 0.123.0    |
| **Database** | PostgreSQL (Supabase)     | 17.6.1.054 |
| **Auth**     | Supabase Auth             | -          |
| **Maps**     | Mapbox GL JS              | 3.6        |
| **Hosting**  | DigitalOcean (Ubuntu)     | 24.04 LTS  |
| **Server**   | nginx                     | 1.24.0     |
| **Process**  | PM2                       | 6.0.14     |
| **Email**    | Resend                    | -          |
| **Payments** | RevenueCat                | -          |
---

## 4. API Structure

### Base URL
- **PROD**: `https://deejiar.com/api`
- **QA**: `https://qa.deejiar.com/api`

### Endpoints

#### Authentication (`/api/user`)
| Method | Endpoint      | Description           |
|--------|---------------|-----------------------|
| POST   | `/login`      | User login            |
| POST   | `/signup`     | User registration     |
| POST   | `/logout`     | User logout           |
| GET    | `/me`         | Get current user      |

#### Map Data (`/api/map`)
| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| GET    | `/map/{filename}`  | Get location GeoJSON     |

#### Search (`/api/search`)
| Method | Endpoint   | Description              |
|--------|------------|--------------------------|
| GET    | `/`        | Search stores by query   |
| GET    | `?q=`      | Text search              |
| GET    | `?type=`   | Filter by type           |
| GET    | `?tags=`   | Filter by tags           |

#### Admin (`/api/admin`)
| Method | Endpoint                | Description           |
|--------|-------------------------|-----------------------|
| POST   | `/auth/login`           | Admin login           |
| GET    | `/auth/json-files`      | List JSON data files  |
| GET    | `/auth/json-data/{file}`| Get JSON file content |
| POST   | `/auth/save/{file}`     | Save JSON file        |

#### Webhooks (`/api/webhooks`)
| Method | Endpoint      | Description              |
|--------|---------------|--------------------------|
| POST   | `/revenuecat` | RevenueCat webhook       |

---

## 5. Environments

| Environment | URL                    | API Base                      | Purpose          |
|-------------|------------------------|-------------------------------|------------------|
| DEV         | `localhost:5173`       | `localhost:8000/api`          | Local dev        |
| QA          | `qa.deejiar.com`       | `qa.deejiar.com/api`          | Testing/staging  |
| PROD        | `deejiar.com`          | `deejiar.com/api`             | Live app         |
---

## 6. Project Structure

```
Deejiar/
├── api/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py               # App entry point
│   │   ├── db/
│   │   │   └── supabase.py       # Supabase client
│   │   ├── models/               # Pydantic models
│   │   ├── routes/
│   │   │   ├── user/
│   │   │   │   └── auth.py       # User auth routes
│   │   │   ├── admin/
│   │   │   │   └── auth.py       # Admin auth routes
│   │   │   ├── webhooks/
│   │   │   │   └── revenuecat.py # Webhook handlers
│   │   │   ├── map.py            # Map data routes
│   │   │   ├── search.py         # Search routes
│   │   │   └── editor.py         # JSON editor routes
│   │   ├── services/             # Business logic
│   │   └── utils/                # Helpers
│   ├── assets/                   # CDN static files
│   ├── templates/                # Email templates
│   ├── .env.local
│   ├── .env.qa
│   ├── .env.production
│   └── requirements.txt
│
├── datacenter/                   # Admin Dashboard
│
└── app/                          # Vue Frontend (Main App)
    └── src/
        ├── components/
        ├── views/
        ├── composables/
        ├── assets/
        └── main.js
```
---

## 7. Third-parties Status
Supabase: https://status.supabase.com
Resend: https://resend-status.com

**Last Updated**: December 2025  
**Version**: 1.0.0
