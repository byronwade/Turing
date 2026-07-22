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

async function runCommand(label) {
  await clickSelector("button.site", `${label} command launcher`);
  await execute(`const input = document.querySelector('.cmd-in input');
    if (!input) throw new Error('Command palette input was not rendered');
    input.focus();
    input.value = ${JSON.stringify(label)};
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return input.value;`);
  await sleep(250);
  await execute(`const target = [...document.querySelectorAll('.cmd-it')]
    .find((element) => element.textContent.trim().startsWith(${JSON.stringify(label)}));
    if (!target) throw new Error(${JSON.stringify(`${label} command was not rendered`)});
    target.click();
    return true;`);
  await sleep(350);
}

async function assertPageText(text, label) {
  const result = await execute(`const page = document.querySelector('.scroll');
    return {
      found: Boolean(page && page.innerText.includes(${JSON.stringify(text)})),
      pageText: page ? page.innerText.slice(0, 240) : '',
      routeText: document.body.innerText.slice(0, 320),
    };`);
  if (!result.found) throw new Error(`${label} was not rendered: ${JSON.stringify(result)}`);
}

async function assertBodyText(text, label) {
  const result = await execute(`return {
    found: document.body.innerText.toLowerCase().includes(${JSON.stringify(text.toLowerCase())}),
    body: document.body.innerText.slice(0, 500),
  };`);
  if (!result.found) throw new Error(`${label} was not rendered: ${JSON.stringify(result)}`);
}

async function dismissOverlay(label) {
  await execute(`window.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Escape', code: 'Escape', keyCode: 27, which: 27,
      bubbles: true, cancelable: true,
    }));`);
  await sleep(250);
  const open = await execute(`return {
    overlays: document.querySelectorAll('.ovl, .sidep, .pop, .tabsrch, .findbar').length,
    shortcuts: Boolean(document.querySelector('[role="dialog"][aria-label="Keyboard shortcuts"]')),
  };`);
  if (open.overlays || open.shortcuts) throw new Error(`${label} did not dismiss: ${JSON.stringify(open)}`);
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
    runtime: window.__TURING_RUNTIME__ ? window.__TURING_RUNTIME__.snapshot() : null,
    viewport: [window.innerWidth, window.innerHeight],
  };`);
  if (!viewport.root || !viewport.stage || !viewport.nova || viewport.outerCanvas
    || !viewport.runtime || !viewport.runtime.mounted
    || viewport.runtime.authoring !== "canonical-nova-jsx"
    || viewport.runtime.renderer !== "preact-compat-on-servo-development"
    || !/^[A-F0-9]{64}$/.test(viewport.runtime.sourceSha256)
    || viewport.runtime.sourceSha256 !== viewport.runtime.tokensSha256) {
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
  await clickText("button.mitem", "History", "history menu item");
  await assertPageText("History", "history page");
  const historyBefore = await execute("return { count: document.querySelectorAll('.hrow').length, first: document.querySelector('.hrow')?.dataset.url || '' };");
  await clickSelector(".hrow .del", "history remove control");
  const historyAfter = await execute("return { count: document.querySelectorAll('.hrow').length, first: document.querySelector('.hrow')?.dataset.url || '' };");
  if (historyAfter.count !== historyBefore.count || historyAfter.first === historyBefore.first) {
    throw new Error(`History removal did not update state: ${JSON.stringify(historyBefore)} -> ${JSON.stringify(historyAfter)}`);
  }
  await clickSelector("button.avatar", "profile control after history");
  await clickText("button.mitem", "Downloads", "downloads menu item");
  await assertPageText("Downloads", "downloads page");
  await clickSelector("button.avatar", "profile control after downloads");
  await clickText("button.mitem", "Extensions", "extensions menu item");
  await assertPageText("Extensions", "extensions page");
  await clickSelector("button.avatar", "profile control after extensions");
  await clickText("button.mitem", "Settings", "settings menu item");
  await assertPageText("Settings", "settings page");
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
  const settingBefore = await execute("return document.querySelector('.sw')?.className || '';");
  await clickSelector(".sw", "settings switch");
  const settingAfter = await execute("return document.querySelector('.sw')?.className || '';");
  if (settingAfter === settingBefore) {
    throw new Error(`Settings switch did not update state: ${settingBefore} -> ${settingAfter}`);
  }
  await clickText("button", "Left", "left tab-position control");

  // Exercise the secondary product surfaces through the same command palette
  // a user uses, keeping the route matrix on the rendered application shell.
  await runCommand("Agent Mode");
  await assertPageText("Agent Mode", "agent mode page");
  await runCommand("Research Canvas");
  await assertBodyText("Research Canvas", "research canvas surface");
  await runCommand("Time Machine");
  await assertPageText("Time Machine", "time machine page");
  await runCommand("Resource Truth Center");
  await assertPageText("Resources", "resource truth center page");
  await runCommand("Import from another browser");
  await assertPageText("Move in · move out", "migration page");
  await runCommand("Agents");
  await assertPageText("Agents", "agents page");
  await runCommand("Workspace & export");
  await assertPageText("Workspace & export", "workspace export settings");

  await clickSelector("button.vnew-top", "return to new-tab shell");
  await runCommand("Reading list");
  await assertBodyText("Reading list", "reading list panel");
  await dismissOverlay("reading list panel");
  await runCommand("Project notes");
  await assertBodyText("Project notes", "project notes panel");
  await dismissOverlay("project notes panel");
  await runCommand("Task manager");
  await assertBodyText("Task manager", "task manager dialog");
  await dismissOverlay("task manager dialog");
  await runCommand("Capture");
  await assertBodyText("Capture", "capture dialog");
  await dismissOverlay("capture dialog");
  await runCommand("Focus session");
  await assertBodyText("Focus session", "focus session dialog");
  await dismissOverlay("focus session dialog");
  await runCommand("Site controls");
  await assertBodyText("Site controls", "site controls popover");
  await dismissOverlay("site controls popover");
  await runCommand("Keyboard shortcuts");
  await assertBodyText("Keyboard shortcuts", "keyboard shortcuts dialog");
  await dismissOverlay("keyboard shortcuts dialog");
  await runCommand("Developer");
  await assertPageText("Developer", "developer settings page");
  await clickSelector(".sw", "developer mode switch");
  await runCommand("DevTools");
  await assertBodyText("Elements", "DevTools elements panel");
  await dismissOverlay("DevTools panel");
  await clickTitle("sidebar", "sidebar control");
  await clickSelector("button.site", "toolbar address control");
  await clickText("button.qa", "Reader", "reader command");
  await clickSelector("button.site", "toolbar address control");
  await clickText("button.qa", "Split", "split command");
  await clickTitle("Ask Turing", "Ask Turing control");
  await execute(`if (!document.querySelector('.ai-htitle')) throw new Error('Ask Turing panel was not rendered');`);
  await clickSelector("button.ai-hbtn[title^='Close']", "Ask Turing close control");
  await clickSelector(".vtab.on button.xc", "active-tab close control");
  await sleep(450);

  const rejected = await execute(`const before = window.__TURING_ENGINE__.snapshot();
    const unknown = window.__TURING_ENGINE__.dispatch({
      version: 1, type: 'unknown.command', payload: {},
    });
    const oversized = window.__TURING_ENGINE__.dispatch({
      version: 1, type: 'tabs.create', payload: { value: 'x'.repeat(65537) },
    });
    const after = window.__TURING_ENGINE__.snapshot();
    return {
      unknown,
      oversized,
      commandDelta: after.commands.length - before.commands.length,
      rejectedDelta: after.rejectedCommands - before.rejectedCommands,
    };`);
  if (rejected.unknown !== false || rejected.oversized !== false
    || rejected.commandDelta !== 0 || rejected.rejectedDelta !== 2) {
    throw new Error(`Adapter rejection assertion failed: ${JSON.stringify(rejected)}`);
  }

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
    "settings.toggle",
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
