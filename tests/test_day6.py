from playwright.sync_api import Page

def test_new_window(page: Page):
    """多窗口测试"""
    # 窗口1：打开 Wikipedia
    page.goto("https://www.wikipedia.org")
    page.wait_for_load_state("networkidle")
    print(f"窗口1: {page.url}")
    
    # 窗口2：创建新窗口，打开 GitHub
    new_page = page.context.new_page()
    new_page.goto("https://github.com")
    new_page.wait_for_load_state("networkidle")
    
    # 验证两个窗口都存在
    all_pages = page.context.pages
    print(f"总窗口数: {len(all_pages)}")
    
    # 验证新窗口 URL
    assert "github.com" in new_page.url
    
    # 在新窗口点击 （用 first 找到第一个匹配的）
    new_page.locator("text=Sign up for GitHub").first.click()
    
    # 关闭新窗口
    new_page.close()