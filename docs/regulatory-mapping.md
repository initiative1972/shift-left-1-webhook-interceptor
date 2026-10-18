# Regulatory mapping — how this control maps to APRA expectations

> General information only. **Not compliance or legal advice.** Verify all
> regulatory facts against [apra.gov.au](https://www.apra.gov.au) before relying
> on them. This is a personal portfolio project built on public sources only.

## Status of the standards (verified)

- **CPS 230 Operational Risk Management** — **fully in force.** Commenced
  1 July 2025; the transition period ended 1 July 2026. Amendments issued
  30 April 2026 are live.
- **CPS 234 Information Security** — in force since 1 July 2019.

APRA's supervisory emphasis has moved toward **evidence of effective
implementation** of controls — being able to *show* that a control operates, not
merely assert that it exists.

## Why a data contract is a relevant control

| Expectation (paraphrased) | How this project evidences it |
|---|---|
| Identify and manage risks from **third-party / upstream service providers** (CPS 230) | The contract defines the technical agreement at the producer boundary and enforces it automatically. |
| Maintain **integrity** of data supporting critical operations | Quality rules (uniqueness, range, enumerations, non-null keys) run on every change. |
| Demonstrate **effective implementation**, not just existence, of controls | The control runs in CI on every pull request, producing a continuous, timestamped, auditable trail — not a point-in-time attestation. |
| Protect critical operations from **disruption** caused by change | A breaking upstream change fails the build and is blocked *before* it reaches the warehouse. |
| **Information asset classification** (CPS 234) | `account_id` is tagged `classification: restricted` in the contract, linking schema to a security classification. |

## What this does *not* claim

This is a single technical control on a synthetic pipeline. It is **not** a
compliance programme, a complete operational-resilience solution, or a
substitute for professional advice. It illustrates one concrete way the
"shift-left" pattern produces the kind of *evidence* APRA's framework asks for.
