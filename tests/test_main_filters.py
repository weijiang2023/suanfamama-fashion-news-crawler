import main as main_module


def test_filter_sources_includes_by_contains():
    sources = [
        {"name": "The New York Times", "url": "#", "category": "general"},
        {"name": "The Guardian", "url": "#", "category": "general"},
        {"name": "Business of Fashion", "url": "#", "category": "industry"},
    ]

    # No filter returns all
    assert main_module.filter_sources(sources, None) == sources

    # Case-insensitive contains
    filtered = main_module.filter_sources(sources, ["guardian", "fashion"])
    names = [s["name"] for s in filtered]
    assert "The Guardian" in names
    assert "Business of Fashion" in names
    # NYT excluded
    assert "The New York Times" not in names