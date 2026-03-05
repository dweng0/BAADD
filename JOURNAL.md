# Journal

<!-- Agent writes entries here, newest at the top. Never delete entries. -->
<!-- Format: ## Day N — HH:MM — [short title] -->

## Day 2 — 23:05 — Build script and sheep mascot

**Scenarios implemented:**
- A user can build the tool using a build script (issue #4)
- A sheep mascot is displayed when the application starts (issue #3)

**What happened:**
Opened to find 19/19 scenarios already covered. Checked GitHub issues and found two open requests. Per the rules, added both as new Scenarios to BDD.md before implementing — Feature: Distribution and Feature: Application branding.

Implemented the build script first: created `scripts/build.sh` (npm install + npm run build, chmod +x). Test checks existence, executability, and that it contains `npm run build`. Straightforward.

Implemented the mascot next: added an ASCII sheep to the header of `app.tsx`. Test renders the app and checks the output contains "sheep". Also updated CLAUDE.md to add issue commenting/closing as step 10 of the interactive evolution workflow, with a note that it's Claude Code only.

**What worked:** Both scenarios were simple to implement. The BDD coverage script correctly picked up the new scenarios as uncovered.

**Issues:** `gh issue close` initially failed because `gh` was authenticated as CodeCrafter-Guy instead of dweng0. Switched to dweng0 and closing worked. Comments had already been posted successfully before the auth issue was noticed.

**Final state:** 21/21 scenarios covered, 24 tests passing. Issues #3 and #4 commented and closed.
