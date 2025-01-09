import { WebSocketClient, WebSocketServer } from "https://deno.land/x/websocket/mod.ts";
import { Application, send } from "https://deno.land/x/oak/mod.ts";

const app = new Application();

app.use(async (ctx) => {
  console.log('path=', ctx.request.url.pathname)
  await send(ctx, ctx.request.url.pathname, {
    root: `${Deno.cwd()}/public/`,
    index: "index.html",
  });
});

// websocket serve
const wss = new WebSocketServer(8080);

wss.on("connection", function (wsc: WebSocketClient) {
	wsc.on("message", function (message: string) {
		// broadcast message
		wss.clients.forEach(function each(client) {
			if (!client.isClosed) {
				client.send(message);
			}
		});
	});
});

console.log('start at : http://127.0.0.1:8001')
await app.listen({ port: 8001});
