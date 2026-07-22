// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use std::collections::BTreeSet;
use std::fmt;

use turing_types::{
    DeviceGeneration, DocumentEpoch, ProfileId, SequenceNumber, SpaceId, SurfaceId, TabId, ViewId,
    WindowId,
};

/// Maximum dimension accepted by the toolkit-neutral surface descriptor.
pub const MAX_SURFACE_DIMENSION: u32 = 16_384;
/// Maximum number of physical pixels described by one surface.
pub const MAX_SURFACE_PIXELS: u64 = 268_435_456;

/// Bounded dimensions for a page surface in logical or physical pixels.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct SurfaceSize {
    /// Width in pixels.
    pub width: u32,
    /// Height in pixels.
    pub height: u32,
}

impl SurfaceSize {
    /// Creates dimensions that fit the resource budget for a single surface.
    pub const fn new(width: u32, height: u32) -> Result<Self, SurfaceSizeError> {
        if width == 0 || height == 0 {
            return Err(SurfaceSizeError::ZeroDimension);
        }
        if width > MAX_SURFACE_DIMENSION || height > MAX_SURFACE_DIMENSION {
            return Err(SurfaceSizeError::DimensionTooLarge);
        }
        if (width as u64) * (height as u64) > MAX_SURFACE_PIXELS {
            return Err(SurfaceSizeError::PixelBudgetExceeded);
        }
        Ok(Self { width, height })
    }
}

/// Failure while constructing bounded surface dimensions.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SurfaceSizeError {
    /// Both dimensions must be non-zero.
    ZeroDimension,
    /// One dimension exceeds the descriptor bound.
    DimensionTooLarge,
    /// The surface exceeds the per-surface pixel budget.
    PixelBudgetExceeded,
}

impl fmt::Display for SurfaceSizeError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::ZeroDimension => "surface dimensions must be non-zero",
            Self::DimensionTooLarge => "surface dimension exceeds the bounded maximum",
            Self::PixelBudgetExceeded => "surface exceeds the bounded pixel budget",
        };
        formatter.write_str(message)
    }
}

impl std::error::Error for SurfaceSizeError {}

/// Color metadata needed by a future compositor without exposing renderer types.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SurfaceColorSpace {
    /// Standard RGB used by the current Nova/Servo development viewport.
    Srgb,
}

/// Alpha semantics for the page content presented into trusted chrome.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SurfaceAlphaMode {
    /// The page surface is fully opaque.
    Opaque,
    /// Color channels are premultiplied by alpha.
    Premultiplied,
}

/// Page content lifecycle visible to the UI model.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PageSurfaceState {
    /// A current frame may be presented.
    Ready,
    /// The renderer or device is being replaced; chrome remains usable.
    Recovering,
}

/// Renderer-neutral page surface metadata.
///
/// This is a development contract, not a renderer handle. It intentionally
/// contains no pixels, process pointers, native GPU handles, or synchronization
/// primitives. A future brokered surface protocol must validate this metadata
/// before presentation and reject stale view, document, or device generations.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PageSurfaceDescriptor {
    /// Stable surface identity issued by the owning browser service.
    pub id: SurfaceId,
    /// View that owns presentation and input routing.
    pub view: ViewId,
    /// Navigation document epoch for stale-frame rejection.
    pub document_epoch: DocumentEpoch,
    /// GPU/software resource generation for device-loss recovery.
    pub device_generation: DeviceGeneration,
    /// CSS/layout-space dimensions.
    pub logical_size: SurfaceSize,
    /// Device-pixel allocation dimensions.
    pub physical_size: SurfaceSize,
    /// Scale factor expressed in thousandths to avoid floating-point state.
    pub scale_factor_milli: u32,
    /// Color interpretation for composition.
    pub color_space: SurfaceColorSpace,
    /// Alpha interpretation for composition.
    pub alpha_mode: SurfaceAlphaMode,
    /// Monotonic frame sequence for stale/replayed frame rejection.
    pub frame_sequence: SequenceNumber,
    /// Current renderer/device recovery state.
    pub state: PageSurfaceState,
}

/// Surface descriptor validation failure.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PageSurfaceError {
    /// Logical or physical dimensions violate the surface resource budget.
    InvalidSize(SurfaceSizeError),
    /// A scale factor below 0.1x or above 64x is outside the bounded contract.
    InvalidScaleFactor(u32),
    /// Physical dimensions do not match logical dimensions and scale metadata.
    MismatchedPhysicalSize {
        expected: SurfaceSize,
        actual: SurfaceSize,
    },
}

impl fmt::Display for PageSurfaceError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidSize(error) => write!(formatter, "invalid surface size: {error}"),
            Self::InvalidScaleFactor(value) => {
                write!(formatter, "invalid surface scale factor {value}/1000")
            }
            Self::MismatchedPhysicalSize { expected, actual } => write!(
                formatter,
                "physical surface size {}x{} does not match expected {}x{}",
                actual.width, actual.height, expected.width, expected.height
            ),
        }
    }
}

impl std::error::Error for PageSurfaceError {}

impl PageSurfaceDescriptor {
    /// Validates scale and physical allocation invariants.
    pub fn validate(&self) -> Result<(), PageSurfaceError> {
        SurfaceSize::new(self.logical_size.width, self.logical_size.height)
            .map_err(PageSurfaceError::InvalidSize)?;
        SurfaceSize::new(self.physical_size.width, self.physical_size.height)
            .map_err(PageSurfaceError::InvalidSize)?;
        if !(100..=64_000).contains(&self.scale_factor_milli) {
            return Err(PageSurfaceError::InvalidScaleFactor(
                self.scale_factor_milli,
            ));
        }

        let scaled = |value: u32| {
            let scaled = (value as u64) * (self.scale_factor_milli as u64);
            scaled.div_ceil(1_000).min(u32::MAX as u64) as u32
        };
        let expected = SurfaceSize::new(
            scaled(self.logical_size.width),
            scaled(self.logical_size.height),
        )
        .map_err(PageSurfaceError::InvalidSize)?;
        if self.physical_size != expected {
            return Err(PageSurfaceError::MismatchedPhysicalSize {
                expected,
                actual: self.physical_size,
            });
        }
        Ok(())
    }
}

/// User-visible lifecycle state of a tab.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum TabLifecycle {
    /// Foreground interactive tab.
    Active,
    /// Background live tab.
    Background,
    /// Execution suspended while restorable state is retained.
    Frozen,
    /// Reload or serialized restoration is required.
    Discarded,
    /// Restoration is in progress.
    Restoring,
}

/// Presentation summary for one tab.
///
/// This intentionally contains no toolkit types, page pointers, credentials, or
/// mutable renderer state.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct TabSummary {
    /// Stable tab identity.
    pub id: TabId,
    /// Page view identity.
    pub view: ViewId,
    /// Display title supplied through trusted sanitization.
    pub title: String,
    /// Display URL supplied through trusted URL formatting.
    pub display_url: String,
    /// Lifecycle state.
    pub lifecycle: TabLifecycle,
    /// Whether unsaved work currently protects this tab from discard.
    pub protects_unsaved_work: bool,
}

/// Immutable presentation state for a browser window.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ShellSnapshot {
    /// Monotonic presentation version.
    pub version: u64,
    /// Window identity.
    pub window: WindowId,
    /// Profile identity.
    pub profile: ProfileId,
    /// Active project Space.
    pub space: SpaceId,
    /// Active tab, when any.
    pub active_tab: Option<TabId>,
    /// Tabs visible to the window.
    pub tabs: Vec<TabSummary>,
    /// Current page surfaces, when a view has renderer content to present.
    pub page_surfaces: Vec<PageSurfaceDescriptor>,
}

/// Validation failure for a shell snapshot.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum SnapshotError {
    /// Snapshot versions begin at one.
    ZeroVersion,
    /// Duplicate tab identity.
    DuplicateTab(TabId),
    /// Active tab does not exist in the snapshot.
    MissingActiveTab(TabId),
    /// A page surface refers to a view not represented by a visible tab.
    MissingSurfaceView(ViewId),
    /// Duplicate surface identity.
    DuplicateSurface(SurfaceId),
    /// More than one page surface targets the same view in one snapshot.
    DuplicateSurfaceView(ViewId),
    /// A page surface violates its bounded metadata contract.
    InvalidSurface(PageSurfaceError),
}

impl fmt::Display for SnapshotError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroVersion => write!(formatter, "shell snapshot version must be non-zero"),
            Self::DuplicateTab(tab) => write!(formatter, "duplicate tab identity {tab}"),
            Self::MissingActiveTab(tab) => write!(formatter, "active tab {tab} is not present"),
            Self::MissingSurfaceView(view) => {
                write!(formatter, "surface view {view} is not present")
            }
            Self::DuplicateSurface(surface) => {
                write!(formatter, "duplicate surface identity {surface}")
            }
            Self::DuplicateSurfaceView(view) => write!(formatter, "duplicate surface view {view}"),
            Self::InvalidSurface(error) => write!(formatter, "invalid page surface: {error}"),
        }
    }
}

impl std::error::Error for SnapshotError {}

impl ShellSnapshot {
    /// Validates identity and version invariants.
    pub fn validate(&self) -> Result<(), SnapshotError> {
        if self.version == 0 {
            return Err(SnapshotError::ZeroVersion);
        }

        let mut ids = BTreeSet::new();
        let mut views = BTreeSet::new();
        for tab in &self.tabs {
            if !ids.insert(tab.id) {
                return Err(SnapshotError::DuplicateTab(tab.id));
            }
            views.insert(tab.view);
        }

        if let Some(active_tab) = self.active_tab
            && !ids.contains(&active_tab)
        {
            return Err(SnapshotError::MissingActiveTab(active_tab));
        }

        let mut surface_ids = BTreeSet::new();
        let mut surface_views = BTreeSet::new();
        for surface in &self.page_surfaces {
            surface.validate().map_err(SnapshotError::InvalidSurface)?;
            if !surface_ids.insert(surface.id) {
                return Err(SnapshotError::DuplicateSurface(surface.id));
            }
            if !views.contains(&surface.view) {
                return Err(SnapshotError::MissingSurfaceView(surface.view));
            }
            if !surface_views.insert(surface.view) {
                return Err(SnapshotError::DuplicateSurfaceView(surface.view));
            }
        }

        Ok(())
    }
}

/// Typed intent emitted by browser chrome.
///
/// The browser kernel or owning service revalidates every command before any
/// privileged or persistent effect occurs.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ShellCommand {
    /// Activate one tab.
    ActivateTab { tab: TabId },
    /// Request closing one tab.
    CloseTab { tab: TabId },
    /// Request navigation in one page view.
    Navigate { view: ViewId, input: String },
    /// Freeze one tab if current protection and policy permit.
    FreezeTab { tab: TabId },
    /// Restore one discarded tab.
    RestoreTab { tab: TabId },
    /// Switch project Space.
    ActivateSpace { space: SpaceId },
    /// Open a new tab. The owning service chooses identifiers and initial
    /// content; chrome only expresses the intent.
    NewTab,
    /// Reload one tab's current content.
    Reload { tab: TabId },
    /// Open the command field focused for typed input, in the context of one
    /// tab when the chrome knows it (the Nova design opens it from the active
    /// tab, which doubles as the address field).
    OpenCommandField { tab: Option<TabId> },
    /// Traverse one entry back in one tab's session history.
    Back { tab: TabId },
    /// Traverse one entry forward in one tab's session history.
    Forward { tab: TabId },
}

#[cfg(test)]
mod tests {
    use super::{
        PageSurfaceDescriptor, PageSurfaceState, ShellSnapshot, SnapshotError, SurfaceAlphaMode,
        SurfaceColorSpace, SurfaceSize, TabLifecycle, TabSummary,
    };
    use turing_types::{
        DeviceGeneration, DocumentEpoch, ProfileId, SequenceNumber, SpaceId, SurfaceId, TabId,
        ViewId, WindowId,
    };

    fn sample_tab(id: u64) -> TabSummary {
        TabSummary {
            id: TabId::new(id).expect("valid tab id"),
            view: ViewId::new(id).expect("valid view id"),
            title: format!("Tab {id}"),
            display_url: "about:blank".to_owned(),
            lifecycle: TabLifecycle::Active,
            protects_unsaved_work: false,
        }
    }

    fn sample_snapshot() -> ShellSnapshot {
        ShellSnapshot {
            version: 1,
            window: WindowId::new(1).expect("valid window id"),
            profile: ProfileId::new(1).expect("valid profile id"),
            space: SpaceId::new(1).expect("valid space id"),
            active_tab: Some(TabId::new(1).expect("valid tab id")),
            tabs: vec![sample_tab(1)],
            page_surfaces: vec![sample_surface(1, 1)],
        }
    }

    fn sample_surface(id: u64, view: u64) -> PageSurfaceDescriptor {
        PageSurfaceDescriptor {
            id: SurfaceId::new(id).expect("valid surface id"),
            view: ViewId::new(view).expect("valid view id"),
            document_epoch: DocumentEpoch::new(1).expect("valid document epoch"),
            device_generation: DeviceGeneration::new(1).expect("valid device generation"),
            logical_size: SurfaceSize::new(1_440, 900).expect("valid logical size"),
            physical_size: SurfaceSize::new(1_440, 900).expect("valid physical size"),
            scale_factor_milli: 1_000,
            color_space: SurfaceColorSpace::Srgb,
            alpha_mode: SurfaceAlphaMode::Opaque,
            frame_sequence: SequenceNumber::new(1).expect("valid frame sequence"),
            state: PageSurfaceState::Ready,
        }
    }

    #[test]
    fn accepts_consistent_snapshot() {
        assert_eq!(sample_snapshot().validate(), Ok(()));
    }

    #[test]
    fn rejects_missing_active_tab() {
        let mut snapshot = sample_snapshot();
        snapshot.active_tab = Some(TabId::new(2).expect("valid tab id"));

        assert_eq!(
            snapshot.validate(),
            Err(SnapshotError::MissingActiveTab(
                TabId::new(2).expect("valid tab id")
            ))
        );
    }

    #[test]
    fn rejects_duplicate_tabs() {
        let mut snapshot = sample_snapshot();
        snapshot.tabs.push(sample_tab(1));

        assert_eq!(
            snapshot.validate(),
            Err(SnapshotError::DuplicateTab(
                TabId::new(1).expect("valid tab id")
            ))
        );
    }

    #[test]
    fn rejects_surface_for_missing_view() {
        let mut snapshot = sample_snapshot();
        snapshot.page_surfaces[0].view = ViewId::new(9).expect("valid view id");

        assert_eq!(
            snapshot.validate(),
            Err(SnapshotError::MissingSurfaceView(
                ViewId::new(9).expect("valid view id")
            ))
        );
    }

    #[test]
    fn rejects_surface_with_mismatched_physical_size() {
        let mut snapshot = sample_snapshot();
        snapshot.page_surfaces[0].physical_size =
            SurfaceSize::new(1_280, 800).expect("valid physical size");

        assert!(matches!(
            snapshot.validate(),
            Err(SnapshotError::InvalidSurface(_))
        ));
    }
}
