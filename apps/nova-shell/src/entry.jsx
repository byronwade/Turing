import { h, render } from "preact";
import Nova from "../../../docs/ui-runtime/design-lab/turing-nova-design-source.jsx";

const commandHistory = [];
const ENGINE_CONSOLE_PREFIX = "TURING_ENGINE_COMMAND";
const MAX_ENGINE_PAYLOAD_BYTES = 64 * 1024;
const SUPPORTED_ENGINE_COMMANDS = new Set([
  "navigation.history",
  "navigation.navigate",
  "navigation.copy-url",
  "shell.view.open",
  "shell.sidebar.toggle",
  "tabs.close.request",
  "tabs.create",
  "tabs.activate",
  "view.reader.toggle",
  "view.split.toggle",
  "ui.control.click",
  "ui.control.pointerdown",
  "ui.control.input",
  "ui.control.change",
  "ui.keyboard",
]);
const engineState = {
  version: 1,
  lastCommand: null,
  rejectedCommands: 0,
};
const bridgeEnabled = (() => {
  try {
    return new URL(window.location.href).searchParams.get("turing_engine_bridge") === "1";
  } catch {
    return false;
  }
})();

// This is the browser-facing adapter boundary. The prototype keeps the
// engine side in-process, but all source interactions cross this typed object
// so a Rust/Servo host can replace it without changing Nova components.
window.__TURING_ENGINE__ = {
  version: 1,
  dispatch(command) {
    if (!command || command.version !== 1 || typeof command.type !== "string"
      || !SUPPORTED_ENGINE_COMMANDS.has(command.type)) {
      engineState.rejectedCommands += 1;
      return false;
    }
    let serializedPayload;
    try {
      serializedPayload = JSON.stringify(command.payload ?? {});
    } catch {
      engineState.rejectedCommands += 1;
      return false;
    }
    if (serializedPayload === undefined
      || new TextEncoder().encode(serializedPayload).byteLength > MAX_ENGINE_PAYLOAD_BYTES) {
      engineState.rejectedCommands += 1;
      return false;
    }
    engineState.lastCommand = command;
    commandHistory.push(command);
    if (commandHistory.length > 128) commandHistory.shift();
    document.documentElement.dataset.turingLastCommand = command.type;
    if (bridgeEnabled && typeof console !== "undefined" && typeof console.log === "function") {
      // The native host observes the type and payload size only. Raw payloads
      // stay inside the page adapter so typed input is not written to stdout.
      console.log([ENGINE_CONSOLE_PREFIX, command.version, command.type, serializedPayload].join("\t"));
    }
    return true;
  },
  snapshot() {
    return {
      ...engineState,
      supportedTypes: [...SUPPORTED_ENGINE_COMMANDS],
      commands: commandHistory.slice(),
    };
  },
};

window.addEventListener("keydown", (event) => {
  window.__TURING_ENGINE__.dispatch({
    version: 1,
    type: "ui.keyboard",
    payload: {
      key: event.key,
      code: event.code,
      ctrl: event.ctrlKey,
      meta: event.metaKey,
      shift: event.shiftKey,
      alt: event.altKey,
    },
  });
});

const root = document.getElementById("root");

if (!root) {
  throw new Error("Nova shell mount point is missing");
}

render(h(Nova, null), root);
