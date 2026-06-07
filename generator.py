from pathlib import Path
from book import Book
import markdown
import html
import datetime

class SiteGenerator:
    """
    Takes a project root, loads templates, and generates HTML pages.
    """
    def __init__(self, project_root: Path, base_path: str = "/", site_url: str = ""):
        self.root = project_root
        self.template_dir = project_root / "templates"
        self.output_dir = project_root / "docs"
        self.base_path = base_path.rstrip("/") + "/"
        self.site_url = site_url.rstrip("/")

        #Load the base template once
        template_path = self.template_dir / "base.html"
        with open(template_path, "r", encoding="utf-8") as f:
            self.base_template = f.read()

    def generate_global_homepage(self, books: list):
        """
        Create the main index.html listing all available books.
        """
        books_html = ""
        for book in books:
            safe_title = html.escape(book.title)
            safe_author = html.escape(book.author)
            slug = book.folder.name
            books_html += f"""
            <a href="{slug}/" class="book-card">
                <h3>{safe_title}</h3>
                <p class="author">by {safe_author}</p>
                <p class="chapters-count">{len(book.chapters)} chapters</p>
            </a>
            """

        content = f"""
        <section class="hero">
        <div class="hero-en" lang="en" dir="ltr">
            <h2>Welcome to OpenLib</h2>
            <p>OpenLib is a community-driven platform for translating and sharing open-source books.</p>
            <p>Explore the books below, read translation, or originals, and contribute your own.</p>
        </div>
        <div class="hero-fa" lang="fa" dir="rtl" hidden>
            <h2>به OpenLib خوش آمدید</h2>
            <p>OpenLib یک پلتفرم جامعه‌محور برای ترجمه و به اشتراک‌گذاری کتابهای متن‌باز است  </p>
            <p>کتابهای زیر را بگردید، ترجمه ها را بخوانید و ترجمه خود را اضافه کنید :)</p>
        </div>
        <button id="lang-toggle" aria-label="Switch language" lang="fa">فارسی</button>
        </section>

        <div id="continue-reading-container"></div>

        <h2>Available Books</h2>
        <div class="bookshelf">
            {books_html}
        </div>
        """

        page = self.base_template.replace("{{ title }}", "OpenLib - Home")
        page = page.replace("{{ base_path }}", self.base_path)
        description = "A Collection of open-source translated books."
        meta_tags = self._make_meta_tags("OpenLib - Home", description, "/")
        page = page.replace("{{ description }}", html.escape(description))
        page = page.replace("{{ meta_tags }}", meta_tags)
        page = page.replace("{% block content %}{% endblock %}", content)
        page = page.replace("{{ build_date }}", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
        page = page.replace("{{ edit_link }}", "")

        self.output_dir.mkdir(exist_ok=True)
        output_path = self.output_dir / "index.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"Generated {output_path}")

    def generate_book_pages(self, book: Book):
        """
        Generate a book's own homepage and its chapter pages.
        """
        slug = book.folder.name
        book_output_dir = self.output_dir / slug
        book_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Book's own homepage
        chapters_list = "<ul>"
        for ch in book.chapters:
            safe_title = html.escape(ch.title)
            chapters_list += f'<li><a href="chapters/{ch.id}.html">{safe_title}</a></li>'
        chapters_list += "</ul>"
        
        book_home_content = f"""
        <div lang="{book.book_lang}" dir="{book.book_dir}">
            <h2>{html.escape(book.title)}</h2>
            <p>Author: {html.escape(book.author)}</p>
            <h3>Table of Contents</h3>
            {chapters_list}        
        </div>
        """

        page = self.base_template.replace("{{ title }}", book.title)
        page = page.replace("{{ base_path }}", self.base_path)
        description = f"Read {book.title} by {book.author} - an open-source translated book."
        meta_tags = self._make_meta_tags(book.title, description, f"/{slug}/")
        page = page.replace("{{ description }}", html.escape(description))
        page = page.replace("{{ meta_tags }}", meta_tags)
        page = page.replace("{% block content %}{% endblock %}", book_home_content)
        page = page.replace("{{ build_date }}", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
        edit_url = f"https://github.com/Far-Davari/OPENLIB/edit/main/content/books/{slug}/metadata.json"
        if book.book_lang == "fa":
            edit_text = "ویرایش این کتاب در گیت‌هاب"
        else:
            edit_text = "Edit this book on GitHub"
        edit_link = f'<p class="edit-page-link"><a href="{edit_url}" lang="{book.book_lang}" target="_blank" rel="noopener noreferrer">{edit_text}</a></p>'
        page = page.replace("{{ edit_link }}", edit_link)

        output_path = book_output_dir / "index.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"Generated {output_path}")

        self._generate_chapter_pages(book, book_output_dir)

    def generate_search_index(self, books: list):
        """
        Create a JSON file that the front-end search can use.
        """
        index = []

        for book in books:
            slug = book.folder.name
            # Add the book itself
            index.append({
                "title": book.title,
                "book": book.title,
                "type": "book",
                "url": f"/{slug}/"
            })

            # Add each chapter
            for ch in book.chapters:
                snippet = ""
                if ch.content_file.exists():
                    raw = ch.content_file.read_text(encoding="utf-8")
                    
                    import re
                    cleaned = re.sub(r'[#*`>\[\]]', '', raw)
                    snippet = cleaned.strip()[:200]
                index.append({
                    "title": ch.title,
                    "book": book.title,
                    "type": "chapter",
                    "url": f"/{slug}/chapters/{ch.id}.html",
                    "snippet": snippet
                })
        
        # Write the JSON file into the output folder
        import json
        output_path = self.output_dir / "search-index.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        print(f"Generated {output_path}")

    def generate_seo_files(self, books: list):
        if not self.site_url:
            print("No SITE_URL set - skipping sitemap and robots.txt")
            return
        
        # Sitemap
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        # Homepage
        sitemap += f"  <url><loc>{self.site_url}{self.base_path}</loc><changefreq>daily</changefreq></url>\n"

        for book in books:
            slug = book.folder.name
            sitemap += f"  <url><loc>{self.site_url}{self.base_path}{slug}/</loc><changefreq>weekly</changefreq></url>\n"
            for ch in book.chapters:
                sitemap += f"  <url><loc>{self.site_url}{self.base_path}{slug}/chapters/{ch.id}.html</loc><changefreq>monthly</changefreq></url>\n"
        
        sitemap += '</urlset>\n'

        output_path = self.output_dir / "sitemap.xml"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sitemap)
        print(f"Generated {output_path}")

        # Robots.txt
        robots = f"User-agent: *\nAllow: /\nSitemap: {self.site_url}{self.base_path}sitemap.xml\n"
        output_path = self.output_dir / "robots.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(robots)
        print(f"Generated {output_path}")

    def _generate_chapter_pages(self, book: Book, book_output_dir: Path):
        """
        Generate each chapter page with proper navigation.
        """
        slug = book.folder.name
        chapters_output_dir = book_output_dir / "chapters"
        chapters_output_dir.mkdir(exist_ok=True)

        total_chapters = len(book.chapters)

        for i, ch in enumerate(book.chapters):
            if not ch.content_file.exists():
                print(f"Warning: {ch.content_file} not found - Skipping")
                continue
            
            md_text = ch.content_file.read_text(encoding="utf-8")
            chapter_html = markdown.markdown(md_text)

            # Navigation bar - all paths relative to the chapter file inside chapters/
            nav_html = '<nav class="chapter-nav" aria-label="Chapter navigation">'

            # Previous link
            if i > 0:
                prev_ch = book.chapters[i - 1]
                nav_html += (
                    f'<a class="prev" href="{prev_ch.id}.html" rel="prev">'
                    f'&laquo; {html.escape(prev_ch.title)}</a>'
                )
            else: 
                nav_html += '<span class="prev disabled">&laquo; Previous</span>'
            
            # Home link
            nav_html += '<a class="home" href="../index.html">Home</a>'

            # Next link
            if i < total_chapters - 1:
                next_ch = book.chapters[i + 1]
                nav_html += (
                    f'<a class="next" href="{next_ch.id}.html" rel="next">'
                    f'{html.escape(next_ch.title)} &raquo;</a>'
                )
            else:
                nav_html += '<span class="next disabled"> Next &raquo;</span>'

            nav_html += "</nav>"

            # Chapter progress indicatior
            if book.book_lang == "fa":
                progress_text = f"فصل {i + 1} از {total_chapters}"
            else: 
                progress_text = f"Chapter {i + 1} of {total_chapters}"
            progress_html = f'<p class="chapter-progress">{progress_text}</p>'

            # Calcuate reading time
            word_count = len(md_text.split())
            minutes = max(1, round(word_count / 200))
            
            if book.book_lang == "fa":
                reading_time_html = f'<p class="reading-time">⏱ ≈ {minutes} دقیقه مطالعه</p>'
            else:
                reading_time_html = f'<p class="reading-time">⏱ ≈ {minutes} min read</p>'

            full_content = f"""
            <div class="chapter-container">
                {nav_html}
                {progress_html}
                <div class="chapter-content"  lang="{book.book_lang}" dir="{book.book_dir}">
                    {reading_time_html}
                    {chapter_html}
                </div>
                {nav_html}
            </div>
            """

            page = self.base_template.replace("{{ title }}", ch.title)
            page = page.replace("{{ base_path }}", self.base_path)
            import re
            cleaned = re.sub(r'[#*`>\[\]]', '', md_text)
            snippet = cleaned.strip()[:200]
            description = snippet if snippet else f"Chapter {ch.title} of {book.title}"
            meta_tags = self._make_meta_tags(ch.title, description, f"/{slug}/chapters/{ch.id}.html")
            page = page.replace("{{ description }}", html.escape(description))
            page = page.replace("{{ meta_tags }}", meta_tags)
            page = page.replace("{% block content %}{% endblock %}", full_content)
            page = page.replace("{{ build_date }}", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))

            edit_url = f"https://github.com/Far-Davari/OPENLIB/edit/main/content/books/{slug}/chapters/{ch.id}.md"
            if book.book_lang == "fa":
                edit_text = "ویرایش این صفحه در گیت‌هاب"
            else:
                edit_text = "Edit this page on GitHub"
            edit_link = f'<p class="edit-page-link"><a href="{edit_url}" lang="{book.book_lang}" target="_blank" rel="noopener noreferrer">{edit_text}</a></p>'
            page = page.replace("{{ edit_link }}", edit_link)

            output_path = chapters_output_dir / f"{ch.id}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(page)
            print(f"Generated {output_path}")
    
    def _make_meta_tags(self, title: str, description: str, url: str) -> str:
        tags = ""
        tags += f'<meta property="og:title" content="{html.escape(title)}">\n'
        tags += f'<meta property="og:description" content="{html.escape(description[:200])}">\n'
        tags += f'<meta property="og:type" content="website">\n'
        if self.site_url:
            full_url = self.site_url + self.base_path.rstrip("/") + url
            tags += f'<meta property="og:url" content="{full_url}">\n'
        tags += '<meta name="twitter:card" content="summary">\n'
        if self.site_url:
            tags += f'<link rel="canonical" href="{self.site_url}{self.base_path.rstrip("/")}{url}">\n'
        return  tags
