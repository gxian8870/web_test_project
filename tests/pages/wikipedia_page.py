class wikipediaPage:
  def __init__(self,page):
    self.page = page
    self.search_input = page.locator("#searchInput")
    self.search_button = page.locator(".pure-button")

  def goto(self):
    self.page.goto("https://www.wikipedia.org/")

  def search(self,keyword):
    self.search_input.fill(keyword)
    self.search_button.click()
  
  def should_be_on_result(self):
    assert "python" in self.page.url
