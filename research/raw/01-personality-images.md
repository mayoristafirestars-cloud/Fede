# Inferring Personality (Big Five / OCEAN) from Instagram Photos and Social-Media Images

**Literature review — compiled 2026-08-23**
**Scope:** peer-reviewed and arXiv work on predicting self-assessed or attributed personality traits from photographic content posted, liked, or set as a profile picture on social media (Instagram, Flickr, Twitter/X, Facebook, Weibo), plus the meta-analytic and LLM/VLM boundary literature needed to bound the accuracy claims.

---

## 0. How to read the numbers in this field (read this first)

Four distinctions determine whether a reported number is meaningful. Almost every headline claim in this literature collapses when one of them is ignored.

**(a) Self-assessed (APR) vs. attributed/perceived (APP) personality.**
"Automatic Personality Recognition" predicts the score a person gives *themselves* on a questionnaire. "Automatic Personality Perception" predicts the score *strangers* assign after looking at the images. APP is systematically ~2–3× easier, because the judges only saw the images — the images therefore *cause* the label. Segalin et al. (2017) ran both on identical data: **APR r ≈ 0.26 max; APP r ≈ 0.68 max**. Any paper reporting r > 0.5 from images alone is almost certainly predicting perception, not personality.

**(b) Survey ground truth vs. text-inferred ground truth.**
Several of the largest and most-cited image studies (Liu et al. 2016; Guntuku et al. 2017 dataset D2; Samani et al. 2018 cross-linked set) do **not** have questionnaire scores. They label users by running a *text* model (Schwartz et al. 2013, itself only r ≈ .35 accurate) over their tweets, then predict those labels from images. Reported correlations of .28–.57 are therefore image→text-model agreement, not image→personality. In both Liu et al. and Guntuku et al., when the same analysis was run on the small subsample with real questionnaires, **the correlations vanished**: Liu et al. found only 3 significant correlations at p<.01 out of 260 tests and *none* at p<.001 (n=429).

**(c) Sample size.** The n=100–200 Instagram studies (Ferwerda 113; Ferwerda & Tkalcic 193; Branz 179; El Bahy 316; Celli 100; Guntuku selfies 123) are underpowered for r ≈ .15–.20 effects. At n=113, the critical |r| for p<.05 is ≈ .185 — meaning most of the "significant" correlations sit exactly at the detection threshold and are expected to be unstable. This is borne out: they do not replicate (§5).

**(d) Binarised accuracy is not accuracy.** Papers reporting "62% accuracy" usually mean binary above/below-median (or top-vs-bottom quartile) classification with a 50% baseline. 62% on a quartile split corresponds to a very small underlying effect. Segalin et al. (2017, MM) is the cleanest demonstration: n=11,736 Facebook profile pictures, and the *best* achievable was 0.60–0.62 accuracy on an extreme-quartile split, 0.55–0.56 on a mean split.

---

## 1. Meta-analyses and field-level effect sizes

### 1.1 Azucar, Marengo & Settanni (2018) — the anchor number

> Azucar, D., Marengo, D., & Settanni, M. (2018). *Predicting the Big 5 personality traits from digital footprints on social media: A meta-analysis.* **Personality and Individual Differences, 124**, 150–159. https://doi.org/10.1016/j.paid.2017.12.018

- **Corpus:** 24 papers / 28 studies screened; after removing non-independent samples (11 excluded for reusing myPersonality Facebook data), **14 papers / 16 independent studies, 80 effect sizes** (16 per trait). Platforms: 7 Facebook, 5 Twitter, 3 Sina Weibo, 1 Instagram+Twitter combined.
- **Meta-analytic correlations (random effects), predicted vs. self-reported:**

| Trait | r | 95% CI | τ² | I² | Fail-safe N |
|---|---|---|---|---|---|
| **Openness** | **0.39** | 0.30 – 0.48 | 0.04 | 97.46 | 12,210 |
| **Conscientiousness** | **0.35** | 0.29 – 0.42 | 0.02 | 94.68 | 7,688 |
| **Extraversion** | **0.40** | 0.33 – 0.46 | 0.02 | 95.33 | 11,933 |
| **Agreeableness** | **0.29** | 0.21 – 0.36 | 0.02 | 95.72 | 6,053 |
| **Neuroticism** | **0.33** | 0.27 – 0.39 | 0.01 | 93.15 | 7,197 |

- **No significant difference in effect size across traits.** Heterogeneity was high (I² ≥ 93.15) but true between-study variance was low (τ² 0.01–0.04).
- **No evidence of publication bias:** symmetric funnel plots; Begg & Mazumdar all p ≥ .21; Egger all p ≥ .14; trim-and-fill added no studies.
- **Moderators.** Using *multiple* footprint types raised accuracy for O (β=0.27, R²=0.16), C (β=0.25, R²=0.20), N (β=0.21, R²=0.14); E trended (β=0.18, p=.08). Demographics helped A (β=0.25, R²=0.19) and N (β=0.25, R²=0.19), and marginally O (β=0.26, p=.09). Activity statistics helped E (β=0.19, p=.06).
- **⚠️ Critical for this review:** *"use of features extracted from texts and pictures posted on social media did not improve prediction accuracy of personality traits over use of other types of digital footprints."* Pictures were, in the pooled data, **not** an incrementally useful modality.
- **Interpretation given by authors:** these values sit at the "personality coefficient" / correlational upper limit for behaviour predicting personality (r ≈ .30–.40; Meyer et al. 2001; Roberts et al. 2007). This is the ceiling, not a waypoint.

### 1.2 Hinds & Joinson — convergent-validity meta-analysis (reported in Celli et al. 2025)

Meta-analysis of >30 personality-perception studies: **human perception convergent validity ρ = 0.38; computational prediction convergent validity ρ = 0.30**, across all channels (text, images, video, smartphone). Data source significantly moderates the variance explained — the medium changes what personality signal is available.

### 1.3 Celli, Vinciarelli, Kosinski & Lepri (2025) — 20-year survey

> Celli, F., Vinciarelli, A., Kosinski, M., & Lepri, B. (2025). *Twenty Years of Personality Computing: Threats, Challenges and Future Directions.* arXiv:2503.02082.

- Surveys **15 image-based personality systems (2014–2021)**. Most common algorithms: neural networks (7/15) and SVMs (6/15). Most common features: colour-based (9/15), CNN-implied (7/15), people/faces (7/15), texture (5/15), composition (4/15), visual words (5/15).
- Benchmark table of best reported results across the whole field (all modalities): text-based shared tasks sit at r/F1 ≈ 0.23–0.30 (WASSA 2022–2024), Youyou et al. social-media Likes at 0.56, LLM zero-shot from text at 0.29 (Peters & Matz 2024).
- Notes a **rising shift from Big Five to MBTI** in recent LLM work precisely because "MBTI labels are easier to classify than Big Five scores" — a methodological warning, since MBTI has no accepted construct validity.

---

## 2. Instagram-specific studies

### 2.1 Ferwerda, Schedl & Tkalcic (2016) — the canonical Instagram colour paper

> Ferwerda, B., Schedl, M., & Tkalcic, M. (2016). *Using Instagram Picture Features to Predict Users' Personality.* In **MultiMedia Modeling (MMM 2016)**, LNCS 9516, pp. 850–861. Springer. (Preliminary version: EMPIRE workshop 2015, "Predicting Personality Traits with Instagram Pictures", pp. 7–10, ACM.)

- **Sample:** 126 recruited via Amazon Mechanical Turk (US only, ≥95% HIT approval, ≥1000 HITs); 113 valid after comprehension checks and Mahalanobis outlier removal. Age 18–64 (median 30); 54 M / 59 F.
- **Data:** **22,398 Instagram pictures** crawled via the Instagram API (≈198 pictures/user). Personality: 44-item BFI, 5-point Likert.
- **Features (all user-level means over the picture collection):**
  - *Hue:* fraction of pixels in orange, yellow, green, blue, violet, red bins; aggregated warm (orange/red/yellow) and cold (green/blue/violet) shares.
  - *Saturation:* mean, variance, and share of pixels in low/mid/high saturation terciles.
  - *Value/brightness:* mean, variance, share in low/mid/high value terciles.
  - *Emotion (Valdez & Mehrabian PAD):* Pleasure = .69·V + .22·S; Arousal = −.31·V + .60·S; Dominance = −.76·V + .32·S.
  - *Content:* average number of faces per image (Viola-Jones / Haar + AdaBoost); average number of full human bodies (HOG + SVM), via MATLAB Computer Vision Toolbox.
  - *Filters:* the applied Instagram filter name (crawled separately).
- **Filter results:** 1,487 filter applications across 22,398 pictures; users used on average 13.15 distinct filters out of 25 offered. Only **4 of 25** filters correlated significantly with any trait: Conscientiousness × "Kelvin" r=.203 (p=.044); Agreeableness × "Crema" r=−.205 (p=.042); Agreeableness × "Gotham" r=−.204 (p=.042); Neuroticism × "Hudson" r=.224 (p=.026). The authors **abandoned the filter line of inquiry**, reasoning that the filter name says nothing about the end result.

**Full correlation matrix (Pearson r, n=113):**

| Feature | O | C | E | A | N |
|---|---|---|---|---|---|
| Red | −0.06 | 0.02 | −0.17^ | −0.05 | 0.03 |
| Green | 0.17^ | 0.14 | **0.23^^** | 0.03 | −0.12 |
| Blue | −0.01 | 0.00 | 0.17^ | 0.02 | −0.01 |
| Yellow | 0.01 | 0.04 | 0.01 | 0.14 | −0.07 |
| Orange | −0.03 | −0.07 | −0.16^ | −0.02 | 0.06 |
| Violet | 0.00 | −0.06 | −0.09 | −0.07 | 0.06 |
| Saturation mean | 0.16^ | 0.06 | 0.03 | −0.04 | 0.00 |
| Saturation variance | **0.20^^** | 0.16^ | **0.19^^** | 0.10 | −0.05 |
| Saturation low | −0.08 | −0.02 | 0.02 | 0.07 | 0.01 |
| Saturation mid | 0.08 | −0.09 | 0.02 | 0.07 | 0.01 |
| Saturation high | 0.13 | 0.10 | 0.04 | −0.01 | 0.01 |
| Value (brightness) mean | **−0.25\*** | −0.10 | −0.19^ | −0.07 | 0.22^ |
| Value variance | 0.06 | 0.00 | 0.00 | −0.07 | 0.05 |
| Value low (dark share) | **0.28\*\*** | 0.09 | 0.16^ | −0.05 | −0.16^ |
| Value mid | −0.09 | 0.06 | 0.04 | 0.15^ | −0.06 |
| Value high (bright share) | −0.20^ | −0.12 | −0.18^ | −0.08 | 0.21^ |
| Warm | −0.05^^ | −0.04 | −0.20 | 0.00 | 0.03 |
| Cold | 0.05^^ | 0.04 | 0.20 | 0.00 | −0.03 |
| Pleasure | **−0.19^^** | −0.08 | −0.18^ | −0.09 | **0.22^^** |
| Arousal | **0.23\*** | 0.09 | 0.10 | 0.00 | −0.08 |
| Dominance | **0.28\*\*** | 0.11 | 0.17^ | 0.05 | −0.18^^ |
| # of faces | −0.16^ | 0.03 | 0.11 | −0.11 | −0.03 |
| # of people | **−0.22^^** | −0.05 | −0.07 | −0.01 | 0.07 |

*^p<0.1, ^^p<.05, \*p<.01, \*\*p<.001. Note the significance markers on the Warm/Cold rows appear misplaced in the published table (r=−0.05 marked p<.05 while r=−0.20 for E is unmarked); treat the warm/cold result as the Red/Green/Blue result restated.*

- **Prediction (10-fold CV × 10 iterations, Weka), RMSE on the [1,5] scale:**

| Trait | RBF Network | Random Forest | M5' Rules | Quercia et al. (Twitter, M5') |
|---|---|---|---|---|
| Openness | **0.68** | 0.71 | 0.77 | 0.69 |
| Conscientiousness | **0.66** | 0.67 | 0.73 | 0.76 |
| Extraversion | 0.90 | 0.95 | 0.96 | **0.88** |
| Agreeableness | **0.69** | 0.71 | 0.78 | 0.79 |
| Neuroticism | 0.95 | 1.01 | 0.97 | **0.85** |

- **Author summary of directions:** *Openness* → more green, lower brightness, higher saturation, more cold colours, fewer faces and people. *Conscientiousness* → mix of saturated and unsaturated colours. *Extraversion* → more green and blue, lower brightness, mixed saturation. *Agreeableness* → fewer dark and fewer bright areas (mid-range). *Neuroticism* → higher brightness.
- **Stated limitations:** n=113 is small; US-only sample and colour meaning is culturally variable; content was not analysed at all (colour only).
- **⚠️ Note on the RMSE framing:** a trait scored on [1,5] with SD ≈ 0.7–0.8 has a *mean-prediction baseline* RMSE roughly equal to its SD. RMSE of 0.66–0.95 is therefore near-baseline for several traits. The paper does not report the baseline, and "personality can be accurately predicted" is not supported by these numbers.

### 2.2 Ferwerda & Tkalcic (2018) — image *content* on Instagram

> Ferwerda, B., & Tkalcic, M. (2018). *You Are What You Post: What the Content of Instagram Pictures Tells About Users' Personality.* **HUMANIZE '18** workshop (IUI), CEUR-WS Vol-2068.
> Companion: Ferwerda, B., & Tkalcic, M. (2018). *Predicting Users' Personality from Instagram Pictures: Using Visual and/or Content Features?* **UMAP '18**, pp. 157–161. ACM. https://doi.org/10.1145/3209219.3209248

- **Sample:** 233 MTurk recruits (US, ≥95% HIT approval), **193 valid**; age 18–64 (median 30), 104 M / 89 F. **54,962 Instagram pictures** (≈285/user). BFI-44.
- **Pipeline:** Google Cloud Vision API label detection → 4,090 unique labels → doc2vec embeddings (pre-trained on English Wikipedia) → k-means into 400 clusters → manual collation into **17 content categories**: architecture, body parts, clothing, music instruments, art, performances, botanical, cartoons, animals, foods, sports, vehicles, electronics, babies, leisure, jewelry, weapons. Per-user category counts normalised to [0,1].

**Spearman ρ, content category × trait (n=193); bold = p<.001 after Bonferroni:**

| # | Category | O | C | E | A | N |
|---|---|---|---|---|---|---|
| 1 | Architecture | −0.009 | −0.009 | 0.044 | −0.002 | −0.043 |
| 2 | Body parts | −0.039 | −0.075 | 0.023 | 0.115 | 0.108 |
| 3 | **Clothing** | 0.040 | **0.148** | 0.110 | **0.234** | **−0.184** |
| 4 | **Music instruments** | **0.156** | 0.133 | 0.034 | 0.049 | −0.081 |
| 5 | Art | 0.048 | −0.003 | 0.122 | 0.111 | −0.065 |
| 6 | Performances | 0.105 | 0.113 | 0.088 | 0.051 | −0.027 |
| 7 | Botanical | 0.002 | −0.034 | −0.074 | 0.099 | 0.057 |
| 8 | Cartoons | 0.027 | −0.040 | 0.053 | 0.050 | −0.076 |
| 9 | Animals | 0.008 | −0.003 | −0.008 | −0.015 | 0.112 |
| 10 | Foods | −0.069 | 0.027 | −0.012 | −0.029 | −0.016 |
| 11 | **Sports** | −0.087 | **0.156** | 0.023 | −0.003 | −0.135 |
| 12 | Vehicles | −0.067 | 0.054 | 0.024 | 0.054 | −0.028 |
| 13 | **Electronics** | −0.057 | 0.097 | **0.167** | 0.062 | −0.132 |
| 14 | Babies | −0.009 | 0.024 | −0.026 | 0.010 | 0.058 |
| 15 | **Leisure** | −0.042 | 0.112 | 0.085 | **0.180** | −0.124 |
| 16 | **Jewelry** | −0.055 | −0.070 | −0.052 | −0.017 | **0.188** |
| 17 | Weapons | 0.009 | 0.096 | −0.019 | 0.041 | 0.032 |

- **Summary:** O → music instruments. C → clothing, sports. E → electronics. A → clothing, leisure. N → jewelry (+), clothing (−).
- **UMAP '18 headline finding:** visual (colour) features and content features **perform about equally well, and combining them does not increase predictive power** — i.e. colour and semantic content in Instagram photos carry largely redundant, not complementary, signal at this sample size.
- **⚠️** With 85 tests (17 categories × 5 traits), Bonferroni-corrected p<.001 survivors are 8 cells with |ρ| = .15–.23. No cross-validated prediction numbers are given in the HUMANIZE paper.

### 2.3 Kim & Kim (2018) — computer vision on Instagram, colour + faces + emotion

> Kim, Y., & Kim, J. H. (2018). *Using computer vision techniques on Instagram to link users' personalities and genders to the features of their photos: An exploratory study.* **Information Processing & Management, 54**(6), 1101–1114. https://doi.org/10.1016/j.ipm.2018.07.005

- Extracted pixel-level features and facial-emotion features from Instagram photos; personality assessed by survey.
- **Findings:** Extraversion, Agreeableness and Openness were *partly* associated with emotions expressed on faces in the photos; several pixel features correlated with Extraversion, Agreeableness, Conscientiousness and gender.
- **RMSE benchmarks** (reported by Branz et al. 2020 for comparison, [1,5] scale): O 0.62, C 0.58, E 0.61, A 0.56, N 0.67.
- Companion: Kim & Kim (2019), *Instagram user characteristics and the color of their photos: Colorfulness, color diversity, and color harmony*, Information Processing & Management.

### 2.4 Branz, Brockmann & Hinze (2020) — first European Instagram replication attempt

> Branz, L., Brockmann, P., & Hinze, A. (2020). *Red Is Open-Minded, Blue Is Conscientious: Predicting User Traits From Instagram Image Data.* **PEOPLES @ COLING 2020**, pp. 23–28. ACL Anthology 2020.peoples-1.3.

- **Sample:** 182 German university students (100 F, 79 M, 3 non-binary excluded → **179 analysed**), ages 18–36 (M=23, SD=3.29). **16,458 images** scraped from their Instagram profiles. Personality: German BFI-2.
- **Features:** exactly the Ferwerda (2015/2016) set — saturation mean/variance; % red/orange/yellow/green/blue/purple/warm/cold pixels; normalised brightness; contrast; PAD. Plus Google Vision API labels → 4,537 unique labels → **29 content categories**.
- **Model:** Random Forest regression/classification, 10-fold CV.

**Spearman ρ, image features × traits (n=179); bold = p≤.05:**

| Feature | O | C | E | A | N | Age |
|---|---|---|---|---|---|---|
| A. Avg saturation | **−0.17** | 0.00 | −0.08 | −0.10 | −0.04 | 0.08 |
| B. Saturation variance | 0.10 | −0.15 | 0.04 | −0.13 | −0.05 | 0.00 |
| C. % Red pixels | **0.24** | **−0.20** | 0.05 | −0.09 | 0.03 | −0.07 |
| D. % Orange | −0.03 | 0.00 | −0.03 | 0.09 | 0.10 | **0.15** |
| F. % Green | −0.07 | 0.03 | **−0.15** | 0.04 | 0.01 | −0.07 |
| G. % Blue | **−0.25** | **0.20** | 0.05 | −0.07 | −0.03 | **−0.20** |
| I. % Warm | **0.25** | **−0.17** | 0.01 | 0.08 | 0.03 | 0.11 |
| J. % Cold | **−0.25** | **0.17** | −0.01 | −0.08 | −0.03 | −0.11 |
| L. Contrast | **−0.21** | 0.05 | −0.02 | 0.06 | −0.07 | −0.14 |
| N. Arousal | **−0.19** | −0.05 | −0.05 | −0.07 | −0.09 | 0.02 |
| O. Dominance | **−0.18** | −0.09 | 0.00 | −0.02 | −0.13 | −0.05 |

- **Prediction (RMSE, [1,5]; Kim & Kim 2018 in parentheses):** Openness **0.62** (0.62); Conscientiousness 0.67 (0.58); Extraversion 0.72 (0.61); Agreeableness **0.55** (0.56); Neuroticism 0.79 (0.67). Gender: F1 = 0.79, AUC = 0.78. Age: RMSE 2.88 years on an 18–36 range.
- **⚠️ This is the single most important negative result in the Instagram literature.** Using a near-identical feature set, the authors state: *"only some findings of (Kim and Kim, 2018) and (Ferwerda et al., 2015) (Ferwerda and Tkalcic, 2018b) could be reproduced while in some cases findings even contradict each other (e.g. a preference for red in conscientious users (Kim and Kim, 2018) vs. blue in conscientious users (this study))."*
  - **Openness flips sign on almost everything.** Ferwerda: O ↔ higher saturation (+.16), more cold/green (+.17), lower brightness, higher arousal (+.23), higher dominance (+.28). Branz: O ↔ **lower** saturation (−.17), more **warm/red** (+.24/+.25), **lower** arousal (−.19), **lower** dominance (−.18).
- **What did replicate:** art-related content vs. social scenes for Openness; warmer colours + social scenes for Extraversion, cooler for introverts.
- **Limitations:** German university students only, narrow age band, single content-label-to-category assignment.

### 2.5 El Bahy, Aboutabit & Hafidi (2023, 2024) — Moroccan Instagram, gender-split

> El Bahy, S., Aboutabit, N., & Hafidi, I. (2023). *Analyzing Instagram Images to Predict Personality Traits.* In **Advances in Machine Intelligence and Computer Science Applications (ICMICSA 2022)**, LNNS 656, Springer, ch. 31.
> El Bahy, S., Aboutabit, N., & Hafidi, I. (2024). *Analysis and prediction of personality traits using a self-generated database of Moroccan Instagram users: impact of gender on image content and quantity on prediction accuracy.* **Multimedia Tools and Applications** (April 2024). https://doi.org/10.1007/s11042-024-19101-2

- **Sample:** **316 Moroccan Instagram users** (first Moroccan corpus), NEO-PI questionnaire. Sub-experiments filter to ≥10 photos (n=270) and ≥20 photos (n=210).
- **Features (3 families):** *visual* — 9 colour bins (red, orange, yellow, yellow-green, green, cyan, blue, violet, rose) + warm/cold + luminosity; *content* — abstract, buildings, dark, object, people, cat, dog, sports ball, TV, laptop, cup, bottle, horse, handbag, % images containing faces, number of faces; *emotional* — angry, disgust, fear, happy, neutral, sad, surprise (facial expression classifier).
- **Models:** Random Forest, Decision Tree, Linear Regression, SVR, RBF Network. RMSE on [1,5].

**Best RMSE by trait (Experiment 1, n=316; H = males, F = females, All = pooled):**

| Trait | Best model | Male | Female | Pooled |
|---|---|---|---|---|
| O | RBF | 0.63 | 0.61 | 0.61 |
| C | RBF | 0.61 | 0.67 | 0.67 |
| E | RBF / SVR | 0.82 (SVR) | 0.73 (RBF) | 0.77 (RBF) |
| A | RBF / RF | 0.67 (RBF) | 0.69 (RF) | 0.72 (RF) |
| N | RF / SVR | 0.84 | 0.86 (SVR) | 0.87 (SVR) |

Best overall across the three experiments: **O = 0.59 (males, ≥10 photos, RBF; and females 0.59)**, **C = 0.53 (males, ≥20 photos, RBF)**, A = 0.65–0.66, E = 0.73–0.77, N = 0.74–0.84.

- **Consistent finding:** RMSE improves monotonically as the minimum photo count per user rises (316 → 270 → 210 users with ≥1 / ≥10 / ≥20 photos). More images per user = better prediction.
- **Consistent finding:** **Extraversion and Neuroticism are the hardest traits**; Openness, Conscientiousness and Agreeableness the easiest — matching Ferwerda (2016).
- **Gender split matters:** pooled-gender RMSE is usually *worse* than either single-gender model. Females express more A and E through images; males more C and N.
- **⚠️ Feature→trait directions contradict earlier work and contradict each other across genders:**
  - Females: Extraversion ↔ **cold** colours, blue (r=.14), warm negative (−.16). Males: Extraversion ↔ **warm** colours, red, purple, pink.
  - Females: Openness ↔ abstract objects (.14), fewer people (−.15), dogs (.12), TV (.13); sadness/fear positive.
  - Females: Conscientiousness ↔ yellow (.16), sports ball (.24), TV (.14), cup (.16), disgust (.15), more photos posted (.15).
  - Females: Agreeableness ↔ objects (.20), abstract (.15), orange (.13), cyan (−.12).
  - Females: Neuroticism ↔ no cats (−.16), less disgust (−.13), bright images.

### 2.6 Cooper, Blake, Pauletti, Cooper, Sherman & Lee (2020) — situational/behavioural coding of Instagram photos

> Cooper, A. B., Blake, A. B., Pauletti, R. E., Cooper, P. J., Sherman, R. A., & Lee, D. I. (2020). *Personality Assessment Through the Situational and Behavioral Features of Instagram Photos.* **European Journal of Psychological Assessment, 36**(6), 959–972. https://doi.org/10.1027/1015-5759/a000596

- Human- and machine-coded *situational* cues (using the Riverside Situational Q-sort / DIAMONDS framework), behaviours, classes and displayed affect in Instagram photos, correlated against both "bright side" (Big Five) and "dark side" traits. Key reported result: **openness was positively related to depicted sociability**. Notable as one of the few studies grounding image features in a validated situation taxonomy rather than ad-hoc colour bins.

### 2.7 Organisational-account Instagram studies (personality of accounts, not people)

> Kim, Y., & Kim, J. H. (2021). *Personality of Public Health Organizations' Instagram Accounts and According Differences in Photos at Content and Pixel Levels.* **IJERPH, 18**(8), 3903. https://doi.org/10.3390/ijerph18083903
> (2024). *Personality of organizational social media accounts and its relationship with characteristics of their photos: analyses of startups' Instagram photos.* **BMC Psychology**. https://doi.org/10.1186/s40359-024-01709-6

- 265 US public-health organisation Instagram accounts. Personality of the *account* inferred from post text via IBM Watson Personality Insights (0–1 scale), then related to photo features.
- **Features:** 15 content categories; facial features (count, age, gender, emotion); content diversity (Gini); RGB means/variances; hue/saturation/brightness; contrast, sharpness, colourfulness, naturalness; colour harmony/diversity; PAD.
- **Findings:** Openness ↔ content-level features (+ plant/food/abstract; − people photos, face count). Agreeableness ↔ + people photos, happiness; − food/plant. Extraversion ↔ pixel-level (+ warm colours, naturalness; − brightness, blue). Neuroticism ↔ + brightness, red; − sharpness, naturalness. Conscientiousness ↔ minimal association (slight + colourfulness). Random forest RMSE acceptable for all traits **except Neuroticism**.
- **⚠️ Ground truth is a text-based commercial API applied to an organisation, not a person.** Use only as a directional cue, not as evidence about human personality.

### 2.8 Other Instagram entries

- **"Prediction of Personality Traits Through Instagram Photo HSV"** (2022), Springer LNNS — HSV-only replication in the Ferwerda tradition.
- **"Personality Prediction Model: An Enhanced Machine Learning Approach"** (2025), *Electronics* 14(13), 2558. https://doi.org/10.3390/electronics14132558 — **941 participants** recruited over 8 weeks via LinkedIn/Instagram, BFI scored, Instagram profiles linked for multimodal analysis. Largest survey-labelled Instagram sample to date.
- **"Image and metadata-driven personality inference for career recommendation"** (2026), *Discover Artificial Intelligence*. https://doi.org/10.1007/s44163-026-00981-2 — UAE high-school students; profile metrics + HSV + semantic labels + texture; reports **Logistic Regression 97% accuracy, AUC 0.97** on a pilot of **30 accounts**. ⚠️ **Treat as unreliable.** 97% accuracy at n=30 with hundreds of candidate features is a textbook overfitting/leakage signature and is two orders of magnitude out of line with every properly-powered study in this table.
- **Marengo, Quilghini, Ricci & Settanni (2024).** *Instagram Stories Unveiled: Exploring Links with Psychological Distress, Personality, and Gender.* **Cyberpsychology, Behavior, and Social Networking.** https://doi.org/10.1089/cyber.2023.0316

---

## 3. Flickr — the PsychoFlickr line (Segalin, Cristani, Vinciarelli)

### 3.1 Segalin, Perina, Cristani & Vinciarelli (2017) — IEEE TAC, the reference study

> Segalin, C., Perina, A., Cristani, M., & Vinciarelli, A. (2017). *The Pictures We Like Are Our Image: Continuous Mapping of Favorite Pictures into Self-Assessed and Attributed Personality Traits.* **IEEE Transactions on Affective Computing, 8**(2), 268–285. https://doi.org/10.1109/TAFFC.2016.2516994

- **Corpus (PsychoFlickr):** 300 Flickr *Pro* users × **200 favourited pictures each = 60,000 images**. 214 M / 86 F (71.3% / 28.7%). Nationality known for 288: Italy 153 (51%), UK 31, US 28, France 13, across 37 countries. Age known for only 44 users (20–62, mean 39).
- **Two label sets:**
  - **Self-assessed** (APR): BFI-10, items scored −2..+2, trait scores on [−4, +4].
  - **Attributed** (APP): **12 independent Italian judges**, unacquainted with the users, each viewed all 200 favourite pictures of each of the 300 users and filled the attribution version of BFI-10; the 12 ratings averaged. Judges paid €95 each.
- **Inter-judge reliability (Krippendorff's α):** Openness **0.06**, Conscientiousness **0.12**, Extraversion **0.26**, Agreeableness **0.17**, Neuroticism **0.22**. All statistically significant, comparable to zero-acquaintance norms — but note Openness is essentially at chance agreement, which caps how well it can be predicted as an attributed trait.
- **Features: 82 per image**, four families —
  - *Colour (20):* HSV statistics — hue circular variance R, S mean/SD, V mean/SD ("use of light"); emotion-based valence/arousal/dominance (Valdez–Mehrabian); colour diversity (EMD from a uniform histogram); 11 colour-name shares (black, blue, brown, green, gray, orange, pink, purple, red, white, yellow).
  - *Composition (9):* Canny edge-pixel count; level of detail (number of mean-shift regions); average region size; low depth-of-field (3, H/S/V); rule of thirds (2, S and V over inner rectangle); image size.
  - *Textural (52):* gray-distribution entropy; 12 Daubechies wavelet features (3 levels × HSV); Tamura coarseness/contrast/directionality; 12 GLCM features (contrast, correlation, energy, homogeneity × HSV); 24 GIST channels.
  - *Content (1):* number of faces (extracted **manually**).
- **Methods:** Multiple Instance Regression — bags = users, instances = pictures. Compared Naive MIR, cit-kNN, Clust-Reg, Topic-Sum, Gen-MoG, **Gen-LDA** (best), Counting Grid. LASSO-regularised regression on the bag representation. **Leave-One-User-Out** evaluation.

**Results (Spearman correlation, predicted vs. actual):**

| | Best correlation |
|---|---|
| **Attributed traits (APP)** | **up to 0.68** (Gen-LDA); prior CG/LASSO work reached 0.62 |
| **Self-assessed traits (APR)** | **up to 0.26**; prior work reached 0.22 |

- **Which traits:** *Extraversion is the best-predicted dimension for both attributed and self-assessed traits.* Neuroticism is above average for attributed traits. **Openness is the worst** for attributed traits (judges showed high uncertainty; α = 0.06).
- **Feature/trait covariation (Spearman ρ; |ρ| > 0.12 significant at .05):** significant for **48.5% of features for attributed traits but only 8.3% for self-assessments.** This is the field's cleanest statement of the perception/reality gap.
- **Bag-size effects:** performance grows with the number of pictures, but statistically significant performance is achievable with as few as **5 training pictures** and **1 test picture** per user.
- **Stated interpretation:** *"When the users self-assess their personality, they take into account information that is not available in the favorite pictures like, e.g., personal history, inner state, education, etc. Therefore, the correlation between visual features and trait scores is low."*

**Attributed-trait feature correlations (Spearman ρ), the most quantitatively specific table in the literature:**

| Feature | Agreeableness | Neuroticism | Openness | Conscientiousness | Extraversion |
|---|---|---|---|---|---|
| Average saturation | **+0.40** | **−0.55** | | | +0.21 (GLCM contrast-S) |
| % orange pixels | **+0.45** | **−0.56** | | | |
| % blue pixels | **+0.36** | **−0.52** | | | |
| % red pixels | **+0.30** | **−0.40** | | | |
| Arousal | **+0.38** | **−0.52** | | | |
| Valence | **+0.27** | **−0.40** | | | |
| Rule of thirds | | | **−0.21** | **+0.22** | |
| Level of detail | | | **−0.30** | **+0.19** | |
| Brightness energy (exposure) | | | **+0.35** | | |
| Gray distribution entropy | | | **−0.27** | | |
| Tamura directionality | | | | **+0.23** | **−0.33** |
| GLCM contrast — hue | | | | | **+0.26** |
| GLCM contrast — saturation | | | | | **+0.21** |
| Tamura contrast | | | | | **+0.25** |
| **Number of faces** | **−0.17** | **−0.28** | *n.s.* | **−0.20** | **+0.53** |

*Number of faces is significant at p<.01 for every trait except Openness. Agreeableness and Neuroticism behave as near-mirror images on all colour features; Openness and Conscientiousness behave as near-mirror images on all composition features.*

### 3.2 Segalin, Cheng & Cristani (2017) — CNN version

> Segalin, C., Cheng, D. S., & Cristani, M. (2017). *Social profiling through image understanding: Personality inference using convolutional neural networks.* **Computer Vision and Image Understanding, 156**, 34–50. https://doi.org/10.1016/j.cviu.2016.10.013

- Same PsychoFlickr corpus (300 users, 60,000 favourited images). Fine-tuned an ImageNet-pretrained CNN; one binary classifier per trait.
- **Average binary accuracy: 54% for self-assessed traits; 65% for attributed traits.** Best single result: **68% on attributed Neuroticism.** CNN features beat computational-aesthetics features by roughly 10 points on attributed traits.
- **⚠️ 54% on a binary task = essentially nothing.** This is the honest measure of what liked images tell you about someone's actual self-reported personality.

### 3.3 Related PsychoFlickr work

- Cristani, M., Vinciarelli, A., Segalin, C., & Perina, A. (2013). *Unveiling the multimedia unconscious: implicit cognitive processes and multimedia content analysis.* **ACM MM 2013.** — the original PsychoFlickr paper; agreement between self-assessed and attributed traits ranged **0.32–0.55** by trait; Counting Grid + LASSO gave up to **0.62** (attributed) and **0.22** (self-assessed).
- Sang, J. et al. (2016); Xiong et al.; Guo et al. (2019), *Inferring Personality Traits from Attentive Regions of User Liked Images via Weakly Supervised Dual Convolutional Network*, **Neural Processing Letters** — WSDCN on PsychoFlickr, ~10% better on attributed than self-assessed, best 68% on attributed Neuroticism.

---

## 4. Twitter / X and Facebook profile pictures

### 4.1 Liu, Preoţiuc-Pietro, Riahi Samani, Moghaddam & Ungar (2016) — the largest interpretable profile-picture study

> Liu, L., Preoţiuc-Pietro, D., Riahi Samani, Z., Moghaddam, M. E., & Ungar, L. (2016). *Analyzing Personality through Social Media Profile Picture Choice.* **ICWSM 2016**, 10(1), 211–220. https://doi.org/10.1609/icwsm.v10i1.14738

- **Two datasets:**
  - **TwitterText:** **66,502** Twitter users (31,307 M / 35,195 F, gender from cross-linked accounts), 104,500,740 tweets. Personality **inferred from text** using Schwartz et al. (2013) — trained on ~70k Facebook users, validation r > .3 per trait. Age inferred via Sap et al. (2014) (r = .835 on Facebook).
  - **TwitterSurvey:** **434** users with real IPIP/NEO-PI-R questionnaire scores (254 with ≥50 tweets).
- **Face detection yield:** Face++ found ≥1 face in **36,402 / 66,502** profile images (55%); EmoVu returned emotions for **26,234 / 66,502** (39%). On the survey set: 208/429 and 124/429.
- **85 features in 6 groups:** Colour (44) — grayscale flag, normalised R/G/B, average RGB, brightness, contrast, saturation, hue, colourfulness, naturalness, sharpness, blur, 17 colour-emotion histogram features, all also saliency-reweighted; Image Composition (10) — rule of thirds, edge distribution, hue count, visual weight, static/dynamic lines; Image Type (5) — default image, is-not-face, one face, multiple faces, face count; Image Demographics (5) — estimated age, gender, Asian/Black/White; Facial Presentation (7) — no glasses / reading glasses / sunglasses, pitch/roll/yaw, face ratio; Facial Expressions (14) — Ekman six + neutral, eye openness ×2, attention, expressiveness, positive/negative mood, valence, smiling.
- **All correlations partialled for age and gender.**

**Pearson r, profile-image feature × trait (n=66,502, text-inferred labels), controlled for age and gender. Only non-blank cells were significant at p<.01 or p<.001:**

| Feature | O | C | E | A | N |
|---|---|---|---|---|---|
| **Image Type** | | | | | |
| Is Not Face | **+.061** | **−.121** | **−.108** | **−.070** | **+.071** |
| One Face | **−.016** | **+.102** | **+.081** | **+.046** | **−.057** |
| Multiple Faces | **−.102** | +.043 | **+.058** | +.053 | −.032 |
| No. Faces | **−.092** | **+.106** | **+.103** | **+.078** | **−.067** |
| Default Image | — | −.043 | +.015 | — | −.023 |
| **Colour** | | | | | |
| Grayscale | **+.050** | −.031 | −.012 | — | +.014 |
| Red | — | −.041 | — | — | — |
| Green | +.012 | +.021 | — | +.011 | — |
| Blue | — | — | — | −.022 | +.045 |
| Average RGB | +.015 | +.025 | **+.033** | +.019 | — |
| Brightness | +.015 | **+.028** | +.012 | +.023 | — |
| Contrast | **+.016** | +.019 | — | −.011 | — |
| Saturation | **+.015** | +.017 | −.016 | +.014 | — |
| Colourfulness | −.017 | +.013 | **+.040** | **+.029** | **−.036** |
| Naturalness | −.015 | +.013 | — | **−.036** | +.011 |
| Sharpness | **+.025** | −.022 | **+.015** | −.021 | +.014 |
| Blur | −.011 | **+.036** | — | **+.023** | — |
| Avg Colour Emotions | −.021 | +.021 | — | **+.021** | −.017 |
| **Composition** | | | | | |
| Avg Rule of Thirds | **−.033** | **−.021** | **+.032** | **+.033** | **−.034** |
| Edge Distribution | **+.047** | — | — | **−.048** | **+.038** |
| Hue Count | **−.028** | — | — | — | — |
| Visual Weight | +.010 | — | — | — | −.014 |
| Static Lines | +.017 | — | **+.018** | — | — |
| Dynamic Lines | **−.020** | +.016 | — | **+.033** | — |
| **Facial Presentation** | | | | | |
| No Glasses | — | **+.085** | **+.026** | +.027 | **−.065** |
| Reading Glasses | **+.054** | **−.099** | **−.017** | +.020 | **+.071** |
| Sunglasses | −.020 | −.017 | −.028 | −.019 | — |
| Face Ratio | **+.038** | **−.039** | **−.097** | **−.039** | **+.057** |
| **Facial Expressions** | | | | | |
| Smiling | **−.089** | **+.190** | **+.050** | **+.148** | **−.104** |
| Joy | **−.093** | **+.180** | **+.061** | **+.140** | **−.107** |
| Positive Mood | **−.093** | **+.175** | **+.065** | **+.137** | **−.107** |
| Valence | **−.075** | **+.140** | **+.053** | **+.105** | **−.090** |
| Expressiveness | **−.072** | **+.140** | **+.054** | **+.106** | **−.089** |
| Neutral | **+.068** | **−.128** | **−.047** | **−.093** | **+.081** |
| Negative Mood | **+.043** | **−.079** | **−.029** | **−.067** | **+.044** |
| Anger | **+.037** | **−.080** | **−.042** | **−.055** | **+.056** |
| Sadness | +.023 | **−.051** | −.034 | — | **+.026** |
| Surprise | −.064 | — | −.041 | −.031 | — |
| Attention | **−.047** | **+.049** | +.018 | **+.040** | **−.048** |
| **Image Demographics** | | | | | |
| Estimated Age | — | **+.050** | **−.105** | — | **−.036** |
| Asian | **−.150** | **−.072** | — | −.042 | — |
| Black | **+.047** | **+.050** | **+.085** | **−.055** | **−.096** |
| White | **+.169** | **+.031** | **−.066** | **+.026** | **+.071** |

**Prediction performance (Elastic Net, 10-fold CV, Pearson r; outcomes residualised on age and gender):**

*TwitterText (n=66,502, text-inferred labels):*

| Feature set | # feat | O | C | E | A | N |
|---|---|---|---|---|---|---|
| Colours | 44 | .071 | .060 | .089 | .057 | .045 |
| Image Composition | 10 | .053 | .031 | .084 | .051 | .039 |
| **Image Type** | **5** | **.112** | **.122** | **.117** | **.082** | **.078** |
| Demographics | 5 | .065 | .086 | .066 | .044 | .065 |
| Facial Presentation | 7 | .046 | .034 | .099 | .037 | .064 |
| Facial Expressions | 14 | .068 | **.114** | .045 | **.090** | .072 |
| **All** | **85** | **.162** | **.189** | **.180** | **.150** | **.145** |

*TwitterSurvey (n=429, real questionnaires); values in brackets are **not** significant:*

| Feature set | O | C | E | A | N |
|---|---|---|---|---|---|
| Colours | (.0) | (.0) | (.0) | (.002) | .122 |
| Image Composition | (.03) | (.026) | (.0) | (.0) | (.043) |
| Image Type | (.0) | (.086) | (.0) | (.030) | (.0) |
| Demographics | (.011) | (.091) | (.0) | (.037) | .128 |
| Facial Presentation | .147 | (.042) | (.040) | (.0) | .033 |
| Facial Expressions | .139 | .125 | (.041) | (.0) | .101 |
| **All** | **.190** | **.134** | **.095** | **(.046)** | **.151** |

- **⚠️ The authors' own caveat is the most important sentence in the paper:** *"The same set of experiments on personality correlations on the TwitterSurvey dataset unveiled a total of only 3 significant correlations at p<.01 and none at p<.001. Given that these were obtained from a total of 260 tests, we cannot consider any of these correlations as being robust to randomness."*
- **Author-stated ceiling:** *"psychological variables typically have a 'correlational upper-bound' around .3 − .4 correlation."* Their own single-profile-image result is r = .145–.189.
- **Qualitative summary:** Users high in **Openness** or **Neuroticism** post fewer photos of people, and when present these do not express positive emotions; they differ in aesthetic quality (high for O, low for N). Users high in **Conscientiousness**, **Agreeableness** or **Extraversion** prefer pictures with at least one face and present positive emotions. Conscientious users post the most normative profile picture: one face, most positive emotion of all five traits. Extraverts and agreeable users post colourful, emotive but not aesthetically pleasing pictures.

### 4.2 Guntuku, Lin, Carpenter, Ng, Ungar & Preoţiuc-Pietro (2017) — posted vs. liked images

> Guntuku, S. C., Lin, W., Carpenter, J., Ng, W. K., Ungar, L. H., & Preoţiuc-Pietro, D. (2017). *Studying Personality through the Content of Posted and Liked Images on Twitter.* **WebSci '17**, pp. 223–227. ACM. https://doi.org/10.1145/3091478.3091522

- **D1:** 436 Twitter users with **NEO-PI-R survey** scores; 579,929 tweets → 34,875 embedded photos across 232 users; **161 users** had ≥10 photos and were analysed.
- **D2:** **4,132** Twitter users, personality **text-inferred** (Schwartz et al. 2013, validation r ≈ .35). 5,547,510 tweets → **700,630 image-bearing tweets across 3,498 users**; plus 3,135,764 liked tweets → **909,861 containing an image**. Filtered to users with ≥20 posted and ≥10 liked images. Text of image-bearing tweets excluded from label generation to reduce confounding. **~1.5M images total.**
- **Features:** Colours (33) — HSV, grayscale filter, saturation, brightness, PAD, hue count, HSV SDs, 6-bin and 12-bin hue histograms, warm-pixel ratio. Content — Imagga auto-tagging → 1,299 distinct tags (≥200 occurrences) → NPMI similarity matrix → **spectral clustering into 400 tag clusters**; plus VGG-19 1,000 ImageNet class probabilities. Mean feature pooling per user.
- **Analysis:** partial correlation controlling for **age, gender, and all four other traits**; Simes multiple-test correction.

**Colour/meta correlations (D2, n≈3,500), p<.01:**

*Posted images:*

| Feature | O | C | E | A | N |
|---|---|---|---|---|---|
| Grayscale | +.039 | **−.130** | **−.128** | **−.152** | **+.262** |
| Brightness | **−.108** | +.040 | **+.124** | +.027 | −.020 |
| Saturation | −.017 | +.023 | **+.102** | +.076 | −.077 |
| Pleasure | −.017 | +.032 | −.079 | +.037 | −.024 |
| Arousal | −.007 | +.005 | **+.119** | +.048 | −.054 |
| Dominance | +.005 | −.013 | **+.113** | +.010 | −.021 |
| Hue Count | **−.094** | +.040 | **+.118** | +.085 | **−.103** |
| % posts with people | **−.106** | **+.109** | **+.116** | +.082 | −.059 |
| # posted images | +.068 | −.025 | +.094 | **−.141** | +.093 |

*Liked images:*

| Feature | O | C | E | A | N |
|---|---|---|---|---|---|
| Brightness | −.081 | +.068 | +.070 | +.087 | −.093 |
| Saturation | +.049 | **+.159** | +.062 | **+.122** | **−.142** |
| Pleasure | −.022 | −.034 | −.029 | +.018 | +.042 |
| Arousal | +.052 | **+.150** | +.065 | +.096 | **−.139** |
| Dominance | +.043 | **+.110** | +.055 | +.049 | **−.107** |
| Hue Count | −.071 | +.030 | +.040 | +.066 | −.092 |
| % posts with people | **−.116** | −.054 | **+.117** | −.041 | +.023 |
| # liked images | −.049 | **−.131** | +.009 | −.068 | **+.159** |

**Content tag-cluster correlations (D2), all p<.01 Simes-corrected, controlled for age, gender and the other four traits. r-post / r-like:**

| Trait | Positive clusters (top, r-post) | Negative clusters (top, r-post) |
|---|---|---|
| **Openness** | senior/old/elderly/grandma (.155); **art, cartoon, clipart (.148 / .112)**; drawing, representation, diagram (.137 / .097); ancient, palace, castle, historic (.120); decoration, sketch, tattoo, graffiti (.119); office, businessman, professional (.108); artwork (.102 / .101) | **ball, sports_equipment, basketball (.207 / .135)**; player, athlete, baseball (.195 / .138); football, helmet (.154 / .109); game, puzzle (.119 / .090); clothing, garment, shirt (.117); tennis, racket (.109); runner, track (.105); child, boy, kid, baby (.099 / .078) |
| **Conscientiousness** | classroom (.153 / .076); office, businessman, professional (.132 / .069); building, architecture, city (.114); structure, fountain (.104); business (.101); paper, document, writing, book (.099 / .059); furniture, table (.094); home, room, house, interior (.078 / .062) | face, pretty, hair, model, fashion, sexy (.125 / .049); art, cartoon, clipart (.111 / .086); drawing (.105 / .065); expression, looking, beard, head (.101 / .084); cute, eyes (.101); artwork (.097 / .100); computer, equipment, technology (.072); people, person, adult, happy, portrait, smile (.068) |
| **Extraversion** | **people, person, adult, man, happy, portrait, smile (.321 / .128)**; face, pretty, hair, model, fashion (.243 / .089); women, group, friends, girls, friendship (.182); lifestyle (.175 / .080); happiness, couple, together, love, fun, family (.171 / .075); disco, cabaret, ballroom (.136 / .093); body, swimsuit, bikini (.127); expression, beard, head (.120) | **art, cartoon, clipart (.253 / .164)**; drawing, representation, diagram (.213 / .122); design, sign, icon, graphic, symbol, web (.165); casual, silhouette, sport, laptop (.149); black, african, picture, dark (.128 / .066); artwork (.127 / .103); text, 3d (.125); color, motion, futuristic (.094) |
| **Agreeableness** | happiness, couple, together, love, fun, family (.144 / .090); performance, concert, stage, musician (.108 / .080); flower, floral, garden, petal, blossom (.098 / .075); **cat, feline, pet, kitten, kitty (.094)**; trees, season (.094); women, group, friends (.093); decoration, sketch, tattoo (.089); music, guitar (.081 / .081) | **office, businessman, professional, corporate, suit (.211 / .096)**; press, print_media (.177 / .076); business (.132 / .077); newspaper, money, currency, finance, cash, bank (.129); work, success, manager, confident (.101); signboard, billboard (.099); people, person, adult, smile (.092); publication, magazine, comic_book (.081) |
| **Neuroticism** | paper, document, writing, menu, pen, book (.107 / .057); happiness, couple, together, love, family (.104 / .071); cute, eyes (.104); face, pretty, hair, model, fashion (.099 / .082); **animal, dog, domestic_animal, canine (.092)**; cat, feline, pet, kitten (.082 / .058); people, person, adult, smile (.079 / .061); retriever, golden_retriever, labrador (.060 / .062) | casual, silhouette, sport, laptop, businessperson (.108); computer, equipment, technology, display, screen (.096); device, machine, slot_machine, vending (.094); design, sign, icon, graphic, web (.064); art, cartoon, clipart (.063); communication, telephone, phone, mobile (.060); space, digital, fractal, laser, glow (.057) |

**Prediction (Elastic Net, 10-fold CV, Pearson r):**

*D1 — n=161, **real NEO-PI-R survey labels** (the honest numbers):*

| Feature set | # feat | O | C | E | A | N |
|---|---|---|---|---|---|---|
| Colours | 33 | .093 | .147 | .022 | .229 | .085 |
| Imagga Clusters | 400 | .044 | .077 | .183 | .085 | **.404** |
| VGG-net Classes | 1000 | .056 | .051 | .061 | .037 | .222 |
| Text | 100 | .168 | .059 | .223 | .111 | .261 |
| **All (Image)** | 3 | .081 | .177 | .187 | .229 | **.416** |
| **All (Image+Text)** | 2 | .171 | .178 | .223 | .230 | **.418** |

*D2 — n≈3,500, **text-inferred labels** (inflated; these predict a text model, not a person):*

| Feature set | O | C | E | A | N |
|---|---|---|---|---|---|
| Colours (posted) | .284 | .352 | .293 | .317 | .398 |
| Imagga (posted) | .275 | .364 | .317 | .221 | .383 |
| VGG-net (posted) | .410 | .383 | .319 | .198 | .398 |
| All image (posted) | .448 | .479 | .369 | .336 | .503 |
| Colours (liked) | .351 | .383 | .229 | .286 | .396 |
| Imagga (liked) | .411 | .492 | .345 | .335 | .412 |
| VGG-net (liked) | .302 | .388 | .193 | .008 | .374 |
| All image (liked) | .468 | .530 | .366 | .378 | .467 |
| **Posts + Likes fused** | **.543** | **.566** | **.440** | **.433** | **.530** |

- Fusing posted + liked images gives **+6% (C) to +10–15% (other traits)** over either alone.
- On D1 the authors note the correlation analyses *"are not robust to randomness due to the small sample size"* — the same admission as Liu et al.

### 4.3 Riahi Samani, Guntuku, Moghaddam, Preoţiuc-Pietro & Ungar (2018) — cross-platform, cross-interaction

> Samani, Z. R., Guntuku, S. C., Moghaddam, M. E., Preoţiuc-Pietro, D., & Ungar, L. H. (2018). *Cross-platform and cross-interaction study of user personality based on images on Twitter and Flickr.* **PLOS ONE, 13**(7), e0198660. https://doi.org/10.1371/journal.pone.0198660

- **Two datasets:** PsychoFlickr (300 users, **self-assessed BFI**, profile + posted + liked images); and a novel **cross-linked Flickr–Twitter set of 334 users** with personality **text-inferred**. Flickr: 60,381 posts (mean 175/user), 28,658 likes (mean 83), 344 profile images. Twitter: 73,576 posts (mean 213), 29,030 likes (mean 84), 344 profile images.
- **Features (6,782 dims):** Colour (32) — grayscale flag; 10 HSV statistics (H/S/V mean and SD, distinct hue count, log hue count); 12-bin normalised hue histogram; Pleasure/Arousal/Dominance; 6-bin hue histogram (yellow, green, cyan, blue, magenta, red). Content — **VGG-Net predictions on 1,000 ImageNet objects + 365 Places scene categories (1,365 dims)**; **VGG-Net penultimate-layer 4,096-d generic features**; **1,299 Imagga tags**.
- **Model:** linear regression with Elastic Net; 10-fold CV, Pearson r; feature/modality/platform combination by linear ensemble; results averaged over 100 randomised splits (SD < 0.001).

**Findings (results are presented as figures; qualitative statements are the authors'):**
- **Modality ranking:** posted images > liked images ≳ profile images overall. Profile images do best for **Conscientiousness**, worst for Agreeableness. Posted images do best for **Agreeableness, Openness and Neuroticism**. Liked images never significantly beat the others, but match posted images for Neuroticism.
- **Feature ranking:** for **profile images**, CNN object/scene probabilities win for O, C, E, N; penultimate CNN features win for A. For **posted and liked images**, Imagga tags and penultimate CNN features win — object/scene probabilities lag because ImageNet's taxonomy lacks faces and common social-media objects. Colour features consistently trail semantic features. Combining features helps for profile and posted images but **not** for liked images ("all feature types capture similar information").
- **Platform:** Flickr more predictive of **O and C**; Twitter more predictive of **E**; similar for A and N. Combining modalities always improves, especially on Flickr (Flickr posting and liking are more disparate acts than on Twitter). Combining platforms improves slightly, **except for Extraversion**.
- **Overall trait ranking:** *"conscientiousness and openness to experience are the most predictable personality traits from images posted online. Extraversion is the least predictable."* — note this **contradicts** Segalin et al. (2017), who found Extraversion the *best*-predicted trait on the very same PsychoFlickr corpus (for attributed traits).
- **Limitations stated:** could not provide deeper interpretability due to data size; recommends larger survey-labelled samples; flags ethical exposure ("few users realize the amount of psycho demographic information that can be gleaned from their digital traces").

### 4.4 Segalin, Celli, Polonio, Kosinski, Stillwell, Sebe, Cristani & Lepri (2017) — 11,736 Facebook profile pictures

> Segalin, C., Celli, F., Polonio, L., Kosinski, M., Stillwell, D., Sebe, N., Cristani, M., & Lepri, B. (2017). *What your Facebook Profile Picture Reveals about your Personality.* **ACM Multimedia '17**, pp. 460–468. https://doi.org/10.1145/3123266.3123331. arXiv:1708.01292

- **Sample: 11,736 Facebook profile pictures, one per user**, from the **myPersonality** corpus, with **self-assessed** Big Five scores. This is by far the largest survey-labelled single-image study.
- **Four feature families (5,418 dims total):** **CA** — 82 Computational Aesthetics features (the Segalin/PsychoFlickr set: colour, composition, texture, number of faces); **PHOW** — 960-d Pyramid Histogram of Visual Words (colour SIFT, 3 scales, 4×4 sectors, 20-word vocabulary); **CNN** — 4,096-d; **IATO** — 280 Image Analysis Tool features (JPEG Huffman/quantisation table statistics).

**Mean |ρ| of the *statistically significant* correlations, and count (%) of significant features, per family (Bonferroni-corrected):**

| Family (dim) | Split | O | C | E | A | N |
|---|---|---|---|---|---|---|
| CA (82) | mean | 0.0168 (61, 74%) | 0.0172 (50, 61%) | 0.0174 (59, 72%) | 0.0131 (39, 47%) | 0.0163 (69, 84%) |
| CA (82) | Q1,3 | 0.0214 (57, 70%) | 0.0191 (60, 73%) | **0.0289** (62, 76%) | 0.0196 (55, 67%) | 0.0225 (65, 79%) |
| PHOW (960) | Q1,3 | 0.0204 | 0.0179 | 0.0210 | 0.0187 | 0.0184 |
| CNN (4096) | Q1,3 | 0.0154 | 0.0155 | 0.0166 | 0.0152 | 0.0152 |
| IATO (280) | Q1,3 | 0.0163 | 0.0151 | 0.0227 | 0.0167 | 0.0190 |

**⚠️ Read those numbers carefully: the mean significant correlation is ρ ≈ 0.02.** With n≈11,700, ρ = 0.02 is "significant" and utterly meaningless. The authors say so: *"the absolute value of the correlations is low, meaning that more can be done."*

**Best individual CA feature correlations (Spearman ρ, extreme-quartile subsample; * = p<.01, unstarred = p<.05):**

| Category | Feature | O | C | E | A | N |
|---|---|---|---|---|---|---|
| Colour | valence | | | +0.04* | +0.03 | |
| Colour | colourfulness | | | −0.04* | | +0.02 |
| Colour | brown | −0.03* | +0.03 | | | |
| Colour | pink | −0.04* | | **+0.08\*** | +0.03 | |
| Colour | purple | −0.03* | | **+0.07\*** | | |
| Colour | red | −0.03* | +0.02 | **+0.09\*** | | |
| Colour | yellow | −0.02 | −0.03 | +0.04* | | |
| Composition | % edge pixels | | | +0.03* | +0.03 | |
| Composition | level of detail | | | **+0.07\*** | +0.03 | −0.02 |
| Composition | avg region size | | | **−0.07\*** | −0.03 | +0.02 |
| Composition | rule of thirds — saturation | | | +0.04* | +0.02 | |
| Texture | gray distribution entropy | | | +0.03 | +0.03 | |
| Texture | brightness wavelet avg | | | +0.04* | | −0.03 |
| Texture | Tamura directionality | | | −0.03 | −0.02 | |
| Texture | GLCM energy — saturation | | | −0.06* | | +0.03* |
| Texture | GLCM contrast — brightness | | | +0.04* | | −0.03 |
| **Faces** | **number of faces** | **−0.08\*** | **+0.04\*** | **+0.07\*** | **+0.03\*** | |

**Classification (logistic regression, correlation-based feature selection, balanced classes ~7,000 images/trait, 75/25 hold-out × 10):**

| Trait | Mean split — Acc | Mean split — F1 | Quartile split — Acc | Quartile split — F1 |
|---|---|---|---|---|
| Openness | 0.55 | 0.56 | 0.60 | 0.60 |
| Conscientiousness | 0.55 | 0.57 | 0.60 | 0.60 |
| **Extraversion** | **0.56** | 0.56 | **0.62** | **0.62** |
| Agreeableness | 0.55 | 0.55 | 0.60 | 0.60 |
| Neuroticism | 0.55 | 0.55 | 0.60 | 0.60 |

**Accuracy by feature family (quartile split):** CNN alone 0.59–0.61 (best single family); CA 0.52–0.55; IATO 0.53–0.55; PHOW 0.54 flat. Best combination CA+CNN+IATO: 0.60–0.62. **Combining all four families adds nothing over CNN+IATO.**

**Human vs. machine (150 users at the trait extremes, 23 human raters):** Krippendorff's α among raters = 0.34 (E), 0.26 (N).

| Trait | Human Acc | Human F1 | Machine Acc | Machine F1 |
|---|---|---|---|---|
| Extraversion | 0.60 | 0.57 | **0.68** | **0.72** |
| Neuroticism | 0.58 | 0.60 | **0.69** | **0.67** |

- **Author-stated directions:** *Extraverts* — many faces, faces near but not exactly at centre (rule of thirds), warm colours (red/pink/purple/yellow), few large sharp saturated regions, low colourfulness. *Introverts* — smooth, dull-coloured images, alone or a drawing standing in for themselves. *Neurotic* — many colours (high colourfulness), large regions, GLCM texture; *emotionally stable* — sharp details, natural scenes. *Agreeable* — lots of faces, warm colour, rule of thirds observed; *disagreeable* — large homogeneous regions, portrayed alone, poorly-exposed/blown-out pictures. *Conscientious* — many faces. *Open* — alone, few faces.
- **Limitations stated:** one profile picture per user only; a single general model across a highly heterogeneous set of subjects (symbols, animals, no faces).

### 4.5 Celli, Bruni & Lepri (2014) — the first profile-picture study

> Celli, F., Bruni, E., & Lepri, B. (2014). *Automatic personality and interaction style recognition from Facebook profile pictures.* **ACM Multimedia '14**, pp. 1101–1104. https://doi.org/10.1145/2647868.2654977

- **Sample:** 100–112 Facebook users, self-assessed BFI-10 personality + interaction style. Features: **bag-of-visual-words over dense SIFT**; multiple ML algorithms combined.
- **Result: ~65% binary accuracy; average F1 ≈ 67%.** Post-hoc clustering of correctly classified images showed *extraverted and emotionally stable people tend to have pictures in which they are smiling or appear with other people*.
- Interaction-style prediction was also attempted. **⚠️ n≈100 with BOVW features; no interpretability; the effect is at the noise floor for this sample size.**

### 4.6 Al Moubayed, Vazquez-Alvarez, McKay & Vinciarelli (2014) — eigenfaces

> Al Moubayed, N., Vazquez-Alvarez, Y., McKay, A., & Vinciarelli, A. (2014). *Face-based automatic personality perception.* **ACM Multimedia '14**, pp. 1153–1156.

- **829 individuals** from the FERET corpus, personality **attributed by 11 independent judges** (perception, not self-report). Features: first **103 eigenfaces**. **~70% accuracy** classifying above/below median. Being an APP task on standardised portraits, this is not comparable to social-media APR results.

### 4.7 Guntuku, Qiu, Roy, Lin & Jakhetiya (2015) — selfies

> Guntuku, S. C., Qiu, L., Roy, S., Lin, W., & Jakhetiya, V. (2015). *Do Others Perceive You As You Want Them To? Modeling Personality Based on Selfies.* **ASM '15** (1st Int'l Workshop on Affect & Sentiment in Multimedia, ACM MM), pp. 21–26. https://doi.org/10.1145/2813524.2813528

- **123 Sina Weibo users**, both **self-assessed and perceived** personality. Selfies annotated with **mid-level cues** relevant to portraits — presence of duckface, whether the user is alone, emotional positivity, etc.
- **Low-level features:** colour histograms, SIFT, LBP → SVM with RBF kernel to detect the mid-level descriptors → personality regression on the mid-level layer.
- **Finding:** **mid-level cue detectors outperform state-of-the-art low-level features for most traits.** The interpretable intermediate representation is the contribution, not the raw accuracy (n=123).
- Companion: Qiu, L., Lu, J., Yang, S., Qu, W., & Zhu, T. (2015). *What does your selfie say about you?* **Computers in Human Behavior, 52**, 443–449.

### 4.8 Skowron, Tkalcic, Ferwerda & Schedl (2016) — Twitter + Instagram fusion

> Skowron, M., Tkalcic, M., Ferwerda, B., & Schedl, M. (2016). *Fusing Social Media Cues: Personality Prediction from Twitter and Instagram.* **WWW '16 Companion**, pp. 107–108. ACM. https://doi.org/10.1145/2872518.2889368

- **Sample: only 62 users** — recruited on MTurk (US, native English, high reputation), BFI-44, active on **both** Instagram and Twitter, filtered to ≥30 Instagram images **and** ≥30 tweets.
- **Features:** Instagram images — PAD, brightness, saturation, hue, faces, full bodies (following Machajdik & Hanbury 2010). Text — LIWC, ANEW, dialog acts, sentiment classifiers over tweets and image captions. Meta — followers, followees, Klout, adapted TIME influence score. Each feature summarised as mean, SD, min, max, median; F-statistic subsampling; **random forest regression** with variable-importance feature reduction; 5 × 10-fold CV.

**RMSE by feature set (T = Twitter, I = Instagram; subscripts l = linguistic, i = image, m = meta):**

| Config | O | C | E | A | N | AVG |
|---|---|---|---|---|---|---|
| Tm | 0.74 | 0.78 | 1.16 | 0.71 | 1.07 | 0.89 |
| **Ii (Instagram images only)** | **0.80** | **0.70** | **0.98** | **0.74** | **0.90** | **0.83** |
| Tlm | 0.75 | 0.73 | 0.92 | 0.71 | 0.80 | 0.78 |
| TmIi | 0.62 | 0.66 | 0.92 | 0.69 | 0.92 | 0.77 |
| Il | 0.62 | 0.66 | 0.92 | 0.69 | 0.92 | 0.76 |
| Tl | 0.73 | 0.66 | 0.96 | 0.63 | 0.75 | 0.75 |
| TmIl | 0.65 | 0.68 | 0.86 | 0.60 | 0.79 | 0.72 |
| TlIl | 0.61 | 0.68 | 0.86 | 0.63 | 0.76 | 0.71 |
| TmIli | **0.51** | 0.68 | 0.86 | 0.55 | 0.88 | 0.70 |
| TlIli | 0.64 | **0.65** | 0.87 | 0.55 | 0.73 | 0.69 |
| **TlmIli (all)** | 0.53 | 0.67 | **0.71** | 0.56 | 0.83 | **0.66** |

Best per trait: **O 0.51** (TmIli), **C 0.65** (TlIli), **E 0.71** (TlmIli), **A 0.55** (TmIli/TlIli), **N 0.73** (TlIli).

**Comparison table given in the paper (baselines from the original papers, different data — not directly comparable):**

| | RMSE Quercia (Twitter) | RMSE TlmIli | MAE Golbeck | MAE TlmIli | PCC Kosinski (FB Likes) | PCC TlmIli |
|---|---|---|---|---|---|---|
| O | 0.69 | 0.51 | 0.12 | 0.11 | **0.43** | 0.74 |
| C | 0.76 | 0.67 | 0.14 | 0.11 | **0.29** | 0.76 |
| E | 0.88 | 0.71 | 0.16 | 0.17 | **0.40** | 0.65 |
| A | 0.79 | 0.50 | 0.12 | 0.12 | **0.30** | 0.34 |
| N | 0.85 | 0.73 | 0.19 | 0.16 | **0.30** | 0.71 |
| AVG | 0.79 | 0.73 | 0.15 | 0.13 | 0.30 | 0.64 |

- **⚠️ The PCC column of 0.64–0.76 at n=62 with heavy per-trait feature selection is almost certainly optimistically biased.** The authors themselves label these "preliminary results" and note the systems "are not directly comparable". This paper is widely cited for the claim that multi-platform fusion helps; the claim is directionally plausible and the effect sizes are not trustworthy.

### 4.9 Cucurull, Rodríguez, Yazici, Gonfaus, Roca & González (2018) — image + word fusion

> Cucurull, G., Rodríguez, P., Yazici, V. O., Gonfaus, J. M., Roca, F. X., & González, J. (2018). *Deep Inference of Personality Traits by Integrating Image and Word Use in Social Networks.* arXiv:1802.06757.

- "MindPics": trains a CNN on images posted alongside words known from the psycholinguistic literature to be trait-diagnostic. Useful mainly for its comparative table of binary classification accuracies (%) in the literature:

| Trait | Golbeck (text) | Iacobelli (text) | **Segalin (images)** | **Guntuku (images)** |
|---|---|---|---|---|
| O | 75.50 | 84.36 | 61.00 | 66.10 |
| C | 61.70 | 79.18 | 67.00 | 70.50 |
| E | 58.60 | 71.68 | 65.00 | 69.70 |
| A | 69.70 | 78.31 | 64.00 | 72.30 |
| N | 42.80 | 70.51 | 69.00 | 61.50 |
| **Avg** | 61.66 | 76.80 | **65.20** | **68.02** |

---

## 5. Boundary studies: the non-image benchmarks that bound image claims

### 5.1 Kosinski, Stillwell & Graepel (2013)

> Kosinski, M., Stillwell, D., & Graepel, T. (2013). *Private traits and attributes are predictable from digital records of human behavior.* **PNAS, 110**(15), 5802–5805. https://doi.org/10.1073/pnas.1218772110

- **58,466 US volunteers** (myPersonality). Mean 170 Facebook Likes/user (median 68, IQR 152). SVD dimensionality reduction (k=100) → logistic/linear regression, 10-fold CV.
- **Big Five prediction (Pearson r, all p<.001):** **Openness 0.43**, **Extraversion 0.40**, **Intelligence 0.39**; the remaining traits (Conscientiousness, Agreeableness, Emotional Stability) and Satisfaction With Life fell in **r = 0.17–0.30** (commonly cited values: C ≈ 0.29, A ≈ 0.30, Emotional Stability ≈ 0.30; SWL = 0.17).
- Non-personality anchors: age r = 0.75; friendship-network density r = 0.52; network size r = 0.47. Dichotomous AUCs: gender 0.93, ethnicity 0.95, male sexual orientation 0.88, female 0.75, political views 0.85, religion 0.82, substance use 0.65–0.73, parental separation 0.60.
- **The key contrast:** the *same* pipeline that hits AUC 0.93–0.95 on gender/ethnicity only reaches r = 0.17–0.43 on personality. **Personality is intrinsically harder to infer than demographics — this is a property of the construct, not of the model.**

### 5.2 Youyou, Kosinski & Stillwell (2015)

> Youyou, W., Kosinski, M., & Stillwell, D. (2015). *Computer-based personality judgments are more accurate than those made by humans.* **PNAS, 112**(4), 1036–1040. https://doi.org/10.1073/pnas.1418680112

- **86,220 volunteers** completed a 100-item IPIP questionnaire; LASSO regression on Facebook Likes, 10-fold CV, models trained on users with ≥20 Likes.
- **Computer accuracy (disattenuated self-other agreement, averaged across Big Five): r = 0.56** at the average user's 227 Likes. **Average single human judge: r = 0.49** (Connelly & Ones meta-analysis: 0.48). **Peak computer performance r = 0.66** for users with >500 Likes.
- Computers need **10 Likes** to beat a work colleague, **70** a cohabitant or friend, **150** a family member, **300** a spouse (spouse r = 0.58; computer vs. spouse z = −1.68, p = .09, i.e. not significantly different).
- Computer/human consensus r = 0.37, but **partial** correlation between computer and human judgments (controlling for self-ratings) is only **r = 0.07** — they capture largely distinct components. Self-rating partial with computer r = 0.38; with human r = 0.42. Inter-judge agreement: computer models r = 0.62 vs. human judges r = 0.38.
- **Openness is the best-predicted trait**, which the authors attribute to it being "largely expressed through individuals' interests, preferences, and values" — highly observable in a digital environment despite being hard for humans to judge.
- **⚠️ Likes are not images.** The r = 0.56 headline is routinely mis-cited as evidence for image-based prediction. It is the ceiling for *aggregated explicit preference declarations across hundreds of items*, which is a far richer signal than a photo stream.

### 5.3 Osterholz, Mosel & Egloff (2023) — the human ceiling on Instagram specifically

> Osterholz, S., Mosel, E. I., & Egloff, B. (2023). *#Insta personality: Personality expression in Instagram accounts, impression formation, and accuracy of personality judgments at zero acquaintance.* **Journal of Personality, 91**(3). https://doi.org/10.1111/jopy.12756

- **102 Instagram users** with self- **and** informant reports of Big Five, self-esteem and narcissism. **100 unacquainted observers** judged from Instagram profile screenshots (up to 102 latest posts). Instagram cues objectively counted and rated by trained independent coders (Brunswik lens design: cue validity × cue utilisation).
- **Averaged-observer accuracy correlations against self-informant composites: r = .44 (extraversion, p<.001) down to r = .25 (conscientiousness, p=.013).** Extraversion and Openness were the easiest to judge. Emotional stability was judged more accurately than in prior social-media studies.
- **Cue findings:** users posting many appearance-focused self-images were perceived as more extraverted, self-confident, narcissistic and less agreeable. Users high in Openness created more aesthetic, professional-looking profiles and were judged higher in openness, conscientiousness, self-esteem and narcissism.
- **⚠️ This is the practical human benchmark for a full Instagram account: r ≈ .25–.44.** No published image-only algorithm has beaten it against survey ground truth.

---

## 6. The LLM / VLM era (2022–2026)

### 6.1 Gan, Sowmya & Mohammadi (2022) — PsyCLIP, zero-shot from faces

> Gan, P. Z., Sowmya, A., & Mohammadi, G. (2022). *Zero-shot Personality Perception From Facial Images.* In **AI 2022: Advances in Artificial Intelligence**, LNAI 13728, Springer, ch. 4. https://doi.org/10.1007/978-3-031-22695-3_4

- New dataset of **41,800 facial images** labelled with **perceived MBTI** types. **PsyCLIP** exploits CLIP's latent psychometric layer for zero-shot personality *perception*, reported as the first zero-shot model competitive with supervised baselines. Statistically significant (p<.01) prediction of all perceived MBTI dimensions.
- **⚠️ Perceived MBTI, not self-reported Big Five.** MBTI has no accepted construct validity, and "perceived" restores the same causal shortcut that inflates APP results everywhere in this literature.

### 6.2 Gan, Sowmya & Mohammadi (2023) — CLIP for apparent personality

> Gan, P. Z., Sowmya, A., & Mohammadi, G. (2023). *CLIP-based Model for Effective and Explainable Apparent Personality Perception.* **MRAC '23** (1st Int'l Workshop on Multimodal and Responsible Affective Computing, ACM MM). https://doi.org/10.1145/3607865.3613178

- Evaluated on **ChaLearn First Impressions V2 (CVPR'17)**. Matches or beats multimodal SOTA **using only visual data**, with natural-language-supervised, interpretable explanations. The ChaLearn benchmark's SOTA sits around **0.90–0.92 "accuracy"** (1 − MAE on [0,1] apparent-trait scores) — but that metric on crowd-averaged first impressions of 15-second videos is **not comparable to any correlation against self-report**, and the field's near-ceiling numbers there reflect the low variance of averaged first-impression labels, not personality inference.

### 6.3 Chen, Zhu, Zhao, Shi, Zhang & Lei (2026) — GlanceFace, VLM from faces

> Chen, S., Zhu, X., Zhao, W., Shi, H., Zhang, X.-Y., & Lei, Z. (2026). *Knowing You at First Glance: Inferring Apparent Personality from Faces.* arXiv:2607.14631.

- **Data:** MS1MV3, CelebA, VGGFace2, IMDB-Face images cross-referenced with MBTI annotations from Personality Database. **3,092 identities / 568,675 training images; 216 identities / 39,788 evaluation images.**
- **Method:** Qwen3-VL-Embedding-2B backbone, Semantic-Enhanced Facial Representation (differential gated attention), Uncertainty-Aware Personality Learning.
- **Results, 16-type MBTI (person level):** Top-1 **26.39%**, Top-3 56.48%, Top-5 75.00%, F1 **17.99%**, AUC 78.19%.
- **Four MBTI dimensions (person level average):** Accuracy **71.41%**, F1 73.18%, AUC 74.19%. Per dimension: **I-E 62.96%**, S-N 76.85%, F-T 72.69%, J-P 73.15%.
- **Authors' own caveat:** predicted traits are *perceived impressions, not intrinsic personality*; explicitly caution against high-stakes use; flag demographic bias and profiling risk.
- **Reference point:** the highest-capacity VLM approach yet published, on half a million faces, gets **26% top-1 on 16-way MBTI**, i.e. only ~4× a 6.25% random baseline — from crowd-attributed labels.

### 6.4 Peters & Matz (2024) — LLM zero-shot from text (the text analogue)

> Peters, H., & Matz, S. C. (2024). *Large language models can infer psychological dispositions of social media users.* **PNAS Nexus, 3**(6), pgae231. https://doi.org/10.1093/pnasnexus/pgae231. arXiv:2309.08631.

- GPT-3.5 Turbo and GPT-4 zero-shot on Facebook status updates. **Average r = .29 with self-reported Big Five (range .22–.33)** — on par with supervised models trained for the task. Accuracy was heterogeneous across demographics: better for women and younger users on several traits.

### 6.5 Marengo, Montag & Settanni (2025) — LLM reliability and validity

> Marengo, D., Montag, C., & Settanni, M. (2025). *Inferring Personality From Social Media Activity Using Large Language Models: Cross-Model Agreement, Temporal Stability, and Convergent Validity With Self-Reports.* **Journal of Personality**. https://doi.org/10.1111/jopy.70019

- **1,214 Italian Facebook users**, 2 years of posts, Gemini 1.5 Pro and GPT-4o, compared against TIPI self-reports.
- **Convergent validity with self-reports, best case (aggregating across both LLMs and both time points):** **Openness 0.31, Extraversion 0.27, Agreeableness 0.24, Conscientiousness 0.23, Neuroticism 0.18.**
- **Systematic bias:** LLMs underestimate Agreeableness and Conscientiousness, overestimate Extraversion; Neuroticism and Openness align with self-report means.
- **Reliability ≠ validity:** cross-LLM agreement reached r = 0.58–0.83 and 2-year test-retest 0.44–0.60 — far higher than agreement with the *actual* person. The models agree with each other much more than they agree with reality. **This is the defining failure mode of the whole field.**

### 6.6 Other recent LLM benchmarks (text, for calibration)

- Zero-shot GPT-4o / GPT-4o-mini on user conversations (2025, arXiv:2501.07532): intermediate BFI-10 item-scoring improves over direct trait inference.
- 555 semi-structured interviews with validated BFI-10 (arXiv:2507.14355, "Can LLMs Infer Personality from Real World Conversations?"): GPT-4.1 Mini, LLaMA, DeepSeek, zero-shot and CoT — **maximum Pearson r = 0.27**, low interrater agreement.
- WASSA shared tasks 2022/2023/2024: 0.230 → 0.252 → 0.300.

---

## 7. FEATURE → TRAIT TABLE

The core deliverable. **Conventions:** ↑ = feature increases with the trait; ↓ = decreases. Values are Pearson or Spearman coefficients as reported. **Bold = replicated in ≥2 independent samples with the same sign.** ⚠️ marks a contradiction across studies. Studies keyed as: **F16** = Ferwerda MMM 2016 (Instagram, n=113, survey); **FT18** = Ferwerda & Tkalcic 2018 (Instagram, n=193, survey); **BR20** = Branz 2020 (Instagram, n=179, survey); **EB24** = El Bahy 2024 (Instagram, n=316, survey); **SEG17** = Segalin TAC 2017 (Flickr favourites, n=300, **attributed**); **SEGMM17** = Segalin ACM MM 2017 (Facebook profile pic, n=11,736, survey); **LIU16** = Liu ICWSM 2016 (Twitter profile pic, n=66,502, **text-inferred**); **GUN17** = Guntuku WebSci 2017 (Twitter posted/liked, n≈3,500, **text-inferred**).

### 7.1 Colour and pixel statistics

| Feature | Trait | Direction & values | Sources | Confidence |
|---|---|---|---|---|
| **Grayscale / desaturated / monochrome** | **Neuroticism ↑** | **r = +.262** (posted) | GUN17 | ⚠️ Contradicted by SEG17 (attributed N ↔ low saturation, ρ=−.55 for *saturation*, consistent) — actually **consistent**: N ↔ low colour |
| Grayscale | Openness ↑ | r = +.039 (n.s.); +.050 | GUN17, LIU16 | Weak, consistent sign; "artistic/black-and-white" |
| Grayscale | Conscientiousness ↓ | r = −.130; −.031 | GUN17, LIU16 | Moderate; Celli survey (2025) notes findings here are **inconsistent** |
| Grayscale | Extraversion ↓ | r = −.128 | GUN17 | Single-source |
| Grayscale | Agreeableness ↓ | r = −.152 | GUN17 | Single-source |
| **Average saturation** | **Extraversion ↑** | **+.102** (posted); attributed E via GLCM contrast-S +.21; +.017 | GUN17, SEG17, LIU16 | **Moderate** |
| Average saturation | Openness ↑ | +.16^ | F16 | ⚠️ **BR20 finds −.17** (opposite sign, both significant) |
| Average saturation | Agreeableness ↑ | +.122 (liked); attributed A **ρ=+.40** | GUN17, SEG17 | Moderate; APP effect much larger |
| Average saturation | Neuroticism ↓ | −.142 (liked); attributed N **ρ=−.55** | GUN17, SEG17 | **Strong for attributed N — the single largest colour effect in the literature** |
| **Saturation variance** (both vivid and bleak) | Openness ↑ / Conscientiousness ↑ / Extraversion ↑ | +.20^^, +.16^, +.19^^ | F16 | Single-source |
| **Brightness / value mean** | **Openness ↓** | **−.25\*** (F16); **−.108** (GUN17 posted); −.081 (liked) | F16, GUN17 | **Strong, replicated** |
| Brightness mean | **Neuroticism ↑** | **+.22^** | F16 | ⚠️ **GUN17 finds −.020 (n.s.); org-account study finds +** — direction unstable |
| Brightness mean | Extraversion ↑ | +.124 (posted) | GUN17 | ⚠️ **F16 finds −.19^** (opposite) |
| Brightness mean | Conscientiousness ↑ | +.028; +.040 | LIU16, GUN17 | Weak, consistent |
| Dark-pixel share (value low) | **Openness ↑** | **+.28\*\*** | F16 | Consistent with brightness-mean result |
| Contrast | Openness ↑ | +.016 | LIU16 | ⚠️ **BR20 finds −.21** |
| **Colourfulness / hue count** | **Extraversion ↑** | **+.040** (LIU16); **+.118** hue count (GUN17 posted) | LIU16, GUN17 | **Moderate, replicated** |
| Colourfulness | Agreeableness ↑ | +.029 | LIU16 | ⚠️ SEGMM17 finds −.04* on Facebook profile pics for E; org-accounts find + |
| Colourfulness / hue count | Neuroticism ↓ | −.036; −.103 (hue count) | LIU16, GUN17 | **Moderate, replicated** |
| Colourfulness | Openness ↓ | −.017; −.094 (hue count) | LIU16, GUN17 | **Moderate, replicated** — open users prefer simpler palettes |
| Naturalness | Agreeableness ↓ | −.036 | LIU16 | Single-source |
| **Warm colours (red/orange/yellow)** | **Extraversion ↑** | red **+.09\***, pink **+.08\***, purple **+.07\*** (Facebook profile pics); "extraverts → warm colours" (Moroccan **males**) | SEGMM17, EB24(M) | ⚠️ **F16 finds E ↔ red −.17^, orange −.16^, green +.23^^, blue +.17^; EB24 females find E ↔ blue +.14, warm −.16.** Direction is genuinely unresolved. |
| Warm colours | Openness ↑ | **+.25** warm, **+.24** red | BR20 | ⚠️ **F16 finds O ↔ cold +.05, green +.17^, warm −.05** |
| Cold colours (green/blue) | Conscientiousness ↑ | **+.20** blue, **+.17** cold | BR20 | ⚠️ **Kim & Kim 2018 find red for conscientious users** — explicitly flagged by BR20 as a replication failure |
| % orange pixels | **Agreeableness ↑ (attributed)** | **ρ = +.45** | SEG17 | Largest single colour→trait effect for A (attributed) |
| % orange pixels | **Neuroticism ↓ (attributed)** | **ρ = −.56** | SEG17 | Largest single colour→trait effect overall |
| % blue pixels | Agreeableness ↑ / Neuroticism ↓ (attributed) | ρ = +.36 / −.52 | SEG17 | Attributed only |
| % red pixels | Agreeableness ↑ / Neuroticism ↓ (attributed) | ρ = +.30 / −.40 | SEG17 | Attributed only |
| Sharpness | Openness ↑ | +.025; "aesthetic quality" | LIU16 | Consistent with O ↔ aesthetics theme |
| Sharpness | Conscientiousness ↓ / Agreeableness ↓ | −.022 / −.021 | LIU16 | Weak |
| Blur | Conscientiousness ↑ / Agreeableness ↑ | +.036 / +.023 | LIU16 | Weak, counterintuitive |

### 7.2 Affective colour dimensions (Valdez–Mehrabian PAD)

*Pleasure = .69·V + .22·S; Arousal = −.31·V + .60·S; Dominance = −.76·V + .32·S. Note these are **linear functions of brightness and saturation** — they are not independent evidence, and any PAD result is a restatement of the V/S results above.*

| Feature | Trait | Values | Sources | Confidence |
|---|---|---|---|---|
| **Pleasure / Valence** | **Neuroticism ↑** | **+.22^^** | F16 | ⚠️ Directly **contradicts** SEG17 attributed N (valence ρ = −.40) and GUN17 (+.042 n.s.) |
| Pleasure / Valence | Openness ↓ | −.19^^ | F16 | Consistent with O ↔ dark images |
| Pleasure / Valence | Extraversion ↓ | −.18^ | F16 | ⚠️ SEGMM17 finds E ↔ valence **+.04\*** (opposite) |
| Valence | Agreeableness ↑ (attributed) | ρ = +.27 | SEG17 | Attributed only |
| **Arousal** | **Openness ↑** | **+.23\*** | F16 | ⚠️ **BR20 finds −.19** (opposite, both significant) |
| **Arousal** | **Extraversion ↑** | **+.119** (posted) | GUN17 | Consistent with E ↔ saturation |
| **Arousal** | **Conscientiousness ↑ / Neuroticism ↓** | **+.150 / −.139** (liked) | GUN17 | Moderate |
| Arousal | Agreeableness ↑ / Neuroticism ↓ (attributed) | ρ = +.38 / −.52 | SEG17 | Strong (attributed) |
| **Dominance** | **Openness ↑** | **+.28\*\*** | F16 | ⚠️ **BR20 finds −.18** |
| Dominance | Extraversion ↑ | +.113 (posted); +.17^ | GUN17, F16 | **Consistent across two Instagram/Twitter samples** |
| Dominance | Neuroticism ↓ | −.18^^; −.107 (liked) | F16, GUN17 | **Moderate, replicated** |

### 7.3 Faces and people — the strongest and most consistent family

| Feature | Trait | Values | Sources | Confidence |
|---|---|---|---|---|
| **Number of faces / people present** | **Extraversion ↑** | **attributed ρ = +.53** (SEG17); **+.07\*** (SEGMM17, n=11,736); **+.103** (LIU16); people-tag cluster **+.321 posted / +.128 liked** (GUN17); % posts with people **+.116** (GUN17); % images with faces **+.14** (EB24 females) | SEG17, SEGMM17, LIU16, GUN17, EB24, Celli14 | ★★★ **The single most robust finding in the entire field.** Replicated in ≥6 independent samples, across Flickr, Facebook, Twitter and Instagram, with both self-assessed and attributed labels. |
| **Number of faces / people present** | **Openness ↓** | **−.16^** faces, **−.22^^** people (F16); **−.08\*** (SEGMM17); **−.092** face count, **+.061** is-not-face, **−.102** multiple faces (LIU16); % posts with people **−.106** posted / **−.116** liked (GUN17); "fewer people" (EB24 both genders); attributed = n.s. (SEG17) | F16, SEGMM17, LIU16, GUN17, EB24 | ★★★ **Second most robust finding.** Open users post objects, art and scenes rather than people. |
| **Presence of ≥1 face** | **Conscientiousness ↑** | **+.04\*** (SEGMM17); **one-face +.102, is-not-face −.121, face count +.106** (LIU16); % posts with people **+.109** (GUN17) | SEGMM17, LIU16, GUN17 | ★★ **Strong.** Conscientious users post the *normative* profile picture: exactly one face. |
| Presence of faces | Agreeableness ↑ | **+.03\*** (SEGMM17); face count **+.078**, is-not-face **−.070** (LIU16); "lots of faces" | SEGMM17, LIU16 | ★★ Moderate |
| Faces / people | Neuroticism ↓ | **is-not-face +.071, face count −.067** (LIU16); attributed ρ = **−.28** (SEG17) | LIU16, SEG17 | ★★ Moderate; neurotic users avoid showing people. ⚠️ GUN17 finds N ↔ *close-ups* of faces (+.099) while posting fewer people images overall. |
| **Face ratio** (face size / image size) | **Extraversion ↓** | **−.097** (strongest of all traits) | LIU16 | Single-source but large; interpreted as more body/environment/other people in frame |
| Face ratio | Openness ↑ / Neuroticism ↑ | +.038 / +.057 | LIU16 | Consistent with the O–N "solitary, larger face" cluster |
| Multiple faces (>1) | Extraversion ↑ | +.058 | LIU16 | Consistent |
| Default/placeholder profile image | Conscientiousness ↓ | −.043 | LIU16 | Weak |

### 7.4 Facial expression and emotion (profile pictures)

*All from LIU16, n=66,502, text-inferred labels, controlled for age and gender. These are the largest-n emotion→trait numbers in the literature but rest on text-inferred ground truth.*

| Feature | O | C | E | A | N | Notes |
|---|---|---|---|---|---|---|
| **Smiling** | **−.089** | **+.190** | +.050 | **+.148** | **−.104** | C > A > E; C is the *most* expressive trait, contrary to theory — the authors attribute this to normative smiling in profile pictures |
| **Joy** | **−.093** | **+.180** | +.061 | **+.140** | **−.107** | |
| **Positive mood** | **−.093** | **+.175** | +.065 | **+.137** | **−.107** | |
| **Valence** | −.075 | **+.140** | +.053 | **+.105** | −.090 | |
| **Expressiveness** | −.072 | **+.140** | +.054 | **+.106** | −.089 | |
| **Neutral (absence of emotion)** | **+.068** | **−.128** | −.047 | **−.093** | **+.081** | The *strongest* neuroticism cue: lack of emotion, not presence of negative emotion |
| Negative mood | +.043 | −.079 | −.029 | −.067 | +.044 | |
| Anger | +.037 | −.080 | −.042 | −.055 | +.056 | |
| Sadness | +.023 | −.051 | −.034 | — | +.026 | |
| Attention (closeness to camera) | −.047 | +.049 | +.018 | +.040 | −.048 | |

- **Two clean clusters** emerge: {Openness, Neuroticism} = low-emotion, non-face images; {Conscientiousness, Extraversion, Agreeableness} = face present, positive emotion. Note this is an *emotion* axis, not an extraversion axis — Conscientiousness, not Extraversion, loads highest.
- **Corroboration:** Celli et al. (2014) found "extroverted and emotionally stable people tend to have pictures in which they are smiling or appear with other people." Osterholz et al. (2023) found appearance-focused self-images → perceived as more extraverted, narcissistic, less agreeable.
- **⚠️ El Bahy (2024) contradicts:** Moroccan *females* high in Openness posted images with **sadness and fear**; high Conscientiousness with **disgust** (+.15) and less neutral (−.12); Neuroticism with **anger** and *less* disgust (−.13). The direction of "conscientious = positive emotion" does not survive the culture change.

### 7.5 Eyewear and self-presentation

| Feature | Trait | Values | Source |
|---|---|---|---|
| **Reading glasses** | **Openness ↑ (+.054), Neuroticism ↑ (+.071), Conscientiousness ↓ (−.099), Extraversion ↓ (−.017)** | LIU16 (n=66,502) | Consistent with prior psychology on glasses ↔ perceived intelligence/introversion (Hellström & Tekle 1994; Terry & Kroger 1976) |
| No glasses | Conscientiousness ↑ (+.085), Neuroticism ↓ (−.065) | LIU16 | |
| Sunglasses | All traits ↓ (−.017 to −.028) | LIU16 | Weak, uniformly negative |
| Estimated age *from the picture* (controlling for real age) | Conscientiousness ↑ (+.050), Extraversion ↓ (−.105) | LIU16 | Conscientious users choose photos making them look older; extraverts younger or photographed with younger people |

### 7.6 Composition and photographic aesthetics

| Feature | Trait | Values | Sources | Confidence |
|---|---|---|---|---|
| **Rule of thirds observed** | **Conscientiousness ↑ (attributed ρ = +.22)**; Extraversion ↑ (+.032 LIU16; +.04* SEGMM17); Agreeableness ↑ (+.033 LIU16; +.02 SEGMM17) | SEG17, LIU16, SEGMM17 | ★★ Consistent across three samples |
| **Rule of thirds observed** | **Openness ↓ (attributed ρ = −.21)**; −.033 (LIU16); Neuroticism ↓ (−.034 LIU16) | SEG17, LIU16 | ★★ Consistent — open users use *unconventional* composition |
| **Level of detail** (number of regions) | **Conscientiousness ↑ (attributed +.19)**; Extraversion ↑ (**+.07\*** SEGMM17) | SEG17, SEGMM17 | ★★ |
| **Level of detail** | **Openness ↓ (attributed −.30)** | SEG17 | Strongest composition effect for O |
| Average region size | Extraversion ↓ (−.07*), Agreeableness ↓ (−.03) | SEGMM17 | |
| Edge distribution (subject-focused edges = simplicity) | **Openness ↑ (+.047)**, Neuroticism ↑ (+.038), **Agreeableness ↓ (−.048)** | LIU16 | Open users' images are simple; agreeable users' are cluttered |
| Hue count (fewer = simpler) | Openness ↓ (−.028 LIU16; −.094 GUN17) | LIU16, GUN17 | ★★ Simplicity is an Openness marker |
| Dynamic lines (emotional) | Openness ↓ (−.020), Agreeableness ↑ (+.033) | LIU16 | |
| Static lines | Extraversion ↑ (+.018), Openness ↑ (+.017) | LIU16 | |
| Gray-distribution entropy | **Openness ↓ (attributed ρ = −.27)** | SEG17 | Open users like homogeneous illumination/texture |
| Brightness energy / exposure | **Openness ↑ (attributed ρ = +.35)** | SEG17 | |
| Tamura directionality | **Extraversion ↓ (attributed ρ = −.33)**, Conscientiousness ↑ (+.23) | SEG17 | |
| Tamura contrast | Extraversion ↑ (attributed ρ = +.25) | SEG17 | |
| GLCM contrast (hue / saturation) | Extraversion ↑ (attributed ρ = +.26 / +.21); +.04* brightness | SEG17, SEGMM17 | ★★ |
| GLCM energy (saturation) | Extraversion ↓ (−.06*), Neuroticism ↑ (+.03*) | SEGMM17 | |
| "Aesthetic quality" composite (contrast + sharpness + saturation, low blur) | **Openness ↑** | LIU16, Osterholz23 | ★★ Corroborated by human judges: open users have "more aesthetic professionally looking profiles" |

### 7.7 Semantic content — objects, scenes and activities

*Values are Pearson r from GUN17 (Twitter, n≈3,500, text-inferred, controlled for age, gender and all four other traits) unless noted. FT18 = Instagram Spearman ρ, n=193, survey labels, Bonferroni p<.001.*

| Content | Trait | Value | Source |
|---|---|---|---|
| **Art / drawing / cartoon / clipart / artwork / sketch / tattoo** | **Openness ↑** | **+.148 / +.137 / +.119 / +.102** (posted); +.112 / +.097 (liked) | GUN17 |
| **Art / drawing / cartoon / artwork** | **Extraversion ↓** | **−.253 / −.213 / −.127** (posted); −.164 / −.122 / −.103 (liked) | GUN17 |
| Art / drawing / artwork | **Conscientiousness ↓** | −.111 / −.105 / −.097 | GUN17 |
| Art / cartoon | Neuroticism ↓ | −.063 | GUN17 |
| **Music instruments** | **Openness ↑** | **ρ = +.156** | FT18 (Instagram) |
| Music / guitar / performance / concert / stage | Agreeableness ↑ | +.108 / +.081 | GUN17 |
| **Sports / ball / athlete / football / tennis / runner** | **Openness ↓** | **−.207 / −.195 / −.154 / −.109 / −.105** (posted) — the strongest *negative* content signal for O | GUN17 |
| **Sports** | **Conscientiousness ↑** | **ρ = +.156** (FT18); sports ball r=+.24 (EB24 females); TV/laptop/cup also + | FT18, EB24 |
| **People / person / adult / portrait / smile / happy** | **Extraversion ↑** | **+.321 posted / +.128 liked** — the largest single content correlation reported anywhere in this literature | GUN17 |
| Face / pretty / hair / model / fashion / sexy | Extraversion ↑ | +.243 / +.089 | GUN17 |
| Women / group / friends / friendship | Extraversion ↑ (+.182), Agreeableness ↑ (+.093) | GUN17 |
| Happiness / couple / together / love / fun / family | Extraversion ↑ (+.171), **Agreeableness ↑ (+.144)**, Neuroticism ↑ (+.104) | GUN17 |
| Disco / cabaret / ballroom | Extraversion ↑ (+.136) | GUN17 |
| Body / swimsuit / bikini | Extraversion ↑ (+.127) | GUN17 |
| **Office / businessman / corporate / suit / business / work / success** | **Agreeableness ↓ (−.211 / −.132 / −.101)**; **Conscientiousness ↑ (+.132 / +.101)**; Openness ↑ (+.108) | GUN17 |
| Classroom / building / architecture / city / structure / furniture / home / room | **Conscientiousness ↑** (+.153 / +.114 / +.104 / +.094 / +.078) | GUN17 |
| Paper / document / writing / book / pen | Conscientiousness ↑ (+.099), **Neuroticism ↑ (+.107)** | GUN17 |
| Press / print media / newspaper / money / finance / signboard | **Agreeableness ↓** (−.177 / −.129 / −.099) | GUN17 |
| **Cat / feline / pet / kitten** | **Agreeableness ↑ (+.094)**; **Neuroticism ↑ (+.082)** | GUN17 |
| Dog / animal / canine / retriever | **Neuroticism ↑ (+.092 / +.060)** | GUN17 |
| Cat (absence of) | Neuroticism ↑ | r = −.16 for cats among Moroccan females | EB24 |
| **Flower / floral / garden / petal / blossom** | **Agreeableness ↑ (+.098)** | GUN17 |
| Trees / season / nature | Agreeableness ↑ (+.094) | GUN17 |
| **Clothing** | **Agreeableness ↑ (ρ = +.234)**, **Conscientiousness ↑ (+.148)**, **Neuroticism ↓ (−.184)** | FT18 (Instagram) |
| **Leisure** | **Agreeableness ↑ (ρ = +.180)** | FT18 |
| **Electronics** | **Extraversion ↑ (ρ = +.167)** | FT18 |
| Computer / equipment / technology / device / phone | **Neuroticism ↓** (−.096 / −.094 / −.060); Conscientiousness ↓ (−.072) | GUN17 |
| **Jewelry** | **Neuroticism ↑ (ρ = +.188)** | FT18 |
| Cute / eyes / close-up face | **Neuroticism ↑ (+.104 / +.099)**; Conscientiousness ↓ (−.101 / −.125) | GUN17 |
| Design / sign / icon / graphic / symbol / web / text / 3D | **Extraversion ↓ (−.165 / −.125)**; Neuroticism ↓ (−.064) | GUN17 |
| Senior / old / elderly / grandma / retired | Openness ↑ (+.155) | GUN17 |
| Ancient / palace / castle / historic | Openness ↑ (+.120) | GUN17 |
| Child / boy / kid / baby | Openness ↓ (−.099) | GUN17 |
| Game / puzzle | Openness ↓ (−.119) | GUN17 |
| Black / african / dark | Extraversion ↓ (−.128) | GUN17 |
| Plant / food / abstract (org. accounts) | Openness ↑ | Kim & Kim 2021 |
| Abstract objects | Openness ↑ (+.14), Agreeableness ↑ (+.15) | EB24 (females) |
| Landscapes / buildings | Conscientiousness ↑ | Celli25 survey; GUN17 |
| Indoor places | Neuroticism ↑ | Segalin MM17 |

### 7.8 Posting-behaviour metadata (not image content, but co-collected)

| Feature | Trait | Value | Source |
|---|---|---|---|
| **Number of images posted** | Agreeableness ↓ | **−.141** | GUN17 |
| Number of images posted | Openness ↑ (+.068), Neuroticism ↑ (+.093), Extraversion ↑ (+.094) | GUN17 |
| Number of images posted | Conscientiousness ↑ (+.15), Extraversion ↑ (+.12) | EB24 (females) |
| **Number of images liked** | **Conscientiousness ↓ (−.131)**; **Neuroticism ↑ (+.159)** | GUN17 |
| More images per user | *All traits: prediction accuracy improves* | EB24 (RMSE monotonically improves ≥1 → ≥10 → ≥20 photos) |
| Appearance-focused self-images (selfies) | Perceived: Extraversion ↑, self-confidence ↑, narcissism ↑, Agreeableness ↓ | Osterholz23 |
| Filter choice (Instagram) | Only 4/25 filters significant; C×Kelvin +.203, A×Crema −.205, A×Gotham −.204, N×Hudson +.224 | F16 — **authors abandoned this line** |

---

## 8. Which traits are reliably predictable, and which are near-noise

**From images specifically, against survey ground truth:**

| Trait | Verdict | Evidence |
|---|---|---|
| **Openness** | **Best-supported.** Strongest and most theoretically coherent cue set (fewer people, artistic/aesthetic content, simple compositions, unconventional framing). Best-predicted trait in Kosinski Likes work (r=.43) and Youyou. Best image-only RMSE across studies (0.59–0.68 on [1,5]). But note **the colour direction does not replicate** (F16 vs BR20 flip on saturation, warmth, arousal, dominance). | F16, FT18, EB24, LIU16, GUN17, Samani18 |
| **Conscientiousness** | **Well-supported, but for a boring reason.** Predicted mainly through *normativity* — one face, positive expression, conventional composition, office/building/classroom content. Best RMSE 0.53–0.67. Samani et al. rank it the most predictable trait from images. Segalin (Flickr) ranks it near the bottom. | LIU16, GUN17, EB24, Samani18 |
| **Extraversion** | **Split verdict, and it matters which task.** For **attributed/perceived** traits it is by far the best (SEG17 ρ up to .68; face count ρ=+.53; SEGMM17 machine accuracy 0.68 vs. human 0.60; Osterholz human r=.44). For **self-assessed** traits from images it is consistently among the **worst** — F16 RMSE 0.90, EB24 0.73–0.82, Samani18 explicitly ranks it least predictable. Extraversion is the most *visible* trait and the least *inferable-from-artefacts* trait. | SEG17, SEGMM17, F16, EB24, Samani18, Osterholz23 |
| **Agreeableness** | **Weak.** Lowest meta-analytic r across all footprint types (0.29). LIU16: the only trait *not* significantly predictable on the survey dataset. Kosinski: r ≈ .17–.30. Its image cues (faces, positive emotion) overlap almost completely with C and E. | Azucar18, LIU16, Kosinski13 |
| **Neuroticism** | **Near-noise from images alone.** Consistently the worst RMSE in every Instagram study (F16 0.95; EB24 0.84–0.98; BR20 0.79; org-account study: the only trait with unacceptable RMSE). GUN17 D1 reports r = .404–.418 from Imagga tags at n=161, which is a striking outlier and is not corroborated by any other survey-labelled study. Its brightness direction contradicts across F16 / SEG17 / GUN17. | F16, EB24, BR20, Kim&Kim21 |

**Ordering by evidence weight:**
`Openness ≈ Conscientiousness > Extraversion (attributed only) > Extraversion (self) ≈ Neuroticism ≈ Agreeableness`

---

## 9. What replicates, what doesn't

### Replicates (≥3 independent samples, same sign)
1. **Number of faces / people present ↑ Extraversion.** Flickr (attributed ρ=+.53), Facebook profile pics (n=11,736, +.07*), Twitter profile pics (n=66,502, +.103), Twitter posts (+.321 on the people tag cluster), Instagram (+.14 % images with faces). Also confirmed by human judges (Celli 2014; Osterholz 2023).
2. **Fewer faces / people ↑ Openness.** Instagram (−.16 to −.22), Facebook (−.08*), Twitter (−.09 to −.12), Moroccan Instagram, organisational accounts.
3. **Exactly one face + positive expression ↑ Conscientiousness.** Twitter profile pics, Facebook profile pics, Twitter posts.
4. **Art / drawings / abstract content ↑ Openness, ↓ Extraversion.** Twitter (posted and liked independently), Instagram (music instruments), Branz's German replication, Marshall et al.
5. **Simplicity (low hue count, low level of detail, unconventional composition) ↑ Openness.** Flickr attributed (ρ=−.30 level of detail, −.21 rule of thirds), Twitter profile pics.
6. **Low saturation / grayscale / low chromatic diversity ↑ Neuroticism.** Flickr attributed (ρ=−.55 saturation), Twitter posted (+.262 grayscale, −.103 hue count).
7. **Attributed > self-assessed by a factor of 2–3.** Segalin 2017 (0.68 vs 0.26); Segalin CVIU (65% vs 54%); Guo et al. (~10 points); confirmed by the whole APP literature.
8. **Extraversion and Neuroticism are the hardest self-assessed traits to regress from images.** Ferwerda 2016, El Bahy 2024, Quercia 2011, Kim & Kim 2021 — all four independently.
9. **More images per user → better prediction.** Segalin 2017 (bag-size curve), El Bahy 2024 (three-experiment ladder), Youyou 2015 (log-linear in Likes).

### Does **not** replicate
1. **Every colour→trait direction except "N ↔ low saturation".** The Ferwerda (2016) Instagram colour matrix and the Branz (2020) Instagram colour matrix, built on the *same features* with comparable n, give **opposite signs** for Openness on saturation (+.16 vs −.17), warm/cold (cold vs warm), arousal (+.23 vs −.19), dominance (+.28 vs −.18) and contrast. Branz explicitly reports the failure.
2. **Warm vs. cold colours for Extraversion.** Segalin (Facebook profile pics) → warm. Ferwerda (Instagram) → cold/green/blue. El Bahy → warm for males, cold for females. Unresolved.
3. **Red vs. blue for Conscientiousness.** Kim & Kim 2018 → red. Branz 2020 → blue. Directly contradictory, explicitly flagged.
4. **Brightness for Neuroticism.** Ferwerda → bright (+.22). Segalin attributed → dark/low-valence (valence ρ=−.40). Guntuku → n.s.
5. **Pleasure/valence for Neuroticism.** Ferwerda +.22^^; Segalin attributed −.40. Opposite.
6. **Which trait is "most predictable from images."** Segalin 2017 (Flickr): Extraversion. Samani et al. 2018 (same Flickr corpus, different features): Conscientiousness and Openness, with Extraversion *least* predictable. Ferwerda: Openness and Conscientiousness. No consensus.
7. **"Conscientious people show the most positive emotion."** LIU16 finds this at n=66,502 and explicitly notes it contradicts personality theory; El Bahy finds Moroccan conscientious users express *fear* and *disgust*.
8. **Filter choice.** 4 significant filters out of 25 in the only study that looked; the authors dropped the line of research.

### Systematic reasons for the non-replication
- **Underpowered samples.** n = 100–320 for r ≈ .15–.25 effects.
- **Massive multiple testing.** 23 features × 5 traits = 115 tests (Ferwerda); 85 features × 5 = 425 (Liu); 17 × 5 (Ferwerda & Tkalcic). Only Guntuku (Simes), Ferwerda & Tkalcic (Bonferroni) and Segalin MM (Bonferroni) correct.
- **Colour statistics are not stable constructs.** They depend on camera hardware, platform compression, filter fashion at time of scraping, ambient light in the user's country, and skin tone distribution in the sample. None of these are personality.
- **Population confounds.** MTurk US adults (Ferwerda), German undergraduates (Branz), Moroccan users (El Bahy), Italian Flickr Pro photographers (Segalin), Chinese Weibo users (Guntuku) — the samples are not exchangeable and neither are the colour norms.
- **Label heterogeneity.** BFI-44, BFI-10, BFI-2, TIPI, IPIP-NEO-PI-R, and text-model outputs are all treated as interchangeable "Big Five."

---

## 10. The honest ceiling

**For self-reported Big Five from photographs alone:**

| Bound | Value | Source |
|---|---|---|
| Meta-analytic ceiling, *all* digital footprints combined | r = 0.29–0.40 | Azucar et al. 2018 |
| Meta-analytic convergent validity, all computational personality prediction | ρ = 0.30 | Hinds & Joinson |
| "Personality coefficient" — the general ceiling for *any* behaviour predicting personality | r = 0.30–0.40 | Meyer et al. 2001; Roberts et al. 2007 |
| Best image-only result at large n against survey labels | **r = 0.145–0.189** (single profile picture, n=66,502) | Liu et al. 2016 |
| Best image-only result at large n, binary classification against survey labels | **55–56% (mean split), 60–62% (extreme-quartile split)**, n=11,736 | Segalin et al. 2017 (MM) |
| Best image-only result, self-assessed traits, Flickr | **r = 0.26** (regression), **54%** (binary) | Segalin et al. 2017 (TAC); Segalin et al. 2017 (CVIU) |
| Human observers judging a *full Instagram account* | **r = 0.25–0.44** | Osterholz et al. 2023 |
| Human observers judging a single Facebook profile picture | **58–60% binary accuracy**; Krippendorff α = 0.26–0.34 | Segalin et al. 2017 (MM) |
| Machine on the same 150 profile pictures | 68–69% binary accuracy | Segalin et al. 2017 (MM) |
| LLM zero-shot from *text* (upper bound of the modality) | r = 0.18–0.31 | Marengo 2025; Peters & Matz 2024 |
| Facebook Likes (not images) — the field's genuine high-water mark | **r = 0.56** (avg. 227 Likes), 0.66 (>500 Likes) | Youyou et al. 2015 |
| Kosinski Likes, best single trait | Openness r = 0.43 | Kosinski et al. 2013 |
| Best VLM on faces, 16-way perceived MBTI | 26.4% top-1, F1 = 18.0% | Chen et al. 2026 |

**The bottom line, stated as plainly as the evidence permits:**

1. **A single image gives you r ≈ 0.15–0.19 per trait.** That is roughly 2–4% of variance. It is real (it survives n=66,502) and it is nearly useless individually.
2. **A large gallery (100–300 images) plus content features gives you r ≈ 0.25–0.30 against survey labels**, and RMSE roughly equal to the trait's own standard deviation. Reported values above 0.40 in this literature come from text-inferred labels, attributed traits, or samples under 200.
3. **The image-only ceiling is *below* the digital-footprints ceiling.** Azucar's meta-analysis found that adding pictures did **not** improve prediction over other footprint types. Images underperform Likes (0.56), text (0.29–0.35), and combined footprints (0.29–0.40).
4. **Attributed personality is a different, much easier problem — r up to 0.68 — and it is not personality.** It is the impression the picture creates. If the goal is impression management, aesthetics, or ad targeting on perceived persona, the ceiling is genuinely high. If the goal is knowing what a person is actually like, it is not.
5. **Machines beat individual humans, but only barely and only on the easy traits.** 68–69% vs. 58–60% on binary Extraversion/Neuroticism from a profile picture, and the human raters agreed with *each other* at α = 0.26–0.34.
6. **The 2023–2026 VLM/LLM turn has not moved the self-report ceiling.** Every headline gain has come from switching to easier targets — perceived traits, MBTI, crowd-averaged first impressions. Where the target stayed "self-reported Big Five," LLMs land at r = 0.18–0.31 from years of text, i.e. exactly where supervised models sat in 2013. Marengo et al.'s finding that models agree with *each other* at r = 0.58–0.83 while agreeing with the *person* at r = 0.18–0.31 is the clearest evidence that current systems have learned a stable stereotype, not a person.
7. **Trait-level asymmetry is real and stable:** Openness and Conscientiousness are recoverable; Agreeableness and Neuroticism are close to noise; Extraversion is highly *perceptible* but poorly *inferable*.

---

## 11. Bibliography

### Instagram
1. Ferwerda, B., Schedl, M., & Tkalcic, M. (2015). Predicting personality traits with Instagram pictures. *Proc. 3rd Workshop on Emotions and Personality in Personalized Systems (EMPIRE)*, 7–10. ACM.
2. Ferwerda, B., Schedl, M., & Tkalcic, M. (2016). Using Instagram picture features to predict users' personality. *MultiMedia Modeling (MMM 2016)*, LNCS 9516, 850–861. Springer. https://doi.org/10.1007/978-3-319-27671-7_71
3. Ferwerda, B., & Tkalcic, M. (2018). You are what you post: What the content of Instagram pictures tells about users' personality. *HUMANIZE '18 @ IUI*, CEUR-WS Vol-2068. https://ceur-ws.org/Vol-2068/humanize2.pdf
4. Ferwerda, B., & Tkalcic, M. (2018). Predicting users' personality from Instagram pictures: Using visual and/or content features? *UMAP '18*, 157–161. ACM. https://doi.org/10.1145/3209219.3209248
5. Ferwerda, B., Schedl, M., & Tkalcic, M. (2016). Personality traits and the relationship with (non-)disclosure behavior on Facebook. *WWW '16 Companion*. ACM. *(Facebook, not Instagram — profile-section disclosure, not images.)*
6. Kim, Y., & Kim, J. H. (2018). Using computer vision techniques on Instagram to link users' personalities and genders to the features of their photos: An exploratory study. *Information Processing & Management, 54*(6), 1101–1114. https://doi.org/10.1016/j.ipm.2018.07.005
7. Kim, Y., & Kim, J. H. (2019). Instagram user characteristics and the color of their photos: Colorfulness, color diversity, and color harmony. *Information Processing & Management*.
8. Branz, L., Brockmann, P., & Hinze, A. (2020). Red is open-minded, blue is conscientious: Predicting user traits from Instagram image data. *PEOPLES @ COLING 2020*, 23–28. https://aclanthology.org/2020.peoples-1.3
9. Cooper, A. B., Blake, A. B., Pauletti, R. E., Cooper, P. J., Sherman, R. A., & Lee, D. I. (2020). Personality assessment through the situational and behavioral features of Instagram photos. *European Journal of Psychological Assessment, 36*(6), 959–972. https://doi.org/10.1027/1015-5759/a000596
10. Kim, Y., & Kim, J. H. (2021). Personality of public health organizations' Instagram accounts and according differences in photos at content and pixel levels. *IJERPH, 18*(8), 3903. https://doi.org/10.3390/ijerph18083903
11. (2022). Prediction of personality traits through Instagram photo HSV. Springer LNNS. https://doi.org/10.1007/978-3-031-05409-9_21
12. El Bahy, S., Aboutabit, N., & Hafidi, I. (2023). Analyzing Instagram images to predict personality traits. *ICMICSA 2022*, LNNS 656, ch. 31. Springer. https://doi.org/10.1007/978-3-031-29313-9_31
13. El Bahy, S., Aboutabit, N., & Hafidi, I. (2024). Analysis and prediction of personality traits using a self-generated database of Moroccan Instagram users. *Multimedia Tools and Applications*. https://doi.org/10.1007/s11042-024-19101-2
14. (2024). Personality of organizational social media accounts and its relationship with characteristics of their photos: analyses of startups' Instagram photos. *BMC Psychology*. https://doi.org/10.1186/s40359-024-01709-6
15. Marengo, D., Quilghini, F., Ricci, G., & Settanni, M. (2024). Instagram Stories unveiled: Exploring links with psychological distress, personality, and gender. *Cyberpsychology, Behavior, and Social Networking*. https://doi.org/10.1089/cyber.2023.0316
16. (2025). Personality prediction model: An enhanced machine learning approach. *Electronics, 14*(13), 2558. https://doi.org/10.3390/electronics14132558
17. Osterholz, S., Mosel, E. I., & Egloff, B. (2023). #Insta personality: Personality expression in Instagram accounts, impression formation, and accuracy of personality judgments at zero acquaintance. *Journal of Personality, 91*(3). https://doi.org/10.1111/jopy.12756
18. (2026). Image and metadata-driven personality inference for career recommendation: a social media-based AI framework for adolescents. *Discover Artificial Intelligence*. https://doi.org/10.1007/s44163-026-00981-2

### Flickr / PsychoFlickr
19. Cristani, M., Vinciarelli, A., Segalin, C., & Perina, A. (2013). Unveiling the multimedia unconscious: implicit cognitive processes and multimedia content analysis. *ACM MM '13*.
20. Segalin, C., Perina, A., Cristani, M., & Vinciarelli, A. (2017). The pictures we like are our image: Continuous mapping of favorite pictures into self-assessed and attributed personality traits. *IEEE Transactions on Affective Computing, 8*(2), 268–285. https://doi.org/10.1109/TAFFC.2016.2516994
21. Segalin, C., Cheng, D. S., & Cristani, M. (2017). Social profiling through image understanding: Personality inference using convolutional neural networks. *Computer Vision and Image Understanding, 156*, 34–50. https://doi.org/10.1016/j.cviu.2016.10.013
22. Guo, et al. (2019). Inferring personality traits from attentive regions of user liked images via weakly supervised dual convolutional network. *Neural Processing Letters*. https://doi.org/10.1007/s11063-019-09987-7

### Twitter / X
23. Quercia, D., Kosinski, M., Stillwell, D., & Crowcroft, J. (2011). Our Twitter profiles, our selves: Predicting personality with Twitter. *IEEE SocialCom*, 180–185.
24. Golbeck, J., Robles, C., Edmondson, M., & Turner, K. (2011). Predicting personality from Twitter. *IEEE SocialCom*, 149–156.
25. Liu, L., Preoţiuc-Pietro, D., Riahi Samani, Z., Moghaddam, M. E., & Ungar, L. (2016). Analyzing personality through social media profile picture choice. *ICWSM 2016*, 10(1), 211–220. https://doi.org/10.1609/icwsm.v10i1.14738
26. Guntuku, S. C., Lin, W., Carpenter, J., Ng, W. K., Ungar, L. H., & Preoţiuc-Pietro, D. (2017). Studying personality through the content of posted and liked images on Twitter. *WebSci '17*, 223–227. https://doi.org/10.1145/3091478.3091522
27. Riahi Samani, Z., Guntuku, S. C., Moghaddam, M. E., Preoţiuc-Pietro, D., & Ungar, L. H. (2018). Cross-platform and cross-interaction study of user personality based on images on Twitter and Flickr. *PLOS ONE, 13*(7), e0198660. https://doi.org/10.1371/journal.pone.0198660

### Facebook profile pictures
28. Celli, F., Bruni, E., & Lepri, B. (2014). Automatic personality and interaction style recognition from Facebook profile pictures. *ACM MM '14*, 1101–1104. https://doi.org/10.1145/2647868.2654977
29. Al Moubayed, N., Vazquez-Alvarez, Y., McKay, A., & Vinciarelli, A. (2014). Face-based automatic personality perception. *ACM MM '14*, 1153–1156.
30. Segalin, C., Celli, F., Polonio, L., Kosinski, M., Stillwell, D., Sebe, N., Cristani, M., & Lepri, B. (2017). What your Facebook profile picture reveals about your personality. *ACM MM '17*, 460–468. https://doi.org/10.1145/3123266.3123331 — arXiv:1708.01292

### Weibo / selfies
31. Guntuku, S. C., Qiu, L., Roy, S., Lin, W., & Jakhetiya, V. (2015). Do others perceive you as you want them to? Modeling personality based on selfies. *ASM '15 @ ACM MM*, 21–26. https://doi.org/10.1145/2813524.2813528
32. Qiu, L., Lu, J., Yang, S., Qu, W., & Zhu, T. (2015). What does your selfie say about you? *Computers in Human Behavior, 52*, 443–449.
33. Wei, H., et al. (2017). Beyond the words: Predicting user personality from heterogeneous information. *WSDM '17*. https://doi.org/10.1145/3018661.3018717

### Multi-platform fusion
34. Skowron, M., Tkalcic, M., Ferwerda, B., & Schedl, M. (2016). Fusing social media cues: Personality prediction from Twitter and Instagram. *WWW '16 Companion*, 107–108. https://doi.org/10.1145/2872518.2889368
35. Cucurull, G., Rodríguez, P., Yazici, V. O., Gonfaus, J. M., Roca, F. X., & González, J. (2018). Deep inference of personality traits by integrating image and word use in social networks. arXiv:1802.06757

### Meta-analyses, surveys and boundary benchmarks
36. Kosinski, M., Stillwell, D., & Graepel, T. (2013). Private traits and attributes are predictable from digital records of human behavior. *PNAS, 110*(15), 5802–5805. https://doi.org/10.1073/pnas.1218772110
37. Schwartz, H. A., et al. (2013). Personality, gender, and age in the language of social media: The open-vocabulary approach. *PLOS ONE, 8*(9), e73791.
38. Youyou, W., Kosinski, M., & Stillwell, D. (2015). Computer-based personality judgments are more accurate than those made by humans. *PNAS, 112*(4), 1036–1040. https://doi.org/10.1073/pnas.1418680112
39. Vinciarelli, A., & Mohammadi, G. (2014). A survey of personality computing. *IEEE Transactions on Affective Computing, 5*(3), 273–291.
40. Azucar, D., Marengo, D., & Settanni, M. (2018). Predicting the Big 5 personality traits from digital footprints on social media: A meta-analysis. *Personality and Individual Differences, 124*, 150–159. https://doi.org/10.1016/j.paid.2017.12.018
41. Junior, J. C. S. J., et al. (2019). First impressions: A survey on vision-based apparent personality trait analysis. *IEEE Transactions on Affective Computing*.
42. Marengo, D., et al. (2023). Predicting Big Five personality traits from smartphone data: A meta-analysis on the potential of digital phenotyping. *Journal of Personality*. https://doi.org/10.1111/jopy.12817
43. Celli, F., Vinciarelli, A., Kosinski, M., & Lepri, B. (2025). Twenty years of personality computing: Threats, challenges and future directions. arXiv:2503.02082
44. Machajdik, J., & Hanbury, A. (2010). Affective image classification using features inspired by psychology and art theory. *ACM MM '10*, 83–92. *(The source of the colour/PAD feature set used by nearly every study above.)*
45. Valdez, P., & Mehrabian, A. (1994). Effects of color on emotions. *Journal of Experimental Psychology: General, 123*(4), 394–409. *(Source of the PAD equations.)*
46. Meyer, G. J., et al. (2001). Psychological testing and psychological assessment: A review of evidence and issues. *American Psychologist, 56*(2), 128–165. *(Source of the r ≈ .30–.40 correlational upper limit.)*

### LLM / VLM era
47. Gan, P. Z., Sowmya, A., & Mohammadi, G. (2022). Zero-shot personality perception from facial images. *AI 2022*, LNAI 13728, Springer. https://doi.org/10.1007/978-3-031-22695-3_4
48. Gan, P. Z., Sowmya, A., & Mohammadi, G. (2023). CLIP-based model for effective and explainable apparent personality perception. *MRAC '23 @ ACM MM*. https://doi.org/10.1145/3607865.3613178
49. Peters, H., & Matz, S. C. (2024). Large language models can infer psychological dispositions of social media users. *PNAS Nexus, 3*(6), pgae231. https://doi.org/10.1093/pnasnexus/pgae231 — arXiv:2309.08631
50. Marengo, D., Montag, C., & Settanni, M. (2025). Inferring personality from social media activity using large language models: Cross-model agreement, temporal stability, and convergent validity with self-reports. *Journal of Personality*. https://doi.org/10.1111/jopy.70019
51. (2025). Can LLMs infer personality from real world conversations? arXiv:2507.14355
52. (2025). Investigating large language models in inferring personality traits from user conversations. arXiv:2501.07532
53. Chen, S., Zhu, X., Zhao, W., Shi, H., Zhang, X.-Y., & Lei, Z. (2026). Knowing you at first glance: Inferring apparent personality from faces. arXiv:2607.14631

---

## 12. Practical notes for anyone building on this

- **Use content, not colour.** Semantic features (CNN penultimate layer, Imagga/Vision API tags, object and scene classes) beat colour statistics in every study that compared them head-to-head at adequate n (Samani et al. 2018; Guntuku et al. 2017). Colour features are the least replicable part of the literature.
- **Face count and "does this image contain people" are the highest-value features per unit of engineering effort.** Liu et al. got r = .078–.122 from a **5-feature** image-type block — better than 44 colour features.
- **Fuse posted + liked images.** +6% to +15% over either alone (Guntuku et al. 2017).
- **Require a minimum gallery size.** Performance rises monotonically with images per user (Segalin 2017; El Bahy 2024). Twenty images is a reasonable floor; the marginal gain is log-linear.
- **Always report the baseline.** RMSE on a [1,5] trait must be compared to the trait's SD, not to zero.
- **Never validate against text-inferred labels alone.** Two of the three largest studies did, and both found the effects disappeared on the survey subsample.
- **Distinguish the product you are building.** If you want to know how a person *comes across* (impression, brand fit, aesthetic persona), the attributed-trait literature supports r ≈ 0.5–0.7 and is a real capability. If you want to know who someone *is*, the ceiling is r ≈ 0.2–0.3 and it does not currently move with more compute.
- **Ethics.** Every high-quality paper in this corpus flags the same risks: users do not know what is inferable from their photos (Samani et al.); personality-weighted credit scoring and hiring risk structural exclusion (Celli et al. 2025); apparent-personality models predict *impressions, not intrinsic personality* and should not drive high-stakes decisions (Chen et al. 2026). Given the effect sizes documented above, any individual-level decision made on image-inferred personality is being made on 2–9% of variance.
