#!/usr/bin/env python3
"""Generate three static Store Displays&reg; "vision" demos (Concept, Release, Prestige).

Static HTML/CSS/JS mockups styled after the layout feel of three Shopify themes.
They are NOT the real themes. All prices, photos and stats are SAMPLE content.

Usage: build_demo.py [OUTPUT_DIR]   (default: ./demo)
"""
import argparse
import html
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
LOGO = U + "/wp-content/uploads/2025/09/sd-logo.png"
UP = "/wp-content/uploads/"

# Internal mock pages stand in for these real storedisplays.com paths. Everything else links to the live site.
MOCK = {
    "/gondola-shelving/": "gondola.html", "/shop/": "collection.html", "/product-category/counters-showcases/": "collection.html",
    "/industries-we-serve/": "industries.html", "/contact/": "industries.html#contact", "/about/": "industries.html#about",
}


def href(path):
    return MOCK.get(path, U + path)


def a_attrs(h):
    return ' target="_blank" rel="noopener"' if h.startswith("http") else ""


# Header navigation (labels follow the live site's menu, plus the concepts the client asked for)
NAV = [
    ("Shop All Products", "collection.html", True),
    ("Gondola Shelving", "gondola.html", False),
    ("Custom Millwork &amp; Showcases", U + "/custom-millwork-showcases/", False),
    ("Shop by Industry", "industries.html", False),
    ("Free Store Layouts", "industries.html#layouts", False),
    ("Blog", U + "/blog/", False),
    ("About Us", "industries.html#about", False),
    ("Contact Us", "industries.html#contact", False),
]

# The live site's 20 product categories, grouped into mega-menu columns
MEGA = [
    ("Shelving &amp; Systems", [("Gondola Shelving", "/gondola-shelving/"), ("Shelving", "/product-category/shelving/"),
                               ("Wall Standards", "/product-category/wall-standards/"), ("Retail Systems", "/product-category/retail-systems/")]),
    ("Showcases &amp; Counters", [("Display Showcases &amp; Counters", "/product-category/counters-showcases/"),
                                 ("Countertop Displays", "/product-category/countertop-displays/"),
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

# (name, image, path) with images from the live site's category tiles
CATEGORY_TILES = [
    ("Gondola Shelving", UP + "2024/09/Double-Sided_WB.png", "/gondola-shelving/", "contain"),
    ("Display Showcases &amp; Counters", UP + "2026/08/display-cases-lg.jpg", "/product-category/counters-showcases/", "cover"),
    ("Slatwall", UP + "2026/08/slatwalls.png", "/product-category/slatwall/", "cover"),
    ("Gridwall", UP + "2026/08/gridwall-lg.jpg", "/product-category/gridwall/", "cover"),
    ("Apparel Racks", UP + "2026/08/apparel-rack-lg.jpg", "/product-category/apparel-racks/", "cover"),
    ("Mannequins", UP + "2026/08/mannequins-lg.jpg", "/product-category/mannequins/", "cover"),
]

# Industries from the live "Industries We Serve" page
INDUSTRIES = ["Apparel Stores", "Beauty Supply Shops", "Jewelry Stores", "Liquor Stores", "Pharmacies", "Pop-Up Shops", "Smoke/Vape Shops", "Supermarkets"]

IMG_STORE = UP + "2026/08/retail-systems-lg.jpg"
IMG_CASES = UP + "2026/08/display-cases-lg.jpg"
GALLERY = [UP + "2026/08/" + f for f in ["retail-systems-lg.jpg", "general-store-lg.jpg", "display-tables-lg.jpg",
                                          "floor-merchandisers-lg.jpg", "glass-wood-cubby-display-lg.jpg", "shoe-displays-lg.jpg"]]


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
    ("Where do you ship?", "Sample wording based on the live site. Store Displays ships within the United States (Alaska and Hawaii excluded per the kickoff). Order by 2 pm ET and Ground orders ship the same day; LTL orders ship the next day."),
    ("Can you help me plan my store layout?", "Sample answer. A free layout request flow is planned. The client asked for free store layouts, in the way Displayarama offers them."),
    ("Do you offer volume discounts?", "Sample answer. The live site has a Volume Discount Pricing page. Tiered pricing may be explored after launch, once performance data exists."),
    ("Do you build custom showcases and millwork?", "Sample answer. The live site has Custom Millwork &amp; Showcases. Real capabilities to be confirmed."),
    ("How does gondola shelving pricing work?", "Sample answer. Today the gondola page is a quote form with units from $107. The redesign aims to show pricing on the page instead."),
    ("Do I need an account to see prices?", "No. Prices are shown on the page, which matches the live site and the client's goal of reducing request-for-quote drop-off."),
]

TESTIMONIALS = [
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
]

THEMES = {
    "concept": dict(name="Concept", tag="Light, airy and rounded. Inter type, pill buttons, a rounded photo slideshow and a bundle-style builder, as on the Concept demo store.",
                    order=["intro", "tiles", "trending", "gondolaband", "industries", "gallery", "reviews", "blog", "faq", "newsletter"]),
    "release": dict(name="Release", tag="Editorial. A transparent header over a full-bleed hero, light Poppins headlines and banner-led sections, as on the Release demo store.",
                    order=["trending", "dualtiles", "banner", "tiles", "callout", "highlight", "industries", "reviews", "showroom", "blog", "faq", "newsletter"]),
    "prestige": dict(name="Prestige", tag="Quiet and architectural. Spaced uppercase headings, square buttons and a light grey page, as on the Prestige demo store.",
                     order=["tiles", "trending", "banner", "industries", "highlight", "blog", "faq", "newsletter"]),
}


# ----------------------------------------------------------------------------
# Shared page chrome
# ----------------------------------------------------------------------------
FONTS = {
    "concept": "Inter:wght@400;500;700",
    "release": "Poppins:wght@300;400;500;600",
    "prestige": "Instrument+Sans:wght@400;500&family=Nunito:wght@400;600;700",
}


def head(theme, title):
    t = THEMES[theme]
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=%s&display=swap">') % FONTS[theme]
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s | Store Displays&reg; | %s concept</title>'
            '<meta name="description" content="Visual concept of Store Displays&reg; on Shopify, modeled on the %s demo store. Sample content.">'
            '%s<link rel="stylesheet" href="style.css"></head><body class="t-%s">') % (title, t["name"], t["name"], fonts, theme)

def concept_bar(theme, page):
    links = []
    for k, v in THEMES.items():
        cur = ' aria-current="page"' if k == theme else ""
        links.append('<a href="../%s/%s"%s>%s</a>' % (k, page, cur, v["name"]))
    return ('<div class="cbar"><span><strong>Visual concept.</strong> Static mockup modeled on the %s theme\'s public demo store, '
            'not the real theme. Prices, photos and stats are SAMPLE.</span><nav aria-label="Switch concept">%s'
            '<a href="../index.html">Overview</a></nav></div>') % (THEMES[theme]["name"], "".join(links))

def esc(s):
    return html.escape(s, quote=True)


def pic(path, alt, cls="", fit="cover"):
    src = path if path.startswith("http") else U + path
    return ('<div class="ph ph-img ph-%s %s"><img src="%s" alt="%s" loading="lazy"></div>') % (fit, cls, src, esc(alt))


def wordmark():
    return '<a class="logo" href="index.html"><img src="%s" alt="Store Displays" width="150" height="40"></a>' % LOGO


def mega():
    cols = []
    for title, items in MEGA:
        lis = "".join('<li><a href="%s"%s>%s</a></li>' % (href(p), a_attrs(href(p)), l) for l, p in items)
        cols.append('<div class="mcol"><span class="mh">%s</span><ul>%s</ul></div>' % (title, lis))
    promo = ('<div class="mcol mpromo"><strong>Need help choosing?</strong><p>Call <a href="tel:%s">%s</a> or request a free layout plan.</p>'
             '<a class="btn btn-sm" href="industries.html#layouts">Free layout plan</a></div>') % (PHONE_TEL, PHONE1)
    return '<div class="mega" role="menu">%s%s</div>' % ("".join(cols), promo)


HEADER_NAV = {
    "concept": ["Shop All Products", "Gondola Shelving", "Custom Millwork &amp; Showcases", "Shop by Industry", "Free Store Layouts", "Contact Us"],
    "release": ["Shop All Products", "Shop by Industry", "Free Store Layouts", "Contact Us"],
    "prestige": ["Shop All Products", "Gondola Shelving", "Shop by Industry", "Contact Us"],
}

_SVG = 'viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICON_SVG = {
    "search": '<svg %s><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>' % _SVG,
    "user": '<svg %s><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>' % _SVG,
    "cart": '<svg %s><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8a3 3 0 016 0"/></svg>' % _SVG,
}


def header(theme, page):
    mm = mega()
    items = []
    for label, h, has_mega in NAV:
        if label not in HEADER_NAV[theme]:
            continue
        if has_mega:
            items.append('<li class="has-mega"><a href="%s">%s</a>%s</li>' % (h, label, mm))
        else:
            items.append('<li><a href="%s"%s>%s</a></li>' % (h, a_attrs(h), label))
    nav = '<nav class="nav" aria-label="Main"><ul>%s</ul></nav>' % "".join(items)
    icons = ('<div class="hicons"><a href="#" aria-label="Search">%s</a><a href="#" aria-label="Account">%s</a>'
             '<a class="cart" href="#" aria-label="Cart, 0 items">%s<span>0</span></a></div>') % (
        ICON_SVG["search"], ICON_SVG["user"], ICON_SVG["cart"])
    if theme == "concept":
        ann = ('<div class="ann"><span class="ann-l">f &nbsp; X &nbsp; ig &nbsp; yt</span>'
               '<span class="ann-m">&lsaquo;&nbsp; Order by 2 pm ET and Ground orders ship the same day &nbsp;&rsaquo;</span>'
               '<span class="ann-r">English &middot; United States (USD $)</span></div>')
        inner, cls = wordmark() + nav + icons, "hdr"
    elif theme == "release":
        ann = ('<div class="ann"><span>United States</span><span>Same-day shipping, order by 2 pm ET</span>'
               '<span>Call %s</span><span>Volume discount pricing</span></div>') % PHONE1
        inner = nav + wordmark() + icons
        cls = "hdr hdr-over" if page == "index.html" else "hdr"
    else:
        ann = '<div class="ann"><span>Same-day shipping on Ground orders placed by 2 pm ET</span><a href="industries.html#layouts">Free layout plan</a></div>'
        inner, cls = nav + wordmark() + icons, "hdr"
    return '%s%s<header class="%s"><div class="hdr-in">%s</div></header>' % (concept_bar(theme, page), ann, cls, inner)


def footer(theme):
    def ext(l, p):
        return '<li><a href="%s"%s>%s</a></li>' % (href(p), a_attrs(href(p)), l)
    shop = "".join(ext(l, p) for l, p in [("Gondola shelving", "/gondola-shelving/"), ("Display showcases &amp; counters", "/product-category/counters-showcases/"),
                                           ("Slatwall", "/product-category/slatwall/"), ("Gridwall", "/product-category/gridwall/"),
                                           ("Apparel racks", "/product-category/apparel-racks/"), ("Mannequins", "/product-category/mannequins/")])
    info = "".join(ext(l, p) for l, p in [("About", "/about/"), ("Blog", "/blog/"), ("Contact", "/contact/"), ("FAQs", "/faqs/")])
    pol = "".join(ext(l, p) for l, p in [("Volume discount pricing", "/volume-discount-pricing/"), ("Shipping policy", "/shipping-policy/"),
                                          ("Return policy", "/return-policy/"), ("Sitemap", "/sitemap/")])
    return ('<footer class="ftr"><div class="wrap fgrid">'
            '<div><div class="logo logo-f"><img src="%s" alt="Store Displays" width="150" height="40"></div>'
            '<p>%s</p><p>Tel <a href="tel:%s">%s</a><br><a href="mailto:%s">%s</a></p></div>'
            '<div><h4>Shop</h4><ul>%s</ul></div><div><h4>Information</h4><ul>%s</ul></div><div><h4>Policies</h4><ul>%s</ul></div></div>'
            '<div class="wrap fine">Concept mockup for review only. Links, product names, SKUs, prices and images come from storedisplays.com; '
            'everything marked sample is not final. Not a live store.</div></footer>'
            '<script src="../assets/app.js"></script></body></html>') % (LOGO, ADDRESS, PHONE_TEL, PHONE1, EMAIL, EMAIL, shop, info, pol)


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
            '<a class="pimg" href="%s"%s>%s%s</a><div class="pbody"><h3><a href="%s"%s>%s</a></h3>'
            '<p class="pdim">%s</p><div class="sws">%s</div><div class="prow"><strong class="price">%s</strong>%s</div>'
            '<span class="instock">In stock</span><a class="btn btn-sm btn-o" href="%s"%s>View details</a></div></article>'
            ) % (p["kind"], fins, round(p["price"]), 1 if p["new"] else 0, h, ex, pic(p["img"], p["name"], "ph-sm", p["fit"]),
                 badge, h, ex, p["name"], p["sub"], sw, price, samp, h, ex)


def grid(prods, theme, cols=4):
    return '<div class="pgrid c%d">%s</div>' % (cols, "".join(card(p, theme) for p in prods))


def faq_block(items=None):
    items = items or FAQ
    return '<div class="faq">%s</div>' % "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in items)


def section_head(eyebrow, title, link=None):
    l = '<a class="more" href="%s">View all &rarr;</a>' % link if link else ""
    return '<div class="sh"><div><span class="eyebrow">%s</span><h2>%s</h2></div>%s</div>' % (eyebrow, title, l)


def crumbs(*items):
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">%s</nav>' % " / ".join(items)


# ---- Home sections --------------------------------------------------------
def hero(theme):
    src = U + IMG_STORE
    if theme == "concept":
        return ('<section class="hero-c"><div class="slide">%s'
                '<div class="slide-copy"><h1>Store displays that capture attention</h1></div>'
                '<a class="btn btn-w" href="collection.html">Shop all products</a>'
                '<div class="dots"><i class="on"></i><i></i><i></i></div></div></section>') % pic(IMG_STORE, "Modern retail store interior", "ph-hero")
    if theme == "release":
        return ('<section class="hero-r" style="background-image:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.7)),url(%s);background-size:cover;background-position:center">'
                '<div class="hero-r-in"><span class="eyebrow">Chosen by trusted brands nationwide</span>'
                '<h1>Store displays, by design</h1><a class="btn btn-ow" href="collection.html">Discover more</a></div></section>') % src
    return ('<section class="hero-p" style="background-image:linear-gradient(rgba(0,0,0,.5),rgba(0,0,0,.72)),url(%s);background-size:cover;background-position:center">'
            '<div class="hero-p-in"><h1>Showcases made to be seen</h1>'
            '<a class="btn btn-lt" href="collection.html">Shop display showcases</a></div></section>') % (U + IMG_CASES)


def sec_intro(theme):
    return ('<section class="sec intro"><div class="wrap narrow center-t"><h2>Store displays that capture attention</h2>'
            '<p>Whether opening a new boutique or redesigning a grocery store, we have everything you need: top-quality products, '
            'best customer service, affordable pricing and fast shipping.</p>'
            '<a class="btn" href="collection.html">Shop all products</a></div></section>')


def sec_dualtiles(theme):
    t = [("Gondola shelving", UP + "2024/09/Double-Sided_WB.png", "gondola.html", "Build your run", "contain"),
         ("Display showcases &amp; counters", UP + "2026/08/display-cases-lg.jpg", "collection.html", "Shop showcases", "cover")]
    tiles = "".join('<a class="dtile" href="%s">%s<div class="dt-copy"><span class="eyebrow">Featured</span><h2>%s</h2>'
                    '<span class="btn btn-ow">%s</span></div></a>' % (h, pic(i, n, "ph-dt", f), n, c) for n, i, h, c, f in t)
    return '<section class="sec dual"><div class="wrap-w dual-g">%s</div></section>' % tiles


def sec_banner(theme):
    return ('<section class="banner"><div class="banner-copy"><span class="eyebrow">Free store layouts</span>'
            '<h2>Plan your store with our team</h2>'
            '<a class="btn btn-ow" href="industries.html#layouts">Request your free layout plan</a></div></section>')


def sec_callout(theme):
    return ('<section class="callout"><div class="wrap center-t"><h2>Volume discount pricing</h2>'
            '<p>Ordering more? See the live volume discount pricing page.</p>'
            '<a class="btn" href="%s/volume-discount-pricing/" target="_blank" rel="noopener">See volume pricing</a></div></section>') % U


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
            ) % (ADDRESS, PHONE_TEL, PHONE1, pic(UP + "2026/08/general-store-lg.jpg", "Assorted store fixtures", "ph-wide", "cover"))


def sec_tiles(theme):
    t = "".join('<a class="ctile" href="%s"%s>%s<span class="ct-name">%s</span><span class="ct-go">Shop all &rarr;</span></a>'
                % (href(p), a_attrs(href(p)), pic(i, n, "ph-tile", f), n) for n, i, p, f in CATEGORY_TILES)
    return '<section class="sec"><div class="wrap">%s<div class="tiles">%s</div></div></section>' % (
        section_head("Popular product categories", "Shop by category", "collection.html"), t)


def sec_industries(theme):
    t = "".join('<a class="itile" href="industries.html"><span class="it-n">%s</span><span class="it-g">Shop fixtures &rarr;</span></a>' % i for i in INDUSTRIES)
    return ('<section class="sec alt"><div class="wrap">%s<div class="itiles">%s</div>'
            '<p class="note">Industries come from the live Industries We Serve page. Dedicated industry pages are a concept.</p></div></section>'
            ) % (section_head("Find your store type", "Shop by industry", "industries.html"), t)


def sec_trending(theme):
    return ('<section class="sec" id="new"><div class="wrap">%s%s</div></section>'
            % (section_head("Just in", "New &amp; trending products", "collection.html"), grid([p for p in PRODUCTS if p["new"]][:4], theme)))


def sec_gondolaband(theme):
    return ('<section class="gband"><div class="wrap gb-in"><div><span class="eyebrow">Interactive builder</span>'
            '<h2>Build your gondola run</h2><p>Pick the unit type, length, height and finish from the live site\'s real options, and see a price as you go. '
            'Concept only. A real configurator needs an app or custom build.</p>'
            '<a class="btn" href="gondola.html#builder">Start building</a></div>%s</div></section>'
            ) % pic(UP + "2024/09/Double-Sided_WB.png", "Double-sided gondola shelving", "ph-wide", "contain")


def sec_gallery(theme):
    imgs = "".join(pic(g, "Store displays", "ph-g", "cover") for g in GALLERY)
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
    posts = [("Gondola Shelving 101: Versatile Shelving Solutions", "From the live blog. Title taken from the post's address.",
              U + "/gondola-shelving-101-versatile-shelving-solutions/", UP + "2024/09/Double-Sided_WB.png", "contain"),
             ("Choosing the right display case", "Sample SEO article that links to showcases and the jewelry store industry page.", "#",
              UP + "2026/08/display-cases-lg.jpg", "cover"),
             ("Slatwall vs gridwall: which fits your layout", "Sample SEO article that links to slatwall and gridwall products.", "#",
              UP + "2026/08/slatwalls.png", "cover")]
    c = "".join('<a class="bcard" href="%s"%s>%s<h3>%s</h3><p>%s</p><span class="more">Read article &rarr;</span></a>'
                % (h, a_attrs(h), pic(i, t, "ph-b", f), t, d) for t, d, h, i, f in posts)
    return '<section class="sec alt"><div class="wrap">%s<div class="blogs">%s</div></div></section>' % (
        section_head("Store ideas", "From the blog", U + "/blog/"), c)


def sec_newsletter(theme):
    return ('<section class="news"><div class="wrap news-in"><div><h2>Get 10% off your first order</h2>'
            '<p>Concept of the newsletter incentive discussed on the kickoff call. Final offer and terms to be confirmed.</p></div>'
            '<form onsubmit="this.querySelector(\'button\').textContent=\'Thanks (demo)\';return false"><label class="sr" for="em">Email</label>'
            '<input id="em" type="email" placeholder="you@yourstore.com" required><button class="btn">Sign up</button></form></div></section>')


SECS = {
    "intro": sec_intro, "tiles": sec_tiles, "dualtiles": sec_dualtiles, "banner": sec_banner, "callout": sec_callout,
    "highlight": sec_highlight, "showroom": sec_showroom, "industries": sec_industries, "trending": sec_trending,
    "gondolaband": sec_gondolaband, "gallery": sec_gallery, "stats": sec_stats, "reviews": sec_reviews,
    "faq": sec_faq, "blog": sec_blog, "newsletter": sec_newsletter,
}


# ---- Pages ----------------------------------------------------------------
def page_home(theme):
    body = hero(theme) + "".join(SECS[k](theme) for k in THEMES[theme]["order"])
    return head(theme, "Home") + header(theme, "index.html") + "<main>" + body + "</main>" + footer(theme)


def builder():
    return ('<div class="builder" id="builder" data-builder>'
            '<div class="b-steps" data-steps></div><div class="b-panel"><div class="b-q" data-q></div><div class="b-opts" data-opts></div>'
            '<div class="b-nav"><button class="btn btn-o btn-sm" data-back type="button">Back</button>'
            '<button class="btn btn-sm" data-next type="button">Next</button></div></div>'
            '<aside class="b-sum" aria-live="polite"><h3>Your run</h3><ul data-sum></ul>'
            '<div class="b-total"><span>Estimated total</span><strong data-total>$0</strong><small>SAMPLE pricing. The live site lists units from $107.</small></div>'
            '<a class="btn" href="industries.html#contact" data-cta>Request a quote (demo)</a>'
            '<a class="btn btn-o" href="industries.html#layouts">Get a free layout plan</a></aside></div>')


def page_gondola(theme):
    g = [p for p in PRODUCTS if p["kind"] == "gondola"]
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
    body = (crumbs('<a href="index.html">Home</a>', "Gondola shelving") +
            '<section class="ghero"><div class="wrap"><span class="eyebrow">Retail &amp; grocery stores</span><h1>Gondola Shelving</h1>'
            '<p>Where convenience, liquor, grocery and apparel stores shop. Units start from $107 on the live site; this concept puts prices and options on the page instead of a quote form.</p>'
            '<a class="btn" href="#builder">Build your gondola run</a></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Step by step", "Build your gondola run", None) + builder() + '</div></section>'
            '<section class="sec alt"><div class="wrap"><div class="vtiles">' + tiles + '</div></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Unit types", "Gondola shelving products", None) + grid(g, theme, 4) +
            '<p class="note">Single-sided "from $107" is from the live site. Other gondola prices are SAMPLE.</p>'
            '<div class="split spec-split"><div class="seo"><h2>Gondola shelving system specifications</h2><table class="spec">' + spec + '</table>'
            '<p class="note">Specifications are from the live Gondola Shelving page.</p></div>'
            '<div class="seo"><h2>Maximizing vertical space</h2><p>Sample SEO copy. Taller gondola units show more product, as long as they stay accessible to customers. '
            'Single- and double-sided units, end units and upper shelves combine into runs that fit the store.</p>'
            '<div class="ctas"><a class="btn" href="industries.html#contact">Get bulk pricing</a><a class="btn btn-o" href="industries.html#layouts">Request free layout</a></div></div></div>'
            '</div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("Gondola FAQ", "Questions about gondola shelving", None) + faq_block() + '</div></section>')
    return head(theme, "Gondola Shelving") + header(theme, "gondola.html") + "<main>" + body + "</main>" + footer(theme)


def page_collection(theme):
    prods = PRODUCTS
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
    body = (crumbs('<a href="index.html">Home</a>', "Shop all products") +
            '<section class="chero"><div class="wrap"><h1>Shop All Products</h1>'
            '<p>Sample intro copy above the grid, aligned to the product-matched H1 recommended in the SEO plan. Color and size are variants, not separate categories. '
            'Products below are real items from storedisplays.com, with their SKUs and listing prices.</p></div></section>'
            '<section class="sec"><div class="wrap clayout">' + side +
            '<div class="cmain"><div class="ctool"><span data-count>%d products</span>'
            '<label>Sort <select data-sort><option value="">Featured</option><option value="new">Newest</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option></select></label></div>'
            % len(prods) + '<div data-grid>' + grid(prods, theme, 3) + '</div><p class="empty" data-empty hidden>No products match these filters.</p>'
            '<div class="seo"><h2>Choosing store fixtures</h2><p>Sample content below the grid. Explains display cases, gondola shelving, slatwall and racks, sizes, lighting and finishes.</p></div></div></div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("FAQ", "Store fixture questions", None) + faq_block(FAQ[:4]) + '</div></section>')
    return head(theme, "Shop All Products") + header(theme, "collection.html") + "<main>" + body + "</main>" + footer(theme)


def page_product(theme):
    p = PRODUCTS[0]
    rel = [x for x in PRODUCTS if x["kind"] == "case" and x["id"] != p["id"]][:4]

    def opts(name, rows):
        out = ""
        for i, (label, add, real) in enumerate(rows):
            out += ('<label class="swl"><input type="radio" name="%s" value="%s" %s data-opt data-add="%d"> %s</label>'
                    % (name, label, "checked" if i == 0 else "", add, label))
        return out
    colors = opts("color", [("Black", 0, True), ("Silver", -20, True)])
    types = opts("type", [("Regular base", 0, True), ("LED spotlights", 565, True), ("RGB lighted base", 180, False)])
    sizes = opts("size", [("4'", 0, True), ("5'", 60, True), ("6'", 120, False)])
    body = (crumbs('<a href="index.html">Home</a>', '<a href="collection.html">Shop all products</a>', "Display showcases &amp; counters", p["name"]) +
            '<section class="sec"><div class="wrap pdp"><div class="gal-p">' +
            pic(UP + "2024/02/ESC4-B-800x711.png", p["name"], "ph-main", "contain") +
            '<div class="thumbs">' + pic(UP + "2024/02/ESC4-B-800x711.png", "Front view", "ph-th", "contain") +
            pic(UP + "2024/02/ESC4-B_2-800x711.png", "Side view", "ph-th", "contain") + '</div></div>'
            '<div class="info"><span class="eyebrow">Display showcases &amp; counters</span><h1>' + p["name"] + '</h1>'
            '<p class="sku">SKU <span data-sku>%s</span> &middot; In stock</p>' % p["sku"] +
            '<div class="prow big"><strong class="price" data-price data-base="%d">%s</strong></div>' % (p["price"], money(p["price"])) +
            '<p class="note">Base price is the live listing price. Option prices: LED spotlights and the 5\' size are based on live listings, the rest are SAMPLE.</p>'
            '<fieldset class="opt"><legend>Color</legend>' + colors + '</fieldset>'
            '<fieldset class="opt"><legend>Type</legend>' + types + '</fieldset>'
            '<fieldset class="opt"><legend>Size</legend>' + sizes + '</fieldset>'
            '<label class="opt">Quantity <input type="number" min="1" value="1" data-qty></label>'
            '<div class="ctas"><button class="btn" type="button" data-add>Add to cart (demo)</button>'
            '<a class="btn btn-o" href="' + U + '/volume-discount-pricing/" target="_blank" rel="noopener">Volume pricing</a></div>'
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
            '<section class="sec alt"><div class="wrap">' + section_head("You may also like", "Related showcases", None) + grid(rel, theme, 4) + '</div></section>')
    return head(theme, p["name"]) + header(theme, "product.html") + "<main>" + body + "</main>" + footer(theme)


def page_industries(theme):
    tiles = "".join('<a class="itile" href="%s/industries-we-serve/" target="_blank" rel="noopener"><span class="it-n">%s</span><span class="it-g">Shop fixtures &rarr;</span></a>' % (U, i) for i in INDUSTRIES)
    steps = "".join('<li><strong>%s</strong><span>%s</span></li>' % x for x in [
        ("Tell us about your store", "Store type, size and what you sell."), ("Share your floor plan", "Upload a sketch or photos."),
        ("Get your layout", "Concept. Turnaround time to be confirmed.")])
    body = (crumbs('<a href="index.html">Home</a>', "Shop by industry") +
            '<section class="chero"><div class="wrap"><span class="eyebrow">Industries served by Store Displays&reg;</span><h1>Shop by Industry</h1>'
            '<p>Find fixtures for your store type. The live site lists these industries on its Industries We Serve page; dedicated industry pages double as SEO landing pages in this concept.</p></div></section>'
            + sec_stats(theme) +
            '<section class="sec"><div class="wrap"><div class="itiles">' + tiles + '</div><p class="note">Tiles link to the live Industries We Serve page.</p></div></section>'
            '<section class="sec alt" id="layouts"><div class="wrap split"><div><span class="eyebrow">Free store layouts</span><h2>Request your free layout plan</h2>'
            '<ol class="steps">' + steps + '</ol></div>'
            '<form class="form" onsubmit="this.querySelector(\'button\').textContent=\'Thanks (demo)\';return false">'
            '<label>Name<input required></label><label>Email<input type="email" required></label><label>Store type<select><option>Apparel store</option><option>Beauty supply shop</option><option>Jewelry store</option><option>Liquor store</option><option>Pharmacy</option><option>Smoke/vape shop</option><option>Supermarket</option><option>Other</option></select></label>'
            '<label>Tell us about your space<textarea rows="3"></textarea></label><button class="btn">Request layout (demo)</button></form></div></section>'
            '<section class="sec" id="custom"><div class="wrap split">' + pic(UP + "2026/08/glass-wood-cubby-display-lg.jpg", "Glass and wooden display", "ph-tall", "cover") +
            '<div><span class="eyebrow">Custom millwork &amp; showcases</span><h2>Custom showcases and millwork</h2>'
            '<p>The live site has a Custom Millwork &amp; Showcases page. Final copy for this section comes from the client.</p>'
            '<a class="btn" href="' + U + '/custom-millwork-showcases/" target="_blank" rel="noopener">See the live page</a></div></div></section>'
            '<section class="sec alt" id="about"><div class="wrap narrow"><span class="eyebrow">About Store Displays&reg;</span><h2>One-stop shop for store displays</h2>'
            '<p>Placeholder about copy. Per the live site, Store Displays personally selects its merchandise and brings decades of retail merchandising experience. '
            'Final story to come from the client.</p></div></section>'
            '<section class="sec" id="contact"><div class="wrap split"><div><span class="eyebrow">Contact</span><h2>Talk to a fixture expert</h2>'
            '<p>' + ADDRESS + '</p><p>Tel <a href="tel:%s">%s</a><br><a href="mailto:%s">%s</a></p></div>' % (PHONE_TEL, PHONE1, EMAIL, EMAIL) +
            '<form class="form" onsubmit="this.querySelector(\'button\').textContent=\'Thanks (demo)\';return false"><label>Name<input required></label>'
            '<label>Email<input type="email" required></label><label>Message<textarea rows="3"></textarea></label><button class="btn">Send (demo)</button></form></div></section>')
    return head(theme, "Shop by Industry") + header(theme, "industries.html") + "<main>" + body + "</main>" + footer(theme)

PAGES = {"index.html": page_home, "gondola.html": page_gondola, "collection.html": page_collection,
         "product.html": page_product, "industries.html": page_industries}

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
.ftr{background:var(--dark);color:#d9d9d9;padding:50px 0 24px;font-size:.9rem}.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:30px}
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
    list.forEach(function(c){gridEl.appendChild(c)});
  }
  fl.addEventListener('change',apply);sel.addEventListener('change',apply);
  document.querySelector('[data-clear]').onclick=function(){[].forEach.call(fl.querySelectorAll('input'),function(x){x.checked=x.dataset.f==='price'&&x.value===''});apply()};
}
/* Product page */
var pp=document.querySelector('[data-price]'),qty=document.querySelector('[data-qty]');
if(pp&&qty){
  var unit=parseFloat(pp.dataset.base)||0;
  function up(){var add=0;[].forEach.call(document.querySelectorAll('[data-opt]:checked'),function(r){add+=+r.dataset.add||0});pp.textContent=money((unit+add)*(+qty.value||1))}
  qty.addEventListener('input',up);document.addEventListener('change',up);
  var add=document.querySelector('[data-add]');if(add)add.onclick=function(){var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+(+qty.value||1);add.textContent='Added (demo)'};
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
<div class="warn"><strong>Read this first.</strong> These are not the real Shopify themes and not a build. They are HTML/CSS mockups modeled on each theme's public demo store (typography, colours, header, hero and section order), without the theme's code or photography. Product names, SKUs, listing prices, links and images come from the live site and are hot-linked from it. Reviews, most copy, the industry pages and the gondola builder are SAMPLE or CONCEPT. The real build happens in Shopify once the client store exists.</div>
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
</table>
<p class="lead" style="margin-top:22px">Still to do for the real build: confirm the 5 non-ecommerce pages and industry list from the workbook, the client's new logo and colors, a real configurator (app or custom code), appointment booking if wanted, quantity pricing (marked Plus on the theme pages, needs checking), and the shipping zone approach.</p>
</div></body></html>"""

# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Generate three static Store Displays&reg; vision demos (Concept, Release, Prestige).")
    ap.add_argument("out", nargs="?", default="demo", help="output directory (default: ./demo)")
    out = ap.parse_args().out
    # Remove only what this script generates, never other files in the output folder.
    for name in ["assets"] + list(THEMES):
        shutil.rmtree(os.path.join(out, name), ignore_errors=True)
    if os.path.isfile(os.path.join(out, "index.html")):
        os.remove(os.path.join(out, "index.html"))
    os.makedirs(os.path.join(out, "assets"))
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
                     [("index.html", "Home"), ("gondola.html", "Gondola"), ("collection.html", "Collection"), ("product.html", "Product"), ("industries.html", "Industry")])
        cards.append('<div class="c"><h2>%s</h2><p>%s</p><div class="pg">%s</div><a class="b" href="%s/index.html">Open %s concept</a></div>'
                     % (t["name"], t["tag"], pg, key, t["name"]))
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(OVERVIEW.replace("@@CARDS@@", "\n".join(cards)))
    print("Built %d pages in %s" % (len(PAGES) * 3 + 1, os.path.abspath(out)))


if __name__ == "__main__":
    main()
