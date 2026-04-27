# MiniPay Submission Requirements

> Source: Opera MiniPay "Build for MiniPay: Developer Requirements" (official PDF, referenced by the MiniPay submission form `https://forms.gle/3MNtw2GNRHp29j51A`).
> Last updated: 2026-04-21.

This file is the **checklist** for getting a Mini App listed in MiniPay. For how to build each piece, see `minipay-guide.md`, `minipay-templates.md`, and `minipay-scaffold-from-scratch.md`.

---

## 1. Seamless User Experience

- **Zero-Click Connect** — do **not** show a "Connect Wallet" button inside MiniPay. Auto-retrieve the wallet address from `window.ethereum`. Pattern: `minipay-templates.md` §1; detection: `minipay-guide.md` → MiniPay Detection.
- **No Message Signing** — do **not** prompt users to `personal_sign` or `eth_signTypedData` to access or authenticate. MiniPay does not support these methods. See `minipay-guide.md` → Important Constraints #4.
- **Phone-First Identity** — **never display raw `0x…` addresses** as the primary identifier. Show the phone number (resolved via ODIS → FederatedAttestations), an app-specific alias, or a truncated form only as a secondary hint. Lookup flow: `odis-socialconnect.md` and `minipay-guide.md` → Phone Number → Address Resolution.

---

## 2. Currency & Stablecoin Logic

- **Token Support** — supported tokens are **USDT, USDC, and USDm only**. **Never display or require the CELO token**; MiniPay handles fees automatically via CIP-64 fee abstraction.
- **Dynamic Adaptation** — adapt to the user's **preferred stablecoin** (the one they hold the most of). Working helper: `minipay-templates.md` §6 — Preferred Stablecoin Selection.
- **Graceful Degradation** — if your app only supports one stablecoin, show a clear explainer ("This app accepts USDC only. Swap in MiniPay first.") instead of a broken interface.

---

## 3. User-Facing Copy (strict)

Replace crypto-jargon with user-friendly terms everywhere a real user sees them (buttons, tooltips, error messages, copy):

| ❌ Don't say | ✅ Say |
|------|------|
| Gas / Gas fee | **Network fee** |
| Onramp / Buy (crypto) | **Deposit** |
| Offramp / Sell (crypto) | **Withdraw** |
| Crypto / Crypto token | **Stablecoin** or **Digital dollar** |
| Wallet address (as primary identifier) | Phone number |

**Scope:** all UI strings, button labels, tooltips, error messages. Code identifiers and RPC method names (`gasEstimate`, `eth_gasPrice`, `feeCurrency`) are technical — keep those as-is.

---

## 4. Technical Performance & Optimization

- **Mobile-First Resolution** — the UI must be responsive and fully functional at **360w × 640h**. Use Chrome DevTools device mode to validate before submission.
- **Asset Optimization** — use **SVG or WebP** for images. Avoid PNG/JPG for anything larger than a few KB.
- **Performance Benchmarking** — submit a **PageSpeed Insights** score (`https://pagespeed.web.dev`) for your production URL with the form. Aim for 90+ on mobile. Low scores block listing.
- **Network Transparency** — provide a full manifest of every **URL, subdomain, and origin** your app calls (JS, CSS, fonts, RPCs, APIs). MiniPay reviews this for supply-chain risk.

---

## 5. Smart Contract Standards

- **Public Verification** — all your contract source code must be **verified on Celoscan** (`https://celoscan.io`) so users can inspect it. How-to: `builder-guide.md` → Verification.
- **Transaction Samples** — for every user-facing method your app uses, provide a **sample transaction link on Celoscan** with the submission.

---

## 6. Integration & Support

- **Code Guidelines** — use the patterns in this skill (`minipay-guide.md`, `minipay-templates.md`). They mirror the canonical MiniPay Developer Documentation.
- **Low-Balance Handling** — when a user cannot complete an action because their balance is too low, **redirect to the MiniPay Deposit deeplink** rather than showing an error. Deeplink: `https://minipay.opera.com/add_cash`. Canonical deeplink list: `https://docs.minipay.xyz/technical-references/deeplinks.html#available-deeplinks` — fetch before shipping; new deeplinks are added periodically.
- **Dedicated Support** — provide an **in-app support link** reachable from inside the Mini App (header icon, footer, or settings). Accepted channels: Telegram, WhatsApp, email, or web support portal.
- **SLA** — you must fix reported **critical issues within 24 hours**, or MiniPay will temporarily disable your listing.

---

## 7. Branding & Legal

- **Clear Ownership** — display your app's **name and logo** prominently. It must be obvious to the user that the service is operated by your entity, not by MiniPay.
- **Legal Links** — provide accessible links to your **Terms of Service** and **Privacy Policy** from inside the app (footer or settings screen). Required for listing.

---

## Deeplinks (MiniPay)

| Deeplink | URL | When to use |
|----------|-----|-------------|
| Deposit (Add Cash) | `https://minipay.opera.com/add_cash` | Low balance; user needs to top up |

> Canonical list: `https://docs.minipay.xyz/technical-references/deeplinks.html#available-deeplinks` — fetch this before shipping; MiniPay publishes new deeplinks periodically.

---

## Pre-submission checklist

Copy this block into your submission PR or internal review doc:

- [ ] Zero-click connect (no Connect Wallet button when `window.ethereum.isMiniPay === true`)
- [ ] No `personal_sign` / `eth_signTypedData` anywhere in the app
- [ ] No raw `0x…` addresses shown as primary user identifier
- [ ] Only USDT / USDC / USDm — no CELO in balances, selectors, or copy
- [ ] Picks the user's highest-balance stablecoin, or explains single-token UX clearly
- [ ] UI copy uses: **Network fee**, **Deposit**, **Withdraw**, **Stablecoin** (not gas / onramp / offramp / crypto)
- [ ] Tested at **360 × 640** mobile resolution
- [ ] Images are SVG or WebP
- [ ] PageSpeed Insights score captured for production URL
- [ ] URL / subdomain / origin manifest prepared
- [ ] All contracts verified on Celoscan
- [ ] Sample transaction hashes collected for every method
- [ ] Redirects to Deposit deeplink on insufficient balance
- [ ] In-app support link (Telegram / WhatsApp / email / web portal)
- [ ] Committed to 24h SLA for critical fixes
- [ ] App name + logo visible and clearly distinct from MiniPay's branding
- [ ] Terms of Service + Privacy Policy links accessible in-app
