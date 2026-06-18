# Current Harness Reference

This document is the current reproduction-grade specification for the harness
used under `docs/plans/current/user-db-python-migration/`.

Its purpose is to let another project reproduce the same harness model without
replaying this workspace history.

## Core Model

The harness is plan-first and leader-orchestrated.

The core rules are:

- the operator enters through `leader`
- the selected plan file is the source of strategy
- the selected plan `tasks.json` is the execution ledger
- active growing records are plan-scoped
- global files stay small and reusable
- specialist roles work in isolated sub-agents
- structured workflow state uses JSON
- narrative guidance and accepted summaries use Markdown

## Canonical Precedence

The reproduction target is the canonical harness, not every file that may exist
in the workspace.

Canonical authority resolves in this order:

1. `index.json`
2. `project-bootstrap.json`
3. `plan-bootstrap.json`
4. `plans/<plan_id>/plan.md`
5. `plans/<plan_id>/tasks.json`
6. `records/records-index.json`
7. `findings/findings-index.json`

Rules:

- reproduce only the canonical paths and contracts described in this document
- do not treat incidental files outside the canonical plan tree as part of the
  harness model
- if a workspace contains compatibility, history, or transitional files, those
  files do not override the canonical plan folder, plan ledger, or plan-scoped
  records model
- startup and routing decisions must always resolve through the canonical index
  and bootstrap files before touching plan-scoped artifacts

## Folder Tree

```text
user-db-python-migration/
|-- START.md
|-- GPT.md
|-- index.json
|-- project-bootstrap.json
|-- plan-bootstrap.json
|-- models.json
|-- bootstrap-tasks.json
|-- lessons-learned.json
|-- user-db-contract-freeze.md
|-- .gpt/
|   |-- leader.md
|   |-- architect.md
|   |-- architecture-reviewer.md
|   |-- developer.md
|   |-- reviewer.md
|   `-- tester.md
|-- conventions/
|   |-- harness-architecture.md
|   |-- token-efficiency.md
|   |-- architecture.md
|   |-- python-standards.md
|   |-- python-migration.md
|   |-- testing.md
|   |-- logging.md
|   |-- libraries.md
|   |-- environment-and-properties.md
|   `-- tools.md
|-- records/
|   |-- decision-log.json
|   `-- records-index.json
|-- findings/
|   |-- findings-index.json
|   `-- *.md
`-- plans/
    |-- README.md
    `-- <plan_id>/
        |-- plan.md
        |-- tasks.json
        |-- migration-design.md
        `-- records/
            |-- handoffs.json
            |-- validation-summary.md
            |-- validation-events.json
            |-- execution-logs/
            `-- architecture-design/
```

## Required Vs Optional Artifacts

### Required Root Artifacts

- `START.md`
  - public harness entry point
- `GPT.md`
  - reusable operating contract
- `index.json`
  - coordination registry and plan mapping
- `project-bootstrap.json`
  - workspace startup ledger
- `plan-bootstrap.json`
  - active plan-stream bootstrap ledger
- `.gpt/leader.md`
- `.gpt/architect.md`
- `.gpt/architecture-reviewer.md`
- `.gpt/developer.md`
- `.gpt/reviewer.md`
- `.gpt/tester.md`
- `conventions/harness-architecture.md`
- `conventions/token-efficiency.md`
- `records/records-index.json`
- `records/decision-log.json`
- `findings/findings-index.json`
- `plans/README.md`

### Conditionally Required Root Artifacts

- `models.json`
  - required only if the workspace wants a shared registry of model/runtime metadata
- `bootstrap-tasks.json`
  - required only if the workspace uses a separate startup task registry
- `lessons-learned.json`
  - required if the workspace wants reusable cross-plan failure memory
- additional convention files under `conventions/`
  - required only when the active task stream depends on those standards
- findings documents under `findings/*.md`
  - required only when an issue needs them

### Optional Root Artifacts

- domain-specific reference files such as `user-db-contract-freeze.md`
  - useful to the project, but not part of the harness control plane

### Required Per-Plan Artifacts

- `plans/<plan_id>/records/`
- `plans/<plan_id>/plan.md`
- `plans/<plan_id>/tasks.json`
- `plans/<plan_id>/records/handoffs.json`
- `plans/<plan_id>/records/validation-summary.md`
- `plans/<plan_id>/records/validation-events.json`
- `plans/<plan_id>/records/execution-logs/`

### Conditionally Required Per-Plan Artifacts

- `plans/<plan_id>/records/architecture-design/`
  - required when the plan contains design or architecture tasks that must output durable artifacts
- `plans/<plan_id>/migration-design.md`
  - required only when the plan stream carries a migration-guide or reusable design-enrichment artifact

## Root Artifact Responsibilities

`START.md`

- simple operator-facing entry point
- names the startup read order
- names the leader as the only public entry role

`GPT.md`

- reusable operating contract
- role definitions
- workflow order
- execution rules
- validation gate rules
- state-transition rules

`index.json`

- global coordination registry
- active plan pointer
- plan registration contract
- canonical mapping from `plan_id` to plan folder and plan ledger

`project-bootstrap.json`

- workspace-level startup ledger
- tells the harness what to read before a plan stream is chosen

`plan-bootstrap.json`

- active plan-stream startup ledger
- points to the active plan root, active plan file, and active tasks file

`models.json`

- optional shared structured registry for model/runtime metadata

`bootstrap-tasks.json`

- optional startup task registry

`lessons-learned.json`

- reusable cross-plan memory for recurring failures, fixes, and attempts

`.gpt/`

- one role prompt file per harness role
- one agent should hold one role only

`conventions/`

- reusable standards library
- only minimum required convention files should be loaded for a task

`records/decision-log.json`

- active global decision history
- machine-friendly but rich enough to capture context, rationale, and tradeoffs

`records/records-index.json`

- discovery index for active record locations

`findings/findings-index.json`

- discovery index for findings by scope and plan

`plans/`

- canonical home for every plan stream

## Role Model

Required roles:

- `leader`
  - orchestration only
- `architect`
  - design only
- `architecture-reviewer`
  - architecture review only
- `developer`
  - implementation only
- `reviewer`
  - implementation review only
- `tester`
  - validation only

Role isolation rules:

- one agent, one role
- specialist work runs in isolated sub-agents
- unrelated sub-agent reuse is forbidden
- if the pool is full, free an unrelated completed agent before spawning a fresh specialist

## Artifact Ownership Matrix

This matrix defines who may author or update each artifact class.

| Artifact | Create Owner | Update Owner | Primary Readers |
|---|---|---|---|
| `index.json` | `leader` | `leader` | all roles |
| `project-bootstrap.json` | `leader` | `leader` | all roles |
| `plan-bootstrap.json` | `leader` | `leader` | all roles |
| `plans/<plan_id>/plan.md` | `leader` | `leader` | all roles |
| `plans/<plan_id>/tasks.json` | `leader` | `leader` maintains authoritative state using specialist outputs | all roles |
| `records/records-index.json` | `leader` | `leader` | all roles |
| `findings/findings-index.json` | `leader` | `leader` | all roles |
| `records/decision-log.json` | `leader` | `leader` | all roles |
| `plans/<plan_id>/records/handoffs.json` | `leader` | `leader` | all roles |
| `plans/<plan_id>/records/validation-summary.md` | `tester` | `tester`, then accepted by `leader` | `leader`, `reviewer`, `tester` |
| `plans/<plan_id>/records/validation-events.json` | `tester` | `tester` | `leader`, `reviewer`, `tester` |
| `plans/<plan_id>/records/architecture-design/*.md` | `architect` | `architect` | `leader`, `architecture-reviewer`, `developer`, `reviewer`, `tester` as needed |
| implementation source files | `developer` | `developer` | all specialist roles as needed |
| implementation review notes in ledger | `reviewer` | `reviewer` | `leader`, `developer`, `tester` |

Rules:

- `leader` owns orchestration artifacts and canonical ledger state
- `architect` owns design content and must author specialist design artifacts directly
- `architecture-reviewer` must not replace architect authorship; it approves or returns rework
- `reviewer` and `tester` may report findings and recommended status changes, but `leader`
  remains the owner of canonical `tasks.json` mutation
- if a specialist-owned artifact needs a stub before delegation, the stub must remain
  non-substantive

## Current Convention Set

Required by default:

- `conventions/harness-architecture.md`
- `conventions/token-efficiency.md`

Common conditional conventions:

- `conventions/architecture.md`
- `conventions/testing.md`
- `conventions/python-standards.md`
- `conventions/python-migration.md`
- `conventions/logging.md`
- `conventions/libraries.md`
- `conventions/environment-and-properties.md`
- `conventions/tools.md`

Rule for loading extra conventions:

- load a convention file only when the active task depends on that topic
- examples:
  - architecture task -> load `architecture.md`
  - Python runtime task -> load `python-standards.md`
  - validation task -> load `testing.md`
  - logging task -> load `logging.md`

## Minimum Startup Contract

### Always-Read Files

These files must be read before any task execution:

1. `START.md`
2. `GPT.md`
3. `index.json`
4. `project-bootstrap.json`
5. `plan-bootstrap.json`
6. selected canonical `plans/<plan_id>/plan.md`
7. `conventions/token-efficiency.md`
8. `conventions/harness-architecture.md`

### Active-Plan Files

Read after the always-read set:

- resolve the selected plan through `index.json` and confirm that
  `plan-bootstrap.json` targets the same canonical plan stream before reading
  plan-scoped state
- selected `plans/<plan_id>/tasks.json` when routing, active-task selection, or rework history requires it
- `records/records-index.json` when active records must be resolved
- `findings/findings-index.json` when findings may be relevant

### Task-Conditional Files

Read only when needed:

- additional convention files for the task domain
- `lessons-learned.json` when a similar recurring failure pattern exists
- specific findings documents resolved from `findings-index.json`
- plan-scoped record files only when the task requires those records

## Canonical JSON Contracts

Type notation used below:

- `string`
- `boolean`
- `integer`
- `object`
- `array<T>`
- `enum<...>`

### `index.json`

Minimum required keys:

- `workspace`
- `version`
- `last_updated`
- `active_plan_id`
- `plan_registration_contract`
- `global_resources`
- `plans`

Minimum `plan_registration_contract` keys:

- `activate_on_register_field`
- `activate_on_register_default`
- `activation_rule`

Minimum `plans[]` item keys:

- `plan_id`
- `label`
- `plan_root`
- `plan_file`
- `tasks_file`
- `activate_on_register`
- `status`

Field types:

- `workspace`: `string`
- `version`: `integer`
- `last_updated`: `string` in ISO 8601 UTC form
- `active_plan_id`: `string`
- `plan_registration_contract`: `object`
- `global_resources`: `object`
- `plans`: `array<object>`

Cross-field constraints:

- `active_plan_id` must match one `plans[].plan_id`
- `plans[].plan_root`, `plan_file`, and `tasks_file` must all point to the same plan folder
- `plans[].status` should be `active` for exactly one plan at a time
- `activate_on_register` defaults from `plan_registration_contract` when omitted during registration

### `project-bootstrap.json`

Minimum required keys:

- `workspace`
- `purpose`
- `version`
- `last_updated`
- `index_file`
- `rules_file`
- `start_file`
- `roles_dir`
- `conventions_dir`
- `records_index_file`
- `findings_index_file`
- `bootstrap_rules`
- `roles`

Field types:

- all path fields: `string`
- `bootstrap_rules`: `array<string>`
- `roles`: `object`

Cross-field constraints:

- `index_file` must point to the canonical `index.json`
- `rules_file` must point to `GPT.md`
- `roles` should list every required role in the harness

### `plan-bootstrap.json`

Minimum required keys:

- `workspace`
- `purpose`
- `version`
- `last_updated`
- `active_plan_id`
- `active_plan_root`
- `active_plan_file`
- `target_tasks_file`
- `bootstrap_status`
- `bootstrap_rules`

Field types:

- all plan target fields: `string`
- `bootstrap_status`: `enum<draft, ready, blocked>`
- `bootstrap_rules`: `array<string>`

Cross-field constraints:

- `active_plan_root`, `active_plan_file`, and `target_tasks_file` must all resolve to the same plan stream
- `active_plan_id` must match `index.json.active_plan_id` for the active stream

### `records-index.json`

Minimum required keys:

- `version`
- `last_updated`
- `purpose`
- `global_records`
- `per_plan_records`

Required `global_records` entries:

- `decision_log`
- `lessons_learned` if lessons are enabled

Required `per_plan_records` entries:

- `handoffs`
- `validation_summary`
- `validation_events`
- `execution_logs`

Field types:

- `global_records`: `object`
- `per_plan_records`: `object`
- each record descriptor: `object` with `format`, `scope`, `path` or `path_pattern`, `status`, and `startup_required`

Cross-field constraints:

- `startup_required: false` means "not a default startup read", not "artifact optional"
- `path_pattern` entries must resolve under `plans/<plan_id>/records/`
- `format` must match the actual artifact contract

### `findings-index.json`

Minimum required keys:

- `version`
- `last_updated`
- `purpose`
- `findings`

Minimum `findings[]` item keys:

- `id`
- `format`
- `scope`
- `plan_id`
- `path`
- `status`

Field types:

- `findings`: `array<object>`
- `path`: `string`
- `status`: `enum<open, accepted, deferred, resolved, archived, active_reference, historical>` or project-approved equivalent

Cross-field constraints:

- `plan_id` should be the owning plan or `global` for workspace-wide findings
- `path` must resolve to an existing or reserved findings artifact path
- if the workspace distinguishes reusable active references from historical findings, both statuses should be explicitly documented in the index contract

## `tasks.json` Contract

### Top-Level Required Keys

- `plan_id`
- `plan_name`
- `version`
- `status`
- `owner`
- `active_task`
- `last_updated`
- `workspace_files`
- `roles`
- `status_model`
- `governance`
- `tasks`

### `workspace_files` Required Keys

- `index`
- `project_bootstrap`
- `plan_bootstrap`
- `plan`
- `rules`

Field types:

- top-level metadata fields: `string` except `version`
- `version`: `integer`
- `roles`: `object`
- `status_model`: `array<string>`
- `tasks`: `array<object>`

### `governance` Required Keys

- `system_of_record`
- `plan_file`

### Task Object Required Keys

- `id`
- `title`
- `status`
- `priority`
- `size`
- `task_type`
- `owner_role`
- `depends_on`
- `objective`
- `affected_modules`
- `expected_outputs`
- `validation_steps`
- `evidence`
- `leader_report`

Field types:

- `id`: `string`
- `title`: `string`
- `status`: `string`
- `priority`: `enum<low, medium, high, critical>` or project-approved equivalent
- `size`: `enum<small, medium, large>` or project-approved equivalent
- `task_type`: `string`
- `owner_role`: `string`
- `depends_on`: `array<string>`
- `affected_modules`: `array<string>`
- `expected_outputs`: `array<string>`
- `validation_steps`: `array<string>`
- `evidence`: `array<string>`
- `leader_report`: `object`

### Conditionally Useful Task Keys

- `related_tasks`
- `reviewer_report`
- `notes`
- `deferred_reason`
- `deferred_accepted_by`

### `leader_report` Required Keys

- `acceptance_notes`

### `active_task` Representation

- `null` means no active executable task is currently selected
- otherwise it should equal one task `id` in `tasks[]`
- `active_task` must never point to a task in `placeholder`, `completed`,
  `cancelled`, or `validated` status

Cross-field constraints:

- every `depends_on` entry must reference another task `id` or be an empty array
- every task `status` must exist in `status_model`
- `owner_role` should match the next specialist expected to act on that task state
- there should be at most one active executable task unless the harness explicitly supports parallel active tasks

### Allowed Status Model

Recommended status set:

- `placeholder`
- `planned`
- `in_architecture_review`
- `architecture_reviewed`
- `ready_for_dev`
- `in_progress`
- `implemented`
- `in_review`
- `reviewed`
- `in_validation`
- `rework_required`
- `validated`
- `completed`
- `deferred`
- `blocked`
- `cancelled`

### Role Transition Authority

- `leader`
  - may set `planned`
  - may select `active_task`
  - may set `completed`
  - may set `deferred` after explicit operator acceptance
  - may record acceptance and sequencing decisions
- `architect`
  - produces design artifacts
  - recommends architecture outcomes through specialist artifacts and handoff output
- `architecture-reviewer`
  - may recommend `in_architecture_review`
  - may recommend `architecture_reviewed`
  - may recommend `rework_required` for architecture failures
- `developer`
  - may recommend `in_progress`
  - may recommend `implemented`
  - may recommend `rework_required` only if blocked by discovered implementation issues that must return upstream
- `reviewer`
  - may recommend `in_review`
  - may recommend `reviewed`
  - may recommend `rework_required`
- `tester`
  - may recommend `in_validation`
  - may recommend `validated`
  - may recommend `rework_required`

Rework rule:

- when a task is `rework_required`, the next step belongs to the role responsible for the correction
- the downstream gate reruns only after that corrective pass completes
- specialist roles report status outcomes; the `leader` writes the canonical state transition into `tasks.json`

### Canonical `tasks.json` Example

Illustrative example only. Replace `<workspace_root>` with the target project root.

```json
{
  "plan_id": "plan_03",
  "plan_name": "Plan 03 - Example",
  "version": 1,
  "status": "in_progress",
  "owner": "leader",
  "active_task": "T002",
  "last_updated": "2026-06-18T18:25:00Z",
  "workspace_files": {
    "index": "<workspace_root>/index.json",
    "project_bootstrap": "<workspace_root>/project-bootstrap.json",
    "plan_bootstrap": "<workspace_root>/plan-bootstrap.json",
    "plan": "<workspace_root>/plans/plan_03/plan.md",
    "rules": "<workspace_root>/GPT.md"
  },
  "roles": {
    "leader": { "model": "gpt-5.4" },
    "architect": { "model": "gpt-5.4-mini" },
    "architecture-reviewer": { "model": "gpt-5.4-mini" },
    "developer": { "model": "gpt-5.4-mini" },
    "reviewer": { "model": "gpt-5.4-mini" },
    "tester": { "model": "gpt-5.4-mini" }
  },
  "status_model": [
    "placeholder",
    "planned",
    "in_architecture_review",
    "architecture_reviewed",
    "ready_for_dev",
    "in_progress",
    "implemented",
    "in_review",
    "reviewed",
    "in_validation",
    "rework_required",
    "validated",
    "completed",
    "deferred",
    "blocked",
    "cancelled"
  ],
  "governance": {
    "system_of_record": "plans/plan_03/tasks.json",
    "plan_file": "<workspace_root>/plans/plan_03/plan.md"
  },
  "tasks": [
    {
      "id": "T002",
      "title": "Implement example task",
      "status": "implemented",
      "priority": "high",
      "size": "small",
      "task_type": "implementation",
      "owner_role": "developer",
      "depends_on": ["T001"],
      "related_tasks": [],
      "objective": "Implement the approved change.",
      "affected_modules": [
        "src/example.py",
        "tests/test_example.py"
      ],
      "expected_outputs": [
        "Runtime behavior updated",
        "Focused test coverage added"
      ],
      "validation_steps": [
        "Run focused unit tests",
        "Route to reviewer"
      ],
      "evidence": [
        "Focused unit proof passed"
      ],
      "leader_report": {
        "acceptance_notes": "Ready for reviewer gate."
      }
    }
  ]
}
```

## Plan Records Contract

### Required `plans/<plan_id>/records/` Artifacts

- `handoffs.json`
- `validation-summary.md`
- `validation-events.json`
- `execution-logs/`

### Conditionally Required `plans/<plan_id>/records/` Artifacts

- `architecture-design/`
  - required when a design or architecture task must output a durable artifact

### `handoffs.json`

Purpose:

- structured role handoff ledger
- machine-friendly workflow state

Minimum required keys:

- `plan_id`
- `version`
- `entries`

Minimum `entries[]` item keys:

- `timestamp`
- `from_role`
- `to_role`
- `task_id`
- `status`
- `summary`
- `next_expected_role`

Optional keys:

- `evidence`
- `notes`

Canonical example:

```json
{
  "plan_id": "plan_03",
  "version": 1,
  "entries": [
    {
      "timestamp": "2026-06-18T18:25:00Z",
      "from_role": "developer",
      "to_role": "leader",
      "task_id": "T058",
      "status": "implemented",
      "summary": "Warm-start connection manager and executor implemented.",
      "evidence": [
        "<workspace_root>/plans/plan_03/records/execution-logs/example.log"
      ],
      "next_expected_role": "reviewer"
    }
  ]
}
```

### `validation-events.json`

Purpose:

- structured event-by-event validation ledger

Minimum required keys:

- `plan_id`
- `version`
- `events`

Minimum `events[]` item keys:

- `timestamp`
- `task_id`
- `role`
- `validation_type`
- `result`
- `summary`

Optional keys:

- `command`
- `evidence`
- `classification`

Illustrative example path rule:

- store command output references under `<workspace_root>/plans/<plan_id>/records/execution-logs/`

### `validation-summary.md`

Purpose:

- accepted validation evidence summary
- curated high-signal digest of proof that the harness accepts

Requirement rule:

- required for every active plan
- update it when validation produces accepted evidence or a decision-relevant blocker
- do not duplicate every raw event; summarize accepted outcomes and point to evidence

### `execution-logs/`

Purpose:

- raw command output and proof logs

Requirement rule:

- required as a directory for every active plan
- write evidence-producing command output here

### `architecture-design/`

Purpose:

- durable design artifacts for architecture/design tasks

Requirement rule:

- required only when the plan includes design or architecture tasks that must output artifacts
- each design task should point to a concrete file path under this directory unless the operator approves another location

## Global Records Contract

### `decision-log.json`

Purpose:

- active global decision history
- structured retrieval for reusable harness decisions

Minimum required keys:

- `entries`

Recommended top-level keys:

- `version`
- `last_updated`

Minimum `entries[]` item keys:

- `id`
- `timestamp`
- `scope`
- `category`
- `title`
- `status`
- `summary`
- `context`
- `decision`
- `rationale`
- `tradeoffs`
- `impact`
- `related_files`

Canonical example:

```json
{
  "version": 1,
  "last_updated": "2026-06-18T18:25:00Z",
  "entries": [
    {
      "id": "D-2026-06-18-001",
      "timestamp": "2026-06-18T18:25:00Z",
      "scope": "global",
      "category": "harness",
      "title": "Per-plan handoffs use JSON",
      "status": "accepted",
      "summary": "Per-plan handoffs are stored in handoffs.json instead of handoffs.md.",
      "context": "Handoffs are consumed mainly by the harness and role-routing flow.",
      "decision": "Use JSON as the canonical per-plan handoff format.",
      "rationale": [
        "Handoffs are workflow-state artifacts.",
        "Structured parsing is better for LLM routing and validation.",
        "Markdown was adding unnecessary ambiguity."
      ],
      "tradeoffs": [
        "Less natural for long narrative explanation.",
        "Requires a stable schema."
      ],
      "impact": [
        "records-index.json must point to handoffs.json",
        "plan record specs must use handoffs.json"
      ],
      "related_files": [
        "<workspace_root>/records/records-index.json"
      ]
    }
  ]
}
```

Rule:

- keep `decision-log.json` rich enough to preserve rationale and tradeoffs
- do not reduce decisions to a single shallow sentence

## Naming Conventions

### Plans

- folder: `plans/<plan_id>/`
- plan file: `plans/<plan_id>/plan.md`
- plan ledger: `plans/<plan_id>/tasks.json`

### Design Artifacts

- default directory: `plans/<plan_id>/records/architecture-design/`
- recommended filename:
  - `<task_id>-<short-kebab-title>.md`

Example:

- `T057-postgres-warm-start-connection-strategy.md`

### Execution Logs

- default directory: `plans/<plan_id>/records/execution-logs/`
- recommended filename:
  - `<task_id>-<short-purpose>-<timestamp>.log`

Example:

- `T058-integration-20260618-182500.log`

### Decision Entries

- recommended `decision-log.json` entry id:
  - `D-YYYY-MM-DD-NNN`

### Handoff Entries

- use ISO timestamp in `timestamp`
- one handoff entry per meaningful role transition or acceptance boundary

## Canonical Current Model

The current harness model is:

- `index.json` chooses the plan
- `project-bootstrap.json` starts the workspace
- `plan-bootstrap.json` starts the active plan stream
- `plans/<plan_id>/plan.md` is the plan
- `plans/<plan_id>/tasks.json` is the execution ledger
- `plans/<plan_id>/records/` contains active handoffs, validation, logs, and design artifacts when required

## Lifecycle Rules

### Plan Registration

1. `leader` registers the new plan in `index.json`
2. `leader` creates the canonical `plans/<plan_id>/` folder
3. `leader` creates `plan.md`, `tasks.json`, and required plan record artifacts
4. `leader` updates `records/records-index.json` only if a new record class is introduced
5. `leader` updates `findings/findings-index.json` only when new findings are created or discovered
6. `leader` updates `plan-bootstrap.json` only when the new plan becomes the active stream

### Task Execution

1. `leader` selects or promotes the next executable task in `tasks.json`
2. owning specialist performs the work in its role boundary
3. owning specialist writes only its owned artifact class
4. `leader` records the resulting canonical state in `tasks.json` and `handoffs.json`
5. downstream gate repeats until the task reaches `completed`, `blocked`, `deferred`, or `cancelled`

### Findings Lifecycle

1. create an index entry when a reusable or decision-relevant finding is first recorded
2. use `open` while investigation is active
3. move to `accepted`, `deferred`, or `resolved` when the finding is classified
4. keep the index path stable; update status rather than creating duplicate entries for the same finding lineage

### Plan Close

1. `leader` confirms there is no remaining executable `active_task`
2. `leader` confirms placeholder or pending tasks are either promoted, completed, or explicitly accepted as deferred by the operator
3. `leader` converts any operator-accepted out-of-scope placeholder or pending task to `deferred` and records `deferred_reason` plus `deferred_accepted_by`
4. `tester` ensures accepted validation evidence is summarized in `validation-summary.md`
5. `leader` leaves plan records in place under the plan folder; do not collapse active records into global history

## Current Startup Flow

The current harness starts in this order:

1. `START.md`
2. `GPT.md`
3. `index.json`
4. `project-bootstrap.json`
5. `plan-bootstrap.json`
6. selected canonical `plans/<plan_id>/plan.md`
7. `conventions/token-efficiency.md`
8. `conventions/harness-architecture.md`
9. only the additional convention files required by the active task
10. selected `plans/<plan_id>/tasks.json` when routing or task history requires it

## Minimal Reproduction Checklist

To reproduce this harness in another project:

1. create the required root artifacts:
   - `START.md`
   - `GPT.md`
   - `index.json`
   - `project-bootstrap.json`
   - `plan-bootstrap.json`
   - `records/decision-log.json`
   - `records/records-index.json`
   - `findings/findings-index.json`
2. create `.gpt/` with one prompt file per role
3. create `conventions/` with at least `harness-architecture.md` and `token-efficiency.md`
4. create `plans/README.md`
5. create `plans/<plan_id>/plan.md`
6. create `plans/<plan_id>/tasks.json` using the canonical task-ledger contract
7. create `plans/<plan_id>/records/handoffs.json`
8. create `plans/<plan_id>/records/validation-summary.md`
9. create `plans/<plan_id>/records/validation-events.json`
10. create `plans/<plan_id>/records/execution-logs/`
11. create `plans/<plan_id>/records/architecture-design/` if the plan contains design tasks
12. ensure active execution routes through the canonical plan folder and plan ledger only
