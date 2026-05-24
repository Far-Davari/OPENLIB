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

    def generate_homepage(self, book: Book):
        """
        Creates the main index.html for a given book.
        """
        # Replace title
        html_output = self.base_template.replace("{{ title }}", book.title)

        # Build the homepage content
        chapters_list = "<ul>"
        for ch in book.chapters:
            safe_title = html.escape(ch.title)
            chapters_list += f'<li><a href="chapters/{ch.id}.html">{safe_title}</a></li>'
        chapters_list += "</ul>"

        home_content = f"""
        <h2>Welcome to {html.escape(book.title)}</h2>
        <p>Author: {html.escape(book.author)}</p>
        <h3>Table of Contents</h3>
        {chapters_list}
        """

        html_output = html_output.replace("{% block content %}{% endblock %}", home_content)

        # Inject content into the template block
        self.output_dir.mkdir(exist_ok=True)
        output_path = self.output_dir / "index.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)

        print (f"Generated {output_path}")
    
    def generate_chapter_pages(self, book: Book):
        """
        Creates one HTML page for each chapter of the book, with Previous/Next nav.
        """
        chapters_output_dir = self.output_dir / "chapters"
        chapters_output_dir.mkdir(exist_ok=True)

        total_chapters = len(book.chapters)

        for i, ch in enumerate(book.chapters):
            # Check if the chapter Markdown exists
            if not ch.content_file.exists():
                print(f"Warning: {ch.content_file} not found - skipping")
                continue
            
            # Read the Markdown and convert to HTML
            md_text = ch.content_file.read_text(encoding="utf-8")
            chapter_html = markdown.markdown(md_text)

            # ---- BUILD NAVIGATION BAR ----
            # Create <nav> element
            nav_html ='<nav class="chapter-nav" aria-label="Chapter Navigation">'

            # -- Previous link --
            if i > 0:
                prev_ch = book.chapters[i - 1]

                # html.escape to protect against broken HTML
                nav_html += (
                    f'<a class="prev" href="{prev_ch.id}.html" rel="prev">'
                    f'&laquo; {html.escape(prev_ch.title)}</a>'
                )
            else:
                # Disable placeholder for the first chapter
                nav_html += '<span class="prev disabled">&laquo; Previous</span>'
            
            # -- Home link -- 
            nav_html += '<a class="home" href="../index.html">Home</a>'

            # -- Next link --
            if i < total_chapters - 1:
                next_ch = book.chapters[i + 1]
                nav_html += (
                    f'<a class="next" href="{next_ch.id}.html" rel="next">'
                    f'{html.escape(next_ch.title)} &raquo;</a>'
                )
            else:
                # Disabled placeholder for the last chapter
                nav_html += '<span class="next disabled"> Next &raquo;</span>'
            
            nav_html += '</nav>'

            # ----- ASSEMBLE FINAL PAGE CONTENT -----
            full_content = f"""
            <div class="chapter-container">
                {nav_html}
                <div class="chapter-content">
                    {chapter_html}
                </div>
                {nav_html}
            </div>
            """

            # ---- FILL THE TEMPLATE ----
            page = self.base_template.replace("{{ title }}", ch.title)
            page = page.replace("{% block content %}{% endblock %}", full_content)

            # ---- WRITE OUTPUT FILE ----
            output_path = chapters_output_dir / f"{ch.id}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(page)
            
            print(f"Generated {output_path}")