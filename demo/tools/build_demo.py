#!/usr/bin/env python3
"""Generate three static Store Displays&reg; "vision" demos (Concept, Release, Prestige).

Static HTML/CSS/JS mockups styled after the layout feel of three Shopify themes.
They are NOT the real themes. All prices, photos and stats are SAMPLE content.

Usage: build_demo.py [OUTPUT_DIR]   (default: ./demo)
"""
import argparse
import html
import json
import re
import os
import shutil

# ----------------------------------------------------------------------------
# Shared content (from the kickoff call, the live storedisplays.com, workbook TBD)
# ----------------------------------------------------------------------------
PHONE1 = "(201) 935-2929"
PHONE_TEL = "2019352929"
EMAIL = "info@storedisplays.com"
ADDRESS = "7 Purcell Ct., Moonachie, NJ 07074"
U = "https://storedisplays.com"
UP = "/wp-content/uploads/"
LOCAL = set()  # filenames found in <out>/assets/img, filled in by main()

# Internal mock pages stand in for these real storedisplays.com paths. Everything else links to the live site.
MOCK = {
    "/gondola-shelving/": "gondola.html", "/shop/": "collection.html", "/product-category/counters-showcases/": "collection.html",
    "/industries-we-serve/": "industries.html", "/contact/": "industries.html#contact", "/about/": "industries.html#about",
}


# Category data scraped from the live category pages (names, SKUs, prices, image paths, sub-categories)
CATS = {}
_cats_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "categories.json")
if os.path.isfile(_cats_file):
    with open(_cats_file, encoding="utf-8") as _f:
        CATS = json.load(_f)
for _slug in CATS:
    MOCK["/product-category/%s/" % _slug] = "cat-%s.html" % _slug


def local_name(path):
    base = os.path.basename(path)
    orig = re.sub(r"-\d+x\d+(?=\.\w+$)", "", base)
    for cand in (orig, base):
        if cand in LOCAL:
            return cand
    return None


def img_src(path):
    ln = local_name(path)
    if ln:
        return "../assets/img/" + ln
    if path.startswith("http"):
        return path
    return U + (path if path.startswith("/") else UP + path)


def href(path):
    return MOCK.get(path, U + path)


def a_attrs(h):
    return ' target="_blank" rel="noopener"' if h.startswith("http") else ""


# Header navigation. The third value says which mega menu the item opens (None for a plain link).
NAV = [
    ("Display Cases", "cat-counters-showcases.html", None),
    ("Gondola Shelving", "gondola.html", None),
    ("Store Fixtures &amp; Displays", "collection.html", "products"),
    ("Custom Millwork &amp; Showcases", U + "/custom-millwork-showcases/", None),
    ("Shop by Industry", "industries.html", "industry"),
    ("Free Store Layouts", "layouts.html", None),
    ("Blog", U + "/blog/", None),
    ("About Us", "industries.html#about", None),
    ("Contact Us", "industries.html#contact", None),
]

# The live site's 20 product categories, grouped into list-style mega-menu columns
MEGA = [
    ("Shelving &amp; Systems", [("Shelving", "/product-category/shelving/"), ("Wall Standards", "/product-category/wall-standards/"),
                               ("Retail Systems", "/product-category/retail-systems/")]),
    ("Counters &amp; Cubbies", [("Countertop Displays", "/product-category/countertop-displays/"),
                               ("Glass &amp; Wooden Cubby Displays", "/product-category/glass-wooden-cubby-displays/"),
                               ("Cube Displays", "/product-category/cube-displays/")]),
    ("Slatwall &amp; Gridwall", [("Slatwall", "/product-category/slatwall/"), ("Gridwall", "/product-category/gridwall/"),
                                ("Pegboard Hooks", "/product-category/pegboard-hooks/")]),
    ("Racks &amp; Tables", [("Apparel Racks", "/product-category/apparel-racks/"), ("Floor Merchandisers", "/product-category/floor-merchandisers/"),
                           ("Display Tables", "/product-category/display-tables/")]),
    ("Mannequins &amp; Forms", [("Mannequins", "/product-category/mannequins/"), ("Jewelry &amp; Handbag Displays", "/product-category/jewelry-handbag-displays/"),
                               ("Shoe Displays", "/product-category/shoe-displays/"), ("Hat &amp; Eyewear Displays", "/product-category/hat-eyewear-displays/")]),
    ("More", [("Card/Magazine Displays", "/product-category/card-and-magazine-displays/"),
              ("General Store Operations", "/product-category/general-store-operations/"),
              ("Candy &amp; Nut Storage", "/product-category/candy-nut-storage-containers/"),
              ("Vintage-Style Displays", "/product-category/vintage-style-displays/")]),
]

# (name, one-line blurb, image, path, image fit). Photos are hi-res product cutouts downloaded from storedisplays.com.
CATEGORY_TILES = [
    ("Gondola Shelving", "Single, double, wall and end units.", "Double-Sided_WB.png", "/gondola-shelving/", "contain"),
    ("Display Showcases &amp; Counters", "Glass cases that keep product secure and visible.", "ESC4-B.png", "/product-category/counters-showcases/", "contain"),
    ("Slatwall", "Panels, hooks and shelves for any wall.", "sw48b-e1711044363236.jpg", "/product-category/slatwall/", "contain"),
    ("Gridwall", "Flexible panels for varied merchandise.", "gridwall-lg.jpg", "/product-category/gridwall/", "cover"),
    ("Apparel Racks", "Hanging and folding space for boutiques.", "LNHFET.png", "/product-category/apparel-racks/", "contain"),
    ("Mannequins", "Forms that put the outfit in front of shoppers.", "R2204W-1.png", "/product-category/mannequins/", "contain"),
]

HERO = "homepage-hero-3.1.jpg"
BANNER = "1-1-scaled.jpg"
GALLERY = ["grocery-shelving.jpg", "AMKO_ESC6-WHITE.jpg", "0316-113.jpg", "FTC48-SHOWCASE-e1715623739376.jpg", "2-1.jpg", "3-1.jpg"]

# Real posts from the live blog (titles of the last three come from the post addresses)
BLOG = [
    ("How Retail Displays Affect Customer Buying Behavior", "/how-retail-displays-affect-customer-buying-behavior/", "retail-displays.jpg"),
    ("New Store Opening Checklist: Every Retail Fixture You'll Need", "/new-store-opening-checklist/", "open-store-checklist.jpg"),
    ("How to Refresh Your Store Displays Without a Full Renovation", "/how-to-refresh-your-store-displays-without-a-full-renovation/", "refresh-your-store.jpg"),
    ("Gondola Displays: The Retail Layout Secret Behind More Sales", "/gondola-displays-the-retail-layout-secret-behind-more-sales/", "shelves-blur.jpg"),
    ("The Best Shelving Materials for Retail Stores: A Complete Guide", "/the-best-shelving-materials-for-retail-stores-a-complete-guide/", "retail-shelving.jpg"),
    ("12 Creative Ways to Use Gridwall Panels in Your Store", "/12-creative-ways-to-use-gridwall-panels-in-your-store/", "plant-grid-wall.jpg"),
    ("Top 5 Types of Commercial Glass Display Cabinets for Retail Stores", "/top-5-types-of-commercial-glass-display-cabinets-for-retail-stores/", "jewelry-case.jpg"),
    ("Tight on Retail Floor Space? 4 Types of Retail Displays That Maximize Your Real Estate", "/tight-on-retail-floor-space-maximize-your-real-estate-with-these-4-types-of-retail-displays/", "clothes-racks.jpg"),
]

# (slug, name, product kinds to show, intro line, intro is from the live site)
IND = [
    ("apparel-stores", "Apparel Stores", ["rack", "form", "slatwall"], "Stylish setups that captivate and convert.", True),
    ("beauty-supply-shops", "Beauty Supply Shops", ["slatwall", "case"], "Sturdy and organized displays for beauty supplies.", True),
    ("jewelry-stores", "Jewelry Stores", ["case", "form"], "Secure, well-lit showcases for high-ticket items.", False),
    ("liquor-stores", "Liquor Stores", ["gondola", "slatwall"], "Robust gondola shelving built for heavy bottles.", False),
    ("pharmacies", "Pharmacies", ["gondola", "case"], "Organized aisles and secure counters for health and beauty.", False),
    ("pop-up-shops", "Pop-Up Shops", ["rack", "slatwall", "form"], "Quick-setup displays for temporary spaces.", False),
    ("smoke-vape-shops", "Smoke/Vape Shops", ["case", "slatwall"], "Sleek showcases and slatwalls for an enhanced shopping experience.", True),
    ("supermarkets", "Supermarkets", ["gondola"], "Organize your aisles with our robust gondola shelving options.", True),
]
INDUSTRIES = [x[1] for x in IND]
IND_IMG = {
    "apparel-stores": "apparel-stores.jpg", "beauty-supply-shops": "beauty-supply.jpg", "jewelry-stores": "jewelry-store-2.jpg",
    "liquor-stores": "liquor-store.jpg", "pharmacies": "pharmacies.jpg", "pop-up-shops": "popup-store.jpg",
    "smoke-vape-shops": "smoke-vape-shop.jpg", "supermarkets": "supermarket-2.jpg",
}

# Draft SEO copy per industry (sample wording for review). kw = primary keyword, sec = secondary keywords.
IND_SEO = {
    "apparel-stores": dict(
        title="Apparel Store Fixtures & Clothing Racks", kw="apparel store fixtures",
        sec=["clothing racks for boutiques", "retail shelving for apparel stores", "mannequins for fashion stores"],
        h1="Apparel Store Fixtures &amp; Clothing Racks",
        meta="Clothing racks, mannequins, slatwall and gridwall for apparel stores and boutiques. Prices shown, same-day Ground shipping on orders by 2 pm ET.",
        body=[("Build a floor that sells clothes", "Boutiques and apparel stores usually mix hanging space, folded product and a few focal displays. Racks give flexible hanging capacity, etageres combine hanging and folding, and mannequins put the outfit in front of the customer.",
               [("Apparel racks", "/product-category/apparel-racks/"), ("Mannequins", "/product-category/mannequins/")]),
              ("Use the walls too", "Slatwall and gridwall turn perimeter walls into display space for accessories, shoes and folded stacks, which frees the floor for browsing.",
               [("Slatwall", "/product-category/slatwall/"), ("Gridwall", "/product-category/gridwall/")])],
        faq=[("What fixtures do I need to open a clothing boutique?", "Most boutiques start with hanging racks, a few tables or etageres for folded product, a fitting room rack, mannequins for focal points and wall displays for accessories."),
             ("Can I mix racks and slatwall?", "Yes. Many stores hang best sellers on racks and use slatwall hooks and shelves for add-on items.")],
        blog=7),
    "beauty-supply-shops": dict(
        title="Beauty Supply Store Displays & Shelving", kw="beauty supply store displays",
        sec=["slatwall for beauty supplies", "glass display cases for cosmetics", "retail shelving for beauty stores"],
        h1="Beauty Supply Store Displays &amp; Shelving",
        meta="Sturdy slatwall, shelving and glass showcases for beauty supply shops, with prices shown and same-day Ground shipping on orders placed by 2 pm ET.",
        body=[("Organize hundreds of small items", "Beauty supply shops carry many small, light products. Slatwall with hooks and shelves keeps them visible and sorted by category, while gondola runs hold larger packaged goods.",
               [("Slatwall", "/product-category/slatwall/"), ("Gondola shelving", "/gondola-shelving/")]),
              ("Protect the premium items", "Glass showcases and counters keep higher-priced products secure while still on display.",
               [("Display showcases &amp; counters", "/product-category/counters-showcases/")])],
        faq=[("What is the best way to display small beauty products?", "Slatwall hooks, small shelves and countertop displays keep small products visible and easy to restock."),
             ("Do you offer glass cases for cosmetics?", "Yes. See the display showcases and counters category for glass cases and counters.")],
        blog=4),
    "jewelry-stores": dict(
        title="Jewelry Store Display Cases & Showcases", kw="jewelry store display cases",
        sec=["glass display cases for jewelry", "jewelry showcases with lighting", "custom display showcases for luxury items"],
        h1="Jewelry Store Display Cases &amp; Showcases",
        meta="Glass showcases, towers and counters for jewelry stores, plus custom millwork. Prices shown, with same-day Ground shipping on orders by 2 pm ET.",
        body=[("Showcases that keep high-ticket items secure", "Jewelry sells on visibility and trust. Glass showcases and counters with locking doors keep product protected while customers browse, and tower cases add height without taking floor space.",
               [("Display showcases &amp; counters", "/product-category/counters-showcases/")]),
              ("Custom millwork for a signature look", "When a standard case will not fit the space or the brand, custom millwork and built-to-order showcases can match your layout.",
               [("Custom millwork &amp; showcases", "/custom-millwork-showcases/"), ("Jewelry &amp; handbag displays", "/product-category/jewelry-handbag-displays/")])],
        faq=[("What kind of case is best for a jewelry store?", "Glass showcases with locking doors suit most jewelry stores. Tower cases and counters can be combined to build a full floor."),
             ("Can you build a custom jewelry counter?", "Store Displays offers custom millwork and built-to-order showcases. Contact the team with your layout.")],
        blog=6),
    "liquor-stores": dict(
        title="Liquor Store Shelving & Display Fixtures", kw="liquor store shelving",
        sec=["gondola shelving for liquor stores", "wine and spirits display shelving", "heavy duty retail shelving"],
        h1="Liquor Store Shelving &amp; Display Fixtures",
        meta="Heavy-duty gondola shelving rated up to 500 lbs per shelf, plus slatwall and showcases for liquor stores. Prices shown, same-day Ground shipping.",
        body=[("Gondola shelving built for heavy bottles", "Liquor stores stock heavy product, so shelf capacity matters. Store Displays gondola shelving is rated up to 500 lbs per shelf and comes in single-sided, double-sided, wall and end units.",
               [("Gondola shelving", "/gondola-shelving/")]),
              ("Secure the high-value bottles", "Locking glass showcases and counters keep premium bottles and tobacco products secure near the register.",
               [("Display showcases &amp; counters", "/product-category/counters-showcases/")])],
        faq=[("How much weight can gondola shelving hold?", "Store Displays lists shelf capacity of up to 500 lbs per shelf for its gondola shelving."),
             ("Which gondola colors are available?", "Black and Antique White.")],
        blog=3),
    "pharmacies": dict(
        title="Pharmacy Shelving & Counter Displays", kw="pharmacy shelving",
        sec=["pharmacy display fixtures", "retail shelving for pharmacies", "countertop displays for pharmacies"],
        h1="Pharmacy Shelving &amp; Counter Displays",
        meta="Gondola shelving, glass counters and countertop displays for pharmacies. Prices shown, with same-day Ground shipping on orders placed by 2 pm ET.",
        body=[("Clear aisles for health and beauty", "Pharmacies need aisles that are easy to scan. Gondola runs create organized rows for over-the-counter products, with end units for promotions.",
               [("Gondola shelving", "/gondola-shelving/")]),
              ("Counters and impulse displays", "Glass counters and countertop displays keep small, high-value items near the checkout.",
               [("Countertop displays", "/product-category/countertop-displays/"), ("Display showcases &amp; counters", "/product-category/counters-showcases/")])],
        faq=[("Can I add end units to promote products?", "Yes. End units finish a gondola run and are a common place for promotions."),
             ("Do you help plan the layout?", "Request a free store layout plan and the team will help.")],
        blog=3),
    "pop-up-shops": dict(
        title="Pop-Up Shop Displays & Portable Fixtures", kw="pop-up shop displays",
        sec=["portable retail displays", "clothing racks for pop-up stores", "slatwall for temporary retail"],
        h1="Pop-Up Shop Displays &amp; Portable Fixtures",
        meta="Racks, tables, slatwall and mannequins for pop-up shops that set up fast. Prices shown, same-day Ground shipping on orders placed by 2 pm ET.",
        body=[("Set up fast, look established", "Pop-up shops need fixtures that go up quickly and still look complete. Racks, tables and floor merchandisers can be arranged in minutes and moved as the space changes.",
               [("Apparel racks", "/product-category/apparel-racks/"), ("Display tables", "/product-category/display-tables/")]),
              ("Make a small space work harder", "Slatwall panels and gridwall add vertical display area when floor space is limited.",
               [("Slatwall", "/product-category/slatwall/"), ("Gridwall", "/product-category/gridwall/")])],
        faq=[("What do I need for a pop-up store?", "Most pop-ups need a few racks or tables, a wall or gridwall display, signage and a counter."),
             ("How fast do orders ship?", "Ground orders placed by 2 pm ET ship the same day.")],
        blog=1),
    "smoke-vape-shops": dict(
        title="Smoke & Vape Shop Display Cases & Slatwall", kw="vape shop display cases",
        sec=["smoke shop display cases", "slatwall for vape shops", "glass showcases for smoke shops"],
        h1="Smoke &amp; Vape Shop Display Cases &amp; Slatwall",
        meta="Sleek glass showcases and slatwall for smoke and vape shops. Prices shown, with same-day Ground shipping on orders placed by 2 pm ET.",
        body=[("Showcases that sell", "Smoke and vape shops rely on visible, secure product. Glass showcases and counters with locking doors show product clearly while keeping it protected.",
               [("Display showcases &amp; counters", "/product-category/counters-showcases/")]),
              ("Slatwall for accessories", "Slatwall panels with shelves and hooks keep accessories organized on the wall behind the counter.",
               [("Slatwall", "/product-category/slatwall/")])],
        faq=[("What display cases work for a smoke shop?", "Locking glass showcases and counters are the most common choice, often paired with slatwall behind the counter."),
             ("Can I get a case with lighting?", "Some extra vision cases are available with LED spotlights. See the product options.")],
        blog=6),
    "supermarkets": dict(
        title="Supermarket Gondola Shelving & Displays", kw="supermarket gondola shelving",
        sec=["gondola shelving for grocery stores", "affordable gondola shelving", "double sided gondola shelving"],
        h1="Supermarket Gondola Shelving &amp; Store Displays",
        meta="Gondola shelving for supermarkets and grocery stores: single, double, wall and end units rated to 500 lbs per shelf. Prices shown, ships fast.",
        body=[("Organize your aisles with gondola shelving", "Gondola shelving is the backbone of grocery aisles. Double-sided units build freestanding aisles, single-sided and wall units line the perimeter, and end units finish each run.",
               [("Gondola shelving", "/gondola-shelving/")]),
              ("Plan the whole floor", "A free layout plan helps match the number of runs, the height and the aisle width to your space.",
               [("Free store layouts", "layouts.html")])],
        faq=[("What is the difference between single- and double-sided gondola shelving?", "Single-sided units sit against a wall. Double-sided units stand freely and are used to build aisles."),
             ("What sizes are available?", 'Lengths of 30", 36" and 48", depths from 12" to 24" and heights from 48" to 96".')],
        blog=3),
}


def P(id, name, sku, kind, cat, price, fin, img, path, sub, real=True, new=False, fit="contain", badge=False, frm=False):
    return dict(id=id, name=name, sku=sku, kind=kind, cat=cat, price=price, fin=fin, img=img, path=path, sub=sub,
                real=real, new=new, fit=fit, badge=badge, **{"from": frm})


CASE = "Display Showcases &amp; Counters"
# Real products, SKUs, prices and images from storedisplays.com. Gondola prices other than "from $107" are SAMPLE.
PRODUCTS = [
    P("extra-vision-black-4", "4′ Black Standard Extra Vision Display Case", "ESC4/B", "case", CASE, 420, ["Black"],
      UP + "2024/02/ESC4-B-800x800.png", "/product/extra-vision-black-4/", "SKU ESC4/B", new=True),
    P("extra-vision-silver-4", "4′ Silver Standard Extra Vision Display Case", "ESC4", "case", CASE, 400, ["Silver"],
      UP + "2024/02/ESC4-800x800.png", "/product/extra-vision-silver-4/", "SKU ESC4"),
    P("cigarette-cabinet", "Black Cigarette Case", "CIG-84BK", "case", CASE, 890, ["Black"],
      UP + "2026/06/wm_Cigarette_case_BK__5_-1-800x800.jpg", "/product/cigarette-cabinet-black/", "SKU CIG-84BK", badge=True),
    P("tower-67", '67" Tiered Bronze Tower Display Case', "16ET-LIN", "case", CASE, 330, ["Bronze"],
      UP + "2024/02/16ET-LIN-800x800.png", "/product/etagere-glass-towers-67-h/", "SKU 16ET-LIN"),
    P("folding-tower-52", '52"H Folding Glass Tower Case', "FGT52", "case", CASE, 195, ["Silver"],
      UP + "2024/02/FGT52_1-1-800x800.png", "/product/folding-glass-towers-52-h/", "SKU FGT52"),
    P("extra-vision-led", "4′ Black Extra Vision Display Case w/ LED Spotlights", "ESC-4BK-LED", "case", CASE, 985, ["Black"],
      UP + "2024/06/ESC-4BK-LED-2-800x800.png", "/product/extra-vision-led-spotlight-4ft/", "SKU ESC-4BK-LED, fully assembled"),
    P("gondola-single", "Single-Sided Gondola Unit", "GOND-SINGLE", "gondola", "Gondola Shelving", 107, ["Black", "Antique White"],
      UP + "2024/09/Single-Sided_WB.png", "/gondola-shelving/", "Units from $107 on the live site", new=True, frm=True),
    P("gondola-double", "Double-Sided Gondola Unit", "GOND-DOUBLE", "gondola", "Gondola Shelving", 189, ["Black", "Antique White"],
      UP + "2024/09/Double-Sided_WB.png", "/gondola-shelving/", "Starter set or add-on", real=False),
    P("gondola-end", "Gondola End Unit", "GOND-END", "gondola", "Gondola Shelving", 118, ["Black", "Antique White"],
      UP + "2024/09/End-Units_WB.png", "/gondola-shelving/", "Ends a run", real=False),
    P("gondola-upper", "Gondola Upper Shelves", "GOND-UPPER", "gondola", "Gondola Shelving", 36, ["Black", "Antique White"],
      UP + "2024/09/Upper-Shelves_WB.png", "/gondola-shelving/", "Add-on for extra height", real=False),
    P("slatwall-2x4", "2' x 4' Slatwall Panels (Pack of 2) - Black", "SW24B", "slatwall", "Slatwall", 85, ["Black"],
      UP + "2024/02/sw48b-e1711044363236.jpg", "/product/4-x-8-slatwall-panels-white-finish-3/", "SKU SW24B"),
    P("wire-shelf-23", '23"L Wire Shelf - Black', "26-082BL", "slatwall", "Slatwall", 7.5, ["Black"],
      UP + "2025/01/26-082BL-800x800.jpg", "/product/23-wire-shelf-universal/", "SKU 26-082BL"),
    P("etagere", "4-Tier Hybrid Bronze Etagere w/ Hang Bar", "LNHFET", "rack", "Apparel Racks", 455, ["Bronze"],
      UP + "2024/02/LNHFET-800x800.png", "/product/hang-fold-etagere/", "SKU LNHFET", new=True),
    P("fitting-room", "Heavy Duty Rolling Fitting Room Rack w/ Basket - White Metal", "CSC-1T-S12", "rack", "Apparel Racks", 390, ["White"],
      UP + "2024/02/2_15_1-e1711466203636-700x800.jpg", "/product/fitting-room-racks/", "SKU CSC-1T-S12"),
    P("mannequin-white", "White Headless Brazilian Full Body Mannequin", "R2204W", "form", "Mannequins", 125, ["White"],
      UP + "2024/02/R2204W-1-800x800.png", "/product/brazilian-female-headless-full-body-mannequin-with-arms-square-base-white/", "SKU R2204W", new=True),
    P("mannequin-base", "Mannequin Square Base - Matte White", "MB1512/W", "form", "Mannequins", 43, ["White"],
      UP + "2025/01/MB1512-W-800x800.png", "/product/12h-mannequin-square-base-matte-white/", "SKU MB1512/W"),
]

FAQ = [
    ("Where do you ship?", "Store Displays ships within the United States (Alaska and Hawaii excluded per the kickoff). Order by 2 pm ET and Ground orders ship the same day; LTL orders ship the next day."),
    ("Can you help me plan my store layout?", "Yes, in this concept. A free layout request flow is planned. The client asked for free store layouts, in the way Displayarama offers them."),
    ("Do you offer volume discounts?", "The live site has a Volume Discount Pricing page. Tiered pricing may be explored after launch, once performance data exists."),
    ("Do you build custom showcases and millwork?", "The live site has Custom Millwork &amp; Showcases. Real capabilities to be confirmed."),
    ("How does gondola shelving pricing work?", "Today the gondola page is a quote form with units from $107. The redesign aims to show pricing on the page instead."),
    ("Do I need an account to see prices?", "No. Prices are shown on the page, which matches the live site and the client's goal of reducing request-for-quote drop-off."),
]

TESTIMONIALS = [
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
]

# Real phrases from the live home page's "Popular Searches", mapped to a page that would target them
POPULAR = [
    ("Affordable Gondola Shelving for Grocery Stores", "industry-supermarkets.html"),
    ("Best Gridwall Displays for Small Retailers", "/product-category/gridwall/"),
    ("Durable Slatwall Panels with Hooks", "/product-category/slatwall/"),
    ("Retail Shelving Solutions for Apparel Stores", "industry-apparel-stores.html"),
    ("Custom Display Showcases for Luxury Items", "/custom-millwork-showcases/"),
    ("Mannequins for Fashion Boutiques and Stores", "/product-category/mannequins/"),
    ("Floor Merchandisers for Promotional Events", "/product-category/floor-merchandisers/"),
    ("Cube Displays and Cubby Storage for Eyewear", "/product-category/cube-displays/"),
    ("Countertop Displays for Last-Minute Sales Items", "/product-category/countertop-displays/"),
    ("Hanging Solutions for Clothing Stores", "/product-category/apparel-racks/"),
    ("Vintage-Style Store Displays for Niche Shops", "/product-category/vintage-style-displays/"),
]

THEMES = {
    "concept": dict(name="Concept", tag="Light, airy and rounded. Inter type, pill buttons, a rotating photo slideshow, card-style mega menus and industry cards, as on the Concept demo store.",
                    order=["intro", "tiles", "trending", "gondolaband", "industries", "gallery", "reviews", "seo", "blog", "faq", "newsletter"]),
    "release": dict(name="Release", tag="Editorial. A transparent header over a full-bleed hero, light Poppins headlines and banner-led sections, as on the Release demo store.",
                    order=["trending", "dualtiles", "banner", "tiles", "callout", "highlight", "industries", "reviews", "showroom", "seo", "blog", "faq", "newsletter"]),
    "prestige": dict(name="Prestige", tag="Quiet and architectural. Spaced uppercase headings, square buttons and a light grey page, as on the Prestige demo store.",
                     order=["tiles", "trending", "banner", "industries", "highlight", "seo", "blog", "faq", "newsletter"]),
}


# ----------------------------------------------------------------------------
# Shared page chrome
# ----------------------------------------------------------------------------
FONTS = {
    "concept": "Inter:wght@400;500;700",
    "release": "Poppins:wght@300;400;500;600",
    "prestige": "Instrument+Sans:wght@400;500&family=Nunito:wght@400;600;700",
}


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def esc(s):
    return html.escape(s, quote=True)


# ---- SEO helpers ----------------------------------------------------------
def ld_org():
    return {"@context": "https://schema.org", "@type": "Organization", "name": "Store Displays", "url": U + "/",
            "logo": U + UP + "2025/09/sd-logo.png", "telephone": "+1-201-935-2929", "email": EMAIL,
            "address": {"@type": "PostalAddress", "streetAddress": "7 Purcell Ct.", "addressLocality": "Moonachie",
                        "addressRegion": "NJ", "postalCode": "07074", "addressCountry": "US"}}


def ld_site():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": "Store Displays", "url": U + "/",
            "potentialAction": {"@type": "SearchAction", "target": U + "/?s={search_term_string}", "query-input": "required name=search_term_string"}}


def ld_bc(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": plain(n), "item": U + live}
                                for i, (n, _, live) in enumerate(items)]}


def ld_faq(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in items]}


def ld_list(prods):
    return {"@context": "https://schema.org", "@type": "ItemList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": plain(p["name"]), "url": U + p["path"]} for i, p in enumerate(prods[:8])]}


def S(path, title, meta, kw, sec, schema, notes):
    return dict(path=path, title=title, meta=meta, kw=kw, sec=sec, schema=schema, notes=notes)


def head(theme, s):
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=' + FONTS[theme] + '&display=swap">')
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace("</", "<\\/") + "</script>" for x in s["schema"])
    data = json.dumps({"path": s["path"], "kw": s["kw"], "sec": s["sec"], "notes": s["notes"],
                       "schema": [x["@type"] for x in s["schema"]]}).replace("</", "<\\/")
    t, m = esc(plain(s["title"])), esc(plain(s["meta"]))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + t + '</title><meta name="description" content="' + m + '">'
            '<meta property="og:title" content="' + t + '"><meta property="og:description" content="' + m + '"><meta property="og:type" content="website">'
            + fonts + '<link rel="stylesheet" href="style.css">' + ld +
            '<script type="application/json" id="seo-data">' + data + '</script></head><body class="t-' + theme + '">')


def concept_bar(theme, page):
    links = []
    for k, v in THEMES.items():
        cur = ' aria-current="page"' if k == theme else ""
        links.append('<a href="../%s/%s"%s>%s</a>' % (k, page, cur, v["name"]))
    return ('<div class="cbar"><span><strong>Visual concept.</strong> Static mockup modeled on the %s theme\'s public demo store, '
            'not the real theme. Prices, photos and stats are SAMPLE unless noted.</span><nav aria-label="Switch concept">%s'
            '<a href="../index.html">Overview</a></nav></div>') % (THEMES[theme]["name"], "".join(links))


def pic(path, alt, cls="", fit="cover"):
    return '<div class="ph ph-img ph-%s %s"><img src="%s" alt="%s" loading="lazy"></div>' % (fit, cls, img_src(path), esc(alt))


def wordmark():
    return '<a class="logo" href="index.html"><img src="%s" alt="Store Displays" width="150" height="40"></a>' % img_src("sd-logo.png")


# ---- Navigation and mega menus ---------------------------------------------
def mega_list():
    cols = []
    for title, items in MEGA:
        lis = "".join('<li><a href="%s"%s>%s</a></li>' % (href(p), a_attrs(href(p)), l) for l, p in items)
        cols.append('<div class="mcol"><span class="mh">%s</span><ul>%s</ul></div>' % (title, lis))
    promo = ('<div class="mcol mpromo"><strong>Need help choosing?</strong><p>Call <a href="tel:%s">%s</a> or request a free layout plan.</p>'
             '<a class="btn btn-sm" href="layouts.html">Free layout plan</a></div>') % (PHONE_TEL, PHONE1)
    return '<div class="mega" role="menu">%s%s</div>' % ("".join(cols), promo)


def mcard(name, blurb, img, h, fit, dark=False):
    cls = "mcard dark" if dark else "mcard"
    return ('<a class="%s" href="%s"%s><div class="mc-img">%s</div><div class="mc-row"><div><strong>%s</strong><span>%s</span></div>'
            '<i class="mc-arr" aria-hidden="true">&rarr;</i></div></a>') % (cls, h, a_attrs(h), pic(img, name, "", fit), name, blurb)


def mega_cards(kind):
    if kind == "products":
        store = [("Slatwall", "slatwall", "Panels, hooks and shelves for any wall."), ("Gridwall", "gridwall", "Flexible panels for varied merchandise."),
                 ("Apparel Racks", "apparel-racks", "Hanging and folding space for boutiques."), ("Mannequins", "mannequins", "Forms that put the outfit in front of shoppers."),
                 ("Retail Systems", "retail-systems", "Modular systems for full store builds.")]
        cards = "".join(mcard(n, b, CATS[s]["items"][0]["img"], href("/product-category/%s/" % s), "contain") for n, s, b in store if s in CATS)
        cards += mcard("All store fixtures", "Browse every category.", HERO, "collection.html", "cover", True)
    else:
        pick = ["apparel-stores", "jewelry-stores", "liquor-stores", "supermarkets"]
        cards = "".join(mcard(n, b, IND_IMG[s], "industry-%s.html" % s, "cover") for s, n, _, b, _ in IND if s in pick)
        cards += mcard("All industries", "Find your store type.", "apparel-stores.jpg", "industries.html", "cover", True)
    return '<div class="mega mega-cards%s" role="menu">%s</div>' % (" n6" if kind == "products" else "", cards)


HEADER_NAV = {
    "concept": ["Display Cases", "Gondola Shelving", "Store Fixtures &amp; Displays", "Shop by Industry", "Free Store Layouts", "Contact Us"],
    "release": ["Display Cases", "Gondola Shelving", "Store Fixtures &amp; Displays", "Shop by Industry", "Contact Us"],
    "prestige": ["Display Cases", "Gondola Shelving", "Store Fixtures &amp; Displays", "Shop by Industry", "Contact Us"],
}

_SVG = 'viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICON_SVG = {
    "search": '<svg %s><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>' % _SVG,
    "user": '<svg %s><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>' % _SVG,
    "cart": '<svg %s><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8a3 3 0 016 0"/></svg>' % _SVG,
}


def header(theme, page):
    items = []
    for label, h, mega in NAV:
        if label not in HEADER_NAV[theme]:
            continue
        panel = ""
        if mega and theme == "concept":
            panel = mega_cards(mega)
        elif mega == "products":
            panel = mega_list()
        cls = ' class="has-mega"' if panel else ""
        items.append('<li%s><a href="%s"%s>%s</a>%s</li>' % (cls, h, a_attrs(h), label, panel))
    nav = '<nav class="nav" aria-label="Main"><ul>%s</ul></nav>' % "".join(items)
    icons = ('<div class="hicons"><button class="hmenu" type="button" data-hmenu aria-label="Menu" aria-expanded="false">&#9776;</button><a href="#" aria-label="Search">%s</a><a href="#" aria-label="Account">%s</a>'
             '<a class="cart" href="#" aria-label="Cart, 0 items">%s<span>0</span></a></div>') % (
        ICON_SVG["search"], ICON_SVG["user"], ICON_SVG["cart"])
    if theme == "concept":
        ann = ('<div class="ann"><span class="ann-l">f &nbsp; X &nbsp; ig &nbsp; yt</span>'
               '<span class="ann-m">&lsaquo;&nbsp; Order by 2 pm ET and Ground orders ship the same day &nbsp;&rsaquo;</span>'
               '<span class="ann-r"><a href="#" data-modal="ship">Calculate shipping</a> &middot; English &middot; USD $</span></div>')
        inner, cls = wordmark() + nav + icons, "hdr"
    elif theme == "release":
        ann = ('<div class="ann"><span>United States</span><span>Same-day shipping, order by 2 pm ET</span>'
               '<span>Call %s</span><a href="#" data-modal="ship">Calculate shipping</a></div>') % PHONE1
        inner = nav + wordmark() + icons
        cls = "hdr"
    else:
        ann = ('<div class="ann"><span>Same-day shipping on Ground orders placed by 2 pm ET</span>'
               '<span><a href="#" data-modal="ship">Calculate shipping</a> &nbsp;&middot;&nbsp; <a href="layouts.html">Free layout plan</a></span></div>')
        inner, cls = nav + wordmark() + icons, "hdr"
    return '%s%s<header class="%s"><div class="hdr-in">%s</div></header>' % (concept_bar(theme, page), ann, cls, inner)


def modals():
    return ('<div class="modal" id="m-ship" hidden role="dialog" aria-modal="true" aria-label="Calculate shipping"><div class="modal-box">'
            '<button class="modal-close" data-close aria-label="Close">&times;</button><h2>Calculate shipping</h2>'
            '<p class="note">Concept. East, Central and West zones were discussed on the kickoff call. Rates here are SAMPLE.</p>'
            '<form class="form" data-ship><label>ZIP code<input inputmode="numeric" maxlength="5" placeholder="07074" required></label>'
            '<label>Estimated order weight (lb)<input type="number" min="1" value="150"></label><button class="btn">Estimate</button></form>'
            '<div class="ship-out" data-ship-out hidden></div></div></div>'
            '<div class="modal" id="m-bulk" hidden role="dialog" aria-modal="true" aria-label="Request bulk pricing"><div class="modal-box">'
            '<button class="modal-close" data-close aria-label="Close">&times;</button><h2>Request bulk pricing</h2>'
            '<p class="note">Concept of the Get Bulk Pricing form on Displayarama. The live site also has a Volume Discount Pricing page.</p>'
            '<form class="form"><label>Name<input required></label><label>Email<input type="email" required></label>'
            '<label>What are you ordering?<input placeholder="e.g. 4 gondola runs"></label><label>Quantity<input type="number" min="1" value="10"></label>'
            '<button class="btn">Request bulk pricing (demo)</button></form></div></div>'
            '<div class="modal" id="m-pop" hidden role="dialog" aria-modal="true" aria-label="Newsletter"><div class="modal-box">'
            '<button class="modal-close" data-close aria-label="Close">&times;</button><h2>Sign up and get 10% off your first order</h2>'
            '<p class="note">Concept of the newsletter capture discussed on the kickoff call. Final offer and terms to be confirmed.</p>'
            '<form class="form"><label>Email<input type="email" required></label><button class="btn">Get my 10% off (demo)</button></form></div></div>'
            '<div class="toast" data-toast hidden role="status"></div>'
            '<button class="seo-toggle" type="button" data-seo-toggle aria-pressed="false">SEO view</button>'
            '<aside class="seo-panel" data-seo-panel hidden aria-label="SEO view"><div class="sp-head"><strong>SEO view</strong>'
            '<span>Strategy for this page</span></div><div data-seo-body></div></aside>')


def footer(theme):
    def ext(l, p):
        return '<li><a href="%s"%s>%s</a></li>' % (href(p), a_attrs(href(p)), l)
    shop = "".join(ext(l, p) for l, p in [("Gondola shelving", "/gondola-shelving/"), ("Display showcases &amp; counters", "/product-category/counters-showcases/"),
                                           ("Slatwall", "/product-category/slatwall/"), ("Gridwall", "/product-category/gridwall/"),
                                           ("Apparel racks", "/product-category/apparel-racks/"), ("Mannequins", "/product-category/mannequins/")])
    info = "".join(ext(l, p) for l, p in [("About", "/about/"), ("Blog", "/blog/"), ("Contact", "/contact/"), ("FAQs", "/faqs/")])
    info += '<li><a href="layouts.html">Free store layouts</a></li><li><a href="#" data-modal="ship">Calculate shipping</a></li>'
    pol = "".join(ext(l, p) for l, p in [("Volume discount pricing", "/volume-discount-pricing/"), ("Shipping policy", "/shipping-policy/"),
                                          ("Return policy", "/return-policy/"), ("Sitemap", "/sitemap/")])
    ind = "".join('<li><a href="industry-%s.html">%s</a></li>' % (s, n) for s, n, _, _, _ in IND)
    out = ('<footer class="ftr"><div class="wrap fgrid">'
           '<div><div class="logo logo-f"><img src="' + img_src("sd-logo.png") + '" alt="Store Displays" width="150" height="40"></div>'
           '<p>' + ADDRESS + '</p><p>Tel <a href="tel:' + PHONE_TEL + '">' + PHONE1 + '</a><br><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></p></div>'
           '<div><h4>Shop</h4><ul>' + shop + '</ul></div><div><h4>Industries</h4><ul>' + ind + '</ul></div>'
           '<div><h4>Information</h4><ul>' + info + '</ul></div><div><h4>Policies</h4><ul>' + pol + '</ul></div></div>'
           '<div class="wrap fine">Concept mockup for review only. Product names, SKUs, prices and images come from storedisplays.com; '
           'everything marked sample is not final. Not a live store.</div></footer>')
    return out + modals() + '<script src="../assets/app.js"></script></body></html>'


def money(n):
    return "${:,.2f}".format(n) if n != int(n) else "${:,.0f}".format(n)


def p_href(p):
    return "product.html" if p["id"] == "extra-vision-black-4" else href(p["path"])


def card(p, theme):
    h = p_href(p)
    ex = a_attrs(h)
    fins = " ".join(f.lower().replace(" ", "-") for f in p["fin"])
    sw = "".join('<i class="sw sw-%s" title="%s"></i>' % (f.lower().replace(" ", "-"), f) for f in p["fin"][:4])
    badge = '<span class="badge">New</span>' if p["badge"] else ""
    price = ("from " if p["from"] else "") + money(p["price"])
    samp = "" if p["real"] else '<span class="samp">sample</span>'
    return ('<article class="pcard" data-kind="%s" data-fin="%s" data-price="%d" data-new="%d">'
            '<div class="pwrap"><a class="pimg" href="%s"%s>%s%s</a><button class="qadd" type="button" data-qadd>Quick add</button></div>'
            '<div class="pbody"><h3><a href="%s"%s>%s</a></h3>'
            '<p class="pdim">%s</p><div class="sws">%s</div><div class="prow"><strong class="price">%s</strong>%s</div>'
            '<span class="instock">In stock</span><a class="btn btn-sm btn-o" href="%s"%s>View details</a></div></article>'
            ) % (p["kind"], fins, round(p["price"]), 1 if p["new"] else 0, h, ex, pic(p["img"], p["name"], "ph-sm", p["fit"]),
                 badge, h, ex, p["name"], p["sub"], sw, price, samp, h, ex)


def grid(prods, theme, cols=4):
    return '<div class="pgrid c%d">%s</div>' % (cols, "".join(card(p, theme) for p in prods))


def faq_block(items=None):
    items = items or FAQ
    return '<div class="faq">%s</div>' % "".join("<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in items)


def section_head(eyebrow, title, link=None):
    l = '<a class="more" href="%s">View all &rarr;</a>' % link if link else ""
    return '<div class="sh"><div><span class="eyebrow">%s</span><h2>%s</h2></div>%s</div>' % (eyebrow, title, l)


def crumbs(items):
    out = []
    for i, (label, h, _) in enumerate(items):
        out.append(label if i == len(items) - 1 else '<a href="%s">%s</a>' % (h, label))
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">%s</nav>' % " / ".join(out)


def alink(label, path):
    h = href(path) if path.startswith("/") else path
    return '<a href="%s"%s>%s</a>' % (h, a_attrs(h), label)


def blog_card(b, cls="ph-b"):
    t, p, i = b
    return '<a class="bcard" href="%s"%s>%s<h3>%s</h3><span class="more">Read article &rarr;</span></a>' % (U + p, a_attrs(U + p), pic(i, t, cls, "cover"), t)


# ---- Industry cards (used on home, hub and layouts pages) --------------------
def ind_cards():
    cards = "".join('<a class="icard" href="industry-%s.html">%s<div class="ic-copy"><h3>%s</h3><p class="ic-more">%s<b>Shop fixtures &rarr;</b></p></div>'
                    '<span class="ic-plus" aria-hidden="true">+</span></a>' % (s, pic(IND_IMG[s], n + " store fixtures", "", "cover"), n, b)
                    for s, n, _, b, _ in IND)
    return '<div class="ind-cards">%s</div>' % cards


# ---- Home sections --------------------------------------------------------
SLIDES = [
    ("Store displays that capture attention", "Shop display showcases", "collection.html", HERO),
    ("Gondola shelving, priced and ready to ship", "Build your gondola run", "gondola.html", "supermarket-2.jpg"),
    ("Fixtures for every kind of store", "Shop by industry", "industries.html", "apparel-stores.jpg"),
]


def hero(theme):
    if theme == "concept":
        slides = "".join('<div class="slide%s">%s<div class="slide-copy"><%s>%s</%s></div><a class="btn btn-w" href="%s">%s</a></div>'
                         % (" on" if i == 0 else "", pic(img, t, "ph-hero", "cover"), "h1" if i == 0 else "h2", t, "h1" if i == 0 else "h2", h, c)
                         for i, (t, c, h, img) in enumerate(SLIDES))
        dots = "".join('<button class="dot%s" type="button" aria-label="Slide %d"></button>' % (" on" if i == 0 else "", i + 1) for i in range(len(SLIDES)))
        return ('<section class="hero-c" data-slider><div class="slides">%s<button class="s-arr" data-prev type="button" aria-label="Previous slide">&larr;</button>'
                '<button class="s-arr" data-next type="button" aria-label="Next slide">&rarr;</button><div class="dots">%s</div></div></section>') % (slides, dots)
    bg = img_src(HERO)
    if theme == "release":
        return ('<section class="hero-r" style="background-image:linear-gradient(rgba(0,0,0,.4),rgba(0,0,0,.7)),url(%s);background-size:cover;background-position:center">'
                '<div class="hero-r-in"><span class="eyebrow">Chosen by trusted brands nationwide</span>'
                '<h1>Store displays, by design</h1><a class="btn btn-ow" href="collection.html">Discover more</a></div></section>') % bg
    return ('<section class="hero-p" style="background-image:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.7)),url(%s);background-size:cover;background-position:center">'
            '<div class="hero-p-in"><h1>Showcases made to be seen</h1>'
            '<a class="btn btn-lt" href="collection.html">Shop display showcases</a></div></section>') % bg


def sec_intro(theme):
    return ('<section class="sec intro"><div class="wrap narrow center-t"><h2>Store displays that capture attention</h2>'
            '<p>Whether opening a new boutique or redesigning a grocery store, we have everything you need: top-quality products, '
            'best customer service, affordable pricing and fast shipping.</p>'
            '<a class="btn" href="collection.html">Shop store fixtures</a></div></section>')


def sec_dualtiles(theme):
    t = [("Gondola shelving", "Double-Sided_WB.png", "gondola.html", "Build your run", "contain"),
         ("Display showcases &amp; counters", "ESC4-B.png", "collection.html", "Shop showcases", "contain")]
    tiles = "".join('<a class="dtile" href="%s">%s<div class="dt-copy"><span class="eyebrow">Featured</span><h2>%s</h2>'
                    '<span class="btn btn-ow">%s</span></div></a>' % (h, pic(i, n, "ph-dt", f), n, c) for n, i, h, c, f in t)
    return '<section class="sec dual"><div class="wrap-w dual-g">%s</div></section>' % tiles


def sec_banner(theme):
    return ('<section class="banner"><div class="banner-copy"><span class="eyebrow">Free store layouts</span>'
            '<h2>Plan your store with our team</h2>'
            '<a class="btn btn-ow" href="layouts.html">Request your free layout plan</a></div></section>')


def sec_callout(theme):
    return ('<section class="callout"><div class="wrap center-t"><h2>Volume discount pricing</h2>'
            '<p>Ordering more? Request bulk pricing or see the live volume discount pricing page.</p>'
            '<a class="btn" href="#" data-modal="bulk">Request bulk pricing</a> <a class="btn btn-o" href="%s/volume-discount-pricing/" target="_blank" rel="noopener">See volume pricing</a></div></section>') % U


def sec_highlight(theme):
    p = PRODUCTS[0]
    return ('<section class="sec"><div class="wrap split hl-split">%s<div><span class="eyebrow">Item of the week</span><h2>%s</h2>'
            '<p class="pdim">%s</p><p><strong class="price">%s</strong></p>'
            '<div class="ctas"><a class="btn" href="product.html">Shop now</a></div></div></div></section>'
            ) % (pic(p["img"], p["name"], "ph-tall", "contain"), p["name"], p["sub"], money(p["price"]))


def sec_showroom(theme):
    return ('<section class="sec alt"><div class="wrap split"><div><span class="eyebrow">Talk to a person</span><h2>Top-notch, personal service</h2>'
            '<p>When you call, you speak with a knowledgeable team member who can answer your questions immediately.</p>'
            '<p>%s<br>Tel <a href="tel:%s">%s</a></p><a class="btn" href="industries.html#contact">Contact us</a></div>%s</div></section>'
            ) % (ADDRESS, PHONE_TEL, PHONE1, pic("0316-113.jpg", "Store Displays showroom", "ph-wide", "cover"))


def sec_tiles(theme):
    t = "".join('<a class="ctile" href="%s"%s>%s<span class="ct-name">%s</span><span class="ct-go">Shop all &rarr;</span></a>'
                % (href(p), a_attrs(href(p)), pic(i, n, "ph-tile", f), n) for n, b, i, p, f in CATEGORY_TILES)
    return '<section class="sec"><div class="wrap">%s<div class="tiles">%s</div></div></section>' % (
        section_head("Popular product categories", "Shop by category", "collection.html"), t)


def sec_industries(theme):
    return ('<section class="sec alt ind-sec"><div class="wrap"><div class="ind-head"><div><span class="eyebrow">Find your store type</span><h2>Shop by industry</h2></div>'
            '<p>Fixtures, layouts and pricing for the way your store sells. Pick your industry to see recommended products.</p></div>%s'
            '<p class="note">Industries come from the live Industries We Serve page. Dedicated industry pages are a concept.</p></div></section>') % ind_cards()


def sec_trending(theme):
    return ('<section class="sec" id="new"><div class="wrap">%s%s</div></section>'
            % (section_head("Just in", "New &amp; trending products", "collection.html"), grid([p for p in PRODUCTS if p["new"]][:4], theme)))


def sec_gondolaband(theme):
    return ('<section class="gband"><div class="wrap gb-in"><div><span class="eyebrow">Interactive builder</span>'
            '<h2>Build your gondola run</h2><p>Pick the unit type, length, height and finish from the live site\'s real options, and see a price as you go. '
            'Concept only. A real configurator needs an app or custom build.</p>'
            '<a class="btn" href="gondola.html#builder">Start building</a></div>%s</div></section>'
            ) % pic("Double-Sided_WB.png", "Double-sided gondola shelving", "ph-wide", "contain")


def sec_gallery(theme):
    imgs = "".join(pic(g, "Store Displays showcase and shelving photo", "ph-g", "cover") for g in GALLERY)
    return ('<section class="sec"><div class="wrap">%s<div class="gal">%s</div>'
            '<div class="center"><a class="btn" href="tel:%s">Call %s</a></div></div></section>'
            % (section_head("Chosen by trusted brands nationwide", "Store displays that capture attention", None), imgs, PHONE_TEL, PHONE1))


def sec_stats(theme):
    s = [("2 pm ET", "Order by 2 pm ET and Ground orders ship the same day"), ("Next day", "LTL orders ship the next day"),
         ("Thousands", "Of ready-to-ship store displays"), ("A real person", "Call %s for expert help" % PHONE1)]
    return ('<section class="band stats"><div class="wrap srow">%s</div></section>'
            % "".join('<div><strong>%s</strong><span>%s</span></div>' % x for x in s))


def sec_reviews(theme):
    c = "".join('<figure class="rev"><blockquote>%s</blockquote><figcaption>%s</figcaption></figure>' % x for x in TESTIMONIALS)
    return '<section class="sec alt"><div class="wrap">%s<div class="revs">%s</div></div></section>' % (
        section_head("What retailers say", "Customer reviews", None), c)


def sec_faq(theme):
    return '<section class="sec"><div class="wrap narrow">%s%s</div></section>' % (
        section_head("Got questions?", "Frequently asked questions", None), faq_block())


def sec_blog(theme):
    c = "".join(blog_card(BLOG[i]) for i in (3, 1, 0))
    return '<section class="sec alt"><div class="wrap">%s<div class="blogs">%s</div></div></section>' % (
        section_head("Store ideas", "From the blog", U + "/blog/"), c)


def sec_seo(theme):
    inds = "".join("<li>%s</li>" % alink(n, "industry-%s.html" % s) for s, n, _, _, _ in IND)
    pop = "".join("<li>%s</li>" % alink(t, p) for t, p in POPULAR)
    return ('<section class="sec seo-sec"><div class="wrap prose"><h2>Store displays and retail fixtures for every kind of store</h2>'
            '<p>Store Displays&reg; supplies ' + alink("gondola shelving", "/gondola-shelving/") + ', ' + alink("display showcases and counters", "/product-category/counters-showcases/") + ', '
            + alink("slatwall", "/product-category/slatwall/") + ', ' + alink("gridwall", "/product-category/gridwall/") + ' and ' + alink("apparel racks", "/product-category/apparel-racks/") +
            ' to boutiques, supermarkets, liquor stores, pharmacies and more, with prices on the page and same-day shipping on Ground orders placed by 2 pm ET.</p>'
            '<h3>Shop by what you sell</h3><ul class="plinks">' + inds + '</ul>'
            '<h3>Popular searches</h3><ul class="plinks">' + pop + '</ul>'
            '<p class="note">Draft copy for SEO review. The popular searches are the live site\'s own list, linked to the pages that would target them.</p></div></section>')


def sec_newsletter(theme):
    return ('<section class="news"><div class="wrap news-in"><div><h2>Get 10% off your first order</h2>'
            '<p>Concept of the newsletter incentive discussed on the kickoff call. Final offer and terms to be confirmed.</p></div>'
            '<form onsubmit="this.querySelector(\'button\').textContent=\'Thanks (demo)\';return false"><label class="sr" for="em">Email</label>'
            '<input id="em" type="email" placeholder="you@yourstore.com" required><button class="btn">Sign up</button></form></div></section>')


SECS = {
    "intro": sec_intro, "tiles": sec_tiles, "dualtiles": sec_dualtiles, "banner": sec_banner, "callout": sec_callout,
    "highlight": sec_highlight, "showroom": sec_showroom, "industries": sec_industries, "trending": sec_trending,
    "gondolaband": sec_gondolaband, "gallery": sec_gallery, "stats": sec_stats, "reviews": sec_reviews,
    "faq": sec_faq, "blog": sec_blog, "seo": sec_seo, "newsletter": sec_newsletter,
}


SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on", "or", "per", "the", "to", "vs", "via", "x"}


def _tc_word(w, force):
    m = re.match(r"^([^A-Za-z0-9&]*)(.*?)([^A-Za-z0-9;/]*)$", w)
    lead, core, trail = m.group(1), m.group(2), m.group(3)
    if not core or "&" in core or "/" in core or any(c.isdigit() for c in core):
        return w
    if any(c.isupper() for c in core[1:]) or (core.isupper() and len(core) > 1):
        return w
    parts = core.split("-")
    out = []
    for part in parts:
        low = part.lower()
        out.append(low if (low in SMALL_WORDS and not force and len(parts) == 1) else low[:1].upper() + low[1:])
    return lead + "-".join(out) + trail


def _tc_text(t, first, last):
    tokens = re.split(r"(\s+)", t)
    idx = [i for i, x in enumerate(tokens) if x.strip()]
    for n, i in enumerate(idx):
        prev = tokens[idx[n - 1]] if n else ""
        force = (first and n == 0) or (last and n == len(idx) - 1) or prev.endswith((":", "?", "!", "."))
        tokens[i] = _tc_word(tokens[i], force)
    return "".join(tokens)


def tc_headings(doc):
    def fix(m):
        parts = re.split(r"(<[^>]+>)", m.group(3))
        text = [i for i, x in enumerate(parts) if x and not x.startswith("<")]
        for i in text:
            parts[i] = _tc_text(parts[i], i == text[0], i == text[-1])
        return "<h%s%s>%s</h%s>" % (m.group(1), m.group(2), "".join(parts), m.group(1))
    doc = re.sub(r"<h([1-4])([^>]*)>(.*?)</h\1>", fix, doc, flags=re.S)
    return re.sub(r'(<span class="eyebrow">)([^<]*)(</span>)', lambda m: m.group(1) + _tc_text(m.group(2), True, True) + m.group(3), doc)


def shell(theme, s, page, body):
    return tc_headings(head(theme, s) + header(theme, page) + "<main>" + body + "</main>" + footer(theme))


# ---- Pages ----------------------------------------------------------------
def page_home(theme):
    s = S("/", "Store Fixtures & Retail Displays | Store Displays®",
          "Shop gondola shelving, display showcases, slatwall, gridwall and apparel racks with prices shown. Same-day Ground shipping on orders placed by 2 pm ET.",
          "store fixtures", ["retail displays", "display cases", "gondola shelving", "slatwall panels", "clothing racks"],
          [ld_org(), ld_site()],
          ["The live title is 'Official Store Displays®: Shop Display Cases, Store Fixtures, Merchandise Displays'. This proposal is shorter and leads with the primary keyword.",
           "Organization and WebSite schema added.", "A crawlable text block links every category and industry, and the live site's own popular searches.",
           "The hero H1 is a keyword-light brand line in the slideshow; the intro H2 carries the keyword theme."])
    body = hero(theme) + "".join(SECS[k](theme) for k in THEMES[theme]["order"])
    return shell(theme, s, "index.html", body)


def builder():
    return ('<div class="builder" id="builder" data-builder>'
            '<div class="b-steps" data-steps></div><div class="b-panel"><div class="b-q" data-q></div><div class="b-opts" data-opts></div>'
            '<div class="b-nav"><button class="btn btn-o btn-sm" data-back type="button">Back</button>'
            '<button class="btn btn-sm" data-next type="button">Next</button></div></div>'
            '<aside class="b-sum" aria-live="polite"><h3>Your run</h3><ul data-sum></ul>'
            '<div class="b-total"><span>Estimated total</span><strong data-total>$0</strong><small>SAMPLE pricing. The live site lists units from $107.</small></div>'
            '<button class="btn" type="button" data-cta data-qadd>Add to cart (demo)</button>'
            '<a class="btn btn-o" href="layouts.html">Get a free layout plan</a></aside></div>')


def page_gondola(theme):
    g = [p for p in PRODUCTS if p["kind"] == "gondola"]
    bc = [("Home", "index.html", "/"), ("Gondola shelving", "gondola.html", "/gondola-shelving/")]
    tiles = "".join('<div class="vt"><strong>%s</strong><span>%s</span></div>' % x for x in [
        ("Same-day shipping", "Order by 2 pm ET and Ground orders ship the same day. LTL ships the next day."),
        ("Top-notch, personal service", "Call %s and speak with a knowledgeable team member." % PHONE1),
        ("Quality without compromise", "Every item is personally selected, with decades of retail merchandising experience."),
        ("Volume discount pricing", "See the live volume discount pricing page for larger orders.")])
    spec = "".join('<tr><th>%s</th><td>%s</td></tr>' % x for x in [
        ("Unit types", "Single sided, double sided, wall unit, end unit"), ("Usage", "Starter set or add-ons"),
        ("Length", '30" / 36" / 48"'), ("Depth", '12" / 14" / 16" / 18" / 20" / 22" / 24"'),
        ("Height", '48" / 54" / 60" / 72" / 84" / 96" plus 12" and 24" extensions'), ("Colors", "Black / Antique White"),
        ("Shelf capacity", "Up to 500 lbs per shelf")])
    faq = FAQ[4:5] + [("What sizes does gondola shelving come in?", 'Lengths of 30", 36" and 48", depths from 12" to 24" and heights from 48" to 96", plus 12" and 24" extensions.'),
                      ("What is the difference between single- and double-sided gondola shelving?", "Single-sided units sit against a wall. Double-sided units stand freely and are used to build aisles.")]
    s = S("/gondola-shelving/", "Gondola Shelving for Retail & Grocery | Store Displays®",
          "Single-sided, double-sided, wall and end gondola shelving rated up to 500 lbs per shelf. Build your run, see prices, and ship fast from Store Displays®.",
          "gondola shelving", ["retail gondola shelving", "grocery store shelving", "double sided gondola shelving", "gondola shelving for liquor stores"],
          [ld_bc(bc), ld_faq(faq), ld_list(g)],
          ["The live title is 62 characters, just over the guideline. This trims it to 55 without losing the primary keyword.",
           "The live page is a quote form; the concept adds visible prices, a builder and crawlable guidance below the fold.",
           "Internal links point to the supermarket, liquor store and pharmacy industry pages and the live gondola blog post.",
           "FAQPage schema added; spec table is real page content."])
    body = (crumbs(bc) +
            '<section class="ghero"><div class="wrap"><span class="eyebrow">Retail &amp; grocery stores</span><h1>Gondola Shelving</h1>'
            '<p>Where convenience, liquor, grocery and apparel stores shop. Units start from $107 on the live site; this concept puts prices and options on the page instead of a quote form.</p>'
            '<a class="btn" href="#builder">Build your gondola run</a></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Step by step", "Build your gondola run", None) + builder() + '</div></section>'
            '<section class="sec alt"><div class="wrap"><div class="vtiles">' + tiles + '</div></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Unit types", "Gondola shelving products", None) + grid(g, theme, 4) +
            '<p class="note">Single-sided "from $107" is from the live site. Other gondola prices are SAMPLE.</p>'
            '<div class="split spec-split"><div class="seo"><h2>Gondola shelving system specifications</h2><table class="spec">' + spec + '</table>'
            '<p class="note">Specifications are from the live Gondola Shelving page.</p></div>'
            '<div class="seo"><h2>Maximizing vertical space</h2><p>Taller gondola units show more product, as long as everything stays within easy reach of customers. '
            'Single- and double-sided units, end units and upper shelves combine into runs that fit your store.</p>'
            '<div class="ctas"><a class="btn" href="#" data-modal="bulk">Request bulk pricing</a><a class="btn btn-o" href="layouts.html">Request free layout</a></div></div></div>'
            '</div></section>'
            '<section class="sec alt seo-sec"><div class="wrap prose"><h2>Single-sided vs double-sided gondola shelving</h2>'
            '<h3>Single-sided units for walls</h3><p>Single-sided and wall units line the perimeter of a store and hold product at the eye level of shoppers walking past. They are the right choice when a run sits against a wall.</p>'
            '<h3>Double-sided units for aisles</h3><p>Double-sided units stand freely and give you two shelving faces back to back. They build the aisles of a grocery, liquor or convenience store, and end units finish each run.</p>'
            '<h2>Gondola shelving for grocery, liquor and convenience stores</h2>'
            '<p>Gondola shelving is the backbone of aisle layouts. See how it fits a ' + alink("supermarket", "industry-supermarkets.html") + ', a ' + alink("liquor store", "industry-liquor-stores.html") +
            ' or a ' + alink("pharmacy", "industry-pharmacies.html") + ', or read ' + alink(BLOG[3][0], BLOG[3][1]) + '.</p>'
            '<p class="note">Draft copy for SEO review.</p></div></section>'
            '<section class="sec"><div class="wrap narrow">' + section_head("Gondola FAQ", "Questions about gondola shelving", None) + faq_block(faq) + '</div></section>')
    return shell(theme, s, "gondola.html", body)


def page_collection(theme):
    prods = PRODUCTS
    bc = [("Home", "index.html", "/"), ("Store fixtures &amp; displays", "collection.html", "/shop/")]
    kinds = [("case", "Showcases &amp; counters"), ("gondola", "Gondola shelving"), ("slatwall", "Slatwall"), ("rack", "Apparel racks"), ("form", "Mannequins")]
    finishes = ["Black", "White", "Silver", "Bronze", "Antique White"]
    f_kind = "".join('<label><input type="checkbox" data-f="kind" value="%s"> %s</label>' % x for x in kinds)
    f_fin = "".join('<label><input type="checkbox" data-f="fin" value="%s"> <i class="sw sw-%s"></i> %s</label>' % (f.lower().replace(" ", "-"), f.lower().replace(" ", "-"), f) for f in finishes)
    f_price = ('<label><input type="radio" name="pr" data-f="price" value="0-100" > Under $100</label>'
               '<label><input type="radio" name="pr" data-f="price" value="100-500"> $100 to $500</label>'
               '<label><input type="radio" name="pr" data-f="price" value="500-99999"> Over $500</label>'
               '<label><input type="radio" name="pr" data-f="price" value="" checked> Any price</label>')
    side = ('<aside class="filters" data-filters><details open><summary>Type</summary>%s</details>'
            '<details open><summary>Finish / color</summary>%s</details><details open><summary>Price</summary>%s</details>'
            '<button class="btn btn-o btn-sm" type="button" data-clear>Clear filters</button></aside>') % (f_kind, f_fin, f_price)
    faq = FAQ[:4]
    s = S("/shop/", "Store Fixtures & Displays | Store Displays®",
          "Shop store displays and retail fixtures: gondola shelving, display showcases, slatwall, gridwall, apparel racks and mannequins. Prices shown, ships fast.",
          "retail store displays", ["store fixtures for sale", "display cases for retail stores", "slatwall panels", "clothing racks"],
          [ld_bc(bc), ld_list(prods), ld_faq(faq)],
          ["Product-matched H1 and an intro paragraph above the grid, as agreed on the kickoff call.",
           "Color and size are variants, so the roughly 360 live categories collapse into filters instead of thin category pages.",
           "Buying-guide content sits below the grid and links to the gondola, industry and layout pages.", "ItemList and FAQPage schema added."])
    body = (crumbs(bc) +
            '<section class="chero"><div class="wrap"><h1>Store Fixtures &amp; Displays</h1>'
            '<p>Browse store fixtures by type, finish and price. Products below are real items from storedisplays.com, with their SKUs and listing prices.</p></div></section>'
            '<section class="sec"><div class="wrap clayout">' + side +
            '<div class="cmain"><div class="ctool"><span data-count>%d products</span>'
            '<label>Sort <select data-sort><option value="">Featured</option><option value="new">Newest</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option></select></label></div>'
            % len(prods) + '<div data-grid>' + grid(prods, theme, 3) + '</div><p class="empty" data-empty hidden>No products match these filters.</p>'
            '<div class="seo prose"><h2>How to choose store fixtures</h2>'
            '<h3>Match the fixture to the merchandise</h3><p>' + alink("Gondola shelving", "/gondola-shelving/") + ' suits many small items in aisles. Glass ' + alink("showcases", "/product-category/counters-showcases/") +
            ' protect high-ticket items. ' + alink("Slatwall", "/product-category/slatwall/") + ' and ' + alink("gridwall", "/product-category/gridwall/") + ' turn walls into flexible display space.</p>'
            '<h3>Plan for space and traffic</h3><p>Leave room for customers to move. A ' + alink("free layout plan", "layouts.html") + ' helps match fixtures to your floor.</p>'
            '<h3>Shop by what you sell</h3><p>Not sure where to start? Browse fixtures for ' + alink("apparel stores", "industry-apparel-stores.html") + ', ' + alink("liquor stores", "industry-liquor-stores.html") +
            ' or ' + alink("jewelry stores", "industry-jewelry-stores.html") + '.</p><p class="note">Draft copy for SEO review.</p></div></div></div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("FAQ", "Store fixture questions", None) + faq_block(faq) + '</div></section>')
    return shell(theme, s, "collection.html", body)


def page_product(theme):
    p = PRODUCTS[0]
    rel = [x for x in PRODUCTS if x["kind"] == "case" and x["id"] != p["id"]][:4]
    bc = [("Home", "index.html", "/"), ("Store fixtures &amp; displays", "collection.html", "/shop/"),
          ("Display showcases &amp; counters", "collection.html", "/product-category/counters-showcases/"), (p["name"], "product.html", p["path"])]

    def opts(name, rows):
        out = ""
        for i, (label, add) in enumerate(rows):
            out += ('<label class="swl"><input type="radio" name="%s" value="%s" %s data-opt data-add="%d"> %s</label>'
                    % (name, label, "checked" if i == 0 else "", add, label))
        return out
    colors = opts("color", [("Black", 0), ("Silver", -20)])
    types = opts("type", [("Regular base", 0), ("LED spotlights", 565), ("RGB lighted base", 180)])
    sizes = opts("size", [("4'", 0), ("5'", 60), ("6'", 120)])
    faq = [("Does the extra vision display case come assembled?", "It ships unassembled and is built for easy assembly. Assembly instructions are available to download on the live product page."),
           ("Does the case lock?", "Yes. It has sliding doors with a key and lock."),
           ("What size is the 4-foot case?", '48" x 20" x 38" (L x W x H), with a top glass of 46 3/4" x 18 3/4" and a 34" display area.')]
    product_ld = {"@context": "https://schema.org", "@type": "Product", "name": plain(p["name"]), "sku": p["sku"],
                  "image": [U + UP + "2024/02/ESC4-B.png", U + UP + "2024/02/ESC4-B_2.png"],
                  "description": "High-quality showcase with tempered glass finish, 2 rows of adjustable shelves, black aluminum frame, 4 inch kick base and sliding doors with key and lock.",
                  "brand": {"@type": "Brand", "name": "Store Displays"},
                  "offers": {"@type": "Offer", "url": U + p["path"], "priceCurrency": "USD", "price": "%.2f" % p["price"],
                             "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition"}}
    s = S(p["path"], "4′ Black Extra Vision Display Case | Store Displays®",
          "4-foot black extra vision glass display case with tempered glass, 2 adjustable shelves and a locking sliding door. 48 x 20 x 38 in. In stock, ships fast.",
          "extra vision display case", ["4 ft glass display case", "black aluminum display case", "locking glass showcase"],
          [ld_bc(bc), product_ld, ld_faq(faq)],
          ["The live title is 61 characters. This shortened title keeps the keyword, and the description adds the size and lock, which searchers compare on.",
           "Product schema with price, SKU, availability and images; BreadcrumbList and FAQPage schema.",
           "The FAQ answers come from facts on the live product page (ships unassembled, key and lock, dimensions).",
           "Internal links go to the category, the glass cabinet buying guide and the layout page."])
    body = (crumbs(bc) +
            '<section class="sec"><div class="wrap pdp"><div class="gal-p">' +
            pic("ESC4-B.png", p["name"], "ph-main", "contain") +
            '<div class="thumbs">' + pic("ESC4-B.png", "Front view of " + p["name"], "ph-th", "contain") +
            pic("ESC4-B_2.png", "Side view of " + p["name"], "ph-th", "contain") + '</div></div>'
            '<div class="info"><span class="eyebrow">Display showcases &amp; counters</span><h1>' + p["name"] + '</h1>'
            '<p class="sku">SKU <span data-sku>%s</span> &middot; In stock</p>' % p["sku"] +
            '<div class="prow big"><strong class="price" data-price data-base="%d">%s</strong></div>' % (p["price"], money(p["price"])) +
            '<p class="note">Base price is the live listing price. Option prices: LED spotlights and the 5\' size are based on live listings, the rest are SAMPLE.</p>'
            '<fieldset class="opt"><legend>Color</legend>' + colors + '</fieldset>'
            '<fieldset class="opt"><legend>Type</legend>' + types + '</fieldset>'
            '<fieldset class="opt"><legend>Size</legend>' + sizes + '</fieldset>'
            '<label class="opt">Quantity <input type="number" min="1" value="1" data-qty></label>'
            '<div class="ctas"><button class="btn" type="button" data-add>Add to cart (demo)</button>'
            '<a class="btn btn-o" href="#" data-modal="bulk">Request bulk pricing</a></div>'
            '<ul class="hl"><li>High-quality showcase with tempered glass finish</li><li>Maximum visibility, 2 rows of adjustable shelves</li>'
            '<li>Sleek black aluminum frame, 4" kick base</li><li>Sliding doors with key and lock</li><li>Easy assembly, built to last. Ships unassembled</li></ul>'
            '<details open><summary>Specifications</summary><table class="spec"><tr><th>4-foot size</th><td>48" x 20" x 38" (L x W x H)</td></tr>'
            '<tr><th>Top glass</th><td>46 3/4" x 18 3/4"</td></tr><tr><th>Top shelf</th><td>8" W x 46" L</td></tr>'
            '<tr><th>Bottom shelf</th><td>10" W x 46" L</td></tr><tr><th>Display area</th><td>34" H</td></tr>'
            '<tr><th>Kick base</th><td>4" (black)</td></tr><tr><th>Weight</th><td>138 lbs</td></tr></table></details>'
            '<details><summary>Shipping &amp; delivery</summary><p>Order by 2 pm ET and Ground orders ship the same day; LTL orders ship the next day. '
            'Concept excludes Alaska and Hawaii per the kickoff.</p></details>'
            '<details><summary>Downloads</summary><p>Assembly instructions download link goes here, as on the live product page.</p></details>'
            '<p class="note">Features, specifications, SKU and images are from the live product page at storedisplays.com.</p></div></div></section>'
            '<section class="sec alt seo-sec"><div class="wrap prose"><h2>About the 4′ black standard extra vision display case</h2>'
            '<p>This showcase pairs a sleek black aluminum frame with tempered glass for maximum visibility, two rows of adjustable shelves and sliding doors that lock with a key. '
            'It is a popular choice for ' + alink("jewelry stores", "industry-jewelry-stores.html") + ', ' + alink("smoke and vape shops", "industry-smoke-vape-shops.html") + ' and ' +
            alink("pharmacies", "industry-pharmacies.html") + '.</p>'
            '<p>Browse more in ' + alink("display showcases and counters", "/product-category/counters-showcases/") + ', or read ' + alink(BLOG[6][0], BLOG[6][1]) + '.</p>'
            '<p class="note">Draft copy for SEO review.</p></div></section>'
            '<section class="sec"><div class="wrap narrow">' + section_head("FAQ", "Questions about extra vision display cases", None) + faq_block(faq) + '</div></section>'
            '<section class="sec alt"><div class="wrap">' + section_head("You may also like", "Related showcases", None) + grid(rel, theme, 4) + '</div></section>')
    return shell(theme, s, "product.html", body)


def page_industries(theme):
    bc = [("Home", "index.html", "/"), ("Shop by industry", "industries.html", "/industries-we-serve/")]
    s = S("/industries-we-serve/", "Retail Fixtures by Industry | Store Displays®",
          "Find retail fixtures for your store type: apparel, beauty supply, jewelry, liquor, pharmacies, pop-up shops, smoke/vape shops and supermarkets.",
          "store displays by industry", ["retail fixtures by store type", "fixtures for boutiques", "grocery store shelving", "jewelry store display cases"],
          [ld_bc(bc), ld_org()],
          ["The live page is 'Industries We Serve'. The concept makes each industry its own landing page, which gives every industry a page to rank for its own keyword.",
           "This hub links all eight industry pages and the free layout page.",
           "Industry cards use the live site's own industry photography."])
    body = (crumbs(bc) +
            '<section class="chero"><div class="wrap"><span class="eyebrow">Industries served by Store Displays&reg;</span><h1>Shop by Industry</h1>'
            '<p>Find fixtures for your store type. The live site lists these industries on its Industries We Serve page; here each one becomes its own landing page, linked to products and blog posts.</p></div></section>'
            + sec_stats(theme) +
            '<section class="sec ind-sec"><div class="wrap">' + ind_cards() + '<p class="note">Each card opens a concept industry page. The live site lists the same industries on its Industries We Serve page.</p></div></section>'
            '<section class="sec alt"><div class="wrap center-t"><span class="eyebrow">Free store layouts</span><h2>Not sure what your store needs?</h2>'
            '<p>Request a free layout plan or book a call with our team.</p><a class="btn" href="layouts.html">Free store layouts</a></div></section>'
            '<section class="sec" id="custom"><div class="wrap">' + pic(BANNER, "Custom millwork and made-in-USA showcases from Store Displays", "ph-banner-img", "cover") +
            '<div class="split custom-split"><div><span class="eyebrow">Custom millwork &amp; showcases</span><h2>Custom showcases and millwork</h2>'
            '<p>The live site has a Custom Millwork &amp; Showcases page. Final copy for this section comes from the client.</p>'
            '<a class="btn" href="' + U + '/custom-millwork-showcases/" target="_blank" rel="noopener">See the live page</a></div>' +
            pic("2-1.jpg", "Custom glass showcase", "ph-wide", "cover") + '</div></div></section>'
            '<section class="sec alt" id="about"><div class="wrap narrow"><span class="eyebrow">About Store Displays&reg;</span><h2>One-stop shop for store displays</h2>'
            '<p>Placeholder about copy. Per the live site, Store Displays personally selects its merchandise and brings decades of retail merchandising experience. '
            'Final story to come from the client.</p></div></section>'
            '<section class="sec" id="contact"><div class="wrap split"><div><span class="eyebrow">Contact</span><h2>Talk to a fixture expert</h2>'
            '<p>' + ADDRESS + '</p><p>Tel <a href="tel:%s">%s</a><br><a href="mailto:%s">%s</a></p></div>' % (PHONE_TEL, PHONE1, EMAIL, EMAIL) +
            '<form class="form" onsubmit="this.querySelector(\'button\').textContent=\'Thanks (demo)\';return false"><label>Name<input required></label>'
            '<label>Email<input type="email" required></label><label>Message<textarea rows="3"></textarea></label><button class="btn">Send (demo)</button></form></div></section>')
    return shell(theme, s, "industries.html", body)


def page_layouts(theme):
    bc = [("Home", "index.html", "/"), ("Free store layouts", "layouts.html", "/free-store-layouts/")]
    faq = FAQ[1:3]
    steps = "".join('<li><strong>%s</strong><span>%s</span></li>' % x for x in [
        ("Tell us about your store", "Store type, size and what you sell."), ("Share your floor plan", "Upload a sketch or photos."),
        ("Get your layout", "Concept. Turnaround time to be confirmed.")])
    types = "".join("<option>%s</option>" % n for n in INDUSTRIES) + "<option>Other</option>"
    tiles = "".join('<a class="itile" href="industry-%s.html"><span class="it-n">%s</span><span class="it-g">Shop fixtures &rarr;</span></a>' % (sl, n) for sl, n, _, _, _ in IND)
    done = "this.querySelector('button').textContent='Thanks (demo)';return false"
    s = S("/free-store-layouts/", "Free Store Layout Planning | Store Displays®",
          "Request a free store layout plan or book a layout call or showroom visit with the Store Displays® team.",
          "free store layout", ["store layout planning", "retail store layout help", "book a showroom visit"],
          [ld_bc(bc), ld_faq(faq)],
          ["A new page: the client liked the free layout service on Displayarama. It targets layout-planning searches and feeds quote-ready leads.",
           "FAQPage and BreadcrumbList schema; the industry links route visitors to the right industry page."])
    body = (crumbs(bc) +
            '<section class="chero"><div class="wrap"><span class="eyebrow">Free store layouts</span><h1>Free Store Layouts</h1>'
            '<p>Concept page for the free layout service the client liked on Displayarama. Request a layout plan, or book a call or a showroom visit.</p></div></section>'
            '<section class="sec"><div class="wrap split"><div><h2>How it works</h2><ol class="steps">' + steps + '</ol></div>'
            '<form class="form" onsubmit="' + done + '"><label>Name<input required></label><label>Email<input type="email" required></label>'
            '<label>Store type<select>' + types + '</select></label><label>Store size (sq ft)<input type="number" min="1"></label>'
            '<label>Tell us about your space<textarea rows="3"></textarea></label><button class="btn">Request layout (demo)</button></form></div></section>'
            '<section class="sec alt" id="book"><div class="wrap"><div class="sh"><div><span class="eyebrow">Appointment scheduling</span>'
            '<h2>Book a layout call or showroom visit</h2></div></div><div class="book" data-book><div>'
            '<h3>1. What would you like?</h3><div class="bk-types" data-bk-types></div><h3>2. Pick a day</h3><div class="bk-days" data-bk-days></div>'
            '<h3>3. Pick a time</h3><div class="bk-times" data-bk-times></div></div><div><h3>Your appointment</h3>'
            '<div class="bk-conf" data-bk-out hidden></div><form class="form" onsubmit="' + done + '"><label>Name<input required></label>'
            '<label>Email<input type="email" required></label><label>Phone<input type="tel"></label><button class="btn">Confirm booking (demo)</button></form>'
            '<p class="note">Showroom: ' + ADDRESS + '. Availability is SAMPLE. Real scheduling needs a booking app.</p></div></div></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Plans by store type", "We plan for every kind of store", "industries.html") +
            '<div class="itiles">' + tiles + '</div></div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("FAQ", "Layout questions", None) + faq_block(faq) + '</div></section>')
    return shell(theme, s, "layouts.html", body)


def page_industry(theme, slug):
    _, name, kinds, blurb, real = next(x for x in IND if x[0] == slug)
    c = IND_SEO[slug]
    prods = [p for p in PRODUCTS if p["kind"] in kinds]
    page = "industry-%s.html" % slug
    live = "/industries-we-serve/%s/" % slug
    bc = [("Home", "index.html", "/"), ("Shop by industry", "industries.html", "/industries-we-serve/"), (name, page, live)]
    others = [x for x in IND if x[0] != slug][:4]
    check = "".join("<li>%s</li>" % x for x in [
        "A free layout plan for your floor", "Fixtures sized to your space and merchandise",
        "Volume discount pricing on larger orders", "Same-day shipping on Ground orders placed by 2 pm ET"])
    sections = "".join('<h2>%s</h2><p>%s</p><p>%s</p>' % (h2, txt, " &middot; ".join(alink(l, p) for l, p in links)) for h2, txt, links in c["body"])
    s = S(live, c["title"] + " | Store Displays®", c["meta"], c["kw"], c["sec"], [ld_bc(bc), ld_faq(c["faq"]), ld_list(prods)],
          ["Unique title, description and H1 built around '" + c["kw"] + "'.",
           "Two content sections link to the category pages, the free layout page and a related live blog post.",
           "FAQPage, ItemList and BreadcrumbList schema. Related-industry links keep visitors moving between store types.",
           "Draft copy for SEO review: tone and claims need client sign-off."])
    body = (crumbs(bc) +
            '<section class="chero"><div class="wrap"><span class="eyebrow">Shop by industry</span><h1>' + c["h1"] + '</h1>'
            '<p>' + blurb + '</p><p class="note">' + ("Intro line is from the live site." if real else "Intro line is sample copy.") +
            ' Industry pages are a concept: they double as SEO landing pages linked to products and blog posts.</p>'
            '<div class="ctas"><a class="btn" href="layouts.html">Free layout plan</a><a class="btn btn-o" href="#" data-modal="bulk">Request bulk pricing</a></div></div></section>'
            '<section class="sec"><div class="wrap split ind-hero">' + pic(IND_IMG[slug], name + " store", "ph-tall", "cover") +
            '<div class="prose"><h2>Store displays for ' + name.lower() + '</h2>' + sections + '</div></div></section>'
            '<section class="sec alt"><div class="wrap">' + section_head("Recommended for " + name.lower(), "Popular fixtures", "collection.html") +
            grid(prods, theme, 4) + '</div></section>'
            '<section class="sec"><div class="wrap split"><div><span class="eyebrow">What you get</span><h2>Everything for your ' + name.lower() + '</h2>'
            '<ul class="hl">' + check + '</ul><div class="ctas"><a class="btn" href="layouts.html#book">Book a call</a></div></div>'
            + pic(GALLERY[0], "Store Displays shelving", "ph-wide", "cover") + '</div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("FAQ", "Questions from " + name.lower(), None) + faq_block(c["faq"]) + '</div></section>'
            '<section class="sec"><div class="wrap"><div class="two-col"><div>' + section_head("Related reading", "From the blog", U + "/blog/") + '<div class="blogs one">' + blog_card(BLOG[c["blog"]]) + '</div></div>'
            '<div><div class="sh"><div><span class="eyebrow">Other store types</span><h2>More industries</h2></div></div><ul class="plinks one">' +
            "".join("<li>%s</li>" % alink(n, "industry-%s.html" % sl) for sl, n, _, _, _ in others) + '</ul></div></div></div></section>')
    return shell(theme, s, page, body)


# ---- Category pages (Concept collection layout) ---------------------------------
CAT_HERO = {
    "shelving": "grocery-shelving.jpg", "wall-standards": "0316-113.jpg", "retail-systems": "0316-113.jpg",
    "counters-showcases": "FTC48-SHOWCASE-e1715623739376.jpg", "countertop-displays": "3-1.jpg",
    "glass-wooden-cubby-displays": "FTC48-SHOWCASE-e1715623739376.jpg", "cube-displays": "FTC48-SHOWCASE-e1715623739376.jpg",
    "slatwall": "0316-113.jpg", "gridwall": "popup-store.jpg", "pegboard-hooks": "0316-113.jpg", "apparel-racks": "apparel-stores.jpg",
    "floor-merchandisers": "popup-store.jpg", "display-tables": "FTC48-SHOWCASE-e1715623739376.jpg", "mannequins": "0316-113.jpg",
    "jewelry-handbag-displays": "jewelry-store-2.jpg", "shoe-displays": "0316-113.jpg", "hat-eyewear-displays": "0316-113.jpg",
    "card-and-magazine-displays": "pharmacies.jpg", "general-store-operations": "supermarket-2.jpg",
    "candy-nut-storage-containers": "supermarket-2.jpg", "vintage-style-displays": "smoke-vape-shop.jpg",
}
FINISH_WORDS = ["Black", "White", "Silver", "Chrome", "Bronze", "Cream", "Gold", "Brown", "Gray", "Grey", "Natural", "Cherry", "Maple", "Walnut", "Red", "Blue", "Clear"]


def cat_finish(name):
    low = name.lower()
    for f in FINISH_WORDS:
        if re.search(r"\b" + f.lower() + r"\b", low):
            return "Gray" if f == "Grey" else f
    return None


def cat_size(name):
    m = re.search(r"\d+(?:\.\d+)?\s?(?:[′'\"″]|-?in(?:ch)?\b)\s*(?:[xX×]\s*\d+(?:\.\d+)?\s*(?:[′'\"″]|-?in(?:ch)?\b)?)?\s*[LWHD]?", name)
    return m.group(0).strip() if m else None


def cat_card(it, cname, slug):
    name = html.escape(it["name"], quote=False)
    fin = cat_finish(it["name"])
    size = cat_size(it["name"])
    if fin:
        sv, sl = fin, "Finish"
    elif size:
        sv, sl = html.escape(size, quote=False), "Size"
    else:
        sv, sl = cname, "Category"
    price = money(it["price"]) if it["price"] is not None else "See product"
    if it["reg"] and it["price"] and it["reg"] > it["price"]:
        badge = '<span class="cc-badge sale">Save %d%%</span>' % round((1 - it["price"] / it["reg"]) * 100)
        pr = '<span class="cc-price sale">%s<s>%s</s></span>' % (price, money(it["reg"]))
    else:
        badge = ""
        pr = '<span class="cc-price">%s</span>' % price
    h = "product.html" if it["url"] == "/product/extra-vision-black-4/" else U + it["url"]
    ex = a_attrs(h)
    sw = '<div class="cc-sw"><i class="sw sw-%s" title="%s"></i></div>' % (fin.lower(), fin) if fin else ""
    return ('<article class="pcard ccard" data-kind="%s" data-fin="%s" data-price="%d" data-new="0">'
            '<a class="cc-img" href="%s"%s>%s%s</a><div class="cc-body"><span class="cc-brand">%s</span>'
            '<div class="cc-row"><a class="cc-name" href="%s"%s>%s</a>%s</div>%s</div>'
            '<div class="cc-specs"><div><i class="cc-ic"></i><span><b>%s</b><small>SKU</small></span></div>'
            '<div><i class="cc-ic"></i><span><b>%s</b><small>%s</small></span></div></div>'
            '<button class="qadd" type="button" data-qadd>Quick add</button></article>'
            ) % (slug, fin.lower() if fin else "", round(it["price"] or 0), h, ex, badge, pic(it["img"], it["name"], "", "contain"),
                 cname.upper(), h, ex, name, pr, sw, html.escape(it["sku"] or "n/a", quote=False), sv, sl)


def cat_blurb(name, subs):
    names = [html.escape(s, quote=False) for s, _ in subs[:3]]
    lead = "Shop %s at Store Displays&reg;" % name.lower()
    if names:
        lead += ", including " + ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1]
    return (lead + ". Prices and SKUs are shown on every card, and Ground orders placed by 2 pm ET ship the same day. "
            "Not sure what fits your store? Request a free layout plan and the team will help.")


def page_category(theme, slug):
    c = CATS[slug]
    name = html.escape(c["h1"], quote=False)
    path = "/product-category/%s/" % slug
    page = "cat-%s.html" % slug
    items = c["items"]
    subs = [x for x in c["subs"] if not cat_finish(x[0])]  # colour options become variants and filters, as agreed on the call
    total = c["total"]
    live = U + path
    shown = total if total else len(items)
    top = slug == "counters-showcases"
    bc = [("Home", "index.html", "/")] + ([] if top else [("Store fixtures &amp; displays", "collection.html", "/shop/")]) + [(name, page, path)]
    hero_img = CAT_HERO.get(slug, "apparel-stores.jpg")
    tabs = '<a class="on" href="#">All %s<sup>%s</sup></a>' % (name, ("%d" % shown) if total else "%d+" % len(items))
    for s_name, s_slug in subs[:5]:
        tabs += '<i>/</i><a href="%s/product-category/%s/%s/" target="_blank" rel="noopener">%s</a>' % (U, slug, s_slug, html.escape(s_name, quote=False))
    fins = []
    for it in items:
        f = cat_finish(it["name"])
        if f and f not in fins:
            fins.append(f)
    f_fin = "".join('<label><input type="checkbox" data-f="fin" value="%s"> <i class="sw sw-%s"></i> %s</label>' % (f.lower(), f.lower(), f) for f in fins) or '<p class="note">No finish options in this selection.</p>'
    f_price = ('<label><input type="radio" name="pr" data-f="price" value="0-100"> Under $100</label>'
               '<label><input type="radio" name="pr" data-f="price" value="100-500"> $100 to $500</label>'
               '<label><input type="radio" name="pr" data-f="price" value="500-99999"> Over $500</label>'
               '<label><input type="radio" name="pr" data-f="price" value="" checked> Any price</label>')
    cards = [cat_card(it, name, slug) for it in items]
    promo = ('<a class="promo-card" href="layouts.html">%s<div class="pc-copy"><i class="pc-ic"></i><h3>Free store layouts</h3>'
             '<p>Not sure what fits your space? Our team will plan your floor, free.</p><span class="btn btn-ow">Request a layout <b>&rarr;</b></span></div></a>'
             ) % pic("popup-store.jpg" if hero_img != "popup-store.jpg" else "supermarket-2.jpg", "Store layout planning", "", "cover")
    cards.insert(min(7, len(cards)), promo)
    tip = ('<div class="cc-tip"><div><strong>Not sure which one fits?</strong><p>Call %s or request a free layout plan, and the team will match fixtures to your space.</p></div>'
           '<a class="btn" href="layouts.html">Free layout plan</a></div>') % PHONE1
    cards.insert(min(8, len(cards)), tip)
    pager = ""
    if total and total > 32:
        n_pages = -(-total // 32)
        nums = "".join('<a href="%spage/%d/" target="_blank" rel="noopener">%d</a>' % (live, k, k) for k in range(2, min(n_pages, 3) + 1))
        pager = ('<div class="pager"><a class="on" href="#" aria-current="page">1</a>%s'
                 '<a class="next" href="%spage/2/" target="_blank" rel="noopener">Next &rarr;</a></div>') % (nums, live)
    seo_txt = cat_blurb(name, subs)
    descr = plain(seo_txt)
    faq = [("What %s does Store Displays carry?" % plain(name).lower(), "Browse %s on the live site, with the price and SKU on every item. Sub-categories include %s." % (
               ("%d products" % total) if total else "the full range", ", ".join(plain(html.escape(s, quote=False)) for s, _ in subs[:3]) or "the options shown above")),
           ("How fast do orders ship?", "Order by 2 pm ET and Ground orders ship the same day; LTL orders ship the next day."),
           ("Can you help me plan my store layout?", "Yes. Request a free layout plan or book a call, and the team will help match fixtures to your floor.")]
    sub_names = [plain(html.escape(s, quote=False)) for s, _ in subs[:3]]
    meta = "Shop %s with prices shown" % name.lower()
    if sub_names:
        meta += ", including " + ", ".join(sub_names[:2]) + (" and " + sub_names[2] if len(sub_names) > 2 else "")
    meta += ". Same-day Ground shipping on orders by 2 pm ET."
    if len(plain(meta)) > 155:
        meta = "Shop %s with prices shown. Same-day Ground shipping on orders placed by 2 pm ET." % name.lower()
    s = S(path, "%s | Store Displays®" % name, meta, name.lower().replace("&amp;", "&"),
          [x.lower() for x in sub_names] + [name.lower().replace("&amp;", "&") + " for sale"],
          [ld_bc(bc), {"@context": "https://schema.org", "@type": "CollectionPage", "name": plain(name), "url": U + path, "description": descr},
           ld_list([dict(name=i["name"], path=i["url"]) for i in items]), ld_faq(faq)],
          ["Product-matched H1, sub-category links and a text block below the grid, as agreed on the kickoff call.",
           "Sub-categories come from the live category's own navigation, so they match what the store already organizes.",
           "Cards show real SKUs, prices and sale prices from the live listing; the layout follows the Concept collection template.",
           "The text block is template-based draft copy, to be replaced by written category copy after keyword research."])
    trust = "".join('<div><i class="tr-ic"></i><span><b>%s</b><small>%s</small></span></div>' % x for x in [
        ("Customer service", "Call %s and speak with a knowledgeable team member." % PHONE1),
        ("Same-day shipping", "Order by 2 pm ET and Ground orders ship the same day."),
        ("Volume pricing", "Request bulk pricing on larger orders."),
        ("Free store layouts", "Our team will plan your floor, free.")])
    body = ('<section class="cat-hero">%s<div class="wrap cat-hero-in"><nav class="cat-crumbs" aria-label="Breadcrumb"><a href="index.html" aria-label="Home">&#8962;</a>'
            '<a href="collection.html">Store Fixtures &amp; Displays</a><span>%s</span></nav><h1>%s</h1></div></section>'
            '<section class="cat-main"><div class="wrap-w">'
            '<div class="cat-tools"><button class="pill" type="button" data-filter-toggle aria-expanded="false"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/></svg><span>Show filters</span></button>'
            '<nav class="cat-tabs" aria-label="Sub-categories">%s</nav>'
            '<a class="cat-viewall" href="%s" target="_blank" rel="noopener">View all %s on storedisplays.com</a>'
            '<label class="pill sortpill"><select data-sort aria-label="Sort"><option value="">Best selling</option><option value="lo">Price: low to high</option>'
            '<option value="hi">Price: high to low</option></select></label></div>'
            '<div class="cat-filters" data-filters hidden><div><h4>Finish</h4>%s</div><div><h4>Price</h4>%s</div>'
            '<div><button class="btn btn-o btn-sm" type="button" data-clear>Clear filters</button></div></div>'
            '<p class="cat-count"><span data-count>%d products</span> shown%s</p>'
            '<div data-grid><div class="pgrid cc-grid">%s</div></div><p class="empty" data-empty hidden>No products match these filters.</p>%s'
            '<div class="center"><a class="btn btn-o" href="%s" target="_blank" rel="noopener">See the full range on storedisplays.com</a></div></div></section>'
            '<section class="cat-seo" style="background-image:linear-gradient(rgba(14,14,14,.86),rgba(14,14,14,.93)),url(%s)"><div class="wrap"><i class="cs-ic"></i>'
            '<span class="cs-label">%s</span><p>%s</p><p class="note-d">Draft copy for SEO review, built from the live category and its sub-categories.</p></div></section>'
            '<section class="trust"><div class="wrap">%s</div></section>'
            ) % (pic(hero_img, name + " store displays", "", "cover"), name, name, tabs, live, ("%d" % shown) if total else "all", f_fin, f_price, len(items),
                 (" of %d on the live site" % total) if total else " (first page)", "".join(cards), pager, live, img_src(hero_img), name.upper(), seo_txt, trust)
    intro = 'Browse %s with prices and SKUs on every card. Ground orders placed by 2 pm ET ship the same day, and the team can plan your layout for free.' % name.lower()
    body = body.replace('<div class="cat-tools">', '<p class="cat-intro">' + intro + '</p><div class="cat-tools">', 1)
    faq_html = ('<section class="sec alt"><div class="wrap narrow">' + section_head("FAQ", "Questions about " + name.lower(), None) + faq_block(faq) + '</div></section>')
    body = body.replace('<section class="cat-seo"', faq_html + '<section class="cat-seo"', 1)
    if top:
        body = body.replace('<a href="collection.html">Store Fixtures &amp; Displays</a>', '', 1)
    return shell(theme, s, page, body)


PAGES = {"index.html": page_home, "gondola.html": page_gondola, "collection.html": page_collection,
         "product.html": page_product, "industries.html": page_industries, "layouts.html": page_layouts}
for _s, _n, _k, _b, _r in IND:
    PAGES["industry-%s.html" % _s] = (lambda t, s=_s: page_industry(t, s))
for _c in CATS:
    PAGES["cat-%s.html" % _c] = (lambda t, s=_c: page_category(t, s))


# ----------------------------------------------------------------------------
# CSS: shared base + per-theme tokens/overrides
# ----------------------------------------------------------------------------
BASE_CSS = r"""
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:var(--body);color:var(--ink);background:var(--bg);line-height:1.55;font-size:16px}
img,svg{max-width:100%}a{color:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px}.narrow{max-width:820px}
.sr{position:absolute;left:-9999px}
h1,h2,h3,h4{font-family:var(--head);line-height:1.1;margin:0 0 .5em;letter-spacing:var(--ls)}
h1{font-size:clamp(2.2rem,5vw,3.8rem)}h2{font-size:clamp(1.6rem,3vw,2.3rem)}h3{font-size:1.05rem}
p{margin:0 0 1em}.note{font-size:.85rem;color:var(--mute)}.center{text-align:center;margin-top:28px}
.eyebrow{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.14em;color:var(--accent);font-weight:700;margin-bottom:.6em}
.btn{display:inline-block;background:var(--accent);color:var(--on-accent);border:2px solid var(--accent);padding:.85em 1.5em;border-radius:var(--r);font-weight:700;text-decoration:none;cursor:pointer;font-family:inherit;font-size:.95rem;text-transform:var(--btt)}
.btn:hover{filter:brightness(1.08)}.btn-o{background:transparent;color:var(--ink);border-color:var(--ink)}
.btn-sm{padding:.55em 1em;font-size:.85rem}.ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:1.4em}
.cbar{background:#111;color:#fff;font-size:.78rem;padding:7px 20px;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}
.cbar nav a{color:#fff;margin-left:14px;opacity:.75;text-decoration:none}.cbar nav a[aria-current]{opacity:1;border-bottom:2px solid #fff}
.ann{background:var(--accent);color:var(--on-accent);text-align:center;font-size:.82rem;padding:7px 12px;font-weight:600}
.hdr{background:var(--hdr);color:var(--hdr-ink);position:relative;z-index:50;border-bottom:var(--hdr-bd)}
@media(min-height:760px) and (min-width:981px){.hdr{position:sticky;top:0}}
.hdr-in{max-width:1240px;margin:0 auto;padding:12px 20px;display:flex;flex-wrap:wrap;align-items:center;gap:14px 24px}
.logo{text-decoration:none;display:flex;flex-direction:column;line-height:1;font-family:var(--head)}
.logo-a{font-size:1.9rem;font-weight:900;letter-spacing:.06em}.logo-d{font-size:.66rem;letter-spacing:.42em;opacity:.8}
.cart{text-decoration:none;font-weight:700}.cart span{background:var(--accent);color:var(--on-accent);border-radius:99px;padding:1px 8px;margin-left:4px;font-size:.8rem}
.nav{order:5;width:100%}.nav>ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 22px}
.nav>ul>li>a{display:block;padding:.4em 0;text-decoration:none;font-weight:600;font-size:.92rem;text-transform:var(--ntt)}
.nav>ul>li>a:hover{color:var(--accent)}.has-mega{position:static}
.mega{display:none;position:absolute;left:0;right:0;background:#fff;color:#1a1a1a;box-shadow:0 18px 30px rgba(0,0,0,.18);padding:24px max(20px,calc((100% - 1200px)/2));grid-template-columns:repeat(7,1fr);gap:20px;border-top:3px solid var(--accent)}
.has-mega:hover .mega,.has-mega:focus-within .mega{display:grid}
.mcol ul{list-style:none;margin:6px 0 0;padding:0}.mcol li a{display:block;padding:3px 0;text-decoration:none;font-size:.85rem;color:#444}.mcol li a:hover{color:var(--accent)}
.mh{font-weight:800;text-decoration:none;font-size:.9rem}.mpromo{background:#f4f4f4;padding:14px;border-radius:8px;font-size:.85rem}
.sec{padding:clamp(40px,6vw,76px) 0}.alt{background:var(--alt)}
.sh{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:28px;flex-wrap:wrap}.sh h2{margin:0}
.more{font-weight:700;text-decoration:none;color:var(--accent);font-size:.9rem}
.ph{position:relative;background:linear-gradient(135deg,var(--ph1),var(--ph2));border-radius:var(--r);overflow:hidden;display:flex;align-items:center;justify-content:center;aspect-ratio:4/3;color:var(--ph-ink)}
.ph-ic{width:46%;opacity:.55}.ph-label{position:absolute;left:10px;bottom:8px;font-size:.68rem;opacity:.75;letter-spacing:.04em}
.ph-sm{aspect-ratio:1/1}.ph-wide{aspect-ratio:16/10}.ph-tall{aspect-ratio:4/5}.ph-main{aspect-ratio:1/1}.ph-th{aspect-ratio:1/1}.ph-g{aspect-ratio:4/3}.ph-b{aspect-ratio:16/10;margin-bottom:12px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.ctile{position:relative;display:block;text-decoration:none}.ct-name{display:block;font-weight:800;font-family:var(--head);font-size:1.1rem;margin-top:10px;text-transform:var(--ntt)}
.ct-go{font-size:.85rem;color:var(--accent);font-weight:700}
.itiles{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.itile{display:flex;flex-direction:column;gap:6px;padding:22px 18px;background:var(--card);border:1px solid var(--line);border-radius:var(--r);text-decoration:none;min-height:104px;justify-content:space-between}
.itile:hover{border-color:var(--accent);transform:translateY(-2px)}.it-n{font-family:var(--head);font-weight:800;font-size:1.05rem}.it-g{font-size:.82rem;color:var(--accent);font-weight:700}
.pgrid{display:grid;gap:22px}.pgrid.c4{grid-template-columns:repeat(4,1fr)}.pgrid.c3{grid-template-columns:repeat(3,1fr)}
.pcard{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}
.pimg{position:relative;display:block}.pimg .ph{border-radius:0}.badge{position:absolute;top:10px;left:10px;background:var(--accent);color:var(--on-accent);font-size:.7rem;font-weight:800;padding:3px 9px;border-radius:99px;text-transform:uppercase;letter-spacing:.05em}
.pbody{padding:14px 16px 18px;display:flex;flex-direction:column;gap:6px;flex:1}.pbody h3{margin:0}.pbody h3 a{text-decoration:none}
.pdim{font-size:.8rem;color:var(--mute);margin:0}.prow{display:flex;align-items:baseline;gap:8px}.price{font-size:1.25rem;font-family:var(--head)}
.samp{font-size:.68rem;text-transform:uppercase;color:var(--mute);letter-spacing:.08em}.instock{font-size:.78rem;color:#1c7a3a;font-weight:700}
.pbody .btn{margin-top:auto;text-align:center}
.sws{display:flex;gap:5px}.sw{display:inline-block;width:16px;height:16px;border-radius:50%;border:1px solid rgba(0,0,0,.25);vertical-align:middle}
.sw-black,.sw-matte-black{background:#171717}.sw-white{background:#fff}.sw-chrome{background:linear-gradient(135deg,#eee,#9aa)}.sw-barnwood{background:#8a6f55}.sw-clear{background:rgba(180,210,230,.5)}
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.band{background:var(--alt);padding:28px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lbl{text-align:center;font-size:.78rem;text-transform:uppercase;letter-spacing:.14em;color:var(--mute);margin-bottom:14px}
.lrow{display:flex;justify-content:space-around;gap:14px;flex-wrap:wrap}.lrow span{padding:10px 22px;border:1px dashed var(--line);border-radius:8px;color:var(--mute);font-size:.8rem}
.srow{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;text-align:center}.srow strong{display:block;font-family:var(--head);font-size:2rem;color:var(--accent)}.srow span{font-size:.8rem;color:var(--mute)}
.revs,.blogs{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.rev{margin:0;background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:24px}.rev blockquote{margin:0 0 12px}.rev figcaption{font-size:.82rem;color:var(--mute)}
.bcard{text-decoration:none;display:block}.bcard h3{margin-bottom:6px}.bcard p{color:var(--mute);font-size:.9rem}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}.faq summary{cursor:pointer;font-weight:700;font-family:var(--head);list-style:none;display:flex;justify-content:space-between}
.faq summary::after{content:"+";color:var(--accent);font-size:1.3rem;line-height:1}.faq details[open] summary::after{content:"\2212"}.faq p{margin:10px 0 0;color:var(--mute)}
.gband{background:var(--dark);color:#fff;padding:clamp(40px,6vw,70px) 0}.gb-in{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:center}
.gband .btn{background:var(--accent);color:var(--on-accent)}.gband .ph{--ph1:#2a3140;--ph2:#3c465a;--ph-ink:#fff}
.news{background:var(--accent);color:var(--on-accent);padding:44px 0}.news-in{display:flex;gap:30px;justify-content:space-between;align-items:center;flex-wrap:wrap}
.news h2{margin:0 0 6px}.news p{margin:0;opacity:.9}.news form{display:flex;gap:10px;flex-wrap:wrap}.news input{padding:.8em 1em;border:0;border-radius:var(--r);min-width:240px;font-family:inherit}
.news .btn{background:#111;border-color:#111;color:#fff}
.ftr{background:var(--dark);color:#d9d9d9;padding:50px 0 24px;font-size:.9rem}.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr 1fr;gap:30px}
.ftr h4{color:#fff;font-size:.95rem}.ftr ul{list-style:none;margin:0;padding:0}.ftr li{margin:6px 0}.ftr a{text-decoration:none}.ftr a:hover{text-decoration:underline}
.logo-f{color:#fff;margin-bottom:12px}.fine{margin-top:30px;padding-top:16px;border-top:1px solid rgba(255,255,255,.15);font-size:.78rem;opacity:.7}
.crumbs{padding:16px 20px;font-size:.82rem;color:var(--mute)}.crumbs a{text-decoration:none}
.chero,.ghero{background:var(--alt);padding:40px 0;border-bottom:1px solid var(--line)}.chero h1,.ghero h1{font-size:clamp(2rem,4vw,3rem)}.chero p,.ghero p{max-width:640px;color:var(--mute)}
.clayout{display:grid;grid-template-columns:240px 1fr;gap:30px}.filters details{border-bottom:1px solid var(--line);padding:12px 0}.filters summary{font-weight:700;cursor:pointer;font-family:var(--head)}
.filters label{display:flex;align-items:center;gap:8px;padding:4px 0;font-size:.9rem}.filters .btn{margin-top:14px}
.ctool{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;font-size:.9rem;flex-wrap:wrap;gap:10px}.ctool select{padding:.5em;font-family:inherit}
.seo{margin-top:40px;padding:26px;background:var(--alt);border-radius:var(--r)}.empty{padding:30px;text-align:center;color:var(--mute)}
.vtiles{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.vt{background:var(--card);padding:20px;border:1px solid var(--line);border-radius:var(--r)}.vt strong{display:block;font-family:var(--head);margin-bottom:6px}.vt span{font-size:.85rem;color:var(--mute)}
.pdp{display:grid;grid-template-columns:1.05fr 1fr;gap:44px}.thumbs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px}
.sku{color:var(--mute);font-size:.85rem}.prow.big .price{font-size:2rem}.opt{display:block;border:0;padding:0;margin:18px 0}.opt legend{font-weight:700;margin-bottom:8px}
.swl{display:inline-flex;gap:6px;align-items:center;margin-right:14px;padding:6px 12px;border:1px solid var(--line);border-radius:99px;cursor:pointer}.swl:has(input:checked){border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.opt input[type=number]{width:80px;padding:.5em;margin-left:8px}.hl{padding-left:1.1em}.hl li{margin:4px 0}
.info details{border-top:1px solid var(--line);padding:12px 0}.info summary{cursor:pointer;font-weight:700;font-family:var(--head)}
.spec{width:100%;border-collapse:collapse;margin-top:10px;font-size:.9rem}.spec th{text-align:left;width:34%;color:var(--mute);font-weight:600;padding:7px 0;border-bottom:1px solid var(--line)}.spec td{padding:7px 0;border-bottom:1px solid var(--line)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:center}
.form{display:grid;gap:12px;background:var(--card);border:1px solid var(--line);padding:24px;border-radius:var(--r)}.form label{display:grid;gap:4px;font-weight:600;font-size:.88rem}
.form input,.form select,.form textarea{padding:.7em;border:1px solid #cfcfcf;border-radius:6px;font-family:inherit;font-size:.95rem}
.steps{padding-left:1.2em}.steps li{margin:12px 0}.steps strong{display:block}.steps span{color:var(--mute);font-size:.9rem}
.builder{display:grid;grid-template-columns:150px 1fr 300px;gap:24px;align-items:start}
.b-steps{display:flex;flex-direction:column;gap:6px}.b-steps button{text-align:left;border:1px solid var(--line);background:var(--card);padding:.6em .8em;border-radius:var(--r);cursor:pointer;font-family:inherit;font-size:.85rem}
.b-steps button.on{background:var(--accent);color:var(--on-accent);border-color:var(--accent);font-weight:700}.b-steps button.done::after{content:" \2713"}
.b-panel{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:24px;min-height:320px;display:flex;flex-direction:column}
.b-q{font-family:var(--head);font-size:1.3rem;font-weight:800;margin-bottom:16px}.b-opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;flex:1;align-content:start}
.b-opts button{border:2px solid var(--line);background:var(--bg);padding:14px 12px;border-radius:var(--r);cursor:pointer;font-family:inherit;text-align:left;font-size:.9rem}
.b-opts button.sel{border-color:var(--accent);background:var(--alt);font-weight:700}.b-opts small{display:block;color:var(--mute);font-weight:400;margin-top:3px}
.b-nav{display:flex;justify-content:space-between;margin-top:20px}
.b-sum{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px;position:static;display:grid;gap:10px}.b-sum ul{list-style:none;margin:0;padding:0;font-size:.88rem}.b-sum li{display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-bottom:1px solid var(--line)}
.b-total{display:grid}.b-total strong{font-size:2rem;font-family:var(--head)}.b-total small{color:var(--mute)}
@media(max-width:980px){.mega{display:none!important}.tiles,.revs,.blogs,.gal{grid-template-columns:1fr 1fr}.itiles,.pgrid.c4{grid-template-columns:1fr 1fr}.pgrid.c3{grid-template-columns:1fr 1fr}
.fgrid,.srow,.vtiles{grid-template-columns:1fr 1fr}.clayout,.pdp,.split,.gb-in{grid-template-columns:1fr}.builder{grid-template-columns:1fr}.b-steps{flex-direction:row;flex-wrap:wrap}.b-sum{position:static}}
@media(max-width:560px){.tiles,.revs,.blogs,.gal,.itiles,.pgrid.c4,.pgrid.c3,.fgrid,.srow,.vtiles{grid-template-columns:1fr}}
"""

EXTRA_CSS = r"""
.center-t{text-align:center}.wrap-w{max-width:1900px;margin:0 auto;padding:0 24px}
.ann{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:10px 24px;font-size:.78rem}
.hdr-in{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px;max-width:1900px;padding:16px 28px}
.nav{order:0;width:auto}.nav a{white-space:nowrap}.hicons{display:flex;gap:18px;align-items:center}.hicons a{display:inline-flex;text-decoration:none;color:inherit}
.cart{position:relative}.cart span{position:absolute;top:-8px;right:-10px;font-size:.62rem;padding:0 5px;line-height:1.5;margin:0}
.dual-g{display:grid;grid-template-columns:1fr 1fr;gap:16px}.dtile{position:relative;display:block;text-decoration:none;color:#fff;overflow:hidden}
.dtile .ph{aspect-ratio:4/3;border-radius:inherit;--ph1:#2b2b2b;--ph2:#161616;--ph-ink:#fff}
.dt-copy{position:absolute;inset:auto 0 0 0;padding:32px;text-align:left}.dt-copy h2{margin:.2em 0 .6em}.dt-copy .eyebrow{color:#fff;opacity:.8}
.banner{position:relative;min-height:520px;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;background:linear-gradient(135deg,#2a2f38,#101216)}
.banner-copy{padding:60px 20px}.banner-copy .eyebrow{color:#fff;opacity:.8}.banner-copy h2{margin-bottom:1em}
.callout{padding:70px 0;background:var(--alt)}.hl-split .ph{max-width:520px}
.ph-img{background:#f6f6f6}.ph-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.ph-contain img{object-fit:contain;padding:6%}
.ph-img .ph-ic,.ph-img .ph-label{display:none}
.logo img{height:34px;width:auto;display:block}.ftr .logo img{filter:brightness(0) invert(1)}.t-release .hdr-over .logo img{filter:brightness(0) invert(1)}
.mh{display:block}.sw-silver{background:linear-gradient(135deg,#f2f4f6,#aab2b8)}.sw-bronze{background:#8c6a43}.sw-cream{background:#f1e8d3}.sw-antique-white{background:#eee6d2}.sw-glass{background:rgba(180,210,230,.5)}
.spec-split{align-items:start;margin-top:40px}.spec-split .seo{margin-top:0}
.modal{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.55);padding:20px}.modal[hidden]{display:none}
.modal-box{background:var(--bg);color:var(--ink);max-width:460px;width:100%;padding:28px;border-radius:var(--r);position:relative;max-height:90vh;overflow:auto}
.modal-close{position:absolute;top:8px;right:14px;border:0;background:none;font-size:1.7rem;cursor:pointer;color:inherit;line-height:1}
.modal-box h2{font-size:1.4rem;text-transform:none;letter-spacing:0;margin-bottom:.4em;padding-right:24px}.modal-box .form{border:0;padding:0;background:none}
.ship-out{margin-top:14px;padding:14px;background:var(--alt);border-radius:var(--r);font-size:.92rem}.ann a{color:inherit}
.book{display:grid;grid-template-columns:1.1fr 1fr;gap:32px}.book h3{margin:.2em 0 .6em;font-size:1rem}
.bk-types,.bk-days,.bk-times{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}
.bk-types button,.bk-days button,.bk-times button{border:1px solid var(--line);background:var(--card);padding:.6em .9em;border-radius:var(--r);cursor:pointer;font-family:inherit;font-size:.88rem;color:inherit}
.bk-sel{border-color:var(--accent)!important;box-shadow:0 0 0 1px var(--accent);font-weight:700}.bk-conf{padding:14px;background:var(--alt);border-radius:var(--r);margin-bottom:14px}
@media(max-width:980px){.book{grid-template-columns:1fr}}
.pwrap{position:relative}.qadd{display:none}.pimg{display:block}
.ind-head{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;margin-bottom:28px;flex-wrap:wrap}.ind-head h2{margin:0}.ind-head p{max-width:420px;color:var(--mute);margin:0}
.ind-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.icard{position:relative;display:block;aspect-ratio:3/4;overflow:hidden;border-radius:var(--r);text-decoration:none;color:#fff;background:#222;isolation:isolate}
.icard .ph{position:absolute;inset:0;border-radius:0;aspect-ratio:auto;transition:transform .7s ease}.icard:hover .ph{transform:scale(1.07)}
.icard::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.78));z-index:1}
.ic-copy{position:absolute;left:20px;right:70px;bottom:20px;z-index:2}.ic-copy h3{margin:0 0 .3em;font-size:1.45rem;line-height:1.05;color:#fff;font-weight:700}
.ic-more{margin:0;font-size:.9rem;line-height:1.3;max-height:0;opacity:0;overflow:hidden;transition:max-height .4s ease,opacity .4s ease}
.icard:hover .ic-more,.icard:focus-visible .ic-more{max-height:150px;opacity:1}.ic-more b{display:block;margin-top:.6em}
.ic-plus{position:absolute;right:16px;bottom:16px;z-index:2;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.22);display:grid;place-items:center;font-size:1.5rem;transition:transform .3s,background .3s,color .3s}
.icard:hover .ic-plus{transform:rotate(45deg);background:#fff;color:#171717}
@media(hover:none){.ic-more{max-height:none;opacity:1}}
@media(max-width:980px){.ind-cards{grid-template-columns:1fr 1fr}}@media(max-width:560px){.ind-cards{grid-template-columns:1fr}}
.mega-cards.n6{grid-template-columns:repeat(6,1fr)}.mega .mcard,.mega .mcard *{white-space:normal}
.mega-cards{grid-template-columns:repeat(5,1fr);gap:16px;padding:22px 32px 32px;border-top:0;border-radius:0 0 16px 16px}
.mcard{display:flex;flex-direction:column;background:#fafafa;border-radius:16px;overflow:hidden;text-decoration:none;color:#171717;transition:transform .25s,box-shadow .25s}
.mcard:hover{transform:translateY(-4px);box-shadow:0 14px 28px rgba(0,0,0,.1)}
.mc-img{position:relative;aspect-ratio:1/.8}.mc-img .ph{position:absolute;inset:0;border-radius:0;aspect-ratio:auto;background:transparent}
.mc-row{display:flex;justify-content:space-between;align-items:flex-end;gap:10px;padding:14px 18px 18px}
.mc-row strong{display:block;font-size:1.25rem;letter-spacing:-.03em;line-height:1.1;font-weight:700}.mc-row span{font-size:.86rem;color:#555;line-height:1.25;display:block;margin-top:4px}
.mc-arr{font-style:normal;font-size:1.4rem;transition:transform .25s}.mcard:hover .mc-arr{transform:translateX(5px)}
.mcard.dark{background:#171717;color:#fff;position:relative;justify-content:flex-end;min-height:260px}
.mcard.dark .mc-img{position:absolute;inset:0;aspect-ratio:auto}.mcard.dark .mc-img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.1),rgba(0,0,0,.78))}
.mcard.dark .mc-row{position:relative;z-index:2}.mcard.dark .mc-row span{color:#ddd}
.has-mega>a{position:relative}.has-mega>a::after{content:"";position:absolute;left:-12px;right:-12px;top:100%;height:34px}
@keyframes mdrop{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}.has-mega:hover .mega{animation:mdrop .2s ease}
.prose{max-width:860px}.prose h2{font-size:clamp(1.4rem,2.4vw,1.9rem);margin:1.2em 0 .5em}.prose h2:first-child{margin-top:0}.prose h3{font-size:1.1rem;margin:1.2em 0 .4em}
.prose p{color:var(--mute);line-height:1.65}.prose a{text-decoration:underline;text-underline-offset:3px}
.plinks{list-style:none;padding:0;margin:0 0 1em;columns:2;column-gap:32px}.plinks li{padding:.35em 0;break-inside:avoid}.plinks a{color:var(--ink);text-decoration:underline;text-underline-offset:3px}.plinks.one{columns:1}
.seo-sec .prose{max-width:960px}.ind-hero{align-items:start}.ind-hero .ph{max-width:480px}
.two-col{display:grid;grid-template-columns:1.2fr 1fr;gap:40px}.blogs.one{grid-template-columns:1fr}
.ph-banner-img{aspect-ratio:2560/836;border-radius:var(--r);margin-bottom:32px}.custom-split{align-items:center}
@media(max-width:980px){.two-col{grid-template-columns:1fr}.plinks{columns:1}}
[hidden]{display:none!important}
.btn-ow{background:transparent;color:#fff;border-color:#fff}
.hdr-over{background:transparent;color:#fff;position:absolute;top:auto;left:0;right:0;z-index:20;border-bottom:0}
.hdr-over .logo img{filter:brightness(0) invert(1)}.hdr-over .cart span{background:#fff;color:#111}
.sw-gold{background:#c9a66b}.sw-brown{background:#6b4a2f}.sw-gray{background:#9a9a9a}.sw-natural{background:#d8c3a0}.sw-cherry{background:#7a2e22}.sw-maple{background:#d9b98a}.sw-walnut{background:#5a3d28}.sw-red{background:#c62828}.sw-blue{background:#1e4fa3}
.cat-hero{position:relative;min-height:380px;display:flex;align-items:flex-end;color:#fff;background:#111;overflow:hidden}
.cat-hero .ph{position:absolute;inset:0;border-radius:0;aspect-ratio:auto}
.cat-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,.25) 45%,rgba(0,0,0,.7));z-index:1}
.cat-hero-in{position:relative;z-index:2;padding-bottom:30px;padding-top:140px}
.cat-crumbs{display:flex;align-items:center;gap:16px;font-size:.85rem;margin-bottom:16px}.cat-crumbs a{color:#fff;text-decoration:none}.cat-crumbs a+a::before,.cat-crumbs span::before{content:"";display:inline-block;width:5px;height:5px;border-top:1.5px solid #fff;border-right:1.5px solid #fff;transform:rotate(45deg);margin-right:14px;vertical-align:middle}
.cat-hero h1{font-size:clamp(3rem,7.5vw,6rem);line-height:1;margin:0;color:#fff;letter-spacing:-.04em}
.cat-main{background:var(--bg);border-radius:20px 20px 0 0;margin-top:-20px;position:relative;z-index:3;padding:28px 0 60px}
.cat-tools{display:flex;flex-wrap:wrap;align-items:center;gap:14px 30px;padding:6px 0 18px}
.pill{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--ink);border-radius:999px;padding:.7em 1.3em;font:500 .9rem var(--body);background:transparent;cursor:pointer;color:var(--ink);transition:background .2s,color .2s}
.pill:hover{background:var(--ink);color:var(--bg)}.sortpill select{border:0;background:transparent;font:inherit;color:inherit;cursor:pointer;outline:0;padding-right:4px}
.cat-tabs{display:flex;gap:6px 14px;align-items:baseline;flex:1;flex-wrap:wrap}.cat-tabs a{font-size:1.15rem;color:#b5b5b5;text-decoration:none;letter-spacing:-.02em;transition:color .2s}
.cat-tabs a:hover{color:var(--ink)}.cat-tabs a.on{color:var(--ink);border-bottom:1.5px solid var(--ink)}.cat-tabs sup{font-size:.55em;margin-left:2px}.cat-tabs i{color:#ccc;font-style:normal}
.cat-viewall{font-size:.85rem;text-decoration:underline;text-underline-offset:3px}
.cat-filters{display:flex;gap:48px;flex-wrap:wrap;padding:18px 24px;margin-bottom:12px;background:var(--alt);border-radius:var(--r)}.cat-filters h4{margin:0 0 .5em;font-size:.9rem}.cat-filters label{display:flex;align-items:center;gap:8px;padding:3px 0;font-size:.9rem}
.cat-count{font-size:.85rem;color:var(--mute);margin:0 0 14px}
.cc-grid{grid-template-columns:repeat(4,1fr);gap:12px}
.ccard{position:relative;background:#fafafa;border-radius:var(--r);overflow:hidden;border:0;display:flex;flex-direction:column;transition:box-shadow .25s,transform .25s}
.ccard:hover{box-shadow:0 12px 28px rgba(0,0,0,.08);transform:translateY(-3px)}
.cc-img{display:block;position:relative;aspect-ratio:1/1}.cc-img .ph{position:absolute;inset:0;background:transparent;border-radius:0;aspect-ratio:auto}.cc-img .ph img{transition:transform .5s}.ccard:hover .cc-img .ph img{transform:scale(1.04)}
.cc-badge{position:absolute;top:14px;left:14px;z-index:2;background:#3f6212;color:#fff;border-radius:99px;padding:.2em .85em;font-size:.72rem}.cc-badge.sale{background:#e11d48}
.cc-body{padding:0 18px 12px}.cc-brand{display:block;font:500 .6rem/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;color:#8a8a8a;margin:6px 0}
.cc-row{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.cc-name{font-size:.95rem;color:var(--ink);text-decoration:none;line-height:1.2}
.cc-price{white-space:nowrap;font-size:.9rem}.cc-price s{display:block;color:#999;font-size:.78rem;text-align:right}.cc-price.sale{color:#e11d48;font-weight:600;text-align:right}
.cc-sw{display:flex;gap:6px;margin-top:10px}.cc-specs{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid #ececec;margin-top:auto}
.cc-specs div{display:flex;align-items:center;gap:10px;padding:12px 18px;font-size:.85rem;min-width:0}.cc-specs div+div{border-left:1px solid #ececec}
.cc-specs b{display:block;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cc-specs small{display:block;color:#9a9a9a;font-size:.62rem}.cc-ic{flex:none;width:20px;height:20px;border:1.5px solid #bdbdbd;border-radius:50%}
.promo-card{position:relative;border-radius:var(--r);overflow:hidden;color:#fff;text-decoration:none;display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;background:#222;isolation:isolate}
.promo-card .ph{position:absolute;inset:0;border-radius:0;aspect-ratio:auto;transition:transform .7s}.promo-card:hover .ph{transform:scale(1.06)}
.promo-card::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.75));z-index:1}
.pc-copy{position:relative;z-index:2}.pc-copy h3{color:#fff;font-size:1.6rem;margin:.6em 0 .3em;line-height:1.05}.pc-copy p{font-size:.9rem;margin:0 0 1.2em}.pc-ic{display:block;width:30px;height:30px;margin:0 auto;border:1.5px solid #fff;border-radius:50%}
.pager{display:flex;gap:16px;align-items:center;justify-content:center;margin:44px 0 18px}.pager a{text-decoration:none;color:var(--ink);font-size:.95rem}
.pager a.on{background:var(--ink);color:var(--bg);width:36px;height:36px;border-radius:50%;display:grid;place-items:center}
.cat-seo{background-color:#171717;background-size:cover;background-position:center;color:#eee;border-radius:20px;margin:30px 20px 0;padding:clamp(60px,9vw,110px) 0}
.cat-seo .wrap{max-width:900px}.cs-ic{display:block;width:34px;height:34px;border:1.5px solid #c9a66b;border-radius:50%;margin-bottom:70px}
.cs-label{display:block;font:500 .75rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.3em;color:#c9a66b;margin-bottom:60px}.cat-seo p{font-size:.95rem;line-height:1.7;max-width:760px;color:#ddd}.note-d{font-size:.78rem!important;color:#888!important}
.trust{padding:34px 0 10px}.trust .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.trust div{display:flex;gap:12px;align-items:flex-start;font-size:.85rem}
.trust b{display:block;font-weight:500;font-size:.95rem;margin-bottom:2px}.trust small{color:var(--mute);font-size:.78rem;line-height:1.3}.tr-ic{flex:none;width:22px;height:22px;border:1.5px solid var(--ink);border-radius:50%}
@media(max-width:1100px){.cc-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:760px){.cc-grid{grid-template-columns:repeat(2,1fr)}.trust .wrap{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.cc-grid{grid-template-columns:1fr}.cat-hero-in{padding-top:110px}}
.t-release .pill,.t-prestige .pill,.t-release .ccard,.t-prestige .ccard{border-radius:0}
.t-release .cat-main,.t-prestige .cat-main{border-radius:0;margin-top:0}.t-release .cat-seo,.t-prestige .cat-seo{border-radius:0;margin:30px 0 0}
.t-release .cat-hero h1{font-weight:400}.t-prestige .cat-hero h1{font-size:clamp(2rem,5vw,3.8rem);letter-spacing:.14em;text-transform:uppercase}
.t-prestige .cat-tabs a{font-family:"Instrument Sans",sans-serif;font-size:.95rem;letter-spacing:.06em;text-transform:uppercase}
.t-prestige .cc-name{font-family:"Instrument Sans",sans-serif;text-transform:uppercase;letter-spacing:.06em;font-size:.82rem}
.cat-intro{max-width:760px;color:var(--mute);margin:0 0 18px;font-size:.95rem}
.cc-tip{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;padding:26px 30px;background:var(--alt);border-radius:var(--r)}
.cc-tip strong{display:block;font-size:1.2rem;margin-bottom:4px}.cc-tip p{margin:0;color:var(--mute);font-size:.9rem}
.hmenu{display:none;background:none;border:0;color:inherit;font-size:1.5rem;cursor:pointer;line-height:1;padding:0}
@media(max-width:980px){.hmenu{display:inline-block}.hdr .nav{display:none}.hdr.nav-open .nav{display:block}.hdr.nav-open{background:#111;color:#fff;position:relative}
.nav>ul{flex-direction:column;gap:0}.nav>ul>li>a{display:block;padding:.85em 0;border-bottom:1px solid rgba(127,127,127,.25)}.hdr-in{padding:14px 18px}}
/* cohesion pass: one container, one header rhythm, readable heroes, the real logo everywhere */
:root{--container:1440px;--gutter:32px}
.wrap,.wrap-w{max-width:var(--container);padding-left:var(--gutter);padding-right:var(--gutter)}
.wrap.narrow{max-width:900px}.hdr-in{max-width:var(--container)}
.ann,.cbar{padding-left:var(--gutter);padding-right:var(--gutter)}
.logo img{height:38px}.ftr .logo img{filter:none;background:#fff;padding:8px 14px;border-radius:8px;height:50px}
.hero-c{max-width:var(--container);margin:0 auto;padding:0 var(--gutter) 8px}
.cat-hero{min-height:300px}
.cat-hero .ph img{filter:blur(2px) brightness(.5) saturate(.9);transform:scale(1.06)}
.cat-hero::after{background:linear-gradient(90deg,rgba(10,10,10,.84),rgba(10,10,10,.58) 60%,rgba(10,10,10,.42))}
.cat-hero-in{padding-top:72px;padding-bottom:46px}.cat-crumbs{margin-bottom:22px;font-size:.82rem}
.cat-hero h1{font-size:clamp(2.2rem,5vw,3.9rem);line-height:1.06;max-width:15em;text-shadow:0 2px 26px rgba(0,0,0,.45)}
.chero,.ghero{padding:clamp(44px,5vw,68px) 0}.chero .wrap,.ghero .wrap{max-width:var(--container)}
.chero h1,.ghero h1{font-size:clamp(2.2rem,5vw,3.9rem);line-height:1.06;letter-spacing:-.03em;margin-bottom:.35em}
.chero p,.ghero p{max-width:660px;margin-bottom:0}.chero .eyebrow,.ghero .eyebrow{margin-bottom:14px}
.crumbs{padding-top:22px;padding-bottom:14px}.sh{margin-bottom:32px}
.t-release .hero-r{padding:96px 20px 84px;min-height:min(78vh,700px)}
@media(max-width:480px){.cat-hero-in{padding-top:48px}:root{--gutter:20px}}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);background:#171717;color:#fff;padding:.8em 1.4em;border-radius:99px;font-size:.9rem;z-index:300;box-shadow:0 8px 24px rgba(0,0,0,.25)}.toast[hidden]{display:none}
.seo-toggle{position:fixed;left:18px;bottom:18px;z-index:250;background:#f5a623;color:#171717;border:0;border-radius:99px;padding:.7em 1.1em;font:700 .8rem system-ui,sans-serif;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25)}
.seo-toggle[aria-pressed=true]{background:#171717;color:#f5a623}
.seo-panel{position:fixed;top:0;right:0;bottom:0;width:min(380px,100vw);background:#111;color:#eee;z-index:240;padding:20px;overflow:auto;font:14px/1.45 system-ui,sans-serif;box-shadow:-12px 0 32px rgba(0,0,0,.35)}.seo-panel[hidden]{display:none}
.sp-head{display:flex;flex-direction:column;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid #333}.sp-head strong{font-size:1.1rem;color:#f5a623}.sp-head span{color:#aaa;font-size:.8rem}
.sp-row{margin-bottom:14px}.sp-row>span{display:block;font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#f5a623;margin-bottom:3px}.sp-row div{word-break:break-word}
.sp-row em{display:block;font-style:normal;font-size:.75rem;margin-top:2px}.sp-row em.ok{color:#6fcf97}.sp-row em.bad{color:#ff8a8a}.sp-row ul{margin:0;padding-left:1.1em}
.sp-chips span{display:inline-block;background:#2a2a2a;border-radius:99px;padding:.15em .7em;margin:0 4px 4px 0;font-size:.78rem;color:#eee}
body.seo-on h1,body.seo-on h2,body.seo-on h3{outline:2px dashed #f5a623;outline-offset:3px;position:relative}
body.seo-on h1::before,body.seo-on h2::before,body.seo-on h3::before{content:attr(data-seo);position:absolute;top:-1.3em;left:0;background:#f5a623;color:#111;font:700 10px system-ui,sans-serif;padding:1px 6px;border-radius:3px;text-transform:none;letter-spacing:0}
@media(max-width:980px){.dual-g{grid-template-columns:1fr}.hdr-in{grid-template-columns:1fr auto;gap:12px}.nav{grid-column:1/-1;order:5}}
"""

CSS_CONCEPT = r"""
:root{--body:Inter,"Helvetica Neue",Arial,sans-serif;--head:Inter,"Helvetica Neue",Arial,sans-serif;--ls:-.03em;--ink:#171717;--bg:#fff;--alt:#f6f6f6;--card:#fff;--line:#e6e6e6;--mute:#6e6e6e;
--accent:#171717;--on-accent:#fff;--dark:#171717;--hdr:#fff;--hdr-ink:#171717;--hdr-bd:0;--r:12px;--btt:none;--ntt:none;--ph1:#f4f4f4;--ph2:#e9e9e9;--ph-ink:#171717}
body.t-concept{line-height:1.35}
.t-concept h1,.t-concept h2{font-weight:700;line-height:1}.t-concept h2{font-size:clamp(1.8rem,3vw,2.5rem)}
.t-concept .btn{border-radius:999px;border-width:2px;font-weight:500;padding:.9em 1.7em}
.t-concept .btn-o{border-color:#171717}.t-concept .btn-w{background:#fff;color:#171717;border-color:#fff}
.t-concept .eyebrow{font-weight:500;letter-spacing:0;text-transform:none;font-size:.9rem;color:var(--mute)}
.t-concept .ann{background:#171717;color:#fff;font-size:.8rem}
.t-concept .hdr-in{padding:22px 32px}.t-concept .nav>ul{justify-content:center;gap:22px}
.t-concept .nav>ul>li>a{font-size:.92rem;font-weight:500;text-transform:none;letter-spacing:0}
.t-concept .logo-a{font-weight:700;letter-spacing:-.03em;font-size:1.7rem}.t-concept .logo-d{letter-spacing:.28em;font-size:.58rem}
.t-concept .cart span{background:#171717;color:#fff}
.hero-c{padding:0 20px 8px}.hero-c .slide{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:16/7;min-height:380px;background:#1b2430}
.ph-hero{position:absolute;inset:0;aspect-ratio:auto;border-radius:0;--ph1:#4a5a70;--ph2:#161d28;--ph-ink:#fff}.ph-hero .ph-ic{width:22%;opacity:.25}
.slide-copy{position:absolute;left:clamp(24px,4vw,56px);bottom:clamp(40px,7vw,80px);max-width:620px;color:#fff;z-index:2}
.slide-copy h1{font-size:clamp(1.8rem,3.4vw,2.7rem);text-transform:uppercase;margin:0}
.hero-c .btn-w{position:absolute;right:clamp(24px,4vw,56px);bottom:clamp(36px,6vw,70px);z-index:2}
.dots{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);display:flex;gap:8px;z-index:2}
.dots i{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.5)}.dots i.on{background:#fff}
.hero-c .slide::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.6));z-index:1}
.t-concept .intro{padding:clamp(60px,9vw,120px) 0}.t-concept .intro h2{font-size:clamp(2rem,4.2vw,3.2rem);max-width:760px;margin-left:auto;margin-right:auto}
.t-concept .intro p{color:var(--mute);max-width:560px;margin:0 auto 1.6em}
.t-concept .sh{align-items:center}.t-concept .more{border:2px solid #171717;border-radius:999px;color:#171717;padding:.5em 1.2em;font-weight:500}
.t-concept .ctile .ph{border-radius:12px;aspect-ratio:1/1}.t-concept .ct-name{font-weight:500;font-size:1.15rem;text-transform:none;letter-spacing:-.01em}.t-concept .ct-go{display:none}
.t-concept .pcard{border:0;background:transparent;border-radius:0}.t-concept .pimg .ph{border-radius:12px;aspect-ratio:1/1}
.t-concept .pbody{padding:12px 0 0}.t-concept .pbody .btn,.t-concept .instock{display:none}
.t-concept .pbody h3{font-weight:500;font-size:1.05rem}.t-concept .price{font-weight:500;font-size:1.05rem}
.t-concept .badge{background:#171717;font-weight:500;text-transform:none;letter-spacing:0;font-size:.74rem}
.t-concept .itile{border:1px solid #171717;border-radius:12px;background:#fff}.t-concept .itile:hover{background:#171717;color:#fff}
.t-concept .itile:hover .it-g{color:#fff}.t-concept .it-g{color:#171717}
.t-concept .gband{background:#f6f6f6;color:#171717;border-radius:16px;margin:24px 20px;padding:clamp(32px,5vw,64px) 0}
.t-concept .news{background:#171717;color:#fff}.t-concept .news .btn{background:#fff;color:#171717;border-color:#fff}.t-concept .ftr{background:#171717}
.t-concept .rev{border:0;background:#f6f6f6}.t-concept .faq summary{font-weight:700}
.t-concept .b-panel,.t-concept .b-sum{border-radius:16px;background:#fff}.t-concept .b-opts button{border-radius:12px}.t-concept .b-steps button{border-radius:999px}
.t-concept .chero,.t-concept .ghero{background:#f6f6f6}.t-concept .srow strong{color:#171717}
.t-concept .nav>ul{gap:4px}.t-concept .nav>ul>li>a{padding:.62em 1.2em;border-radius:999px;transition:background .2s,color .2s}
.t-concept .nav>ul>li>a:hover,.t-concept .has-mega:hover>a{background:#171717;color:#fff}
.t-concept .mega{background:#fff;box-shadow:0 24px 40px rgba(0,0,0,.12)}
.t-concept .btn{transition:background .2s,color .2s,border-color .2s,transform .15s}
.t-concept .btn:hover{background:#fff;color:#171717;border-color:#171717;filter:none}
.t-concept .btn-o:hover{background:#171717;color:#fff}.t-concept .btn-w:hover{background:#171717;color:#fff;border-color:#171717}
.t-concept .btn:active{transform:scale(.97)}.t-concept .news .btn:hover{background:transparent;color:#fff;border-color:#fff}
.t-concept .more{transition:background .2s,color .2s}.t-concept .more:hover{background:#171717;color:#fff}
.hero-c .slides{position:relative;width:100%;border-radius:16px;overflow:hidden;height:clamp(400px,44vw,640px);background:#171717}
@media(max-width:560px){.slide-copy h1{font-size:1.5rem}.hero-c .btn-w{left:24px;right:auto;bottom:84px}.slide-copy{bottom:150px}}
.hero-c .slide{position:absolute;inset:0;opacity:0;transition:opacity .7s ease;pointer-events:none;aspect-ratio:auto;min-height:0;border-radius:0;background:none}
.hero-c .slide.on{opacity:1;pointer-events:auto}.hero-c .slide .ph{position:absolute;inset:0;border-radius:0;aspect-ratio:auto}
.hero-c .slide .ph img{object-position:center}
.s-arr{position:absolute;bottom:22px;z-index:3;width:44px;height:44px;border-radius:50%;border:2px solid rgba(255,255,255,.75);background:transparent;color:#fff;font-size:1.2rem;cursor:pointer;transition:background .2s,color .2s}
.s-arr:hover{background:#fff;color:#171717}.s-arr[data-prev]{left:24px}.s-arr[data-next]{right:24px}
.hero-c .dots{display:flex;gap:8px;align-items:center}.dot{width:8px;height:8px;border-radius:99px;border:0;background:rgba(255,255,255,.5);padding:0;cursor:pointer;transition:width .3s,background .3s}
.dot.on{background:#fff;width:24px}
.t-concept .qadd{display:block;position:absolute;left:12px;right:12px;bottom:12px;padding:.75em;border-radius:999px;border:0;background:#fff;color:#171717;font:500 .86rem Inter,sans-serif;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.14);opacity:0;transform:translateY(8px);transition:opacity .25s,transform .25s,background .2s,color .2s}
.t-concept .pcard:hover .qadd,.t-concept .qadd:focus-visible{opacity:1;transform:none}.t-concept .qadd:hover{background:#171717;color:#fff}
.t-concept .pimg .ph img{transition:transform .5s}.t-concept .pcard:hover .pimg .ph img{transform:scale(1.04)}
.t-concept .ctile{transition:transform .25s}.t-concept .ctile:hover{transform:translateY(-4px)}.t-concept .ctile .ph{transition:box-shadow .25s}.t-concept .ctile:hover .ph{box-shadow:0 14px 28px rgba(0,0,0,.1)}
.t-concept .ct-go{display:inline-block;opacity:0;transform:translateX(-6px);transition:opacity .25s,transform .25s}.t-concept .ctile:hover .ct-go{opacity:1;transform:none}
.t-concept .ic-copy h3{letter-spacing:-.03em}.t-concept .ind-head h2{font-size:clamp(2rem,3.4vw,2.8rem)}
.t-concept .ph-img{background:#fafafa}
.t-concept .icard .ph-img,.t-concept .mcard.dark .ph-img{background:#222}
"""

CSS_RELEASE = r"""
:root{--body:Poppins,"Helvetica Neue",Arial,sans-serif;--head:Poppins,"Helvetica Neue",Arial,sans-serif;--ls:-.04em;--ink:#111;--bg:#fff;--alt:#f4f4f4;--card:#fff;--line:#e4e4e4;--mute:#707070;
--accent:#111;--on-accent:#fff;--dark:#0d0d0d;--hdr:#fff;--hdr-ink:#111;--hdr-bd:0;--r:0px;--btt:uppercase;--ntt:uppercase;--ph1:#efefef;--ph2:#e2e2e2;--ph-ink:#111}
.t-release h1,.t-release h2{font-weight:400;line-height:1.05}.t-release h2{font-size:clamp(2rem,4vw,2.9rem)}
.t-release .btn{border-radius:0;font-size:.72rem;letter-spacing:.14em;font-weight:500;padding:1.05em 2.2em}
.t-release .btn-ow{background:transparent;color:#fff;border-color:#fff}
.t-release .eyebrow{color:inherit;opacity:.7;font-size:.66rem;letter-spacing:.24em;font-weight:500}
.t-release .ann{background:#0d0d0d;color:#fff;text-transform:uppercase;font-size:.62rem;letter-spacing:.1em;font-weight:600;justify-content:space-around}
.t-release .hdr-in{grid-template-columns:1fr auto 1fr;padding:22px 32px}.t-release .nav{justify-self:start}.t-release .hicons{justify-self:end}
.t-release .nav>ul{gap:20px}.t-release .nav>ul>li>a{font-size:.66rem;letter-spacing:.1em;font-weight:500}
.t-release .logo{align-items:center}.t-release .logo-a{font-size:2rem;font-weight:300;letter-spacing:-.04em;text-transform:lowercase}.t-release .logo-d{display:none}
.t-release .cart span{background:#111;color:#fff}
.t-release .hdr-over{background:transparent;color:#fff;position:absolute;top:auto;left:0;right:0;z-index:20}
.t-release .hdr-over .cart span{background:#fff;color:#111}
.hero-r{min-height:min(88vh,820px);display:flex;align-items:flex-end;justify-content:center;text-align:center;color:#fff;
background:radial-gradient(ellipse at 50% 30%,#4a3f36 0%,#1d1815 45%,#0c0b0a 100%);padding:140px 20px 90px}
.hero-r h1{font-size:clamp(2.6rem,6vw,4.4rem);color:#fff;margin:.2em 0 .7em}
.t-release .pcard{border:0;background:transparent}.t-release .pimg .ph{aspect-ratio:4/5}.t-release .pbody{padding:12px 0 0}
.t-release .pbody .btn,.t-release .instock{display:none}.t-release .pbody h3{font-weight:400;font-size:.85rem;letter-spacing:-.01em}.t-release .price{font-size:.85rem;font-weight:500}
.t-release .badge{background:#111;border-radius:0;font-weight:500;font-size:.62rem}
.t-release .ctile .ph{aspect-ratio:4/5}.t-release .ct-name{font-weight:400;font-size:1rem;letter-spacing:-.02em;text-transform:none}.t-release .ct-go{display:none}
.t-release .sh{align-items:center}.t-release .more{color:#111;border-bottom:1px solid #111;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase}
.t-release .dtile .ph{aspect-ratio:3/2}.t-release .dt-copy{inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.t-release .dt-copy h2{color:#fff}.t-release .banner{min-height:560px}.t-release .banner h2{font-size:clamp(2.4rem,5vw,3.8rem);color:#fff}
.t-release .callout h2{font-size:clamp(2.4rem,5vw,3.8rem)}.t-release .callout p{color:var(--mute)}
.t-release .itile{background:#fff;border:0;border-bottom:1px solid #111;padding:22px 4px}.t-release .it-n{font-weight:400}
.t-release .rev{border:0;background:#f4f4f4}.t-release .news{background:#111;color:#fff}.t-release .news .btn{background:#fff;color:#111;border-color:#fff}
.t-release .ftr{background:#0d0d0d}.t-release .gband{background:#0d0d0d}.t-release .chero,.t-release .ghero{background:#f4f4f4}
.t-release .b-panel,.t-release .b-sum{background:#fff}.t-release .srow strong{color:#111;font-weight:400}
.t-release .icard{border-radius:0;aspect-ratio:4/5}.t-release .ic-plus{border-radius:0}.t-release .ic-copy h3{font-weight:400;letter-spacing:-.02em}
.t-release .ind-head h2{font-weight:400}
"""

CSS_PRESTIGE = r"""
:root{--body:Nunito,"Helvetica Neue",Arial,sans-serif;--head:"Instrument Sans","Helvetica Neue",Arial,sans-serif;--ls:.18em;--ink:#1c1c1c;--bg:#efefef;--alt:#e6e6e6;--card:#f8f8f8;--line:#d6d6d6;--mute:#6a6a6a;
--accent:#1c1c1c;--on-accent:#efefef;--dark:#1c1c1c;--hdr:#efefef;--hdr-ink:#1c1c1c;--hdr-bd:1px solid #dcdcdc;--r:0;--btt:none;--ntt:uppercase;--ph1:#e4e4e4;--ph2:#d2d2d2;--ph-ink:#1c1c1c}
.t-prestige h1,.t-prestige h2,.t-prestige h3{font-weight:400;text-transform:uppercase}
.t-prestige h2{font-size:clamp(1.2rem,2vw,1.6rem);letter-spacing:.18em;line-height:1.3}.t-prestige h3{font-size:.85rem;letter-spacing:.1em}
.t-prestige .btn{border-radius:0;border-width:1px;font-weight:400;font-size:.85rem;letter-spacing:.05em;padding:1.05em 2.2em}
.t-prestige .btn-lt{background:#efefef;color:#1c1c1c;border-color:#efefef}.t-prestige .btn-ow{background:transparent;color:#fff;border-color:#fff}
.t-prestige .eyebrow{font-family:"Instrument Sans",sans-serif;font-weight:400;letter-spacing:.22em;font-size:.68rem;color:var(--mute)}
.t-prestige .ann{background:#1c1c1c;color:#efefef;font-family:"Instrument Sans",sans-serif;text-transform:uppercase;letter-spacing:.12em;font-size:.68rem;justify-content:flex-start}
.t-prestige .ann a{text-decoration:underline}
.t-prestige .hdr-in{grid-template-columns:1fr auto 1fr;padding:18px 32px}.t-prestige .nav{justify-self:start}.t-prestige .hicons{justify-self:end}
.t-prestige .nav>ul{gap:22px}.t-prestige .nav>ul>li>a{font-family:"Instrument Sans",sans-serif;font-size:.72rem;letter-spacing:.12em;font-weight:400}
.t-prestige .logo{align-items:center}.t-prestige .logo-a{font-family:"Instrument Sans",sans-serif;font-weight:400;font-size:1.5rem;letter-spacing:.34em;margin-right:-.34em}
.t-prestige .logo-d{font-size:.52rem;letter-spacing:.5em;margin-right:-.5em}.t-prestige .cart span{background:#1c1c1c;color:#efefef}
.hero-p{min-height:min(88vh,768px);display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;
background:radial-gradient(ellipse at 50% 35%,#3a3a3a 0%,#161616 60%,#0b0b0b 100%);padding:100px 20px}
.hero-p h1{font-size:clamp(1.6rem,3.6vw,2.6rem);letter-spacing:.2em;margin:0 0 1.4em;line-height:1.3}
.t-prestige .sec{padding:clamp(56px,8vw,100px) 0}.t-prestige .sh{justify-content:center;text-align:center}
.t-prestige .more{color:#1c1c1c;text-decoration:underline;font-family:"Instrument Sans",sans-serif;font-weight:400;letter-spacing:.08em}
.t-prestige .pcard{border:0;background:transparent}.t-prestige .pimg .ph{aspect-ratio:3/4}.t-prestige .pbody{padding:14px 0 0;text-align:center}
.t-prestige .pbody .btn,.t-prestige .instock,.t-prestige .sws{display:none}.t-prestige .prow{justify-content:center}
.t-prestige .price{font-family:"Instrument Sans",sans-serif;font-size:.85rem;font-weight:400}.t-prestige .pdim{display:none}
.t-prestige .badge{background:#1c1c1c;border-radius:0;font-weight:400;letter-spacing:.14em}
.t-prestige .ctile .ph{aspect-ratio:3/4}.t-prestige .ct-name{font-family:"Instrument Sans",sans-serif;font-weight:400;font-size:.9rem;letter-spacing:.18em;text-align:center}
.t-prestige .ct-go{display:none}.t-prestige .itile{background:transparent;border:0;border-bottom:1px solid #1c1c1c}.t-prestige .it-n{font-weight:400;letter-spacing:.1em;text-transform:uppercase;font-size:.9rem}
.t-prestige .banner{min-height:480px;background:linear-gradient(135deg,#3a3a3a,#141414)}.t-prestige .banner h2{color:#fff}
.t-prestige .rev{border:0;background:#f8f8f8}.t-prestige .news{background:#1c1c1c;color:#efefef}.t-prestige .news .btn{background:#efefef;color:#1c1c1c;border-color:#efefef}
.t-prestige .ftr{background:#1c1c1c}.t-prestige .gband{background:#1c1c1c}.t-prestige .chero,.t-prestige .ghero{background:#e6e6e6}
.t-prestige .faq summary{font-family:"Instrument Sans",sans-serif;font-weight:400;letter-spacing:.08em;text-transform:uppercase;font-size:.9rem}
.t-prestige .srow strong{color:#1c1c1c;font-weight:400}.t-prestige .pimg{display:block}
.t-prestige .icard{border-radius:0}.t-prestige .ic-plus{border-radius:0}
.t-prestige .ic-copy h3{font-family:"Instrument Sans",sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.14em;font-size:1rem}
"""


# ----------------------------------------------------------------------------
# Shared JS
# ----------------------------------------------------------------------------
APP_JS = r"""
(function(){
'use strict';
var money=function(n){return '$'+Math.round(n).toLocaleString('en-US');};
/* Gondola builder (SAMPLE pricing, concept only). Option lists mirror the live Gondola Shelving page. */
var b=document.querySelector('[data-builder]');
if(b){
  var steps=[
    {k:'store',l:'Store type',q:'What kind of store is it?',o:[['Supermarket','Long runs'],['Liquor store','Heavy loads'],['Pharmacy','Mixed goods'],['Apparel store','Light merchandise'],['Other','Tell us more']]},
    {k:'unit',l:'Unit type',q:'Which unit type?',o:[['Single sided','Against a wall',1],['Double sided','Freestanding aisle',1.7],['Wall unit','Wall run',0.9],['End unit','Ends a run',1.1]]},
    {k:'len',l:'Length',q:'How long is each section?',o:[['30 in','Compact',0.9],['36 in','Standard',1],['48 in','Wide',1.3]]},
    {k:'h',l:'Height',q:'How tall?',o:[['48 in','',1],['54 in','',1.05],['60 in','',1.12],['72 in','Most popular',1.3],['84 in','',1.5],['96 in','Max display',1.7]]},
    {k:'fin',l:'Finish',q:'Choose a finish',o:[['Black','Powder coat'],['Antique white','Powder coat']]},
    {k:'secs',l:'Sections',q:'How many sections?',o:[['2 sections','',2],['4 sections','',4],['6 sections','',6],['8 sections','',8]]},
    {k:'acc',l:'Add-ons',q:'Add anything?',multi:true,o:[['Upper shelves','$25 per section',25],['End units','$236 for a pair',236],['Accessories','$12 per section',12]]}
  ];
  var st={},i=0,qs=function(s){return b.querySelector(s)};
  var stepsEl=qs('[data-steps]'),q=qs('[data-q]'),opts=qs('[data-opts]'),sum=qs('[data-sum]'),total=qs('[data-total]');
  function calc(){
    var secs=(st.secs&&st.secs[2])||0,u=(st.unit&&st.unit[2])||1,l=(st.len&&st.len[2])||1,h=(st.h&&st.h[2])||1;
    var t=secs*107*u*l*h;
    (st.acc||[]).forEach(function(a){t+=a[0]==='End units'?a[2]:a[2]*secs});
    return t;
  }
  function render(){
    stepsEl.innerHTML='';
    steps.forEach(function(s,n){var x=document.createElement('button');x.type='button';x.textContent=(n+1)+'. '+s.l;
      x.className=(n===i?'on ':'')+(st[s.k]&&(!s.multi||st[s.k].length)?'done':'');x.onclick=function(){i=n;render()};stepsEl.appendChild(x)});
    var s=steps[i];q.textContent=s.q;opts.innerHTML='';
    s.o.forEach(function(o){var x=document.createElement('button');x.type='button';x.innerHTML=o[0]+(o[1]?'<small>'+o[1]+'</small>':'');
      var cur=st[s.k];var sel=s.multi?(cur||[]).some(function(c){return c[0]===o[0]}):(cur&&cur[0]===o[0]);if(sel)x.className='sel';
      x.onclick=function(){if(s.multi){var a=st[s.k]||[];var ix=a.findIndex(function(c){return c[0]===o[0]});if(ix>-1)a.splice(ix,1);else a.push(o);st[s.k]=a}else{st[s.k]=o}render()};opts.appendChild(x)});
    sum.innerHTML='';
    steps.forEach(function(s){var v=st[s.k];if(!v||(s.multi&&!v.length))return;var li=document.createElement('li');li.innerHTML='<span>'+s.l+'</span><strong>'+(s.multi?v.map(function(c){return c[0]}).join(', '):v[0])+'</strong>';sum.appendChild(li)});
    total.textContent=money(calc());
    qs('[data-back]').disabled=i===0;qs('[data-next]').textContent=i===steps.length-1?'Finish':'Next';
  }
  qs('[data-back]').onclick=function(){if(i>0){i--;render()}};
  qs('[data-next]').onclick=function(){if(i<steps.length-1){i++;render()}else{qs('[data-cta]').focus()}};
  render();
}

/* Collection filters and sort */
var fl=document.querySelector('[data-filters]');
if(fl){
  var gridWrap=document.querySelector('[data-grid]'),cards=[].slice.call(gridWrap.querySelectorAll('.pcard')),cnt=document.querySelector('[data-count]'),emp=document.querySelector('[data-empty]'),sel=document.querySelector('[data-sort]');
  var gridEl=gridWrap.querySelector('.pgrid');
  function apply(){
    var kinds=[].slice.call(fl.querySelectorAll('[data-f=kind]:checked')).map(function(x){return x.value});
    var fins=[].slice.call(fl.querySelectorAll('[data-f=fin]:checked')).map(function(x){return x.value});
    var pr=fl.querySelector('[data-f=price]:checked');pr=pr&&pr.value?pr.value.split('-').map(Number):null;
    var shown=0;
    cards.forEach(function(c){var ok=true;
      if(kinds.length&&kinds.indexOf(c.dataset.kind)<0)ok=false;
      if(fins.length&&!fins.some(function(f){return (' '+c.dataset.fin+' ').indexOf(' '+f+' ')>-1}))ok=false;
      var p=+c.dataset.price;if(pr&&(p<pr[0]||p>=pr[1]))ok=false;
      c.hidden=!ok;if(ok)shown++});
    cnt.textContent=shown+' product'+(shown===1?'':'s');emp.hidden=shown>0;
    var s=sel.value,list=cards.slice();
    if(s==='lo')list.sort(function(a,b){return a.dataset.price-b.dataset.price});
    if(s==='hi')list.sort(function(a,b){return b.dataset.price-a.dataset.price});
    if(s==='new')list.sort(function(a,b){return b.dataset.new-a.dataset.new});
    list.forEach(function(c){gridEl.appendChild(c)});var pr=gridEl.querySelector('.promo-card');var vis=[].filter.call(gridEl.querySelectorAll('.pcard'),function(c){return !c.hidden});if(pr){gridEl.insertBefore(pr,vis[7]||null)}var tp=gridEl.querySelector('.cc-tip');if(tp){gridEl.insertBefore(tp,vis[7]||null)}
  }
  fl.addEventListener('change',apply);sel.addEventListener('change',apply);
  document.querySelector('[data-clear]').onclick=function(){[].forEach.call(fl.querySelectorAll('input'),function(x){x.checked=x.dataset.f==='price'&&x.value===''});apply()};
}
/* Modals: shipping estimate, bulk pricing, newsletter popup (SAMPLE rates and offer) */
var openM=function(id){var m=document.getElementById('m-'+id);if(m){m.hidden=false;var f=m.querySelector('input');if(f)f.focus()}};
var closeM=function(){[].forEach.call(document.querySelectorAll('.modal'),function(m){m.hidden=true})};
document.addEventListener('click',function(e){var t=e.target.closest('[data-modal]');if(t){e.preventDefault();closeM();openM(t.dataset.modal);return}
  if(e.target.closest('[data-close]')||e.target.classList.contains('modal'))closeM()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeM()});
var shipF=document.querySelector('[data-ship]');
if(shipF){shipF.addEventListener('submit',function(e){e.preventDefault();
  var z=shipF.querySelector('input').value.trim(),lb=+shipF.querySelector('input[type=number]').value||1,out=document.querySelector('[data-ship-out]');out.hidden=false;
  if(!/^\d{5}$/.test(z)){out.textContent='Enter a 5-digit ZIP code.';return}
  var n=+z.slice(0,3),d=+z[0];
  if((n>=967&&n<=968)||(n>=995&&n<=999)){out.textContent='Sample rule: this concept does not ship to Alaska or Hawaii.';return}
  var reg=d<=3?'East':d<=7?'Central':'West',f=reg==='East'?1:reg==='Central'?1.25:1.6,ltl=lb>=150;
  var est=ltl?Math.round((120+0.9*lb)*f):Math.round((14+0.28*lb)*f);
  out.innerHTML='<strong>'+reg+' zone, '+(ltl?'LTL freight':'Ground')+'</strong><br>Estimated shipping: '+money(est)+' <small>(SAMPLE rate)</small><br>'+(ltl?'LTL orders ship the next day.':'Order by 2 pm ET and Ground orders ship the same day.')})}
[].forEach.call(document.querySelectorAll('.modal form:not([data-ship])'),function(f){f.addEventListener('submit',function(e){e.preventDefault();var b=f.querySelector('button');b.textContent='Thanks (demo)';b.disabled=true})});
if(document.querySelector('.hero-c,.hero-r,.hero-p')){try{if(!sessionStorage.getItem('sd-pop')){setTimeout(function(){if(!document.querySelector('.modal:not([hidden])')){openM('pop');sessionStorage.setItem('sd-pop','1')}},6000)}}catch(e){}}
/* Appointment booking (SAMPLE availability, demo only) */
var bk=document.querySelector('[data-book]');
if(bk){
  var type='Free layout call',day=null,time=null,days=[],dt=new Date();
  while(days.length<7){dt.setDate(dt.getDate()+1);if(dt.getDay()%6)days.push(new Date(dt))}
  var times=['9:00 AM','10:30 AM','12:00 PM','1:30 PM','3:00 PM','4:30 PM'];
  var fmt=function(x){return x.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})};
  var bout=bk.querySelector('[data-bk-out]');
  var draw=function(){
    var t=bk.querySelector('[data-bk-types]'),dd=bk.querySelector('[data-bk-days]'),tt=bk.querySelector('[data-bk-times]');
    var mk=function(host,label,on,fn){var b=document.createElement('button');b.type='button';b.textContent=label;if(on)b.className='bk-sel';b.onclick=fn;host.appendChild(b)};
    t.innerHTML='';dd.innerHTML='';tt.innerHTML='';
    ['Free layout call','Showroom visit'].forEach(function(x){mk(t,x,x===type,function(){type=x;draw()})});
    days.forEach(function(x,i){mk(dd,fmt(x),day===i,function(){day=i;draw()})});
    times.forEach(function(x){mk(tt,x+' ET',time===x,function(){time=x;draw()})});
    bout.hidden=!(day!==null&&time);
    if(!bout.hidden)bout.innerHTML='<strong>'+type+'</strong><br>'+fmt(days[day])+' at '+time+' ET (SAMPLE availability, demo only)';
  };
  draw();
}
/* Hero slider (Concept) */
var sl=document.querySelector('[data-slider]');
if(sl){var slides=[].slice.call(sl.querySelectorAll('.slide')),dots=[].slice.call(sl.querySelectorAll('.dot')),cur=0,timer=null;
  var go=function(n){cur=(n+slides.length)%slides.length;slides.forEach(function(s,i){s.classList.toggle('on',i===cur)});dots.forEach(function(d,i){d.classList.toggle('on',i===cur)})};
  var stop=function(){clearInterval(timer)},play=function(){stop();timer=setInterval(function(){go(cur+1)},6000)};
  sl.querySelector('[data-prev]').onclick=function(){go(cur-1);play()};sl.querySelector('[data-next]').onclick=function(){go(cur+1);play()};
  dots.forEach(function(d,i){d.onclick=function(){go(i);play()}});sl.addEventListener('mouseenter',stop);sl.addEventListener('mouseleave',play);play();}
/* Toast and quick add */
var toastEl=document.querySelector('[data-toast]');
var toast=function(t){if(!toastEl)return;toastEl.textContent=t;toastEl.hidden=false;clearTimeout(toastEl._t);toastEl._t=setTimeout(function(){toastEl.hidden=true},2200)};
document.addEventListener('click',function(e){var q=e.target.closest('[data-qadd]');if(q){e.preventDefault();var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+1;toast('Added to cart (demo)')}});
/* SEO view panel */
var seoBtn=document.querySelector('[data-seo-toggle]'),seoPanel=document.querySelector('[data-seo-panel]');
if(seoBtn&&seoPanel){
  var sd={};try{sd=JSON.parse(document.getElementById('seo-data').textContent)}catch(e){}
  var metaEl=document.querySelector('meta[name=description]'),h1El=document.querySelector('h1');
  var il=0,el=0;[].forEach.call(document.querySelectorAll('main a[href]'),function(a){var h=a.getAttribute('href');if(a.hasAttribute('data-modal')||h==='#')return;if(/^https?:/.test(h))el++;else il++});
  var imgs=document.querySelectorAll('main img'),noAlt=[].filter.call(imgs,function(i){return !i.alt}).length;
  var chip=function(a){return '<div class="sp-chips">'+(a||[]).map(function(x){return '<span>'+x+'</span>'}).join('')+'</div>'};
  var lenNote=function(s,max){return '<em class="'+(s.length>max?'bad':'ok')+'">'+s.length+' characters (aim for '+max+' or fewer)</em>'};
  var row=function(l,v,e){return '<div class="sp-row"><span>'+l+'</span><div>'+v+'</div>'+(e||'')+'</div>'};
  var ttl=document.title,mt=metaEl?metaEl.content:'';
  seoPanel.querySelector('[data-seo-body]').innerHTML=
    row('Title tag',ttl,lenNote(ttl,60))+row('Meta description',mt,lenNote(mt,155))+row('H1',h1El?h1El.textContent:'')+row('Suggested live URL',sd.path||'')+
    row('Primary keyword',sd.kw||'')+row('Secondary keywords',chip(sd.sec))+row('Schema',chip(sd.schema))+
    row('Links in main content',il+' internal, '+el+' external')+row('Images',imgs.length+' ('+noAlt+' missing alt text)')+
    row('Strategy notes','<ul>'+(sd.notes||[]).map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul>');
  seoBtn.onclick=function(){var on=seoPanel.hidden;seoPanel.hidden=!on;document.body.classList.toggle('seo-on',on);seoBtn.setAttribute('aria-pressed',on?'true':'false');seoBtn.textContent=on?'Hide SEO view':'SEO view';
    [].forEach.call(document.querySelectorAll('h1,h2,h3'),function(h){h.setAttribute('data-seo',h.tagName)})};
}
var ft=document.querySelector('[data-filter-toggle]'),fp=document.querySelector('[data-filters]');
if(ft&&fp){ft.onclick=function(){fp.hidden=!fp.hidden;ft.setAttribute('aria-expanded',fp.hidden?'false':'true');ft.querySelector('span').textContent=fp.hidden?'Show filters':'Hide filters'}}
var hm=document.querySelector('[data-hmenu]');
if(hm){hm.onclick=function(){var h=hm.closest('.hdr');var on=!h.classList.contains('nav-open');h.classList.toggle('nav-open',on);hm.setAttribute('aria-expanded',on?'true':'false')}}
/* Product page */
var pp=document.querySelector('[data-price]'),qty=document.querySelector('[data-qty]');
if(pp&&qty){
  var unit=parseFloat(pp.dataset.base)||0;
  function up(){var add=0;[].forEach.call(document.querySelectorAll('[data-opt]:checked'),function(r){add+=+r.dataset.add||0});pp.textContent=money((unit+add)*(+qty.value||1))}
  qty.addEventListener('input',up);document.addEventListener('change',up);
  var add=document.querySelector('[data-add]');if(add)add.onclick=function(){var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+(+qty.value||1);add.textContent='Added (demo)';toast('Added to cart (demo)')};
}
})();

"""

OVERVIEW = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Store Displays&reg; Vision Demos | SmartSites concept</title>
<style>
:root{--bg:#f6f7f9;--ink:#141a24;--mute:#586174;--card:#fff;--line:#dde2ea;--accent:#1d4ed8}
@media(prefers-color-scheme:dark){:root{--bg:#10141c;--ink:#eef1f6;--mute:#a4adbd;--card:#171c27;--line:#2a3140;--accent:#7aa2ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Segoe UI",Arial,sans-serif}
.w{max-width:1100px;margin:0 auto;padding:36px 20px}h1{font-size:clamp(1.8rem,4vw,2.6rem);margin:0 0 8px}
.lead{color:var(--mute);max-width:760px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:28px 0}
.c{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px;display:flex;flex-direction:column;gap:8px}
.c h2{margin:0;font-size:1.3rem}.c p{margin:0;color:var(--mute);font-size:.92rem}.c a.b{margin-top:auto;display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:.65em 1.1em;border-radius:8px;font-weight:700;text-align:center}
.pg{display:flex;flex-wrap:wrap;gap:8px 14px;font-size:.88rem}.pg a{color:var(--accent)}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:.9rem}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:rgba(127,127,127,.08)}
.warn{background:rgba(255,170,0,.14);border:1px solid rgba(255,170,0,.5);padding:14px 16px;border-radius:10px;margin:22px 0;font-size:.92rem}
@media(max-width:800px){.cards{grid-template-columns:1fr}}
</style></head><body><div class="w">
<h1>Store Displays&reg;: three visual concepts</h1>
<p class="lead">Static mockups for the redesign discussion, built from the SmartSites x Store Display kickoff call (13 Nov 2026) and the live storedisplays.com. Each concept uses the same content, drawn from the live storedisplays.com (real products, SKUs, prices, links and images) plus clearly marked samples, so the client compares layout and feel, not copy.</p>
<div class="warn"><strong>Read this first.</strong> These are not the real Shopify themes and not a build. They are HTML/CSS mockups modeled on each theme's public demo store (typography, colours, header, hero and section order), without the theme's code or photography. Product names, SKUs, listing prices, links and images come from the live site; the images are saved here at full resolution. Reviews, most copy, the industry pages and the gondola builder are SAMPLE or CONCEPT. The real build happens in Shopify once the client store exists.</div>
<div class="cards">
@@CARDS@@
</div>
<h2>How each concept answers the kickoff</h2>
<table><tr><th>Client wish</th><th>Concept</th><th>Release</th><th>Prestige</th></tr>
<tr><td>Modern look like Displayarama</td><td>Light and airy: Inter type, pill buttons, rounded photo slideshow</td><td>Editorial: transparent header over a full-bleed hero, light Poppins headlines</td><td>Quiet and architectural: spaced uppercase headings, square buttons</td></tr>
<tr><td>Prices and details on the page, no quote form</td><td>Price on every card and product page</td><td>Same</td><td>Same</td></tr>
<tr><td>Gondola configurator</td><td>Step builder mock, like the theme's bundle builder</td><td>Same mock</td><td>Same mock</td></tr>
<tr><td>Shop by industry, free store layouts</td><td>Industry tiles and layout request form</td><td>Same</td><td>Same, list style</td></tr>
<tr><td>New and trending products</td><td>Grid on home</td><td>Grid on home</td><td>Grid on home</td></tr>
<tr><td>Palay-style detail and information</td><td>Spec table, accordions</td><td>Featured, Specials and New Arrivals pattern</td><td>Spec table, accordions</td></tr>
<tr><td>Colors variants, not 360 categories</td><td>Swatch filters and finish selector</td><td>Same</td><td>Same</td></tr>
<tr><td>Free store layouts and appointment scheduling</td><td>Dedicated page with a booking widget</td><td>Same</td><td>Same</td></tr>
<tr><td>Calculate shipping (regional zones)</td><td>ZIP-based zone estimate, sample rates</td><td>Same</td><td>Same</td></tr>
<tr><td>Bulk and volume pricing</td><td>Request form, plus the live volume pricing page</td><td>Same</td><td>Same</td></tr>
<tr><td>Shop by industry pages</td><td>8 concept industry pages with recommended products</td><td>Same</td><td>Same</td></tr>
<tr><td>10% newsletter capture</td><td>Popup and a footer band</td><td>Same</td><td>Same</td></tr>
<tr><td>SEO strategy visible to the client</td><td>SEO view panel on every page: title, description, H1, keywords, schema, links</td><td>Same</td><td>Same</td></tr>
<tr><td>Shop by industry like the theme</td><td>Tall photo cards with a plus that opens, plus card-style mega menus</td><td>Square photo cards</td><td>Square cards, spaced caps</td></tr>
<tr><td>Interactive feel</td><td>Rotating hero, pill nav, quick add, hover reveals</td><td>Hover reveals on cards</td><td>Hover reveals on cards</td></tr>
<tr><td>Category pages like the Concept collection template</td><td>21 category pages: hero with title, sub-category tabs, filters, sort, real products, promo card, text block</td><td>Same structure, Release styling</td><td>Same structure, Prestige styling</td></tr>
</table>
<p class="lead" style="margin-top:22px">Still to do for the real build: confirm the 5 non-ecommerce pages and industry list from the workbook, the client's new logo and colors, a real configurator (app or custom code), a real booking tool for appointments, quantity pricing (marked Plus on the theme pages, needs checking), and the shipping zone approach.</p>
</div></body></html>"""

# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Generate three static Store Displays&reg; vision demos (Concept, Release, Prestige).")
    ap.add_argument("out", nargs="?", default="demo", help="output directory (default: ./demo)")
    out = ap.parse_args().out
    img_dir = os.path.join(out, "assets", "img")
    if os.path.isdir(img_dir):
        LOCAL.update(os.listdir(img_dir))
    # Remove only what this script generates, never other files in the output folder.
    for name in list(THEMES):
        shutil.rmtree(os.path.join(out, name), ignore_errors=True)
    if os.path.isfile(os.path.join(out, "index.html")):
        os.remove(os.path.join(out, "index.html"))
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    with open(os.path.join(out, "assets", "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)
    css = {"concept": CSS_CONCEPT, "release": CSS_RELEASE, "prestige": CSS_PRESTIGE}
    cards = []
    for key, t in THEMES.items():
        d = os.path.join(out, key)
        os.makedirs(d)
        with open(os.path.join(d, "style.css"), "w", encoding="utf-8") as f:
            f.write(BASE_CSS + "\n" + EXTRA_CSS + "\n" + css[key])
        for fn, fnc in PAGES.items():
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write(fnc(key))
        pg = "".join('<a href="%s/%s">%s</a>' % (key, fn, lbl) for fn, lbl in
                     [("index.html", "Home"), ("gondola.html", "Gondola"), ("collection.html", "Collection"), ("product.html", "Product"), ("industries.html", "Industry"), ("layouts.html", "Layouts"), ("industry-liquor-stores.html", "Industry page")])
        cards.append('<div class="c"><h2>%s</h2><p>%s</p><div class="pg">%s</div><a class="b" href="%s/index.html">Open %s concept</a></div>'
                     % (t["name"], t["tag"], pg, key, t["name"]))
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(OVERVIEW.replace("@@CARDS@@", "\n".join(cards)))
    print("Built %d pages in %s" % (len(PAGES) * 3 + 1, os.path.abspath(out)))


if __name__ == "__main__":
    main()
