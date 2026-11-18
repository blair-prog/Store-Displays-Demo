# Store Displays: vision demos

Three static visual concepts for the Store Displays® Shopify redesign, built from the
SmartSites x Store Display kickoff call (13 Nov 2026) and the live https://storedisplays.com.
They exist so the client can react to a design direction before their Shopify store exists.

| Concept | Feel |
|---|---|
| `concept/` | Light, airy and rounded: Inter type, pill buttons, a rounded photo slideshow. Modeled on the Concept demo store. |
| `release/` | Editorial: a transparent header over a full-bleed hero, light Poppins headlines, banner-led sections. Modeled on the Release demo store. |
| `prestige/` | Quiet and architectural: spaced uppercase headings, square buttons, a light grey page. Modeled on the Prestige demo store. |

Open `index.html` for the overview and a comparison table.

## What this is not

- **Not the real Shopify themes.** Concept, Release and Prestige are paid themes whose code is not available
  without purchase. These are HTML/CSS mockups modeled on each theme's public demo store (typography, colours,
  header, hero and section order). They use none of the theme code or the demo photography, so they approximate
  the look and are not a substitute for the real themes.
- **Not a build.** Reviews, most copy, the industry pages and the gondola builder are SAMPLE or CONCEPT.
- **Not a configurator.** The gondola builder is a step-by-step mock with sample pricing. A real one needs an
  app or custom code.

## What comes from the live site

Content is taken from storedisplays.com so the concepts look like this client's store:

- **Links:** the main menu labels, the mega menu (the live site's categories), policies, blog, FAQs, volume
  discount pricing, Industries We Serve, Custom Millwork & Showcases. Deeper links open the live site in a new tab.
- **Products:** 16 products with real names, SKUs and listing prices (gondola units other than "from $107" are sample).
- **Images:** downloaded from storedisplays.com at the highest resolution the site serves and saved in `assets/img/` (44 files, about 13 MB): the logo, the home hero banner (2560 px wide), eight industry photos (about 2360 px square), product photos (900 px) and the gondola photos. They are the client's own photography; confirm usage rights before publishing anywhere public. A few category images on the live site are only 430 px wide, so the demos do not use them at large sizes.
- **Gondola options:** unit types, lengths, heights, colors and shelf capacity follow the live Gondola Shelving page.
- **Product page:** the 4′ Black Standard Extra Vision Display Case (ESC4/B) page uses its real features,
  specifications and variation options. Option prices are partly sample.
- **Contact:** the address, phone (201) 935-2929 and info@storedisplays.com.

Product, category, policy and blog links still open the live storedisplays.com in a new tab.

## Features requested on the kickoff call

These are the features the client asked for or liked on competitor sites (Displayarama, Palay Display). All of
them are concepts with sample data unless noted:

- **Shop by Industry:** a hub plus 8 industry pages, each with recommended products, a checklist and FAQ.
- **Free store layouts:** a dedicated page with a request form.
- **Appointment scheduling:** a booking widget (layout call or showroom visit) with sample availability.
- **Gondola configurator:** a step-by-step builder using the live site's real unit options, sample pricing.
- **Direct pricing:** prices on every card and product page, replacing request-for-quote.
- **Calculate shipping:** a ZIP-based East / Central / West estimate with sample rates (the regional matrix
  discussed on the call). It refuses Alaska and Hawaii.
- **Bulk and volume pricing:** a request form, plus a link to the live Volume Discount Pricing page.
- **New and trending products**, **color and size as variants**, and a **10% newsletter capture** (popup and band).
- **Concept-only interactions** (modeled on the Concept demo): a rotating hero slideshow, pill-style nav with card mega menus for products and industries, industry photo cards whose plus button opens a description on hover, quick add on product cards, and pill buttons that invert on hover.

The real build needs apps or custom code for the configurator, booking, shipping zones and bulk pricing.

## SEO layer

Draft strategy built into every page, with an **SEO view** button (bottom left) that opens a panel for the current page and outlines its headings:

- Unique title tag and meta description per page, kept within the usual length guidance, plus a primary keyword and secondary keywords.
- JSON-LD schema: Organization and WebSite on the home page, Product on the product page, BreadcrumbList, FAQPage and ItemList where they apply.
- Product-matched H1s, an intro above each product grid and buying-guide content below it, as agreed on the kickoff call.
- Eight industry landing pages with their own copy, FAQ and internal links, a crawlable block of popular searches taken from the live home page, and related live blog posts.
- Descriptive alt text on every image.

All SEO copy is draft wording for review. It has not been through keyword research.

## Pages (same in each concept)

`index.html` home, `gondola.html` gondola landing page with the builder, `collection.html` filters, sort and
product grid, `product.html` product page, `industries.html` Shop by Industry hub, `layouts.html` free store
layouts and booking, and `industry-<name>.html` for each of the 8 industries.

The scope allows up to five non-ecommerce pages, to be confirmed against the workbook. These demos show more,
so the page list in the real build needs agreeing.

## Run locally

No build step. Serve the folder, for example from the repo root:

```
python -m http.server 8765 --directory demo
```

then open http://localhost:8765/. The page needs internet access only for the web fonts; images are local.

## Regenerate

`demo/tools/build_demo.py` generates every file except this README and the tools folder:

```
python demo/tools/build_demo.py demo
```

## Open items before the real build

- Confirm the non-ecommerce pages and industry list from the workbook website plan.
- Client's new logo and colors (these demos use the current logo).
- Gondola configurator: app or custom code. The live gondola page is a quote form today.
- Quantity pricing is marked "Plus" on the theme pages. Check whether it needs Shopify Plus.
- Shipping zones (East / West / Central) and the shipping app.
- Appointment booking tool: it was mentioned on the call but is on neither reference site, so it is the least proven idea.
- Compare against the real themes once the Shopify dev store exists.
