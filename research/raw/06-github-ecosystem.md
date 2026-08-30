# The Open-Source / GitHub Ecosystem for Image-Based Profiling and Instagram Visual Analysis

**Research date:** 2026-08-30
**Method:** GitHub repo search + code search via the GitHub API (MCP), plus web search where GitHub search returned nothing. Star counts, `pushed_at` (true last-commit date, not the misleading `updated_at`), license SPDX id and archive status pulled from the GitHub REST repo objects. Where a repo could not be resolved via the API, it is marked.

**The short answer to "is there nothing on GitHub about this?":**
There is a *lot* on GitHub about every individual **step**. There is essentially **nothing** about the **whole**. The academic personality-from-images literature has almost no surviving code; the marketing/brand visual-analytics literature has literally none. The infrastructure (CLIP, IQA, dedup, structured decoding, dataset curation) is excellent, maintained, and permissively licensed. The domain layer — schema, aggregation, calibration, evidence linkage, refusal — does not exist in any repo I could find.

---

## 1. Personality prediction from images / social media

### Verdict for the category: **near-total abandonware.**

A GitHub repo search for `automatic personality recognition` returns **12 repos total, none above 2 stars**. `personality prediction instagram images` returns **2 repos, 3★ and 2★**. `apparent personality analysis first impressions chalearn` returns **1 repo, 3★**. This is not a search artifact — this is the whole field's public code footprint.

| Repo | ★ | Last commit | License | Lang | What it does | Verdict |
|---|---|---|---|---|---|---|
| `liaorongfan/DeepPersonality` | 70 | 2024-10-07 | MIT | Python | The only real one. "An Open-source Benchmark of Deep Learning Models for Audio-visual Apparent and Self-reported Personality Recognition." 18 model configs (visual / audio / multimodal), configs + pretrained weights + notebooks, evaluated on ChaLearn First Impressions V2 and UDIVA. 434 commits. | **Needs work.** Best available artifact by a wide margin. But: video-first (not still images), requires ChaLearn/UDIVA under data agreements you must apply for, README still lists unfinished TODOs ("pip install testing", "notebook tutorials"), 14 open issues, dormant ~2 years. |
| `aimclub/OCEANAI` | 65 | 2025-12-05 | BSD-3-Clause | Python | Multimodal (video + audio + text) Big Five estimation, pip-installable, real docs at oceanai.readthedocs.io. Framed explicitly as "ranking potential candidates to perform professional responsibilities." | **Usable but do not touch for hiring.** The code is the most professionally packaged in this category. The stated use case (automated candidate ranking) is an EU AI Act Annex III high-risk employment application. Also needs a talking-head video, not a photo feed. |
| `grimmdaniel/personality-trait-prediction` | 20 | 2021-01-14 | none | Jupyter | Big Five on First Impressions V2 with VGG16/ResNet50 + MFCC audio. | **Abandoned.** No license = legally unusable. Coursework. |
| `pascalmi/chalearn_first_impression` | 8 | 2021-07-23 | MIT | Python | Big Five from facial images (stills, not video). | **Abandoned**, but MIT and the closest thing to a stills-only reference implementation. |
| `raoulg/PsychoFlickr` | 7 | 2017-07-31 | none | C++/Matlab | Feature extraction for the PsychoFlickr corpus (Segalin et al.), "updated for Matlab R2017a". | **Abandoned.** Matlab, 2017, no license. It is the *feature extractor*, not the trait model. |
| `frkngrpnr/lapfi` | 3 | 2017-06-09 | GPL-3.0 | Matlab | An entry (not a winning one) in ChaLearn LAP Apparent Personality Analysis: First Impressions, ICPR 2016. | **Abandoned.** Historical interest only. |
| `KRKarthik5/Predicting-Personality-Traits` | 5 | 2020-02-29 | none | Jupyter | ChaLearn FI with facial + gaze modalities. | **Abandoned.** |
| `RanimBenMbarek/Personality-Prediction-of-Instagram-Users` | 3 | 2024-10-08 | none | Jupyter | OCEAN from Instagram posts, image + text. | **Student project.** No license, no eval you can trust. |
| `HediKhemiri3001/instagram-profile-personality-classifier` | 2 | 2023-10-06 | none | Jupyter | Same idea, NLP + image + multimodal. | **Student project.** |
| `atefeh-alimohammadi/Personality-Traits-Recognition` | 0 | 2026-01-03 | — | Python | Visual-feature fusion on ChaLearn FI. Created Dec 2025. | **Unproven.** Too new, zero adoption. |
| `jkwieser/personality-prediction-from-text` | 176 | active (2026-07) | — | Jupyter | Big Five **from text**. The most-starred thing in the whole personality-prediction space. | Adjacent — text only. Noted because it shows where the community's attention actually went. |

### The ChaLearn First Impressions winning entries: **not on GitHub.**
The 2016 ICPR challenge was won by NJU-LAMDA (Deep Bimodal Regression), with evolgen and DCC placing; BU-NKU won the 2017 CVPR second round. I searched `chalearn personality`, `first impressions personality video regression`, `deep impression bimodal personality`, and `apparent personality analysis first impressions chalearn`. **None of the winning entries has a public repository.** `frkngrpnr/lapfi` (3★, Matlab, 2017) is the only challenge-participant codebase on GitHub, and it did not win. If you want the winning architectures you are reading the papers and reimplementing, or you are using `DeepPersonality`, which reimplements several of them as baselines.

### Papers with no code at all
- **Segalin et al., "The Pictures We Like Are Our Image"** (IEEE TAC 2017, PsychoFlickr, 60k images / 300 users): no implementation repo. Only `raoulg/PsychoFlickr` (7★, Matlab, 2017), which is a feature-extraction port, not the trait-mapping model.
- **Ferwerda & Schedl, "Using Instagram Picture Features to Predict Users' Personality"**: no repo. Confirmed by web search — the author's GitHub has nothing matching, and the dataset was collected under the now-dead Instagram API with per-user consent.
- **MM-OCEAN**: a GitHub *code* search for the literal string `"MM-OCEAN"` returns **3 hits, all irrelevant** (a filament-color JSON, a route-optimizer component, an unrelated spec doc). It does not exist as public code. The nearest real thing is `aimclub/OCEANAI` above.

---

## 2. Instagram data collection

**The single most important fact:** the official API and the scrapers solve *different problems*, and only one of them can legally reach a third-party account.

### Officially sanctioned path
Meta deprecated the Instagram Basic Display API. What remains is **Instagram API with Instagram Login** and **Instagram API with Facebook Login** (Graph API). Both only reach accounts that have **authorized your app**. For accounts that have not, the only sanctioned surface is **Business Discovery**, which returns a limited public field set for another *Business or Creator* account: username, biography, website, profile picture, followers_count, follows_count, media_count, and recent media. Hashtag search is capped at **30 unique hashtags per week per account**. There is no follower list, no audience data, no arbitrary personal-account access.

**Consequence:** for your own account, or a client account that grants a token, there is a clean legal path that gets you the images. For a competitor or a cold influencer prospect, the sanctioned path gets you counts and a thumbnail-grade recent-media list — enough for a light visual read, not a deep one.

### Official Graph API wrappers on GitHub: **the category is a desert**
A search for `instagram graph api wrapper` returns **11 repos total**. The top result has **14 stars**.

| Repo | ★ | Last activity | License | Lang | Verdict |
|---|---|---|---|---|---|
| `abjerner/Skybrud.Social.Instagram` | 14 | 2025-12 | — | C# | Best-maintained official-API wrapper on GitHub. That is a damning sentence. |
| `MatthieuThib/pystagram` | 8 | 2025-11 | — | Python | Basic Display + Graph. **Needs work**, but the only Python option with any signal. |
| `ckoutavas/SocialMediaAnalytics` | 4 | 2025-10 | — | Python | Meta Graph wrapper for *your own* connected FB/IG business accounts' post analytics over time. Tiny but on-point. |
| `NextFaze/instagram-graph-sdk` | 8 | 2023-04 | — | TS | Abandoned. |
| others (`insta-nova`, `grpi`, `InstagramGraphAPI`, ...) | 0–1 | various | — | — | **Vaporware.** |

**Practical verdict: write raw HTTP against `graph.facebook.com` yourself.** There is no maintained client worth a dependency. The API surface is small enough that a wrapper is ~200 lines.

### Scrapers (unofficial — all violate Instagram's automated-access terms)

| Repo | ★ | Last commit | License | Lang | What it does | ToS / legal | Verdict |
|---|---|---|---|---|---|---|---|
| `instaloader/instaloader` | 13,258 | 2026-07-26 | MIT | Python | Downloads posts, stories, highlights, captions and metadata from public (and, logged-in, private) profiles via the web/GraphQL endpoints. Excellent library API, not just a CLI. | **Unsanctioned.** Violates IG's automated-access clause. Anonymous rate ceiling is now ~1–2 requests / 30s and falling; `doc_id`s get revoked and break `get_posts()` for everyone (401 for all users, patched reactively). Cookie import from a browser is the standard workaround, which means you're using your logged-in identity. | **Usable, with eyes open.** Actively maintained, MIT, the cleanest code in the category. But it is a permanent cat-and-mouse dependency and it is the thing that gets your account or IP blocked. |
| `subzeroid/instagrapi` | 6,725 | 2026-08-26 | "Other" (NOASSERTION; upstream ships MIT text) | Python | Full **private mobile API** client: login, feed, stories, DMs, posting, insights. | **Unsanctioned and higher-risk than instaloader.** Requires a logged-in session; real ban risk that scales with request volume, missing/rotating proxies, and fresh accounts. The maintainer now openly upsells **HikerAPI**, a paid SaaS, from the README and description. | **Needs work / commercial trap.** Most capable, most dangerous. The SaaS steer means the free path gets less love over time. Non-standard license declaration is a diligence flag. |
| `subzeroid/aiograpi` | 436 | 2026-08-28 | — | Python | Async rewrite of instagrapi. | same | Same caveats, less battle-tested. |
| `subzeroid/aiograpi-rest` | 640 | 2026-08-28 | — | Python | REST wrapper around the private API. | same | Convenience layer over a risk. |
| `dilame/instagram-private-api` | 6,470 | 2024-08-09 | MIT | TypeScript | The JS private-API client. | same | **Abandoned** — two years stale against a moving target. |
| `Datalux/Osintgram` | 14,180 | 2025-08-25 | GPL-3.0 | Python | Interactive OSINT shell against any user by nickname: followers, followees, emails, phone numbers, tagged photos, geolocations. 885 open issues. | **Unsanctioned, and the use case itself is the problem.** | **Do not touch.** GPL-3.0 (viral), 885 open issues, and it is a surveillance tool. Legally and reputationally radioactive for a commercial product. |
| `misiektoja/instagram_monitor` | 1,389 | 2026-08-28 | GPL-3.0 | Python | Tracks a specific user's activity, profile changes and content, with dashboards and push notifications. | **Unsanctioned; targeted-surveillance shaped.** | **Actively maintained**, well-built, and I would still not ship it. GPL-3.0 + stalkerware framing. |
| `th3unkn0n/osi.ig` | 1,554 | 2024-02-01 | **none** | Python | IG information gathering. | Unsanctioned. | **Abandoned + no license.** Unusable. |
| `huaying/instagram-crawler` | 1,351 | 2024-05-03 | MIT | Python | Selenium-driven posts/profile/hashtag scraper without the API. | Unsanctioned. | **Abandoned.** Selenium approach is brittle. |
| `GramAddict/bot` | 1,632 | 2025-02-16 | MIT | Python | UIAutomator2 device automation on a real/emulated Android — likes, follows, scraping through the actual app UI. | **Unsanctioned engagement automation** — a different and worse ToS violation than reading. | **Dormant.** The fork `joeahkim/InstaAddict` (93★, active 2026-08) claims to be the maintained continuation. Irrelevant to profiling anyway — this is a growth bot. |
| `tnychn/instascrape` (176★), `yogeshwaran01/instagramy` (153★) | — | — | — | Python | — | — | **ARCHIVED.** Dead. |

### Apify
`apify/instagram-scraper` is a **hosted, closed-source, paid actor**, not an open-source library — there is no GitHub repo to audit. Apify's own position: their social scrapers collect only publicly available data and do not access private content, but they explicitly note that public data can still be personal data under GDPR, that Instagram's Terms restrict automated access, and that the legal responsibility for having a legitimate basis sits with **you**, the user of the actor. Related store actors: `profile-scraper/scrape-instagram-profiles`, `post-scraper/scrape-instagram-posts`, `image-scraper/scrape-instagram-images`.
**Verdict:** commercially convenient, operationally reliable (they absorb the block-evasion arms race), **not sanctioned by Meta**, and it moves the ToS exposure onto your account rather than removing it.

### Bottom line on collection
- **Own / consenting account:** Graph API. Clean. Write your own thin client.
- **Third-party account:** there is no legal-and-complete option. Business Discovery is legal and thin. instaloader is complete and against the terms. Apify is complete, paid, and still against the terms.

---

## 3. Computational aesthetics / image quality

**Verdict for the category: strong, maintained, and the classic feature extractors are missing.**

| Repo | ★ | Last commit | License | Lang | What it does | Verdict |
|---|---|---|---|---|---|---|
| `chaofengc/IQA-PyTorch` | 3,381 | 2026-07-08 | NOASSERTION (custom; some weights carry non-commercial terms — **audit per metric**) | Python | 30+ IQA and image-*aesthetics* metrics in one API: NIMA, MUSIQ, TOPIQ, CLIPIQA, DBCNN, BRISQUE, NIQE, NRQM, LPIPS, PSNR/SSIM/FID. Docs site. | **USABLE — the single best pick in this category.** Actively maintained, one import, covers both technical and aesthetic. Check the license of each specific pretrained weight before commercial use. |
| `idealo/image-quality-assessment` | 2,243 | 2024-07-12 | Apache-2.0 | Python | The famous Keras/TF NIMA implementation (aesthetic + technical MobileNet heads), Docker + AWS training. | **ABANDONWARE — ARCHIVED by the owner.** Still the top Google result for "NIMA implementation." Do not start here. Use IQA-PyTorch's NIMA. |
| `Q-Future/Q-Align` | 621 | 2026-06-24 | NOASSERTION | Python | ICML 2024. An LMM fine-tuned as a unified scorer for image quality, image *aesthetics*, and video quality. Fine-tunable to your own rating data. | **Usable, active, research-grade.** The most interesting modern option if you have (or can collect) human ratings for your specific domain. |
| `Q-Future/Q-Bench` | 285 | active | — | Jupyter | ICLR 2024 Spotlight. Benchmarks whether MLLMs (GPT-4V, Gemini, 16 OSS models) can actually make correct low-level visual and quality judgments. | **Usable** — and see §5, this is the only thing that measures whether a VLM's *subjective visual claims* are calibrated. |
| `Q-Future/Q-Instruct` | 238 | 2026-07 | — | Python | CVPR 2024. 200K low-level visual instruction-tuning dataset + fine-tuned checkpoints. | Usable if fine-tuning. |
| `christophschuhmann/improved-aesthetic-predictor` | 1,339 | 2024-07-01 | Apache-2.0 | Python | CLIP ViT-L/14 embedding → small MLP → LAION aesthetic score (the one used to filter LAION-Aesthetics). | **Usable as a frozen artifact.** Unmaintained but it is ~30 lines plus a weights file; nothing to rot. Apache-2.0. |
| `LAION-AI/aesthetic-predictor` | 732 | 2022-08-15 | MIT | Jupyter | v1: a linear probe on CLIP embeddings. | **Abandoned but functional.** Superseded by the above. |
| `discus0434/aesthetic-predictor-v2-5` | 438 | 2024-12-18 | **AGPL-3.0** | Python | SigLIP-based aesthetic scorer. Best quality of the CLIP-aesthetic family. | **Commercial blocker.** AGPL-3.0. Technically the best of the three; legally the worst if you ship a service. |
| `woshidandan/TANet-...` | 375 | 2025-09-25 | Apache-2.0 | Python | IJCAI 2022. Theme-aware aesthetics assessment + the TAD66K dataset + weights + demos. | **Usable.** The most relevant academic aesthetics model with clean licensing. |
| `photosynthesis-team/piq` | 1,574 | 2024-05-12 | Apache-2.0 | Python | Metrics for image2image tasks (mostly full-reference: SSIM, MS-SSIM, VIF, FID, KID, BRISQUE). | **Dormant, ~2 years.** Overlaps IQA-PyTorch, which is more active and more aesthetics-oriented. |
| `francois-rozet/piqa` | 439 | 2026-08-02 | — | Python | Lean PyTorch IQA metrics package. | Usable, narrow. |
| `ocampor/image-quality` | 434 | 2026-07 | — | Python | BRISQUE and friends. | Legacy. |
| `bukalapak/pybrisque` | 250 | 2026-07 | — | Python | BRISQUE. | Legacy. |
| `zwx8981/LIQE` | 243 | 2026-08 | — | Python | CVPR 2023. Blind IQA via vision-language correspondence — CLIP-based, multitask (quality + scene + distortion). | **Interesting** — closest in spirit to "probe an image with text and get a graded judgment." |

### Scene classification
| Repo | ★ | Last commit | License | Verdict |
|---|---|---|---|---|
| `CSAILVision/places365` | 2,083 | 2025-10-17 | MIT (code) | **Usable, still the standard.** Places365-CNNs (ResNet18/50, AlexNet, DenseNet161), 365 scene categories, plus indoor/outdoor and SUN scene-attribute heads — the scene-attribute output is the underrated part for profiling ("cluttered", "natural light", "man-made"). Weights are 2016-era ports; the **dataset** carries its own non-commercial-leaning terms separate from the MIT code. |
| `baileyqbb/places365-tf`, `kishanmurthy/scene-recognition`, others | ≤13 | 2021–2026 | — | **Abandoned reimplementations.** Use the CSAIL repo. |

### Palette extraction
| Repo | ★ | Last commit | License | Lang | Verdict |
|---|---|---|---|---|---|
| `qTipTip/Pylette` | 170 | **2026-07-21** | MIT | Python | **USABLE — the only actively maintained Python option.** Palette extraction with k-means/median-cut, CLI, sortable by frequency/luminance. Has a Dash demo app (`AnnMarieW/dash-pylette`). |
| `fengsp/color-thief-py` | 1,110 | 2022-10-31 | NOASSERTION | Python | The famous one. **Dormant but complete** — modified median-cut, ~200 lines, nothing to break. License declaration is non-standard. |
| `obskyr/colorgram.py` | 471 | 2021-08-13 | MIT | Python | Palette extraction with proportions. **Dormant, works.** |
| `bedapisl/fast-colorthief` | 57 | 2026-03 | — | C++ | C++-accelerated color-thief. Useful at scale. |
| `Vibrant-Colors/node-vibrant` | 2,444 | 2026-08-28 | — | TS | JS. Active. Vibrant/Muted swatch extraction (the Android Palette algorithm). Relevant if your stack is JS. |
| ~16 other `dominant color` repos | 0–3 | various | — | — | **All junk.** Coursework k-means notebooks. |

### **The gap: Datta and Machajdik feature extractors do not exist as maintained code.**
A search for `colorfulness metric image emotion Machajdik` returns **zero repos**. There is no maintained Python implementation of Datta et al.'s 56 aesthetics features or of the Machajdik–Hanbury emotion feature set (Itten color contrasts, Tamura texture, wavelet features, rule-of-thirds composition). These are the exact features the Segalin/Ferwerda personality papers used.

You reimplement them. It is roughly 150–250 lines of NumPy/OpenCV: Hasler–Süsstrunk colorfulness, HSV/Lab statistics and their variances, saturation-brightness product, rule-of-thirds subject placement, edge density, Tamura coarseness/contrast/directionality, and low-depth-of-field indicators. Not hard, but nobody has published it in a form you can `pip install`.

---

## 4. CLIP-based attribute probing, embedding clustering, dedup

**Verdict for the category: excellent and healthy. This is the strongest part of the ecosystem.**

| Repo | ★ | Last commit | License | Lang | What it does | Verdict |
|---|---|---|---|---|---|---|
| `mlfoundations/open_clip` | 14,100 | 2026-08-28 | NOASSERTION (permissive, custom) | Python | The open CLIP implementation. Every CLIP/SigLIP/EVA-CLIP checkpoint, unified API, zero-shot classification built in. | **USABLE — foundational. Take it.** Actively maintained, only 30 open issues at 14k stars. |
| `LAION-AI/CLIP_benchmark` | 814 | 2026-07-23 | MIT | Python | Zero-shot classification and retrieval benchmark harness across ~40 datasets, **with the prompt-template ensembles built in**. | **USABLE — this is the closest thing to a prompt-ensembling harness that exists.** Its per-dataset `classnames` + `templates` JSON files are directly reusable for your own attribute taxonomies. Underrated. |
| `rom1504/clip-retrieval` | 2,795 | 2026-03-28 | MIT | Jupyter/Python | Compute CLIP embeddings at scale, build a knn (autofaiss) index, serve a back-end + front-end for semantic search and dedup. 95 open issues. | **Usable as a local embedder + index builder.** The hosted LAION-5B index it was famous for is gone; treat this as an embedding/indexing pipeline, not a search service. |
| `rom1504/img2dataset` | 4,443 | 2025-10-19 | MIT | Python | URL list → resized webdataset shards, fast, resumable, with dedup and exif handling. | **Usable.** The right ingestion layer if your collector emits a manifest of image URLs. Dormant ~10mo but feature-complete. |
| `xinyu1205/recognize-anything` (RAM / RAM++ / Tag2Text) | 3,712 | 2025-02-18 | Apache-2.0 | Jupyter/Python | Open-vocabulary image tagging — 4,500+ recognizable tags out of the box, plus Tag2Text captioning. | **Usable, dormant-but-done.** Apache-2.0. Gives you a controlled-vocabulary tag layer without prompt engineering. Third-party wrappers exist (`Beowolve/ImageTagService` FastAPI, `derekslinz/photoram` CLI) but both are 0★ — write your own. |
| `pharmapsychotic/clip-interrogator` | 2,983 | 2024-05-15 | MIT | Python | CLIP + BLIP → a descriptive prompt string, by ranking a curated vocabulary (artists, mediums, movements, flavors, trending) against the image embedding. | **Abandoned (2 yrs) — but steal the data.** Conceptually this *is* CLIP attribute probing with a controlled vocabulary. Don't take it as a dependency; take its `data/*.txt` vocabulary lists and its ranking loop. |
| `idealo/imagededup` | 5,666 | 2025-08-15 | Apache-2.0 | Python | PHash / DHash / AHash / WHash + CNN-embedding dedup, with `find_duplicates`, `find_duplicates_to_remove`, and an evaluation module. | **USABLE — best pick for dedup.** Apache-2.0, clean API, plotting helpers. Note the same org's `image-quality-assessment` is archived; this one is not. |
| `JohannesBuchner/imagehash` | ~3,900 | active | BSD-2-Clause | Python | The primitive perceptual hashes (average, perceptual, difference, wavelet, colorhash, crop-resistant). | **Usable.** Lower level than imagededup; use it if you want the hash, not the pipeline. (Resolved via web — GitHub's repo-search index would not return it by name.) |
| `voxel51/fiftyone` | 11,047 | **2026-08-30** | Apache-2.0 | TS/Python | Dataset curation for visual AI: load a folder of images, attach arbitrary per-sample fields, compute embeddings, run similarity / uniqueness / representativeness / mistakenness ("Brain" methods), visualize in an embeddings plot, filter in a UI, export. Also ships a FACET dataset loader. | **USABLE — this is the best available *glue*.** Apache-2.0, committed to today, 676 open issues (large project, not neglect). If you build one thing on top of one dependency, build it on this. |
| `LAION-AI/CLIP-based-NSFW-Detector` | 471 | 2023-05-30 | NOASSERTION | Python | Safety classifier on CLIP embeddings. | Abandoned but a useful frozen head for content gating. |
| `mattpodolak/duplicate-img-detection` | 35 | 2026-03 | — | Python | imagehash + faiss + FastAPI reference service. | Small but a clean architecture reference. |

---

## 5. VLM evaluation and structured extraction harnesses

**Verdict: the structured-decoding layer is mature and competitive. The psychological/demographic VLM benchmark layer does not exist.**

### Constrained / structured decoding

| Repo | ★ | Last commit | License | Lang | What it does | Verdict |
|---|---|---|---|---|---|---|
| `dottxt-ai/outlines` | 15,715 | 2026-08-28 | Apache-2.0 | Python | Structured generation: JSON Schema, regex, and CFG constraints enforced at the token level. Works with local models (transformers, vllm, llama.cpp, mlx) and API models. | **USABLE.** The right pick if you run a local VLM and need a guarantee, not a retry loop. Rust core in `dottxt-ai/outlines-core` (309★). |
| `567-labs/instructor` | 13,801 | 2026-08-29 | MIT | Python | Pydantic model in, validated object out, with automatic retry-on-validation-failure. Multimodal inputs supported. TS port `instructor-js` (802★, stale since 2025-01). | **USABLE — the default pick for hosted VLMs.** MIT, committed yesterday, only 40 open issues. Lowest friction path from "folder of images" to "list of typed records". |
| `guidance-ai/guidance` | 21,729 | 2026-05-21 | MIT | Jupyter | Constrained generation via an embedded control language; interleaves generation and control flow. 322 open issues. | **Usable, but slowing.** The live engineering is in `guidance-ai/llguidance` (851★, Rust, 2026-08-25), the constraint core now used by other runtimes. Use llguidance via vLLM/TensorRT rather than the Python DSL. |
| `eth-sri/lmql` | 4,209 | 2025-05-22 | Apache-2.0 | Python | A query language for constrained LLM programming. 120 open issues. | **DEAD.** 15 months since a commit, superseded by outlines and guidance. **Do not bother.** |
| `guidance-ai/llgtrt` | 72 | 2026-08 | MIT | Rust | TensorRT-LLM server with JSON structured outputs. | Niche, for self-hosted throughput. |

### VLM evaluation harnesses

| Repo | ★ | Last commit | License | Lang | What it does | Verdict |
|---|---|---|---|---|---|---|
| `open-compass/VLMEvalKit` | 4,363 | 2026-08-28 | Apache-2.0 | Python | One-command evaluation of **220+ VLMs across 80+ benchmarks**, including hosted APIs (GPT-4V, Claude, Gemini) and OSS models. | **USABLE, active.** The right harness if you want to know whether your chosen VLM is actually good at the visual judgments you're asking it to make. Apache-2.0. 300 open issues (breadth, not rot). |
| `EvolvingLMMs-Lab/lmms-eval` | 4,383 | 2026-08-29 | NOASSERTION | Python | The other one. Text, image, video and audio task coverage. | **Usable, active.** Overlaps VLMEvalKit; pick one. VLMEvalKit's license is cleaner. |
| `Q-Future/Q-Bench` | 285 | 2026-08 | — | Jupyter | Whether MLLMs can make correct **low-level visual and quality judgments**. | **The only benchmark family in this space that tests subjective visual judgment calibration.** No personality/demographic equivalent exists. |
| **MM-OCEAN** | — | — | — | — | Multimodal Big Five benchmark. | **NO CODE. Does not exist on GitHub.** Code search for the literal string returns 3 irrelevant files. |
| `swordlidev/Evaluation-Multimodal-LLMs-Survey` | — | active | — | md | Survey of MLLM benchmarks. | Useful index. |

### Supporting infra
- `pixeltable/pixeltable` — 1,615★, active (2026-08-30), "unified multimodal backend for AI data apps." Declarative columns that are *computed by a model*, incremental, with versioning. **Interesting** as an alternative spine to FiftyOne if you want persistence + incremental recompute over a growing image set rather than curation + UI.

---

## 6. Marketing / brand visual analytics

### Verdict for the category: **EMPTY. This is the single biggest hole in the ecosystem.**

- **"Visual Listening In"** (Liu, Dzyabura & Mizik, *Marketing Science* 2020 — mining brand perceptions from consumer-posted social media images): a GitHub **code search** for the phrase returns **zero results**. A repo search for `visual listening brand image social media marketing` returns **zero repos**. There is no open implementation, no reimplementation, and no fork.
- **Brand image extraction / social media image mining for marketing:** `brand logo detection social media images` returns **zero repos**. There is no maintained open logo-detection-for-brand-analytics project. You would assemble this from `ultralytics/YOLO` (61,085★, active) trained on LogoDet-3K, or zero-shot with OWL-ViT / GroundingDINO.
- **Influencer analytics:** 40 repos. **Every single one is ≤2 stars.** The entire cohort is Power BI dashboards, Tableau workbooks and SQL exercises over the same Kaggle "Top 200 Instagram Influencers" CSV (`rank, channel_info, influence_score, posts, followers, avg_likes, 60_day_eng_rate, country`). **Not one of them looks at an image.** This is a genre of portfolio project, not a body of tooling.
- The only marginally relevant thing: `drkostas/Insta-Likes-Predict` — 70★, GPL-3.0, pushed 2026-08-09, Python. Predicts like counts from a photo (CNN + its own scraper). **Hobby project, still occasionally touched.** GPL-3.0. Interesting as evidence that the "image → engagement" idea has been tried at toy scale; not something to build on.

**If you want visual brand analytics, you are the first mover in open source.** There is nothing to fork, extend, or even read.

---

## 7. Fairness / bias auditing for vision models

**Verdict: you get generic metric libraries and a demographic classifier. You do not get an image-bias audit harness.**

| Repo / asset | ★ | Last commit | License | What it is | Verdict |
|---|---|---|---|---|---|
| `joojs/fairface` | 502 | 2026-01-04 | **NO LICENSE** | The FairFace dataset (108k images balanced across 7 race groups) + pretrained race/gender/age models. The de facto academic standard. | **Legally unusable as-is.** No license file. Also: this is a *demographic classifier* — the thing you'd audit, not the auditor. Using it to label people is exactly the harm the fairness literature warns about. |
| `yakhyo/fairface-onnx` | 4 | 2026-07-30 | — | ONNX inference for FairFace. | Convenience wrapper, no adoption. |
| `serengil/deepface` | 23,353 | 2026-08-24 | MIT | Face recognition + facial attribute analysis: age, gender, emotion, "race". Wraps VGG-Face, FaceNet, ArcFace, Dlib, SFace, GhostFaceNet. | **Code is usable (MIT, active, 9 open issues). The race and emotion heads are not.** They are trained on small, unrepresentative sets and are the classic source of the exact disparities you'd be auditing for. Use the detection/embedding parts; treat the demographic heads as a liability, not a feature. `serengil/retinaface` (2,029★, MIT, 2026-06) is the good part. |
| **Meta FACET** | — | — | Meta terms | 32k images, 13 person attributes (incl. perceived gender presentation, perceived skin tone, hairstyle) and 52 person classes, for evaluating classification/detection/segmentation disparities. | **Not on GitHub.** Hosted at facet.metademolab.com / ai.meta.com. **Evaluation-only — training on the annotations is explicitly prohibited.** FiftyOne ships a loader and Voxel51 published a walkthrough; that's the practical access path. |
| **Monk Skin Tone tooling** | — | — | — | Google's 10-point MST scale. | **Essentially does not exist.** The four repos that mention it are 1★, 0★, 0★, 0★ (a sunscreen recommender, a clothing-color web app, an OpenCV+MTCNN script, and a browser annotation tool for sign-language video). There is no library. MST is a scale and a set of swatches; the code is yours to write. |
| **Gender Shades follow-ups** | — | — | — | Buolamwini & Gebru's intersectional audit of commercial gender classifiers. | **No code repos.** A search returns 6 results, top is 3★ and unrelated. Those audits were papers plus probes against proprietary APIs; the probe harnesses were never released. |
| `Trusted-AI/AIF360` | 2,859 | 2026-08-29 | Apache-2.0 | 70+ fairness metrics + bias mitigation algorithms, Python and R. | **Usable, active — but tabular-first.** No native image or VLM path. You'd feed it your own (prediction, group) pairs. |
| `fairlearn/fairlearn` | 2,280 | 2026-08-29 | MIT | Fairness assessment + mitigation, scikit-learn-shaped. | **Usable, active, MIT.** Lightest-weight way to compute group disparity metrics once you have labels. Same caveat: tabular-first. |
| `dssg/aequitas` | 771 | 2026-08-20 | — | Bias audit toolkit with report generation. | Usable, group-metrics oriented. |
| `microsoft/responsible-ai-toolbox` | 1,827 | 2026-08-30 | — | Error analysis + fairness + interpretability dashboards. | Usable, heavy, active. |
| **Counterfactual image bias probes** | — | — | — | Generate matched image pairs varying only a protected attribute, measure prediction delta. | **Nothing off-the-shelf and maintained.** A handful of 0–1★ academic repos (`MedVLM-Audit`, `WPI-REU-2026`, two `EqualEyes` repos). All medical-VLM specific or empty. |

**Practical conclusion:** the audit harness for "does my VLM say different things about the same feed depending on the apparent skin tone / gender / age of the people in it" **does not exist**. You build it: generate or select matched image sets, run your extraction twice, and feed the two label sets to `fairlearn`. The metrics library is free; the vision-specific protocol is yours.

---

## 8. Awesome-lists and survey repos

| Repo | ★ | Status | Covers |
|---|---|---|---|
| `BradyFU/Awesome-Multimodal-Large-Language-Models` | 17,994 | **Active (2026-08-30)** | The canonical MLLM index. Best entry point for §5. |
| `jphall663/awesome-machine-learning-interpretability` | 4,063 | Active | Responsible ML broadly — fairness, interpretability, privacy. Best entry point for §7. |
| `chaofengc/Awesome-Image-Quality-Assessment` | 1,539 | **Active (2026-08-26)** | Comprehensive IQA paper collection, by the IQA-PyTorch author. Best entry point for §3. |
| `Kobaayyy/Awesome-CVPR...-Low-Level-Vision` | 1,737 | Active | CVPR low-level vision incl. IQA. |
| `MinghuiChen43/awesome-trustworthy-deep-learning` | 389 | Active | Fairness, robustness, privacy, unlearning. |
| `datamllab/awesome-fairness-in-ai` | 337 | Active | Fairness in AI. |
| `AmrMKayid/awesome-affective-computing` | 194 | Nominally active, content is 2018–2020 | Affective computing. **Stale content.** |
| `matthewvowels1/Awesome_ML_for_mental_health` | 127 | Active | Facial expression, emotion prediction, psychiatry. Closest index to the psychological-inference space. |
| `Yasen03/awesome-affective-computing` | 38 | New (2026-01) | Multimodal emotion recognition, empathetic LLMs. Thin. |
| `nku-zhichengzhang/Awesome-emotion_llm_and_mllm` | 38 | New | Affective computing with LLMs/MLLMs. Thin but current. |
| `NEU-DataMining/awesome-affective-computing` | 34 | Active | Affective computing in the LLM era. |
| `swordlidev/Evaluation-Multimodal-LLMs-Survey` | — | Active | MLLM benchmark survey. |
| **awesome-personality-computing** | — | — | **DOES NOT EXIST.** A search for `awesome personality computing` returns **zero repos.** |

The absence of a personality-computing awesome-list is itself the finding: the field never built enough public code to be worth indexing.

---

## The direct question: is there a maintained, end-to-end open-source pipeline that goes "folder of photos → structured profile"?

## **No. Plainly, no. Nothing close.**

I searched for it directly (`instagram feed analysis AI vision LLM`, `batch image captioning vision language model json`, `vlm structured extraction images pydantic`, `user profiling images social media`) and every one of those queries returned **zero relevant repos** or pure noise.

The two nearest misses, and why they miss:

- **`liaorongfan/DeepPersonality`** gets you *folder of videos → five numbers*. Wrong input modality (video with audio, not a photo feed), requires datasets under application-only agreements, dormant since Oct 2024, and it outputs traits with no evidence trail.
- **`aimclub/OCEANAI`** gets you *talking-head video → Big Five + a candidate ranking*. Best packaging in the space, BSD-3, docs, pip-installable — and still the wrong input and a use case (automated employment screening) you should not go near.

### The Lego pieces that do exist and are good
1. **Ingest / curate:** `voxel51/fiftyone` (Apache-2.0, active today) — the spine.
2. **Deduplicate / sample:** `idealo/imagededup` (Apache-2.0) — cut a 900-image feed to ~150 representative ones before you spend VLM tokens.
3. **Embed / probe:** `mlfoundations/open_clip` + `LAION-AI/CLIP_benchmark`'s prompt-template machinery (MIT) — cheap, deterministic, auditable attribute scores.
4. **Tag:** `xinyu1205/recognize-anything` (Apache-2.0) — controlled-vocabulary object/scene tags.
5. **Scene:** `CSAILVision/places365` (MIT code) — 365 scenes plus SUN scene attributes.
6. **Aesthetics / quality:** `chaofengc/IQA-PyTorch` + `christophschuhmann/improved-aesthetic-predictor` (Apache-2.0).
7. **Color:** `qTipTip/Pylette` (MIT, active).
8. **Extract:** `567-labs/instructor` (MIT) or `dottxt-ai/outlines` (Apache-2.0) — VLM → typed JSON.
9. **Measure yourself:** `open-compass/VLMEvalKit` (Apache-2.0) and the Q-Bench protocol.
10. **Fairness metrics:** `fairlearn/fairlearn` (MIT).

### The glue that is missing — every one of these you write yourself
1. **Account-level aggregation.** Every tool in this report is per-image. Nothing rolls N per-image records into one account-level record with recency weighting, outlier handling, or consistency measures. This is the core of what a "profile" is, and it is 100% greenfield.
2. **A schema.** No open project publishes a validated JSON schema for "visual profile of an account." No shared vocabulary, no field definitions, no versioning.
3. **Confidence and calibration.** Nothing tells you how much to trust an inference or when to abstain. Q-Bench measures whether MLLMs get low-level visual facts right; there is no equivalent for higher-order subjective claims.
4. **Evidence linkage.** Nothing links a claim back to the specific images that produced it. Every tool emits a number or a label with no provenance. For a profiling product this is the difference between a defensible report and a horoscope.
5. **Refusal and consent gating.** No repo implements "this account should not be profiled." Not one.
6. **Cost-aware batching.** No harness handles running a hosted VLM over hundreds of images with budget caps, caching, and partial-failure recovery. `instructor` gives you retries; it does not give you a budget.
7. **The classic aesthetics feature bank.** Datta/Machajdik features — the actual basis of the personality-from-images literature — have no maintained implementation anywhere. ~200 lines you must write.

---

## What I would actually build with — the shortlist

| # | Repo | License | Why |
|---|---|---|---|
| 1 | `voxel51/fiftyone` | Apache-2.0 | Dataset spine, per-sample fields, embeddings, similarity/uniqueness, inspection UI. Committed today. If one dependency, this one. |
| 2 | `idealo/imagededup` | Apache-2.0 | Dedup and representative sampling before any expensive pass. |
| 3 | `mlfoundations/open_clip` | permissive | Embeddings + zero-shot. Non-negotiable. |
| 4 | `LAION-AI/CLIP_benchmark` | MIT | Reuse its class-name/template ensembles as the pattern for your own attribute taxonomies. The best-kept secret here. |
| 5 | `chaofengc/IQA-PyTorch` | NOASSERTION — **audit per-weight** | Aesthetic + technical quality in one API. |
| 6 | `christophschuhmann/improved-aesthetic-predictor` | Apache-2.0 | Frozen LAION aesthetic head. Clean license, zero maintenance risk. |
| 7 | `qTipTip/Pylette` | MIT | Palettes. The only maintained one. |
| 8 | `CSAILVision/places365` | MIT (code) | Scene + scene-attribute labels. |
| 9 | `xinyu1205/recognize-anything` | Apache-2.0 | Open-vocab tagging. |
| 10 | `567-labs/instructor` (hosted VLM) or `dottxt-ai/outlines` (local) | MIT / Apache-2.0 | VLM → validated typed JSON. |
| 11 | `open-compass/VLMEvalKit` | Apache-2.0 | Prove your extraction is any good before you sell its output. |
| 12 | `fairlearn/fairlearn` | MIT | Group-disparity metrics over your own labels. |
| 13 | Instagram **Graph API** (Business Discovery) — hand-rolled client | — | The only sanctioned collection path. No wrapper is worth a dependency. |
| 14 | `instaloader/instaloader` | MIT | *Only* if you accept the ToS violation and the block arms race. Cleanest of the scrapers. |
| 15 | `pixeltable/pixeltable` | — | Optional alternative spine if you need incremental recompute over a growing set. |

## Do not bother

- **`idealo/image-quality-assessment`** — **ARCHIVED**. Still the top search result for "NIMA implementation". Use IQA-PyTorch.
- **`eth-sri/lmql`** — dead since 2025-05. Superseded.
- **`pharmapsychotic/clip-interrogator` as a dependency** — abandoned 2 years. Steal its vocabulary files, don't import it.
- **`discus0434/aesthetic-predictor-v2-5` for anything commercial** — AGPL-3.0.
- **`joojs/fairface`** — no license file. And it's a demographic classifier, which is the problem, not the solution.
- **`serengil/deepface`'s race / emotion heads** — scientifically weak, bias-amplifying, reputationally toxic. The detector and embeddings are fine.
- **`Datalux/Osintgram`, `misiektoja/instagram_monitor`, `th3unkn0n/osi.ig`** — surveillance-shaped, GPL-3.0 or unlicensed, 885 open issues in the first case. Radioactive for a commercial product.
- **`dilame/instagram-private-api`** — 2 years stale against a target that changes monthly.
- **`GramAddict/bot`** — engagement automation, dormant, irrelevant to profiling, and the worst class of ToS violation.
- **Every personality repo under 20★** — coursework, mostly unlicensed, none reproducible.
- **`raoulg/PsychoFlickr`, `frkngrpnr/lapfi`** — Matlab, 2017, one has no license.
- **The entire influencer-analytics cohort (40 repos, all ≤2★)** — Power BI over one Kaggle CSV. Zero image analysis.
- **Searching for MM-OCEAN code** — it isn't on GitHub. Confirmed by literal-string code search.
- **Searching for a Visual Listening In implementation** — it isn't on GitHub. Zero code-search hits, zero repo hits.
- **Searching for Monk Skin Tone tooling** — top four repos are 1★, 0★, 0★, 0★. Write it yourself or don't.
- **Searching for the ChaLearn First Impressions winning entries** — not published. `DeepPersonality` reimplements several as baselines; that is your only route.
- **Searching for an awesome-personality-computing list** — doesn't exist.

---

## Data-quality note

`updated_at` in GitHub's API bumps on stars and forks, not just commits, and is therefore worthless as a maintenance signal. Every "last commit" in this report is `pushed_at`. Where a repo's activity claim came from a page fetch rather than the API (`JohannesBuchner/imagehash`), it is flagged inline. The GitHub REST API was blocked for direct curl in this environment; all figures came through the authenticated MCP search endpoints or targeted page fetches.
