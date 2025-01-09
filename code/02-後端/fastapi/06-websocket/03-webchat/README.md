
無法單獨為 WebSocket 設定不同的端口，WebSocket 會與 HTTP 伺服器共享相同的埠號。所有的 WebSocket 連線都會使用設定的 FastAPI 伺服器端口，預設是 8000。