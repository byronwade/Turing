//! Native desktop entry point for the interactive Nova shell prototype.
//!
//! The host owns local build orchestration and Servo process discovery. The
//! Nova source remains the visual and component source of truth; this binary
//! deliberately does not recreate its UI in Rust. The long-term replacement
//! for the child-process boundary is a reviewed Servo/Turing embedding host.

#![forbid(unsafe_code)]

use std::env;
use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::process::Command;

const PACKAGE_RELATIVE: &str = "apps/nova-shell";

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
    let url = file_url(&html)?;
    println!("turing-nova: launching {}", servo.display());
    println!("turing-nova: loading {url}");
    let status = Command::new(&servo)
        .arg(url)
        .status()
        .map_err(|error| format!("cannot launch Servo: {error}"))?;
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
    use std::path::Path;

    #[test]
    fn file_url_uses_a_local_file_scheme() {
        let url = file_url(Path::new("Cargo.toml")).expect("workspace file resolves");
        assert!(url.starts_with("file://"));
        assert!(url.ends_with("Cargo.toml"));
        assert!(!url.contains('\\'));
        assert!(!url.contains("%3F"));
    }
}
