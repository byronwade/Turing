// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum RenderStage {
    Parse,
    Style,
    Layout,
    Paint,
    Composite,
}

impl RenderStage {
    const ORDER: [Self; 5] = [
        Self::Parse,
        Self::Style,
        Self::Layout,
        Self::Paint,
        Self::Composite,
    ];

    const fn index(self) -> usize {
        match self {
            Self::Parse => 0,
            Self::Style => 1,
            Self::Layout => 2,
            Self::Paint => 3,
            Self::Composite => 4,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RenderPipeline {
    dirty_from: Option<RenderStage>,
    completed_epoch: u64,
}

impl RenderPipeline {
    #[must_use]
    pub const fn new() -> Self {
        Self {
            dirty_from: Some(RenderStage::Parse),
            completed_epoch: 0,
        }
    }

    pub fn invalidate_from(&mut self, stage: RenderStage) {
        self.dirty_from = match self.dirty_from {
            Some(existing) if existing <= stage => Some(existing),
            _ => Some(stage),
        };
    }

    #[must_use]
    pub const fn dirty_from(&self) -> Option<RenderStage> {
        self.dirty_from
    }

    #[must_use]
    pub const fn completed_epoch(&self) -> u64 {
        self.completed_epoch
    }

    pub fn run(&mut self) -> Result<Vec<RenderStage>, RenderError> {
        let Some(first) = self.dirty_from else {
            return Ok(Vec::new());
        };

        let completed = RenderStage::ORDER[first.index()..].to_vec();
        self.completed_epoch = self
            .completed_epoch
            .checked_add(1)
            .ok_or(RenderError::EpochOverflow)?;
        self.dirty_from = None;
        Ok(completed)
    }
}

impl Default for RenderPipeline {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RenderError {
    EpochOverflow,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn initial_run_executes_every_stage_in_order() {
        let mut pipeline = RenderPipeline::new();
        assert_eq!(
            pipeline.run().unwrap(),
            vec![
                RenderStage::Parse,
                RenderStage::Style,
                RenderStage::Layout,
                RenderStage::Paint,
                RenderStage::Composite
            ]
        );
    }

    #[test]
    fn layout_invalidation_does_not_repeat_parse_or_style() {
        let mut pipeline = RenderPipeline::new();
        pipeline.run().unwrap();
        pipeline.invalidate_from(RenderStage::Layout);
        assert_eq!(
            pipeline.run().unwrap(),
            vec![
                RenderStage::Layout,
                RenderStage::Paint,
                RenderStage::Composite
            ]
        );
    }

    #[test]
    fn earlier_invalidation_wins() {
        let mut pipeline = RenderPipeline::new();
        pipeline.run().unwrap();
        pipeline.invalidate_from(RenderStage::Paint);
        pipeline.invalidate_from(RenderStage::Style);
        pipeline.invalidate_from(RenderStage::Composite);
        assert_eq!(pipeline.dirty_from(), Some(RenderStage::Style));
    }
}
