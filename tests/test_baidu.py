import re
from playwright.sync_api import expect,Page

def test_baidu_search(page:Page):
  page.goto("https://www.baidu.com")
  expect(page).to_have_title(re.compile("百度一下"))
  search_input = page.get_by_role("textbox")
  search_input.wait_for(state="visible")
  search_input.fill("Playwright Python")
  page.get_by_role("button", name="百度一下").click()
  page.wait_for_timeout(3000)