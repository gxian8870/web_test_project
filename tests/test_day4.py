import pytest
import json
from pathlib import Path

from playwright.sync_api import Page
from pages.example_page import ExamplePage
from pages.wikipedia_page import wikipediaPage

def load_test_data():
  data_file = Path(__file__).parent.parent / "data" / "search_data.json"
  with open(data_file,"r",encoding="utf-8") as f:
    return json.load(f)

def text_example_with_pom(page:Page):
  example_page = ExamplePage(page)

  example_page.goto()
  assert example_page.get_h1_text == "Example Domain"

@pytest.mark.parametrize("test_data",load_test_data())
def test_wikipedia_with_pom(page:Page,test_data):
  keyword = test_data["keyword"]
  expected = test_data["expected"]
  wiki_page = wikipediaPage(page)

  wiki_page.goto()
  wiki_page.search(keyword)
  assert expected in page.url