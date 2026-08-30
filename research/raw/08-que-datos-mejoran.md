# Which Additional Data Signals Actually Improve Profiling Accuracy — and by How Much

**Evidence review — compiled 2026-08-30**
**Question:** given a system that currently analyses social-media *images*, what additional inputs measurably raise the accuracy of its analyses, and what is the size of each gain?
**Answer format:** every entry is expressed as a measured Δ (delta in Pearson r, in RMSE, in binary accuracy, or in elasticity), with the study, the sample, and the caveat that would invalidate it.

---

## 0. Read this before reading any number

Five distinctions decide whether a "gain" is real. They are the reason most of the field's headline numbers are wrong by a factor of two or more.

**(a) Δr is not r.** The relevant quantity for "what should I feed the system" is *incremental* validity — how much a channel adds **over what is already there** — not its standalone correlation. Many channels with respectable standalone r (images, demographics-adjacent behaviour) have near-zero Δr because they are redundant with what you already have.

**(b) Self-assessed vs. attributed personality.** Predicting the score a person gives *themselves* (APR) is 2–3× harder than predicting the score *strangers assign after seeing the same images* (APP). Segalin/PsychoFlickr on identical data: **54% accuracy for self-assessed vs. 65% for observer-attributed** traits. Anything above r ≈ .35 from images alone is measuring perception, not personality. *For a brand-account audit this is good news, not bad — the account audit case genuinely wants the perceived construct (§5).*

**(c) Ground truth that is itself a model.** Liu et al. (2016), the most-cited profile-picture study, has no questionnaires: it labels 66,502 Twitter users by running a *text* model over their tweets, then predicts those labels from images. Its r values are image→text-model agreement.

**(d) Sample size and the fusion literature.** The single most-cited "multimodal fusion helps" result on social media (Skowron et al. 2016) has **n = 62 users**. At that n, nothing below Δr ≈ .25 is detectable.

**(e) Meta-regression at study level ≠ ablation at feature level.** Azucar et al.'s "pictures did not improve prediction" is a *between-study* moderator test on 16 studies, of which only a minority used pictures at all. It is genuine evidence, but it is weak evidence, and it says the same thing about text. Both facts are reported below.

---

## 1. Ranking of signal channels by measured predictive power

### 1.1 Master table — standalone validity per channel (predicting self-reported Big Five)

| Rank | Channel | O | C | E | A | N | Avg | Source / n |
|---|---|---|---|---|---|---|---|---|
| **1** | **Facebook Likes** (227 Likes = population avg) | — | — | — | — | — | **.56** | Youyou et al. 2015, n = 70,520 |
| 1b | Facebook Likes, >500 Likes subsample | — | — | — | — | — | **.66** | ibid. (selected subsample, upward-biased) |
| 1c | Facebook Likes (earlier estimate) | **.43** | ≈.29 | **.40** | ≈.30 | ≈.30 | ≈.35 | Kosinski et al. 2013, n = 58,466 |
| **2** | **Smartphone behavioural logs** (30 days, all classes) | — | — | — | — | — | **.37** (median, domains); **.40** (facets) | Stachl et al. 2020, n = 624 |
| **3** | **Language / text** (Facebook status updates, ≥1,000 words) | **.43** | .37 | **.42** | .35 | .35 | **.38** | Park et al. 2015, n = 4,824 |
| 3b | Language / text — meta-analytic | **.30** | .27 | .28 | .26 | .26 | ≈.27 | Moreno et al. 2021, 23 estimates |
| **4** | **Music: Facebook artist Likes** | **.30** | .19 | .21 | .17 | .18 | .21 | Nave et al. 2018, n = 21,929 |
| 4b | Music: reactions to unfamiliar 15-s excerpts | .25 | .11 | .16 | .15 | .12 | .16 | Nave et al. 2018, n = 17,904 |
| **5** | **Smartphone logs — meta-analytic** | .25 | .23 | **.35** | .24 | .24 | .26 | Marengo et al. 2023, 21 effect sizes |
| **6** | **Digital footprints, all types pooled** | .39 | .35 | **.40** | .29 | .33 | .35 | Azucar et al. 2018, 16 studies |
| **7** | **Images / profile pictures** | .07–.15 | .05–.19 | .06–.15 | .07–.10 | .04–.15 | **≈.12, max .19** | Liu et al. 2016, n = 66,502 *(text-inferred ground truth)* |
| 7b | Images — binary classification, self-assessed | .55–.56 acc (mean split); .60–.62 acc (quartile split) | | | | | ~r ≈ .10–.24 equivalent | Segalin et al. 2017, n = 11,736 profile pictures |
| 7c | Images — 200 favourite pictures/user, CNN | 54% accuracy (self-assessed) vs **65% (observer-attributed)** | | | | | | PsychoFlickr, n = 300 |
| **8** | **Purchase / transaction records** | — | — | — | — | — | **.15** (corrected ρ = .21) | Gladstone, Matz & Lemaire 2019, n = 2,193, 2M transactions |
| 8b | Purchase records → *materialism* (not Big Five) | — | — | — | — | — | **.33** (ρ = .42) | ibid. |
| **9** | **Network structure / who you follow** | no reliable meta-analytic estimate exists | | | | | see §1.3 | — |

**Values marked ≈ are read off published figures rather than tables and should be treated as ±.03.**

### 1.2 What this table actually says

- **Likes/follows are the single strongest channel by a wide margin.** r = .56 vs r ≈ .12–.19 for images. Likes are not behaviour; they are *declared preference statements*, which is why they break through the "personality coefficient" ceiling of .30–.40 that constrains every behavioural channel (Meyer et al. 2001; Roberts et al. 2007 — Azucar et al. explicitly note their pooled .29–.40 sits exactly at that ceiling).
- A follow list, a saved-posts list, a "liked" list, a Spotify library and a subscription list are all the *same kind of signal* as Facebook Likes. This is the family to prioritise.
- **Text is second-tier but robust:** .38 in the best-powered single study, .26–.30 meta-analytically. Note the gap — the .38 figure comes from users with ≥1,000 words; the meta-analytic figure pools studies with far less text.
- **Behavioural logs (posting times, app usage, mobility) are third-tier and highly trait-specific.** Marengo et al.'s meta-analysis: extraversion .35, everything else .23–.25. And critically, *which* log matters is narrow — see §7.
- **Images are the weakest channel that still has a signal.** Confirmed at every level of the evidence hierarchy.
- **Purchase history is nearly useless for Big Five (r = .15) but good for consumer-relevant traits** — materialism r = .33, self-control comparable. If the target construct is a *consumer* construct rather than a personality construct, purchase data jumps several ranks.

### 1.3 The network-structure gap (honest answer)

There is **no meta-analytic estimate** of how well ego-network structure alone predicts Big Five. The best proxies available:

- Azucar et al. 2018's "user activity statistics" moderator improved prediction of **extraversion only** (β = .19, R² = .18, p = .06 — marginal).
- Marengo et al. 2023 tested three log types as moderators. Only **call- and text-log data** moved anything, and only for **extraversion** (β = .14, p = .03). Sensors/system data: all p ≥ .11. App usage: all p ≥ .53.
- Kosinski et al. 2013 predicted network *size* (r = .47) and *density* (r = .52) *from* Likes — the inverse direction, and both are structural facts, not traits.

**Working conclusion:** network structure carries a real signal for extraversion (~Δr .10–.15 over nothing) and essentially nothing demonstrated for the other four traits. Treat any vendor claim above that as unvalidated.

---

## 2. Fusion: what does adding a channel actually buy?

### 2.1 The key negative result — verified precisely

> Azucar, D., Marengo, D., & Settanni, M. (2018). *Predicting the Big 5 personality traits from digital footprints on social media: A meta-analysis.* **Personality and Individual Differences, 124**, 150–159.

Eight moderators were tested by random-effects univariate meta-regression on 16 independent studies (80 effect sizes). Verbatim from the Discussion:

> "Also, **use of features extracted from texts and pictures posted on social media did not improve prediction accuracy of personality traits over use of other types of digital footprints.**"

Full moderator results:

| Moderator | Result |
|---|---|
| **Multiple vs. single footprint type** | **Significant:** O β = .27 (R² = .16); C β = .25 (R² = .20); N β = .21 (R² = .14). E β = .18 (R² = .12), **p = .08** (n.s.). A: no effect. |
| **Demographics (age, gender) included** | **Significant:** A β = .25 (R² = .19); N β = .25 (R² = .19). O β = .26 (R² = .12), p = .09 (marginal). |
| **User activity statistics included** | E β = .19 (R² = .18), p = .06 (marginal). Nothing else. |
| **Pictures used (yes/no)** | **No significant effect on any trait.** |
| **Language/text used (yes/no)** | **No significant effect on any trait.** |
| Likes used | Not testable — only 1 of 16 studies used Likes. |
| Private vs. public platform | No effect. |
| Study quality | No effect. |

**Two things must be said about this result, and both are load-bearing:**

1. **It is real and it is the correct headline.** Pictures do not add measurable accuracy over other footprint types. The system's current primary input is, meta-analytically, the one input with no demonstrated incremental value.
2. **It is weak evidence, and it condemns text equally.** Azucar et al.'s own Limitations section: *"only a minority of studies included in the meta-analysis used pictures to predict personality, and none of them included data about videos; further, all examined studies, except for one (Skowron et al. 2016), failed to investigate use of digital footprints collected from highly visual social media platforms such as Instagram and Snapchat. For this reason, results concerning the predictive power of visual data to predict personality are to be taken as preliminary."* The honest reading is **"no evidence of benefit," not "evidence of no benefit"** — but seven years later nothing has overturned it, and the direct within-study ablations (§2.2) point the same way.

**What DID move the needle in that meta-analysis:** using *more than one type* of footprint (β = .21–.27, i.e. roughly Δr ≈ +.05 to +.08 at the study level), and — remarkably — including **plain demographics** (β = .25–.26). Age and gender are cheaper than any of this and buy as much as the modality choice.

### 2.2 Within-study ablations — the fusion deltas that exist

**Adding image feature families to each other (Segalin et al. 2017, MM'17, n = 11,736 Facebook profile pictures, quartile-split binary accuracy):**

| Feature set | O | C | E | A | N |
|---|---|---|---|---|---|
| CNN alone (best single family) | 0.59 | 0.60 | 0.61 | 0.60 | 0.59 |
| CA alone | 0.55 | 0.52 | 0.55 | 0.53 | 0.53 |
| PHOW alone | 0.54 | 0.54 | 0.54 | 0.54 | 0.54 |
| IATO alone | 0.53 | 0.53 | 0.55 | 0.53 | 0.53 |
| **All four fused** | **0.60** | **0.60** | **0.62** | **0.60** | **0.60** |

**Δ from fusing four independent visual feature families = +0.00 to +0.01 accuracy.** Within-modality fusion of images buys nothing.

**Adding images to text (Skowron et al. 2016, WWW'16, Twitter + Instagram, RMSE, lower is better):**

| Feature set | Avg RMSE |
|---|---|
| Twitter linguistic only (Tl) | 0.75 |
| Instagram image only (Ii) | 0.83 |
| Twitter meta only (Tm) | 0.89 |
| Twitter text + Instagram captions (TlIl) | 0.71 |
| **Twitter text + Instagram captions + Instagram images (TlIli)** | **0.69** |
| Everything (TlmIli) | 0.66 |

**Δ from adding image features on top of text = 0.71 → 0.69 RMSE, a 2.8% error reduction.** Going from text-only (0.75) to everything (0.66) is a 12% error reduction, but most of that comes from adding *more text* (Instagram captions) and *metadata* (follower/followee counts), not from pixels.

**The fatal caveat:** **n = 62 users.** Participants were required to have ≥30 Instagram images *and* ≥30 tweets, which collapsed the sample. At n = 62 with 10-fold CV, a 2.8% RMSE difference is indistinguishable from noise. This is the strongest published "images help on top of text" result in the social-media literature, and it does not survive a power calculation.

**Adding the *modality* vs. adding *more of the same*:** Nave et al. 2018 gives the cleanest incremental-validity numbers in the whole field, because they explicitly contrast a rich channel against a demographic baseline on the same people:

| Adding music Likes on top of age + gender | Δr |
|---|---|
| Openness | **+0.20** (200% increase) |
| Extraversion | **+0.15** (260%) |
| Agreeableness | **+0.12** (240%) |
| Conscientiousness | **+0.07** (70%) |
| Neuroticism | **+0.00** (2% — demographics already capture it) |

That is what a *genuinely* incremental channel looks like. Compare against images, where no equivalent Δ has ever been demonstrated.

### 2.3 Fusion summary

| Fusion move | Measured Δ | Confidence |
|---|---|---|
| Add a **second footprint type** (any) | Study-level β = .21–.27; ≈ **Δr +.05 to +.08** | Moderate (meta-regression, k = 16) |
| Add **demographics** (age, gender) | β = .25–.26 for A, N, O; ≈ **Δr +.05 to +.08** | Moderate |
| Add **music/artist Likes** over demographics | **Δr +.20 (O), +.15 (E), +.12 (A), +.07 (C), .00 (N)** | High (n = 21,929, out-of-sample) |
| Add **images** over other footprints | **no significant effect** | Moderate-low, but consistently null |
| Add **images** over text (within study) | **−2.8% RMSE**, n = 62 | Very low |
| Fuse **image feature families** with each other | **+0.00 to +0.01 accuracy** | High (n = 11,736) |
| Add **text** over other footprints (meta) | **no significant effect** | Moderate-low |

---

## 3. Volume effects — how accuracy scales with data per person

### 3.1 Likes: the only well-characterised curve

Youyou, Kosinski & Stillwell (2015), PNAS 112(4):1036–1040, n = 86,220 (70,520 with Likes). LASSO + 10-fold CV, disattenuated self-other agreement. Models trained on users with ≥20 Likes; accuracy below 20 estimated by applying the model to random subsets of 1–19 Likes.

**The relationship is approximately log-linear in the number of Likes.** Anchor points, verbatim:

| Likes available | Average accuracy across Big Five | Equivalent human judge |
|---|---|---|
| 10 | — | average **work colleague** |
| 70 | — | average **cohabitant or friend** |
| 90–100 | **r = .49** | **average human judge in this sample** |
| 150 | — | average **family member** |
| **227 (population mean)** | **r = .56** | between family member and spouse |
| 300 | — | average **spouse (r = .58)**, the best human judge |
| >500 | **r = .66** (peak observed) | exceeds every human judge |

Verbatim on diminishing returns:

> "The approximately log-linear relationship between the number of Likes and computer accuracy, shown in Fig. 2, suggests that increasing the amount of signal beyond what was available in this study could further boost the accuracy, **although gains are expected to be diminishing**."

**Derived rule of thumb:** in the 100–500 Like range, each **doubling** of the footprint buys roughly **Δr ≈ +.05 to +.08**. (100 → 227 Likes ≈ 1.2 doublings for Δr = +.07; 227 → 500+ ≈ 1.1 doublings for Δr = +.10, though the >500 group is self-selected and upward-biased.)

**Point of diminishing returns:** the practical inflection is around **150–300 Likes**. Below 100 you are worse than a random friend; above ~300 you have already beaten a spouse and each further doubling costs exponentially more collection for a linear-ish gain. **Collecting the first 100 signals is worth roughly as much as collecting the next 400.**

### 3.2 Text: threshold, not curve

- **Park et al. 2015 imposed a hard floor of 1,000 words per user per interval.** Everything below was discarded — the field's de facto minimum.
- Within their validation sample, the language-based assessment's own **test–retest reliability across consecutive 6-month windows was r = .70** (O .74, C .76, E .72, A .65, N .62), attenuating as intervals spread apart. For comparison, Big Five self-report questionnaires retest at .65–.85. **A language model built on ≥1,000 words is about as stable as the questionnaire it is imitating.**
- **Moreno et al. 2021 fitted a meta-regression of effect size on text length (number of words) across 23 estimates: not significant.** This is a *cross-study* test with restricted range (most studies sit above the 1,000-word floor anyway), so read it as "past the threshold, more words stop mattering much," not as "volume is irrelevant."

**Regarding the reported "Liu ≥50-tweet threshold":** I could not verify a ≥50-tweet criterion in the accessible Liu et al. (2016) materials. What *is* verifiable in this literature: **Park et al.'s ≥1,000 words**, and **Skowron et al.'s ≥30 tweets AND ≥30 images**. Treat the ≥50-tweet figure as unconfirmed.

### 3.3 Images: the curve does not exist, and the two data points available point the wrong way

There is **no published accuracy-vs-number-of-images curve** on a large sample. The two anchor points from the same research group:

| Study | Images per user | n users | Result (self-assessed) |
|---|---|---|---|
| Segalin et al. 2017 (MM'17) | **1** (profile picture) | 11,736 | 0.55–0.56 acc (mean split); 0.60–0.62 (quartile split) |
| PsychoFlickr (Segalin et al., IEEE TAC 2017) | **200** favourite pictures | 300 | **0.54** acc (self-assessed); 0.65 (attributed) |

Going from **one** picture to **two hundred** pictures per user did **not** improve self-assessed-trait accuracy (0.55 → 0.54). The datasets differ (Facebook profile pictures vs. Flickr favourites) so this is not a clean ablation, but it is the only evidence there is, and it is not encouraging.

**Practical implication for the account case:** feeding the system 60 posts instead of 12 has no demonstrated accuracy benefit *for trait inference*. It has an obvious benefit for *consistency/variance* estimates and for detecting change over time — which is a different (and, for a brand audit, more valuable) question.

### 3.4 Volume summary

| Signal | Floor below which it is worthless | Point of diminishing returns | Δr per doubling in the useful range |
|---|---|---|---|
| Likes / follows | ~20 (models cannot be fit below this) | **150–300** | +.05 to +.08 |
| Text | **~1,000 words** | poorly characterised; likely ~2,000–5,000 words | not significant past the floor (Moreno 2021) |
| Images | 1 | **1** — no demonstrated gain from more | ≈ 0 |
| Smartphone logs | ~1 week | ~30 days (Stachl et al. used exactly 30) | not characterised |

---

## 4. Ground-truth quality — the most underrated number in the field

### 4.1 The instrument matters, and the effect is bigger than most fusion gains

**Park et al. 2015 ran the same model against the same people scored on two different instruments.** Convergent validity:

| Ground-truth instrument | Average r with language-based prediction |
|---|---|
| **100-item IPIP** | **.41** |
| **20-item subset** | **.34** |

**z = 2.65, p = .008. Δr = +0.07 from lengthening the questionnaire alone.** Same users, same model, same text. That single change buys more than adding an entire visual modality does.

### 4.2 The hard ceiling any predictor faces

**Test-retest reliability of the Big Five itself:**

- **Gnambs (2014), meta-analysis of dependability coefficients:** median aggregated ρ_tt = **.816**; at ~4 weeks, estimates range **.77–.82**. Short-interval (1 week–2 months) rank-order stabilities: E .85, C .82, N .82, O .81, A .78.
- **Anusic & Schimmack (2016):** retest correlations decline with interval then **stabilise at about r = .80** after a few years.
- Park et al. note self-report questionnaires typically retest at **.65–.85**, rising with scale length and falling with interval.

**The arithmetic of the ceiling:** the maximum observable correlation between a perfectly reliable predictor and a criterion of reliability r_yy is √r_yy. With r_yy = .80, **no predictor can exceed r ≈ .89** against a single-administration self-report — and that is the *generous* bound, assuming a noiseless predictor.

**The practical ceiling is much lower.** The "personality coefficient" — the empirical upper limit on how well any *behaviour* predicts a *trait* — is **r = .30 to .40** (Meyer et al. 2001; Roberts et al. 2007). Azucar et al. explicitly frame their pooled .29–.40 as sitting *at* that limit:

> "the predictive power of digital footprints over personality traits is in line with the standard 'correlational upper-limit' for behavior to predict personality"

**This is the most important structural fact in the whole review.** Behavioural channels — posting times, app usage, mobility, image content — are already at their theoretical ceiling. **Grinding on behavioural features cannot produce large gains, because there is nothing left above .40.** Only *declared-preference* channels (Likes, follows, music artists, saved content) break through, and only up to ~.56–.66.

Cross-study caveat: **Moreno et al. 2021 found the personality instrument was NOT a significant moderator in any trait** across 23 estimates. That contradicts Park et al. only superficially — it is a low-powered between-study test with confounded instruments, versus a high-powered within-study contrast. Trust the within-study number (Δr = +.07).

### 4.3 Informant reports — the number that reframes everything

**Connelly & Ones (2010), *Psychological Bulletin* 136:1092–1122 — 44,178 targets across 263 independent samples:**

| Informant type | Self-other agreement (disattenuated) |
|---|---|
| **Well-acquainted dyads** | **r = .46** |
| Strangers / casual acquaintances | r = .38 |
| Meta-analytic average human judge | **r = .48** |

**Youyou et al. 2015 measured this directly and benchmarked the machine against it:**

| Judge | Accuracy (r) |
|---|---|
| Work colleague | matched by a computer with **10 Likes** |
| Cohabitant / friend | matched with **70 Likes** |
| **Average single friend (10-item measure), in-sample** | **.49** |
| Family member | matched with **150 Likes** |
| **Spouse — the best human judge** | **.58** |
| **Computer, 227 Likes** | **.56** (n.s. vs. spouse: z = −1.68, p = .09) |
| Computer, >500 Likes | .66 |

**Interjudge agreement:** humans .38 (this sample) / .41 (meta-analytic); **computer models .62.** Machines agree with each other far more than people do — which is consistency, not necessarily accuracy.

**One friend with a ten-item questionnaire (about 60 seconds of their time) achieves r = .49.** That is more than *three times* the best image-only result and is matched only by ~100 Facebook Likes. **A single acquaintance is a better data source than an entire photo feed.**

**And humans and algorithms are not measuring the same thing.** Youyou et al., n = 1,919 with both:
- Computer–human consensus: r = .37
- **Computer–human *partial* correlation (controlling self-ratings): r = .07**
- Self–computer partial: .38; self–human partial: .42

> "computer and human judgments each provide unique information."

**Park et al. 2015 confirms and monetises this:**
- Average self–LBA agreement .39; average self–informant agreement .32 (low because they used 2-item informant scales)
- Average LBA–informant agreement .24
- Substantial partial correlations remained in both directions
- **"aggregate ratings (the average of LBA and informant reports) were consistently more accurate than informant ratings alone (p < .001 in each comparison) and more accurate than LBAs for all traits but openness (p < .01)"**

**Averaging the algorithm with one human informant beats either alone.** This is the single best-documented accuracy gain in the entire literature and it costs one short questionnaire.

**Predictive-validity corroboration:** Oh, Wang & Mount (2011), *JAP* 96:762–773 — observer ratings of the Five-Factor Model have **higher operational validity for job performance than self-reports**, show **incremental validity over self-reports**, *and the reverse is not true*; adding more observers consistently improves validity.

---

## 5. The ACCOUNT / BRAND audit case (not persons)

Different problem, different evidence base, and — crucially — a different target construct. An account audit legitimately wants **attributed/perceived** properties (what does this feed communicate?) and **commercial** properties (does it work?). Images are a *much* better input for the first than for the second, and useless for the second.

### 5.1 The central finding: engagement ≠ commercial outcome

**Liadeli, Sotgiu & Verlegh (2023), *Journal of Marketing* — meta-analysis of brands' owned social media:**

| Outcome | Average elasticity |
|---|---|
| Social media **engagement** | **.137** |
| **Sales** | **.353** |

And the mechanism does not transfer:

> "what drives the effect on social media engagement does not necessarily work for sales. More specifically, emotional content is more effective for social media engagement compared to social content (e.g., calls for action, questions) … To stimulate sales, content should be more **functional**, rather than emotional, in nature and communicate product benefits."

Moderators: owned social media is **more effective for brands with *fewer* followers**, and for **new** rather than mature products.

**Corroboration from three directions:**

- **Colicev, Malshe, Pauwels & O'Connor (2018), *JM* 82(1):37–56** — 45 brands, 21 sectors, daily VAR models: **owned social media raises brand awareness and customer satisfaction but NOT purchase intent. Earned social media (consumer conversation volume) raises awareness AND purchase intent.** → *Comment text and mentions are more commercially diagnostic than the brand's own feed.*
- **John, Emrich, Gupta & Norton (2017), *JMR* 54(1):144–155** — five experiments + two meta-analyses, **N > 14,000**: "liking" a brand page does **not** change brand attitudes or purchasing; likes *reflect* pre-existing fondness. Follower count is an outcome, not a cause.
- **Babić Rosario, Sotgiu, de Valck & Bijmolt (2016), *JMR* 53(3):297–318** — 96 studies, 1,532 effect sizes, 40 platforms: average eWOM–sales correlation **r = .091**. Real, but small.
- **Lee, Hosanagar & Nair (2018), *Management Science* 64(11):5105–5131** — 106,316 Facebook messages, 782 firms: brand-personality content (humour, emotion) ↑ engagement; directly informative content (price, deals) ↓ engagement *in isolation* but ↑ when **combined** with brand-personality content. → The optimum is a *blend*, and a feed audit that scores only aesthetics cannot detect it.

### 5.2 What each additional input buys, ranked

| Rank | Input | What it buys | Evidence |
|---|---|---|---|
| **1** | **Actual sales / conversion data** | Converts the audit from an engagement audit into a commercial audit. The two have **different optima** — sales elasticity .353 vs engagement .137, and opposite content prescriptions. Without it every recommendation is optimising the wrong objective. | Liadeli 2023; Colicev 2018; John 2017 |
| **2** | **Platform Insights: reach/impressions + saves + shares + profile visits** | Two distinct gains. **(a) Correct denominator:** engagement-per-follower is a biased estimator; engagement-per-reach is the real rate, and only Insights has reach. **(b) Invisible channel:** median per-post on Instagram — carousels get **37 saves vs 25 comments**; Reels **35 saves vs 33 comments**; images **10 saves vs 20 comments**. Saves are comparable in magnitude to comments and are **completely invisible to scraping**. | Socialinsider 2026, 15M posts / 417,130 pages |
| **3** | **Historical time series (≥6–12 months)** | Every credible marketing estimate above is an **elasticity from a time-series or panel model**. A single snapshot cannot estimate an elasticity at all — it can only describe. This is a categorical capability gain, not an incremental one. | Colicev 2018 (daily VAR); Liadeli 2023 |
| **4** | **Comment text + mentions (earned media)** | Earned media moves **purchase intent**; owned media does not. Comment text is also the only unfiltered source of the audience's own vocabulary for the brand. eWOM–sales r = .091. | Colicev 2018; Babić Rosario 2016 |
| **5** | **Follower demographics + follower–brand fit** | Follower–brand fit, influencer activity and post positivity all have **inverted-U** effects — meaning both too little and too much are wrong, and you cannot locate yourself on the curve without the audience composition. Follower count itself is also inverted-U ("Goldilocks influencers"). | Leung, Gu, Li, Zhang & Palmatier 2022, *JM* 86(6):93–115; Wies, Bleier & Edeling 2023, *JM* |
| **6** | **Format split: Reels vs carousel vs static vs Stories** | Format effects are large and measurable: Reels ≈ **+36% reach vs carousels, +125% vs single images**; carousels highest engagement rate (0.55%) and **9× the saves of single images**; static images declining ~17% YoY in engagement. A feed audit that ignores format is confounding format with content. | Socialinsider 2026 (35M posts / 447,613 pages); Metricool 2026 (24.3M posts) |
| **7** | **Competitor set** | Converts absolute numbers into percentiles. Necessary for judgement ("is 0.6% ER good?"), but adds **nothing causal** — it cannot tell you what to change. Overall Instagram engagement fell ~24% YoY, so any un-benchmarked trend line will read as failure. | Socialinsider 2026 |
| **8** | **More photos from the same feed** | The §3.3 result transplanted: no demonstrated accuracy gain from more images. Useful only for variance/consistency estimates and change detection. | Segalin 2017 |

### 5.3 The one place images genuinely earn their keep

**Attributed personality is 2–3× easier to predict from images than self-assessed personality** (65% vs 54% accuracy on identical PsychoFlickr data; Segalin's APP r reaching ~.68 vs APR ~.26). A brand-account audit asking *"what does this feed communicate to a stranger who scrolls past?"* is asking an **APP question**, where the images are the *cause* of the label. That is a legitimate, well-supported use. The same pipeline pointed at *"what is this business owner like?"* is asking an APR question, where the same images are worth r ≈ .12.

---

## 6. Human input — how much does asking beat any amount of passive data?

### 6.1 Asking is not marginally better; it is categorically better

| Method | Time cost | Correlation with the target construct |
|---|---|---|
| **10-item self-report (TIPI)** | ~60 s | convergence with full BFI: **E .87, N .81, C .75, A .70, O .65 (mean ≈ .77)**; 6-week retest **.72** |
| **10-item self-report (BFI-10)** | ~60 s | mean part-whole r with BFI-44 = **.83**; recovers ~70% of full-scale variance |
| **Full 100-item IPIP** | ~20 min | r = 1.00 by definition; retest ρ_tt ≈ **.82** |
| Facebook Likes, 227 of them | passive | **.56** |
| Language, ≥1,000 words | passive | **.38** |
| One friend, 10-item measure | ~60 s of *their* time | **.49** |
| Images (self-assessed traits) | passive | **≈.12–.19** |

**A one-minute questionnaire outperforms the best passive digital footprint by Δr ≈ +0.21 to +0.27, and outperforms images by Δr ≈ +0.6.** There is no quantity of passive data that closes this gap, because the ceiling on passive behavioural inference is .30–.40 and the ceiling on Like-based inference is ~.66, while a short self-report is *measuring the construct directly at r ≈ .80.*

**Structured elicitation is also the best predictor in the adjacent, well-studied domain.** Sackett, Zhang, Berry & Lievens (2022), *JAP* 107(11):2040–2068 — corrected meta-analytic validities for job performance:

| Predictor | Corrected validity |
|---|---|
| **Structured interview** | **.42** |
| Biodata | .38 |
| General mental ability | .31 |
| Integrity test | .31 |
| **Conscientiousness self-report test** | **.19** |

Structured interviews are now the strongest single predictor, having overtaken cognitive ability once range-restriction overcorrections were removed. **Structure is what makes the interview work** — unstructured judgement performs far worse.

### 6.2 Hybrid human + algorithm — the honest, uncomfortable answer

**Vaccaro, Almaatouq & Malone (2024), *Nature Human Behaviour* — preregistered meta-analysis, 106 experiments, 370 effect sizes, 74 papers:**

| Comparison | Hedges' g | 95% CI |
|---|---|---|
| **Human–AI combination vs. best of either alone** | **−0.23** | [−0.39, −0.07] |
| **Decision tasks** | **−0.27** | [−0.44, −0.10] |
| Creation tasks | +0.19 | [−0.09, 0.48] (n.s.) |
| When humans alone were better than AI | **+0.46** | [0.28, 0.66] |
| **When AI alone was better than humans** | **−0.54** | [−0.71, −0.37] |
| Human augmentation vs. humans alone | +0.64 | [0.53, 0.74] |

**Grove & Zald (2000), *Psychological Assessment* 12(1):19–30:** mechanical prediction is on average **~10% more accurate** than clinical judgement; substantially better in 33–47% of studies; clinical judgement substantially better in only 6–16%. Superiority held "regardless of the judgment task, type of judges, judges' amounts of experience."

**Synthesis — this is a two-sided result and both sides matter:**

1. **Human *input as data* is enormously valuable.** Park et al.: averaging the language model with one informant beat informants alone (p < .001, every trait) and beat the model alone on 4 of 5 traits (p < .01). Youyou et al.: partial r = .07 between computer and human judgements means they capture **almost entirely non-overlapping information**.
2. **Human *override of the output* destroys accuracy.** On decision tasks where the algorithm is already better, human-in-the-loop is **g = −0.54**. Letting a person "adjust" a prediction they cannot outperform reliably makes it worse.

**Operational rule:** take human input **as an input variable to be averaged in**, never as a **veto on the output.**

---

## 7. THE RANKED LIST — what to feed the system, worth what

Ordered by expected incremental value. Each entry states the delta and the evidence class.

### Tier A — categorical gains (Δr ≥ +0.15, or a new capability entirely)

| # | Give the system | Worth roughly | Evidence |
|---|---|---|---|
| **1** | **A 10-item self-report from the subject (TIPI / BFI-10)** | **r ≈ .77–.83 with the full instrument**, vs .56 for the best passive channel and ≈.15 for images. **Δr ≈ +0.25 over the best passive alternative; +0.6 over images.** Costs 60 seconds. | Gosling 2003; Rammstedt & John 2007 |
| **2** | **One informant rating (a friend/colleague, 10 items)** | **r = .46–.49** on its own; and because computer–human partial r = .07, **averaging it with the model beats either alone (p < .001)**. | Connelly & Ones 2010; Youyou 2015; Park 2015 |
| **3** | **Likes / follows / saved-content / subscription lists** | Standalone **r = .56** at 227 items, **.66** above 500. The only channel that breaks the .30–.40 behavioural ceiling. **Δr ≈ +0.35 to +0.45 over images.** | Youyou 2015; Kosinski 2013 |
| **4** | **Music listening history (Spotify library, followed artists)** | Standalone **O .30, E .21, C .19, N .18, A .17**; and **incrementally over demographics: Δr +0.20 (O), +0.15 (E), +0.12 (A)**. Best documented incremental channel in the field. | Nave et al. 2018, n = 21,929 |
| **5** | **A longer/better ground-truth instrument (100-item vs 20-item)** | **Δr = +0.07** on identical data (.41 vs .34, z = 2.65, p = .008). Free — it is a measurement decision, not a data-collection one. | Park et al. 2015 |

### Tier B — real but modest gains (Δr ≈ +0.05 to +0.15)

| # | Give the system | Worth roughly | Evidence |
|---|---|---|---|
| **6** | **Text: posts, captions, DMs — at least 1,000 words per person** | Standalone **r = .38** (avg; O .43, E .42); meta-analytic .26–.30. Predictions are stable at **retest r = .70** over 6 months. | Park 2015; Moreno 2021 |
| **7** | **Age and gender** | Study-level β = .25–.26 for A, N, O; **≈ Δr +.05 to +.08**. Cheapest gain available. | Azucar 2018 |
| **8** | **A second footprint type — any second type** | β = .21–.27 (O, C, N); **≈ Δr +.05 to +.08**. Note the gain is from *diversity*, not from any specific modality. | Azucar 2018 |
| **9** | **More Likes/follows, up to ~300** | **+0.05 to +0.08 per doubling** in the 100–500 range. Diminishing above ~300. First 100 items ≈ as valuable as the next 400. | Youyou 2015 |
| **10** | **Behavioural logs — but only call/message/communication logs, and only for extraversion** | Extraversion **r = .35** (meta); communication logs the only significant moderator (β = .14, p = .03). All-class smartphone models reach **r = .37 median** over 30 days. | Marengo 2023; Stachl 2020 |

### Tier C — narrow or construct-dependent

| # | Give the system | Worth roughly | Evidence |
|---|---|---|---|
| **11** | **Purchase / transaction history** | **r = .15 for Big Five (useless)** but **r = .33 for materialism, comparable for self-control**. Jumps to Tier A *if the target construct is a consumer construct.* | Gladstone, Matz & Lemaire 2019 |
| **12** | **Network structure / who you follow** | Real signal for **extraversion only** (≈ Δr +.10–.15). No validated estimate for the other four traits. | Azucar 2018 (β = .19, p = .06); Marengo 2023 |
| **13** | **More images from the same person** | No demonstrated gain. 1 picture → 200 pictures moved self-assessed accuracy 0.55 → 0.54. | Segalin 2017 ×2 |

### Tier D — measurably worth nothing (the honest entries)

| # | The move | Measured result |
|---|---|---|
| **14** | **Adding pictures on top of other footprint types** | **No significant moderator effect on any trait.** Same meta-analysis found the same for text features. Weak evidence (few picture studies), but never overturned. — *Azucar et al. 2018* |
| **15** | **Adding image features on top of text features** | RMSE 0.71 → 0.69 (−2.8%) on **n = 62**. Statistically indistinguishable from noise. — *Skowron et al. 2016* |
| **16** | **Fusing multiple image feature families with each other** | Best single family 0.59–0.61 → all four fused 0.60–0.62. **Δ = +0.00 to +0.01.** n = 11,736, so this null is well-powered. — *Segalin et al. 2017* |
| **17** | **App-usage data and phone sensor data** | Meta-regression moderator tests: app usage all p ≥ .53; sensors/system data all p ≥ .11. **Nothing.** — *Marengo et al. 2023* |
| **18** | **Newer models / more recent methods** | Meta-regression of effect size on **publication year**: O β = .02, C β = .00, E β = .01, A β = .00, N β = .00 — **all n.s.** A decade of deep learning produced no measurable meta-level improvement. — *Marengo et al. 2023* |
| **19** | **More words, once past ~1,000** | Meta-regression on text length: **not significant.** — *Moreno et al. 2021* |
| **20** | **Human review of the model's output on a decision task** | **g = −0.27** overall; **g = −0.54** when the algorithm was already the better judge. Human input is valuable as an *input*, harmful as a *veto*. — *Vaccaro et al. 2024; Grove & Zald 2000* |
| **21** | **[Brand case] Follower count / page likes as a commercial signal** | Five experiments + two meta-analyses, **N > 14,000**: "liking" a brand page does not change brand attitudes or purchasing. Follower count is an outcome, not a lever. — *John et al. 2017* |

### Tier A′ — the brand/account audit, ranked separately

| # | Give the system | Worth roughly |
|---|---|---|
| **B1** | **Sales / conversion data** | Sales elasticity **.353** vs engagement elasticity **.137**, with *opposite* content prescriptions (functional for sales, emotional for engagement). Without it the audit optimises the wrong objective. |
| **B2** | **Insights: reach, saves, shares, profile visits, follower demographics** | Fixes the denominator (per-reach, not per-follower) **and** recovers a channel invisible to scraping — carousels get 37 saves vs 25 comments. |
| **B3** | **6–12 months of historical performance** | Enables elasticity estimation at all. A snapshot can describe; only a time series can attribute. |
| **B4** | **Comment text and mentions** | Earned media moves purchase intent; owned media does not. eWOM–sales r = .091. |
| **B5** | **Follower–brand fit / audience composition** | Inverted-U effects mean you cannot position yourself on the curve without it. |
| **B6** | **Format labels (Reel / carousel / static / Story)** | Reels +36% reach vs carousels, +125% vs static; carousels 9× the saves of static. Ignoring format confounds it with content quality. |
| **B7** | **Competitor set** | Percentile context only. No causal content. |
| **B8** | **More photos of the same feed** | ≈ 0. |

---

## 8. The three sentences that matter

1. **Images are the weakest input the system currently has, and the meta-analytic evidence says adding more of them adds nothing** — but they are legitimately good at the *attributed/perceived* question ("what does this communicate?"), which is what a brand-account audit is actually asking.
2. **The highest-value additions are not more passive data — they are declared preferences (Likes, follows, music, saved content: r = .56–.66) and one minute of asking (self-report r ≈ .80; one informant r ≈ .49, and averaging the informant with the model beats both).**
3. **Behavioural channels are already at their theoretical ceiling of r ≈ .30–.40, so no amount of feature engineering on photos, posting times or app logs can produce a large gain** — which is why "give me a follow list and a 10-item questionnaire" beats "give me 200 more photos" by an order of magnitude.

---

## 9. Sources

**Meta-analyses and field-level estimates**
- Azucar, D., Marengo, D., & Settanni, M. (2018). Predicting the Big 5 personality traits from digital footprints on social media: A meta-analysis. *Personality and Individual Differences, 124*, 150–159. https://doi.org/10.1016/j.paid.2017.12.018 — [full text](https://www.cs.columbia.edu/~julia/papers/azucaretal2017.pdf)
- Marengo, D., Elhai, J. D., & Montag, C. (2023). Predicting Big Five personality traits from smartphone data: A meta-analysis on the potential of digital phenotyping. *Journal of Personality*. https://doi.org/10.1111/jopy.12817
- Moreno, J. D., Martínez-Huertas, J. Á., Olmos, R., Jorge-Botana, G., & Botella, J. (2021). Can personality traits be measured analyzing written language? A meta-analytic study on computational methods. *Personality and Individual Differences, 177*, 110818. https://doi.org/10.1016/j.paid.2021.110818
- Connelly, B. S., & Ones, D. S. (2010). An other perspective on personality: Meta-analytic integration of observers' accuracy and predictive validity. *Psychological Bulletin, 136*(6), 1092–1122.
- Oh, I.-S., Wang, G., & Mount, M. K. (2011). Validity of observer ratings of the five-factor model of personality traits: A meta-analysis. *Journal of Applied Psychology, 96*(4), 762–773.
- Gnambs, T. (2014). A meta-analysis of dependability coefficients (test–retest reliabilities) for measures of the Big Five. *Journal of Research in Personality, 52*, 20–28.
- Anusic, I., & Schimmack, U. (2016). Stability and change of personality traits, self-esteem, and well-being. *JPSP, 110*(5), 766–781.
- Grove, W. M., Zald, D. H., Lebow, B. S., Snitz, B. E., & Nelson, C. (2000). Clinical versus mechanical prediction: A meta-analysis. *Psychological Assessment, 12*(1), 19–30.
- Vaccaro, M., Almaatouq, A., & Malone, T. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-024-02024-1 — [preprint](https://arxiv.org/abs/2405.06087)
- Sackett, P. R., Zhang, C., Berry, C. M., & Lievens, F. (2022). Revisiting meta-analytic estimates of validity in personnel selection. *Journal of Applied Psychology, 107*(11), 2040–2068.

**Primary studies — channels**
- Youyou, W., Kosinski, M., & Stillwell, D. (2015). Computer-based personality judgments are more accurate than those made by humans. *PNAS, 112*(4), 1036–1040. https://doi.org/10.1073/pnas.1418680112
- Kosinski, M., Stillwell, D., & Graepel, T. (2013). Private traits and attributes are predictable from digital records of human behavior. *PNAS, 110*(15), 5802–5805.
- Park, G., Schwartz, H. A., Eichstaedt, J. C., Kern, M. L., Kosinski, M., Stillwell, D. J., Ungar, L. H., & Seligman, M. E. P. (2015). Automatic personality assessment through social media language. *JPSP, 108*(6), 934–952. — [full text](http://www.peggykern.org/uploads/5/6/6/7/56678211/park_2015_-_automatic_personality_assessment_through_social_media_language.pdf)
- Stachl, C., et al. (2020). Predicting personality from patterns of behavior collected with smartphones. *PNAS, 117*(30), 17680–17687.
- Nave, G., Minxha, J., Greenberg, D. M., Kosinski, M., Stillwell, D., & Rentfrow, J. (2018). Musical preferences predict personality: Evidence from active listening and Facebook Likes. *Psychological Science, 29*(7), 1145–1158.
- Gladstone, J. J., Matz, S. C., & Lemaire, A. (2019). Can psychological traits be inferred from spending? Evidence from transaction data. *Psychological Science, 30*(7), 1087–1096.
- Segalin, C., Celli, F., Polonio, L., Kosinski, M., Stillwell, D., Sebe, N., Cristani, M., & Lepri, B. (2017). What your Facebook profile picture reveals about your personality. *ACM Multimedia '17*. https://arxiv.org/abs/1708.01292
- Segalin, C., Perina, A., Cristani, M., & Vinciarelli, A. (2017). The pictures we like are our image: Continuous mapping of favorite pictures into self-assessed and attributed personality traits. *IEEE Trans. Affective Computing, 8*(2), 268–285.
- Liu, L., Preoţiuc-Pietro, D., Riahi, Z., Moghaddam, M. E., & Ungar, L. (2016). Analyzing personality through social media profile picture choice. *ICWSM 2016*.
- Skowron, M., Tkalčič, M., Ferwerda, B., & Schedl, M. (2016). Fusing social media cues: Personality prediction from Twitter and Instagram. *WWW '16 Companion*, 107–108. — [PDF](https://www.cp.jku.at/people/schedl/Research/Publications/pdf/skowron_www_2016.pdf)

**Instruments**
- Gosling, S. D., Rentfrow, P. J., & Swann, W. B. (2003). A very brief measure of the Big-Five personality domains. *JRP, 37*(6), 504–528.
- Rammstedt, B., & John, O. P. (2007). Measuring personality in one minute or less: A 10-item short version of the Big Five Inventory. *JRP, 41*(1), 203–212.

**Marketing / brand-account**
- Liadeli, G., Sotgiu, F., & Verlegh, P. W. J. (2023). A meta-analysis of the effects of brands' owned social media on social media engagement and sales. *Journal of Marketing, 87*(3).
- Colicev, A., Malshe, A., Pauwels, K., & O'Connor, P. (2018). Improving consumer mindset metrics and shareholder value through social media. *Journal of Marketing, 82*(1), 37–56.
- John, L. K., Emrich, O., Gupta, S., & Norton, M. I. (2017). Does "liking" lead to loving? *JMR, 54*(1), 144–155.
- Babić Rosario, A., Sotgiu, F., De Valck, K., & Bijmolt, T. H. A. (2016). The effect of electronic word of mouth on sales. *JMR, 53*(3), 297–318.
- Lee, D., Hosanagar, K., & Nair, H. S. (2018). Advertising content and consumer engagement on social media: Evidence from Facebook. *Management Science, 64*(11), 5105–5131.
- Leung, F. F., Gu, F. F., Li, Y., Zhang, J. Z., & Palmatier, R. W. (2022). Influencer marketing effectiveness. *Journal of Marketing, 86*(6), 93–115.
- Wies, S., Bleier, A., & Edeling, A. (2023). Finding Goldilocks influencers: How follower count drives social media engagement. *Journal of Marketing, 87*(3).
- Socialinsider (2026). Instagram benchmarks — 35M posts / 447,613 pages (Jan–Dec 2025); Instagram engagement report — 15M posts / 417,130 pages (Oct 2025–Mar 2026). https://www.socialinsider.io/social-media-benchmarks/instagram
- Metricool (2026). Instagram study — 24.3M posts. https://metricool.com/press-release-instagram-study-2026/
