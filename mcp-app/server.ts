import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import fs from "node:fs/promises";
import path from "node:path";

const DIST_DIR = path.join(import.meta.dirname, "dist");

// ユーザーがボタンをクリックするまでツール結果を保留するための共有ステート
let pendingResolver: ((value: string) => void) | null = null;

export function createServer(): McpServer {
  const server = new McpServer({
    name: "Quickstart MCP App Server",
    version: "1.0.0",
  });

  // Two-part registration: tool + resource, tied together by the resource URI.
  const resourceUri = "ui://get-time/mcp-app.html";

  // Register a tool with UI metadata. When the host calls this tool, it reads
  // `_meta.ui.resourceUri` to know which resource to fetch and render as an
  // interactive UI.
  registerAppTool(
    server,
    "get-time",
    {
      title: "Get Time",
      description: "Returns the current server time.",
      inputSchema: {},
      _meta: { ui: { resourceUri } },
    },
    async () => {
      // ユーザーがUIのボタンをクリックするまで結果を返さない
      const time = await new Promise<string>((resolve) => {
        pendingResolver = resolve;
      });
      return { content: [{ type: "text", text: time }] };
    },
  );

  // UIからのみ呼ばれる。保留中のget-timeを解決する
  server.tool("confirm-time", {}, async () => {
    const time = new Date().toISOString();
    if (pendingResolver) {
      pendingResolver(time);
      pendingResolver = null;
    }
    return { content: [{ type: "text", text: time }] };
  });

  // Register the resource, which returns the bundled HTML/JavaScript for the UI.
  registerAppResource(
    server,
    resourceUri,
    resourceUri,
    { mimeType: RESOURCE_MIME_TYPE },
    async () => {
      const html = await fs.readFile(path.join(DIST_DIR, "mcp-app.html"), "utf-8");

      return {
        contents: [
          { uri: resourceUri, mimeType: RESOURCE_MIME_TYPE, text: html },
        ],
      };
    },
  );

  return server;
}