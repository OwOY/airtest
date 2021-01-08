# airtest  
## 使用步驟 
!python3.7(python3.8以上版本不適用）  
1.下載Airtest IDE  
2.python -m pip install airtest  
3.python -m pip install pocoui   
4.check adb version   (//airtest/core/android/windows/adb/adb.exe --version  >   //nox/bin/adb.exe&nox_adb.exe). 
5.確認手機或模擬器開啟ROOT&手機調適設定  
6.開始使用Airtest  

## 基本用法  
### 連接手機模擬器 port:62025(nox)  
- auto_setup(__file__, devices = ['Android://127.0.0.1:5037/127.0.0.1:62025?cap_method=JAVACAP^&^&ori_method=ADBORI'])  多設備連接  

- x.attr(‘desc’)取得特殊屬性值  
- x.click()  點擊  
- x.get_text()  獲得文本  
- swipe([0, 0], [1, 1]) 滑動螢幕(按比例 左上至右下)  
- x.exist()  確認元素是否存在  
- poco.wait_for_any([a,b,c]) 等待元素存在才繼續  
- poco.wait_for_all([a,b,c]) 等待所有元素存在才繼續  

## 參考文件  
https://www.jianshu.com/p/203eb5f08761 adb 操作  
https://airtest.doc.io.netease.com/   airtest Documents  
https://github.com/AirtestProject/Poco  POCO源碼  
https://www.mdeditor.tw/pl/2iK6/zh-tw  基本介紹  
https://www.cnblogs.com/wutaotaosin/articles/11396827.html  基本操作  
https://www.codenong.com/cs105283799/  進階指令  

## adb    
連接nox  
- adb -s 127.0.0.1:{port}  
查看adb狀態  
- adb devices  
斷開連結！！  
- adb kill-server  
重新連結  
- adb start-server  
進入shell  
- adb -s 127.0.0.1:{port} shell  
重啟adb  
- adb -s 127.0.0.1:{port} reboot  

### 喚醒媒體庫  

- adb shell "am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard  
- adb shell "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/Camera/Video/{video}"  
  
### 強制停止youtube  
- am force-stop com.google.android.youtube
