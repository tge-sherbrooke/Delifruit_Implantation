import os
import sys
import pypandoc

# 1st entree
# wkhtmltopdf
pypandoc.convert_text(
    "## Mon titre\n\nCeci est un test.",
    to="pdf",
    format="md",
    outputfile="sortie.pdf",
    extra_args=[
        '--standalone',
        '--pdf-engine=wkhtmltopdf'  # <--- nécessite wkhtmltopdf installé
    ]
)

