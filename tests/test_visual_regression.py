from playwright.sync_api import Page
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
import os

def test_take_screenshot(page:Page):
  os.makedirs("screenshots",exist_ok=True)
  page.goto("https://example.com")
  page.screenshot(path="screenshots/example.png")

  assert os.path.exists("screenshots/example.png"),"截图文件不存在"
  
def test_image_same(page:Page):
  os.makedirs("screenshots",exist_ok=True)
  page.goto("https://example.com")
  page.screenshot(path="screenshots/example1.png")
  page.screenshot(path="screenshots/example2.png")
  img1 = Image.open("screenshots/example1.png")
  img2 = Image.open("screenshots/example2.png")
  diff = pixelmatch(img1,img2,output=None,threshold=0.1)
  print(f"差异像素数量:{diff}")
  if diff < 100:print("视觉测试通过")
  else: print("视觉测试失败")
  assert img1.size == img2.size,"图像尺寸不同"
  diff_output = Image.new("RGBA",img1.size,(0,0,0,0))
  diff = pixelmatch(img1,img2,output=diff_output,threshold=0.1)
  diff_output.save("screenshots/diff.png")
  if list(img1.getdata()) == list(img2.getdata()):
    print("一样")
  else :
    print("不太一样")
  
