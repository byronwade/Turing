import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { resolve } from "node:path";
import { request as httpRequest } from "node:http";

const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const html = resolve(here, "dist/index.html");
const port = Number(process.env.TURING_SERVO_WEBDRIVER_PORT || 7010);
const candidates = [
  process.env.TURING_SERVO,
  "C:\\ts\\servo\\target\\debug\\servoshell.exe",
  "C:\\ts\\servo\\target\\release\\servoshell.exe",
].filter(Boolean);
const servo = candidates.find((candidate) => existsSync(candidate));

if (!servo) {
  throw new Error("Servo was not found; set TURING_SERVO to a servoshell executable");
}
if (!existsSync(html)) {
  throw new Error("Nova shell is not built; run npm run check first");
}

const base = `http://127.0.0.1:${port}`;
const page = `${pathToFileURL(html).href}?turing_engine_bridge=1`;
const child = spawn(servo, ["--webdriver", String(port), "-z", "--window-size", "1440x900", page], {
  cwd: here,
  stdio: ["ignore", "pipe", "ignore"],
  windowsHide: true,
});
child.stdout.on("data", () => {});
let sessionId;

async function request(path, options = {}) {
  const requestBody = options.body || "";
  const text = await new Promise((resolvePromise, reject) => {
    const request = httpRequest(
      {
        hostname: "127.0.0.1",
        port,
        path,
        method: options.method || "GET",
        agent: false,
        headers: {
          "content-type": "application/json",
          ...(requestBody ? { "content-length": Buffer.byteLength(requestBody) } : {}),
          ...(options.headers || {}),
        },
      },
      (response) => {
        let responseText = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => { responseText += chunk; });
        response.on("end", () => resolvePromise({ statusCode: response.statusCode || 0, text: responseText }));
      },
    );
    request.on("error", (error) => reject(new Error(`Servo request ${path} failed: ${error.message}`)));
    request.end(requestBody);
  });
  let body;
  try {
    body = text.text ? JSON.parse(text.text) : {};
  } catch {
    throw new Error(`Servo returned non-JSON for ${path}: ${text.text.slice(0, 200)}`);
  }
  if (text.statusCode < 200 || text.statusCode >= 300 || body.value?.error) {
    throw new Error(`Servo WebDriver ${path} failed: ${text.text.slice(0, 500)}`);
  }
  return body.value;
}

async function waitForServo() {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    try {
      const status = await request("/status", { method: "GET" });
      if (status.ready) return;
    } catch {
      // Servo needs a short startup window before its WebDriver endpoint binds.
    }
    await new Promise((resolvePromise) => setTimeout(resolvePromise, 250));
  }
  throw new Error("Servo WebDriver did not become ready");
}

async function execute(script) {
  return request(`/session/${sessionId}/execute/sync`, {
    method: "POST",
    body: JSON.stringify({ script, args: [] }),
  });
}

const sleep = (milliseconds) => new Promise((resolvePromise) => setTimeout(resolvePromise, milliseconds));

async function clickSelector(selector, label) {
  await execute(`const target = document.querySelector(${JSON.stringify(selector)});
    if (!target) throw new Error(${JSON.stringify(`${label} was not rendered`)});
    target.click();
    return true;`);
  await sleep(250);
}

async function clickText(selector, text, label) {
  await execute(`const target = [...document.querySelectorAll(${JSON.stringify(selector)})]
    .find((element) => element.textContent.trim().includes(${JSON.stringify(text)}));
    if (!target) throw new Error(${JSON.stringify(`${label} was not rendered`)});
    target.click();
    return true;`);
  await sleep(250);
}

async function clickTitle(fragment, label) {
  await execute(`const target = [...document.querySelectorAll('button')]
    .find((element) => (element.title || '').toLowerCase().includes(${JSON.stringify(fragment.toLowerCase())}));
    if (!target) throw new Error(${JSON.stringify(`${label} was not rendered`)});
    target.click();
    return true;`);
  await sleep(250);
}

async function waitForNovaMount() {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    try {
      if (await execute("return Boolean(document.querySelector('.stage.nova'));")) return;
    } catch {
      // The document can still be transitioning while Servo finishes loading.
    }
    await sleep(250);
  }
  throw new Error("Nova JSX root did not mount in Servo");
}

try {
  await waitForServo();
  const session = await request("/session", {
    method: "POST",
    body: JSON.stringify({ capabilities: { alwaysMatch: { browserName: "servo" } } }),
  });
  sessionId = session.sessionId;
  await waitForNovaMount();

  const viewport = await execute(`return {
    root: Boolean(document.querySelector('#root')),
    stage: Boolean(document.querySelector('.stage')),
    nova: Boolean(document.querySelector('.nova')),
    outerCanvas: Boolean(document.querySelector('.canvas, .holder, .zbar, .zexit')),
    viewport: [window.innerWidth, window.innerHeight],
  };`);
  if (!viewport.root || !viewport.stage || !viewport.nova || viewport.outerCanvas) {
    throw new Error(`Nova viewport assertion failed: ${JSON.stringify(viewport)}`);
  }

  await execute("document.querySelector('.ttab.on').click(); return true;");
  await sleep(350);
  const hasInput = await execute("return Boolean(document.querySelector('.cmd-in input'));");
  if (!hasInput) throw new Error("Command palette input was not rendered");
  await execute(`const input = document.querySelector('.cmd-in input');
    input.focus();
    input.value = 'example.com';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return input.value;`);
  await sleep(250);
  await execute(`window.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Enter', code: 'Enter', keyCode: 13, which: 13,
      bubbles: true, cancelable: true,
    }));`);
  await sleep(700);

  // Exercise the major shell surfaces through their rendered controls. These
  // are deliberately DOM interactions, not direct adapter calls.
  await clickSelector("button.newtab", "new-tab control");
  await clickSelector("button.avatar", "profile control");
  await clickText("button.mitem", "Settings", "settings menu item");
  const settingsInput = await execute("return Boolean(document.querySelector('.pnav-search input'));");
  if (!settingsInput) throw new Error("Settings search input was not rendered");
  await execute(`const input = document.querySelector('.pnav-search input');
    input.focus();
    input.value = 'appearance';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return input.value;`);
  await sleep(250);
  await clickText("a", "Appearance", "appearance settings navigation");
  await clickText("button", "Left", "left tab-position control");
  await clickTitle("sidebar", "sidebar control");
  await clickSelector("button.site", "toolbar address control");
  await clickText("button.qa", "Reader", "reader command");
  await clickSelector("button.site", "toolbar address control");
  await clickText("button.qa", "Split", "split command");
  await clickSelector(".vtab.on button.xc", "active-tab close control");
  await sleep(450);

  const snapshot = await execute("return window.__TURING_ENGINE__.snapshot();");
  const types = snapshot.commands.map((command) => command.type);
  for (const required of [
    "ui.control.click",
    "ui.control.input",
    "ui.control.change",
    "navigation.navigate",
    "tabs.create",
    "shell.sidebar.toggle",
    "shell.view.open",
    "view.reader.toggle",
    "view.split.toggle",
    "tabs.close.request",
  ]) {
    if (!types.includes(required)) {
      throw new Error(`Missing engine command ${required}: ${JSON.stringify(types)}`);
    }
  }
  console.log(`Servo verification passed: viewport=${viewport.viewport.join("x")} commands=${types.join(",")}`);
} finally {
  if (sessionId) {
    try {
      await request(`/session/${sessionId}`, { method: "DELETE" });
    } catch {
      // The browser may already be exiting during a failed verification.
    }
  }
  child.kill();
}
