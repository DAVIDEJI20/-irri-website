# Midas Touch

## What This Is

Midas Touch is a website for an existing event design business that offers two core services: self-service rental of decor, furniture, and tableware, and consultation-based event design bookings. Clients can browse the rental catalog, book and pay for items online, or schedule a consultation to plan a full event.

## Core Value

Clients can discover, book, and pay for rentals — or schedule an event consultation — entirely online, without needing to call.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Clients can browse rental catalog (furniture, decor & props, tableware)
- [ ] Clients can select rental items, choose dates, and pay in full online
- [ ] Clients can book a consultation slot for event design services
- [ ] Admin team can manage catalog inventory and view/manage bookings
- [ ] Website showcases Midas Touch's portfolio to build trust and win clients

### Out of Scope

- Mobile app — web-first, responsive design covers mobile use
- Deposit-based payments — full payment upfront selected for v1
- Real-time inventory tracking across multiple locations — single inventory source for now

## Context

- Existing business moving online; clients currently book by phone/in-person
- Two distinct user flows: rental self-service (transactional) and event consultation (relationship-based)
- Small team needs admin access to manage catalog items, availability, and bookings
- Visual presentation is critical — this is a design business; the site itself is a portfolio statement
- Consultation booking should work like a scheduling tool (Calendly-style slot selection)

## Constraints

- **Payments**: Full online payment for rentals via a payment processor (Stripe or similar)
- **Admin**: Multi-user admin panel for team to manage catalog and bookings
- **Design**: High-quality visual design reflecting the "Midas Touch" luxury/gold brand identity

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Full payment upfront for rentals | Simpler flow, no follow-up collection needed | — Pending |
| Consultation booking (not package selection) for events | Events are custom; consultation scopes before committing | — Pending |

---
*Last updated: 2026-03-05 after initialization*
