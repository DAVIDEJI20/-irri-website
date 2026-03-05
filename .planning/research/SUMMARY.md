# Project Research Summary

**Project:** Midas Touch - Event Rental and Design Booking Website
**Domain:** Luxury event rental catalog + consultation booking (furniture, decor, tableware)
**Researched:** 2026-03-05
**Confidence:** HIGH

## Executive Summary

Midas Touch is a luxury event rental and design services business that needs a custom-built web platform to replace phone and in-person booking with self-service online transactions. The product combines two independent but complementary flows: a date-scoped rental catalog with real-time availability and Stripe checkout, and a consultation slot-booking system with an intake questionnaire. Research confirms that no existing SaaS platform (Booqable, Goodshuffle, Shopify, Webflow) adequately handles both flows with the brand control and UX quality a luxury positioning demands. A custom Next.js application with PostgreSQL is the right approach - not an off-the-shelf tool with workarounds bolted on.

The recommended stack is Next.js 14+ (App Router) on Vercel, PostgreSQL via Supabase, Prisma ORM, Tailwind CSS + shadcn/ui, Stripe for payments, and Resend + React Email for transactional email. The single most important architectural decision is the soft-hold inventory reservation pattern: inventory must be locked at checkout entry and only permanently confirmed on Stripe webhook receipt - not on the client-side redirect. Consultation booking should be built directly into the platform (custom slot picker) rather than embedded via Calendly, which cannot be styled to the luxury standard and creates a jarring aesthetic mismatch.

The two highest-risk areas are payment integrity and inventory correctness. Double bookings caused by missing inventory holds, and missed booking confirmations caused by relying on browser redirects instead of webhooks, are both industry-documented failure modes with high recovery costs. These are not edge cases - they are predictable production failures if the architecture does not account for them from the start. Both must be designed into the data model before any checkout UI is built. Secondary risks are image performance (luxury sites are photo-heavy; without CDN-based optimization, mobile load times will kill conversions) and admin panel usability (a developer-centric CRUD panel will be abandoned by the non-technical operations team).

## Key Findings

### Recommended Stack

The stack is cohesive and all choices reinforce each other. Next.js App Router provides SSR for catalog and portfolio pages (SEO-critical for a business that depends on organic discovery) and Server Actions for form handling. Supabase gives PostgreSQL with built-in auth and row-level security, eliminating the need for a separate auth service at the cost of minimal lock-in risk. Prisma makes the relational booking schema type-safe and migration-friendly as the data model evolves. Stripe is pre-decided and correct - the Payment Intents API with webhook confirmation is the right pattern. Resend + React Email provides branded transactional email on a generous free tier. Cloudinary (or Supabase Storage + Cloudflare) handles image delivery with CDN-level transformation, which is non-negotiable for a catalog-heavy luxury brand.

**Core technologies:**
- **Next.js 14+ (App Router):** Framework - SSR for SEO, Server Actions for forms, image optimization built in
- **PostgreSQL (Supabase):** Database - relational model required for inventory-booking-availability join queries; date-range queries well-supported
- **Prisma 5.x:** ORM - type-safe schema; supports migrations as booking model evolves
- **Tailwind CSS + shadcn/ui:** Styling - utility-first for custom luxury aesthetic; shadcn for accessible, re-styleable component primitives
- **NextAuth.js v5:** Auth - admin-only; credential provider for small team; no client accounts at v1
- **Stripe (SDK + Payment Intents):** Payments - full-amount checkout; webhook-driven confirmation is mandatory
- **Resend + React Email:** Email - booking and consultation confirmations, reminders; branded templates
- **Cloudinary or Supabase Storage:** Image delivery - CDN with transformation; never serve originals directly
- **Vercel:** Hosting - native Next.js deployment; zero config; edge CDN for static assets

### Expected Features

Research identifies a clear priority split. The critical path for the rental flow is: catalog items to per-item availability by date to date-scoped cart to Stripe checkout. Every item in that chain is a hard dependency; none can be skipped. The consultation flow is independent and can be built in parallel. Admin capability over both flows is needed before either can go live for real operations.

**Must have (table stakes):**
- Browsable rental catalog with categories (furniture, decor, tableware), photos, descriptions, pricing
- Per-item availability gated by event date - prevents overbooking; clients expect it
- Date-based cart tied to event date; availability re-validated at checkout
- Online checkout with full payment via Stripe - core value proposition; eliminates phone booking
- Damage waiver acceptance at checkout - protects business; low complexity; industry standard
- Order confirmation email - clients need proof of purchase; required for dispute defense
- Consultation slot booking with intake questionnaire - second core service; must be live at launch
- Consultation confirmation and reminder emails - reduces no-shows; shared email infrastructure
- Portfolio / gallery section - trust signal; consultation bookings will not happen without it
- Testimonials - event services are high-stakes; social proof is a prerequisite for conversions
- Admin: catalog management (CRUD for items, photos, pricing, availability overrides)
- Admin: unified view of rental orders and consultation bookings - team must see all commitments in one place
- Mobile-responsive design - 60-70% of browsing is mobile; non-negotiable

**Should have (competitive differentiators):**
- Pre-consultation intake questionnaire embedded in booking flow (captures event context before the meeting)
- Automatic consultation reminder emails (24-hour and 1-hour; 40-80% reported no-show reduction)
- Portfolio organized by event type (wedding, corporate, birthday - clients shop by context)
- Style-based catalog filtering (boho, modern glam; add when catalog exceeds ~30 items)
- Self-service consultation rescheduling via token link in confirmation email
- Package / bundle display with add-all-to-cart
- Item cross-sell (pairs well with) - increases average order value organically
- Wishlist / save for later - captures browse-not-ready-to-book clients

**Defer (v2+):**
- Client accounts / login portal - infrequent bookers; login friction outweighs benefit at v1
- Coupon / promo code system - adds checkout complexity; defer until marketing strategy requires it
- Multiple consultation types (30-min vs 2-hour) - defer until volume requires segmentation
- Automated post-event review requests - nice to have; not launch-critical

**Explicit anti-features (do not build):**
- Quote-request-only flow - kills the self-service value proposition
- Live Instagram embed - unreliable API; degrades page quality; use curated portfolio instead
- Dynamic demand-based pricing - confuses clients; inconsistent with luxury positioning
- Real-time multi-location inventory sync - out of scope; no current benefit

### Architecture Approach

The system is organized into five modules that map directly to user flows and build dependencies. The Public Site and Catalog modules can be built first as static/ISR pages with no payment logic. The Booking and Payment module adds the transactional layer (soft hold to Stripe to webhook to confirmed booking). The Consultation Scheduling module is independent of the rental flow and can proceed in parallel after catalog infrastructure exists. The Admin Panel is a read/write surface over data produced by both flows and should be built after both flows produce data.

**Major components:**
1. **Public Site Module** - Home, portfolio, about, contact; static/ISR; brand-first entry point
2. **Catalog and Inventory Module** - Category browsing, item detail, date-range availability picker; soft-hold reservation written at checkout entry
3. **Booking and Payment Module** - Cart, Stripe Payment Intent creation, webhook handler (payment_intent.succeeded), confirmed booking write, confirmation email
4. **Consultation Scheduling Module** - Admin-managed slot display, intake form, slot reservation, branded confirmation and reminder emails
5. **Admin Panel Module** - Unified dashboard: catalog CRUD, booking lifecycle management, consultation management, availability overrides; task-oriented workflows not raw table views

**Key architectural decisions with strong research backing:**
- Soft-hold pattern (15-min TTL reservation row in DB) prevents double bookings during payment window
- Webhook-only booking confirmation (never browser redirect) prevents orphaned payments and missed confirmations
- Custom slot picker (not Calendly embed) preserves brand consistency
- Admin-only auth at v1 (no client accounts) eliminates an entire auth surface area

### Critical Pitfalls

1. **No inventory hold during checkout (double booking)** - Must create a time-boxed soft-hold row in the database when a client enters checkout; confirm it on webhook receipt; expire it with a TTL job if payment is not completed. Use a DB-level unique constraint on the hold write. Must be in the data model before any checkout UI is built.

2. **Booking confirmation on browser redirect instead of Stripe webhook** - Mark bookings as pending at PaymentIntent creation; only confirm inside the payment_intent.succeeded webhook handler. Store processed Stripe event IDs for idempotency. Never trust the redirect. Must be built before go-live, not added later.

3. **No turnaround buffer time in availability logic** - Availability queries must treat [booking end date + configurable buffer] as the effective block end (e.g., 24-hour buffer for item inspection and repacking). Design into the schema from the start - retrofitting is painful.

4. **Image performance failure on luxury catalog pages** - Never serve original uploaded images directly. Use Next.js Image component with a CDN provider (Cloudinary or Cloudflare). Thumbnails under 200KB; hero images under 400KB. Set LCP targets before catalog pages are built. Every extra second of load reduces conversions approximately 12%.

5. **Admin panel abandoned because it was built for developers, not operations staff** - Design around daily workflows (pending bookings, confirmations due, items to update), not database table views. Test with the actual team before launch. Use shadcn/ui for quality UI without from-scratch build cost.

6. **No cancellation/refund logic enforced at code level** - Define refund policy tiers before writing the booking system. Admin panel cancellation action must auto-calculate refund amount and call stripe.refunds.create(). Policy text must be surfaced at checkout with timestamped acceptance capture - primary chargeback defense.

7. **Consultation booking aesthetic mismatch** - A generic scheduling UI embedded in a luxury site destroys brand credibility. Custom slot picker with branded cards and confirmation emails is the correct approach; verify brand consistency across all scheduling screens before launch.

## Implications for Roadmap

Based on dependency chains in the feature research and the build order confirmed by architecture research, six phases emerge. The ordering is non-negotiable in the early phases - each phase produces the data or infrastructure that the next phase requires.

### Phase 1: Infrastructure and Foundation
**Rationale:** Every subsequent phase depends on the database schema, image delivery pipeline, and environment configuration being correct from the start. Retrofitting the soft-hold pattern or adding a CDN later is painful and risky.
**Delivers:** PostgreSQL schema (items, categories, bookings, holds, consultation slots, admin users, turnaround buffer config), Prisma setup, NextAuth admin auth, Cloudinary/Supabase Storage integration, Resend email plumbing, Vercel deployment pipeline.
**Avoids:** Pitfall 1 (inventory hold must be in schema from day one), Pitfall 3 (buffer time must be in schema), Pitfall 8 (image CDN pipeline decided before catalog is built).
**Research flag:** Standard patterns - skip phase research.

### Phase 2: Rental Catalog (Browse Only)
**Rationale:** Catalog browsing is the entry point for all rental transactions and can be built without payment logic. SSR/ISR pages are well-documented Next.js patterns. Establishing the catalog gives the team real content to work with before the booking flow is wired up.
**Delivers:** Category listing pages, item detail pages (images, descriptions, pricing), basic availability display, mobile-responsive design system.
**Addresses:** Browsable catalog, high-quality photography delivery, mobile-responsive design.
**Avoids:** Pitfall 8 (image optimization enforced at catalog page level before any images go live).
**Research flag:** Standard patterns - skip phase research.

### Phase 3: Rental Booking Flow (Cart + Stripe + Confirmation)
**Rationale:** This is the highest-risk and highest-value phase. The soft-hold pattern, Stripe Payment Intents, and webhook handling must all be correct before this goes live. Feature dependencies require the full chain: availability hold to cart to Stripe to webhook to confirmed booking to confirmation email.
**Delivers:** Date-scoped cart, soft-hold reservation (15-min TTL), Stripe Payment Intent checkout, payment_intent.succeeded webhook handler with idempotency, booking confirmation in DB, damage waiver acceptance with timestamped policy capture, order confirmation email.
**Addresses:** Per-item availability by date, date-based cart, online checkout, damage waiver, order confirmation email.
**Avoids:** Pitfall 1 (soft-hold prevents double booking), Pitfall 2 (webhook-only confirmation), Pitfall 3 (refund policy captured at checkout), Pitfall 4 (chargeback evidence via policy acceptance timestamp).
**Research flag:** Needs phase research - Stripe Payment Intents webhook pattern, soft-hold TTL implementation, idempotency key strategy, concurrent booking race condition prevention at DB level.

### Phase 4: Consultation Booking Flow
**Rationale:** Consultation booking is independent of the rental flow and shares only the email infrastructure established in Phase 1. It is the second core service and must be live at launch. Building it after the rental flow ensures email infrastructure and admin data patterns are established.
**Delivers:** Admin-managed slot availability, custom branded slot picker UI, intake questionnaire (event date, type, headcount, budget, style notes), slot reservation in DB, branded confirmation email, 24-hour and 1-hour reminder emails.
**Addresses:** Consultation slot booking, intake form, confirmation and reminder emails.
**Avoids:** Pitfall 5 (consultation slots written to same DB as rental bookings for unified admin visibility), Pitfall 6 (custom slot picker maintains luxury brand aesthetic).
**Research flag:** Standard patterns - skip phase research. Custom slot picker is simpler than third-party integration; email patterns established in Phase 1.

### Phase 5: Admin Panel
**Rationale:** Admin panel requires both flows to exist and produce data. Building it last among the launch-required phases means it can be designed around real data and real workflows rather than hypothetical ones.
**Delivers:** Catalog management (CRUD for items, photos, pricing, availability overrides, turnaround buffer config), unified booking and consultation dashboard with status-driven workflow views (Pending, Confirmed, Upcoming Today, Overdue Return), booking lifecycle management (cancellation with auto-calculated Stripe refund, delivery/pickup status marking), consultation slot management.
**Addresses:** Admin catalog management, admin booking and orders view, admin consultation management.
**Avoids:** Pitfall 3 (cancellation + auto-refund logic in admin), Pitfall 4 (delivery status and evidence accessible per booking), Pitfall 5 (unified calendar view for both commitment types), Pitfall 7 (workflow-oriented panel tested with actual operations team before launch).
**Research flag:** Needs phase research - shadcn/ui admin panel component patterns, Stripe refunds.create() with partial amount calculation, role-based route protection in Next.js App Router middleware.

### Phase 6: Public Site, Portfolio, and Brand Polish
**Rationale:** Public site content does not block the core flows but must be ready before launch. Building it last allows the team to incorporate real project photography and brand decisions finalized during earlier phases.
**Delivers:** Homepage hero with brand statement and calls to action, portfolio/gallery section organized by event type, testimonials, about page, contact page, trust signals, privacy policy and rental terms.
**Addresses:** Portfolio/gallery, testimonials, contact information, privacy policy, visual brand identity.
**Avoids:** Pitfall 6 (brand consistency audit across all flows before this phase closes), Pitfall 8 (Lighthouse performance audit on portfolio pages before launch).
**Research flag:** Standard patterns - skip phase research. Content and design work; no novel integrations.

### Phase Ordering Rationale

- **Infrastructure before everything:** The soft-hold schema design, buffer time field, and image CDN pipeline cannot be added retroactively without pain. They must precede the features that depend on them.
- **Catalog before booking:** Booking requires catalog items to exist. Catalog browsing is also lower risk and provides the team with something demonstrable early.
- **Rental flow before consultation:** Rental flow is the primary revenue driver and the higher-risk integration (Stripe). Consultation flow is independent but benefits from shared email infrastructure being tested first.
- **Admin after both flows:** Admin is a read/write surface over data both flows produce. It also encapsulates the cancellation/refund logic that requires the rental flow to be complete.
- **Brand polish last:** Content and visual polish do not block anything technical. Finishing here allows real portfolio photography and brand refinement to inform the public-facing pages.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Rental Booking Flow):** Soft-hold TTL mechanism (background job vs DB-level expiry), Stripe Payment Intents vs Checkout Session trade-offs, idempotency key strategy, concurrent booking race condition prevention at DB level.
- **Phase 5 (Admin Panel):** Route-level role protection patterns in Next.js App Router middleware, Stripe refunds.create() with partial amount calculation, admin calendar component options for unified scheduling view.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Infrastructure):** Supabase + Prisma + NextAuth + Vercel are all well-documented; setup is mechanical.
- **Phase 2 (Catalog):** Next.js ISR catalog pages with image optimization are a canonical pattern; no novel integrations.
- **Phase 4 (Consultation Booking):** Custom slot picker is simpler than a third-party integration; Resend email patterns established in Phase 1.
- **Phase 6 (Portfolio and Polish):** Content and design work; no novel technical integrations.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All choices verified against official docs and well-established community consensus. NextAuth v5 is in beta - monitor for breaking changes during implementation. |
| Features | HIGH (table stakes), MEDIUM (differentiators) | Table stakes confirmed by multiple rental industry sources. Consultation scheduling UX patterns have fewer reference points. |
| Architecture | HIGH | Soft-hold pattern, webhook-driven confirmation, and modular build order are all validated by Stripe docs and rental domain sources. |
| Pitfalls | HIGH | Critical pitfalls (double booking, redirect-based confirmation) are documented failure modes with Stripe documentation and rental software industry sources as primary evidence. |

**Overall confidence:** HIGH

### Gaps to Address

- **Consultation slot granularity:** Research recommends a custom slot picker but does not define how granular slots should be (30-min increments vs half-day vs full-day windows). Needs clarification with the client team before Phase 4 begins.
- **Turnaround buffer value:** The 24-hour buffer is used as an example in research. The actual value (e.g., 48 hours for large furniture, 12 hours for tableware) requires input from the operations team before the schema is finalized in Phase 1.
- **Initial catalog size at launch:** The style-based filtering recommendation triggers at approximately 30 items. If the launch catalog exceeds 30 items, style filtering should move from v1.x to v1.
- **Cancellation/refund policy tiers:** The actual policy (e.g., full refund more than 14 days out, 50% within 7 days, none within 48 hours) must be defined by the business before Phase 3 checkout or Phase 5 admin panel can implement the calculation logic.
- **NextAuth v5 stability:** Next-auth v5 is listed as beta. Verify current stability before Phase 1 begins; fall back to v4 if critical issues are documented.

## Sources

### Primary (HIGH confidence)
- Stripe Documentation (Payment Intents, Webhooks, Refunds, Disputes) - payment flow, webhook pattern, idempotency, chargeback evidence requirements
- Supabase Documentation - PostgreSQL + auth + storage setup
- Next.js 14 App Router Documentation - SSR, Server Actions, image optimization
- Prisma 5 Documentation - schema design, migrations, date-range queries

### Secondary (MEDIUM confidence)
- Goodshuffle Pro Blog (2026 Event Rental Trends, Inventory Management 101) - domain feature expectations
- Booqable Blog (Preventing Double Bookings) - soft-hold availability pattern validation
- TwiceCommerce Blog (Real-Time Rental Availability) - inventory hold race condition documentation
- Path and Compass (Website Checklist for Rental Companies) - table stakes feature validation
- RW Elephant Blog (Five Mistakes Event Rental Pros Make) - operational pitfall validation
- Rentopian (Avoid Overbooking Inventory) - buffer time / turnaround operational requirement
- Triotech Labs / Marketing LTB (Speed Impact on Conversions 2025) - image performance urgency
- Stigg Blog (Stripe Webhook Best Practices) - webhook idempotency implementation
- Hookdeck (Implement Webhook Idempotency) - idempotency key strategy

### Tertiary (LOW confidence)
- Colorlib (Event Planner Website Design Examples) - luxury design pattern reference; purely visual
- Acuity Scheduling (Calendly Alternatives) - scheduling tool comparison; used to confirm Calendly aesthetic limitations

---
*Research completed: 2026-03-05*
*Ready for roadmap: yes*
