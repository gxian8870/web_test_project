#Page Object Model (POM) 模式
class ExamplePage:
  def __init__(self,page):
    self.page = page
    self.h1 = page.locator("h1")
    self.paragraph = page.locator("p")

  def goto(self):
    self.page.goto("https://example.com")
  
  def get_h1_text(self):
    return self.h1.text_content()

  def get_first_paragraph(self):
    return self.paragraph.first.text_content()