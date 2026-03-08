import { App } from "@modelcontextprotocol/ext-apps";

// Get element references
const serverTimeEl = document.getElementById("server-time")!;
const getTimeBtn = document.getElementById("get-time-btn")!;

// Create app instance
const app = new App({ name: "Get Time App", version: "1.0.0" });

// AIがツールを呼び出したらボタンを有効化して待機状態にする
app.ontoolinput = () => {
  serverTimeEl.textContent = "Click the button to get the time";
  (getTimeBtn as HTMLButtonElement).disabled = false;
};

// ツール結果が返ってきたら表示する
app.ontoolresult = (result) => {
  const time = result.content?.find((c) => c.type === "text")?.text;
  serverTimeEl.textContent = time ?? "[ERROR]";
};

// ボタンクリックでサーバーの保留中のツール呼び出しを解決する
getTimeBtn.addEventListener("click", async () => {
  (getTimeBtn as HTMLButtonElement).disabled = true;
  serverTimeEl.textContent = "Loading...";
  await app.callServerTool({ name: "confirm-time", arguments: {} });
});

// Connect to host
app.connect();