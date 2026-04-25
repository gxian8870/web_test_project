from playwright.sync_api import Page,expect

def test_example(page:Page):
  page.goto("https://example.com")
  p = page.locator("p").first
  expect(p).to_have_text("This domain is for use in documentation examples without needing permission. Avoid use in operations.")
  expect(p).to_contain_text("This domain")
  h = page.get_by_role("heading",name="Example Domain")
  expect(h).to_contain_text("Example")