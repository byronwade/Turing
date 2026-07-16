// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

mod agent;
mod network;
mod process;
mod render;
mod tabs;

use std::collections::BTreeSet;
use std::error::Error;

use agent::{authorize, ActionKind, AgentAction, AgentGrant};
use network::{CredentialMode, DocumentEpoch, Origin, ProfileId, RequestContext, TopLevelSite};
use process::{Capability, CapabilitySet, MessageEnvelope, ProcessRole};
use render::{RenderPipeline, RenderStage};
use tabs::{ProtectionReason, TabLifecycle, TabState};

fn main() -> Result<(), Box<dyn Error>> {
    let renderer = CapabilitySet::for_role(ProcessRole::Renderer);
    assert!(!renderer.permits(Capability::OpenNetworkSockets));

    let message = MessageEnvelope::bounded(
        1,
        ProcessRole::Renderer,
        ProcessRole::BrowserKernel,
        128,
        4 * 1024,
        "navigation intent",
    )?;

    let mut tab = TabLifecycle::new();
    tab.transition(TabState::Background)?;
    tab.protect(ProtectionReason::UnsavedWork);
    assert!(tab.transition(TabState::Frozen).is_err());
    tab.remove_protection(ProtectionReason::UnsavedWork);
    tab.transition(TabState::Frozen)?;

    let mut pipeline = RenderPipeline::new();
    let first_frame = pipeline.run().map_err(|_| "render epoch overflow")?;
    pipeline.invalidate_from(RenderStage::Layout);
    let relayout = pipeline.run().map_err(|_| "render epoch overflow")?;

    let profile = ProfileId::new("personal")?;
    let epoch = DocumentEpoch::new(12)?;
    let origin = Origin::parse_ascii("https://example.test")?;
    let request = RequestContext::new(
        profile.clone(),
        epoch,
        origin.clone(),
        TopLevelSite::parse_ascii("https://example.test")?,
        "https://example.test/data",
        CredentialMode::SameOrigin,
        "personal|https://example.test",
    )?;

    let grant = AgentGrant {
        principal_id: "agent.local.dev".to_string(),
        profile: profile.clone(),
        allowed_origins: BTreeSet::from([origin.clone()]),
        allowed_actions: BTreeSet::from([ActionKind::Observe, ActionKind::Navigate]),
        expires_at_unix_seconds: 2_000,
        maximum_actions: 20,
    };
    let action = AgentAction {
        principal_id: "agent.local.dev".to_string(),
        profile,
        origin,
        document_epoch: epoch,
        kind: ActionKind::Navigate,
        prior_action_count: 0,
        confirmed: false,
    };
    let decision = authorize(1_000, epoch, &grant, &action);

    println!("Turing architecture prototype");
    println!(
        "IPC: seq={} {:?}->{:?} {} bytes payload={}",
        message.sequence, message.sender, message.receiver, message.encoded_len, message.payload
    );
    println!(
        "Tab: state={:?} transition_epoch={}",
        tab.state(),
        tab.transition_epoch()
    );
    println!("First frame stages: {first_frame:?}");
    println!("Relayout stages: {relayout:?}");
    println!(
        "Request: profile={} epoch={} origin={} top_site={} destination={} partition={} credentials={:?}",
        request.profile.as_str(),
        request.document_epoch.get(),
        request.requesting_origin.as_str(),
        request.top_level_site.as_str(),
        request.destination_url,
        request.network_partition,
        request.credentials
    );
    println!("Agent decision: {decision:?}");

    Ok(())
}
