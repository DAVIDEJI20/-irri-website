# Feature Research

**Domain:** Event rental catalog + consultation booking website (luxury decor, furniture, tableware)
**Researched:** 2026-03-05
**Confidence:** HIGH (rental catalog patterns), MEDIUM (consultation scheduling patterns)

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete or unprofessional.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Browsable rental catalog with categories | Users expect to see what is available before committing; no catalog = no business | LOW | Categories: furniture, decor and props, tableware. Each item needs photos, description, dimensions/quantity, price per event |
| Per-item availability by date | Rental sites that do not show availability waste time; users have learned to expect date-gating | MEDIUM | Must block out already-booked dates per item; date picker on item or cart level |
| Date-based cart (single event date or range) | Renting is fundamentally date-scoped; a cart without date context is meaningless for rentals | MEDIUM | Cart tied to event date; availability validation runs at add-to-cart or at checkout |
| Online checkout with full payment | Business goal: replace phone/in-person; users expect to complete the transaction end-to-end | MEDIUM | Stripe or equivalent; order confirmation email required |
| Consultation scheduling (slot selection) | Calendly-style slot picking is the standard UX for service scheduling; phone tag is unacceptable | MEDIUM | Show available slots, capture client info and event brief, send confirmation |
| High-quality item photography | This is a visual product -- photos ARE the product; low quality = no sale | LOW (design) / MEDIUM (infra) | Multiple angles, in-context shots (styled event settings), not white-background only |
| Portfolio / gallery section | Event design is trust-driven; without portfolio evidence, consultation bookings will not happen | LOW | Categorized by event type; before/after or styled event shots |
| Mobile-responsive design | 60-70% of browsing happens on mobile; broken mobile = lost leads | LOW (with modern framework) | Catalog grid, cart, checkout, and booking flow must all work on small screens |
| Contact information and service area | Users need to verify the business serves their location before investing time | LOW | Physical address or service region, phone, email, social links |
| Order confirmation emails | Users expect immediate email confirmation for any transaction or booking | LOW | Rental order confirmation + consultation booking confirmation; include order summary and next steps |
| Admin: catalog management | Small team must be able to add/edit/remove items without developer help | MEDIUM | CRUD for catalog items including photos, pricing, availability overrides |
| Admin: booking and order view | Team needs to see all rentals and consultations in one place | MEDIUM | List view with filters (date, status); ability to mark as confirmed/completed/cancelled |
| Trust signals (testimonials) | Event services are high-stakes purchases; social proof is a prerequisite for conversions | LOW | Testimonials with client name, event type, possibly photo |
| Privacy policy and rental terms | Legal requirement; also a credibility signal -- missing it reads as amateur | LOW | Cookie/data policy, rental terms, cancellation policy |

---

### Differentiators (Competitive Advantage)

Features that set Midas Touch apart. Not universally expected, but highly valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Damage waiver option at checkout | Industry standard for professional rentals; clients feel protected; reduces post-event disputes | LOW | Non-refundable fee (3-10% of order total) covering accidental damage; displayed and accepted at checkout |
| Pre-consultation intake questionnaire | Captures event date, type, headcount, budget range, and style brief before the consultation; saves both parties time | LOW | Embedded in the consultation booking flow as step 2 after slot selection |
| Package / bundle display | Pre-curated packages help clients who do not know where to start; increases average order value | MEDIUM | Not full e-commerce bundles -- show curated groupings with 1-click add-all to cart |
| Style-based catalog filtering | Clients often shop by aesthetic (boho, modern glam) rather than product category; filtering by style reduces decision fatigue | MEDIUM | Tag items with style keywords; filter panel alongside category filter |
| Portfolio organized by event type | Clients planning a wedding look for wedding portfolio, not a generic gallery | LOW | Filter or tab by: Wedding, Corporate, Birthday, Styled Shoot, etc. |
| Automatic reminder emails for consultations | Reduces no-shows significantly (reported 40-80% reduction industry-wide); makes the business feel organized | LOW | 24-hour and 1-hour reminder; include rescheduling link |
| Self-service rescheduling / cancellation | Clients expect autonomy; removing friction on rescheduling increases satisfaction even when plans change | MEDIUM | Token-based link in confirmation email; re-opens slot in availability calendar |
| Wishlist / save for later | Clients often browse well before they are ready to book; saving items for a return visit keeps them engaged | LOW | Session or account-based; shareable link is a bonus |
| Visual brand identity (luxury/gold) | The site itself is a portfolio statement -- a generic-looking site undercuts the luxury positioning | LOW (design) | Gold accent palette, editorial typography, generous whitespace |
| Item cross-sell / pairs well with | Helps clients discover complementary items; increases cart size organically | MEDIUM | Manually curated relationships between items (e.g., charger plates pairs with napkin rings) |

---

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem appealing but create real problems for this business context.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Quote-request-only flow (no online payment) | Some rental businesses use add-to-cart then request-quote then we-call-you to retain sales control | Kills the core value proposition of Midas Touch (eliminating the need to call); drops conversion rates; creates manual follow-up workload | Full online checkout with Stripe -- commit to the self-service model |
| Deposit-based payment (partial upfront) | Feels lower commitment for clients; common in event industry | Already explicitly out of scope per PROJECT.md; adds collection complexity and partial-payment tracking | Full payment upfront -- simpler, committed bookings only |
| Real-time multi-location inventory sync | Useful if inventory lives in multiple warehouses | Out of scope per PROJECT.md; adds significant backend complexity for no current benefit | Single inventory source; manual availability overrides in admin when needed |
| Client accounts / login portal | Users like having an account to track orders | Adds auth complexity, password reset flows, account management surface area; most clients book infrequently so login friction outweighs benefit at v1 | Guest checkout with order lookup by email/order number; reconsider at v2 |
| Live chat / chatbot | Seems like a good conversion tool | Requires monitoring or a trained bot; creates expectation of instant response the small team may not meet; can undermine luxury brand positioning | Clear contact form and phone number; consultation booking as the structured inquiry path |
| Dynamic demand-based pricing | Pricing adjusts by season or demand | Adds pricing engine complexity; confuses clients who expect stable prices; luxury brands do not compete on price signals | Fixed pricing per item; seasonal packages curated manually |
| Social media feed embed (live Instagram) | Shows off portfolio dynamically | API access is unreliable (Instagram has repeatedly broken third-party embeds); loads slowly; pulls design quality down when post types vary | Manually curated portfolio gallery with editorial control; link to Instagram in footer |

---

## Feature Dependencies

```
[Online Checkout]
    requires [Date-Based Cart]
        requires [Per-Item Availability by Date]
            requires [Catalog with Items]

[Consultation Booking]
    requires [Availability Calendar / Slot System]
    enhances [Pre-Consultation Intake Form]
        enhances [Admin: Booking View]

[Damage Waiver at Checkout]
    requires [Online Checkout]

[Order Confirmation Emails]
    requires [Online Checkout] (rental orders)
    requires [Consultation Booking] (consultation confirmations)

[Automatic Reminder Emails]
    requires [Consultation Booking]
    requires [Order Confirmation Emails] (email infrastructure shared)

[Self-Service Rescheduling]
    requires [Consultation Booking]
    requires [Automatic Reminder Emails] (link delivered via email)

[Style-Based Catalog Filtering]
    requires [Catalog with Items] (items must be tagged)

[Item Cross-Sell]
    requires [Catalog with Items] (relationships must be defined)

[Portfolio Organized by Event Type]
    requires [Portfolio / Gallery Section]

[Package / Bundle Display]
    requires [Catalog with Items]
    enhances [Date-Based Cart] (add-all-to-cart)

[Admin: Booking and Order View]
    requires [Online Checkout] (rental orders)
    requires [Consultation Booking] (consultation records)

[Admin: Catalog Management]
    requires [Catalog with Items] (CRUD surface)
```

### Dependency Notes

- **Checkout requires the full availability chain:** Before checkout can exist, the catalog, per-item availability, and date-scoped cart must all work. These form the critical path for the rental flow.
- **Consultation booking is an independent flow:** It does not depend on the rental catalog at all. It can be built in parallel with the rental checkout flow.
- **Email infrastructure is shared:** Rental order confirmations and consultation confirmations both need a transactional email system (e.g., Resend, SendGrid, Postmark). Build once, use for both.
- **Admin view requires both flows to exist:** The admin panel is a read/write surface over data produced by both flows; build it after both flows produce data.
- **Damage waiver is a checkout enhancement:** Low complexity, high business value -- add it in the same phase as checkout, not after.

---

## MVP Definition

### Launch With (v1)

Minimum viable product to replace the current phone/in-person booking entirely.

- [ ] Rental catalog with categories, photos, descriptions, and pricing -- without this, there is no product
- [ ] Per-item availability by event date -- prevents overbooking and wasted inquiries
- [ ] Date-based cart + full payment checkout (Stripe) -- core value proposition; must work completely
- [ ] Damage waiver acceptance at checkout -- protects business; low complexity
- [ ] Order confirmation email -- clients need proof of purchase
- [ ] Consultation slot booking with intake form -- second core service; must be live at launch
- [ ] Consultation confirmation and reminder emails -- reduces no-shows; uses shared email infra
- [ ] Portfolio / gallery section -- required for consultation conversion; trust signal
- [ ] Testimonials -- required for trust; consultation bookings will not happen without them
- [ ] Admin: catalog management (add/edit/archive items) -- team cannot operate without this
- [ ] Admin: rental orders and consultation bookings view -- team must see what is booked
- [ ] Mobile-responsive design throughout -- non-negotiable given mobile traffic volume

### Add After Validation (v1.x)

Features to add once the core flows are proven and client patterns are understood.

- [ ] Style-based catalog filtering -- add when catalog grows large enough that style filtering becomes navigationally useful (threshold: roughly 30 or more items)
- [ ] Self-service rescheduling for consultations -- add when no-show or reschedule rates create admin burden
- [ ] Item cross-sell / pairs well with -- add when average order size data suggests upsell opportunity
- [ ] Wishlist / save for later -- add if analytics show high browse-to-book gap (users leaving without converting)
- [ ] Package / bundle display -- add when catalog is stable enough to create meaningful curated groupings

### Future Consideration (v2+)

Defer until product-market fit is clear and repeat client patterns are established.

- [ ] Client accounts / login portal -- defer until repeat booking frequency justifies the auth investment
- [ ] Coupon / promo code system -- defer until marketing strategy requires it; adds checkout complexity
- [ ] Multiple consultation types (e.g., 30-min intro call vs 2-hour full design session) -- defer until consultation volume creates a need to segment
- [ ] Automated post-event review requests -- defer; good to have but not launch-critical

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Rental catalog (browse + filter) | HIGH | LOW | P1 |
| Per-item availability by date | HIGH | MEDIUM | P1 |
| Date-based cart | HIGH | MEDIUM | P1 |
| Online checkout (Stripe) | HIGH | MEDIUM | P1 |
| Consultation slot booking | HIGH | MEDIUM | P1 |
| Intake form (pre-consultation) | HIGH | LOW | P1 |
| Order and booking confirmation emails | HIGH | LOW | P1 |
| Portfolio / gallery | HIGH | LOW | P1 |
| Admin: catalog management | HIGH | MEDIUM | P1 |
| Admin: bookings and orders view | HIGH | MEDIUM | P1 |
| Mobile-responsive design | HIGH | LOW | P1 |
| Testimonials | HIGH | LOW | P1 |
| Damage waiver at checkout | MEDIUM | LOW | P1 |
| Consultation reminder emails | MEDIUM | LOW | P1 |
| Style-based filtering | MEDIUM | MEDIUM | P2 |
| Package / bundle display | MEDIUM | MEDIUM | P2 |
| Item cross-sell | MEDIUM | MEDIUM | P2 |
| Self-service rescheduling | MEDIUM | MEDIUM | P2 |
| Wishlist / save for later | LOW | LOW | P2 |
| Client accounts / login | MEDIUM | HIGH | P3 |
| Promo codes / coupons | LOW | MEDIUM | P3 |
| Multiple consultation types | LOW | MEDIUM | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

| Feature | Booqable / Goodshuffle (SaaS tools) | Generic Event Planner Sites | Our Approach |
|---------|-------------------------------|------------------------------|--------------|
| Rental catalog | Full-featured but generic-looking | Photo gallery only, no booking | Custom branded catalog with date-availability and direct checkout |
| Availability management | Real-time, admin-controlled | None | Per-item, date-blocked; admin can override manually |
| Checkout | Full e-commerce checkout | Inquiry form only | Stripe checkout with damage waiver; no quote loop |
| Consultation booking | Not typically included | Contact form then email tag | Calendly-style slot picker with intake form; confirmations automated |
| Portfolio | Not a feature | Primary feature | Both: catalog as portfolio plus dedicated gallery section |
| Brand and design | Generic SaaS UI | Often custom but varies | Luxury editorial identity (Midas Touch gold palette) -- site is itself a portfolio statement |
| Admin panel | Comprehensive but complex | None | Focused admin: catalog CRUD plus orders plus consultation bookings |

---

## Sources

- [2025 Website Checklist for Party Rental Companies -- Path and Compass](https://www.pathandcompass.com/the-website-checklist-for-rental-companies/)
- [What's Changing in Event Rentals in 2026 -- Goodshuffle Pro](https://pro.goodshuffle.com/blog/event-rental-software-trends-2026-roadmap)
- [Five Mistakes Event Rental Pros Make -- RW Elephant](https://rwelephant.com/blog/five-mistakes-event-rental-pros-make-how-to-avoid-them/)
- [How Rental Businesses Can Prevent Overbooking -- Booqable](https://booqable.com/blog/preventing-overboooking-double-bookings/)
- [Booqable vs. Goodshuffle Pro Comparison -- Goodshuffle Pro](https://pro.goodshuffle.com/booqable-vs-goodshuffle-pro-which-is-best-for-event-rental-businesses/)
- [8 Best Scheduling Apps for Small Businesses -- Calendly](https://calendly.com/blog/appointment-scheduling-software)
- [Top 5 Party Rental Website Builders -- RentalSetup](https://rentalsetup.com/articles/top-five-party-rental-website-builder-in-2025)
- [18 Best Event Planner Website Design Examples -- Colorlib](https://colorlib.com/wp/event-planner-websites/)
- [How to Start a Party and Event Rental Business in 2026 -- Rentrax](https://rentrax.com/blog/how-to-start-a-party-event-rental-business-in-2026/)
- [Avoid Overbooking Your Event Rental Inventory -- Rentopian](https://rentopian.com/avoid-overbooking-your-event-rental-inventory/)
- [10 Calendly Alternatives for Smarter Scheduling -- Acuity Scheduling](https://acuityscheduling.com/learn/calendly-alternatives)

---

*Feature research for: event rental catalog + consultation booking website (Midas Touch)*
*Researched: 2026-03-05*
