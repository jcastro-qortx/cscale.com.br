# CoreScale Site Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the existing CoreScale Hugo site's conversion, accessibility, SEO, content automation, and build hygiene while preserving its visual identity, commercial claims, AWS deployment model, and pre-existing local changes.

**Architecture:** Extend the existing Hugo templates rather than replacing them. Add a small structural test script that builds the site into a temporary directory and asserts required HTML behavior, then implement each improvement against those tests. Keep styling changes limited to shared accessibility and form-state rules.

**Tech Stack:** Hugo 0.163+, Go templates, HTML, CSS, vanilla JavaScript, POSIX shell.

## Global Constraints

- Preserve the current layout, palette, typography, hierarchy, and AWS deployment architecture.
- Preserve all commercial metrics and claims, with a discreet qualification note.
- Preserve all pre-existing working-tree changes and do not deploy to AWS.
- Do not add analytics, CRM, consent-manager, or JavaScript framework dependencies.
- Do not broadly refactor inline styles.
- Do not delete a static asset unless repository-wide reference checks prove it unused.

---

### Task 1: Structural regression harness and clean Hugo configuration

**Files:**
- Create: `tests/site-audit.sh`
- Modify: `hugo/hugo.toml`
- Create: `hugo/layouts/categories/terms.html`
- Create: `hugo/layouts/categories/taxonomy.html`

**Interfaces:**
- Consumes: Hugo templates and content under `hugo/`.
- Produces: `tests/site-audit.sh`, which builds to a temporary directory and validates generated HTML with `rg` assertions.

- [ ] **Step 1: Write the failing structural test**

Create a shell test that builds with `--printPathWarnings`, captures warnings, and asserts that generated category pages exist and contain a heading and article links.

- [ ] **Step 2: Verify the test fails**

Run: `bash tests/site-audit.sh`

Expected: non-zero exit because taxonomy templates and later required markup are absent.

- [ ] **Step 3: Implement the Hugo configuration and taxonomy templates**

Replace deprecated `languageCode = "pt-br"` with `locale = "pt-BR"`. Add category term and taxonomy templates that reuse the shared header/footer, expose one `h1`, and render linked article cards.

- [ ] **Step 4: Verify the configuration slice passes**

Run the build portion and taxonomy assertions from `tests/site-audit.sh`.

Expected: Hugo exits 0 without the deprecated-key or missing-taxonomy-layout warnings.

### Task 2: SEO metadata and structured data

**Files:**
- Modify: `hugo/layouts/_default/baseof.html`
- Modify: `hugo/hugo.toml`

**Interfaces:**
- Consumes: `.Title`, `.Description`, `.Permalink`, `.IsPage`, `.Section`, `.Date`, `.Params`, and global site params.
- Produces: canonical, Open Graph, X/Twitter, and JSON-LD metadata in every generated page.

- [ ] **Step 1: Add failing metadata assertions**

Assert that home and article output contain an absolute canonical URL, description fallback, `og:title`, `og:description`, `og:url`, `og:image`, `twitter:card`, and valid organization/article JSON-LD markers.

- [ ] **Step 2: Verify metadata assertions fail**

Run: `bash tests/site-audit.sh`

Expected: non-zero exit at the first missing canonical/Open Graph assertion.

- [ ] **Step 3: Implement metadata**

Define template variables for title, description, canonical URL, type, and social image. Render escaped meta tags and one JSON-LD object appropriate to the page type. Add organization contact and social profile parameters to `hugo.toml`.

- [ ] **Step 4: Verify metadata assertions pass**

Run: `bash tests/site-audit.sh`

Expected: metadata checks pass and the script proceeds to later failing assertions.

### Task 3: Accessible navigation and shared interaction states

**Files:**
- Modify: `hugo/layouts/_default/baseof.html`
- Modify: `hugo/layouts/partials/rd-header.html`
- Modify: `hugo/layouts/partials/rd-footer.html`

**Interfaces:**
- Consumes: existing `rm-menu-btn`, `rm-mobile-nav`, `data-hover`, and `data-focus` hooks.
- Produces: `#conteudo-principal`, skip link, visible focus, accurate menu ARIA state, Escape behavior, and accessible external-link names.

- [ ] **Step 1: Add failing accessibility assertions**

Assert generated home HTML includes a skip link, main landmark target, `aria-controls`, initial `aria-expanded="false"`, an `aria-label` on the floating WhatsApp link, and accessible labels on social links.

- [ ] **Step 2: Verify accessibility assertions fail**

Run: `bash tests/site-audit.sh`

Expected: non-zero exit because the skip link and ARIA state are absent.

- [ ] **Step 3: Implement accessible navigation**

Wrap the Hugo main block in `<main id="conteudo-principal">`, add the skip link and global `:focus-visible` styles, update menu attributes in markup and JavaScript, close on Escape, restore focus, and provide explicit link labels.

- [ ] **Step 4: Verify accessibility assertions pass**

Run: `bash tests/site-audit.sh`

Expected: accessibility checks pass and the script proceeds.

### Task 4: Accessible, bot-resistant contact form

**Files:**
- Modify: `hugo/layouts/index.html`
- Modify: `hugo/layouts/_default/baseof.html`

**Interfaces:**
- Consumes: existing API endpoint and fields `nome`, `email`, and `telefone`.
- Produces: API JSON `{name, email, message, website}` using the actual honeypot value and an in-page status region.

- [ ] **Step 1: Add failing form assertions**

Assert labels use `for`, fields have matching `id`, required/autocomplete attributes exist, `website` is a real input, a privacy link exists, and an `aria-live` status node exists. Assert JavaScript reads `website` instead of hard-coding it.

- [ ] **Step 2: Verify form assertions fail**

Run: `bash tests/site-audit.sh`

Expected: non-zero exit on missing field associations or honeypot.

- [ ] **Step 3: Implement form behavior**

Add semantic fields and the visually hidden honeypot. Use native `checkValidity()`/`reportValidity()`, render progress/success/error messages in the status node, safely parse JSON responses, preserve user input after errors, and clear only after success.

- [ ] **Step 4: Verify form assertions pass**

Run: `bash tests/site-audit.sh`

Expected: all form structural assertions pass.

### Task 5: Dynamic home content and claim qualification

**Files:**
- Modify: `hugo/layouts/index.html`

**Interfaces:**
- Consumes: `where .Site.RegularPages "Section" "blog"`, article dates, categories, and reading time.
- Produces: the latest three published blog cards on the home page and a discreet claim qualification note.

- [ ] **Step 1: Add failing content assertions**

Assert the template contains a Hugo query for blog pages, no hard-coded article URLs in the home card block, and the generated home contains the three newest article titles plus a qualification note.

- [ ] **Step 2: Verify content assertions fail**

Run: `bash tests/site-audit.sh`

Expected: non-zero exit because the cards are hard-coded and no note exists.

- [ ] **Step 3: Implement dynamic cards and note**

Replace the three literal cards with a ranged collection sorted by date descending and limited to three. Render category, localized date, reading time, title, and relative permalink. Add one compact note below the metrics.

- [ ] **Step 4: Verify content assertions pass**

Run: `bash tests/site-audit.sh`

Expected: dynamic content and note assertions pass.

### Task 6: Image hints and safe static-asset cleanup

**Files:**
- Modify: `hugo/layouts/index.html`
- Modify: `hugo/layouts/partials/rd-header.html`
- Modify: `hugo/layouts/partials/rd-footer.html`
- Modify: `hugo/layouts/partials/rd-nossa-historia.html`
- Delete only if still unreferenced: `hugo/static/header.mp4`
- Delete only if still unreferenced: `hugo/static/yas.mov`

**Interfaces:**
- Consumes: existing static images and repository-wide reference search.
- Produces: stable image layout hints and a smaller deploy artifact without visual changes.

- [ ] **Step 1: Add failing image assertions**

Assert non-hero content images carry `loading="lazy"` and `decoding="async"`, while above-the-fold brand imagery is eager. Assert generated output contains no references to candidate obsolete videos.

- [ ] **Step 2: Verify image assertions fail**

Run: `bash tests/site-audit.sh`

Expected: non-zero exit because lazy/decoding hints are missing.

- [ ] **Step 3: Add image hints and confirm asset references**

Add intrinsic dimensions where known and loading/decoding attributes based on viewport importance. Run `rg -n "header\\.mp4|yas\\.mov" .`; delete each candidate only if the command confirms no project reference outside documentation or the asset itself.

- [ ] **Step 4: Verify image and artifact checks pass**

Run: `bash tests/site-audit.sh`

Expected: image assertions pass and Hugo output does not reference deleted assets.

### Task 7: Final verification and preservation audit

**Files:**
- Modify only if verification exposes a defect in files already listed above.

**Interfaces:**
- Consumes: complete working tree and structural test harness.
- Produces: evidence that the approved scope works and pre-existing changes remain present.

- [ ] **Step 1: Run the full structural suite**

Run: `bash tests/site-audit.sh`

Expected: exit 0 with explicit success output.

- [ ] **Step 2: Run a clean production build**

Run: `hugo --source hugo --destination /tmp/corescale-site-final --cleanDestinationDir --minify`

Expected: exit 0 with no project warnings.

- [ ] **Step 3: Check whitespace and inspect the full diff**

Run: `git diff --check && git status --short && git diff --stat && git diff -- hugo/layouts hugo/hugo.toml tests`

Expected: no whitespace errors; only approved files changed by this implementation, alongside the user's pre-existing modifications and untracked files.

- [ ] **Step 4: Report without deploying**

Summarize implemented behavior, verification evidence, files affected, preserved local work, and any remaining commercial/source follow-up. Do not run deployment scripts or change AWS resources.
