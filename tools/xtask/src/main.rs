// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use std::env;
use std::ffi::OsStr;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

const REQUIRED_RUSTC: &str = "rustc 1.97.1";

fn repository_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(2)
        .expect("xtask is located at tools/xtask")
        .to_path_buf()
}

fn output(program: &str, arguments: &[&str]) -> Result<String, String> {
    let result = Command::new(program)
        .args(arguments)
        .output()
        .map_err(|error| format!("failed to execute {program}: {error}"))?;

    if !result.status.success() {
        let stderr = String::from_utf8_lossy(&result.stderr);
        return Err(format!(
            "{program} {} failed: {}",
            arguments.join(" "),
            stderr.trim()
        ));
    }

    Ok(String::from_utf8_lossy(&result.stdout).trim().to_owned())
}

fn command<I, S>(root: &Path, program: &str, arguments: I) -> Result<(), String>
where
    I: IntoIterator<Item = S>,
    S: AsRef<OsStr>,
{
    let status = Command::new(program)
        .current_dir(root)
        .args(arguments)
        .status()
        .map_err(|error| format!("failed to execute {program}: {error}"))?;

    if status.success() {
        Ok(())
    } else {
        Err(format!("{program} exited with {status}"))
    }
}

fn doctor(require_exact_toolchain: bool) -> Result<(), String> {
    let checks = [
        ("rustc", vec!["--version"]),
        ("cargo", vec!["--version"]),
        ("rustfmt", vec!["--version"]),
        ("cargo", vec!["clippy", "--version"]),
        ("python3", vec!["--version"]),
        ("git", vec!["--version"]),
    ];

    for (program, arguments) in checks {
        let value = output(program, &arguments)?;
        println!("{program}: {value}");
        if require_exact_toolchain && program == "rustc" && !value.starts_with(REQUIRED_RUSTC) {
            return Err(format!(
                "expected {REQUIRED_RUSTC}; rust-toolchain.toml must be honored"
            ));
        }
    }

    let root = repository_root();
    for required in [
        "Cargo.toml",
        "Cargo.lock",
        "rust-toolchain.toml",
        "docs/README.md",
        "docs/project-buildout/implementation-plan/README.md",
        "tools/validate_implementation_plan.py",
        "security/dependencies.json",
        "security/unsafe-code.json",
    ] {
        if !root.join(required).is_file() {
            return Err(format!("missing required repository file: {required}"));
        }
    }

    println!("repository: {}", root.display());
    println!("doctor: ready for contained M0 development");
    Ok(())
}

fn bootstrap() -> Result<(), String> {
    println!("Turing bootstrap is intentionally non-installing during M0.");
    println!("rustup will honor rust-toolchain.toml when Cargo is invoked.");
    doctor(false)?;
    println!("next: cargo run -p xtask -- check");
    Ok(())
}

fn check() -> Result<(), String> {
    let root = repository_root();
    command(&root, "python3", ["-B", "tools/validate_blueprint.py"])?;
    command(
        &root,
        "python3",
        ["-B", "tools/validate_build_foundation.py"],
    )?;
    command(
        &root,
        "python3",
        ["-B", "tools/validate_implementation_plan.py"],
    )?;
    command(&root, "cargo", ["fmt", "--all", "--", "--check"])?;
    command(
        &root,
        "cargo",
        [
            "clippy",
            "--workspace",
            "--all-targets",
            "--all-features",
            "--locked",
            "--",
            "-D",
            "warnings",
        ],
    )?;
    command(
        &root,
        "cargo",
        ["test", "--workspace", "--all-targets", "--locked"],
    )?;
    command(
        &root,
        "cargo",
        ["run", "--locked", "-p", "turing-shell", "--", "--self-test"],
    )?;
    command(
        &root,
        "cargo",
        [
            "run",
            "--locked",
            "-p",
            "turing-architecture-prototype",
            "--quiet",
        ],
    )?;

    println!("check: all M0 repository and implementation-plan checks passed");
    Ok(())
}

fn run() -> Result<(), String> {
    let mut arguments = env::args().skip(1);
    let subcommand = arguments.next().unwrap_or_else(|| "help".to_owned());

    match subcommand.as_str() {
        "bootstrap" => bootstrap(),
        "doctor" => doctor(arguments.any(|argument| argument == "--ci")),
        "check" => check(),
        "help" | "--help" | "-h" => {
            println!("usage: cargo run -p xtask -- <bootstrap|doctor [--ci]|check>");
            Ok(())
        }
        other => Err(format!("unknown xtask command: {other}")),
    }
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("xtask: {error}");
            ExitCode::FAILURE
        }
    }
}
