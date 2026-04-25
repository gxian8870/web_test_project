import pytest
from playwright.sync_api import Page
from datetime import datetime

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True
    }

@pytest.fixture
def page(page: Page):
    page.goto("about:blank")
    return page

def pytest_html_report_title(report):
    report.title = f"Web自动化测试报告 - {datetime.now().strftime('%Y-%m-%d')}"

def pytest_html_results_table_header(cells):
    cells.insert(2,"<th>浏览器</th>")

def pytest_html_results_table_row(report,cells):
    """report:测试报告对象,cells:每个列的数据"""
    cells.pop()
    cells.append("<td>Chromium</td>")


