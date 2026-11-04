from .. import theme


def build(doc):
    theme.exp_head(doc, "01", "08/07/2026",
                   "Static web page design using HTML and CSS")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design and develop a multi-page static website using HTML5 and "
                    "CSS3, covering a common navigation bar, semantic sectioning, tables, "
                    "forms, images and responsive styling.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Create a project folder named RentEase inside the web root.",
        "Create the files index.html, about.html, properties.html, contact.html and css/style.css.",
        "Declare the document type, language and character set in every page.",
        "Build a shared navigation bar with <nav> and <a> so every page links to the others.",
        "Design the home page with a banner image, an introduction and a list of highlights.",
        "Design the about page with the organisation profile, vision, mission and objectives.",
        "Design the properties page with a price table and listing cards.",
        "Design the contact page with an address block and a contact form.",
        "Apply CSS for colour, typography, spacing, borders, box shadows and hover effects.",
        "Make the layout responsive with media queries and flexible grid columns.",
        "Open index.html in a browser and verify links, images and styling.",
    ])
    theme.heading_plain(doc, "HTML ELEMENTS USED:")
    theme.body(doc, "<!DOCTYPE html>, <html>, <head>, <meta>, <title>, <link>, <body>, "
                    "<header>, <nav>, <main>, <section>, <article>, <footer>, <div>, "
                    "<h1>-<h6>, <p>, <ul>, <ol>, <li>, <a>, <img>, <table>, <tr>, <th>, "
                    "<td>, <form>, <label>, <input>, <textarea>, <button>")
    theme.heading_plain(doc, "CSS PROPERTIES USED:")
    theme.body(doc, "font-family, font-size, color, background-color, margin, padding, "
                    "max-width, display, flex, grid, gap, text-align, text-decoration, "
                    "border, border-radius, box-shadow, transition, hover, media queries, "
                    "CSS custom properties (--var).")
    theme.heading_plain(doc, "CODE:")
    theme.code(doc, """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RentEase - Find your next home</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header class="site-header">
        <div class="wrap header-inner">
            <a class="brand" href="index.php">RentEase</a>
            <nav class="site-nav">
                <a href="index.php">Home</a>
                <a href="properties.php">Properties</a>
                <a href="login.php">Login</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="wrap">
            <h1>Rent smarter. Live better.</h1>
            <p class="lead">Search listings, apply online, pay rent and track
               maintenance complaints in one place.</p>
        </div>
    </section>

    <footer class="site-footer">
        <div class="wrap">
            <p>&copy; 2026 RentEase. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>""")
    theme.heading_plain(doc, "KEY CSS:")
    theme.code(doc, """   :root{
     --brand:#0f766e;
     --line:#dfe6ee;
     --radius:14px;
   }

   .header-inner{
     display:flex;
     align-items:center;
     justify-content:space-between;
     min-height:66px;
   }

   .site-nav{display:flex;gap:1.4rem}
   .site-nav a{color:#4b6076;text-decoration:none}
   .site-nav a:hover{color:var(--brand)}

   .cards{
     display:grid;
     grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
     gap:1.2rem;
   }

   @media (max-width:700px){
     .site-nav{flex-direction:column}
   }""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "The home page renders with a fixed header, a full-width hero banner, "
                    "a highlight strip and a three-column feature grid. On a 700 px "
                    "viewport the columns collapse to a single column and the navigation "
                    "stacks vertically.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the static web pages were designed using HTML5 and CSS3 and were "
                    "verified in the browser.")

    theme.rubric_table(doc)
    theme.page_break(doc)
