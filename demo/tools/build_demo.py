#!/usr/bin/env python3
"""Generate three static AMKO Displays "vision" demos (Concept, Release, Prestige).

Static HTML/CSS/JS mockups styled after the layout feel of three Shopify themes.
They are NOT the real themes. All prices, photos and stats are SAMPLE content.

Usage: build_demo.py [OUTPUT_DIR]   (default: ./demo)
"""
import argparse
import os
import shutil

# ----------------------------------------------------------------------------
# Shared content (from the kickoff call, the live amkodisplays.com, workbook TBD)
# ----------------------------------------------------------------------------
PHONE1 = "+1-800-503-7199"
PHONE2 = "+1-201-460-7199"
ADDRESS = "7 Purcell Ct., Moonachie, NJ 07074"

NAV = [
    ("Shop Products", "collection.html", True),
    ("Gondola Shelving", "gondola.html", False),
    ("Display Cases", "collection.html", False),
    ("Shop by Industry", "industries.html", False),
    ("Free Store Layouts", "industries.html#layouts", False),
    ("Custom Manufacturing", "industries.html#custom", False),
    ("New &amp; Trending", "collection.html#new", False),
    ("About", "industries.html#about", False),
    ("Contact", "industries.html#contact", False),
]

MEGA = [
    ("Gondola Shelving", ["Single-sided runs", "Double-sided runs", "End caps", "Accessories"], "gondola.html"),
    ("Display Cases &amp; Counters", ["Jewelry &amp; museum cases", "Frameless", "Extra / full / half vision", "Counter &amp; corner", "Pedestal"], "collection.html"),
    ("Slatwall &amp; Gridwall", ["Slatwall merchandisers", "Slotted wall standards", "Gridwall panels", "Accessories"], "collection.html"),
    ("Racks &amp; Hangers", ["Apparel racks", "Hangers &amp; supplies", "Retail merchandisers"], "collection.html"),
    ("Mannequins &amp; Forms", ["Full-body mannequins", "Torso forms", "Flexible body forms", "Pedestals"], "collection.html"),
    ("Acrylic &amp; Countertop", ["Acrylic &amp; glass displays", "Countertop displays", "Sign holders", "Store supplies"], "collection.html"),
]

CATEGORY_TILES = [
    ("Gondola Shelving", "gondola", "gondola.html"),
    ("Display Cases &amp; Counters", "case", "collection.html"),
    ("Slatwall &amp; Gridwall", "slatwall", "collection.html"),
    ("Apparel Racks", "rack", "collection.html"),
    ("Mannequins &amp; Forms", "form", "collection.html"),
    ("Acrylic &amp; Countertop", "acrylic", "collection.html"),
]

INDUSTRIES = [
    "Jewelry Store", "Clothing Store", "Convenience Store", "Liquor Store", "Sports Card Shop",
    "Gift Shop", "Boutique", "Cell Phone Store", "Pharmacy", "Hardware Store", "Museum &amp; Gallery", "Shoe Store",
]

# kind drives the SVG icon and the filter group
PRODUCTS = [
    dict(id="museum-case", name="Museum Case", sku="JECAG48", kind="case", cat="Jewelry &amp; museum cases",
         price=1895, fin=["Black", "White"], new=True,
         dims='47 1/4"L x 23"W x 37 1/2"H'),
    dict(id="white-jewelry", name="White Jewelry Display", sku="SAMPLE-W1", kind="case", cat="Jewelry &amp; museum cases",
         price=1495, fin=["White"], new=True, dims='47 1/4"L x 23"W x 38"H'),
    dict(id="black-sitdown", name="Black Jewelry Sit-Down Case", sku="SAMPLE-B2", kind="case", cat="Jewelry &amp; museum cases",
         price=1745, fin=["Black"], new=False, dims='47 1/4"L x 29"W x 36"H'),
    dict(id="frameless", name="Frameless Showcase", sku="SAMPLE-F3", kind="case", cat="Frameless",
         price=1295, fin=["Black", "White"], new=True, dims='35"L x 18"W x 38"H'),
    dict(id="ledgetop", name="Ledgetop Counter", sku="SAMPLE-L4", kind="case", cat="Counter &amp; corner",
         price=1650, fin=["Black", "White", "Barnwood"], new=False, dims='70"L x 20"W x 38"H'),
    dict(id="pedestal", name="Pedestal Case", sku="SAMPLE-P5", kind="case", cat="Pedestal",
         price=640, fin=["Black", "White"], new=False, dims='16"L x 16"W x 42"H'),
    dict(id="gondola-double", name="Gondola Starter Unit, Double-Sided", sku="SAMPLE-G6", kind="gondola", cat="Gondola shelving",
         price=1954, fin=["Black", "White"], new=True, dims='48"W x 36"D x 72"H, 4 shelves per side'),
    dict(id="gondola-single", name="Gondola Starter Unit, Single-Sided", sku="SAMPLE-G7", kind="gondola", cat="Gondola shelving",
         price=1090, fin=["Black", "White"], new=False, dims='48"W x 18"D x 72"H, 4 shelves'),
    dict(id="slat-merch", name="Slatwall Merchandiser", sku="SAMPLE-S8", kind="slatwall", cat="Slatwall",
         price=880, fin=["Black", "White"], new=False, dims='48"W x 24"D x 72"H'),
    dict(id="grid-panel", name="Gridwall Panel", sku="SAMPLE-D9", kind="slatwall", cat="Gridwall",
         price=95, fin=["Black", "White", "Chrome"], new=False, dims='24"W x 72"H'),
    dict(id="rack-4way", name="4-Way Apparel Rack", sku="SAMPLE-R10", kind="rack", cat="Apparel racks",
         price=244, fin=["Chrome", "Matte Black"], new=True, dims='48"W x 48"D x 48-72"H'),
    dict(id="torso", name="Female Torso Form", sku="SAMPLE-M11", kind="form", cat="Mannequins &amp; forms",
         price=118, fin=["Black", "White"], new=False, dims='15 15/16"W x 31 1/2"H'),
    dict(id="signholder", name="Acrylic Sign Holder", sku="SAMPLE-A12", kind="acrylic", cat="Sign holders",
         price=14, fin=["Clear"], new=True, dims='8 1/2" x 11"'),
]

FAQ = [
    ("Do you ship nationwide?", "Sample answer. Per the kickoff, shipping is within the United States, excluding Alaska and Hawaii. Rates by weight, size and region are still being researched."),
    ("Can you help me plan my store layout?", "Sample answer. A free layout request flow is planned. The client asked for free store layouts, in the way Displayarama offers them."),
    ("Do you build custom sizes and finishes?", "Sample answer. AMKO lists Custom Manufacturing and Custom Showcases today. Real capabilities to be confirmed in the workbook."),
    ("How do I get bulk pricing?", "Sample answer. Bulk and tiered pricing is handled by phone today and may be explored after launch, once performance data exists."),
    ("How long does delivery take?", "Sample answer. Delivery times and freight rules to be confirmed with the client."),
    ("Do I need an account to see prices?", "In this concept, no. Showing prices directly is one of the main goals of the redesign, replacing today's Login to see prices."),
]

TESTIMONIALS = [
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
    ("Placeholder testimonial. Real customer reviews to be supplied by the client.", "Customer name, City"),
]

BLOGS = [
    ("Gondola shelving: how many runs does your store need?", "Sample SEO article that links to the gondola page and industry pages."),
    ("Choosing the right display case for jewelry", "Sample SEO article that links to jewelry cases and the jewelry store industry page."),
    ("Slatwall vs gridwall: which fits your retail layout", "Sample SEO article that links to slatwall and gridwall products."),
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
# SVG icons (simple line drawings, colored by currentColor)
# ----------------------------------------------------------------------------
def icon(kind):
    s = 'viewBox="0 0 120 90" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"'
    paths = {
        "case": '<rect x="14" y="30" width="92" height="34" rx="2"/><path d="M14 44h92M24 64v18M96 64v18M20 30l8-10h64l8 10"/>',
        "gondola": '<path d="M18 10v72M102 10v72M18 26h84M18 46h84M18 66h84M60 10v72"/><path d="M22 20h12M70 40h12M24 60h10" stroke-width="5"/>',
        "slatwall": '<rect x="16" y="10" width="88" height="70" rx="2"/><path d="M16 24h88M16 38h88M16 52h88M16 66h88"/><path d="M34 30l8 8M70 44h18M40 58h24" stroke-width="5"/>',
        "rack": '<path d="M14 24h92M24 24v58M96 24v58M14 82h20M86 82h20"/><path d="M36 24l6 22h12l6-22M68 24l6 22h12l6-22"/>',
        "form": '<path d="M60 10c-8 0-12 6-12 12 0 4 2 8 4 10l-14 8v28h44V40l-14-8c2-2 4-6 4-10 0-6-4-12-12-12z"/><path d="M60 78v10M44 88h32"/>',
        "acrylic": '<rect x="34" y="14" width="52" height="46" rx="3"/><path d="M42 26h36M42 36h24M42 46h30M46 60l-8 22h44l-8-22"/>',
    }
    return '<svg %s aria-hidden="true">%s</svg>' % (s, paths.get(kind, paths["case"]))


def ph(kind, label="Photo placeholder", cls=""):
    return ('<div class="ph %s" role="img" aria-label="%s"><div class="ph-ic">%s</div>'
            '<span class="ph-label">%s</span></div>') % (cls, label, icon(kind), label)

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
            '<title>%s | AMKO Displays | %s concept</title>'
            '<meta name="description" content="Visual concept of AMKO Displays on Shopify, modeled on the %s demo store. Sample content.">'
            '%s<link rel="stylesheet" href="style.css"></head><body class="t-%s">') % (title, t["name"], t["name"], fonts, theme)

def concept_bar(theme, page):
    links = []
    for k, v in THEMES.items():
        cur = ' aria-current="page"' if k == theme else ""
        links.append('<a href="../%s/%s"%s>%s</a>' % (k, page, cur, v["name"]))
    return ('<div class="cbar"><span><strong>Visual concept.</strong> Static mockup modeled on the %s theme\'s public demo store, '
            'not the real theme. Prices, photos and stats are SAMPLE.</span><nav aria-label="Switch concept">%s'
            '<a href="../index.html">Overview</a></nav></div>') % (THEMES[theme]["name"], "".join(links))

def wordmark():
    return '<a class="logo" href="index.html"><span class="logo-a">AMKO</span><span class="logo-d">DISPLAYS</span></a>'


def mega():
    cols = []
    for title, items, href in MEGA:
        lis = "".join('<li><a href="%s">%s</a></li>' % (href, i) for i in items)
        cols.append('<div class="mcol"><a class="mh" href="%s">%s</a><ul>%s</ul></div>' % (href, title, lis))
    return '<div class="mega" role="menu">%s<div class="mcol mpromo"><strong>Need help choosing?</strong><p>Call our fixture experts or request a free layout plan.</p><a class="btn btn-sm" href="industries.html#layouts">Free layout plan</a></div></div>' % "".join(cols)


HEADER_NAV = {
    "concept": ["Shop Products", "Gondola Shelving", "Display Cases", "Shop by Industry", "Free Store Layouts", "Contact"],
    "release": ["Shop Products", "Shop by Industry", "Free Store Layouts", "Contact"],
    "prestige": ["Shop Products", "Display Cases", "Shop by Industry", "Contact"],
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
    for label, href, has_mega in NAV:
        if label not in HEADER_NAV[theme]:
            continue
        if has_mega:
            items.append('<li class="has-mega"><a href="%s">%s</a>%s</li>' % (href, label, mm))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (href, label))
    nav = '<nav class="nav" aria-label="Main"><ul>%s</ul></nav>' % "".join(items)
    icons = ('<div class="hicons"><a href="#" aria-label="Search">%s</a><a href="#" aria-label="Account">%s</a>'
             '<a class="cart" href="#" aria-label="Cart, 0 items">%s<span>0</span></a></div>') % (
        ICON_SVG["search"], ICON_SVG["user"], ICON_SVG["cart"])
    if theme == "concept":
        ann = ('<div class="ann"><span class="ann-l">f &nbsp; X &nbsp; ig &nbsp; yt</span>'
               '<span class="ann-m">&lsaquo;&nbsp; Free store layout plans &middot; ships across the U.S. except AK and HI &nbsp;&rsaquo;</span>'
               '<span class="ann-r">English &middot; United States (USD $)</span></div>')
        inner, cls = wordmark() + nav + icons, "hdr"
    elif theme == "release":
        ann = ('<div class="ann"><span>United States</span><span>Free store layout plans</span>'
               '<span>Call %s</span><span>Ships across the U.S.</span></div>') % PHONE1
        inner = nav + wordmark() + icons
        cls = "hdr hdr-over" if page == "index.html" else "hdr"
    else:
        ann = '<div class="ann"><span>Free store layout plans</span><a href="industries.html#layouts">Shop now</a></div>'
        inner, cls = nav + wordmark() + icons, "hdr"
    return '%s%s<header class="%s"><div class="hdr-in">%s</div></header>' % (concept_bar(theme, page), ann, cls, inner)

def footer(theme):
    return ('<footer class="ftr"><div class="wrap fgrid">'
            '<div><div class="logo logo-f"><span class="logo-a">AMKO</span><span class="logo-d">DISPLAYS</span></div>'
            '<p>Displays solution leader. Showroom: %s.</p><p>Tel <a href="tel:%s">%s</a><br>Tel <a href="tel:%s">%s</a></p></div>'
            '<div><h4>Shop</h4><ul><li><a href="gondola.html">Gondola shelving</a></li><li><a href="collection.html">Display cases</a></li>'
            '<li><a href="collection.html">Slatwall &amp; gridwall</a></li><li><a href="collection.html">New arrivals</a></li></ul></div>'
            '<div><h4>Customer service</h4><ul><li><a href="industries.html#contact">Contact us</a></li><li><a href="#">New customer application</a></li>'
            '<li><a href="#">Downloadable catalog</a></li><li><a href="#">Assembly instructions</a></li><li><a href="#">Policies</a></li></ul></div>'
            '<div><h4>Company</h4><ul><li><a href="industries.html#about">About us</a></li><li><a href="industries.html#custom">Custom manufacturing</a></li>'
            '<li><a href="#">Our clients</a></li><li><a href="#">Careers</a></li></ul></div></div>'
            '<div class="wrap fine">Concept mockup for review only. Sample content. Not a live store.</div></footer>'
            '<script src="../assets/app.js"></script></body></html>') % (ADDRESS, PHONE1, PHONE1, PHONE2, PHONE2)


def money(n):
    return "${:,.0f}".format(n)


def card(p, theme):
    fins = " ".join(f.lower().replace(" ", "-") for f in p["fin"])
    sw = "".join('<i class="sw sw-%s" title="%s"></i>' % (f.lower().replace(" ", "-"), f) for f in p["fin"][:4])
    badge = '<span class="badge">New</span>' if p["new"] else ""
    return ('<article class="pcard" data-kind="%s" data-fin="%s" data-price="%d" data-new="%d">'
            '<a class="pimg" href="product.html">%s%s</a><div class="pbody"><h3><a href="product.html">%s</a></h3>'
            '<p class="pdim">%s</p><div class="sws">%s</div>'
            '<div class="prow"><strong class="price">%s</strong><span class="samp">sample</span></div>'
            '<span class="instock">In stock</span><a class="btn btn-sm btn-o" href="product.html">View details</a></div></article>'
            ) % (p["kind"], fins, p["price"], 1 if p["new"] else 0, ph(p["kind"], "Product photo", "ph-sm"), badge, p["name"], p["dims"], sw, money(p["price"]))


def grid(prods, theme, cols=4):
    return '<div class="pgrid c%d">%s</div>' % (cols, "".join(card(p, theme) for p in prods))


def faq_block(items=None):
    items = items or FAQ
    return '<div class="faq">%s</div>' % "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in items)


def section_head(eyebrow, title, link=None):
    l = '<a class="more" href="%s">View all &rarr;</a>' % link if link else ""
    return '<div class="sh"><div><span class="eyebrow">%s</span><h2>%s</h2></div>%s</div>' % (eyebrow, title, l)

# ----------------------------------------------------------------------------
# Home sections
# ----------------------------------------------------------------------------
def hero(theme):
    if theme == "concept":
        return ('<section class="hero-c"><div class="slide"><div class="ph ph-hero" role="img" aria-label="Hero photo placeholder">'
                '<div class="ph-ic">%s</div><span class="ph-label">Hero photo placeholder</span></div>'
                '<div class="slide-copy"><h1>Store fixtures, priced and ready to ship</h1></div>'
                '<a class="btn btn-w" href="gondola.html">Shop gondola shelving</a>'
                '<div class="dots"><i class="on"></i><i></i><i></i></div></div></section>') % icon("gondola")
    if theme == "release":
        return ('<section class="hero-r"><div class="hero-r-in"><span class="eyebrow">Everything your store needs</span>'
                '<h1>Fixtures, by design</h1><a class="btn btn-ow" href="collection.html">Discover more</a></div></section>')
    return ('<section class="hero-p"><div class="hero-p-in"><h1>Showcases made to be seen</h1>'
            '<a class="btn btn-lt" href="collection.html">Shop display cases</a></div></section>')


def sec_intro(theme):
    return ('<section class="sec intro"><div class="wrap narrow center-t"><h2>We believe in clear prices and real details</h2>'
            '<p>Sample intro copy. Store fixtures with sizes, finishes and prices on the page, and a team ready to plan your layout.</p>'
            '<a class="btn" href="industries.html#layouts">Request a free layout plan</a></div></section>')


def sec_dualtiles(theme):
    t = [("Gondola shelving", "gondola", "gondola.html", "Build your run"),
         ("Display cases &amp; counters", "case", "collection.html", "Shop cases")]
    tiles = "".join('<a class="dtile" href="%s">%s<div class="dt-copy"><span class="eyebrow">Featured</span><h2>%s</h2>'
                    '<span class="btn btn-ow">%s</span></div></a>' % (h, ph(k, "Tile photo placeholder", "ph-dt"), n, c)
                    for n, k, h, c in t)
    return '<section class="sec dual"><div class="wrap-w dual-g">%s</div></section>' % tiles


def sec_banner(theme):
    return ('<section class="banner"><div class="banner-copy"><span class="eyebrow">Free store layouts</span>'
            '<h2>Plan your store with our team</h2>'
            '<a class="btn btn-ow" href="industries.html#layouts">Request your free layout plan</a></div></section>')


def sec_callout(theme):
    return ('<section class="callout"><div class="wrap center-t"><h2>Volume pricing on gondola runs</h2>'
            '<p>Concept offer. Final bulk pricing terms to be confirmed.</p>'
            '<a class="btn" href="industries.html#contact">Get bulk pricing</a></div></section>')


def sec_highlight(theme):
    p = PRODUCTS[0]
    return ('<section class="sec"><div class="wrap split hl-split">%s<div><span class="eyebrow">Item of the week</span><h2>%s</h2>'
            '<p class="pdim">%s</p><p><strong class="price">%s</strong> <span class="samp">sample</span></p>'
            '<div class="ctas"><a class="btn" href="product.html">Shop now</a></div></div></div></section>'
            ) % (ph("case", "Product photo placeholder", "ph-tall"), p["name"], p["dims"], money(p["price"]))


def sec_showroom(theme):
    return ('<section class="sec alt"><div class="wrap split"><div><span class="eyebrow">Our showroom</span><h2>Visit AMKO Displays</h2>'
            '<p>%s</p><p>Tel <a href="tel:%s">%s</a></p><a class="btn" href="industries.html#contact">Get directions (concept)</a></div>%s</div></section>'
            ) % (ADDRESS, PHONE1, PHONE1, ph("form", "Showroom photo placeholder", "ph-wide"))

def sec_tiles(theme):
    t = "".join('<a class="ctile" href="%s">%s<span class="ct-name">%s</span><span class="ct-go">Shop all &rarr;</span></a>'
                % (h, ph(k, "Category photo", "ph-tile"), n) for n, k, h in CATEGORY_TILES)
    return '<section class="sec"><div class="wrap">%s<div class="tiles">%s</div></div></section>' % (
        section_head("Everything your store needs", "Shop by category", "collection.html"), t)


def sec_industries(theme):
    t = "".join('<a class="itile" href="industries.html"><span class="it-n">%s</span><span class="it-g">Shop fixtures &rarr;</span></a>' % i for i in INDUSTRIES[:8])
    return ('<section class="sec alt"><div class="wrap">%s<div class="itiles">%s</div>'
            '<p class="note">Industry list is a concept. Final list comes from the workbook website plan.</p></div></section>'
            ) % (section_head("Find your store type", "Shop by industry", "industries.html"), t)


def sec_trending(theme):
    return ('<section class="sec" id="new"><div class="wrap">%s%s</div></section>'
            % (section_head("Just in", "New &amp; trending products", "collection.html"), grid([p for p in PRODUCTS if p["new"]][:4], theme)))


def sec_gondolaband(theme):
    return ('<section class="gband"><div class="wrap gb-in"><div><span class="eyebrow">Interactive builder</span>'
            '<h2>Build your gondola run</h2><p>Pick your store type, run length, sides, height and finish. See a price as you go. '
            'Concept only. A real configurator needs an app or custom build.</p>'
            '<a class="btn" href="gondola.html#builder">Start building</a></div>%s</div></section>') % ph("gondola", "Gondola run illustration", "ph-wide")


def sec_gallery(theme):
    return ('<section class="sec"><div class="wrap">%s<div class="gal">%s</div>'
            '<div class="center"><a class="btn" href="tel:%s">Want results like this? Call %s</a></div></div></section>'
            % (section_head("Customer installs", "Real stores. Real results.", None),
               "".join(ph(k, "Store install photo", "ph-g") for k in ["gondola", "case", "slatwall", "rack", "form", "acrylic"]), PHONE1, PHONE1))


def sec_stats(theme):
    s = [("00,000+", "Businesses supplied (placeholder)"), ("00+", "Years in business (placeholder)"),
         ("000+", "Products in catalog (placeholder)"), ("0.0", "Customer rating (placeholder)")]
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
    c = "".join('<a class="bcard" href="#">%s<h3>%s</h3><p>%s</p><span class="more">Read article &rarr;</span></a>'
                % (ph("case", "Article image", "ph-b"), t, d) for t, d in BLOGS)
    return '<section class="sec alt"><div class="wrap">%s<div class="blogs">%s</div></div></section>' % (
        section_head("Store ideas", "From the blog", None), c)


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


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_home(theme):
    body = hero(theme) + "".join(SECS[k](theme) for k in THEMES[theme]["order"])
    return head(theme, "Home") + header(theme, "index.html") + "<main>" + body + "</main>" + footer(theme)


def crumbs(*items):
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">%s</nav>' % " / ".join(items)


def builder():
    return ('<div class="builder" id="builder" data-builder>'
            '<div class="b-steps" data-steps></div><div class="b-panel"><div class="b-q" data-q></div><div class="b-opts" data-opts></div>'
            '<div class="b-nav"><button class="btn btn-o btn-sm" data-back type="button">Back</button>'
            '<button class="btn btn-sm" data-next type="button">Next</button></div></div>'
            '<aside class="b-sum" aria-live="polite"><h3>Your run</h3><ul data-sum></ul>'
            '<div class="b-total"><span>Estimated total</span><strong data-total>$0</strong><small>SAMPLE pricing for the concept only</small></div>'
            '<a class="btn" href="product.html" data-cta>Add to cart (demo)</a>'
            '<a class="btn btn-o" href="industries.html#layouts">Get a free layout plan</a></aside></div>')


def page_gondola(theme):
    g = [p for p in PRODUCTS if p["kind"] == "gondola"]
    tiles = "".join('<div class="vt"><strong>%s</strong><span>%s</span></div>' % x for x in [
        ("Always in stock", "Concept copy. Real stock claims to be confirmed."), ("Wholesale pricing", "Bulk pricing request, quantity tiers after launch."),
        ("Damage-free shipping", "Concept copy. Freight rules to be confirmed."), ("Scheduled deliveries", "Concept copy. Delivery options to be confirmed.")])
    body = (crumbs('<a href="index.html">Home</a>', "Gondola shelving") +
            '<section class="ghero"><div class="wrap"><span class="eyebrow">Store fixtures</span><h1>Gondola Shelving</h1>'
            '<p>Single- and double-sided gondola runs with prices on the page. No quote form needed to start.</p>'
            '<a class="btn" href="#builder">Build your gondola run</a></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Step by step", "Build your gondola run", None) + builder() + '</div></section>'
            '<section class="sec alt"><div class="wrap"><div class="vtiles">' + tiles + '</div></div></section>'
            '<section class="sec"><div class="wrap">' + section_head("Starter units", "Gondola shelving products", None) + grid(g, theme, 3) +
            '<div class="seo"><h2>About gondola shelving</h2><p>Sample SEO copy. Gondola shelving is the freestanding, double- or single-sided shelving used in grocery, liquor, '
            'convenience and general retail. Runs are built from starter units and add-on sections, with end caps, peg hooks and price tag holders.</p>'
            '<p>This block sits below the product grid, as recommended in the SEO plan from the kickoff. Final copy is written after keyword research.</p>'
            '<div class="ctas"><a class="btn" href="industries.html#contact">Get bulk pricing (concept)</a><a class="btn btn-o" href="industries.html#layouts">Request free layout</a></div></div></div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("Gondola FAQ", "Questions about gondola shelving", None) + faq_block() + '</div></section>')
    return head(theme, "Gondola Shelving") + header(theme, "gondola.html") + "<main>" + body + "</main>" + footer(theme)


def page_collection(theme):
    cases = [p for p in PRODUCTS if p["kind"] in ("case",)] + [p for p in PRODUCTS if p["kind"] in ("slatwall", "rack", "form", "acrylic", "gondola")]
    kinds = [("case", "Display cases"), ("gondola", "Gondola"), ("slatwall", "Slatwall &amp; gridwall"), ("rack", "Racks"), ("form", "Forms"), ("acrylic", "Acrylic")]
    finishes = ["Black", "White", "Chrome", "Barnwood", "Matte Black", "Clear"]
    f_kind = "".join('<label><input type="checkbox" data-f="kind" value="%s"> %s</label>' % x for x in kinds)
    f_fin = "".join('<label><input type="checkbox" data-f="fin" value="%s"> <i class="sw sw-%s"></i> %s</label>' % (f.lower().replace(" ", "-"), f.lower().replace(" ", "-"), f) for f in finishes)
    f_price = ('<label><input type="radio" name="pr" data-f="price" value="0-100" > Under $100</label>'
               '<label><input type="radio" name="pr" data-f="price" value="100-1000"> $100 to $1,000</label>'
               '<label><input type="radio" name="pr" data-f="price" value="1000-99999"> Over $1,000</label>'
               '<label><input type="radio" name="pr" data-f="price" value="" checked> Any price</label>')
    side = ('<aside class="filters" data-filters><details open><summary>Type</summary>%s</details>'
            '<details open><summary>Finish / color</summary>%s</details><details open><summary>Price</summary>%s</details>'
            '<button class="btn btn-o btn-sm" type="button" data-clear>Clear filters</button></aside>') % (f_kind, f_fin, f_price)
    body = (crumbs('<a href="index.html">Home</a>', "Store fixtures &amp; displays") +
            '<section class="chero"><div class="wrap"><h1>Store Fixtures &amp; Displays</h1>'
            '<p>Sample intro copy above the grid, aligned to the product-matched H1 recommended in the SEO plan. This is the broad parent category from the kickoff, with Gondola Shelving and Display Cases as prominent standalone areas. Color and size are variants, not separate categories.</p></div></section>'
            '<section class="sec"><div class="wrap clayout">' + side +
            '<div class="cmain"><div class="ctool"><span data-count>%d products</span>'
            '<label>Sort <select data-sort><option value="">Featured</option><option value="new">Newest</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option></select></label></div>'
            % len(cases) + '<div data-grid>' + grid(cases, theme, 3) + '</div><p class="empty" data-empty hidden>No products match these filters.</p>'
            '<div class="seo"><h2>Choosing store fixtures</h2><p>Sample content below the grid. Explains display cases, gondola shelving, slatwall and racks, sizes, lighting and finishes.</p></div></div></div></section>'
            '<section class="sec alt"><div class="wrap narrow">' + section_head("FAQ", "Store fixture questions", None) + faq_block(FAQ[:4]) + '</div></section>')
    return head(theme, "Store Fixtures & Displays") + header(theme, "collection.html") + "<main>" + body + "</main>" + footer(theme)


def page_product(theme):
    p = PRODUCTS[0]
    rel = [x for x in PRODUCTS if x["kind"] == "case" and x["id"] != p["id"]][:4]
    sw = "".join('<label class="swl"><input type="radio" name="fin" value="%s" %s data-fin><i class="sw sw-%s"></i> %s</label>'
                 % (f, "checked" if i == 0 else "", f.lower(), f) for i, f in enumerate(p["fin"]))
    body = (crumbs('<a href="index.html">Home</a>', '<a href="collection.html">Display cases</a>', "Jewelry &amp; museum cases", p["name"]) +
            '<section class="sec"><div class="wrap pdp"><div class="gal-p">' + ph("case", "Main product photo", "ph-main") +
            '<div class="thumbs">' + ph("case", "Photo 2", "ph-th") + ph("case", "Photo 3", "ph-th") + ph("case", "Photo 4", "ph-th") + '</div></div>'
            '<div class="info"><span class="eyebrow">Jewelry &amp; museum cases</span><h1>' + p["name"] + '</h1>'
            '<p class="sku">SKU <span data-sku>%s</span></p>' % p["sku"] +
            '<div class="prow big"><strong class="price" data-price>' + money(p["price"]) + '</strong><span class="samp">sample price</span></div>'
            '<span class="instock">In stock</span>'
            '<fieldset class="opt"><legend>Finish</legend>' + sw + '</fieldset>'
            '<label class="opt">Quantity <input type="number" min="1" value="1" data-qty></label>'
            '<div class="ctas"><button class="btn" type="button" data-add>Add to cart (demo)</button><a class="btn btn-o" href="industries.html#contact">Talk to an expert</a></div>'
            '<ul class="hl"><li>Pull-out tray</li><li>Fabric inner deck</li><li>Gold stainless steel legs</li><li>Four-way top LED lights</li></ul>'
            '<details open><summary>Specifications</summary><table class="spec"><tr><th>Overall size</th><td>47 1/4"L x 23"W x 37 1/2"H</td></tr>'
            '<tr><th>Glass size</th><td>47 1/2"L x 22 3/4"W x 10"H</td></tr><tr><th>Lighting</th><td>Four-way top LED</td></tr>'
            '<tr><th>Legs</th><td>Gold stainless steel</td></tr><tr><th>Interior</th><td>Pull-out tray, fabric inner deck</td></tr></table></details>'
            '<details><summary>Shipping &amp; delivery</summary><p>Concept. U.S. only, excluding Alaska and Hawaii. Freight rules to be confirmed.</p></details>'
            '<details><summary>Assembly &amp; downloads</summary><p>Concept. Assembly instructions and catalog downloads link from here.</p></details>'
            '<p class="note">Specs and SKU are from the live amkodisplays.com Museum Case page. Everything else is sample.</p></div></div></section>'
            '<section class="sec alt"><div class="wrap">' + section_head("You may also like", "Related display cases", None) + grid(rel, theme, 4) + '</div></section>')
    return head(theme, "Museum Case") + header(theme, "product.html") + "<main>" + body + "</main>" + footer(theme)


def page_industries(theme):
    tiles = "".join('<a class="itile" href="#"><span class="it-n">%s</span><span class="it-g">Shop fixtures &rarr;</span></a>' % i for i in INDUSTRIES)
    steps = "".join('<li><strong>%s</strong><span>%s</span></li>' % x for x in [
        ("Tell us about your store", "Store type, size and what you sell."), ("Share your floor plan", "Upload a sketch or photos."),
        ("Get your layout", "Concept. Turnaround time to be confirmed.")])
    body = (crumbs('<a href="index.html">Home</a>', "Shop by industry") +
            '<section class="chero"><div class="wrap"><span class="eyebrow">Every retail business, every fixture</span><h1>Shop by Industry</h1>'
            '<p>Find fixtures for your store type. Industry pages double as SEO landing pages linked to products and blog posts.</p></div></section>'
            + sec_stats(theme) +
            '<section class="sec"><div class="wrap"><div class="itiles">' + tiles + '</div><p class="note">Industry list is a concept pending the workbook website plan.</p></div></section>'
            '<section class="sec alt" id="layouts"><div class="wrap split"><div><span class="eyebrow">Free store layouts</span><h2>Request your free layout plan</h2>'
            '<ol class="steps">' + steps + '</ol></div>'
            '<form class="form" onsubmit="this.querySelector(\'button\').textContent=\'Thanks (demo)\';return false">'
            '<label>Name<input required></label><label>Email<input type="email" required></label><label>Store type<select><option>Jewelry store</option><option>Clothing store</option><option>Convenience store</option><option>Other</option></select></label>'
            '<label>Tell us about your space<textarea rows="3"></textarea></label><button class="btn">Request layout (demo)</button></form></div></section>'
            '<section class="sec" id="custom"><div class="wrap split">' + ph("case", "Custom manufacturing photo", "ph-tall") +
            '<div><span class="eyebrow">Custom manufacturing</span><h2>Custom showcases and fixtures</h2>'
            '<p>Sample page for the existing Custom and Our Services &amp; Capabilities content. Final copy comes from the client.</p>'
            '<ul class="hl"><li>Custom sizes and finishes</li><li>Custom showcases</li><li>Project quotes by request</li></ul>'
            '<a class="btn" href="#contact">Start a custom project</a></div></div></section>'
            '<section class="sec alt" id="about"><div class="wrap narrow"><span class="eyebrow">About AMKO Displays</span><h2>A customer-facing showroom and a nationwide supplier</h2>'
            '<p>Placeholder about copy. The client operates from a customer-facing physical storefront. Real story, history and credentials to come from the client.</p></div></section>'
            '<section class="sec" id="contact"><div class="wrap split"><div><span class="eyebrow">Contact</span><h2>Talk to a fixture expert</h2>'
            '<p>' + ADDRESS + '</p><p>Tel <a href="tel:%s">%s</a><br>Tel <a href="tel:%s">%s</a></p></div>' % (PHONE1, PHONE1, PHONE2, PHONE2) +
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
.t-concept .hdr-in{padding:22px 32px}.t-concept .nav>ul{justify-content:center;gap:28px}
.t-concept .nav>ul>li>a{font-size:1.02rem;font-weight:500;text-transform:none;letter-spacing:0}
.t-concept .logo-a{font-weight:700;letter-spacing:-.03em;font-size:1.7rem}.t-concept .logo-d{letter-spacing:.28em;font-size:.58rem}
.t-concept .cart span{background:#171717;color:#fff}
.hero-c{padding:0 20px 8px}.hero-c .slide{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:16/7;min-height:380px;background:#1b2430}
.ph-hero{position:absolute;inset:0;aspect-ratio:auto;border-radius:0;--ph1:#4a5a70;--ph2:#161d28;--ph-ink:#fff}.ph-hero .ph-ic{width:22%;opacity:.25}
.slide-copy{position:absolute;left:clamp(24px,4vw,56px);bottom:clamp(40px,7vw,80px);max-width:620px;color:#fff;z-index:2}
.slide-copy h1{font-size:clamp(1.8rem,3.4vw,2.7rem);text-transform:uppercase;margin:0}
.hero-c .btn-w{position:absolute;right:clamp(24px,4vw,56px);bottom:clamp(36px,6vw,70px);z-index:2}
.dots{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);display:flex;gap:8px;z-index:2}
.dots i{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.5)}.dots i.on{background:#fff}
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
/* Gondola builder (SAMPLE pricing, concept only) */
var b=document.querySelector('[data-builder]');
if(b){
  var steps=[
    {k:'store',q:'What kind of store is it?',o:[['Convenience store','Compact aisles'],['Liquor store','Heavy loads'],['Grocery','Long runs'],['Gift shop','Mixed goods'],['Other','Tell us more']]},
    {k:'len',q:'How long is the run?',o:[['2 sections','8 ft',2],['4 sections','16 ft',4],['6 sections','24 ft',6],['8 sections','32 ft',8]]},
    {k:'side',q:'Single or double sided?',o:[['Single-sided','Against a wall',1],['Double-sided','Freestanding aisle',1.55]]},
    {k:'h',q:'How tall?',o:[['60 in','Open sightlines',0],['72 in','Most popular',40],['84 in','Max display',90]]},
    {k:'fin',q:'Choose a finish',o:[['Black','Powder coat'],['White','Powder coat']]},
    {k:'acc',q:'Add accessories',multi:true,o:[['End caps','$120 each, x2',240],['Peg hooks pack','$45 per section',45],['Price tag holders','$18 per section',18]]}
  ];
  var st={},i=0,qs=function(s){return b.querySelector(s)};
  var stepsEl=qs('[data-steps]'),q=qs('[data-q]'),opts=qs('[data-opts]'),sum=qs('[data-sum]'),total=qs('[data-total]');
  var base=380;
  function calc(){
    var secs=(st.len&&st.len[2])||0,side=(st.side&&st.side[2])||1,h=(st.h&&st.h[2])||0,t=secs*(base*side+h);
    var accs=st.acc||[];accs.forEach(function(a){t+=a[0]==='End caps'?a[2]:a[2]*secs});
    return t;
  }
  function render(){
    stepsEl.innerHTML='';
    steps.forEach(function(s,n){var x=document.createElement('button');x.type='button';x.textContent=(n+1)+'. '+({store:'Store type',len:'Length',side:'Sides',h:'Height',fin:'Finish',acc:'Accessories'})[s.k];
      x.className=(n===i?'on ':'')+(st[s.k]&&(!s.multi||st[s.k].length)?'done':'');x.onclick=function(){i=n;render()};stepsEl.appendChild(x)});
    var s=steps[i];q.textContent=s.q;opts.innerHTML='';
    s.o.forEach(function(o){var x=document.createElement('button');x.type='button';x.innerHTML=o[0]+'<small>'+o[1]+'</small>';
      var cur=st[s.k];var sel=s.multi?(cur||[]).some(function(c){return c[0]===o[0]}):(cur&&cur[0]===o[0]);if(sel)x.className='sel';
      x.onclick=function(){if(s.multi){var a=st[s.k]||[];var ix=a.findIndex(function(c){return c[0]===o[0]});if(ix>-1)a.splice(ix,1);else a.push(o);st[s.k]=a}else{st[s.k]=o}render()};opts.appendChild(x)});
    sum.innerHTML='';
    steps.forEach(function(s){var v=st[s.k];if(!v||(s.multi&&!v.length))return;var li=document.createElement('li');li.innerHTML='<span>'+({store:'Store',len:'Length',side:'Sides',h:'Height',fin:'Finish',acc:'Extras'})[s.k]+'</span><strong>'+(s.multi?v.map(function(c){return c[0]}).join(', '):v[0])+'</strong>';sum.appendChild(li)});
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
  var unit=parseFloat(pp.textContent.replace(/[^0-9.]/g,''))||0;
  function up(){var f=document.querySelector('[data-fin]:checked');var adj=f&&f.value==='White'?0:0;pp.textContent=money((unit+adj)*(+qty.value||1))}
  qty.addEventListener('input',up);document.addEventListener('change',up);
  var add=document.querySelector('[data-add]');if(add)add.onclick=function(){var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+(+qty.value||1);add.textContent='Added (demo)'};
}
})();
"""

OVERVIEW = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AMKO Displays Vision Demos | SmartSites concept</title>
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
<h1>AMKO Displays: three visual concepts</h1>
<p class="lead">Static mockups for the redesign discussion, built from the SmartSites x Store Display kickoff call (13 Nov 2026) and the live amkodisplays.com. Each concept uses the same sample content so the client compares layout and feel, not copy.</p>
<div class="warn"><strong>Read this first.</strong> These are not the real Shopify themes and not a build. They are HTML/CSS mockups modeled on each theme's public demo store (typography, colours, header, hero and section order), without the theme's code or photography. All prices, photos, stats, reviews and the gondola builder are SAMPLE or CONCEPT. The real build happens in Shopify once the client store exists.</div>
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
    ap = argparse.ArgumentParser(description="Generate three static AMKO Displays vision demos (Concept, Release, Prestige).")
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
