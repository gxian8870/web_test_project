from playwright.sync_api import Page,expect

def test_example(page:Page ):
  page.goto("https://example.com")
  h1 = page.locator("h1")
  expect(h1).to_have_text("Example Domain")
  p = page.locator("p").first
  expect(p).to_contain_text("This domain")

  h1_xpath = page.locator("xpath=//h1")
  assert h1.text_content() == h1_xpath.text_content()

  expect(page).to_have_url("https://example.com/")

  # expect(page.locator("h1")).to_be_visable()
  # expect(page.locator("button")).to_be_enable()
  # # 3. 断言元素有特定属性
  # expect(page.locator("input")).to_hava_attribute("type","text")

  # expect(page.locator("p")).to_have_count(2)

  page.goto("https://www.wikipedia.org")
  page.wait_for_load_state("networkidle")
  page.locator("#searchInput").fill("Python")
  page.locator(".pure-button").click()
  page.wait_for_url("**Python*")




