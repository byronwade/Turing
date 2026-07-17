// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use std::env;
use std::process::ExitCode;

use turing_build_info::{BuildIdentity, Maturity};
use turing_types::{ProfileId, SpaceId, TabId, ViewId, WindowId};
use turing_ui_model::{ShellSnapshot, TabLifecycle, TabSummary};

fn shell_self_test() -> Result<(), Box<dyn std::error::Error>> {
    let tab = TabSummary {
        id: TabId::new(1)?,
        view: ViewId::new(1)?,
        title: "New Tab".to_owned(),
        display_url: "about:blank".to_owned(),
        lifecycle: TabLifecycle::Active,
        protects_unsaved_work: false,
    };

    ShellSnapshot {
        version: 1,
        window: WindowId::new(1)?,
        profile: ProfileId::new(1)?,
        space: SpaceId::new(1)?,
        active_tab: Some(tab.id),
        tabs: vec![tab],
    }
    .validate()?;

    Ok(())
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let identity = BuildIdentity::current();
    let argument = env::args().nth(1);

    match argument.as_deref() {
        Some("--version") => {
            println!(
                "turing-shell {} {:?} {}",
                identity.version,
                identity.maturity,
                identity.source_commit.unwrap_or("unversioned-source")
            );
        }
        Some("--self-test") => {
            shell_self_test()?;
            println!("turing-shell self-test passed");
        }
        Some(flag) => {
            return Err(format!("unsupported argument: {flag}").into());
        }
        None => {
            debug_assert_eq!(identity.maturity, Maturity::Research);
            println!("Turing M0 shell laboratory");
            println!("No native UI, web engine, network, storage, Plug-ins, or AI runtime exists yet.");
            println!("Run with --self-test to validate toolkit-neutral shell contracts.");
        }
    }

    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("turing-shell: {error}");
            ExitCode::FAILURE
        }
    }
}
