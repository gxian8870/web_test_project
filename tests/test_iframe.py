from playwright.sync_api import Page,expect


def test_iframe(page:Page):
  page.goto("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_iframe")

  frame = page. frame_locator("iframe[name='iframeResult']")

  expect(frame.locator("body")).to_be_visible()