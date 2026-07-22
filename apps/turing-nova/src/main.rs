//! Native desktop entry point for the interactive Nova shell prototype.
//!
//! The host owns local build orchestration and Servo process discovery. The
//! Nova source remains the visual and component source of truth; this binary
//! deliberately does not recreate its UI in Rust. The long-term replacement
//! for the child-process boundary is a reviewed Servo/Turing embedding host.

#![forbid(unsafe_code)]

use std::env;
use std::fmt::Write as _;
use std::io::{BufRead, BufReader, Read};
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::thread;

const PACKAGE_RELATIVE: &str = "apps/nova-shell";
const ENGINE_COMMAND_PREFIX: &str = "TURING_ENGINE_COMMAND\t";
const RUNTIME_READY_PREFIX: &str = "TURING_RUNTIME_READY\t";
const MAX_ENGINE_RECORD_BYTES: usize = 64 * 1024;

/// Typed command kinds observed at the development Servo boundary.
///
/// The host deliberately classifies intent without trusting page payloads as
/// browser authority. A future IPC receiver can attach identity and policy
/// validation before translating a command into `turing-ui-model` state.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum EngineCommandKind {
    NavigationHistory,
    NavigationNavigate,
    NavigationCopyUrl,
    ShellViewOpen,
    ShellSidebarToggle,
    TabsCloseRequest,
    TabsCreate,
    TabsActivate,
    ViewReaderToggle,
    ViewSplitToggle,
    SettingsToggle,
    UiControlClick,
    UiControlPointerdown,
    UiControlInput,
    UiControlChange,
    UiKeyboard,
}

impl EngineCommandKind {
    fn parse(value: &str) -> Option<Self> {
        Some(match value {
            "navigation.history" => Self::NavigationHistory,
            "navigation.navigate" => Self::NavigationNavigate,
            "navigation.copy-url" => Self::NavigationCopyUrl,
            "shell.view.open" => Self::ShellViewOpen,
            "shell.sidebar.toggle" => Self::ShellSidebarToggle,
            "tabs.close.request" => Self::TabsCloseRequest,
            "tabs.create" => Self::TabsCreate,
            "tabs.activate" => Self::TabsActivate,
            "view.reader.toggle" => Self::ViewReaderToggle,
            "view.split.toggle" => Self::ViewSplitToggle,
            "settings.toggle" => Self::SettingsToggle,
            "ui.control.click" => Self::UiControlClick,
            "ui.control.pointerdown" => Self::UiControlPointerdown,
            "ui.control.input" => Self::UiControlInput,
            "ui.control.change" => Self::UiControlChange,
            "ui.keyboard" => Self::UiKeyboard,
            _ => return None,
        })
    }

    const fn as_str(self) -> &'static str {
        match self {
            Self::NavigationHistory => "navigation.history",
            Self::NavigationNavigate => "navigation.navigate",
            Self::NavigationCopyUrl => "navigation.copy-url",
            Self::ShellViewOpen => "shell.view.open",
            Self::ShellSidebarToggle => "shell.sidebar.toggle",
            Self::TabsCloseRequest => "tabs.close.request",
            Self::TabsCreate => "tabs.create",
            Self::TabsActivate => "tabs.activate",
            Self::ViewReaderToggle => "view.reader.toggle",
            Self::ViewSplitToggle => "view.split.toggle",
            Self::SettingsToggle => "settings.toggle",
            Self::UiControlClick => "ui.control.click",
            Self::UiControlPointerdown => "ui.control.pointerdown",
            Self::UiControlInput => "ui.control.input",
            Self::UiControlChange => "ui.control.change",
            Self::UiKeyboard => "ui.keyboard",
        }
    }
}

fn repository_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..")
}

fn package_root(root: &Path) -> PathBuf {
    root.join(PACKAGE_RELATIVE)
}

fn npm_executable() -> &'static str {
    if cfg!(windows) { "npm.cmd" } else { "npm" }
}

fn run_build(root: &Path, package: &Path) -> Result<(), String> {
    let status = Command::new(npm_executable())
        .args(["run", "check", "--prefix"])
        .arg(package)
        .current_dir(root)
        .status()
        .map_err(|error| format!("cannot start npm: {error}"))?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("Nova package check failed with {status}"))
    }
}

fn find_servo() -> Result<PathBuf, String> {
    let mut candidates = Vec::new();
    if let Some(configured) = env::var_os("TURING_SERVO")
        && !configured.is_empty()
    {
        candidates.push(PathBuf::from(configured));
    }
    if cfg!(windows) {
        candidates.push(PathBuf::from(r"C:\ts\servo\target\debug\servoshell.exe"));
        candidates.push(PathBuf::from(r"C:\ts\servo\target\release\servoshell.exe"));
    } else {
        candidates.push(PathBuf::from("/usr/local/bin/servoshell"));
        candidates.push(PathBuf::from("/usr/bin/servoshell"));
    }

    candidates
        .into_iter()
        .find(|candidate| candidate.is_file())
        .ok_or_else(|| {
            "Servo was not found; set TURING_SERVO to a servoshell executable".to_owned()
        })
}

fn file_url(path: &Path) -> Result<String, String> {
    let absolute = path
        .canonicalize()
        .map_err(|error| format!("cannot resolve {}: {error}", path.display()))?;
    let mut normalized = absolute.to_string_lossy().replace('\\', "/");
    // Windows canonicalization may return an extended path such as
    // `//?/C:/...`; file URLs need the ordinary drive-path form.
    if cfg!(windows)
        && let Some(stripped) = normalized.strip_prefix("//?/")
    {
        normalized = stripped.to_owned();
    }
    let mut url = if cfg!(windows) {
        String::from("file:///")
    } else {
        String::from("file://")
    };

    for byte in normalized.bytes() {
        if byte.is_ascii_alphanumeric() || matches!(byte, b'/' | b':' | b'-' | b'_' | b'.' | b'~') {
            url.push(byte as char);
        } else {
            write!(&mut url, "%{byte:02X}").map_err(|_| "cannot encode file URL".to_owned())?;
        }
    }
    Ok(url)
}

#[derive(Debug, Eq, PartialEq)]
struct EngineRecord {
    version: u16,
    kind: EngineCommandKind,
    payload_bytes: usize,
}

#[derive(Debug, Eq, PartialEq)]
struct RuntimeRecord {
    version: u16,
    source_sha256: String,
    tokens_sha256: String,
}

/// Bounded host-side observation state for one development launch.
#[derive(Debug, Default, Eq, PartialEq)]
struct BridgeState {
    runtime_ready: bool,
    accepted_commands: u64,
    last_command: Option<EngineCommandKind>,
    recent_commands: Vec<EngineCommandKind>,
}

fn valid_sha256(value: &str) -> bool {
    value.len() == 64 && value.bytes().all(|byte| byte.is_ascii_hexdigit())
}

fn parse_runtime_record(line: &str) -> Option<RuntimeRecord> {
    let record = line
        .find(RUNTIME_READY_PREFIX)
        .map(|index| &line[index..])?;
    let fields: Vec<&str> = record[RUNTIME_READY_PREFIX.len()..].split('\t').collect();
    if fields.len() != 3 {
        return None;
    }
    let version = fields[0].parse().ok()?;
    if version != 1
        || !valid_sha256(fields[1])
        || !valid_sha256(fields[2])
        || !fields[1].eq_ignore_ascii_case(fields[2])
    {
        return None;
    }
    Some(RuntimeRecord {
        version,
        source_sha256: fields[1].to_ascii_uppercase(),
        tokens_sha256: fields[2].to_ascii_uppercase(),
    })
}

impl BridgeState {
    fn observe(&mut self, record: &EngineRecord) {
        self.accepted_commands += 1;
        self.last_command = Some(record.kind);
        self.recent_commands.push(record.kind);
        if self.recent_commands.len() > 128 {
            self.recent_commands.remove(0);
        }
    }
}

fn parse_engine_record(line: &str) -> Option<EngineRecord> {
    let record = line
        .find(ENGINE_COMMAND_PREFIX)
        .map(|index| &line[index..])?;
    let fields: Vec<&str> = record[ENGINE_COMMAND_PREFIX.len()..]
        .splitn(3, '\t')
        .collect();
    if fields.len() != 3 {
        return None;
    }
    let version = fields[0].parse().ok()?;
    let kind = EngineCommandKind::parse(fields[1]);
    if version != 1 {
        return None;
    }
    let kind = kind?;
    let payload_bytes = fields[2].len();
    (payload_bytes <= MAX_ENGINE_RECORD_BYTES).then_some(EngineRecord {
        version,
        kind,
        payload_bytes,
    })
}

fn observe_engine_output<R: Read + Send + 'static>(
    output: R,
    state: Arc<Mutex<BridgeState>>,
) -> thread::JoinHandle<()> {
    thread::spawn(move || {
        let reader = BufReader::new(output);
        for line in reader.lines() {
            let Ok(line) = line else { break };
            if let Some(record) = parse_runtime_record(&line) {
                if let Ok(mut bridge) = state.lock() {
                    bridge.runtime_ready = true;
                }
                println!(
                    "turing-nova: runtime ready v{} source_sha256={} tokens_sha256={}",
                    record.version, record.source_sha256, record.tokens_sha256
                );
            } else if let Some(record) = parse_engine_record(&line) {
                let ready = state
                    .lock()
                    .map(|bridge| bridge.runtime_ready)
                    .unwrap_or(false);
                if !ready {
                    continue;
                }
                if let Ok(mut bridge) = state.lock() {
                    bridge.observe(&record);
                }
                println!(
                    "turing-nova: engine command v{} type={} payload_bytes={}",
                    record.version,
                    record.kind.as_str(),
                    record.payload_bytes
                );
            }
        }
    })
}

fn launch_servo(servo: &Path, url: String) -> Result<std::process::ExitStatus, String> {
    let mut child: Child = Command::new(servo)
        .arg(url)
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit())
        .spawn()
        .map_err(|error| format!("cannot launch Servo: {error}"))?;
    let output = child
        .stdout
        .take()
        .ok_or_else(|| "Servo stdout pipe was unavailable".to_owned())?;
    let bridge = Arc::new(Mutex::new(BridgeState::default()));
    let observer = observe_engine_output(output, Arc::clone(&bridge));
    let status = child
        .wait()
        .map_err(|error| format!("cannot wait for Servo: {error}"))?;
    let _ = observer.join();
    if let Ok(state) = bridge.lock() {
        println!(
            "turing-nova: runtime_ready={} observed_commands={} recent_commands={}",
            state.runtime_ready,
            state.accepted_commands,
            state.recent_commands.len()
        );
    }
    Ok(status)
}

fn usage() {
    println!(
        "turing-nova\n\nUsage: cargo run -p turing-nova [-- --no-build]\n\n\
         Builds the Nova JSX bundle, then opens it in local Servo.\n\
         Set TURING_SERVO to override the Servo executable path.\n\
         --no-build  launch the existing dist bundle without npm."
    );
}

fn run() -> Result<(), String> {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.iter().any(|arg| arg == "--help" || arg == "-h") {
        usage();
        return Ok(());
    }
    let no_build = args.iter().any(|arg| arg == "--no-build");
    if args.iter().any(|arg| arg != "--no-build") {
        return Err("unknown argument; use --help for usage".to_owned());
    }

    let root = repository_root();
    let package = package_root(&root);
    let html = package.join("dist/index.html");
    if !no_build {
        run_build(&root, &package)?;
    }
    if !html.is_file() {
        return Err(format!(
            "Nova bundle is missing at {}; run without --no-build or build it with npm",
            html.display()
        ));
    }

    let servo = find_servo()?;
    let mut url = file_url(&html)?;
    url.push_str("?turing_engine_bridge=1");
    println!("turing-nova: launching {}", servo.display());
    println!("turing-nova: loading {url}");
    let status = launch_servo(&servo, url)?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("Servo exited with {status}"))
    }
}

fn main() {
    if let Err(error) = run() {
        eprintln!("turing-nova: {error}");
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::file_url;
    use super::{BridgeState, EngineCommandKind, EngineRecord};
    use std::path::Path;

    #[test]
    fn file_url_uses_a_local_file_scheme() {
        let url = file_url(Path::new("Cargo.toml")).expect("workspace file resolves");
        assert!(url.starts_with("file://"));
        assert!(url.ends_with("Cargo.toml"));
        assert!(!url.contains('\\'));
        assert!(!url.contains("%3F"));
    }

    #[test]
    fn engine_record_accepts_known_types_without_exposing_payload() {
        let record = super::parse_engine_record(
            "prefix TURING_ENGINE_COMMAND\t1\tnavigation.navigate\t{\"url\":\"secret\"}",
        )
        .expect("known command is accepted");
        assert_eq!(record.version, 1);
        assert_eq!(record.kind, EngineCommandKind::NavigationNavigate);
        assert!(record.payload_bytes > 0);
    }

    #[test]
    fn engine_record_rejects_unknown_or_wrong_version() {
        assert!(super::parse_engine_record("TURING_ENGINE_COMMAND\t2\ttabs.create\t{}").is_none());
        assert!(super::parse_engine_record("TURING_ENGINE_COMMAND\t1\tsecret.read\t{}").is_none());
    }

    #[test]
    fn bridge_state_keeps_only_bounded_typed_history() {
        let record = EngineRecord {
            version: 1,
            kind: EngineCommandKind::TabsCreate,
            payload_bytes: 2,
        };
        let mut state = BridgeState::default();
        for _ in 0..130 {
            state.observe(&record);
        }
        assert_eq!(state.accepted_commands, 130);
        assert_eq!(state.last_command, Some(EngineCommandKind::TabsCreate));
        assert_eq!(state.recent_commands.len(), 128);
    }

    #[test]
    fn runtime_record_requires_matching_sha256_provenance() {
        let hash = "C812F5545C8EF4B6FEB4E488CCA091E96787042493623B57CB7AAEE0366B50D5";
        let line = format!("prefix TURING_RUNTIME_READY\t1\t{hash}\t{hash}");
        let record = super::parse_runtime_record(&line).expect("matching runtime record");
        assert_eq!(record.version, 1);
        assert_eq!(record.source_sha256, hash);
        assert!(
            super::parse_runtime_record(&format!(
                "TURING_RUNTIME_READY\t1\t{hash}\t{}",
                "0".repeat(64)
            ))
            .is_none()
        );
    }
}
