# Building Audience & Customer Profiles from Instagram Visual Content
## A review of the published marketing / consumer-research literature, and an audit of the practitioner frameworks

Compiled 2026-08-23. Scope: peer-reviewed marketing science on image mining, visual brand measurement and social-media engagement; the adjacent CS/arXiv literature on demographic inference from images; and the practitioner canon (content pillars, brand archetypes, colour psychology, VALS/PRIZM). Ends with a practical taxonomy of what a business can legitimately infer from a public Instagram grid.

### How to read the evidence labels

| Label | Meaning |
|---|---|
| **[A] Peer-reviewed, top-tier** | Marketing Science, JMR, JM, JCR, IJRM, JAMS, Management Science. Replicable method, reported out-of-sample performance or identified causal design. |
| **[B] Peer-reviewed, second-tier / applied** | JBR, JRCS, CHB, Electronic Markets, regional journals. Real data, weaker identification or narrower generalisability. |
| **[C] Preprint / working paper / conference** | arXiv, SSRN, IEEE. Not (yet) refereed. |
| **[D] Practitioner folklore** | Agency blogs, platform vendors, books without empirical validation. Useful as a *heuristic vocabulary*, not as evidence. |
| **[E] Contested / weak** | Widely repeated but poorly sourced, non-replicated, or refuted. |

A running theme: **the literature is much stronger on "what is in an image" than on "who is behind the account."** Nearly all the top-tier work measures *brand portrayal* or *post engagement*. Almost none of it validates inferring a *customer profile* from a grid. That gap is where the practitioner frameworks rush in, and where the evidence is thinnest.

---

# PART A — Core image-mining papers in marketing

## A1. Liu, Dzyabura & Mizik — "Visual Listening In" **[A]**

**Citation.** Liu, L., Dzyabura, D., & Mizik, N. (2020). "Visual Listening In: Extracting Brand Image Portrayed on Social Media." *Marketing Science*, 39(4), 669–686. DOI 10.1287/mksc.2020.1226. (Working paper: SSRN 2978805; MSI Report 20-113.)

**Question.** Can you measure how a brand is *portrayed* by consumers, from the photos consumers post, without asking anyone anything?

**Method — two stages.**

*Stage 1: train attribute classifiers.* No labelled dataset of "brand attributes in images" existed, so they built one from **Flickr**, exploiting Flickr's text+content+clickstream search. For each of four intangible brand attributes they queried the attribute word for positive examples and its antonym for negatives, taking the top ~200 result pages (≈2,000 photos) each:

| Attribute | Antonym used for negatives |
|---|---|
| glamorous | drab (robustness: dull) |
| rugged | gentle (robustness: smooth) |
| healthy | unhealthy |
| fun | dull (robustness: boring) |

**Training set: 16,368 photographs**, balanced 50/50 positive/negative (so chance = 50%).

Two model families:
- **SVM on 13 hand-defined feature types**, grouped as colour / shape / texture — RGB histogram (192-dim), HSV joint histogram (256-dim), L\*a\*b joint histogram (784-dim); Canny + Hough line features (count of straight lines, % parallel lines, orientation and orientation×distance histograms), Harris corner features (global and 2×2-block local corner %), edge-orientation histogram (64-dim), HOG (144-dim); LBP (26-dim) and Gabor (32-dim) texture.
- **ConvNets with transfer learning**, fine-tuned from (a) ImageNet and (b) the **Flickr Style** model. Training on a single K80 GPU node, ~8 hours, converging at 600–4,100 iterations depending on attribute.

**Out-of-sample accuracy (balanced, chance = 50%):**

| Classifier | glamorous | rugged | healthy | fun | Mean |
|---|---|---|---|---|---|
| SVM (best feature set) | 74.1% | 73.3% | 63.4% | 65.3% | ~65–69%* |
| SVM colour only | 69.5% | 65.6% | 63.4% | 60.4% | — |
| SVM shape only | 70.0% | 70.0% | 56.0% | 57.3% | — |
| SVM texture only | 70.9% | 67.2% | 51.4% | 55.6% | — |
| ConvNet ← ImageNet | 81.5% | 76.6% | 57.1% | 74.5% | **72.4%** |
| ConvNet ← **Flickr Style** | **84.9%** | **80.7%** | **70.6%** | **81.5%** | **79.4%** |

\* The working paper's body text states an SVM mean of 65.3%; the per-attribute figures average 69.0%. Minor internal inconsistency — treat SVM as "mid-to-high 60s."

Two substantive method findings worth carrying over: (i) **transfer from a *style* model beats transfer from an *object-detection* model** for perceptual/aesthetic attributes — brand attribute classification is a style task, not an object task; (ii) for **`healthy`, colour alone is the best SVM feature set** — shape and texture add nothing. Perceptual attributes have genuinely different visual substrates.

*Stage 2: apply to Instagram.* Crawled posts hashtagged with brand names, filtering spam, resale posts and official-account posts.

| Data | Size |
|---|---|
| Brands | **56** (29 apparel, 27 beverage) |
| Consumer-created Instagram photos | **114,367** (~2,000 per brand) |
| Firm-created photos (official accounts) | **72,089** (mean 1,360 per brand; 3 beverage brands had no official account) |
| Collection window | May–October 2016 |
| Survey benchmark | Young & Rubicam **BAV**, Q1 2016 |

**Brand metric.** F{j,p} = proportion of brand *j*'s images classified positive on attribute *p*.

**Quantitative findings.**
- Face-validity example: **60.0%** of consumer-posted #Prada images classified glamorous vs **43.1%** for Eddie Bauer; **63.2%** of Eddie Bauer images rugged vs **49.9%** for Prada. Both p < 10⁻⁶.
- Convergent validity, "% of brand pairs ordered consistently" with BAV (chance = 50%): consumer-images-vs-BAV ranged roughly **51%–84%** across attribute × category cells. Best cells: apparel rugged 84%, apparel glamorous 77%. Worst: apparel fun ~51–62%, beverage glamorous ~50–60%.
- Pearson correlations, consumer-image metric vs BAV: from **−0.22 (n.s.)** to **0.803 (p<0.001, beverage healthy)**. Many cells non-significant. Apparel `healthy` was **negative or null**.
- Correlations between **consumer images and firm images were far higher** (mostly 0.4–0.83) than either against the survey.

**Why the last bullet matters more than the headline.** The three data sources measure genuinely different things: firm images = intended positioning; consumer images = how the brand is actually *depicted in use*; BAV = nationally representative *stated* perception. The paper is explicit that divergences are informative, not error — e.g. Fanta clusters as "unhealthy" in BAV (people know it's a soda) but not in image space (people photograph it at parties, in sunlight, with fruit). **A grid tells you how something is being staged, not how it is judged.**

**Limits for our purpose.** Four attributes only. Attributes chosen *a priori* to fit two categories. All U.S. national brands. Nothing about the account owner or the audience. Accuracy of ~80% per image is fine for a 2,000-image brand aggregate and useless for a single post.

## A2. Klostermann, Plumeyer, Böger & Decker **[A]**

**Citation.** Klostermann, J., Plumeyer, A., Böger, D., & Decker, R. (2018). "Extracting brand information from social networks: Integrating image, text, and social tagging data." *International Journal of Research in Marketing*, 35(4), 538–556.

**Method.** Two-step: (1) collect Instagram brand-related **images + caption texts + social tags**; label images with the **Google Cloud Vision API**; **cluster** the labelled images to surface heterogeneous *brand-related situations* (product contents and consumption contexts). (2) **Map** the textual/tag information onto each cluster to build an associative network per cluster — i.e. what people *think and feel* inside each visually-defined situation.

**Core insight (and the one most directly transferable to grid profiling).** Brand-related UGC is *not* homogeneous. Brand associations and sentiment **vary systematically across situation clusters**. The paper names the exact obstacle: images show *situations*, they rarely show *evaluations* — so image data must be fused with text/tags to become interpretable.

**Practical translation.** The right unit of analysis for a grid is not "the account" but **the set of recurring situations the account stages**. That is, empirically, what "content pillars" are trying to be — see Part F1.

**Caveat.** I could not retrieve the exact brand(s) and post counts from open sources (publisher paywalled). Cite the method, not a specific N, until verified.

## A3. Nanne, Antheunis, van der Lee, Postma, Wubben & van Noort **[A/B]**

**Citation.** Nanne, A. J., Antheunis, M. L., van der Lee, C. G., Postma, E. O., Wubben, S., & van Noort, G. (2020). "The Use of Computer Vision to Analyze Brand-Related User Generated Image Content." *Journal of Interactive Marketing*, 50, 156–167.

**Method.** Head-to-head usability comparison of three **off-the-shelf pretrained** vision models — YOLOv2, Google Cloud Vision, Clarifai — on brand-related UGC.

**Findings.** **Google Cloud Vision** is the more accurate object detector; **Clarifai** produces *more useful labels for interpreting brand portrayal* (it emits adjectives, scenes, moods, not just objects); **YOLOv2 was not useful** for this task.

**Why this matters.** It is the cleanest published statement that **detection accuracy and marketing usefulness are different axes**. For profiling a grid, a label vocabulary rich in scene/mood/adjective terms beats a precise object detector.

## A4. Lee & Bradlow — the text-side precedent **[A]**

**Citation.** Lee, T. Y., & Bradlow, E. T. (2011). "Automated Marketing Research Using Online Customer Reviews." *Journal of Marketing Research*, 48(5), 881–894. (Finalist, Paul E. Green Award.)

**Method.** Parse Pros/Cons from online reviews; vectorise sentences; cluster by cosine similarity; k-means to group attributes; produce attribute-level brand positions and a market-structure map. Applied to digital-camera reviews over ~6 years.

**Relevance.** This is the template the whole "visual listening" stream copies: *elicit the attribute space from the consumer's own artefacts rather than imposing the manufacturer's attribute list, then position brands in it.* The design principle transfers directly to grids: **derive the pillar taxonomy from the account's own posts; do not impose a pre-baked category list.**

**Documented limitation of the family.** Liu et al. note that text mining of UGC recovers mostly *functional* attributes (power, mileage, "an oral-care product that whitens"). Images are where the *non-functional / situational / identity* attributes live. Text and image are complements, not substitutes.

---

# PART B — Image content and demand / engagement

## B1. Li & Xie — "Is a Picture Worth a Thousand Words?" **[A]**

**Citation.** Li, Y., & Xie, Y. (2020). *Journal of Marketing Research*, 57(1), 1–19.

**Method.** Three observational datasets of brand-related social posts: two Twitter (airlines; SUVs) and one Instagram. Image features measured with **Google Cloud Vision plus manual coding**: picture quality (theme clarity, composition, lighting, resolution), photo source (professional / amateur / screenshot), human-face presence, colourfulness, and image–text fit. Crucially they **correct for selection into posting an image** (an account chooses whether to attach an image) via matching/selection correction — most agency "studies" of this question do not, which is why their effect sizes are inflated.

**Quantitative findings.**
- **Mere-presence effect (Twitter).** Including an image raises **retweets by ~119%** (air travel) and **~213%** (SUVs); **likes by ~87%** (air travel) and **~151%** (SUVs).
- **Picture quality / professionalism.** High-quality, professionally shot images raise engagement **consistently on both platforms and both categories.** This is the single most robust image finding in the JMR paper.
- **Colourfulness.** Effect **varies by product category** — no universal "more colourful is better."
- **Human faces** and **image–text fit** raise engagement **on Twitter but not on Instagram.**
- **Linked images underperformed text-only posts** (i.e. the image must be native, not a link).

**The Instagram null results are the important part.** Faces and caption–image congruence help on Twitter, where images are scarce, and do *not* help on Instagram, where images are the medium. This is a **visual-saturation / baseline-expectation effect**: on Instagram an image is not a signal, it is the floor. Any framework that ports Twitter/Facebook image heuristics to Instagram is making an error this paper already documented.

## B2. Hartmann, Heitmann, Schamp & Netzer — "The Power of Brand Selfies" **[A]**

**Citation.** Hartmann, J., Heitmann, M., Schamp, C., & Netzer, O. (2021). *Journal of Marketing Research*, 58(6), 1159–1177.

**Taxonomy (three archetypes of consumer-generated brand imagery).**
1. **Consumer selfie** — consumer's face visible *with* the brand.
2. **Brand selfie** — the consumer is invisible; a hand holds/presents the branded product, first-person point of view.
3. **Packshot** — product alone, no person.

**Method / data.**

| Component | Size |
|---|---|
| Total branded images classified | **258,148** posts |
| Twitter | 214,563 images, 185 brands, Jan 2014 – Dec 2016 |
| Instagram | 43,585 images, same 185 brands, Jun 2011 – Oct 2019 |
| Manual annotation for training | 19,949 images (16,949 Twitter + 3,000 Instagram) |
| Classifier | VGG-16 transfer learning, data augmentation; **>90% holdout accuracy** |
| Display-ad field data | 2,255 campaigns / 622 ads |
| Lab experiments | n = 750 and n = 450 |
| Response inference | trained language models over post replies to infer purchase intent |

**Findings — the key dissociation.**
- **Consumer selfies → more *sender* engagement** (likes, comments).
- **Brand selfies → more *brand* engagement** (expressed purchase intention in replies), on both platforms.
- **Display ads: brand selfies achieved higher click-through than consumer selfies** (reported uplift on the order of ~13%).
- Mechanism, from the lab studies: **self-reference**. The first-person hand-holding-product framing invites the viewer to mentally place themselves in the scene; a stranger's face does not.

*(Directional signs and dataset sizes above are solid. Exact regression coefficients should be checked against the published tables before being quoted — I read them via automated extraction.)*

**Why this is the single most actionable paper here.** It is direct evidence that **likes and purchase intent are driven by different image types**. An account optimised for likes will look different from an account optimised for selling. That difference is *visible in the grid* and is therefore a legitimate, evidence-backed inference: a grid dominated by face-forward creator selfies is optimised for audience-building; a grid dominated by POV product-in-hand shots is optimised for conversion.

## B3. Hartmann et al. — "Comparing automated text classification methods" **[A]**

**Citation.** Hartmann, J., Huppertz, J., Schamp, C., & Heitmann, M. (2019). *International Journal of Research in Marketing*, 36(1), 20–38.

**Method.** Benchmark of **10 approaches** (5 lexicon-based, 5 machine-learning) across **41 social-media datasets**, varying platform, sample size and language.

**Finding.** Across the tasks studied, **random forest or naive Bayes performed best** at recovering human coders' intuition. Off-the-shelf **lexicons underperform** trained classifiers.

**Related.** Hartmann, Heitmann, Siebert & Schamp (2023), "More than a Feeling: Accuracy and Application of Sentiment Analysis," *IJRM*, 40(1), 75–87 — the follow-up specifically on sentiment-tool accuracy. (The prompt conflated the two papers; they are distinct.)

**Transfer to grid profiling.** Caption analysis (Spanish-language, in our case) should use a **trained classifier on your own labelled sample**, not a generic Spanish sentiment lexicon. The 2019 paper's whole point is that lexicon shortcuts lose meaningful accuracy, and the effect is worse in non-English and in short, emoji-heavy, slang-heavy text — exactly Argentine Instagram captions.

## B4. Zhang, Lee, Singh & Srinivasan — Airbnb image analytics **[A]**

**Citation.** Zhang, S., Lee, D., Singh, P. V., & Srinivasan, K. (2022). "What Makes a Good Image? Airbnb Demand Analytics Leveraging Interpretable Image Features." *Management Science*, 68(8), 5644–5666. (Earlier version: "How Much Is an Image Worth?")

**Method.** Panel of **7,423 Airbnb properties over 16 months**; **difference-in-differences** around Airbnb's free professional-photography programme (a plausibly exogenous shock to image quality). Deep learning classified image quality across **>510,000 photos**. They then defined **12 human-interpretable image attributes** across three artistic dimensions: **composition, colour, figure-ground relationship**.

**Findings.**
- Properties with **verified (professional) images had 8.98% higher occupancy**.
- **58.83%** of that effect is attributable to the *high image quality* of verified photos (the rest being the verification badge / signalling itself).
- Value of verified photos estimated in the **thousands of dollars per property per year**.
- Most of the 12 interpretable attributes correlated significantly with demand in theoretically predicted directions.

**Why this is the strongest causal evidence in the visual-marketing literature.** The DiD around a free-photography rollout is a much cleaner identification than anything in the social-media engagement literature.

## B5. Zhang, Mehta, Singh & Srinivasan — the counter-result **[C, forthcoming]**

**Citation.** Zhang, S., Mehta, N., Singh, P. V., & Srinivasan, K. (2023/2024). "Do Lower-Quality Images Lead to Higher Demand on Airbnb?" SSRN 4588974; accepted at *Marketing Science*.

**Method.** One-year panel, **958 Manhattan properties**; structural model of the host's image-quality choice.

**Finding.** High-quality images create a **trade-off**: they attract more guests now, but if the property does not live up to the image, guests leave bad reviews or no reviews, damaging future demand. **Counterfactual: Airbnb could raise profits by up to 18.9%** by offering *medium*-quality images, letting hosts match image quality to actual property quality.

**Read this next to B4 and B1.** "Professional photos increase engagement/demand" is true *conditional on the underlying offer matching the image*. **Aesthetic quality is a promise.** When profiling a grid, a highly polished feed attached to a modest operation is not simply "good marketing" — the literature says it is a mismatch that costs the account later. This is a genuine, published, empirically-grounded correction to the "just make it look nicer" folklore.

## B6. Philp, Jacobson & Pancer — food marketing on Instagram **[B]**

**Citation.** Philp, M., Jacobson, J., & Pancer, E. (2022). "Predicting social media engagement with computer vision: An examination of food marketing on Instagram." *Journal of Business Research*, 149, 736–747.

**Method.** Google Vision AI over restaurant Instagram posts; used the model's **confidence score on the food object as a proxy for food typicality**.

**Finding (counter-intuitive, and important).** **The more *typical* a food appears, the more engagement it receives** — contradicting the "Instagrammable = elaborate/novel" industry orthodoxy. Higher classifier confidence ⇒ higher engagement.

**Mechanism (my read, not theirs).** Classifier confidence is a machine-readable proxy for **processing fluency**. Fluency is one of the best-replicated effects in consumer psychology; "novelty" is not.

## B7. Visual complexity and brand status **[A, very recent — verify]**

**Citation (partial).** "How visual complexity signals brand status," *Journal of the Academy of Marketing Science* (2026), DOI 10.1007/s11747-026-01178-w. **I could not retrieve the author list** — verify before citing.

**Method/data.** Analysis of **>400,000 visuals**, plus process evidence.

**Findings.**
- **Edge complexity** (edge density and irregularity) has a **U-shaped** effect on perceived brand status.
- **Colour complexity** (hue quantity and dissimilarity) **monotonically reduces** perceived brand status.
- Both operate **sequentially through perceived visual curation → perceived exclusivity**.

**Practical translation, and the most defensible visual price-positioning signal available.** *Fewer distinct hues across a grid ⇒ higher perceived status/price tier.* This is a measurable, cheap, replicated-at-scale signal — count distinct dominant hues per post and across the grid (e.g. k-means on downsampled pixels; see D3). It is far better grounded than any "colour psychology" claim about what individual hues *mean*.

**Related:** "Visual complexity, brand gender, and ad effectiveness," *IJRM* (2024) — complexity effects are moderated by brand gender positioning.

---

# PART C — Visual elicitation and psychographics

## C1. Dzyabura & Peres — "Visual Elicitation of Brand Perception" **[A]**

**Citation.** Dzyabura, D., & Peres, R. (2021). *Journal of Marketing*, 85(4), 44–66. (MSI Report 19-132.)

**Method.** A **Brand Visual Elicitation Platform (B-VEP)**: respondents build an online **collage** for a brand by dragging photos from a repository of **tens of thousands** of images (free browsing plus keyword search, with certain brand-related search terms banned to prevent respondents simply retrieving the brand's own marketing). Then:
1. Tag every photo with **Clarifai** ("general 1.3"), a CNN over **>11,000 semantic tags** covering objects, scenery, actions, emotions and adjectives; top 20 tags per photo.
2. **Word embeddings** over the tags to seed topics.
3. **Guided LDA** (semi-supervised LDA) over collage-level tag documents → **150 interpretable brand associations**.
4. Regress respondent-level brand ratings on the collage's association distribution.

**Data.**

| Item | Value |
|---|---|
| Collages | **4,743** |
| Respondents | **1,851** |
| Brands | **303** large U.S. brands, across categories (e.g. beauty, cars, household cleaning 19 brands, 16 brands in another category) |
| Associations extracted | **150** |
| Mean photos per collage | **11.45** |
| Mean time per collage | ~8 minutes |
| Self-rated difficulty | 2.5 / 5 |
| Search behaviour | 17.5% of collages used no search at all; median 5 search terms, mean 6.4; of 25,262 search terms only 1,111 (<5%) attempted banned words |
| Brand-rating survey | 49 items = Aaker (1997) brand personality + BAV equity pillars |
| Regression | 3,937 observations, 150 regressors, per characteristic |

**Validation.**
- Correlation between their in-house brand ratings and **actual BAV 2016–17 scores: r = 0.58 (p < .05)** — respectable given different format, population and year.
- A median-split on search-term usage produced association sets **not significantly different from a random split**, i.e. the search tool did not bias the elicited associations.

**Findings that map visuals → psychographics (this is the closest thing in the literature to a validated visual→psychographic bridge).**
- **`glamorous`** (Aaker sophistication/upper-class facet) is positively associated with *wedding, eye, fashion, glamour*; negatively with *heavy vehicles, construction, patriotism*.
- **`rugged`** (Aaker ruggedness) is positively associated with *heavy vehicle, military, bicycle, industry, desert*; negatively with *therapy, church, candy, arts and crafts, sparkling*.
- **`innovative`** (BAV differentiation pillar): positively *hand, religion, painting, cityscape, light*; negatively *patriotism, chest, ruin, symbol, cowboy*.
- **Price/quality tier is visible in association space.** Regressing perceived "high quality" on associations, within **cars**: *alcoholic drink, cityscape, house, fashion, suit* load **positively**; *music festival, healthy cooking, breakfast, rain, dance, ruin* load **negatively**. The luxury car brands (Audi, Lamborghini, Porsche, Mercedes-Benz) are exactly the ones whose collages contain expensive alcohol, mansions and Riviera vacations.
- **Association valence is category-specific.** *breakfast* and *healthy cooking* are negative for cars and positive in food — **there is no universal lexicon of "premium visuals."** Any archetype/aesthetic mapping must be built per category.
- Application: **prototypical collages** generated by cosine similarity between a brand's association distribution and the repository (demonstrated for Axe, Degree, Secret).

**Two caveats the authors flag.** The respondent sample is **not nationally representative** (screened for brand familiarity), and this is an *elicitation instrument* — it measures perceptions of brands people already know, not profiles of unknown accounts.

## C2. Image Analytics in Marketing — the survey **[A]**

**Citation.** Dzyabura, D., El Kihal, S., & Peres, R. (2022). "Image Analytics in Marketing." In *Handbook of Market Research*, Springer, pp. 665–692.

The best single entry point to the field. Establishes the taxonomy of image-analytics tasks in marketing (classification, feature extraction, elicitation, generation) and the recurring caution that **interpretable features and predictive features are different objects** — a theme visible in A1 (SVM interpretable vs ConvNet accurate), A3 (Google accurate vs Clarifai interpretable) and C1 (tags chosen *because* interpretable).

---

# PART D — Inferring the *person / audience*, not the brand

This is the thinnest and most hazardous part of the literature, and the part practitioner tools most aggressively oversell.

## D1. Gender inference from a user's images **[C]**

**Citation.** arXiv:1810.04531, "Inferring User Gender from User Generated Visual Content on a Deep Semantic Space."

**Method.** Classify a user's *binary* gender from a small set of images from their Instagram profile, on a deep semantic embedding; single- and multiple-instance learning classifiers.

**Finding.** Precision **>0.825** for gender detection, language-independent.

**Related.** A CNN on Instagram *profile pictures* alone reports **70.11%** accuracy (IEEE, 2020). Multimodal architectures for joint age/gender/organisation-status inference across 32 languages exist (arXiv:1905.05961).

**Read the numbers honestly.** ~0.83 precision on a **binary** target from a *whole profile* is far weaker than it sounds when the actual business question is "who is this account's *audience*." And gender is the *easiest* of these targets. Age, income and social class inference from images is materially worse and I found no peer-reviewed marketing paper validating income inference from Instagram content.

## D2. Demographic disparities in deployed vision models **[C — but the most important caution here]**

**Citation.** arXiv:2403.19717, "A Picture is Worth 500 Labels: A Case Study of Demographic Disparities in Local Machine Learning Models for Instagram and TikTok."

**Method.** Reverse-engineered the on-device ML pipelines shipped inside the Instagram and TikTok apps (ML task detection → pipeline reconstruction → performance assessment).

**Findings.**
- **TikTok:** measurable **errors in age and gender prediction, worst for minors and for Black individuals**.
- **Instagram:** demographic disparities in the extraction of **>500 visual concepts**, with **spurious correlations between demographic features and specific concepts**.

**Implication for any grid-profiling system.** Off-the-shelf vision labels are **not demographically neutral**. Labels co-vary with skin tone, age and setting in ways that are not the thing you meant to measure. If a profiling pipeline outputs "target demographic," a meaningful share of that signal may be model bias re-branded as insight. Treat any automated demographic output as a hypothesis for human verification, never as a field in a CRM.

## D3. Cross-country Instagram colour/sentiment/structure — includes Argentina **[C]**

**Citation.** Konka, R., & Kurani, P. (2025). "Color, Sentiment, and Structure: A Comparative Study of Instagram Marketing Across Economies." arXiv:2512.18310. *Not peer-reviewed; undergraduate-level engineering preprint; treat as descriptive only.*

**Method.** CrowdTangle API, official Instagram accounts of **7 global F&B brands** (Starbucks, Burger King, McDonald's, Domino's, Pizza Hut, KFC, Subway) across **21 countries** split developed/developing. **Argentina, Brazil, Mexico** are in the developing set (alongside India, Saudi Arabia, Egypt, Turkey, Malaysia, UAE, Indonesia, South Korea). Sentiment via a HuggingFace classifier on captions; dominant colour via **k-means (k=5) on downsampled RGB pixels**, aggregated to per-outlet colour bands; then OLS of likes/comments/views on log-population, log-GDP and adult obesity rate, stratified by development status.

**Findings.**
- Engagement patterns **differ significantly by development status** for some brands (ANOVA p ≈ 0.026 Starbucks, p ≈ 0.049 Pizza Hut; n.s. for McDonald's, KFC).
- In **developing** markets, certain colour combinations (off-white + green) associate with higher interaction, and **GDP is a positive predictor** of engagement.
- In **developed** markets, larger population raises engagement while **higher GDP correlates with *reduced*** engagement.
- Obesity rate has mixed effects (raising likes in some regions, lowering comments in others).
- Positive caption sentiment dominates everywhere; neutral sentiment is rare.

**Verdict.** The country-level regressions are ecological (n = countries, post-level DV, no fixed effects) and I would not trust the coefficients. **The reusable part is the method**: k-means dominant-colour extraction per post, aggregated to a per-account palette, is a cheap and legitimate way to characterise a grid's aesthetic — and it is the same operationalisation used in the (much better identified) brand-status work in B7.

---

# PART E — Influencer / creator profiling from the grid

## E1. Argyris, Wang, Kim & Yin — visual congruence **[B, high-quality]**

**Citation.** Argyris, Y. A., Wang, Z., Kim, Y., & Yin, Z. (2020). "The effects of visual congruence on increasing consumers' brand engagement: An empirical investigation of influencer marketing on Instagram using deep-learning algorithms for automatic image classification." *Computers in Human Behavior*, 112, 106443.

**Method.** In-vivo observation, **>45,000 images** plus social-media usage behaviour over **26 months**; deep-learning classification of every image; analysis of visual elements ↔ brand engagement.

**Findings.**
- **Visual congruence between influencer and follower content increases followers' engagement with the influencer's posts.**
- That increase **in turn** raises followers' engagement with the **endorsed brand**.
- **Affiliation (perceived similarity/bond) mediates** both relationships.
- Framework proposed: **Visual-Congruence-induced Social Influence (VCSI)**, a contextualisation of the Similarity-Attraction Model.

**Why this legitimises "aesthetic coherence" as a construct — with an important twist.** The academically supported version of "aesthetic coherence" is *congruence with the audience's own visual world*, not internal prettiness of the grid. Coherence matters because it signals **shared interests / homophily**, not because symmetry is pleasing. A grid that is internally immaculate but visually alien to its followers is *not* what this paper found to work.

## E2. Decoding influencer marketing effectiveness **[B]**

**Citation.** (2025). "Decoding influencer marketing effectiveness on Instagram: Insights from image, text, and influencer features." *Journal of Retailing and Consumer Services*, 85, 104285.

**Method.** Predict sponsored-post popularity from **four feature sets**: image *visual* features, image *topic* features, text *topic* features, and *influencer* features.

**Finding.** Best predictive performance comes from **combining all four**; each block adds incremental signal.

**Translation.** A defensible creator/account profile is a **four-block feature vector** — low-level visual style, image topics, caption topics, account-level attributes (followers, cadence, category). This is the closest thing in the literature to a published, validated schema for "profiling an Instagram account."

## E3. Sponsored-post detection **[C]**

**Citation.** arXiv:2011.05757, "Characterising and Detecting Sponsored Influencer Posts on Instagram." Relevant to inferring **commercial intent** from a grid — sponsorship leaves detectable textual and visual regularities.

---

# PART F — Practitioner frameworks: an evidence audit

**Blunt summary up front.** Of the four canonical practitioner frameworks below, **one (content pillars) is a reasonable operationalisation of something the peer-reviewed literature independently found**; **one (brand archetypes) is unfalsifiable but useful as a shared vocabulary**; **one (hue-level colour psychology) is largely refuted or unsupported at the level marketers use it**; and **one (VALS/PRIZM-style psychographic segmentation) has been criticised for weak predictive validity for decades, including by its own field.**

## F1. Content pillars **[D — but with a real [A] cousin]**

**What it is.** Choose 3–5 recurring themes/content types; every post belongs to one; the grid is a mix across them. Promoted by Sprout Social, Hootsuite, Later, Mailchimp, Sendible, Planable, Socialinsider et al.

**Provenance.** No identifiable originator. It is agency convention, not a research construct. The "pillars/Greek temple" metaphor is decoration.

**Evidence.** No controlled evidence that having named pillars causes better outcomes. The claimed benefits (consistency, SEO, loyalty, conversions) are asserted, not measured, in every practitioner source I read.

**But — the underlying object is real.** Klostermann et al. (A2) found empirically that brand-related UGC clusters into **heterogeneous brand-related situations** with **systematically different associations and sentiment**. That is a content-pillar structure, discovered bottom-up from data rather than asserted top-down. And Lee & Bradlow (A4) is the methodological argument for deriving the taxonomy from the artefacts rather than imposing it.

**Correct use.** Do not ask "what are this account's pillars?" as if the answer were a fixed list of five nouns from a blog post. **Cluster the account's actual posts and report the clusters, their share of posts, and their differential engagement.** That is a defensible measurement. The named-pillar version is a planning heuristic for the account owner, not an analytic finding about them.

## F2. Brand archetypes — Jung / Mark & Pearson **[D, bordering on E]**

**Citation.** Mark, M., & Pearson, C. S. (2001). *The Hero and the Outlaw: Building Extraordinary Brands Through the Power of Archetypes.* McGraw-Hill.

**The framework.** Twelve archetypes — Innocent, Sage, Explorer, Hero, Outlaw, Magician, Everyman, Lover, Jester, Caregiver, Creator, Ruler — organised by four motivations: **independence, mastery, belonging, stability**.

**Evidence audit.**
- **Jung's archetypes have long been criticised as difficult to test and short on empirical support.** The brand adaptation inherits that.
- The construct is **applied post hoc**, essentially never predicted in advance and then tested.
- The academic literature on brand archetypes is **dominated by conceptual and theoretical work; empirical research is limited** (see e.g. "Exploring the changing role of brand archetypes in customer–brand relationships," *Business Horizons*, 2023).
- **The falsifiability problem is fatal to any scientific claim:** if archetypes are universal patterns in an inherited unconscious, no observation can disconfirm them. Practitioner critics have called it *"pseudoscience — ideas dressed in scientific language without the empirical backing to match."*

**Contrast with the validated alternative.** Where archetypes are unfalsifiable, **Aaker's (1997) brand personality scale** — five factors: sincerity, excitement, competence, sophistication, ruggedness — is a psychometrically developed, widely replicated instrument, and Dzyabura & Peres (C1) empirically link **specific visual associations to specific Aaker traits**. If you want a defensible personality read on a grid, **use Aaker's dimensions with C1's visual-association mappings, not the 12 archetypes.**

**Where archetypes are still fine.** As a **generative and consistency heuristic** — a shared vocabulary for keeping an identity coherent across contributors. That is a real organisational benefit. It is not a measurement.

## F3. Colour psychology in branding **[E — mostly]**

**What has real support.**
- **Labrecque, L. I., & Milne, G. R. (2012). "Exciting red and competent blue: the importance of color in marketing." *Journal of the Academy of Marketing Science*, 40(5), 711–727.** Controlled studies mapping hue to brand-personality dimensions: red does associate with excitement, blue with competence/reliability. **Critically, they show hue alone is a blunt instrument — saturation and value amplify or mute the personality signal.**
- **Labrecque, Patrick & Milne (2013). "The Marketers' Prismatic Palette: A Review of Color Research and Future Directions." *Psychology & Marketing*, 30(2), 187–202.** The field's own review.
- **Labrecque & Milne (2013), "To be or not to be different"** — colour *differentiation* within a category carries information.
- **Elliot & Maier's review** in psychology: colour effects on behaviour are **context-dependent**, varying with saturation, brightness, product category and culture.
- **B7 above (JAMS 2026)** — *colour complexity* (number and dissimilarity of hues) reliably reduces perceived brand status across >400,000 visuals. This is a **structural** colour finding, and it is much stronger than any hue-meaning finding.

**What does not have support, and is repeated constantly.**
- **"Blue = trust, red = urgency, green = nature"** as a decision rule. People do form colour–emotion associations, measurably and somewhat cross-culturally; what is missing is reliable evidence that **choosing the "right" hue changes purchase behaviour**.
- **"85% of buyers choose primarily because of colour."** This statistic is **weakly sourced** — traceable to secondary 1990s/2006 references, not to any controlled buying experiment. **Treat it as folklore.** It appears in a very large fraction of agency material.
- Li & Xie (B1) found the engagement effect of **colourfulness varies by product category**, i.e. no universal direction, even for the simplest colour construct.

**Defensible position for a profiling product.** Do not claim to read *meaning* from hue. Do measure and report **structural colour properties** — palette breadth (number of distinct dominant hues), saturation/value distribution, palette consistency across the grid, and differentiation from category norms. Those are (a) objectively measurable, (b) supported by B7 and Labrecque & Milne's saturation/value result, and (c) genuinely diagnostic of positioning tier.

## F4. VALS, PRIZM and psychographic segmentation **[D/E]**

**VALS.** Developed 1978 by Arnold Mitchell at SRI International. Proprietary. Current form: **8 segments** on two axes — *primary motivation* (ideals, achievement, self-expression) and *resources* (financial, educational, intellectual).

**PRIZM.** "Potential Ratings Index by ZIP Market," Nielsen Claritas. **Geodemographic**, not psychographic in origin: combines consumer expenditure and socio-economic variables with geography to assign neighbourhood-level lifestyle types.

**Evidence audit.**
- **Daniel Yankelovich** — a founder of the field — concluded psychographics are **"very weak"** at predicting purchases and therefore a **"very poor"** tool for corporate decision-makers.
- Psychographic segmentation has **limited usefulness for predicting specific brand behaviour**; despite technical advances in the 1980s–90s, segmenting on needs or feelings **rarely yields segments that can actually be targeted** in practice.
- **VALS is criticised as too culturally specific for international use** — a decisive objection for Argentine application. There is no validated Argentine VALS instrument.
- PRIZM's geodemographic logic is an **ecological inference**: it assigns a neighbourhood's modal profile to every individual in it. That is a known statistical error type, not a subtle one.

**Direct consequence for Instagram profiling.** **Do not map visual signals onto VALS or PRIZM types.** You would be chaining a weakly-validated inference (image → psychographic) onto a weakly-validated framework (psychographic → behaviour), in a country neither framework was built for. The chain compounds error and adds nothing a behavioural segmentation would not give you better.

**What to use instead.** Behavioural and observable segmentation: category, price tier, purchase cadence, geography, business type, commercial intent, posting behaviour. These are directly observable from a grid, are not culture-bound, and predict better.

## F5. Posting cadence **[D, with vendor-data caveats]**

Vendor studies (Buffer: >2M posts / 100k Instagram accounts; Tailwind; Zoomsphere; Socialinsider) consistently report a **positive frequency–growth relationship** on Instagram, a measurable **"no-post penalty"** for accounts that skip a week, and that 3–5 posts/week roughly doubles follower growth rate vs. less, with continued gains at 6–9+.

**Caveats that matter.** These are vendor datasets, non-peer-reviewed, and above all **not causally identified** — the accounts that post more are systematically different (resourced, professional, motivated) from those that post less. Li & Xie (B1) is instructive here precisely because it *does* correct for selection and finds smaller effects than naive comparisons.

**Legitimate use.** Cadence is still one of the **best observable proxies for operational capacity and commercial seriousness** of a business account — see the taxonomy in Part H. That inference does not require the causal claim.

## F6. Engagement metrics as business outcomes **[E]**

Practitioner and academic sources converge on the caution: **likes and follower counts are weak indicators of revenue.** One study on Instagram engagement metrics and corporate revenue growth (*Information*, MDPI, 2025, 16(4), 287) found only a moderate, statistically insufficient correlation between a "loyalty rate" metric and turnover, with follower count showing a stronger relationship than engagement rate. Hartmann et al. (B2) is the sharper statement of the same point: **the image types that maximise likes are not the image types that maximise purchase intent.**

---

# PART G — LATAM / Argentine / Spanish-language

The peer-reviewed evidence base here is **thin**. What exists:

**G1. Quiroz Cedeño, I. V., Loor Carvajal, G. I., & Beltrán Cedeño, R. A. (2022).** "Instagram y su incidencia en la comercialización de empresas registradas en directorios digitales en la ciudad de Portoviejo." *ECA Sinergia*, 13(1), 112–129. **[B]**
- **Method:** quantitative online survey, random probability sampling; **n = 42** businesses drawn from a population of 180 in a digital directory. Ecuador, not Argentina.
- **Findings:** **100%** said Instagram aided commercialisation; **95%** reported increased sales volume attributable to Instagram; **84%** treat Instagram as a priority sales channel; **41%** rated Stories the most effective format, **36%** consistent feed posts; sample skewed to owners aged 26–30; **46%** food & beverage, **17%** health/spa.
- **Caveat:** self-reported, tiny n, no control group, directory-listed (hence already digitally active) firms. Directionally useful, not evidential.

**G2.** "El uso de las redes sociales en las [PyMEs]," *Visión de Negocios*, vol. 2 (2024), Universidad Católica de Santa Fe (Argentina). **[B]** — Argentine SME social-media usage.

**G3.** "Las Redes Sociales y las PyMES. Una relación productiva," *Cuadernos del Centro de Estudios en Diseño y Comunicación*, Universidad de Palermo (Argentina). **[B]**

**G4.** Segmentation of e-consumers, *Cuadernos de Gestión* (Universidad de Lleida + Universidad de Flores, Argentina) — Spanish-language e-consumer segmentation. **[B]**

**G5.** "Instagram como objeto de estudio en investigaciones recientes," *Ámbitos: Revista Internacional de Comunicación* — Spanish-language literature review of Instagram research. **[B]**

**G6. Market context (non-academic, [D]).** Argentina is reported as the **third-largest Instagram market in Latin America** with ~**30.5 million** users; ~**90%** of Argentines access social platforms monthly, averaging ~**44 hours/month**. Instagram functions as the primary *vidriera* (shop window) for small-business commerce, largely because SMEs lack budget for paid campaigns.

**Assessment.** There is **no published, validated Argentine or Spanish-language visual-segmentation instrument for Instagram.** Every image-mining paper in Part A is trained on English-language, U.S.-brand, Flickr/Instagram data. Two concrete transfer risks:
1. **Caption NLP.** Hartmann et al. (B3) already show lexicon methods underperform trained classifiers; Argentine Spanish (voseo, lunfardo, heavy emoji, regional slang) makes generic Spanish sentiment tools worse still. **Label your own sample.**
2. **Visual attribute semantics.** Dzyabura & Peres (C1) demonstrated association valence flips across *categories* within one country. Assuming it holds across *cultures* is unjustified. Any "glamorous / rugged / premium" visual scoring needs local recalibration before it means anything.

---

# PART H — Small-business B2B prospecting via Instagram

**Evidence status: [D] throughout.** I found **no peer-reviewed study** of Instagram as a B2B prospecting channel. The published social-selling literature is LinkedIn-centric. What circulates is vendor material with unverifiable numbers: "78% of businesses using social selling outperform those that don't" (LinkedIn's own figure), "DM response rates of 15–20%," "over 90% of Instagram users follow at least one business." Treat all of these as marketing claims.

**What *is* defensible, from the peer-reviewed literature above:** a public business grid emits genuine, machine-readable signals about **category, price tier, operational capacity, commercial intent and current marketing sophistication**. That makes Instagram a legitimate **qualification and personalisation** surface even though its efficacy as a *channel* is unstudied. See the taxonomy in Part I.

## Legal and ethical constraints (non-optional)

- **"Public" ≠ "consented."** Under GDPR, public availability is **not itself a lawful basis**. A scraper processing EU residents' data is a **data controller**. Legitimate interest can work for B2B prospecting, but requires a **documented three-part balancing test** (interest / necessity / balance), and **Art. 14 notification** to the data subject — normally within one month of obtaining the data — because it was not collected from them directly.
- **Argentina: Ley 25.326 (Protección de los Datos Personales).** Requires **free, express and informed consent**, plus data accuracy and purpose limitation, and processing without a lawful basis is unlawful. The law is old (2000) and does not carve out B2B clearly; reform has been under discussion. **Data on a natural person remains personal data even when it is a business account** — critical in Argentina, where a large share of SME accounts are sole traders posting under their own name and face.
- **Platform Terms of Service** are a separate matter from data-protection law; Instagram's ToS restrict automated collection regardless of the legal basis.
- **Practical stance:** collect **firmographic** signals (category, price tier, city, cadence, commercial intent), not **personal** ones (inferred age, gender, ethnicity, household income, relationship status). The firmographic set is what actually improves prospecting, it is far more defensible legally, and per D2 the personal set is unreliable anyway.

---

# PART I — Practical taxonomy: what a public Instagram grid legitimately supports

Confidence key: **High** = supported by [A] evidence and directly observable; **Medium** = observable but inference requires assumption or local calibration; **Low** = weak evidence, high error rate, use only as a flagged hypothesis; **Do not** = not supportable.

## I.1 — Inferences about the ACCOUNT / BUSINESS

| # | Inference | Observable evidence in the grid | Confidence | Grounding | How it fails |
|---|---|---|---|---|---|
| 1 | **Product / service categories** | Object labels from a vision API across posts; recurring objects; caption nouns; profile category field; link-in-bio | **High** | A3 (Google CV accurate at objects); A2 | Multi-category retailers; reposted supplier content; heavy meme/quote content masks the product |
| 2 | **Content pillars (recurring situations)** | Unsupervised clustering of image labels + caption topics over the last 60–90 posts; report cluster share-of-posts | **High** | A2 (situations vary systematically); A4 (derive, don't impose); E2 (image topics + text topics as separate blocks) | Fewer than ~30 posts; a single campaign dominating the window; a rebrand mid-window |
| 3 | **Posting cadence & consistency** | Timestamps: posts/week, gaps, longest silence, weekday/hour distribution, burstiness | **High** | Direct measurement; F5 | Stories/Reels invisible in a grid scrape; scheduled batches inflate apparent activity |
| 4 | **Operational capacity / commercial seriousness** | Cadence + production quality + response to comments + presence of shop tags, price captions, contact/WhatsApp CTA, catalogue | **High** | F5 (cadence–growth correlation) + B4 (professional imagery is a costly, meaningful signal) | Agency-run accounts overstate in-house capacity; a dormant account may be a thriving offline business |
| 5 | **Commercial intent (sell vs. build audience)** | Ratio of Hartmann's three image types (brand selfie / consumer selfie / packshot); shoppable tags; price-in-caption; DM-to-order CTAs; sponsored-post markers | **High** | **B2** (the direct dissociation between engagement-optimised and conversion-optimised imagery); E3 | Same person runs both a personal and a shop account; seasonal campaign shifts the mix |
| 6 | **Production quality tier** | Resolution, focus, lighting consistency, composition regularity, professional-vs-amateur classification; presence of studio/flat-lay setups | **High** | **B1** (quality → engagement, robust across platform and category); **B4** (DiD: +8.98% occupancy, 58.83% attributable to quality) | Phone cameras are now very good; templated Canva graphics read as "professional" without any real production capability |
| 7 | **Price positioning / status tier** | **Colour complexity** (count of distinct dominant hues per post and across grid — fewer ⇒ higher status); **edge complexity** (U-shaped); whitespace; category-specific luxury associations | **Medium-High** | **B7** (>400k visuals; colour complexity monotonically ↓ status); **C1** (perceived "high quality" loads on category-specific associations) | Aspirational mismatch (see B5 — polished grid, modest offer); needs **per-category** calibration; luxury cues in Argentina ≠ luxury cues in the U.S. |
| 8 | **Aesthetic style / visual identity** | Per-post k-means dominant-colour palette aggregated across grid; saturation and value distributions; palette stability over time; recurring templates/typography | **Medium-High** | **D3** method; **B7**; Labrecque & Milne (saturation/value matter, not just hue) | Filter and preset trends produce convergent palettes with no shared identity; platform compression alters colour |
| 9 | **Aesthetic coherence** | Within-account variance of palette, composition and topic distribution across recent posts | **Medium** | **E1** — but note the finding is about **congruence with the audience**, not internal tidiness | An immaculate but audience-alien grid scores high and performs badly — the exact case E1 warns about |
| 10 | **Brand personality (Aaker dimensions)** | Map image tags to the visual associations validated in C1 (e.g. *heavy vehicle / military / desert* ⇒ ruggedness; *wedding / fashion / glamour* ⇒ sophistication) | **Medium** | **C1** (validated on 4,743 collages, 303 brands; r = 0.58 vs BAV) | Validated on U.S. brands and on **elicited collages**, not on a business's own feed — different data-generating process. Category-specific valence (C1). Recalibrate locally. |
| 11 | **Brand attributes (glamorous / rugged / healthy / fun)** | Style-transfer CNN classifiers per Liu et al. | **Medium** | **A1** — but note ~79% per-image accuracy, and correlations with survey perception between −0.22 and 0.80 | Meaningful only in **aggregate over hundreds of images and only for relative comparison between accounts**; never for a single post |
| 12 | **Brand archetype (Mark & Pearson 12)** | — | **Do not present as a finding** | **F2** — unfalsifiable, no predictive validation | Use Aaker (row 10) for anything measured. If archetype language is wanted for client-facing copy, label it explicitly as an interpretive frame |
| 13 | **Geography / market served** | Geotags, city names in captions/bio, language variety (voseo, regional slang), local landmarks, currency in price captions, shipping/delivery mentions | **High** | Direct observation | Geotags are sparse and often aspirational; a national brand's account is not local |
| 14 | **Approximate business size** | Follower count × cadence × production quality × staff visible in posts × number of SKUs shown × comment-response behaviour | **Medium** | Composite of the above | Followers are purchasable; B2B firms are systematically small-follower/high-value |
| 15 | **Marketing sophistication / upsell opportunity** | Consistent templates, branded typography, planned grid layout, use of Reels, link-in-bio tooling, UGC reposting, campaign structure | **Medium** | Composite | The signal for "does this business need help" is precisely the *absence* of the above — which is also the signal for "cannot pay" |

## I.2 — Inferences about the ACCOUNT'S AUDIENCE

**This entire block is materially weaker than I.1 and should be presented as hypotheses, never as data.**

| # | Inference | Observable evidence | Confidence | Grounding | How it fails |
|---|---|---|---|---|---|
| 16 | **Target demographic the account is *addressing*** | Who appears in the account's own imagery (age, apparent gender, setting); language register; price points shown; cultural references | **Medium** | Distinguish sharply from row 17 — this is about the account's *intent*, which is genuinely encoded in its output | Aspirational casting: brands photograph who they want, not who buys |
| 17 | **Actual audience composition** | Commenter names/photos; follower sample | **Low** | D1 (~0.83 precision for **binary gender** from a whole profile — the *easiest* target) | **D2**: deployed vision models show demographic disparities and spurious concept–demographic correlations, worst for minors and Black individuals. Commenters ≠ followers ≠ customers. **Do not put this in a CRM field.** |
| 18 | **Audience income / social class** | — | **Do not** | No peer-reviewed marketing validation found for income inference from Instagram content | High error, high harm, likely unlawful under both GDPR and Ley 25.326 for a natural person |
| 19 | **Audience psychographic type (VALS/PRIZM)** | — | **Do not** | **F4** — weak predictive validity (Yankelovich), culturally specific to the U.S., PRIZM is an ecological inference | Chaining a weak inference onto a weak framework in a country neither was built for |
| 20 | **Audience–creator affinity / homophily** | Visual congruence between the account's imagery and its commenters' visible content | **Medium** | **E1** (>45k images, 26 months; affiliation mediates) | Requires access to follower content; expensive; privacy-sensitive |
| 21 | **Engagement quality** | Comment:like ratio; saves/shares if available; comment text substance vs emoji-only; repeat commenters | **Medium** | **B2** (engagement type ≠ commercial value); **F6** | Engagement pods, bots, giveaway spikes. A study of 3.5M Instagram accounts found repeat engagement by the same individual on one post is rare — so raw counts are near-unique-user counts |

## I.3 — Operating rules for anyone building this

1. **Aggregate, never single-post.** Every accuracy figure in Part A (65–85% per image) is only tolerable because it is averaged over ~2,000 images per brand. A profile built on 12 posts is noise. **Minimum ~30 posts; prefer 60–90.**
2. **Relative, never absolute.** Liu et al. validate by *ordering brand pairs*, not by absolute scores. Report "more premium-coded than 80% of comparable accounts in this category," never "premium score: 7.2."
3. **Calibrate per category.** C1 proves association valence flips across categories in a single country. Build category baselines before scoring anything.
4. **Calibrate per locale.** Every core model is trained on U.S./English data. Argentine recalibration is required before claiming meaning, not optional polish.
5. **Choose interpretable features where a human will read the output.** A1, A3 and C1 all independently make this trade-off explicitly.
6. **Fuse image + text + account metadata.** E2's central finding; A2's central method. Image-only profiling leaves signal on the table.
7. **Label evidence tiers in the output itself.** A profile that mixes "posts 4×/week" (measured) with "Explorer archetype" (interpretive) without marking the difference is misleading its own user.
8. **Firmographic over personal.** Better legally, better ethically, and — per D2 — better empirically.

---

# PART J — Bibliography

**Tier A — peer-reviewed, top-tier**
1. Liu, L., Dzyabura, D., & Mizik, N. (2020). Visual Listening In: Extracting Brand Image Portrayed on Social Media. *Marketing Science*, 39(4), 669–686. DOI 10.1287/mksc.2020.1226
2. Klostermann, J., Plumeyer, A., Böger, D., & Decker, R. (2018). Extracting brand information from social networks: Integrating image, text, and social tagging data. *IJRM*, 35(4), 538–556.
3. Li, Y., & Xie, Y. (2020). Is a Picture Worth a Thousand Words? An Empirical Study of Image Content and Social Media Engagement. *JMR*, 57(1), 1–19. DOI 10.1177/0022243719881113
4. Hartmann, J., Heitmann, M., Schamp, C., & Netzer, O. (2021). The Power of Brand Selfies. *JMR*, 58(6), 1159–1177. DOI 10.1177/00222437211037258
5. Hartmann, J., Huppertz, J., Schamp, C., & Heitmann, M. (2019). Comparing automated text classification methods. *IJRM*, 36(1), 20–38.
6. Hartmann, J., Heitmann, M., Siebert, C., & Schamp, C. (2023). More than a Feeling: Accuracy and Application of Sentiment Analysis. *IJRM*, 40(1), 75–87.
7. Dzyabura, D., & Peres, R. (2021). Visual Elicitation of Brand Perception. *Journal of Marketing*, 85(4), 44–66. DOI 10.1177/0022242921996661
8. Zhang, S., Lee, D., Singh, P. V., & Srinivasan, K. (2022). What Makes a Good Image? Airbnb Demand Analytics Leveraging Interpretable Image Features. *Management Science*, 68(8), 5644–5666.
9. Lee, T. Y., & Bradlow, E. T. (2011). Automated Marketing Research Using Online Customer Reviews. *JMR*, 48(5), 881–894.
10. Nanne, A. J., Antheunis, M. L., van der Lee, C. G., Postma, E. O., Wubben, S., & van Noort, G. (2020). The Use of Computer Vision to Analyze Brand-Related User Generated Image Content. *JIM*, 50, 156–167.
11. Labrecque, L. I., & Milne, G. R. (2012). Exciting red and competent blue: the importance of color in marketing. *JAMS*, 40(5), 711–727.
12. Labrecque, L. I., Patrick, V. M., & Milne, G. R. (2013). The Marketers' Prismatic Palette: A Review of Color Research and Future Directions. *Psychology & Marketing*, 30(2), 187–202.
13. Aaker, J. L. (1997). Dimensions of Brand Personality. *JMR*, 34(3), 347–356.
14. (2026). How visual complexity signals brand status. *JAMS*. DOI 10.1007/s11747-026-01178-w — **author list unverified**
15. (2024). Visual complexity, brand gender, and ad effectiveness. *IJRM*.
16. Dzyabura, D., El Kihal, S., & Peres, R. (2022). Image Analytics in Marketing. *Handbook of Market Research*, Springer, 665–692.

**Tier B — peer-reviewed, applied**
17. Argyris, Y. A., Wang, Z., Kim, Y., & Yin, Z. (2020). The effects of visual congruence on increasing consumers' brand engagement. *Computers in Human Behavior*, 112, 106443.
18. Philp, M., Jacobson, J., & Pancer, E. (2022). Predicting social media engagement with computer vision: An examination of food marketing on Instagram. *JBR*, 149, 736–747.
19. (2025). Decoding influencer marketing effectiveness on Instagram: Insights from image, text, and influencer features. *Journal of Retailing and Consumer Services*, 85, 104285.
20. (2023). Visual strategies of luxury and fast fashion brands on Instagram and their effects on user engagement. *JRCS*.
21. (2018). Visual communication of luxury fashion brands on social media: effects of visual complexity and brand familiarity. *Journal of Brand Management*.
22. Quiroz Cedeño, I. V., Loor Carvajal, G. I., & Beltrán Cedeño, R. A. (2022). Instagram y su incidencia en la comercialización de empresas registradas en directorios digitales en la ciudad de Portoviejo. *ECA Sinergia*, 13(1), 112–129.
23. (2024). El uso de las redes sociales en las PyMEs. *Visión de Negocios*, vol. 2, UCSF (Argentina).
24. Las Redes Sociales y las PyMES. Una relación productiva. *Cuadernos del Centro de Estudios en Diseño y Comunicación*, Universidad de Palermo.
25. (2025). Evaluating the Impact of Instagram Engagement Metrics on Corporate Revenue Growth: Introducing the Loyalty Rate. *Information* (MDPI), 16(4), 287.
26. (2023). Exploring the changing role of brand archetypes in customer–brand relationships. *Business Horizons*.
27. (2025). Multiple engagement by an individual on a social media post is rare: 3.5 million Instagram user accounts and 29 user interviews.

**Tier C — preprints / working papers**
28. Zhang, S., Mehta, N., Singh, P. V., & Srinivasan, K. (2023). Do Lower-Quality Images Lead to Higher Demand on Airbnb? SSRN 4588974 (accepted, *Marketing Science*).
29. arXiv:1810.04531 — Inferring User Gender from User Generated Visual Content on a Deep Semantic Space.
30. arXiv:2403.19717 — A Picture is Worth 500 Labels: Demographic Disparities in Local ML Models for Instagram and TikTok.
31. arXiv:1905.05961 — Demographic Inference and Representative Population Estimates from Multilingual Social Media Data.
32. arXiv:2011.05757 — Characterising and Detecting Sponsored Influencer Posts on Instagram.
33. Konka, R., & Kurani, P. (2025). Color, Sentiment, and Structure: A Comparative Study of Instagram Marketing Across Economies. arXiv:2512.18310.

**Tier D — practitioner**
34. Mark, M., & Pearson, C. S. (2001). *The Hero and the Outlaw*. McGraw-Hill.
35. VALS — SRI International / Strategic Business Insights (proprietary, 1978–).
36. PRIZM — Nielsen Claritas (proprietary).
37. Content-pillar guidance: Sprout Social, Hootsuite, Later, Mailchimp, Sendible, Socialinsider, Planable (various, no primary evidence).
38. Cadence benchmarks: Buffer (2M+ posts / 100k Instagram accounts), Tailwind, Zoomsphere (vendor data, non-causal).

---

# PART K — The five things worth remembering

1. **The literature validates reading the *staging*, not the *stager*.** Every top-tier paper measures what an image portrays about a brand. None validates inferring who owns or follows an account. Sell the first; flag the second as hypothesis.
2. **Hartmann et al. (B2) is the most commercially useful finding in the whole corpus.** Face-forward selfies buy likes; POV product-in-hand shots buy purchase intent; the two goals are visibly different in a grid. This is a real, published, 258k-post dissociation — and it is a diagnosis most account owners cannot make about themselves.
3. **Structural colour beats hue meaning.** "Blue = trust" is folklore. "Fewer distinct hues ⇒ higher perceived status, across 400,000 visuals" is evidence. Measure palette breadth, saturation and value; do not narrate hue symbolism.
4. **Aesthetic quality is a promise, not a free win.** B4 says professional images lift demand ~9%; B5 says over-promising images destroy future demand through reviews. Recommending "make it prettier" without matching the underlying offer is contradicted by the literature.
5. **Everything above is calibrated on U.S./English data.** C1 proved association valence flips across categories inside one country. Assuming it survives a jump to Argentine Spanish-language SME accounts is the single largest unvalidated assumption in any product built on this corpus. Budget for local labelling.
