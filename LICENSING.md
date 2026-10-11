# Licensing scope

The Apache License, Version 2.0, reproduced in [LICENSE](LICENSE), applies to
Pavlo-authored repository material within the scope below, to the extent Pavlo
owns or is authorized to license the relevant rights.

Copyright 2026 Pavlo Tvardovskyi

Existing third-party copyright, license, patent, attribution and trademark
notices remain applicable. For mixed or adapted material, the new grant covers
only Pavlo's original additions. Imported source, external contributions,
quoted specifications, captures and other third-party material are not
relicensed by this grant. Inclusion in this repository or a missing license
does not itself supply permission. Existing grants are not withdrawn or narrowed.

| Material | Applicable boundary |
| --- | --- |
| Pavlo-authored implementation in `src/**`, `demo/**`, `contracts/**`, tests, schemas, tools/scripts, configuration and original documentation/examples | Apache-2.0 for Pavlo's original code/prose. Existing MIT grants in the Solidity anchor source headers remain available. |
| `fixtures/mldsa/**` and externally sourced vector, signature or entropy operands | Preserved fixture/source rights apply. A local path, a reference to a Pavlo-owned vendor repository, or a digest does not independently establish authorship of each operand. No new grant is asserted for unconfirmed vector material. |
| `examples/stealth/**`, Stealth handoff fixtures and externally supplied integration fields | Pavlo's original adapter and synthetic additions are covered; upstream ATP/Stealth captures, quoted structures and externally supplied portions retain original rights. No ATP/Stealth core is relicensed. |
| `artifacts/**`, `data/**`, `reports/**`, `output/**`, generated demo/example receipts, historical audit and integration records in `docs/**` | Pavlo-authored synthetic/analytical additions are covered only within his authority. Captured outputs, third-party data, quotations, identifiers and embedded external content retain applicable source rights. Historical bytes and provenance are unchanged. |
| npm/Hardhat dependencies referenced by `package-lock.json` | Their own licenses apply. Only the root first-party package license field is updated; dependency entries and hashes are unchanged. |

The root package metadata describes Pavlo's Hardhat anchoring package code,
not a license grant for third-party fixtures or dependency contents. Prior
dated notes reporting a missing root license remain historical observations.
No real-backend vendor repository was fetched, changed or relicensed by this task.
