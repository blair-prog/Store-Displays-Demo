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
    "concept": dict(name="Concept", tag="Bold and modern. Closest to the Displayarama feel the client asked for.",
                    order=["tiles", "industries", "trending", "gondolaband", "gallery", "stats", "reviews", "faq", "blog", "newsletter"]),
    "release": dict(name="Release", tag="Content-rich and sectional. Featured, Specials and New Arrivals blocks, like Palay, with Displayarama's industry tiles.",
                    order=["logos", "tiles", "trending", "industries", "gondolaband", "gallery", "stats", "reviews", "faq", "blog", "newsletter"]),
    "prestige": dict(name="Prestige", tag="Premium and showcase-led. Calmer, larger imagery, a more upscale read.",
                     order=["showcase", "tiles", "trending", "industries", "gondolaband", "stats", "reviews", "faq", "blog", "newsletter"]),
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
def head(theme, title, extra=""):
    t = THEMES[theme]
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s | AMKO Displays | %s concept</title>'
            '<meta name="description" content="Visual concept of AMKO Displays on Shopify, styled after the %s theme layout. Sample content.">'
            '<link rel="stylesheet" href="style.css">%s</head><body class="t-%s">') % (title, t["name"], t["name"], extra, theme)


def concept_bar(theme, page):
    links = []
    for k, v in THEMES.items():
        cur = ' aria-current="page"' if k == theme else ""
        links.append('<a href="../%s/%s"%s>%s</a>' % (k, page, cur, v["name"]))
    return ('<div class="cbar"><span><strong>Visual concept.</strong> Static mockup styled after the %s theme layout, '
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


def header(theme, page):
    items = []
    for label, href, has_mega in NAV:
        if has_mega:
            items.append('<li class="has-mega"><a href="%s">%s <span class="car">&#9662;</span></a>%s</li>' % (href, label, mega()))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (href, label))
    ann = ""
    if theme == "release":
        ann = '<div class="ann">Free store layout plans &middot; Volume pricing on gondola runs &middot; Ships across the U.S. (except AK and HI)</div>'
    util = ('<div class="util"><span>Call now <a href="tel:%s">%s</a></span>'
            '<span class="ulinks"><a href="#">Calculate shipping</a><a href="#">New customer application</a><a href="#">My account</a></span></div>') % (PHONE1, PHONE1)
    search = ('<form class="search" role="search" onsubmit="return false"><input type="search" aria-label="Search products" '
              'placeholder="Search products, e.g. gondola, museum case"><button type="submit" aria-label="Search">&#128269;</button></form>')
    cart = '<a class="cart" href="#" aria-label="Cart, 0 items">Cart <span>0</span></a>'
    return ('%s%s<header class="hdr">%s<div class="hdr-in">%s%s<nav class="nav" aria-label="Main"><ul>%s</ul></nav>%s</div></header>'
            % (concept_bar(theme, page), ann, util, wordmark(), search, "".join(items), cart))


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
        return ('<section class="hero hero-c"><div class="wrap hero-grid"><div class="hero-copy">'
                '<span class="eyebrow">Displays solution leader</span>'
                '<h1>Store fixtures,<br>priced and ready<br>to ship.</h1>'
                '<p>See product details and pricing right on the site. Build a gondola run in minutes or get a free layout plan from our team.</p>'
                '<div class="ctas"><a class="btn" href="gondola.html">Build your gondola run</a>'
                '<a class="btn btn-o" href="industries.html#layouts">Request free layout</a></div></div>'
                '<div class="hero-tiles">%s%s%s%s</div></div></section>'
                ) % (ph("gondola", "Gondola shelving photo", "h-t1"), ph("case", "Display case photo", "h-t2"),
                     ph("slatwall", "Slatwall photo", "h-t3"), ph("rack", "Apparel rack photo", "h-t4"))
    if theme == "release":
        return ('<section class="hero hero-r"><div class="wrap"><span class="eyebrow">Everything your store needs</span>'
                '<h1>Shop store fixtures by category or by industry</h1>'
                '<p>Slatwall, gondola shelving, display cases, racks and more, with product details and prices up front.</p>'
                '<form class="hero-search" onsubmit="return false"><input type="search" aria-label="Search" placeholder="Search fixtures"><button class="btn">Search</button></form>'
                '<div class="chips"><a href="gondola.html">Gondola shelving</a><a href="collection.html">Display cases</a><a href="industries.html">Shop by industry</a>'
                '<a href="industries.html#layouts">Free store layouts</a></div></div></section>')
    return ('<section class="hero hero-p"><div class="wrap hero-p-in"><span class="eyebrow">AMKO Displays</span>'
            '<h1>Showcases made to be seen.</h1>'
            '<p>Display cases, counters and fixtures for retailers who care how their merchandise is presented.</p>'
            '<div class="ctas"><a class="btn" href="collection.html">Shop display cases</a><a class="btn btn-o" href="industries.html#layouts">Free layout plan</a></div></div></section>')


def sec_logos(theme):
    return ('<section class="band logos"><div class="wrap"><p class="lbl">Trusted by retailers nationwide (placeholder logos)</p>'
            '<div class="lrow">%s</div></div></section>') % "".join('<span>Client logo</span>' for _ in range(6))


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


def sec_showcase(theme):
    return ('<section class="sec"><div class="wrap split">%s<div><span class="eyebrow">Display cases</span>'
            '<h2>Museum, frameless and counter showcases</h2><p>Jewelry and museum cases, extra, full and half vision cases, ledgetop and corner counters, '
            'with sizes, glass dimensions, lighting and finishes listed right on the page.</p>'
            '<a class="btn" href="collection.html">Explore display cases</a></div></div></section>') % ph("case", "Showcase photo", "ph-tall")


SECS = {
    "logos": sec_logos, "tiles": sec_tiles, "industries": sec_industries, "trending": sec_trending,
    "gondolaband": sec_gondolaband, "gallery": sec_gallery, "stats": sec_stats, "reviews": sec_reviews,
    "faq": sec_faq, "blog": sec_blog, "newsletter": sec_newsletter, "showcase": sec_showcase,
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
.util{display:flex;justify-content:space-between;max-width:1240px;margin:0 auto;padding:6px 20px;font-size:.78rem;opacity:.85}
.util a{margin-left:14px}.util .ulinks a:first-child{margin-left:0}
.hdr-in{max-width:1240px;margin:0 auto;padding:12px 20px;display:flex;flex-wrap:wrap;align-items:center;gap:14px 24px}
.logo{text-decoration:none;display:flex;flex-direction:column;line-height:1;font-family:var(--head)}
.logo-a{font-size:1.9rem;font-weight:900;letter-spacing:.06em}.logo-d{font-size:.66rem;letter-spacing:.42em;opacity:.8}
.search{flex:1;min-width:200px;display:flex}.search input{flex:1;padding:.7em 1em;border:1px solid #cfcfcf;border-radius:var(--r) 0 0 var(--r);font-family:inherit}
.search button{border:0;background:var(--accent);color:var(--on-accent);padding:0 1em;border-radius:0 var(--r) var(--r) 0;cursor:pointer}
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
.hero-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:center}
@media(max-width:980px){.mega{display:none!important}.tiles,.revs,.blogs,.gal{grid-template-columns:1fr 1fr}.itiles,.pgrid.c4{grid-template-columns:1fr 1fr}.pgrid.c3{grid-template-columns:1fr 1fr}
.fgrid,.srow,.vtiles{grid-template-columns:1fr 1fr}.clayout,.pdp,.split,.gb-in,.hero-grid{grid-template-columns:1fr}.builder{grid-template-columns:1fr}.b-steps{flex-direction:row;flex-wrap:wrap}.b-sum{position:static}}
@media(max-width:560px){.tiles,.revs,.blogs,.gal,.itiles,.pgrid.c4,.pgrid.c3,.fgrid,.srow,.vtiles{grid-template-columns:1fr}.util{flex-direction:column;gap:4px}}
"""

CSS_CONCEPT = r"""
:root{--body:"Helvetica Neue",Arial,sans-serif;--head:"Arial Black","Helvetica Neue",Arial,sans-serif;--ls:-.01em;--ink:#10151f;--bg:#fff;--alt:#f1f3f6;--card:#fff;--line:#d9dee6;--mute:#5b6577;
--accent:#ff5a1f;--on-accent:#fff;--dark:#0e1624;--hdr:#0e1624;--hdr-ink:#fff;--hdr-bd:0;--r:2px;--btt:uppercase;--ntt:uppercase;--ph1:#dfe4ec;--ph2:#c3cbd8;--ph-ink:#1b2535}
.t-concept h1,.t-concept h2{text-transform:uppercase}.t-concept .search input{border-color:#2a3550}
.hero-c{background:var(--dark);color:#fff;padding:64px 0}.hero-c h1{font-size:clamp(2.6rem,6vw,4.6rem);line-height:.98}.hero-c p{max-width:480px;color:#c8d0de}.hero-c .btn-o{color:#fff;border-color:#fff}
.hero-tiles{display:grid;grid-template-columns:1fr 1fr;gap:14px}.hero-tiles .ph{aspect-ratio:1/1;--ph1:#26324a;--ph2:#35435f;--ph-ink:#fff}.h-t2{transform:translateY(24px)}.h-t4{transform:translateY(24px)}
.t-concept .itile,.t-concept .pcard,.t-concept .vt,.t-concept .rev{border-width:2px;border-color:#10151f}.t-concept .itile:hover{background:var(--accent);color:#fff}.t-concept .itile:hover .it-g{color:#fff}
.t-concept .ctile .ph{border:2px solid #10151f}.t-concept .badge{border-radius:0}
.t-concept .stats{background:var(--accent);border:0}.t-concept .srow strong,.t-concept .srow span{color:#fff}
.nav>ul>li>a{font-size:.8rem;letter-spacing:.04em}
"""

CSS_RELEASE = r"""
:root{--body:"Segoe UI","Helvetica Neue",Arial,sans-serif;--head:"Segoe UI","Helvetica Neue",Arial,sans-serif;--ls:0;--ink:#1d2b2f;--bg:#fff;--alt:#f3f8f8;--card:#fff;--line:#dbe6e7;--mute:#5c7075;
--accent:#0e7c86;--on-accent:#fff;--dark:#12343a;--hdr:#fff;--hdr-ink:#1d2b2f;--hdr-bd:1px solid #dbe6e7;--r:12px;--btt:none;--ntt:none;--ph1:#e1eeef;--ph2:#c6dcde;--ph-ink:#12343a}
.hero-r{background:linear-gradient(180deg,#e9f4f5,#fff);padding:70px 0 54px;text-align:center}.hero-r p{max-width:620px;margin:0 auto 22px;color:var(--mute)}
.hero-search{display:flex;gap:10px;max-width:560px;margin:0 auto 18px}.hero-search input{flex:1;padding:.9em 1.1em;border:1px solid #bfd3d5;border-radius:99px;font-size:1rem}.hero-search .btn{border-radius:99px}
.chips{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}.chips a{padding:.5em 1.1em;background:#fff;border:1px solid var(--line);border-radius:99px;text-decoration:none;font-weight:600;font-size:.9rem}.chips a:hover{border-color:var(--accent);color:var(--accent)}
.t-release .btn{border-radius:99px}.t-release .pcard,.t-release .itile,.t-release .rev,.t-release .vt{box-shadow:0 2px 10px rgba(18,52,58,.06)}
.t-release .pcard:hover{box-shadow:0 10px 26px rgba(18,52,58,.14)}.t-release .ph{border-radius:12px}.t-release .pimg .ph{border-radius:12px 12px 0 0}
.t-release .logos{background:#fff}.t-release .gband{background:var(--dark)}
.t-release .filters{display:block}
"""

CSS_PRESTIGE = r"""
:root{--body:Georgia,"Times New Roman",serif;--head:Georgia,"Times New Roman",serif;--ls:.01em;--ink:#1c1a17;--bg:#faf8f4;--alt:#f1ede5;--card:#fff;--line:#e2dccf;--mute:#6f685b;
--accent:#9a7b3f;--on-accent:#fff;--dark:#171512;--hdr:#faf8f4;--hdr-ink:#1c1a17;--hdr-bd:1px solid #e2dccf;--r:0;--btt:uppercase;--ntt:uppercase;--ph1:#ebe5d8;--ph2:#d9d0bd;--ph-ink:#4a4130}
h1,h2{font-weight:400}.t-prestige .btn{letter-spacing:.12em;font-size:.78rem;font-family:"Helvetica Neue",Arial,sans-serif}.t-prestige .eyebrow,.t-prestige .nav a,.t-prestige .util,.t-prestige .ctool,.t-prestige .pdim,.t-prestige .samp{font-family:"Helvetica Neue",Arial,sans-serif}
.t-prestige .hdr-in{justify-content:center;text-align:center}.t-prestige .logo{align-items:center}.t-prestige .search{max-width:360px;flex:none}.t-prestige .nav>ul{justify-content:center}
.t-prestige .nav>ul>li>a{font-size:.72rem;letter-spacing:.14em;font-family:"Helvetica Neue",Arial,sans-serif}
.hero-p{background:var(--dark);color:#f4efe4;padding:clamp(90px,14vw,170px) 0;text-align:center}.hero-p h1{font-size:clamp(2.6rem,6vw,5rem);font-style:italic}.hero-p p{max-width:520px;margin:0 auto;color:#c9c1b0}.hero-p .ctas{justify-content:center}.hero-p .btn-o{color:#f4efe4;border-color:#f4efe4}
.t-prestige .ph{aspect-ratio:3/4}.t-prestige .ph-wide{aspect-ratio:16/10}.t-prestige .ph-tall{aspect-ratio:4/5}.t-prestige .ph-g{aspect-ratio:1/1}.t-prestige .ph-b{aspect-ratio:3/2}
.t-prestige .ctile .ct-name{font-weight:400;font-style:italic;font-size:1.3rem;text-transform:none}.t-prestige .pcard{border:0;background:transparent}.t-prestige .pbody{padding:12px 0}.t-prestige .pimg .ph{aspect-ratio:3/4}
.t-prestige .itile{background:transparent;border-width:0 0 1px 0}.t-prestige .itiles{grid-template-columns:repeat(2,1fr);column-gap:50px}.t-prestige .badge{border-radius:0}
.t-prestige .sh{border-bottom:1px solid var(--line);padding-bottom:14px}.t-prestige .rev{border:0;background:transparent;text-align:center;font-size:1.15rem;font-style:italic}
.t-prestige .stats{background:transparent;border-color:var(--line)}.t-prestige .srow strong{font-weight:400}.t-prestige .news{background:var(--dark);color:#f4efe4}.t-prestige .news .btn{background:var(--accent);border-color:var(--accent)}
.t-prestige .tiles{grid-template-columns:repeat(3,1fr);gap:30px}.t-prestige .vt,.t-prestige .b-panel,.t-prestige .b-sum,.t-prestige .form{border-radius:0}
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
<div class="warn"><strong>Read this first.</strong> These are not the real Shopify themes and not a build. They are HTML/CSS mockups styled after the layout feel of Concept, Release and Prestige. All prices, photos, stats, reviews and the gondola builder are SAMPLE or CONCEPT. The real build happens in Shopify once the client store exists.</div>
<div class="cards">
@@CARDS@@
</div>
<h2>How each concept answers the kickoff</h2>
<table><tr><th>Client wish</th><th>Concept</th><th>Release</th><th>Prestige</th></tr>
<tr><td>Modern look like Displayarama</td><td>Closest: bold type, heavy tiles, dark hero</td><td>Clean and friendly, rounded</td><td>Upscale, serif, calmer</td></tr>
<tr><td>Prices and details on the page, no quote form</td><td>Price on every card and product page</td><td>Same</td><td>Same</td></tr>
<tr><td>Gondola configurator</td><td>Step builder mock on the gondola page</td><td>Same mock</td><td>Same mock</td></tr>
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
            f.write(css[key] + "\n" + BASE_CSS)
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
