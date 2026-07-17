# Branch, Pull Request, Review, and Merge Policy

Status: operating baseline  
Owner: repository operations, quality, security, and code owners

## Production rule

All production source, schemas, security policy, release configuration, dependencies, and accepted ADR changes use protected pull requests. The research-phase documentation-only direct-to-main exception expires before broad implementation.

Required controls include:

- required status checks;
- code-owner review for affected paths;
- approval after the latest reviewable push;
- stale-review dismissal for high-risk changes;
- resolved review conversations;
- no force pushes or deletion of protected branches;
- restricted bypass authority;
- verified merge identity;
- deployment approval for stable channels.

## Agent restrictions

An implementation agent cannot approve or merge its own change. An agent may not amend a reviewed commit after approval without causing review to become stale. Generated changes identify their source and regeneration command.

## Emergency work

Embargoed security branches use restricted visibility and independent review. Emergency process may shorten ordinary waiting periods but cannot remove signing separation, artifact verification, rollback preparation, or post-release review.
