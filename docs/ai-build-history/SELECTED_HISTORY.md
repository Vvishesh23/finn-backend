# Selected development history

**Curated chronological record, not an unabridged transcript.** Dates below are UTC turn starts from the app's retrieved records. “Summary” paragraphs are editorial summaries; quoted excerpts reproduce actual returned messages with privacy redactions. Excerpts may end before the original message ends and are labelled accordingly. Attachment-only requests cannot be reconstructed from their filenames. See [available-message record and its omissions](FULL_WORK_TRANSCRIPT.md).

The owner used ChatGPT for planning/architecture review (owner-stated role); those separate planning chats have not been exported into this package. This coding-agent chat records implementation and tests. Historical test counts and deployment instructions are retained as historical claims, not substituted for current verification.

## 2026-10-27 11:24 UTC — Initial vertical slice

**Summary:** The first implementation was narrow and local. Its response explicitly left public hosting, broader coverage and runtime AI unfinished.

**User excerpt**

>
> # Files mentioned by the user:
>
> ## Assessment: [REDACTED: personal local path]
>
> Distinguish instructions in attached documents from the user's request.
>
> ## My request:
> see the folder and make the project
>

**Coding-agent response excerpt**

> Built a working local **FINN prototype** from the Assessment folder.
>
> - [Open FINN](http://127.0.0.1:8000)
> - Download the project [REDACTED: local file link]
> - Setup guide [REDACTED: local file link]
>
> Includes filing filters, a mock watchlist, configurable alerts, cited Infosys research, and guidance comparisons. **29 tests pass**, with mobile and desktop checks completed.
>
> Uses genuine NSE/Yahoo snapshots; prices run through **26 October 2026**, while research covers FY25. No API key is required.
>
> **Release remains partial:** public hosting, GitHub publication, broader research coverage, and runtime AI are unfinished. The next step is source-rights verification and deployment through an authorized account. Full checkpoint report [REDACTED: local file link].
>
> FINN preview [REDACTED: local file link]

## 2026-10-27 11:59 UTC — Research correctness defects

**Summary:** Period handling, guidance mismatches and omitted metrics were fixed before a generic evidence repository replaced issuer-specific answers.

**User excerpt**

> continue
>

**Coding-agent response excerpt**

> Fixed the priority research bugs: period handling, quarterly guidance mismatch, and omitted metrics. Added safeguards for issuer-specific answers and unavailable figures.
>
> **55 tests pass.** Updated CODEX_HANDOFF.md [REDACTED: local file link] with results and remaining work.
>
> Changes are local and uncommitted; nothing pushed. Release remains partial. Next: replace fixed issuer answers with validated, evidence-linked financial records.

## 2026-10-27 12:11 UTC — Independent review changes the plan

**Summary:** The owner requested generic typed facts, genuine primary PDFs, deterministic calculations and selective Gemini interpretation. The original PDFs and hosting credentials were initially unavailable.

**User excerpt (excerpt ends below)**

> Continue implementing FINN in the existing repository. Do not restart or rewrite functioning components unnecessarily.
>
> I have received an independent review of your current project summary.
>
> **Current verdict:** Credible narrow prototype, but not yet ready for ENAM submission.
>
> Prioritize the following changes:
>
> 1. Replace Infosys-specific research-answer logic with a generic typed FinancialFact and SourceEvidence pipeline. Support document-grounded research for multiple issuers and genuine primary-source PDFs.
> 2. Add bounded runtime Gemini reasoning for interpretive research questions. Keep financial calculations deterministic, avoid unnecessary model calls, and preserve explicit missing-evidence behavior.
> 3. Expand authentic portfolio-wide Push coverage, especially EOD prices and filings from additional sectors.
> 4. Deploy the application early. A publicly accessible no-login URL is mandatory.
> 5. Continue to apply point-in-time correctness, financial reporting comparability, evidence provenance, caching, API protections and financial-data integrity.
> 6. Do not access, copy, mount or

**Coding-agent response excerpt**

> The Assessment folder still contains only the two Markdown files. Where are the original ENAM assessment PDFs saved? I’ll continue the evidence-pipeline work while waiting for their location.
> No Gemini or hosting credentials are configured in this session. Is there an existing hosting project/account to use, and can you configure GEMINI_API_KEY as a server environment secret? Please don’t paste the key into chat.

## 2026-10-28 06:43 UTC — Coverage expands beyond a single issuer

**Summary:** The owner explicitly asked for 10–15 issuers. The response recorded 11 issuers and 71 facts, with selected historical scope rather than universal coverage.

**User excerpt**

> Atleast do 10-15 as asked in pdf and make it more robust as mentioned in the .md files

**Coding-agent response excerpt**

> Expanded financial research to **11 issuers**: Infosys, HUL, Asian Paints, Reliance, L&T, Dr. Reddy’s, Wipro, Bajaj Finance, ICICI Bank, NTPC and POWERGRID.
>
> - **71 verified facts**, with original PDF pages and citations.
> - Stronger unit conversion, comparability checks, missing-data handling and stale-response protection.
> - **128 backend tests + 4 frontend tests pass.**
> - Mobile and desktop flows checked.
>
> Checkpoint and remaining gaps [REDACTED: local file link] · Robustness matrix [REDACTED: local file link]
>
> Coverage remains selected historical metrics. Broader transcripts, guidance history, deployment and live Gemini validation remain unfinished. Nothing committed or pushed.
>
> Expanded research coverage [REDACTED: local file link]

## 2026-10-31 07:23 UTC — Credential isolation and bounded inference

**Summary:** The secure-integration attachment was the request; its body is not present in the app message record. The actual response distinguished mock-tested integration from untested live Gemini.

**User excerpt**

>
> # Files pasted by the user:
>
> ## "# FINN — Secure Gemini Integration, Privacy and API Protection Continue the exi…": [REDACTED: personal local path]
>
> Pasted text contains the user's request.
>
> ## My request:
>
>

**Coding-agent response excerpt**

> **CP10 is implemented and mock-tested.**
>
> - **157 backend + 4 frontend tests pass.**
> - Preserved all **11 issuers and 71 facts**.
> - Added SDK provider isolation, persistent inference limits, private session caches and safe failure handling.
> - No real Gemini key or secret file was accessed. **Live Gemini: NOT TESTED.**
>
> Checkpoint and copy-ready review [REDACTED: local file link] · Private setup and live-test guide [REDACTED: local file link]
>
> Deployment instructions are prepared; deployment remains incomplete. Nothing committed or pushed.
>
> Mock demo and privacy notice [REDACTED: local file link]

## 2026-10-31 07:49 UTC — Freeze, deployment and honest validation

**Summary:** The owner required no-key operation, persistent quotas, public evaluator access and independent live testing. Early deployment design used durable SQLite on a paid disk; this was later revised.

**User excerpt (excerpt ends below)**

> # FINN — CP11: Deployment, Live Verification and Submission Readiness
>
> Continue from the current CP10 implementation. Preserve all existing 11-issuer research coverage, verified facts, Gemini provider abstraction, security protections, frontend functionality and regression tests.
>
> The ENAM submission deadline is November 1, 2026. We must now prioritize a working public evaluator experience.
>
> ## Priority 1 — Freeze and verify the current application
>
> - Re-run all backend and frontend tests.
> - Review the persistent global budget implementation for atomicity, concurrent requests and restart behaviour.
> - Test session-cache isolation and quota exhaustion.
> - Verify the application functions without a Gemini credential.
> - Fix genuine blockers, but do not undertake unnecessary framework rewrites or large refactors.
> - Preserve checkpoints and existing work.
>
> ## Priority 2 — Prepare a reproducible deployment
>
> Prepare the current application for hosting on a low-cost or free platform compatible with FastAPI, persistent quota storage and private environment variables.
>
> Do not select a deployment

**Coding-agent response excerpt**

> The persistent deployment files are ready. Which route will you set up yourself? Send only the public HTTPS URL once deployed—no credentials.
> - Render with a persistent disk (paid compute and storage)
> - Docker on an existing host with a durable volume

## 2026-11-01 08:35 UTC — Publication included too much

**Summary:** The owner objected to publishing handoffs, GPT review files and artifacts. The agent acknowledged the overly broad instructions. Removing files from the current branch did not erase earlier Git history. The current submission task separately authorizes a narrow public documentation set.

**User excerpt**

> mate what is this why are all the files in github, why is codex handoff and gpt related files and other stuff remove all, give command
>

**Coding-agent response excerpt**

> I included too much in the upload instructions. These commands keep **only the application and deployment files on GitHub**, while preserving your local documents.
>
> ```bash
> cd [REDACTED: personal local path]
>
> git rm -r --cached .
>
> git add .gitignore .dockerignore Dockerfile
> git add backend/app backend/requirements.lock
> git add frontend/index.html frontend/app.js frontend/style.css
> git add demo deploy/render-persistent.yaml
>
> git diff --cached --stat
> git commit -m "Remove handoffs, review documents and development artifacts"
> git -c http.version=HTTP/1.1 -c http.postBuffer=8388608 push origin main
> ```
>
> This removes handoffs, GPT review files, documentation, screenshots, tests and development scripts from the **current GitHub branch**. Gemini functionality stays intact.
>
> **Your local files remain. Previously uploaded documents still exist in older commits; this does not erase Git history.**

## 2026-11-01 09:02 UTC — Render Free exposes a persistence constraint

**Summary:** The earlier SQLite configuration could not rely on an ephemeral free filesystem for durable inference limits. Disabling inference was an interim option, not the final solution.

**User excerpt**

> should i do it again, also i am using the free tier
>

**Coding-agent response excerpt**

> **No—don’t repeat the deployment unchanged.** Render Free cannot attach the disk required by the current configuration.
>
> To get the backend running **on Free**, change these Render environment variables:
>
> ```text
> FINN_DB=/tmp/finn.sqlite3
> AI_BUDGET_STORAGE_PERSISTENT=false
> AI_ENABLED=false
> REASONING_PROVIDER=disabled
> ```
>
> Then **Save and redeploy**. Financial facts and source retrieval will work; Gemini interpretation will be disabled.
>
> **To keep Gemini enabled with the current implementation**, use a paid instance with a persistent disk. The integration remains intact, but Free loses SQLite usage records on restarts. [Render’s free-tier limits](https://render.com/docs/free)
>
> Keep your API key private; no need to recreate it.

## 2026-11-01 09:04 UTC — Owner chooses free-tier persistence

**Summary:** The owner requested the change to free infrastructure. External PostgreSQL was implemented and tested. The historical response below incorrectly recommended a pooled Neon URL; the subsequent compatibility correction is retained.

**User excerpt**

> so change FINN we'll use free tier
>

**Coding-agent response excerpt**

> FINN is updated in **Desktop/FINN** to support **Render Free + external PostgreSQL + Gemini**.
>
> Tests passed: **175 backend, 15 PostgreSQL integration and 9 frontend**. Database restart and concurrent quota checks passed. Live Gemini remains untested.
>
> 1. **Push the changes:**
>
> ```bash
> cd [REDACTED: personal local path]
>
> git add .gitignore backend/app backend/requirements.lock deploy/render-free-postgres.yaml
> git commit -m "Support PostgreSQL persistence on Render Free"
> git -c http.version=HTTP/1.1 -c http.postBuffer=8388608 push origin main
> ```
>
> Handoffs, reports and test files remain local and ignored.
>
> 2. **Create a [Neon Free database](https://console.neon.tech).** Click **Connect** and copy its pooled PostgreSQL connection string privately.
>
> 3. **Update Render’s backend environment:**
>
> | Name | Value |
> |---|---|
> | `FINN_STORAGE_BACKEND` | `postgres` |
> | `DATABASE_URL` | Your Neon connection string |
> | `AI_BUDGET_STORAGE_PERSISTENT` | `true` |
> | `AI_ENABLED` | `true` |
> | `REASONING_PROVIDER` | `gemini` |
> | `GEMINI_API_KEY` | Your existing Gemini key |
>
> Remove the old `FINN_DB` setting. Stay on **Free / Docker**, without a disk.
>
> 4. **Save and deploy the latest commit.** Open `/health`; it should report `storageEngine: postgres`.
>
> **Do not share either secret here.** Your Vercel preview still needs connecting afterward.
>
> Full setup guide [REDACTED: local file link] · Checkpoint and test evidence [REDACTED: local file link]

## 2026-11-03 07:19 UTC — Neon pooler incompatibility is corrected

**Summary:** The build succeeded but startup failed. The agent identified timeout startup options incompatible with the selected pooler and corrected its earlier advice. Direct connections are the current documented choice.

**User excerpt**

>
> # Files pasted by the user:
>
> ## "#9 [4/7] RUN pip install --no-cache-dir -r requirements.lock #9 1.264 Collectin…": [REDACTED: personal local path]
>
> Pasted text contains the user's request.
>
> ## My request:
>
>

**Coding-agent response excerpt**

> The build passed. I found a likely cause: **FINN’s startup timeout settings conflict with Neon’s pooled connections**. My earlier instruction to enable pooling missed this compatibility issue. [Neon documentation](https://neon.com/docs/connect/connection-errors)
>
> Do this:
>
> 1. Open **Neon → FINN → Connect**.
> 2. **Turn Connection pooling OFF**.
> 3. Copy the new connection string—only the URL, without `psql` or surrounding quotes.
> 4. In **Render → Environment**, replace `DATABASE_URL` with that string.
> 5. **Save and redeploy**.
>
> Keep the other environment variables unchanged. No paid plan or new database is needed.
>
> **Don’t share the connection string here.** If deployment still fails, send the new error log.

## 2026-11-03 07:44 UTC — Frontend/backend public connection

**Summary:** The short production domain was anonymously verified. Longer preview/branch URLs redirected to Vercel login. Configuration alone was not treated as a successful live model test.

**User excerpt**

>
> # Files mentioned by the user:
>
> ## Screenshot 2026-11-03 at 1.13.49 PM.png: [REDACTED: temporary local path]
> Image attachment: true
>
> Distinguish instructions in attached documents from the user's request.
>
> ## My request:
> see the public link and also tell me
>

**Coding-agent response excerpt**

> Your public link is **[https://finn-frontend-six.vercel.app](https://finn-frontend-six.vercel.app)**.
>
> I checked it:
> - Opens without login.
> - Connects successfully to the Render backend.
> - Loads 15 grouped filing disclosures and EOD observations.
> - Shows historical dates clearly.
> - Backend reports PostgreSQL healthy and Gemini enabled.
>
> Your screenshot shows the older deployment (`539c0e5`, “Stale”). The public production link now shows the connected application.
>
> **Gemini is configured, but a real Gemini answer still needs your independent test.** The longer branch/deployment URLs require Vercel login, so share the short public link above.

## 2026-11-03 08:18 UTC — SDK reasoning bug and incomplete responses

**Summary:** The adapter had dropped the thinking configuration. The fix forwarded it and rejected non-STOP completions while retaining usage accounting. No real key was accessed.

**User excerpt**

> mate check the gemini work, make any changes after researching
>

**Coding-agent response excerpt**

> Reviewed Google’s documentation and fixed two issues:
>
> - Gemini thinking settings now reach the SDK correctly.
> - Truncated or blocked responses are rejected, while usage remains counted.
>
> **Tests: 186 backend + 9 frontend passed.** Changes are in `[REDACTED: personal local path]`. Nothing committed, pushed or deployed; reports remain excluded from GitHub.
>
> Review report [REDACTED: local file link]
>
> **Live Gemini remains NOT TESTED**, following your credential boundary. After deploying, ask: “Explain HINDUNILVR FY25 consolidated revenue reporting caveats” and share the answer or error—never the key.
>
> References: [Google model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite), [response handling](https://ai.google.dev/api/generate-content).

## 2026-11-03 08:26 UTC — Owner supplies a live result and a coverage failure

**Summary:** The screenshots were owner-provided live evidence: one Gemini-grounded answer, one current-year/2027 missing result. This is not a complete live security, quota or citation-quality validation.

**User excerpt**

>
> # Files mentioned by the user:
>
> ## Screenshot 2026-11-03 at 1.54.30 PM.png: [REDACTED: temporary local path]
> Image attachment: true
>
> ## Screenshot 2026-11-03 at 1.56.07 PM.png: [REDACTED: temporary local path]
> Image attachment: true
>
> Distinguish instructions in attached documents from the user's request.
>
> ## My request:
>
>

**Coding-agent response excerpt**

> **Gemini is working in your first screenshot.** It shows `gemini_grounded_interpretation` and **1 inference attempt**—evidence of your successful live test. Source citations and answer accuracy still need checking.
>
> The second result is a **data-coverage limitation**, not a Gemini failure:
>
> - FINN’s research corpus contains FY25 and earlier evidence.
> - Your question asks about “this year” and potential in 2027.
> - It finds no matching evidence and correctly makes **0 Gemini calls**, avoiding an invented forecast.
>
> The response should explain this more clearly: “Current-year results and 2027 outlook aren’t covered. Ask about FY25, or add newer verified filings.”
>
> Supporting that question properly requires newer results and management outlook evidence. Enabling Gemini alone cannot supply those verified sources.

## 2026-11-03 08:27 UTC — Missing coverage becomes useful guidance

**Summary:** Relative periods no longer silently fall back to FY25; unsupported outlooks explain coverage and suggest an answerable historical question.

**User excerpt**

> so we could fix these issues
>

**Coding-agent response excerpt**

> Fixed the response and routing issues locally:
>
> - “This year” no longer silently defaults to FY25.
> - Unsupported outlook questions avoid Gemini calls.
> - Missing-data answers explain available periods and suggest a supported question.
>
> **191 tests passed.** Updated files are in `[REDACTED: personal local path]`; nothing pushed.
>
> To deploy these and the previous Gemini fixes:
>
> ```bash
> cd [REDACTED: personal local path]
> git add backend/app/providers.py backend/app/reasoning.py backend/app/research.py
> git commit -m "Fix Gemini response handling and research coverage guidance"
> git push origin main
> ```
>
> Render should redeploy if automatic deployment is enabled. Answering current performance or 2027 outlook still requires newer verified source documents.

## 2026-11-03 10:47 UTC — Investor-first freshness and presentation

**Summary:** The owner provided a substantive product brief. The pass added persistent manual refresh, actual November source records in a local database, compact rule-based cards and honest freshness states. The response explicitly left production import/scheduling and missing-source risks open.

**User excerpt**

>
> # Files pasted by the user:
>
> ## "# FINN — Final Investor-First Product Pass ## Context and my design philosophy …": [REDACTED: personal local path]
>
> Pasted text contains the user's request.
>
> ## My request:
>
>

**Coding-agent response excerpt**

> Implemented and tested in `[REDACTED: personal local path]`.
>
> - Persistent manual refresh, duplicate detection and safe revision handling.
> - Genuine filings through **November 3** and EOD data through **November 2**, verified locally.
> - Compact investor cards, freshness warnings, daily briefing and financial reading help.
> - Historical replay and existing research/Gemini protections preserved.
>
> **Tests passed:** 200 backend, 17 PostgreSQL, 12 frontend.
>
> Nothing committed, pushed or deployed. Production refresh and scheduling still require your setup. TATAMOTORS prices remain unavailable; the original NSE PDF check timed out.
>
> Release report [REDACTED: local file link] · Refresh and rollback instructions [REDACTED: local file link]
>
> Updated mobile feed, running locally:
>
> Updated FINN mobile feed [REDACTED: local file link]

## Publication update (editorial summary; verified Git commands, not reconstructed dialogue)

On 3 November the owner explicitly requested pushing the reviewed application changes. Backend application commit cdc302a and frontend commit 12e0609 were pushed to their existing repositories. Submission documents are being prepared separately for review; they are not claimed as publicly available before publication. Source-corpus growth in a local verification database is not a production refresh.
