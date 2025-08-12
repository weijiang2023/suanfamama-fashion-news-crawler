from app.crawler import fetch_and_extract


class DummyResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code


def test_fetch_and_extract_success(monkeypatch):
    html = """
    <html>
      <head>
        <meta property="og:image" content="https://img.example.com/x.jpg" />
      </head>
      <body>
        <article>
          <p>Paragraph one.</p>
          <p>""" + ("Long text. " * 30) + """</p>
        </article>
      </body>
    </html>
    """

    def mock_get(url, headers=None, timeout=None):
        return DummyResponse(html)

    monkeypatch.setattr("app.crawler.requests.get", mock_get)
    result = fetch_and_extract("https://example.com/a")
    assert result["top_image"] == "https://img.example.com/x.jpg"
    assert isinstance(result["content"], str) and len(result["content"]) > 50


def test_fetch_and_extract_short_content(monkeypatch):
    html = "<html><body><article><p>short</p></article></body></html>"

    def mock_get(url, headers=None, timeout=None):
        return DummyResponse(html)

    monkeypatch.setattr("app.crawler.requests.get", mock_get)
    result = fetch_and_extract("https://example.com/a")
    assert result["top_image"] is None
    assert result["content"].strip() == "short"


def test_fetch_and_extract_bad_status(monkeypatch):
    def mock_get(url, headers=None, timeout=None):
        return DummyResponse("oops", status_code=500)

    monkeypatch.setattr("app.crawler.requests.get", mock_get)
    result = fetch_and_extract("https://example.com/a")
    assert result == {"content": None, "top_image": None}


essential_error = RuntimeError("boom")


def test_fetch_and_extract_exception(monkeypatch):
    def mock_get(url, headers=None, timeout=None):
        raise essential_error

    monkeypatch.setattr("app.crawler.requests.get", mock_get)
    result = fetch_and_extract("https://example.com/a")
    assert result == {"content": None, "top_image": None}