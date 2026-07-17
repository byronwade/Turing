# Cost, Resource, and Concurrency Budgets

Status: operating baseline  
Owner: agent operations, performance, infrastructure, and program

Every agent task declares maximum wall time, CPU, memory, disk, network transfer, external API cost, model tokens, parallel workers, retries, and artifact retention.

Concurrency follows dependency and ownership boundaries. More agents are not automatically faster when they duplicate research, race on shared interfaces, create incompatible abstractions, or overwhelm review capacity.

The coordinator limits work in progress according to available code owners, security reviewers, test infrastructure, and release capacity. A queue may pause even when compute is available.

Budget overruns stop or escalate the task. Agents cannot hide cost by spawning untracked subagents or external services.
