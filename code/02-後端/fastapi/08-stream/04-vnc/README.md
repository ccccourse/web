
https://chatgpt.com/c/6743ce84-d4ec-8012-af6a-f69ce50ae68e

本程式測試執行尚未成功，失敗畫面如下

![](./img/vncRun.png)

## install

```
brew install tiger-vnc
```

https://github.com/novnc/noVNC

## start noVNC

```
(base) cccimac@cccimacdeiMac test % git clone https://github.com/novnc/noVNC.git 
Cloning into 'noVNC'...
remote: Enumerating objects: 13057, done.
remote: Counting objects: 100% (88/88), done.
remote: Compressing objects: 100% (56/56), done.
remote: Total 13057 (delta 44), reused 58 (delta 32), pack-reused 12969 (from 1)
Receiving objects: 100% (13057/13057), 10.32 MiB | 1.89 MiB/s, done.
Resolving deltas: 100% (9122/9122), done.
(base) cccimac@cccimacdeiMac test % cd noVNC
(base) cccimac@cccimacdeiMac noVNC % ls
AUTHORS                 core                    karma.conf.js           snap                    vnc.html
LICENSE.txt             defaults.json           mandatory.json          tests                   vnc_lite.html
README.md               docs                    package.json            utils
app                     eslint.config.mjs       po                      vendor
(base) cccimac@cccimacdeiMac noVNC % ./utils/novnc_proxy --vnc localhost:5901
Warning: could not find self.pem
No installed websockify, attempting to clone websockify...
Cloning into '/Users/cccimac/Desktop/ccc/test/noVNC/utils/websockify'...
remote: Enumerating objects: 4614, done.
remote: Counting objects: 100% (287/287), done.
remote: Compressing objects: 100% (137/137), done.
remote: Total 4614 (delta 179), reused 199 (delta 136), pack-reused 4327 (from 1)
Receiving objects: 100% (4614/4614), 4.70 MiB | 1.94 MiB/s, done.
Resolving deltas: 100% (3021/3021), done.
Using local websockify at /Users/cccimac/Desktop/ccc/test/noVNC/utils/websockify/run
Starting webserver and WebSockets proxy on port 6080


Navigate to this URL:

    http://cccimacdeiMac.local:6080/vnc.html?host=cccimacdeiMac.local&port=6080

Press Ctrl-C to exit


WebSocket server settings:
  - Listen on :6080
  - Web server. Web root: /Users/cccimac/Desktop/ccc/test/noVNC
  - No SSL/TLS support (no cert file)
  - proxying from :6080 to localhost:5901
```
