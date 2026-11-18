# AMKO Displays: vision demos

Three static visual concepts for the AMKO Displays Shopify redesign, built from the
SmartSites x Store Display kickoff call (13 Nov 2026) and the live amkodisplays.com.
They exist so the client can react to a design direction before their Shopify store exists.

| Concept | Feel |
|---|---|
| `concept/` | Bold and modern. Closest to the Displayarama look the client asked for. |
| `release/` | Content-rich and sectional. Featured, Specials and New Arrivals blocks, like Palay Display, plus Displayarama-style industry tiles. |
| `prestige/` | Premium and showcase-led. Calmer, serif, more upscale. |

Open `index.html` for the overview and a comparison table.

## What this is not

- **Not the real Shopify themes.** Concept, Release and Prestige are paid themes whose code is not available
  without purchase. These are HTML/CSS mockups styled after each theme's layout feel.
- **Not a build.** Prices, photos, stats, reviews, blog posts, FAQ answers and the industry list are SAMPLE or
  CONCEPT. Nothing here is client-approved copy.
- **Not a configurator.** The gondola builder is a step-by-step mock with sample pricing. A real one needs an
  app or custom code.

## Pages (same in each concept)

`index.html` home, `gondola.html` gondola landing page with the builder, `collection.html` filters, sort and
product grid, `product.html` product page, `industries.html` Shop by Industry plus anchors for Free Store
Layouts, Custom Manufacturing, About and Contact.

In the real build these anchored sections would be separate pages. The scope allows up to five
non-ecommerce pages, to be confirmed against the workbook.

## Real facts used from the live site

Navigation labels, the category names, the Museum Case specs and SKU (JECAG48), the showroom address and the
two phone numbers. Everything else is sample.

## Sources

- Fireflies kickoff: SmartSites x Store Display Project Kickoff
- Live site: https://amkodisplays.com
- Reference sites: Displayarama (https://displayarama.com), named "Displayorama" in the transcript, and Palay Display
  (https://www.palaydisplay.com), named "Pali Displays" in the transcript

## Run locally

No build step. Serve the folder, for example:

```
python -m http.server 8765 --directory demo
```

then open http://localhost:8765/.

## Regenerate

`demo/tools/build_demo.py` generates every file except this README and the tools folder:

```
python demo/tools/build_demo.py demo
```

## Open items before the real build

- Confirm the non-ecommerce pages and industry list from the workbook website plan.
- Client's new logo and colors (this demo uses a text wordmark and a neutral palette).
- Gondola configurator: app or custom code.
- Quantity pricing is marked "Plus" on the theme pages. Check whether it needs Shopify Plus.
- Shipping zones (East / West / Central) and the shipping app.
- Appointment booking, if wanted. It was mentioned on the call but not on the reference site.
- Compare against the real themes once the Shopify dev store exists.
