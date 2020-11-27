# airtest  
auto_setup(__file__, devices = ['Android://127.0.0.1:5037/127.0.0.1:62025?cap_method=JAVACAP^&^&ori_method=ADBORI'])  多設備連接  

x.attr(‘desc’)取得特殊屬性值  
x.click()  點擊  
x.get_text()  獲得文本  
swipe([0, 0], [1, 1]) 滑動螢幕(按比例 左上至右下)  
x.exist()  確認元素是否存在  
poco.wait_for_any([a,b,c]) 等待元素存在才繼續  
poco.wait_for_all([a,b,c]) 等待所有元素存在才繼續  

https://www.jianshu.com/p/203eb5f08761 adb 操作  
https://airtest.doc.io.netease.com/   airtest Documents  
https://github.com/AirtestProject/Poco  POCO源碼  
https://www.mdeditor.tw/pl/2iK6/zh-tw  基本介紹  
https://www.cnblogs.com/wutaotaosin/articles/11396827.html  基本操作  
https://www.codenong.com/cs105283799/  進階指令  
