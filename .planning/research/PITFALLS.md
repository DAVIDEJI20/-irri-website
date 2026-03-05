# Pitfalls Research

**Domain:** Event rental and design booking website (Midas Touch)
**Researched:** 2026-03-05
**Confidence:** HIGH (critical paths verified via Stripe docs, rental industry sources, and booking system patterns)

---

## Critical Pitfalls

### Pitfall 1: Inventory Not Held During Checkout -- Double Bookings Are Inevitable

**What goes wrong:**
A client adds items to their cart and completes payment. Simultaneously, a second client books the same items for the same date range. Both payments succeed. You are now committed to fulfilling the same inventory twice on the same date.

**Why it happens:**
Developers check availability at the "add to cart" step but never hold (lock) that inventory during the checkout window. Between the moment a client selects dates and the moment payment completes, the inventory record remains available to other sessions. At event rental scale -- even with only dozens of simultaneous visitors -- this window is long enough to trigger conflicts.

**How to avoid:**
Use a two-phase reservation model:
1. Soft hold -- when the client enters checkout, write a time-boxed reservation row (e.g., 15-minute TTL) that blocks those items on those dates from appearing available to anyone else.
2. Confirm hold -- on payment_intent.succeeded webhook, convert the soft hold to a confirmed booking.
3. Release hold -- if the TTL expires with no payment, a background job deletes the soft hold and the items become available again.

Use a database-level unique constraint or row locking on the availability check+hold write to prevent two concurrent sessions from both creating soft holds for the same item on the same dates.

**Warning signs:**
- Availability check and booking write are two separate, unguarded database operations
- No "reservation" or "hold" table exists in the schema -- only "bookings"
- Cart page shows item as available to new sessions even while another user is mid-checkout

**Phase to address:** Booking and inventory data model phase (foundation); must be designed before any checkout UI is built.

---

### Pitfall 2: Fulfilling Orders Based on the Payment Success Redirect, Not the Stripe Webhook

**What goes wrong:**
The booking confirmation page fires when the client's browser returns from Stripe Checkout. The developer marks the booking as confirmed at that point. If the client closes their browser before returning, or if the redirect fails, the booking is never confirmed in the database -- even though payment succeeded. Conversely, if a network glitch causes the redirect to fire twice, the booking is confirmed twice.

**Why it happens:**
Client-side redirects feel intuitive and work in happy-path testing. Webhook handling requires server infrastructure, signature verification, and idempotency logic that developers often defer or skip.

**How to avoid:**
- Mark bookings as pending when the PaymentIntent is created.
- Only mark bookings as confirmed inside the payment_intent.succeeded or checkout.session.completed webhook handler.
- Make the webhook handler idempotent: store processed Stripe event IDs; skip re-processing if the event ID is already in the database.
- Return 200 OK immediately after signature verification; process the booking state change asynchronously if it takes time.
- Never trust the redirect as the source of truth.

**Warning signs:**
- Booking confirmation logic lives in the success page route handler rather than a webhook endpoint
- No stripe_event_id column (or equivalent) stored in the database to detect duplicates
- Webhook endpoint is not registered in the Stripe dashboard during development

**Phase to address:** Stripe payment integration phase; webhook handling must be built before going live, not added afterward.

---

### Pitfall 3: No Cancellation and Refund Policy Enforced at the Code Level

**What goes wrong:**
The business decides its policy (e.g., full refund if cancelled 14+ days before event, 50% within 7 days, no refund inside 48 hours), but this logic is never implemented in the admin panel or the booking system. Refunds are processed manually by logging into Stripe directly. Clients dispute charges claiming the cancellation policy was unclear. The admin team has no consistent process.

**Why it happens:**
Refund policy enforcement feels like a "later" problem during initial build. Developers focus on the happy path (booking succeeds) and defer cancellation flows.

**How to avoid:**
- Design the cancellation/refund rules as explicit business logic with defined tiers before writing the booking system.
- Build a cancellation action in the admin panel that automatically calculates the correct refund amount based on days until the event and calls stripe.refunds.create() with the correct amount.
- Show the cancellation policy clearly on the booking confirmation page and in confirmation emails -- this is your primary chargeback defense.
- Store the policy version accepted at booking time so disputes can reference it.

**Warning signs:**
- No cancellation flow in the admin panel -- refunds are done by logging directly into Stripe
- Refund amounts are manually entered each time (no calculation logic)
- Policy text is only in a terms-of-service page, not surfaced at checkout

**Phase to address:** Admin panel phase and checkout flow phase (policy acceptance checkpoint).

---

### Pitfall 4: Stripe Chargebacks for Physical Rental Goods Are Hard to Win Without Documented Evidence

**What goes wrong:**
A client files a chargeback claiming "services not rendered" or "item not as described" after using rented decor. Stripe's 2025 dispute fee model charges an additional counter fee when a merchant contests, plus Smart Disputes takes 30% of recovered amounts. Without evidence (delivery records, signed pickup agreements, photo documentation), the merchant loses.

**Why it happens:**
Event rental is a physical goods service -- there is no digital delivery confirmation. Developers building the booking system do not think about the evidentiary trail needed to win a dispute six months later.

**How to avoid:**
- Build a delivery/pickup acknowledgment into the admin workflow: admin marks items as "delivered" or "picked up" with a timestamp.
- Store photos of item condition at pickup and return in the booking record.
- Surface the rental agreement and damage policy at checkout (not buried in terms of service) and capture a checkbox acknowledgment with timestamp.
- Keep the accepted cancellation/refund policy text archived per booking -- Stripe dispute evidence form requires this.

**Warning signs:**
- No "delivered" or "returned" status states in the booking lifecycle
- No documentation attachment capability in the admin panel
- Policy only in a generic terms page, not tied to individual bookings

**Phase to address:** Admin panel phase (booking lifecycle states) and checkout phase (policy acceptance evidence).

---

### Pitfall 5: Consultation Booking Slots Not Unified with Rental Bookings -- Scheduling Collisions

**What goes wrong:**
The consultation scheduler and the rental booking system share no data, so the admin team is simultaneously looking at two separate dashboards. A consultation is booked for 2pm Friday; a rental pickup is also scheduled for 2pm Friday. No conflict is surfaced. The team discovers collisions by accident.

**Why it happens:**
Rental bookings and consultation slots are implemented as entirely separate systems (often using a third-party scheduler like Calendly for consultations and a custom system for rentals). Integration between them is an afterthought.

**How to avoid:**
- If using a third-party scheduling tool for consultations (Calendly or Cal.com), mirror confirmed consultations into the main admin view as blocked time slots.
- Design the admin dashboard to show all commitments -- rentals and consultations -- in a unified calendar view.
- Alternatively, build the consultation slot system directly into the same platform as the rental system (simpler for a small team).

**Warning signs:**
- Two separate logins for consultation schedule and rental bookings
- No unified calendar view in the admin panel
- Admin team manually cross-referencing two separate tools

**Phase to address:** Admin panel design phase (unified scheduling view).

---

### Pitfall 6: Consultation Booking Flow Feels Transactional -- Mismatches the Luxury Brand

**What goes wrong:**
The consultation scheduler shows a generic date/time grid (Calendly default aesthetic) embedded in a gold-and-white luxury website. The mismatch in visual quality signals to high-end clients that the business is not as polished as it presents. Conversion rates on consultation requests drop.

**Why it happens:**
Developers integrate the fastest scheduling solution without customizing the visual presentation. Luxury clients are more sensitive to visual consistency than typical SaaS users.

**How to avoid:**
- If using a third-party scheduler, use one with extensive white-labeling support (Cal.com self-hosted or Calendly paid tiers), and ensure the booking widget is styled to match the Midas Touch brand.
- Alternatively, build a simple custom slot selector -- a curated set of available windows displayed as elegant cards, not a generic calendar grid -- that matches the brand tone.
- The confirmation experience (email, page) must match the brand: custom email template, Midas Touch logo, gold accents, personalized copy.

**Warning signs:**
- Generic Calendly embed with no custom color or logo applied
- Confirmation emails sent from a noreply@calendly.com address
- The scheduling modal breaks the page layout on mobile

**Phase to address:** Consultation booking phase and visual design phase (brand consistency audit).

---

### Pitfall 7: Admin Panel Built for Developers, Not for the Small Non-Technical Team Using It Daily

**What goes wrong:**
The admin panel exposes raw data in table rows, requires multiple clicks to accomplish common tasks (confirm a booking, mark items as returned, add a new catalog item), and has no inline status indicators. The Midas Touch team abandons the admin panel and reverts to phone/spreadsheet workflows.

**Why it happens:**
Admin panels are built as CRUD interfaces because that is what frameworks generate quickly. Developers think in terms of database records; operations staff think in terms of tasks ("confirm today's delivery" or "add three new vases to the catalog").

**How to avoid:**
- Design the admin panel around workflows, not tables. Primary views: Today's bookings, Pending confirmations, Inventory that needs updating.
- Limit the initial admin panel to what the team actually needs for day-one operations. Do not build features preemptively.
- Test the admin panel with the actual team before launch -- watch them try to complete a real task without guidance.
- Use a component library (shadcn/ui or similar) for quick, high-quality UI rather than building from scratch.

**Warning signs:**
- Admin panel design review involves only developers
- No walkthrough session with the actual operations team before launch
- Every common task requires navigating to three different pages

**Phase to address:** Admin panel phase; incorporate workflow review with the client team before building.

---

### Pitfall 8: Luxury Visual Design Kills Performance -- Image-Heavy Pages Load Slowly

**What goes wrong:**
The portfolio and catalog pages feature large, high-resolution photos (appropriate for a luxury brand). These images are served without optimization: full-size JPEGs, no lazy loading, no WebP format. Page load times exceed 5 seconds on mobile. Every extra second of load time reduces conversion rates by approximately 12%. The luxury aesthetic undermines itself.

**Why it happens:**
Designers hand off full-resolution assets; developers upload them directly to the CMS or S3 bucket without an optimization pipeline. The site looks great in Figma and on a fast desktop connection, and the performance problem only surfaces on real mobile hardware.

**How to avoid:**
- Use a CDN with automatic image transformation (Cloudflare Images, Imgix, or Next.js Image component with a CDN provider). Never serve original uploaded files directly.
- Require WebP format with JPEG fallback. Target image file sizes under 200KB for catalog thumbnails, under 400KB for hero images.
- Lazy-load all below-the-fold images. Eagerly load the hero image only.
- Set Core Web Vitals targets before the design phase: LCP under 2.5s, INP under 200ms. Measure against them in staging.

**Warning signs:**
- No image optimization library or CDN in the stack
- Designers delivering assets at 4K resolution with no compression instructions
- Performance benchmarking is not on the launch checklist

**Phase to address:** Infrastructure and front-end foundation phase; image delivery strategy must be decided before catalog and portfolio pages are built.

---

### Pitfall 9: Availability Logic Does Not Account for Turnaround Buffer Time Between Bookings

**What goes wrong:**
A client books items for Saturday. Another client books the same items for Sunday. The admin team needs Saturday evening to inspect, clean, and repack the items before Sunday's event. The system shows Sunday as available because the Saturday booking ends Saturday night. The team is forced to cancel one booking or work through the night.

**Why it happens:**
Availability logic checks whether booking dates overlap with other bookings. It does not account for operational buffer time between events. This is obvious to the operations team but invisible to developers who are not domain experts.

**How to avoid:**
- Build a configurable "buffer/turnaround time" setting per item or globally (e.g., 24 hours). When computing availability for a requested date range, treat [booking end date + buffer] as the effective block end.
- Surface this setting in the admin panel so the team can adjust it without code changes.
- Make the buffer time explicit in the admin availability view so staff can see why a slot is blocked.

**Warning signs:**
- Availability check only queries for date-range overlaps with confirmed bookings, with no buffer concept
- No "turnaround time" or "prep time" field visible anywhere in the admin panel
- Operations staff have not been interviewed about their item-return-to-rebook workflow

**Phase to address:** Booking and inventory data model phase (design into the schema from the start; retrofitting is painful).

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Checking availability but not holding inventory during checkout | Simpler schema, faster to build | Double bookings in production; emergency manual intervention | Never -- hold logic must exist before launch |
| Fulfilling bookings from the redirect URL, not the webhook | Simpler to build, works in demo | Missed confirmations, orphaned payments, customer complaints | Never for paid bookings |
| Hardcoding refund policy logic | Faster to ship | Policy change requires code deployment | Only if policy is truly immutable |
| Using Calendly free tier for consultation booking | Zero backend work | No brand customization; looks out of place on a luxury site | Only as a temporary placeholder before brand is finalized |
| Uploading images directly without a CDN/optimizer | Simpler asset pipeline | Slow load times, poor Core Web Vitals, damaged conversions | Never for production launch |
| Building admin as raw CRUD table views | Framework generates it in minutes | Team abandons the tool; reverts to manual processes | Only in early internal testing -- refine before client handoff |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Stripe Webhooks | Not verifying the Stripe-Signature header | Always verify using stripe.webhooks.constructEvent() before processing |
| Stripe Webhooks | Processing the same event twice when Stripe retries | Store stripe_event_id and skip processing if already handled |
| Stripe Refunds | Manually refunding from Stripe dashboard instead of via API | Call stripe.refunds.create() from the admin panel; keep refund records linked to bookings |
| Stripe Checkout | Creating a new PaymentIntent on every page refresh | Create the PaymentIntent once per checkout session; reuse it across retries using idempotency keys |
| Calendly / Cal.com | Using the free embed without white-labeling | Use a paid tier or Cal.com self-hosted; apply brand colors and custom domain |
| Image delivery | Serving original uploaded images directly from storage | Serve all images through a CDN with width and format transformation parameters |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Querying all bookings to compute availability | Availability check slows as bookings accumulate | Index on item ID + date range; query only the relevant date window | ~500+ bookings in the database |
| Loading the full catalog with full-resolution images on the listing page | Catalog page LCP > 5 seconds on mobile | Paginate the catalog; serve thumbnails via CDN; full image only on detail page | At 20+ catalog items with unoptimized images |
| Synchronous webhook processing that exceeds 20 seconds | Webhook times out; Stripe retries; duplicate processing triggered | Return 200 immediately; push event to a queue; process asynchronously | Under any meaningful concurrent booking traffic |
| No database indexes on booking date range columns | Availability queries scan all rows | Add indexes on start_date, end_date, item_id, status at schema creation | ~1,000+ bookings |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Trusting client-supplied price in the checkout request | Client manipulates price to pay less than the actual rental cost | Compute price server-side from the item's database record; never accept price from the client payload |
| Admin panel routes without role-based auth | Any authenticated user can access booking data and payment records if auth middleware is misconfigured | Require authentication + admin role check on every admin route via middleware, not per-route checks |
| Storing Stripe webhook secret in client-side code or public env | Attackers send fake webhook events to confirm fake bookings | Webhook secret must only exist in server environment variables; never ship it to the browser |
| Not capturing policy acceptance at checkout | No evidence to fight chargebacks; client claims unawareness of no-refund window | Store a timestamped record of which policy version was accepted with each booking |
| Serving customer booking details without ownership check | Client A can view Client B's booking by guessing a booking ID | Always filter booking queries by the authenticated user's ID; never trust a URL parameter alone |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Date picker that allows selecting unavailable dates, only to error at checkout | Client invests time building a cart then discovers at payment that items are unavailable; high abandonment | Disable unavailable dates directly in the calendar UI; check availability in real time as dates are selected |
| No cart summary before payment | Client is unsure what they are paying for; checkout anxiety increases | Show a full itemized summary (items, dates, quantities, total) on the checkout page before the Stripe Payment Element |
| Consultation booking form with no confirmation or next-steps email | Client doubts whether the booking registered; may book again or call to verify | Send a branded confirmation email immediately with slot time, what to expect, and a contact address |
| Rental catalog with no availability indicator on listing cards | Client clicks into item detail, selects dates, and only then learns the item is unavailable | Show availability status on catalog cards once dates are selected |
| Admin panel with no booking status visual hierarchy | Admin sees a flat list of all bookings; cannot quickly identify what needs action today | Use status badges and filter defaults (Pending, Confirmed, Upcoming Today, Overdue Return) as the primary navigation model |

---

## "Looks Done But Isn't" Checklist

- [ ] **Inventory hold during checkout:** Soft-hold logic exists and expires on TTL -- verify by opening two browser sessions simultaneously attempting to book the same item for the same dates.
- [ ] **Webhook-driven confirmation:** Disable the success redirect temporarily and verify the booking is still confirmed via webhook alone.
- [ ] **Webhook idempotency:** Replay a Stripe event in the dashboard and verify the booking is not duplicated or double-confirmed.
- [ ] **Turnaround buffer time:** Book an item for Saturday and verify Sunday is blocked until the buffer clears.
- [ ] **Cancellation refund logic:** Process a test cancellation at each policy tier and verify the Stripe refund amount is correctly calculated.
- [ ] **Chargeback evidence trail:** For a test booking, verify that policy acceptance timestamp, item delivery status, and booking details are all accessible in the admin panel in the format needed for a Stripe dispute response.
- [ ] **Image performance:** Run a Lighthouse audit on the catalog page from a throttled mobile connection; LCP must be under 2.5 seconds.
- [ ] **Admin role guard:** Attempt to access an admin route while logged in as a regular client account -- must be denied.
- [ ] **Price integrity:** Attempt to submit a checkout with a manipulated price in the browser network tab -- server must reject and use its own price calculation.
- [ ] **Consultation confirmation email:** Complete a consultation booking and verify the branded confirmation email arrives with correct slot details.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Double booking discovered after payment | HIGH | Manual intervention: contact one client, offer reschedule or full refund, arrange substitute items; add inventory hold logic immediately |
| Missed booking confirmation (redirect-only logic, webhook not built) | HIGH | Audit Stripe dashboard against booking database to find gaps; manually confirm missed bookings; rebuild confirmation logic around webhooks |
| Refund processed incorrectly (wrong amount, no policy calculation) | MEDIUM | Issue correcting refund via Stripe dashboard; update admin panel with automated calculation logic before next cancellation |
| Chargeback lost due to no evidence | MEDIUM | Accept the loss; implement policy acceptance capture, delivery status tracking, and photo documentation before next booking cycle |
| Admin team not using the panel | MEDIUM | Run a structured observation session; identify the 3 most-needed daily tasks; rebuild those flows as priority; defer all others |
| Image performance failure post-launch | MEDIUM | Set up CDN with image transformation (Cloudflare or similar) and update all image src attributes; no data migration required |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Double booking via no inventory hold | Booking and inventory data model (foundation) | Two-session concurrent booking test |
| Webhook-not-redirect confirmation | Stripe payment integration phase | Disable redirect; verify webhook-only confirmation |
| No cancellation/refund logic | Admin panel phase + Checkout phase | Process test cancellations at each policy tier; verify Stripe refund amounts |
| Chargeback evidence gap | Admin panel phase + Checkout phase | Audit all evidence fields accessible per booking |
| Consultation/rental scheduling collision | Admin panel phase | Unified calendar view shows both commitment types |
| Consultation aesthetic mismatch | Visual design phase + Consultation booking phase | Brand consistency audit across all scheduler screens |
| Admin panel unusable by non-technical team | Admin panel phase | Observation session with actual operations staff |
| Image performance failure | Infrastructure and front-end foundation phase | Lighthouse audit before catalog page goes live |
| No turnaround buffer time | Booking and inventory data model (foundation) | Book back-to-back dates; verify buffer blocks the second booking |

---

## Sources

- [Stripe -- Idempotent Requests](https://docs.stripe.com/api/idempotent_requests)
- [Stripe -- Payment Intents API](https://docs.stripe.com/payments/payment-intents)
- [Stripe -- Refunds Documentation](https://docs.stripe.com/refunds)
- [Stripe -- Respond to Disputes](https://docs.stripe.com/disputes/responding)
- [Stripe -- Booking Systems with Payments](https://stripe.com/resources/more/booking-systems-with-payments-101-what-they-are-and-how-they-work)
- [Stripe -- Payment Element Best Practices](https://docs.stripe.com/payments/payment-element/best-practices)
- [Stripe Dispute Fees 2025 -- Chargeflow](https://www.chargeflow.io/blog/stripe-dispute-fees-2025)
- [Goodshuffle Pro -- Event Inventory Management 101](https://pro.goodshuffle.com/education/event-inventory-management/)
- [TapGoods -- Best Practices for Rental Inventory Management](https://www.tapgoods.com/pro/blog/event-rental-software/best-practices-for-rental-inventory-management-and-tracking/)
- [Stoa Logistics -- Inventory Reservation Patterns](https://stoalogistics.com/blog/inventory-reservation-patterns)
- [TwiceCommerce -- Real-Time Rental Availability and Double Bookings](https://www.twicecommerce.com/blog/real-time-rental-availability-avoid-double-bookings)
- [Tokeet -- Prevent Double Bookings: 3 Methods That Work](https://blog.tokeet.com/prevent-double-bookings/)
- [Stigg -- Best Practices for Stripe Webhooks](https://www.stigg.io/blog-posts/best-practices-i-wish-we-knew-when-integrating-stripe-webhooks)
- [Website Speed Statistics 2025 -- Marketing LTB](https://marketingltb.com/blog/statistics/website-speed-statistics/)
- [Triotech Labs -- How Website Speed Impacts Conversions 2025](https://www.triotechlabs.com/blogs/how-website-speed-impacts-your-conversions-in-2025/)
- [Hookdeck -- How to Implement Webhook Idempotency](https://hookdeck.com/webhooks/guides/implement-webhook-idempotency)
- [DEV Community -- Stop Doing Business Logic in Webhook Endpoints](https://dev.to/elvissautet/stop-doing-business-logic-in-webhook-endpoints-i-dont-care-what-your-lead-engineer-says-8o0)

---
*Pitfalls research for: event rental and design booking website (Midas Touch)*
*Researched: 2026-03-05*
