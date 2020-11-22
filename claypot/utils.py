def get_html_lang_attribute(language_code: str) -> str:
    """
    return the HTML lang attribute for a given language code, e. g.
    "en-us" -> "en", "en" -> "en"
    """
    try:
        pos = language_code.index("-")
    except ValueError:
        # no "-" in language_code
        return language_code
    return language_code[:pos]
