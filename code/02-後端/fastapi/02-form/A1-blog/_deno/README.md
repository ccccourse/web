# Blog -- Classic

```
PS D:\ccc\ccc109a\ws\deno\06-form\blog> deno run -A app.js
Check file:///D:/ccc/ccc109a/ws/deno/06-form/blog/app.js
Server run at http://127.0.0.1:8000
post= { title: "ccc", body: "ccccc" }
post= { title: "ddd", body: "ddddd" }
post= { title: "eee", body: "eeeee" }
...
```

## 使用 ngrok

```
$ ngrok http 8000
```

然後看畫面，連入其網址 （案例中為 http://dcbff267f2a8.ngrok.io)

```
ngrok by @inconshreveable                            (Ctrl+C to quit)
                                                                     
Session Status                online                                 
Session Expires               7 hours, 59 minutes                    
Update                        update available (version 2.3.35, Ctrl-
Version                       2.2.8                                  
Region                        United States (us)                     
Web Interface                 http://127.0.0.1:4040                  
Forwarding                    http://dcbff267f2a8.ngrok.io -> localho
Forwarding                    https://dcbff267f2a8.ngrok.io -> localh
                                                                     
Connections                   ttl     opn     rt1     rt5     p50    
                              0       0       0.00    0.00    0.00 
```