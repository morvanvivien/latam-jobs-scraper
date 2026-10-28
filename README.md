# How to Scrape Bumeran, Zonajobs, Laborum & Multitrabajos: LatAm Job Postings

> **Run it now, no code: [latam-jobs-bumeran-scraper on the Apify Store](https://apify.com/bibian/latam-jobs-bumeran-scraper)** &nbsp;|&nbsp; no browser needed for most countries &nbsp;|&nbsp; ~70,000 live jobs

Bumeran, Zonajobs, Laborum, Multitrabajos and Konzerta are Latin America's leading job boards, and they all share the same underlying platform (Navent/Grupo ZAP). None of them has a public export or an official API for third parties. This guide shows how to get their postings as clean structured data in a single run: company, location, work mode and full description, with a free Apify Actor, from the console or from code.

Searches this page answers: bumeran scraper, zonajobs scraper, laborum scraper, latam jobs scraper, scrape jobs argentina chile peru.

## What you get from this scraper

- Every job posting matching your keywords, across one or several countries, newest first.
- Company name (or `confidentialCompany: true` when the employer hides it), location, work type and work mode (remote, hybrid, on site).
- Number of vacancies, publication and update dates.
- Optional full description as plain text.

| Country | Job board | Live postings (Oct 2026) |
|---|---|---|
| Argentina | Bumeran, Zonajobs | ~9,700 |
| Chile | Laborum | ~16,500 |
| Peru | Bumeran | ~35,000 |
| Ecuador | Multitrabajos | ~5,800 |
| Panama | Konzerta | ~3,000 |
| Venezuela | Bumeran | ~700 |

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results from Argentina, personal data removed, long texts truncated) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url` | Posting id and public link |
| `country`, `jobBoard` | Which country and which board served the posting |
| `title`, `companyName`, `confidentialCompany` | Job title and hiring company; company is empty when published confidentially |
| `location`, `workType`, `workMode` | Where the job is based, contract type and remote/hybrid/on site |
| `vacancies`, `suitableForDisabled` | Number of open positions, accessibility flag |
| `publishedAt`, `updatedAt` | Local timestamps for the job board |
| `description` | Plain text, only when full descriptions are enabled |

## Use cases

- **Monitor hiring across Latin America.** Track new postings by country and keyword, every day.
- **Build a daily job alert.** Schedule a run every morning with "published within 1 day" and send only the new jobs to Slack, e-mail or a Google Sheet.
- **Find the companies that are hiring.** List which employers recruit for a given role across several countries at once.
- **Study the LatAm job market.** Work modes, contract types and locations in one dataset instead of five separate sites.

## Input

| Field | What it does |
|---|---|
| `countries` | One or several of `argentina`, `chile`, `peru`, `ecuador`, `panama`, `venezuela`. Default: Argentina. |
| `keywords` | Job title or skill, for example `desarrollador` or `enfermera`. Uses the job boards' own search. Empty means every posting. |
| `publishedWithinDays` | Keep only postings published in the last N days. Use `1` for a daily monitoring run. |
| `maxItems` | The run stops once this many postings are saved, across all countries (default 50). |
| `includeDescriptions` | Adds the full job description as plain text. |

Example input:

```json
{
  "countries": ["argentina", "chile"],
  "keywords": "desarrollador",
  "publishedWithinDays": 7,
  "maxItems": 100,
  "includeDescriptions": true
}
```

## Four ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/latam-jobs-bumeran-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (countries, keywords and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/latam-jobs-bumeran-scraper').call({
    "countries": ["argentina", "chile"],
    "keywords": "desarrollador",
    "publishedWithinDays": 7,
    "maxItems": 100,
    "includeDescriptions": true
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.companyName ?? 'confidential'} | ${item.location} | ${item.country}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/latam-jobs-bumeran-scraper").call(run_input={
    "countries": ["argentina", "chile"],
    "keywords": "desarrollador",
    "publishedWithinDays": 7,
    "maxItems": 100,
    "includeDescriptions": True,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['title']} | {item.get('companyName') or 'confidential'} | {item.get('location')} | {item.get('country')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

### 4. REST API on RapidAPI, one key for all your APIs

If you already use RapidAPI, the same data is available as a plain REST API with monthly plans and a free tier: [latam-jobs-bumeran-zonajobs-laborum on RapidAPI](https://rapidapi.com/VivienMORVAN/api/latam-jobs-bumeran-zonajobs-laborum), also listed on [Zyla API Hub](https://zylalabs.com/api-marketplace/company+data/latam+job+postings+api/14513). No Apify account needed, billing goes through your marketplace subscription.

```bash
curl -X POST "https://latam-jobs-bumeran-zonajobs-laborum.p.rapidapi.com/v2/acts/bibian~latam-jobs-bumeran-scraper/run-sync-get-dataset-items?clean=true" \
  -H "x-rapidapi-key: <YOUR_RAPIDAPI_KEY>" \
  -H "x-rapidapi-host: latam-jobs-bumeran-zonajobs-laborum.p.rapidapi.com" \
  -H "content-type: application/json" \
  -d '{"countries": ["argentina"], "keywords": "desarrollador", "maxItems": 50}'
```

The response is the JSON array of postings, with the same fields as above.

## Pricing

Pay per result, in line with the price shown on the [Store page](https://apify.com/bibian/latam-jobs-bumeran-scraper) when this guide was written; the Store page is the reference. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results.

## Why this one

- **Five job boards, one actor.** Bumeran, Zonajobs, Laborum, Multitrabajos and Konzerta in a single run instead of five separate tools.
- **No browser for most countries.** Only the boards that actively block Apify's cloud addresses (mainly Laborum) fall back to a proxy automatically.
- **Confidential employers handled explicitly.** `confidentialCompany: true` instead of an empty field you have to guess the meaning of.

## Limits and honest notes

- Up to 100 postings per request: large extractions are fast and cheap.
- If a job board refuses Apify's cloud addresses (Laborum often does), the Actor switches that board to Apify Proxy automatically.
- When an employer publishes confidentially, `companyName` is empty and `confidentialCompany` is `true`.
- Dates are local to each job board, not normalized to a single timezone.
- No candidate or recruiter personal data is collected.
- This is an unofficial tool, not affiliated with Navent, Bumeran, Zonajobs, Laborum, Multitrabajos or Konzerta. Check each site's terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**  
Not for most countries. The Actor reads the data directly; it only falls back to Apify Proxy for the boards that block direct cloud requests.

**How do I only get new jobs every day?**  
Set `publishedWithinDays` to `1` and schedule the Actor once a day.

**Can I collect several countries in the same run?**  
Yes, set `countries` to an array, for example `["argentina", "chile", "peru"]`.

**Can I get the data in Excel or Google Sheets?**  
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open latam-jobs-bumeran-scraper on the Apify Store](https://apify.com/bibian/latam-jobs-bumeran-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
