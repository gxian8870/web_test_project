import time 
from playwright.sync_api import Page

def test_example_com(page:Page):
  start_time = time.time()
  page.goto("https://example.com")
  end_time = time.time()
  load_time = end_time - start_time
  print(load_time)
  assert load_time < 1,f"加载极快,{load_time:.2f}秒"

def test_baidu_com(page:Page):
  start_time = time.time()
  page.goto("https://baidu.com")
  end_time = time.time()
  load_time = end_time - start_time
  print(load_time)
  assert load_time < 2,f"加载速度还行:{load_time:.2f}秒"

def test_github(page:Page):
  start_time = time.time()
  page.goto("https://github.com")
  end_time = time.time()
  load_time = end_time - start_time
  assert load_time < 5,f"加载太慢:{load_time:.2f}秒"
  print(load_time)

def test_performance_comparison(page:Page):
  webs =[
    ("https://example.com",3),
    ("https://baidu.com",5),
    ("https://github.com",5)
  ]
  results = []
  for url,threshold in webs:
    start = time.time()
    page.goto(url)
    end = time.time()
    load_time = end - start
    if load_time < threshold :
      status = "成功"
    else: 
      status = "失败"
    results.append((url,load_time,threshold))
    assert load_time < threshold

  slowest = max(results,key=lambda x:x[1])
  print(f"最慢的是:{slowest[0]},耗时{slowest[1]:.2f}秒")

    
