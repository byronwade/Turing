import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const html = resolve(here, "dist/index.html");
const configured = process.env.TURING_SERVO;
const candidates = [
  configured,
  "C:\\ts\\servo\\target\\debug\\servoshell.exe",
  "C:\\ts\\servo\\target\\release\\servoshell.exe",
].filter(Boolean);
const servo = candidates.find((candidate) => existsSync(candidate));

if (!servo) {
  throw new Error(
    "Servo was not found; set TURING_SERVO to an executable servoshell path",
  );
}

if (!existsSync(html)) {
  throw new Error("Nova shell is not built; run npm run build first");
}

const child = spawn(servo, [pathToFileURL(html).href], {
  cwd: here,
  stdio: "inherit",
  windowsHide: false,
});

child.on("error", (error) => {
  throw error;
});

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
  } else {
    process.exit(code ?? 1);
  }
});
