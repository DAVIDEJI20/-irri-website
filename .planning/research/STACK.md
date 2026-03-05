# Stack Research

**Domain:** Event rental and design booking website
**Researched:** 2026-03-05
**Confidence:** HIGH

## Recommended Stack

### Frontend Framework

**Next.js 14+ (App Router)** — HIGH confidence
- Server-side rendering for catalog and portfolio pages (SEO-critical)
- Server Actions for form submissions (rental booking, consultation scheduling)
- Image optimization built-in (`next/image`) — essential for a luxury image-heavy brand
- Do NOT use: Create React App (no SSR), Vite-only SPA (poor SEO for catalog pages)

### Styling

**Tailwind CSS 3.x + shadcn/ui** — HIGH confidence
- Tailwind for rapid utility-first styling; required for a custom luxury aesthetic
- shadcn/ui for accessible component primitives (forms, dialogs, date pickers) that can be fully re-styled
- Do NOT use: Bootstrap/MUI — opinionated defaults fight a custom brand aesthetic

### Database

**PostgreSQL (via Supabase or Railway)** — HIGH confidence
- Relational model is required for: inventory items ↔ bookings ↔ availability holds
- Date-range queries and inventory hold TTLs are well-supported
- Supabase adds auth and row-level security (useful for admin access control) at no extra complexity
- Do NOT use: MongoDB — document model makes date-range availability queries awkward

### ORM

**Prisma 5.x** — HIGH confidence
- Type-safe schema-driven ORM; works natively with Next.js
- Migrations are straightforward for evolving the booking data model
- Do NOT use: raw SQL for a project with complex relational schemas

### Authentication

**NextAuth.js v5 (Auth.js)** — HIGH confidence
- Admin-only authentication (clients do not log in at v1)
- Supports credential provider (email/password) for the admin team
- Do NOT use: Clerk/Auth0 — overkill for admin-only auth; adds external dependency and cost

### Payments

**Stripe** — HIGH confidence (pre-decided by user)
- Use `stripe` Node SDK + `@stripe/stripe-js` for client
- Payment Intents API for full-amount rental payments
- Webhooks (`payment_intent.succeeded`) to confirm bookings server-side — critical
- Do NOT use: browser redirect confirmation — race condition that causes missed bookings

### Email

**Resend + React Email** — HIGH confidence
- Transactional emails: booking confirmation, consultation confirmation, reminders
- React Email for templating (render to HTML with luxury brand styling)
- Resend: generous free tier, excellent deliverability, simple API
- Do NOT use: Nodemailer with SMTP directly — deliverability issues in production

### Scheduling (Consultation Booking)

**Custom slot-picker UI** over Calendly — MEDIUM confidence
- Calendly's iframe/embed doesn't match a luxury brand aesthetic
- Cal.com (open source, self-hosted) is an alternative if full brand control is needed
- Simplest v1: Admin sets available slots in DB; client picks from them; no external tool dependency
- Do NOT use: Calendly embedded — cannot be styled to match Midas Touch brand

### File/Image Storage

**Cloudinary or Supabase Storage** — HIGH confidence
- Catalog item images + portfolio gallery images
- Cloudinary: automatic image transformation, CDN delivery, crucial for performance
- Supabase Storage: simpler if already using Supabase; add Cloudflare CDN for transformation
- Do NOT use: S3 directly without CDN — performance penalty on image-heavy pages

### Hosting

**Vercel** — HIGH confidence
- Native Next.js deployment; zero config
- Edge network handles CDN for static assets
- Do NOT use: shared hosting — no support for Next.js server features

## Version Summary

| Package | Version | Role |
|---------|---------|------|
| next | 14.x | Framework |
| react | 18.x | UI library |
| tailwindcss | 3.x | Styling |
| @prisma/client | 5.x | ORM |
| next-auth | 5.x (beta) | Admin auth |
| stripe | 14.x | Payments |
| @stripe/stripe-js | 2.x | Client SDK |
| resend | 3.x | Email |
| react-email | 2.x | Email templates |
| zod | 3.x | Schema validation |

## What NOT to Use

| Tool | Reason |
|------|--------|
| WordPress + WooCommerce | Too rigid for custom rental booking logic; date-based availability is a plugin nightmare |
| Shopify | Not designed for rental/date-based inventory; workarounds are fragile |
| Webflow | No server-side logic for real inventory management |
| Firebase/Firestore | Document DB makes relational rental queries difficult |
| jQuery | Not appropriate for a modern React-based stack |
