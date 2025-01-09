# static

```
PS D:\ccc\ccc109a\ws\deno\04-oak\03-static> deno run -A static1.ts
Check file:///D:/ccc/ccc109a/ws/deno/04-oak/03-static/static1.ts
start at : http://127.0.0.1:8000
cwd= D:\ccc\ccc109a\ws\deno\04-oak\03-static
path= /
path= /README.md
path= /README.md
```

注意！一定要加 -A 或 --allow-read --allow-net 否則 Deno.cwd() 會失敗，而且不會報錯！
