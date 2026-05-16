from pathlib import Path
from book import Book

class SiteGenerator:
    """
    Takes a project root, loads templates, and generates HTML pages.
    """
    def __init__(self, project_root: Path):
        self .root = project_root
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
        html = self.base_template.replace("{{ title }}", book.title)

        # Build the homepage content
        chapters_list = "<ul>"
        for ch in book.chapters:
            chapters_list += f'<li><a href="chapters/{ch.id}.html">{ch.title}</a></li>'
        chapters_list += "</ul>"

        home_content = f"""
        <h2>Welcome to {book.title}</h2>
        <p>Author: {book.author}</p>
        <h3>Table of Contents</h3>
        {chapters_list}
        """

        # Inject content into the template block
        self.output_dir.mkdir(exist_ok=True)
        output_path = self.output_dir / "index.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print (f"Generated {output_path}")