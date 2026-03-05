# Architecture Research

**Domain:** Event rental and design booking website
**Researched:** 2026-03-05
**Confidence:** HIGH (patterns verified against multiple official/authoritative sources)

## Standard Architecture

### System Overview

```
+---------------------------------------------------------------------+
|                       CLIENT LAYER (Browser)                         |
+---------------+------------------+--------------+-------------------+
|  Public Site  |  Rental Catalog  |  Booking UI  |   Admin Panel     |
|  (Portfolio,  |  (Browse, Filter,|  (Cart, Date |   (Inventory,     |
|   Gallery)    |   Item Detail)   |   Picker,    |    Bookings,      |
|               |                  |   Checkout)  |    Schedule)      |
+-------+-------+--------+---------+------+-------+---------+---------+
        |                |                |                 |
        |    Next.js App Router (SSR + Server Actions + API Routes)
        |                |                |                 |
+-------+-------+---------+--------+-------+-------+---------+---------+
|  Content      |  Catalog &       |  Booking &    |   Auth &          |
|  Module       |  Inventory       |  Payment      |   Admin           |
|  (Static/ISR) |  Module          |  Module       |   Module          |
+---------------+--------+---------+-------+--------+-------------------+
                         |                 |
              +----------+-----------------+----------+
              |         DATA LAYER (PostgreSQL)         |
              |  +----------+  +----------+            |
              |  | Catalog  |  |Bookings/ |            |
              |  |Inventory |  |Schedules |            |
              |  +----------+  +----------+            |
              +-------------------------------------------+
                         |                 |
              +----------+---+   +---------+----------+
              |   Stripe     |   |  Email (Resend/    |
              |  (Payments)  |   |   Nodemailer)      |
              +--------------+   +--------------------+
```

## Component Breakdown

### Public Site Module
- Home page (hero, brand statement, call to action)
- Portfolio/gallery (past events, curated images)
- About page
- Contact page

### Catalog & Inventory Module
- Category browsing (Furniture, Decor & Props, Tableware)
- Item detail page (images, description, pricing, availability picker)
- Availability: date-range query against bookings table + soft-hold TTL on cart

### Booking & Payment Module
- Cart (selected items + dates)
- Soft inventory hold (TTL reservation created on cart, released if checkout not completed)
- Stripe checkout (Payment Intent, full amount)
- Webhook handler (`payment_intent.succeeded`) → confirms booking in DB
- Booking confirmation email (Resend)

### Consultation Scheduling Module
- Available slot display (admin-managed slots in DB)
- Intake form (event date, type, headcount, budget, style notes)
- Slot reservation + confirmation email
- Admin notification email

### Admin Panel Module
- Catalog management (add/edit/delete items, upload images, set pricing)
- Availability management (mark dates unavailable, set turnaround buffer)
- Booking management (view, cancel, track delivery/return status)
- Consultation management (view scheduled consultations, manage available slots)
- Multi-user access (small team, role-based: admin vs staff)

## Data Flow

```
Client selects items + dates
  → Soft-hold created in DB (TTL: 15 min)
  → Stripe Payment Intent created
  → Client completes payment
  → Stripe fires webhook: payment_intent.succeeded
  → Webhook handler confirms booking, releases hold, sends confirmation email

Client selects consultation slot
  → Slot marked reserved in DB
  → Intake form submitted
  → Confirmation email sent to client
  → Notification email sent to admin team
```

## Build Order (Dependency Chain)

1. **Infrastructure** — DB schema, auth, image storage, email setup
2. **Catalog browsing** — Items, categories, detail pages (no booking yet)
3. **Rental booking flow** — Cart, availability hold, Stripe payment, webhooks, confirmation
4. **Consultation scheduling** — Slot picker, intake form, emails
5. **Admin panel** — Manage catalog, bookings, slots (needs data from steps 2-4)
6. **Portfolio & brand polish** — Gallery, testimonials, homepage hero

## Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Soft-hold pattern for inventory | Prevents double-booking during payment window |
| Webhook-only booking confirmation | Prevents orphaned payments from redirect-based confirmation |
| Admin-only auth (no client accounts) | Clients are infrequent bookers; login adds friction without value at v1 |
| Custom slot picker vs Calendly embed | Brand control; Calendly cannot be styled to luxury standard |
