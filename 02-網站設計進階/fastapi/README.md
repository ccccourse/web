# fastapi 使用方法

假如有個 main.py

可以用下列指令來啟動該 server

    fastapi dev main.py 

或者用

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

這兩種方法都會在程式修改後自動重載

如果不要自動重載，那麼

可以用下列指令來啟動該 server

    fastapi run main.py

或者用

    uvicorn main:app --host 0.0.0.0 --port 8000


## 參考

* https://fastapi.tiangolo.com/
    * [fastapi 教程 - 用户指南](https://fastapi.tiangolo.com/)

啟動後，會自動產生文件檔

* http://127.0.0.1:8000/docs#/
* http://127.0.0.1:8000/redoc

## ChatGPT

* [fastapi 的歷史](https://chatgpt.com/c/6743e10d-6f50-8012-8b5b-522e55f8a1ae)

* [fastapi 的程式可以不要用 typed annotation 還能跑嗎？](https://chatgpt.com/c/6743de52-fb40-8012-81b0-d3cb6a4421a5)

* [哪些套件最常和 fastapi 搭配](https://chatgpt.com/c/6743e88e-860c-8012-b80e-75e24e0adc0a)
