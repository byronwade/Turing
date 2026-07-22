// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use std::env;
use std::process::ExitCode;

use turing_build_info::{BuildIdentity, Maturity};
use turing_ipc::{BoundedQueue, ControlEnvelope, MessageKind, QueueClass};
use turing_kernel::{ProcessRegistry, ProcessRole};
use turing_types::{
    ChannelId, DocumentEpoch, OperationId, ProcessId, ProfileId, SequenceNumber, SpaceId, TabId,
    ViewId, WindowId,
};
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
        page_surfaces: Vec::new(),
    }
    .validate()?;

    let mut registry = ProcessRegistry::new(ProcessId::new(1)?);
    let kernel = registry.kernel();
    let renderer = registry.launch(kernel, ProcessId::new(2)?, ProcessRole::Renderer)?;
    let channel = ChannelId::new(1)?;
    registry.register_channel(kernel, channel, renderer, kernel)?;
    let message = ControlEnvelope::new(
        MessageKind::NavigationIntent,
        renderer,
        kernel,
        channel,
        SequenceNumber::new(1)?,
        OperationId::new(1)?,
        Some(DocumentEpoch::new(1)?),
        128,
        "about:blank",
    )?;
    let mut queue = BoundedQueue::new(QueueClass::Control);
    queue.try_push(message).map_err(|error| {
        std::io::Error::other(format!(
            "control queue rejected message: {:?}",
            error.kind()
        ))
    })?;
    let message = queue
        .pop_front()
        .ok_or_else(|| std::io::Error::other("control queue lost its message"))?;
    let route = registry.authorize(&message)?;
    assert_eq!(route.sender_role(), ProcessRole::Renderer);
    assert_eq!(route.receiver_role(), ProcessRole::BrowserKernel);

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
            println!("Turing M0 shell and kernel laboratory");
            println!(
                "Typed process identity, generated IPC policy, and bounded queues exist; no native UI or web runtime exists yet."
            );
            println!("Run with --self-test to validate the M0 control-plane contracts.");
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
