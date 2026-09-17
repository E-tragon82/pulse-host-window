# pulse-host-window

Host-plane GitHub Action for **The Pulse** news desk.

- Repo: https://github.com/E-tragon82/pulse-host-window
- Workflow: `.github/workflows/pulse-host-window.yml`
- Not a QuadForge pack skill. Do not copy into `mac-quadforge/skills/`.
- `aired` stays false until desk review + `fulfil_publish`.
- Windows: 00 / 06 / 12 / 18 UTC only.

## What is installed

The workflow file is in this repo. The **pin tree** (`news-desk-pin/host_job.py` and friends) is not.
Until you push that tree (or run the job from a checkout that already has it), the Action checks out, proves the hour is legal, and exits `HOLD pin-not-in-repo` without failing the schedule.

## Run

Actions → pulse-host-window → Run workflow. Inputs: `hour`, `country`, `lane`.

Grok Automations `pulse-window-00/06/12/18utc` already exist and do not replace this repo.
