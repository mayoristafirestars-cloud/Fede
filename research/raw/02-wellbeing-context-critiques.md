# What Instagram Photos Reveal About a Person's State and Context — Evidence and Critique

Research brief. Scope: published literature on inferring **wellbeing / mental health, mood, life stage, socioeconomic status, and lifestyle** from Instagram (and closely comparable) photo data, plus the replication and critique record. Compiled 2026-08-23.

**Framing rule used throughout:** a reported "accuracy" or "AUC" is a *discrimination* statistic measured on the study's own sample. Whether it supports a *usable inference about a particular person* depends on the base rate of the trait in the population you deploy on. Every headline number below is therefore re-expressed as positive predictive value (PPV) at realistic prevalence wherever the paper reports enough to do so.

---

## 1. The flagship paper: Reece & Danforth (2017)

**Citation.** Reece, A. G., & Danforth, C. M. (2017). Instagram photos reveal predictive markers of depression. *EPJ Data Science*, 6:15. DOI 10.1140/epjds/s13688-017-0110-z. Preprint: arXiv:1608.03282 (v2, Aug 2016). Erratum: *EPJ Data Science* 6:21, DOI 10.1140/epjds/s13688-017-0118-4.

### 1.1 Method and sample (exact)

| Item | Value |
|---|---|
| Recruitment | Amazon Mechanical Turk, US IP addresses only, ≥100 prior HITs, ≥95% approval rating |
| Began survey | 509 individuals |
| **Refused to share Instagram data** | **221 (43%)** |
| Depressed arm: completed + shared | 84 |
| Depressed arm after CES-D cutoff (score ≥22) | **71** |
| Healthy arm: completed + shared | **95** ("active Instagram users, no history of depression") |
| **Total participants** | **166** |
| **Total photos** | **43,950** (mean 264.8/user, SD 396.1, **median 122.5** — heavily skewed) |
| Depressed mean age | 28.8 (SD 7.09), range 19–55 |
| Healthy mean age | 30.7, range 19–53, 65.3% female (**gender not collected for the depressed arm**) |
| Data collection window | 1 Feb 2016 – 6 Apr 2016 |
| Diagnosis dates | Feb 2010 – Jan 2016; **90.1% fell in 2013–2015** |
| Human-rated photo subset | 13,184 photos, ≥3 MTurk raters each, 0–5 scales for happy/sad/likable/interesting |

**Ground truth.** Self-reported history of a clinical depression diagnosis **plus** a current CES-D score ≥22 (the "optimal cutoff for clinically relevant depression" per the cited literature). Controls were self-declared as having no history of depression. **No clinician ever assessed anyone.** Diagnosis dates were self-recalled and, where participants could not recall, *approximated*.

**Features (the full primary set — it is small).**
- Pixel-mean **Hue**, **Saturation**, **Value** (brightness) per photo.
- **Whether an Instagram filter was applied** (binary from metadata) + which filter.
- **Face present (binary)** and **face count**, via face detection (SI notes the detector slightly undercounted faces in both groups).
- **Number of comments** and **number of likes** received.
- **Posts per user per day** (activity).
- A separate model used only the four human-rating dimensions.

**Unit of analysis.** *User-days*, following De Choudhury et al. — all of one user's posts on one calendar day aggregated into one row.
- All-data model: 43,950 posts (24,811 from depressed users) → **24,713 user-days**, 13,230 depressed = **53.4% prevalence**.
- Pre-diagnosis model: 32,311 posts (13,192 depressed) → **18,513 user-days**, 7,030 depressed = **38% prevalence**.

**Models.** (a) Bayesian logistic regression with uninformative priors for inference (Bayes factors vs. an intercept-only null: K_All = 1.57e5, K_Pre = 1.49e8 — reported as such in the text). (b) For prediction, a suite of supervised learners, reporting only the best: a **1200-tree Random Forest**, hyperparameters tuned by stratified 5-fold CV, **trained on a randomly-selected 70% of total observations and tested on the remaining 30%**, averaged over 5 randomized iterations.

### 1.2 Reported associations

- Higher **hue** (bluer), lower **saturation** (grayer), lower **value** (darker) → depression. All-data predictors at 99% posterior confidence; in the Pre-diagnosis model brightness fell to 90% and **posting frequency fell to 30% (i.e., null)**.
- **More comments** → depression; **fewer likes** → depression.
- Depressed users **more likely to post photos containing faces**, but with a **lower average face count per photo**.
- Depressed users **less likely to apply any filter**. Chi-square of filter independence: χ²_All = 913.80, p ≈ 2.87e-144; χ²_Pre = 807.84, p ≈ 9.17e-164. Among filter users, depressed disproportionately favoured **Inkwell** (color → black-and-white); healthy disproportionately favoured **Valencia** (lightens tint).
- Human ratings: only **sad** and **happy** were significant predictors. Critically, human ratings were **essentially uncorrelated with the computational (HSV) features** — the authors flag this themselves. The one exception was a modest positive correlation of rated happiness with face presence/count.

### 1.3 Reported performance — and what it actually means

The paper explicitly **does not report AUC or ROC**, on the stated grounds that naive accuracy is misleading under class imbalance. It reports:

| Metric | GP benchmark (Mitchell, Vaze & Rao) | All-data μ (σ) | Pre-diagnosis μ (σ) |
|---|---|---|---|
| Recall (sensitivity) | .510 | **.697 (.008)** | **.318 (.012)** |
| Specificity | .813 | **.478 (.010)** | **.833 (.010)** |
| Precision (PPV) | .42 | **.604 (.009)** | **.541 (.009)** |
| NPV | .858 | .579 (.008) | .647 (.003) |
| F1 | .461 | .665 (.006) | .401 (.008) |

The paper's own illustration: "Given 100 observations, our model correctly identified 70% of all depressed cases (n=37), with a relatively low number of false alarms (n=23) and misses (n=17)." Note that this is 100 **user-days from a 53%-prevalence sample**, not 100 people from the population.

**Base-rate re-expression.** Holding the reported sensitivity and specificity fixed and varying prevalence:

| Model | Prevalence | PPV | NPV |
|---|---|---|---|
| All-data (sens .697 / spec .478) | .534 (study sample) | **.605** | .579 |
| All-data | .20 | .250 | .863 |
| All-data | **.083** (US 12-month MDE, adults) | **.108** | .946 |
| All-data | .05 | .066 | .968 |
| Pre-diagnosis (sens .318 / spec .833) | .38 (study sample) | **.539** | .666 |
| Pre-diagnosis | .20 | .323 | .830 |
| Pre-diagnosis | **.083** | **.147** | .931 |
| Pre-diagnosis | .05 | .091 | .959 |

**Read that table carefully.** Deployed at a realistic population prevalence of ~8%, the headline model's positive predictions are **wrong about 89% of the time**. And the All-data model's specificity of **.478 means it flags 52% of all non-depressed user-days**. In a screening context that is close to unusable: you would be telling more than half of healthy users they show markers of depression. The "beats GPs" claim rests on a specificity that is *worse than a coin flip*, purchased in exchange for higher recall — a trade that only looks good because the test set is 53% depressed.

### 1.4 Methodological critiques

These are the load-bearing objections. Several are stated by the authors themselves; the first two are not.

**(a) Subject-level leakage in the train/test split — the most serious problem.** SI text: classifiers were "trained on a randomly-selected 70% of total observations, and tested on the remaining 30%." *Observations are user-days, not users.* With 24,713 user-days drawn from only **166 people** (median 122.5 posts/user; some users contributing hundreds of days), a random row-wise split places the **same individuals in both train and test**. A 1200-tree Random Forest with per-user-stable features (a user's characteristic follower base drives their like/comment counts; a user's camera, editing habits and lighting drive their mean HSV; a user's filter habit is near-constant) can achieve much of its performance by effectively **re-identifying the user** and recalling that user's label. The reported .697/.478 is therefore best read as an upper bound on within-sample memorization, not as an estimate of generalization to a new person. The paper reports no user-level (subject-exclusive / grouped) cross-validation. This is the identical flaw that the facial-age-estimation literature has since had to confront — see §5.

**(b) Temporal confounding between arms.** Depressed users' *pre-diagnosis* posts are, by construction, older; 90.1% of diagnoses fell in 2013–2015, so pre-diagnosis data skews toward 2010–2015. Healthy users' data runs up to the collection date in **early 2016**. Instagram's filter set, default camera quality, image resolution, and platform-wide filter-usage norms all changed substantially over 2010–2016 (heavy filter use was a 2011–2013 phenomenon; Inkwell and Valencia are early-era filters). A classifier fed filter-use, HSV and engagement counts can partly be learning **when a photo was posted**, not who posted it. The paper does not report any date control, cohort matching, or time-stratified analysis. (This is an inference from the reported date distributions and feature set, not a published rebuttal — but it is directly checkable and would need to be ruled out before the causal story is credible.)

**(c) No audience-size control.** Likes and comments are raw counts. They are dominated by **follower count**, which the study did not collect and did not control for. Bakhshi, Shamma & Gilbert (CHI 2014, §6.1) show follower count is the single largest driver of engagement and treat it as the mandatory control. The "depressed users get fewer likes" coefficient is therefore confounded with account popularity, account age, and posting reach. Similarly, "fewer filters" is confounded with era and with engagement (filtered photos get more engagement — see §6.2), so the filter and likes findings are not independent.

**(d) "Pre-diagnosis" ≠ "pre-onset."** The Hypothesis-2 claim ("held even for posts made before first diagnosis") is a claim about *diagnosis timing*, not *illness onset*. Depression typically precedes first clinical diagnosis by months to years, and diagnosis dates here were self-recalled and sometimes approximated. Detecting signal in the months before someone finally saw a clinician is largely detecting *prodromal or already-active illness*, not forecasting future illness in a well person. Note also that Pre-diagnosis recall is **.318** — the model misses roughly two-thirds of the depressed user-days it is claimed to anticipate.

**(e) The GP comparison is not a valid comparison.** Mitchell, Vaze & Rao's general practitioners were diagnosing *individual patients* in *primary care*, at primary-care prevalence, in a single unaided encounter. The model classifies *user-days* in a 53%-prevalence lab sample. Different unit, different population, different prevalence, different decision. The authors partly concede this in a footnote ("Comparing point estimates of accuracy metrics is not a statistically robust means of model comparison"), but the comparison is nonetheless the paper's abstract-level claim and is what the press coverage reproduced. For reference, at 8.3% prevalence the GP operating point (sens .510 / spec .813) yields PPV = **.198** — also poor, but the model does not beat it: the model's All-data PPV at the same prevalence is **.108**.

**(f) MTurk sampling and self-selection.** Depressed participants are MTurk workers who (i) sought and received a clinical diagnosis, (ii) still score ≥22 on CES-D at survey time, (iii) actively use Instagram, and (iv) consented to hand over their entire posting history. The authors explicitly flag the treatment-seeking selection: people who seek mental health services are "well-informed and psychologically minded... [with] little stigma... adequate social support, and high self-efficacy," and they caution against broad inference. Add the 43% consent refusal and the population is narrow and unrepresentative in ways that plausibly correlate with the outcome.

**(g) Construct non-specificity.** The authors note depression is a general clinical state, frequently comorbid, and that a specific comorbid diagnostic class may be driving the result. Controls were screened only for absence of *diagnosed* depression — undiagnosed depressives sit in the control group.

**(h) Posterior predictive check failure.** The paper's own diagnostics report that observations replicated from the joint posterior **consistently overestimated** the proportion of depressed observations (replicated 53.5% vs. original 30.9%, Bayesian p = 1.0) — a flagged model-fit problem.

**(i) The erratum.** Two corrections were published: the exclusion rule was misstated in the Methods (should read "excluded participants with CES-D scores of 21 or lower"), and the "likes" bars in Fig. 2 were the wrong colour (direction of effect misdrawn).

**(j) Convergent-validity failure.** The computational features and human ratings of the same photos were essentially uncorrelated, despite both "predicting" depression. This is a red flag for construct validity: two putative measures of the same latent signal that do not covary suggests at least one is tracking something other than the construct.

### 1.5 Replication record

**There is no published direct replication of Reece & Danforth, successful or failed.** Extensive searching (arXiv, Springer, PLOS, JMIR, Nature portfolio, ICWSM/CSCW/CHI proceedings) surfaced no independent attempt to re-run the protocol on a fresh sample. The paper is heavily cited (~700+) but overwhelmingly as background, not as a replicated finding. **Absence of replication is itself the finding**: the single most-cited claim in this space rests on one MTurk study of 166 people with a leaky evaluation, and nine years later no one has reproduced it. Treat the effect as **unreplicated**.

What *does* exist is a body of methodological work showing that this class of study systematically fails to generalize (§2), and a related-but-distinct Instagram study — Ricard et al., "Exploring the Utility of Community-Generated Social Media Content for Detecting Depression" (*JMIR Mental Health*, 2018; PMC6302231) — which found that *community-generated* signals (comments received) outperformed user-generated content features, consistent with the audience-size confound in (c).

---

## 2. The critique and generalization literature (this is the solid part)

### 2.1 Ernala et al. (2019) — the decisive external-validity demonstration

**Citation.** Ernala, S. K., Birnbaum, M. L., Candan, K. A., Rizvi, A. F., Sterling, W. A., Kane, J. M., & De Choudhury, M. (2019). Methodological Gaps in Predicting Mental Health States from Social Media: Triangulating Diagnostic Signals. *CHI '19*. DOI 10.1145/3290605.3300364.

**Design.** Build classifiers for schizophrenia on Twitter using each of the three "proxy diagnostic signals" the literature relies on — (1) **affiliation** (following a disorder-related account, here @sardaa, N=1847 followers sampled), (2) **self-report** ("I have been diagnosed with schizophrenia", N=412 authors), (3) **clinician-appraised self-report** (635 self-reporters, expert-adjudicated; inter-rater κ=0.81) — each with matched controls (N=640 pool). Then test each model against a **clinically diagnosed schizophrenia patient cohort** recruited through a hospital.

**Results.**

| Model | Internal validity (own held-out data) | External validity (on clinical patient data) |
|---|---|---|
| Affiliation | acc ≈ .89, F1 ≈ .91 | **acc .21, F1 .15, AUC .20** |
| Self-report | acc ≈ .72 | **acc .48, F1 .61, AUC .38** |
| Clinician-appraised self-report | acc ≈ .80 | **acc .55, F1 .70, AUC .51** |
| Patient model (trained on real patients) | acc .72–.75, F1 .77–.79 (5-fold CV) | **AUC .82** |

The best-known proxy achieves **AUC .20 — decisively worse than chance** — on the population it claims to serve. Even the clinician-vetted proxy lands at **AUC .51, i.e., pure chance**. The authors also show that clinically diagnosed people who *do not post about mental health* behave differently from proxy-identified people, and that models learn spurious tokens ("creepy" β=0.241, "jesus" β=0.091, "hell" β=0.096, "help" β=0.401).

**Why this matters for Instagram photo inference:** it is the same architecture of error. Strong in-sample discrimination on a convenience-recruited, symptom-disclosing cohort tells you nothing about performance on an arbitrary person's account.

### 2.2 Chancellor & De Choudhury (2020) — systematic review

**Citation.** Chancellor, S., & De Choudhury, M. (2020). Methods in predictive techniques for mental health status on social media: a critical review. *npj Digital Medicine*, 3:43. DOI 10.1038/s41746-020-0233-7.

**Scope.** 75 studies, 2013–2018. Reported field-level accuracies commonly 80–90%.

**Findings with counts:**
- Six distinct methods of establishing "positive" ground truth were in use (clinician annotation, CS-researcher annotation, crowdworkers, affiliation/network membership, self-report regex, screening questionnaires, acquired annotations from prior work, news reports). **There was no reflection anywhere in the corpus on what ground truth means or which method is preferable.**
- **40/55** studies performing annotation did not validate the annotation.
- 53/75 studies filtered data to manage sampling bias; 42/75 reported the total number of features used.
- Minimum reporting standards, explicitly counted: **71/75** reported N; **42/75** reported number of features; **73/75** reported algorithm; **72/75** reported a validation method; **70/75** reported explicit performance metrics. **Only 32/75 (42%) reported all five.** In five papers, performance could only be *estimated off bar charts*.
- Nearly half (37/75) studied depression; 8 eating disorders; 8 anxiety; 4 self-harm.
- Central conclusion: pervasive **construct-validity failure** — papers rarely define the disorder they claim to measure ("anxiety" is used across five papers without any operationalization), rarely ground it in clinical literature, rarely validate that the proxy captures the construct, and rarely control for confounds or sampling bias. Strong internal validity, poor external validity.

### 2.3 Chancellor et al. (2019) — ethics taxonomy

**Citation.** Chancellor, S., Birnbaum, M. L., Caine, E. D., Silenzio, V. M. B., & De Choudhury, M. (2019). A Taxonomy of Ethical Tensions in Inferring Mental Health States from Social Media. *FAT\* '19*. DOI 10.1145/3287560.3287587. See also: Zhang et al., *A Systematic Review of Ethics Disclosures in Predictive Mental Health Research*, FAccT 2023, DOI 10.1145/3593013.3594082.

Documents that this research area routinely (i) constructs mental-health labels for people who never consented to be so labelled, (ii) has no protocol for what to do about a positive prediction, (iii) creates a re-identification surface, and (iv) risks producing tools that function as covert screening by employers, insurers, or platforms. Reece & Danforth themselves note that strict anonymity was "nearly impossible to guarantee."

### 2.4 The wellbeing-effects literature, for calibration

**Citation.** Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and digital technology use. *Nature Human Behaviour*, 3, 173–182. DOI 10.1038/s41562-018-0506-1. Specification-curve analysis across three datasets, **total n = 355,358**.

Digital technology use explains **at most 0.4% of the variance** in adolescent wellbeing — an effect the authors benchmark as comparable in size to regularly eating potatoes. Relevant here as a **sanity anchor on effect magnitude**: the aggregate relationship between social media behaviour and wellbeing is tiny at population scale. Any claim that a handful of colour statistics from someone's feed sharply identifies their mental state should be read against that.

---

## 3. ICWSM / CSCW work on Instagram, mental health, self-harm and eating disorders

This subfield is **methodologically much stronger than the depression-prediction work**, because most of it is descriptive/characterization research about *content and communities*, not individual-level diagnostic inference. Its claims are correspondingly narrower and hold up better.

**Chancellor, S., Pater, J., Clear, T., Gilbert, E., & De Choudhury, M. (2016). #thyghgapp: Instagram Content Moderation and Lexical Variation in Pro-Eating Disorder Communities.** *CSCW '16*, 1201–1213. DOI 10.1145/2818048.2819963.
- Dataset: **2.5M Instagram posts, 2011–2014**, on pro-ED tags.
- Finding: after Instagram banned/advisory-flagged pro-ED tags, users generated **lexical variants** ("thyghgapp" for "thighgap") at scale; moderation displaced rather than suppressed the community, and variant-using communities became *more* engaged and more toxic. This is a robust, well-evidenced finding about **content and community dynamics** — it says nothing about diagnosing an individual.

**Chancellor, S., Lin, Z., Goodman, E. L., Zerwas, S., & De Choudhury, M. (2016). Quantifying and Predicting Mental Illness Severity in Online Pro-Eating Disorder Communities.** *CSCW '16*. DOI 10.1145/2818048.2819973. Best Paper Honorable Mention.
- Dataset: **~26M posts from ~100K Instagram users** on pro-ED tags.
- Method: topic modelling + novice and clinician annotations to derive a mental-illness-severity (MIS) scale.
- Findings: proportion of users expressing high MIS rising ~**13%/year since 2012**; prior seven months of a user's MIS predicts future MIS at **~81% accuracy**.
- **Limitation to hold onto:** the "81%" is predicting *future expressed severity from past expressed severity within a self-selected pro-ED tag community* — i.e., behavioural persistence in an extreme, self-labelling population. It is not a diagnostic instrument and does not transfer to general Instagram users.

**Chancellor, S., Mitra, T., & De Choudhury, M. (2016). Recovery Amid Pro-Anorexia: Analysis of Recovery in Social Media.** *CHI '16*. And **Chancellor, S., Kalantidis, Y., Pater, J., De Choudhury, M., & Shamma, D. A. (2017). Multimodal Classification of Moderated Online Pro-Eating Disorder Content.** *CHI '17*, DOI 10.1145/3025453.3025985 — image+text classification of moderated pro-ED content; again a *content* classifier, not a person classifier.

**Andalibi, N., Ozturk, P., & Forte, A. (2015). Depression-related Imagery on Instagram.** *CSCW '15 Companion*, 231–234. DOI 10.1145/2685553.2699014.
- **95,046** depression-tagged photos collected over one month; **788** posts qualitatively content-analysed.
- Purely descriptive taxonomy of depression-related imagery and captions (self-loathing, self-harm, loneliness, support-seeking). Establishes that such imagery *exists in volume* under the tag. It does **not** establish that the posters are clinically depressed, nor that non-tagging depressed users post similarly.

**Manikonda, L., & De Choudhury, M. (2017). Modeling and Understanding Visual Attributes of Mental Health Disclosures in Social Media.** *CHI '17*, 170–181. DOI 10.1145/3025453.3025932.
- Computer-vision analysis of visual features (colour), themes, and emotions in Instagram mental-health disclosure posts.
- Finding: imagery serves distinct self-disclosure functions from text — emotional distress, calls for help, explicit vulnerability display. **Descriptive**, on self-disclosing users.

**De Choudhury, M., Kiciman, E., Dredze, M., Coppersmith, G., & Kumar, M. (2016). Discovering Shifts to Suicidal Ideation from Mental Health Content in Social Media.** *CHI '16*, 2098–2110. Reddit, not Instagram, but the canonical suicidality-transition work; subject to the same proxy-label critique in §2.1.

**Guntuku, S. C., Preoţiuc-Pietro, D., Eichstaedt, J. C., & Ungar, L. H. (2019). What Twitter Profile and Posted Images Reveal About Depression and Anxiety.** *ICWSM* 13, 236–246. arXiv:1904.02670.
- Twitter, not Instagram, but the closest methodological cousin. Language model of survey-reported depression/anxiety built on **28,749 Facebook users**, validated on **887 Twitter users** who took the surveys, then used to **impute** labels for **4,132 Twitter users** whose images were analysed.
- Findings: depressed users' *profile* pictures **suppress positive emotion** rather than display negative emotion; show a single face rather than groups; posted images show **grayscale dominance and low aesthetic cohesion**; anxious users show a weaker version of the same. Multitask learning with demographics improves prediction.
- **Two large caveats.** (i) The image analysis is run against **imputed, language-model-derived labels**, not measured depression — errors in the language model propagate into and can manufacture the image findings. (ii) The paper reports *associations controlling for demographics*, and does not present a deployable individual-level classifier with calibrated PPV. Directionally it **corroborates the grayscale/low-saturation signal** from Reece & Danforth, which is the single most-replicated-ish observation in this literature — but corroboration of a weak group-level association is not validation of individual prediction.

---

## 4. Socioeconomic status, income, and occupation inference from imagery

### 4.1 Gebru et al. (2017) — cars → demographics (aggregate only)

**Citation.** Gebru, T., Krause, J., Wang, Y., Chen, D., Deng, J., Aiden, E. L., & Fei-Fei, L. (2017). Using deep learning and Google Street View to estimate the demographic makeup of neighborhoods across the United States. *PNAS*, 114(50), 13108–13113. DOI 10.1073/pnas.1700035114. Preprint arXiv:1702.06683.

**Scale.** **50 million** Street View images; **200** US cities; **3,068** ZIP codes; **39,286** voting precincts. DPM car detection → **22 million** vehicles (**32%** of vehicles in the studied cities, ~8% of all US automobiles); CNN classification into **2,657** fine-grained make/model/year classes at 0.2 s/vehicle.

**Performance (city-level, 165 held-out test cities):** median household income **r = 0.82**; %Asian **r = 0.87**; %Black **r = 0.81**; %White **r = 0.77**; graduate degree **r = 0.70**; bachelor's **r = 0.58**; some college **r = 0.62**; high school **r = 0.65**; less than high school **r = 0.54**. Voter preference **r = 0.73**. ZIP-level examples: %Caucasian in Seattle r = 0.84; education in Milwaukee r = 0.70–0.83; income in Tampa r = 0.87. Precinct classification: Milwaukee 264/311 = **85%**, Gilbert AZ 58/60 = **97%**, Birmingham 87/105 = **83%**. Headline heuristic: sedans > pickups in a 15-minute drive → 88% chance the city votes Democratic; otherwise 82% Republican.

**The limitation that matters.** Every one of these numbers is an **ecological** (aggregate, area-level) estimate. The unit is a precinct (~1000 people) or a ZIP code. **Nothing in this paper licenses an inference about an individual.** Applying an area-level r = 0.82 to a person is the textbook ecological fallacy. The paper is a *census-substitution* method, and it is a good one; it is not a person-profiling method.

### 4.2 Jean et al. (2016) — satellite imagery → poverty (also aggregate)

**Citation.** Jean, N., Burke, M., Xie, M., Davis, W. M., Lobell, D. B., & Ermon, S. (2016). Combining satellite imagery and machine learning to predict poverty. *Science*, 353(6301), 790–794. DOI 10.1126/science.aaf7894. Transfer learning from daytime imagery via a nightlight-intensity proxy task; explains up to ~75% of variation in **cluster-level** (village/enumeration-area) average household consumption and assets across five African countries. Again: **cluster-level**, not household-level, not person-level.

### 4.3 Individual-level SES inference — much weaker

- **Facebook profiles → income:** Matz, Menges, Stillwell & Schwartz, "Predicting individual-level income from Facebook profiles," *PLOS ONE* 14(3): e0214369 (2019), PMC6438464. Likes and status updates predict income at **r ≈ 0.43** (roughly 18% of variance). That is a real, non-trivial group-level association and a poor individual estimator.
- **Behaviour/language → SES:** Preoţiuc-Pietro et al., "Studying User Income through Language, Behaviour and Affect in Social Media," *PLOS ONE* 10(9): e0138717 (2015) — occupational-class and income inference from Twitter; reported binary classification ~**82%**, 3-way ~**75%**, on *balanced, curated* occupational samples.
- **Household images → economic status:** Kumar et al., "Assessing the Feasibility and Ethics of Economic Status Prediction using Deep Learning on Household Images," *ACM Journal on Computing and Sustainable Societies* (2024), DOI 10.1145/3675160. Explicitly frames the household/individual level as an **open problem** despite success at aggregated geographic levels, and treats the ethics as a first-class concern.
- **Bias in the models themselves:** "Digital divides in scene recognition: uncovering socioeconomic biases in deep learning systems," *Humanities and Social Sciences Communications* (2025), DOI 10.1057/s41599-025-04719-w — scene-recognition accuracy **increases with household income**, i.e., the vision systems used to infer SES work better on rich people's photos. Errors are structurally concentrated on the poor.

**Bottom line on SES:** aggregate/geographic inference from imagery is genuinely strong (r = 0.7–0.87). Individual inference from a person's own photos is weak (r ≈ 0.4 from far richer signals than photos alone), and is systematically less accurate for lower-income subjects.

---

## 5. Age and gender inference from face images

### 5.1 Gender classification — accuracy and documented bias

**Citation.** Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *PMLR* 81 (FAT\* 2018), 77–91.

**Benchmark.** The Pilot Parliaments Benchmark: **1,270 individuals** from three African and three European parliaments; 44.6% female / 55.4% male; 46.4% darker (Fitzpatrick IV–VI) / 53.6% lighter (I–III); intersectional cells DF 21.3%, DM 25.0%, LF 23.3%, LM 30.3%. Deliberately balanced against prior benchmarks (IJB-A was 79.6% lighter; Adience 86.2% lighter).

**Results (3 commercial APIs: Microsoft Cognitive Services, Face++, IBM Watson):**

| | MSFT | Face++ | IBM |
|---|---|---|---|
| Overall accuracy | **93.7%** | **90.0%** | **87.9%** |
| Darker-skin error | 12.9% | — | **22.4%** (≈7× its lighter-skin error) |
| Lighter-skin error | 0.7% | — | ~3.2% |
| **Darker female error** | **20.8%** | **34.5%** | **34.7%** |
| **Lighter male error** | **0.0%** | 0.7% | 0.3% |

- Female–male error gaps ranged **8.1% to 20.6%**.
- Darker females are **21.3%** of the benchmark but **61.0%–72.4%** of all classification errors. Lighter males are 30.3% of the benchmark and **0.0%–2.4%** of errors.
- A South-Africa-only subset (comparable image quality, 79.2% darker) reproduces the pattern, ruling out image-quality-by-country as the explanation.
- The paper also notes that binary gender classification is itself a contested construct that erases non-binary and trans people.

**Corroboration at scale.** NIST, *Face Recognition Vendor Test (FRVT) Part 3: Demographic Effects*, NISTIR 8280 (Dec 2019). Across 189 algorithms and 18.27M images: **false-positive differentials of 10× to >100×** across demographic groups; highest FPRs for **West African, East African, and East Asian** cohorts, lowest for **Eastern European**; also elevated for the elderly and children. Algorithms developed in China showed *low* FPRs on East Asian faces — evidence that training-data composition, not "difficulty," drives the disparity. (Follow-up: NISTIR 8429, FRVT Part 8.)

### 5.2 Age estimation — headline MAEs and why they are inflated

Reported state-of-the-art mean absolute errors: **~1.7–2.9 years** on MORPH-II (e.g., Deep Regression Forests, arXiv:1712.07195, MAE 2.91; TAA-GCN, arXiv:2305.08779, MAE 1.69). Broad cross-paradigm benchmarks report far worse in the wild: an evaluation of 34 models across eight datasets (UTKFace, IMDB-WIKI, MORPH, AFAD, CACD, FG-NET, APPA-REAL, AgeDB) found zero-shot vision-language models averaging **MAE 5.65 years** and non-LLM specialist models averaging **9.88 years**.

**The critique that matters — and it is the same one as §1.4(a).** Paluzo-Hidalgo et al., *A Call to Reflect on Evaluation Practices for Age Estimation* (arXiv:2307.04570, CVPR 2023) show that **subject-exclusive (identity-disjoint) data splitting is rarely used** in this literature, and that once you enforce it, "all evaluated methods yield comparable results, failing to achieve the performance gains promised by random splitting." In other words: much of the reported progress in facial age estimation was leakage from the same person appearing in train and test. Datasets like IMDB-WIKI also carry substantial label noise. And most work does not disaggregate by gender, ethnicity, or skin tone.

**Practical read:** in-the-wild age estimation on a single photo is realistically ±5 years or worse, with unquantified demographic skew. Sufficient to bucket someone loosely (teen / 20s–30s / 50+); insufficient to assert an age.

---

## 6. What photo content predicts about ENGAGEMENT (the most solid body of work here)

This is the part of the literature with big samples, appropriate controls, correct count models, and effects that have held up in commercial replication.

### 6.1 Bakhshi, Shamma & Gilbert (2014) — faces

**Citation.** Bakhshi, S., Shamma, D. A., & Gilbert, E. (2014). Faces Engage Us: Photos with Faces Attract More Likes and Comments on Instagram. *CHI '14*, 965–974. DOI 10.1145/2556288.2557403.

- **Corpus:** ~**1.1 million** Instagram photos randomly selected from a snowball-sampled user set (~1M analysed).
- **Face detection:** Face++ API (detection only), returning face count, bounding boxes, and estimated age range and gender.
- **Model:** **negative binomial regression** (chosen over Poisson after overdispersion testing), with **two controls: user follower count and user photo count** — follower count has by far the largest coefficient.
- **Result:** a photo containing ≥1 face receives on average **+38% likes** and **+32% comments** versus a photo with no face, *after* controlling for follower count and activity.
- **Null results (important and often dropped in retellings):** the **number** of faces, and the estimated **age** and **gender** of the faces, have **no effect** on engagement.
- **Validation:** MTurk validation of the face detector reported high agreement (e.g., 99% ± 0.44% for ages over 35).
- **Limitations:** 2014 Instagram, pre-algorithmic-feed (chronological ordering), pre-Stories, pre-Reels. Correlational and observational — no random assignment of face-presence, so the effect could reflect selection (people post faces on occasions that are inherently more engaging). The generalization to a 2026 ranked feed is unverified.

### 6.2 Bakhshi, Shamma, Kennedy & Gilbert (2015) — filters

**Citation.** Bakhshi, S., Shamma, D. A., Kennedy, L., & Gilbert, E. (2015). Why We Filter Our Photos and How It Impacts Engagement. *ICWSM* 9(1), 12–21.

- **Mixed method:** 15 in-depth interviews with Flickr mobile users + quantitative analysis of **7.6 million Flickr photos**.
- **Results:** filtered photos are **21% more likely to be viewed** and **45% more likely to be commented on**. Filters that increase **warmth, exposure and contrast** boost engagement most; filters that increase age/vintage effects and high saturation do worse.
- **Two distinct user groups:** professional/serious photographers use filters for subtle correction; casual photographers use bold transformative effects.
- **Limitation:** this is **Flickr, not Instagram**, and Flickr's "views" metric has no Instagram analogue. Directionally, it is the standard citation for "filters help engagement," and note that it points the *opposite* way from Reece & Danforth's association (depressed users filter less, and get fewer likes) — meaning filter use is a plausible mediator that the depression study left uncontrolled.

### 6.3 Marketing literature on brand image content

**Rietveld, R., van Dolen, W., Mazloom, M., & Worring, M. (2020). What You Feel, Is What You Like: Influence of Message Appeals on Customer Engagement on Instagram.** *Journal of Interactive Marketing*, 49(1), 20–53. DOI 10.1016/j.intmar.2019.06.003.
- **46,900 Instagram posts, 59 brands, 6 sectors.** Deep-learning extraction of emotional and informative appeals from images; **negative binomial** model of likes and comments.
- Findings: **positive-high-arousal** and **negative-low-arousal** imagery drive engagement. **Informative appeals generally do not**, with the exception of informative *brand-related* appeals. Explicit product promotion does **not** increase engagement (and informative appeals reduce likes).

**Li & Xie (2020), "Is a Picture Worth a Thousand Words? An Empirical Study of Image Content and Social Media Engagement,"** *Journal of Marketing Research* 57(1), 1–19 — image presence and image quality/professionalism raise engagement on Twitter and Instagram; the presence of a face raises it further, consistent with §6.1.

**Consumer Engagement With Visual Content on Instagram (Journal of Interactive Marketing / adjacent, 2022)** — one comprehensive brand-post model reports **R² = 73.1% for likes and 47.5% for comments** — but note that in engagement models nearly all of that explained variance is carried by **follower count and posting cadence**, not image content. Image-content effects are real but incremental. This is the single most important calibration for anyone reading engagement research: *the audience-size term dominates; content features are second-order.*

### 6.4 Follower growth specifically

Note a gap: the literature robustly models **per-post engagement**, and much less robustly models **follower growth over time**. Cross-sectional per-post like counts should not be read as a growth model — the causal direction between followers and engagement runs primarily followers → engagement.

---

## 7. Life events, travel, and family status from photo streams

The weakest-evidenced category, and mostly not Instagram-specific.

- **Personal life-event detection** (travel, birthday, wedding, graduation, new job) has been attempted mainly from **text**, not images: Choudhury & Breslin, "Personal Life Event Detection from Social Media" (HT '14 workshop, CEUR Vol-1210); Dickinson et al., "Identifying Prominent Life Events on Twitter" (K-CAP 2015); Li et al., "Major Life Event Extraction from Twitter based on Congratulations/Condolences Speech Acts" (EMNLP 2014). Reported per-event F1 varies widely by event type; the authors consistently report that combining linguistic and social-interaction features helps but that "some events are relatively more difficult than others." **No study establishes reliable image-only life-event inference.**
- **Travel and mobility from geotagged photos** is well established at the *aggregate* level: Zheng et al., "Mining Travel Patterns from Geotagged Photos," *ACM TIST* 3(3) (2012); Hawelka et al. (2014) on geolocated Twitter; and Barchiesi et al., "Modelling human mobility patterns using photographic data shared online," *Royal Society Open Science* (2015; PMC4555850) — ~16,000 Flickr users, inferred mobility flows agreeing with official UK figures. Home-location inference from social text reaches roughly **58% (city) / 66% (state) / 78% (time zone)** accuracy.
- **The Instagram-specific catch:** Instagram (like Facebook) **strips EXIF metadata on upload**, so precise GPS coordinates are not recoverable from a downloaded image. What remains is (a) the user-attached place tag, which is voluntary, coarse, and often wrong or aspirational, and (b) visual scene recognition, which is imprecise. Aggregate tourism-flow studies (e.g., "An Exploratory Analysis of Geotagged Photos From Instagram for Residents of and Visitors to Vienna," 2020) rely on the *place tag*, not on true geodata.
- **Family status** (partnered, parent, number of children) from images: no validated published method. Kosinski et al. (2013) predict relationship status from Facebook Likes at AUC ≈ .67 and "parents separated before age 21" at AUC ≈ .60 — both barely above chance and from a far richer behavioural signal than photos.

**Honest summary:** you can often *read* life events off someone's feed as a human, from captions and obvious visual cues. There is no validated automated system with published accuracy for doing this from Instagram images, and no basis for quoting a number.

---

## 8. INFERENCES THE LITERATURE DOES NOT SUPPORT

Explicit list. Each item is either (a) not replicated, (b) confounded such that the published number does not mean what it appears to mean, (c) useless at real base rates, or (d) legally prohibited or ethically off-limits — and several are all four.

### 8.1 Health and mental-health status

**Do not infer depression, anxiety, or any psychiatric condition from an individual's Instagram photos.**
- The flagship result (§1) is a single unreplicated MTurk study with subject-level leakage in its evaluation, no follower-count control, an uncontrolled temporal confound, and a 53%-prevalence test set.
- At realistic prevalence its PPV is **~11%** (All-data) or **~15%** (Pre-diagnosis).
- Its specificity of **.478** means it would flag over half of healthy people.
- Ernala et al. (§2.1) show that proxy-labelled models of this exact family collapse to **AUC .20–.51** on clinically diagnosed populations.
- Chancellor & De Choudhury (§2.2) show the field-wide 80–90% accuracies rest on unvalidated ground truth in 40/55 annotated studies and full reporting in only 42% of papers.
- **Legally:** in the EU, mental health is special-category personal data under GDPR Art. 9 — inferring it creates processing of health data requiring an Art. 9 basis, which marketing/analytics does not have. In the US, deriving mental-health inferences may implicate state health-privacy and unfair-practice law even outside HIPAA-covered entities.

**Do not infer eating disorders or self-harm risk about a person.** The Chancellor et al. work (§3) is valid *about content and communities*; its 81% figure predicts *future expressed severity from past expressed severity inside a self-identifying pro-ED tag community*, and does not transfer.

**Do not infer pregnancy, disability, substance use, or medication status.** No validated image-based method exists; all are special-category data.

### 8.2 Sexual orientation

**Not supported. This is the canonical example of a headline that does not survive inspection.**
- Wang, Y., & Kosinski, M. (2018). Deep neural networks are more accurate than humans at detecting sexual orientation from facial images. *Journal of Personality and Social Psychology*, 114(2), 246–257. Reported **81%** (men) and **71%** (women) accuracy at distinguishing gay from straight in **paired** comparisons, vs. human judges at 61%/54%.
- **Rebuttal:** Agüera y Arcas, B., Todorov, A., & Mitchell, M., "Do algorithms reveal sexual orientation or just expose our stereotypes?" (2018) demonstrate the classifier keys on **self-presentation and grooming** — eyeshadow, facial hair, glasses, head pose, tan, camera angle, image framing — i.e., artifacts of dating-profile self-presentation and cultural style, **not facial morphology**. They characterize the enterprise as physiognomy in modern dress.
- **The paired-task inflation:** "81% accuracy" is on forced-choice pairs *known to contain one gay and one straight person*. That task does not exist in the real world. On an unpaired population at ~3.9% prevalence, a classifier at sens = spec = .80 yields **PPV ≈ 14%** — six of every seven people it flags are straight.
- **Legally:** sexual orientation is special-category data under GDPR Art. 9, and **EU AI Act Article 5(1)(g) outright prohibits** biometric categorisation systems that deduce or infer sexual orientation. This is a hard ban, not a risk-managed permission.

### 8.3 Political affiliation

**Not supported for individuals.**
- Kosinski, M. (2021). Facial recognition technology can expose political orientation from naturalistic facial images. *Scientific Reports*, 11, 100. (Author Correction: *Sci Rep* 11, 23292, PMC8617159.) Reports **72%** accuracy on liberal–conservative **face pairs**, vs. chance 50%, humans 55%, and a 100-item personality questionnaire 66%.
- **Same three problems as §8.2:** it is a *paired* task; the images are self-selected (social-media and dating profile pictures), so self-presentation, expression, image resolution, camera and framing are all confounded with political orientation; and Todorov's critique is that the model may be keying on almost anything except stable facial structure. Kosinski's own 2023 follow-up (arXiv:2303.16343) attempts to control for demographics and self-presentation and still reports above-chance results, but the effect shrinks and the confound debate is unresolved.
- Gebru et al.'s 88%/82% voting figures (§4.1) are **precinct-level**, and transferring them to a person is an ecological fallacy.
- **Legally:** political opinions are GDPR Art. 9 special-category data and are named in the **EU AI Act Art. 5(1)(g)** prohibition.

### 8.4 Religion

**Not supported.** The only widely cited figure — 82% for Christian vs. Muslim — is Kosinski, Stillwell & Graepel (2013), and it is an **AUC**, on a **balanced two-class subsample**, from **Facebook Likes** (which include explicit religious pages), not from photos. There is no validated method for inferring religion from Instagram imagery, and religious/philosophical belief is GDPR Art. 9 data and named in the **EU AI Act Art. 5(1)(g)** prohibition.

### 8.5 Race / ethnicity

**Not supported and prohibited.**
- The 95% figure for "African American vs. Caucasian American" is again Kosinski et al. (2013) — an **AUC** on Facebook Likes with a balanced two-class design, largely reflecting cultural-consumption segregation, not a photo method.
- Gebru et al.'s r = 0.77–0.87 for racial composition is **area-level**.
- Face-based racial classification carries the documented error structure of §5: NIST FRVT found **10× to >100×** false-positive differentials, worst for West African, East African and East Asian cohorts.
- **Legally:** racial or ethnic origin is GDPR Art. 9 data and is named in the **EU AI Act Art. 5(1)(g)** prohibition on biometric categorisation.

### 8.6 Emotion and internal affective state from facial expression

**Not supported by the psychology.** Barrett, L. F., Adolphs, R., Marsella, S., Martinez, A. M., & Pollak, S. D. (2019). Emotional Expressions Reconsidered: Challenges to Inferring Emotion From Human Facial Movements. *Psychological Science in the Public Interest*, 20(1), 1–68. A 68-page consensus review across the six canonical categories (anger, disgust, fear, happiness, sadness, surprise) concluding that facial configurations are **not reliable, specific, or generalizable** indicators of emotional state across people, contexts, and cultures. Commercial "emotion AI" reads a *display*, not a *feeling*. Note the EU AI Act separately **prohibits emotion inference in workplace and education settings** (Art. 5(1)(f)), with narrow medical/safety exceptions.

Reece & Danforth's own data contains a small version of this: their human "sad/happy" photo ratings were **uncorrelated with the computational features**, yet both "predicted" depression.

### 8.7 Criminality, trustworthiness, and personality-from-face

**Physiognomy.** Wu & Zhang's "automated inference on criminality" (arXiv:1611.04135) was comprehensively rebutted (Agüera y Arcas, Mitchell & Todorov, "Physiognomy's New Clothes," 2017) — the classifier separated ID photos from mugshots, largely on smiling and collar. Treat any face-to-character claim as pseudoscience by default. See also "Facial Analysis AI as Social Pseudotechnology" (2025) for the current framing.

### 8.8 Individual income or social class from photos

**Not supported at the individual level.** Imagery→SES works at the **aggregate** geographic level (r = 0.7–0.87, §4.1–4.2). Individual-level income prediction from far richer signals (all of a person's Facebook Likes and status updates) reaches only **r ≈ 0.43**. And scene-recognition accuracy itself **increases with the subject's income**, so errors concentrate on poorer people.

### 8.9 Reliable age or gender assertion from a single photo

**Usable only as a coarse bucket, never as an assertion.** Best-in-the-wild age MAE is ~5 years or worse once identity-disjoint splitting is enforced; commercial gender classification is 87.9%–93.7% overall but **20.8%–34.7% wrong for darker-skinned women**. Any pipeline that acts on these labels will act disproportionately wrongly on darker-skinned and female subjects. Binary gender labels also misclassify non-binary and trans people by construction.

---

## 9. What IS solid

For balance, the claims below are well-evidenced and reusable:

1. **Faces in a photo raise Instagram engagement by roughly a third** (+38% likes, +32% comments), controlling for followers and activity, on ~1.1M photos with an appropriate count model. The *number* of faces, their age and their gender do not matter. (Bakhshi et al. 2014; corroborated by Li & Xie 2020.)
2. **Filtered photos out-engage unfiltered ones**, with warmth/exposure/contrast filters best (+21% views, +45% comments on 7.6M Flickr photos). (Bakhshi et al. 2015.)
3. **Emotional imagery beats informative imagery for brand engagement**; explicit product promotion does not lift engagement. (Rietveld et al. 2020, 46,900 posts / 59 brands.)
4. **Follower count and posting cadence dominate engagement variance**; image-content effects are real but second-order. Any content effect quoted without an audience-size control should be discounted.
5. **Aggregate socioeconomic inference from imagery works well** at the precinct/ZIP/cluster level (r = 0.7–0.87 for income, race, education; ~75% of variance for cluster consumption). (Gebru et al. 2017; Jean et al. 2016.)
6. **Pro-ED and mental-health content communities on Instagram are describable and moderation displaces rather than removes them** (2.5M posts, lexical-variant adaptation). (Chancellor et al. 2016.)
7. **Face-analysis systems have large, measured, intersectional accuracy disparities** — this is one of the most replicated findings in the whole area (Gender Shades + NIST FRVT Part 3 across 189 algorithms).
8. **Group-level colour associations with depressed mood** (bluer/grayer/darker imagery) appear in more than one dataset — Reece & Danforth on Instagram and Guntuku et al. on Twitter both report grayscale/low-saturation dominance. This is the closest thing to a corroborated signal in the wellbeing literature. It is a **weak group-level association**, not an individual test.

---

## 10. One-line rule of thumb

> A group-level association strong enough to publish is almost never strong enough to act on for a named individual. Ask three questions of every number: *What was the unit of analysis?* *Was the train/test split disjoint by person?* *What is the base rate where you plan to use it?* In this literature, those three questions dissolve most of the headlines.

---

## Full citation list

1. Reece, A. G., & Danforth, C. M. (2017). Instagram photos reveal predictive markers of depression. *EPJ Data Science*, 6:15. DOI 10.1140/epjds/s13688-017-0110-z. arXiv:1608.03282.
2. Reece, A. G., & Danforth, C. M. (2017). Erratum. *EPJ Data Science*, 6:21. DOI 10.1140/epjds/s13688-017-0118-4.
3. Ernala, S. K., et al. (2019). Methodological Gaps in Predicting Mental Health States from Social Media. *CHI '19*. DOI 10.1145/3290605.3300364.
4. Chancellor, S., & De Choudhury, M. (2020). Methods in predictive techniques for mental health status on social media: a critical review. *npj Digital Medicine*, 3:43. DOI 10.1038/s41746-020-0233-7.
5. Chancellor, S., Birnbaum, M. L., Caine, E. D., Silenzio, V. M. B., & De Choudhury, M. (2019). A Taxonomy of Ethical Tensions in Inferring Mental Health States from Social Media. *FAT\* '19*. DOI 10.1145/3287560.3287587.
6. Chancellor, S., Pater, J., Clear, T., Gilbert, E., & De Choudhury, M. (2016). #thyghgapp: Instagram Content Moderation and Lexical Variation in Pro-Eating Disorder Communities. *CSCW '16*. DOI 10.1145/2818048.2819963.
7. Chancellor, S., Lin, Z., Goodman, E. L., Zerwas, S., & De Choudhury, M. (2016). Quantifying and Predicting Mental Illness Severity in Online Pro-Eating Disorder Communities. *CSCW '16*. DOI 10.1145/2818048.2819973.
8. Chancellor, S., Kalantidis, Y., Pater, J., De Choudhury, M., & Shamma, D. A. (2017). Multimodal Classification of Moderated Online Pro-Eating Disorder Content. *CHI '17*. DOI 10.1145/3025453.3025985.
9. Andalibi, N., Ozturk, P., & Forte, A. (2015). Depression-related Imagery on Instagram. *CSCW '15 Companion*, 231–234. DOI 10.1145/2685553.2699014.
10. Manikonda, L., & De Choudhury, M. (2017). Modeling and Understanding Visual Attributes of Mental Health Disclosures in Social Media. *CHI '17*, 170–181. DOI 10.1145/3025453.3025932.
11. Guntuku, S. C., Preoţiuc-Pietro, D., Eichstaedt, J. C., & Ungar, L. H. (2019). What Twitter Profile and Posted Images Reveal About Depression and Anxiety. *ICWSM* 13, 236–246. arXiv:1904.02670.
12. Ricard, B. J., Marsch, L. A., Crosier, B., & Hassanpour, S. (2018). Exploring the Utility of Community-Generated Social Media Content for Detecting Depression. *JMIR Mental Health*, 5(4):e11817.
13. Gebru, T., Krause, J., Wang, Y., Chen, D., Deng, J., Aiden, E. L., & Fei-Fei, L. (2017). Using deep learning and Google Street View to estimate the demographic makeup of neighborhoods across the United States. *PNAS*, 114(50), 13108–13113. DOI 10.1073/pnas.1700035114.
14. Jean, N., Burke, M., Xie, M., Davis, W. M., Lobell, D. B., & Ermon, S. (2016). Combining satellite imagery and machine learning to predict poverty. *Science*, 353(6301), 790–794.
15. Matz, S. C., Menges, J. I., Stillwell, D. J., & Schwartz, H. A. (2019). Predicting individual-level income from Facebook profiles. *PLOS ONE*, 14(3):e0214369.
16. Preoţiuc-Pietro, D., Volkova, S., Lampos, V., Bachrach, Y., & Aletras, N. (2015). Studying User Income through Language, Behaviour and Affect in Social Media. *PLOS ONE*, 10(9):e0138717.
17. Kumar, et al. (2024). Assessing the Feasibility and Ethics of Economic Status Prediction using Deep Learning on Household Images. *ACM JCSS*. DOI 10.1145/3675160.
18. (2025). Digital divides in scene recognition: uncovering socioeconomic biases in deep learning systems. *Humanities and Social Sciences Communications*. DOI 10.1057/s41599-025-04719-w.
19. Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *PMLR* 81, 77–91.
20. Grother, P., Ngan, M., & Hanaoka, K. (2019). Face Recognition Vendor Test (FRVT) Part 3: Demographic Effects. NISTIR 8280.
21. Paluzo-Hidalgo, E., et al. (2023). A Call to Reflect on Evaluation Practices for Age Estimation. arXiv:2307.04570.
22. Bakhshi, S., Shamma, D. A., & Gilbert, E. (2014). Faces Engage Us: Photos with Faces Attract More Likes and Comments on Instagram. *CHI '14*, 965–974. DOI 10.1145/2556288.2557403.
23. Bakhshi, S., Shamma, D. A., Kennedy, L., & Gilbert, E. (2015). Why We Filter Our Photos and How It Impacts Engagement. *ICWSM* 9(1), 12–21.
24. Rietveld, R., van Dolen, W., Mazloom, M., & Worring, M. (2020). What You Feel, Is What You Like. *Journal of Interactive Marketing*, 49(1), 20–53.
25. Li, Y., & Xie, Y. (2020). Is a Picture Worth a Thousand Words? *Journal of Marketing Research*, 57(1), 1–19.
26. Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and digital technology use. *Nature Human Behaviour*, 3, 173–182.
27. Kosinski, M., Stillwell, D., & Graepel, T. (2013). Private traits and attributes are predictable from digital records of human behavior. *PNAS*, 110(15), 5802–5805.
28. Wang, Y., & Kosinski, M. (2018). Deep neural networks are more accurate than humans at detecting sexual orientation from facial images. *JPSP*, 114(2), 246–257.
29. Agüera y Arcas, B., Todorov, A., & Mitchell, M. (2018). Do algorithms reveal sexual orientation or just expose our stereotypes? Medium.
30. Agüera y Arcas, B., Mitchell, M., & Todorov, A. (2017). Physiognomy's New Clothes. Medium.
31. Kosinski, M. (2021). Facial recognition technology can expose political orientation from naturalistic facial images. *Scientific Reports*, 11, 100. (Author Correction: *Sci Rep* 11, 23292.)
32. Barrett, L. F., Adolphs, R., Marsella, S., Martinez, A. M., & Pollak, S. D. (2019). Emotional Expressions Reconsidered. *Psychological Science in the Public Interest*, 20(1), 1–68.
33. Barchiesi, D., Moat, H. S., Alis, C., Bishop, S., & Preis, T. (2015). Modelling human mobility patterns using photographic data shared online. *Royal Society Open Science*, 2:150046.
34. Zheng, Y.-T., Zha, Z.-J., & Chua, T.-S. (2012). Mining Travel Patterns from Geotagged Photos. *ACM TIST*, 3(3).
35. Regulation (EU) 2024/1689 (AI Act), Article 5(1)(f) and 5(1)(g). Regulation (EU) 2016/679 (GDPR), Article 9.
