we have two code:
1. 登录淘宝
2. 购物车结算

模拟登录淘宝:
1. 滑动窗口也好解决，还是复制 XPath 匹配元素，然后使用 Selenium 的 ActionChains 方法，拖动滑块。
2. 淘宝反 Selenium 登陆破解
只要是使用 Selenium 完成的点击事件，淘宝就不让你登录。
python -m pip install pyautogui
用法很简单，截取登录按钮那里的图片，
然后 pyautogui 就可以根据这张图片，找到按钮的坐标，然后操控电脑的鼠标进行点击。
coords = pyautogui.locateOnScreen('1.png')
x, y = pyautogui.center(coords)
pyautogui.leftClick(x, y)
