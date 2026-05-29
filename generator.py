from pathlib import Path
from book import Book
import markdown
import html

class SiteGenerator:
    """
    Takes a project root, loads templates, and generates HTML pages.
    """
    def __init__(self, project_root: Path):
        self.root = project_root
        self.template_dir = project_root / "templates"
        self.output_dir = project_root / "docs"

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
        <h2>Available Books</h2>
        <div class="bookshelf">
            {books_html}
        </div>
        """

        page = self.base_template.replace("{{ title }}", "OpenLib - Home")
        page = page.replace("{% block content %}{% endblock %}", content)

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
        <h2>{html.escape(book.title)}</h2>
        <p>Author: {html.escape(book.author)}</p>
        <h3>Table of Contents</h3>
        {chapters_list}
        """

        page = self.base_template.replace("{{ title }}", book.title)
        page = page.replace("{% block content %}{% endblock %}", book_home_content)

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


    def _generate_chapter_pages(self, book: Book, book_output_dir: Path):
        """
        Generate each chapter page with proper navigation.
        """
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

            full_content = f"""
            <div class="chapter-container">
                {nav_html}
                <div class="chapter-content">
                    {chapter_html}
                </div>
                {nav_html}
            </div>
            """

            page = self.base_template.replace("{{ title }}", ch.title)
            page = page.replace("{% block content %}{% endblock %}", full_content)

            output_path = chapters_output_dir / f"{ch.id}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(page)
            print(f"Generated {output_path}")
