# ha-ups-hat-e-remote — Directives

Home Assistant integration that displays Waveshare UPS HAT (E) data published by the remote Pi agent.

## Ownership
- **Masta-Rob** owns this home project DIRECTIVES.md. Flag Rob only for policy changes.

## Safety (always wins)
- Low-battery shutdown behavior changes need Rob's OK (power safety).

## Directives (priority order, highest first)
- Pair with `ups-hat-e-remote`; keep reporting password handling out of git.
- Both HA instances are production; target by hardware location.

## Non-goals
- Not the I2C HAT driver itself (see homeassistant_waveshare_ups_hat_e / ups-hat-e-remote).

## Standing rules that apply here
- No secrets in git. Deploy via MyHACS approve policy.

## Change log
- 2026-11-04 — Masta-Rob — Initial DIRECTIVES.md (Rob's OK: yes, pt1410u).
