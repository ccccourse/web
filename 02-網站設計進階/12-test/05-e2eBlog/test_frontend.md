
```
(base) cccimac@cccimacdeiMac 05-e2eBlog % pytest -s test_frontend.py
/opt/miniconda3/lib/python3.12/site-packages/pytest_asyncio/plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
====================================================== test session starts =======================================================
platform darwin -- Python 3.12.2, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/cccimac/Desktop/ccc/html2server/02-後端/fastapi/12-test/05-e2eBlog
plugins: asyncio-0.24.0, playwright-0.6.1, anyio-4.6.0, base-url-2.1.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 1 item                                                                                                                 

test_frontend.py INFO:     Started server process [28420]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
enter home page ...
INFO:     127.0.0.1:50286 - "GET / HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:50286 - "GET /static/index.html HTTP/1.1" 200 OK
INFO:     127.0.0.1:50287 - "GET /static/main.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:50286 - "GET /static/main.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:50287 - "GET /list HTTP/1.1" 200 OK
INFO:     127.0.0.1:50287 - "GET /favicon.ico HTTP/1.1" 404 Not Found
we should have 0 post at start
create post: 
key in : title=aaa, body=aaa
INFO:     127.0.0.1:50287 - "POST /post HTTP/1.1" 200 OK
INFO:     127.0.0.1:50287 - "GET /list HTTP/1.1" 200 OK
we should have 1 post now...
INFO:     127.0.0.1:50287 - "GET /post/0 HTTP/1.1" 200 OK
the title of posts[0] is aaa
.

======================================================= 1 passed in 11.68s =======================================================
INFO:     Shutting down
(base) cccimac@cccimacdeiMac 05-e2eBlog % INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [28420]
```