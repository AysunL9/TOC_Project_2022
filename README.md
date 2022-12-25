# Readme_我想回家了
TOC Project 2022
Template Code for TOC Project 2020
A Line bot based on a FSM(finite state machine)
# 目的
 利用Python+LINE Bot建立解謎遊戲，並透過LINE應用

LINE Bot是一種透過Channel Gateway Server，在客戶端系統的Bot Server與LINE App之間，發送和接收資訊的機制。使用發送和接收JSON格式數據的API，來發出請求
# Setup
### Prerequisite
* Python 3.10.5
### Install Dependency
```
pip3 install pipenv
pipenv --three
pipenv install flask
pipenv install line-bot-sdk
pipenv shell
```
# Ngrok
### Install `ngrok`
* [macOS, Windows, Linux](https://ngrok.com/)
or you can use Homebrew (MAC)
```
brew cask install ngrok
```

### Setup
* [How to setup](https://dashboard.ngrok.com/get-started/setup)
> 備註：在終端機需輸入`ngrok http 5000`

# 程式執行先前設置
### 設置伺服器
在終端機開啟CMD輸入執行`ngrok http 5000`
得到Forwarding網址，將此複製到Line Developers的Webhook URL並加上`/callback`
### 虛擬環境執行程式
在終端機中輸入`pipenv shell`進入虛擬環境
於`pipenv`環境中執行`python app.py`

# Finite State Machine
![](https://i.imgur.com/FnJgHhI.png)

# Usage
### 基本操作
* 輸入`開始`即可觸發遊戲
* 在還沒進入遊戲的狀態下，輸入任何字若沒觸發都會有提示
* 隨時輸入`END`(不分大小寫)，即會跳出提示，且回到state->`user`
### 架構圖
1. 輸入`開始`觸發遊戲，進入`教室`場景
2. 進入`教室`場景後，即可開始切換至`黑板`、`書桌`和`置物櫃`場景，搜集各種資訊解開密碼
3. 成功脫逃後，即恢復state->`user`，需輸入`開始`再次觸發
# 使用示範
* ### 加入好友
![](https://i.imgur.com/Ja3VU1E.png#50)

* ### 輸入`開始`，進入`教室`
![](https://i.imgur.com/uJR6InA.png)

* ### 左轉去`黑板`，解出`保險箱`密碼
![](https://i.imgur.com/9eZNJ8C.jpg)


1. ### 左轉去`書桌`，查看`書`的資訊
![](https://i.imgur.com/Dgo34yz.jpg)

* ### 左轉去`置物櫃`，解開`橘色箱子`
![](https://i.imgur.com/6W3jJdM.jpg)

* ### 左轉回`教室`，輸入`門`的密碼，逃出學校
![](https://i.imgur.com/nFb1zSM.jpg)

# state說明
* user: initial state
* pic1: 教室
* pic2: 黑板
* pic3: 書桌
* pic4: 置物櫃
* door: 查看門
* brick: 查看方塊
* book: 查看書
* box: 查看箱子
* safe: 查看保險箱
* check_safe: 確認保險箱的密碼
* safe_pen: 解開保險箱的線索
* check_box: 確認箱子的密碼
* box_pen: 解開箱子的線索
* check_door: 確認門的密碼
* success: 開門
* open: 逃脫成功

# Lauguages : Python 100%
> [name=Ting Yun Liao]
