from playwright.sync_api import Page,expect
from urllib.parse import urlparse, parse_qs
import json

def test_mock_posts(page:Page):
  page.route("**post**",lambda route: route.fulfill(
    status=200,
    content_type = "application/json",
    body = '[{"id":1,"title":"Mock标题","body":"Mock内容"}]'
  ))

  page.goto("https://jsonplaceholder.typicode.com/posts")
  expect(page.locator("body")).to_contain_text("Mock标题")
  expect(page.locator("body")).to_contain_text("Mock内容")

def test_mock_404(page:Page):
  page.route("**post**",lambda route:route.fulfill(
    status=404,
    content_type="text/plain",
    body='Not found'
  ))
  page.goto("https://jsonplaceholder.typicode.com/posts")
  expect(page.locator("body")).to_contain_text("Not found")

def test_dynamic_mock(page:Page):
  def handle_user_id_request(route):
    url = route.request.url
    user_id = url.split("/")[-1]
    if user_id == "1":
      body = '{"id":1, "name":"张三"}'
    elif user_id == "2":
      body = '{"id":2,"name":"李四"}'
    elif user_id == '3':  
      body = '{"id":3,"name":"王五"}'
    route.fulfill(
      status=200,
      content_type="application/json",
      body=body
    )
  page.route("**user**",handle_user_id_request)
  page.goto("https://jsonplaceholder.typicode.com/users/1")
  expect(page.locator("body")).to_contain_text("张三")

def test_method_mock(page:Page):
  def handle_method_request(route):
    method = route.request.method
    if method == "GET":
      body = "使用的是get方法"
    elif method == "POST":
      body = "使用的是post方法"
    else: 
      body= "不知道使用的什么"
    route.fulfill(
      status=200,
      content_type="text/plain",
      body=body
    )
  page.route("**api**",handle_method_request)
  page.goto("https://jsonplaceholder.typicode.com/api/test")
  expect(page.locator("body")).to_contain_text("get")

def test_url_mock(page:Page):
  def handle_url_mock(route):
    page1 = route.request.url.split("=")[-1]
    if page1 == "1":
      body = "这是第一页的数据"
    elif page1 == "2":
      body = "这是第二页的数据"
    else:
      body = "这是第n页得数据"
    
    route.fulfill(
      status=200,
      content_type="text/plain; charset=utf-8",
      body = body
    )
  page.route("**api**",handle_url_mock)
  page.goto("https://jsonplaceholder.typicode.com/api/posts?page=2")
  expect(page.locator("body")).to_have_text("这是第二页的数据")    

def test_login_success(page:Page):
  def handle_login_request(route):
    try:
      data = route.request.post_data_json
      username = data.get("username","")
      password = data.get("password","")
    except:
      route.fulfill(
        status=400,
        content_type="application/json",
        body="找不到数据"
      )
      return 
    if username == "admin" and password == "123456":
      route.fulfill(
        status=200,
        content_type="application/json",
        body='{"message":"登录成功,欢迎用户admin"}'
      )
    elif username == "123" and password == "123456":
      route.fulfill(
        status=200,
        content_type="application/json",
        body = '{"message":"登录成功,欢迎用户123"}'
      )
    else :
      route.fulfill(
        status=400,
        content_type="application/json",
        body='{"用户名错误或者密码错误"}'
      )
  page.route("**/api/login**",handle_login_request)
  def log_response(response):
    print(f"收到响应: {response.url} 状态码: {response.status}")
  page.on("response", log_response)
  page.goto("about:blank")
  result = page.evaluate("""
    async () => {
      try {
        const response = await fetch('https://example.com/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: 'admin',
                password: '123456'
            })
        });
        const data = await response.json();
        return data.message;
      } catch (error) {
        return 'Error: ' + error.message;
      }
    }
  """)
  print(f"登录结果: {result}")
  page.wait_for_timeout(5000)
  assert "登录成功" in result, f"期望包含'登录成功'，实际: {result}"

def test_login_wrong_password(page:Page):
  def handle_login_request(route):
    try:
      data = route.request.post_data_json
      username = data.get("username","")
      password = data.get("password","")
    except:
      route.fulfill(
        status=400,
        content_type="application/json",
        body="找不到数据"
      )
      return 
    if username == "admin" and password == "123456":
      route.fulfill(
        status=200,
        content_type="application/json",
        body='{"message":"登录成功,欢迎用户admin"}'
      )
    elif username == "123" and password == "123456":
      route.fulfill(
        status=200,
        content_type="application/json",
        body = '{"message":"登录成功,欢迎用户123"}'
      )
    else :
      route.fulfill(
        status=400,
        content_type="application/json",
        body='{"error":"用户名错误或者密码错误"}'
      )
  page.route("**/api/login**",handle_login_request)
  def log_response(response):
    print(f"收到响应: {response.url} 状态码: {response.status}")
  page.on("response", log_response)
  page.goto("about:blank")
  result = page.evaluate("""
    async () => {
      try {
        const response = await fetch('https://example.com/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: 'admin',
                password: '1234567'
            })
        });
        const data = await response.json();
        return data.error;
      } catch (error) {
        return 'Error: ' + error.message;
      }
    }
  """)
  assert "用户名错误" in result

def test_search(page:Page):
  def handle_search(route):
    url = route.request.url
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    keyword = params.get("keyword",[''])[0]
    category = params.get("category",[''])[0]
    page1 = params.get("page",[''])[0]

    if keyword == "手机" :
      results = ["小米手机","红米手机","大米手机"]
    elif keyword == "电脑":
      results = ["联想电脑","戴尔电脑","苹果电脑"]
    else : 
      results = [f"关于{keyword}的搜索结果"]
    route.fulfill(
      status=200,
      content_type="application/json",
      body=json.dumps({
        "keyword":keyword,
        "results":results,
        "total":2
      })
    )
  page.route("**search**",handle_search)
  result = page.evaluate("""
    async () => {
      try{
        const response = await fetch("https://example.com/search?keyword=手机&category=电子产品&page=1");
        const data = await response.json();
        return data.results.join(',');
      }
      catch(error){
        return "Error: " + error.message;
      }
    }
  """)
  assert "小米手机" in result

