import { h, render } from "preact";
import Nova from "../../../docs/ui-runtime/design-lab/turing-nova-design-source.jsx";

const commandHistory = [];
const engineState = {
  version: 1,
  lastCommand: null,
};

// This is the browser-facing adapter boundary. The prototype keeps the
// engine side in-process, but all source interactions cross this typed object
// so a Rust/Servo host can replace it without changing Nova components.
window.__TURING_ENGINE__ = {
  version: 1,
  dispatch(command) {
    engineState.lastCommand = command;
    commandHistory.push(command);
    if (commandHistory.length > 128) commandHistory.shift();
    document.documentElement.dataset.turingLastCommand = command.type;
  },
  snapshot() {
    return {
      ...engineState,
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
