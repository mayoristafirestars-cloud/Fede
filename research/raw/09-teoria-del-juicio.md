# 09 — The theory of judgment: why reading people from images works as well, and as badly, as it does

**Scope.** The conceptual scaffolding underneath reports 01–05. Report 01 tells you *what coefficient* you get. This one tells you *why that coefficient and not another*, and how to reason about a case the literature has never studied. Nine bodies of theory, each with the citation, the core claim, the numbers, and — the point of the exercise — what it implies for designing an analysis of an Instagram account.

**Compiled 2026-08-30.**

### How to read this document

| Marker | Meaning |
|---|---|
| **[FORMALISM]** | A model with an equation or a defined decomposition. Use it to structure the analysis. |
| **[EMPIRICAL]** | A measured effect with numbers you can anchor to. |
| **[CONTESTED]** | The literature disagrees. Both sides reported. |
| **[NO SUPPORT]** | A folk heuristic that the literature does not sustain. Do not ship it. |
| **⇒ IG** | Implication for designing an Instagram analysis. |

---

## 0. The framework in one page

Six claims, each defended below:

1. **Any judgment from images is a two-link chain**, and both links can break independently. Link 1: does the cue actually covary with the trait (*cue validity*)? Link 2: does the observer use that cue (*cue utilization*)? Accuracy is what happens when the two links happen to line up. This is Brunswik's lens model, and it is the correct formalism for the whole problem.
2. **Accuracy is multiplicative, not additive** (Funder's RAM). Relevance × availability × detection × utilization. Any zero kills the product. That is why the ceiling is low and why it is low *for structural reasons*, not because the model is not big enough.
3. **More looking does not help much.** Thin-slice accuracy at 5 seconds is roughly two-thirds of accuracy at 5 minutes, and 60 s is the efficiency optimum (Carney et al. 2007). Curation ceilings apply the same way to a grid: post 200 does not add what post 20 did.
4. **The observable traits are the extraverted-expressive ones.** Extraversion and Openness are readable; Agreeableness, Conscientiousness and Neuroticism are near-noise from static images. This is stable across bedrooms, offices, websites, Facebook, Instagram, photographs and video — five decades and six media.
5. **Consensus is not accuracy.** Observers converge because they share a stereotype, not because they see the person. Every consensus number in the literature exceeds its matching accuracy number, usually by 2–3×. This directly explains the modern LLM result (models agree with each other at r = .58–.83, with the person at r = .18–.31).
6. **A social-media grid is mostly an identity claim, not behavioural residue** — but identity claims turn out to be *surprisingly* informative, because claims are made by the same person whose traits produced the claim. What identity claims are bad at is anything the person has a motive to fake.

---

## 1. Brunswik's Lens Model — the right formalism

### 1.1 The framework **[FORMALISM]**

> Brunswik, E. (1956). *Perception and the Representative Design of Psychological Experiments.* Berkeley: University of California Press.

Brunswik's probabilistic functionalism holds that an organism never perceives a distal object directly. It perceives *proximal cues* which are probabilistically — never deterministically — related to the distal object. The set of cues is the **lens** through which the distal variable is (imperfectly) seen.

Seven elements (standard enumeration):

1. a **distal variable** — the thing being judged (e.g. the account owner's Extraversion);
2. a set of **cues** / proximal variables (e.g. number of faces per post, colour saturation, smiling, clutter);
3. a **judgment** about the distal variable, formed from the cues;
4. **cue validities** — the imperfect correlations between each cue and the criterion;
5. **cue utilizations** — the imperfect correlations between each cue and the judgment;
6. **intercorrelations among the cues** (they are redundant, and this matters for regression);
7. **achievement** (Brunswik's own term: *functional achievement*) — the correlation between judgment and criterion, i.e. accuracy.

The critical structural insight: **cue validity and cue utilization are separate parameters and can be independently zero.** Four cases:

| | Cue is valid | Cue is invalid |
|---|---|---|
| **Observer uses it** | Accuracy | Systematic error (this is where stereotypes live) |
| **Observer ignores it** | Missed information | Correctly ignored |

Good judgment = using valid cues *and* ignoring invalid ones. Poor judgment has two distinct failure modes that require different fixes.

### 1.2 The Lens Model Equation **[FORMALISM]**

> Hursch, C. J., Hammond, K. R., & Hursch, J. L. (1964). Some methodological considerations in multiple-cue probability studies. *Psychological Review, 71*(1), 42–60.
> Tucker, L. R. (1964). A suggested alternative formulation in the developments by Hursch, Hammond, and Hursch, and by Hammond, Hursch, and Todd. *Psychological Review, 71*(6), 528–530.
> Hammond, K. R., Hursch, C. J., & Todd, F. J. (1964). Analyzing the components of clinical inference. *Psychological Review, 71*(6), 438–456.

Tucker's formulation, the one universally used:

$$r_a \;=\; G \cdot R_e \cdot R_s \;+\; C\sqrt{1-R_e^{2}}\;\sqrt{1-R_s^{2}}$$

| Term | Name | Definition | Whose fault it is |
|---|---|---|---|
| $r_a$ | **achievement** | correlation between the judgment and the criterion | the outcome |
| $R_e$ | **environmental predictability** | multiple *R* of the linear model predicting the **criterion** from the cues | the world's — this is the hard ceiling |
| $R_s$ | **cognitive control / consistency** | multiple *R* of the linear model predicting the **judgment** from the cues | the judge's reliability |
| $G$ | **matching index / linear knowledge** | correlation between the *predicted values* of those two models | whether the judge's policy matches reality's policy |
| $C$ | **unmodelled knowledge** | correlation between the *residuals* of the two models | configural/nonlinear insight the linear models missed |

Three things this equation buys you that a bare correlation does not:

- **It separates "the world is noisy" from "the judge is wrong."** $R_e$ is the maximum achievable $r_a$ if the judge were perfect ($G = R_s = 1$). If $R_e = .35$ — which is roughly where photo cues sit for Big Five traits — no observer, human or model, can exceed $r_a = .35$ from those cues. **Building a better model cannot raise $R_e$. Only finding new cues can.**
- **It separates "wrong policy" ($G$ low) from "inconsistent execution" ($R_s$ low).** An LLM has near-perfect $R_s$ (it applies its policy the same way every time) — which is exactly why it agrees with itself and with other LLMs, and why that agreement is uninformative about $G$.
- **It quantifies the residual term.** In practice $C$ is negligible: a critical meta-analysis of 31 lens-model studies (49 tasks, 1,151 judgments, 1,055 participants) reports **average C = .08** and recommends dropping it. Configural genius is mostly a myth.

> Kaufmann, E., Reips, U.-D., & Wittmann, W. W. (2013). A critical meta-analysis of lens model studies in human judgment and decision-making. *PLOS ONE, 8*(11), e83528.
> — Mean achievement $r_a = .45$ across domains; $R_e > .68$ in all analyses. **Psychology was the *lowest*-achievement domain at $r_a = .22$**, against business .50, misc. professions .44, medicine .40, education .39. Judging people is the hardest lens task studied.

> Karelaia, N., & Hogarth, R. M. (2008). Determinants of linear judgment: A meta-analysis of lens model studies. *Psychological Bulletin, 134*(3), 404–426. (Correction 2008 — two columns of the published table were transposed.)
> — 249 task environments from 86 articles across five decades. Achievement is similar in noisy and predictable environments; achievement varies little between lab and field; the most effective feedback is *information about the task*, not outcome feedback.

⇒ **IG.** Write your analysis so that it *has* a $R_e$. Concretely: name the cues you are reading (faces per post, smiling rate, colour statistics, scene diversity, posting cadence, caption length, product-in-hand vs. selfie), and for each one state whether you have a published validity estimate or only an intuition. Cues with no published validity are $R_e$ = unknown, and any confident claim built on them is $G$ noise dressed as insight. And note the asymmetry the equation forces: **an analysis can be internally beautiful, perfectly consistent, entirely reproducible ($R_s = 1$) and completely wrong ($G = 0$).** That is the exact failure mode of an LLM reading a grid.

### 1.3 The canonical application: *A Room With a Cue* **[EMPIRICAL]**

> Gosling, S. D., Ko, S. J., Mannarelli, T., & Morris, M. E. (2002). A room with a cue: Personality judgments based on offices and bedrooms. *Journal of Personality and Social Psychology, 82*(3), 379–398. https://doi.org/10.1037/0022-3514.82.3.379

The paper that made the lens model the standard tool for this problem. Two studies, both structured identically: observers judge occupants they never meet, from the physical space alone; independent coders rate the space on a fixed cue inventory; criterion is a self + peer composite.

**Study 1 — Offices.** 94 occupants across five workplaces in a large US city (commercial real-estate agency, advertising agency, business school, architecture firm, retail bank). 8 observers. 43 coded environmental features (mean α = .63). Criterion: 69 self-reports + 1–2 peer reports for 60 occupants (mean acquaintance 8.3 yr); self–peer *r* = .40; criterion α = .61. BFI, 7-point.

**Study 2 — Bedrooms.** 83 occupants (mean age 21.9), dorms/co-ops/Greek housing near a large West Coast university; 69% women, 42% Asian, 36% White. 7 observers. 42 coded features (mean α = .72). Criterion: 78 self-reports + 1–2 peers for 77 (mean acquaintance 3.4 yr); self–peer *r* = .53; criterion α = .78. BFI, 5-point.

**Table 1 + Table 4 — consensus, accuracy, and vector correlations**

| Trait | Office consensus | Office accuracy | Office vector *r* | Bedroom consensus | Bedroom accuracy | Bedroom vector *r* |
|---|---|---|---|---|---|---|
| Extraversion | .39** | .24* | .36* | .31* | .22* | .24 |
| Agreeableness | .23* | −.04 | −.08 | .20 | .20* | −.23 |
| Conscientiousness | .42** | .24* | **.80**\*\* | .47** | .33** | **.79**\*\* |
| Emotional Stability | .14 | .19 | .09 | .08 | .36** | .16 |
| Openness | **.51**\*\* | **.46**\*\* | .60** | **.58**\*\* | **.65**\*\* | **.80**\*\* |
| **Mean** | **.34** | **.22** | — | **.34** | **.37** | — |

*Consensus = mean of all 28 (offices) / 21 (bedrooms) pairwise inter-observer correlations. Accuracy = aggregated observers vs. self+peer criterion. Vector correlation = Fisher-z correlation between the cue-utilization column and the cue-validity column for that trait, across the 43/42 cues — i.e. **a direct measure of $G$**.*

The vector correlation column is the payload. **Conscientiousness has $G$ ≈ .80 in both studies**: observers' theory of what a conscientious room looks like is almost exactly right. **Agreeableness has negative $G$ in bedrooms (−.23)**: observers' theory is not merely useless, it is anti-correlated with reality. And accuracy tracks $G$ closely, which is the model working.

**Cue utilization vs. cue validity — selected pairs**

*Conscientiousness, offices:* observers used good use of space **.56**, clean **.44**, organized **.73**, cluttered **−.55**. Actual conscientiousness: organized **.35**, neat **.30**, uncluttered **.29** — and *not* good use of space. So three of four intuitions were valid, at roughly half the strength at which they were used.

*Conscientiousness, bedrooms:* used clean **.61**, organized **.70**, cluttered **−.56**. Valid: organized **.29**, neat **.27**, uncluttered **−.32**.

*Openness, offices:* used distinctiveness **.60**, decoration **.49**, magazines **.34**, book quantity **.28** / book variety **.44**, CD quantity **.32** / CD variety **.61**. Valid: distinctive **.30**, unconventional **.24**.

*Openness, bedrooms:* used distinctiveness **.35**, decoration **.35**. Valid: distinctiveness **.35**, **variety** of books **.44**, **variety** of magazines **.51**. The authors' own emphasis: *"it is the variety, not the quantity, of books and magazines that served as the crucial cue."*

*Extraversion, offices:* used decorated **.48**, cheerful **.47**, colourful **.46**, inviting **.35**, unconventional **.41**, cluttered **.24**. Valid: warm **.26**, decorated **.27**, inviting **.29**. Weak but real.

*Agreeableness, bedrooms:* used cheerful **.66**, inviting **.52**, colourful **.51**, comfortable **.43**, clean **.37**, neat **.33**, organized **.26**, clothes strewn **−.39** — **and essentially none of it was valid.** The authors' explanation is the folk belief that *like goes with like*: pleasant people occupy pleasant rooms. This is the single most instructive negative result in the corpus, because "cheerful colourful room ⇒ warm person" is exactly the inference an untrained analyst makes from a warm-toned Instagram grid.

**Cross-context stability (Table 7, 36 cues common to both studies)**

| Trait | Cue-*utilization* vectors, office vs. bedroom | Cue-*validity* vectors, office vs. bedroom |
|---|---|---|
| Extraversion | .37* | −.18 |
| Agreeableness | .44** | −.04 |
| Conscientiousness | **.86**\*\* | **.58**\*\* |
| Emotional Stability | .05 | .17 |
| Openness | .54** | .27 |

**Observers carry the same theory from context to context. Reality does not.** Only Conscientiousness manifests through the same cues in an office and a bedroom. This is the empirical basis for refusing to transport a cue→trait mapping across contexts — and an Instagram grid is a *different context again* from either.

**Stereotype mediation.** In offices, women were *perceived* as more agreeable and less emotionally stable; the only *real* sex difference was Emotional Stability (women lower). In bedrooms, Whites were perceived as more extraverted, more open, more emotionally stable and less agreeable than Asians; the only *real* race difference was Openness (Whites higher). Occupant effect sizes greatly exceeded stereotype effect sizes, so stereotypes explained only a small share — but the mechanism is documented, in the canonical paper, with the authors saying so plainly.

**Benchmarks the paper anchors against** (from Kenny 1994): zero-acquaintance consensus averaged **.12** (range .03–.27) across 9 studies; zero-acquaintance accuracy **.25** across 10 studies. Rooms beat both.

⇒ **IG.** (a) Build an explicit cue inventory *before* looking at the account, with coder-level definitions, and rate the cues independently of the trait inference — this is the only way to separate utilization from validity in your own pipeline. (b) For any cue you rely on, ask which of the four cells of the 2×2 you are in; if you cannot answer, you are in the "systematic error" cell by default. (c) Treat **variety > quantity** as a transferable heuristic for Openness (grid subject diversity, scene diversity, palette range) — it is one of the few cue-level findings that replicated. (d) Do **not** read Agreeableness/warmth from the pleasantness of the aesthetic. That specific inference has been measured and is invalid.

### 1.4 Lens applications to physical appearance **[EMPIRICAL]**

> Naumann, L. P., Vazire, S., Rentfrow, P. J., & Gosling, S. D. (2009). Personality judgments based on physical appearance. *Personality and Social Psychology Bulletin, 35*(12), 1661–1671. https://doi.org/10.1177/0146167209346309

The closest analogue in the literature to "judging a person from one photograph." 113 targets (of 123 UT Austin undergraduates; 10 who smiled in the standardized condition were dropped). Two full-body photographs each: **spontaneous** (no instruction) then **standardized** (look at camera, neutral expression, feet shoulder-width, hands at sides). Compliance was high: in the standardized shots 100% hands at sides, 92% looking at camera, 12% smiling; in the spontaneous shots 66% smiled, 66% looked at camera, 30% feet shoulder-width. Six observers per condition (different people). Criterion = self + up to 3 informants (305 informants, mean acquaintance 9.6 yr, 86% "quite/very well"), ICC α = .79.

**Table 1 — accuracy by condition**

| Trait | Standardized, aggregated | Standardized, single obs. | Spontaneous, aggregated | Spontaneous, single obs. |
|---|---|---|---|---|
| Extraversion | **.39**\*\* | **.29**\*\* | **.42**\*\* | **.34**\*\* |
| Agreeableness | −.11 | −.05 | .20* | .13 |
| Conscientiousness | −.03 | −.01 | .12 | .08 |
| Emotional stability | .17† | .09 | .18† | .10 |
| Openness | .17† | .12 | **.35**\*\* | .20* |
| Likability | .10 | .07 | .28** | .19* |
| Self-esteem | .26** | .14 | .28** | .20* |
| Loneliness | .06 | .04 | .23* | .16† |
| Religiosity | .24** | .11 | .27** | .15† |
| Political orientation | .16† | .10 | .17† | .10 |
| **Mean** | **.14** | **.09** | **.25** | **.17** |

Strip out posture and expression and you keep Extraversion, self-esteem and religiosity, and lose almost everything else. Put expression back and 9 of 10 traits become judgeable — and the spontaneous photo adds incremental validity over the standardized one for 6 of 10 traits (ΔR: Openness .18**, Likability .18**, Loneliness .18*, Agreeableness .16**, Extraversion .07**, Religiosity .06*).

**The cue tables (Table 3/4) are where the lens logic bites.** Observers' Extraversion judgments correlated **.76** with energetic stance and **.71** with smiling; **−.66** with tense stance. Actual Extraversion correlated with the same cues at roughly **.28–.40**. The judgment policy is *directionally correct and roughly twice as steep as reality*. Textbook over-utilization of a valid cue.

Selected validity/utilization mismatches:

- **Openness:** *valid* cues were distinctive dress (+), healthy and neat appearance (−), looking away from camera (+). Observers used distinctive appearance — and then also used smiling and energetic stance, which are not valid for Openness at all.
- **Conscientiousness:** the only valid cue was *not* being distinctively dressed; observers instead used neat, healthy, energetic and smiling. $G$ collapses; accuracy is .12/−.03.
- **Emotional stability:** valid = healthier looking, more relaxed stance. Observers used those *and* smiling and energetic stance, which are invalid for ES.
- **Political orientation:** **none of the coded cues was a valid indicator of liberalism.** Observers nonetheless read it off distinctive, neat and unhealthy appearance. This is the purest available demonstration of cue utilization with zero cue validity — and it is a *demographic-adjacent* inference, which is exactly the class of inference a commercial profiler is most tempted by.
- **Gender moderation:** Conscientiousness was judged accurately for male targets (*r* = .31) and *negatively* for female targets (*r* = −.17), *z* = 2.55, *p* < .05. In males, actual C was associated with neat (.33), healthy (.29), distinctive (.29) appearance. **Among females there were no valid indicators of conscientiousness at all.** A single accuracy figure averaged over a mixed sample hides a sign flip.

Comparison anchors the authors themselves cite: Hall et al. (2008) put average Big Five accuracy from a *dynamic* stimulus at **.23** (range .40 extraversion to .12 agreeableness); Borkenau et al. at 50 ms of video, mean **.13**; Carney et al. at 5 s, mean **.14**; and Richard, Bond & Stokes-Zoota (2003) put the average effect in all of social/personality psychology at **r = .21**.

> Borkenau, P., & Liebler, A. (1992). Trait inferences: Sources of validity at zero acquaintance. *Journal of Personality and Social Psychology, 62*(4), 645–657.
> — 100 adults videotaped entering a room, walking, sitting, looking at camera, reading a standard text; 24 strangers each given one of four channels: sound film, silent film, **still photograph**, or audiotape. The first systematic demonstration that channel determines which traits are readable. Target variance across the Big Five averaged .22, from .17 (Agreeableness) to .33 (Extraversion).

> Vazire, S., Naumann, L. P., Rentfrow, P. J., & Gosling, S. D. (2008). Portrait of a narcissist: Manifestations of narcissism in physical appearance. *Journal of Research in Personality, 42*(6), 1439–1447.
> — N = 160, 7 observers, one full-body photo. **Accuracy for narcissism (NPI) r = .25**, against a well-acquainted-informant benchmark of **.39** (difference n.s., *t* = 1.41). Valid cues: expensive clothes **.29**, amount of preparation required **.28**, attractiveness **.23**, stylish clothes **.22**, organized appearance **.17**, neat appearance **.17**, fashionable **.16**, plain clothes **−.18**; women only — feminine **.26**, makeup **.22**, plucked eyebrows **.23**, cleavage **.23**; men only — eyeglasses **−.25**. Observers used essentially the same set *plus* a few near-invalid ones (fraternity/sorority insignia). Observers' narcissism judgments correlated .25 with targets' Extraversion, −.25 with Agreeableness, .14 (n.s.) with explicit self-esteem, and with the NPI facets: self-absorption/self-admiration .24, leadership/authority .21, exploitativeness/entitlement .19, superiority/arrogance .12 (n.s.).
> **This is the strongest single-photo result in the literature for a non-Big-Five construct — and it is exactly .25.**

⇒ **IG.** Instagram photos are the *spontaneous* condition, not the standardized one — expression and posture are present, and that roughly doubles what is readable (.14 → .25). But the same tables say the readable set is Extraversion, self-esteem, likability, loneliness, religiosity and narcissism — **not** Conscientiousness, and **not** political orientation. If a pipeline outputs a confident conscientiousness or politics read from a grid, it is reproducing the exact error Naumann et al. measured. Also: **run your accuracy numbers split by target gender**, because the one moderator that has been tested flipped sign.

### 1.5 Lens applications to online environments

> Vazire, S., & Gosling, S. D. (2004). e-Perceptions: Personality impressions based on personal websites. *Journal of Personality and Social Psychology, 87*(1), 123–132.

89 personal websites, 11 observers, criterion = self + informants.

| Trait | Consensus ICC(2,1) | Observer accuracy | Single-observer accuracy | Obs.–self | Obs.–informant |
|---|---|---|---|---|---|
| Extraversion | .32** | .38** | .26** | .26* | .39** |
| Agreeableness | .28** | .28** | .17 | .31** | .22* |
| Conscientiousness | .27** | .43** | .27** | .35** | .39** |
| Emotional Stability | .18* | .31** | .19* | .21* | .31** |
| Openness | .32** | **.63**\*\* | .46** | .42** | **.60**\*\* |
| **Mean** | **.27** | **.42** | **.27** | **.31** | **.39** |

Target variances against Kenny's (1994) zero-acquaintance values in parentheses: E .27 (.27), A .19 (.03), C .19 (.13), ES .10 (.09), O .22 (.07). Websites carry far more Agreeableness, Conscientiousness and Openness signal than a first meeting does.

**Impression management (Table 2, β from Step 2 controlling the accuracy criterion):** Extraversion criterion .31**/ideal .24*; Agreeableness .12/.34**; Conscientiousness .43**/.03; Emotional Stability .32**/−.04; Openness .67**/−.07. **Websites are enhanced on Extraversion and Agreeableness, and only those.**

For Facebook and Instagram see §4 and §5 below, and report 01 §5.3 for Osterholz et al. (2023), which is the direct Instagram lens study (102 users, 100 observers, accuracy .25–.44).

---

## 2. Funder's Realistic Accuracy Model (RAM)

> Funder, D. C. (1995). On the accuracy of personality judgment: A realistic approach. *Psychological Review, 102*(4), 652–670.
> Funder, D. C. (1999). *Personality Judgment: A Realistic Approach to Person Perception.* San Diego: Academic Press.
> Letzring, T. D., & Funder, D. C. (2019). The Realistic Accuracy Model. In T. D. Letzring & J. S. Spain (Eds.), *The Oxford Handbook of Accurate Personality Judgment.* Oxford University Press.

### 2.1 The four stages **[FORMALISM]**

RAM is the process model that sits *behind* the lens model — it says what has to happen for a valid cue to end up in an accurate judgment.

> **accuracy = [(relevance of behavioural cues to the trait) × (extent to which those cues are available to observation)] × [(extent to which they are detected) × (the way in which they are used)]**

| Stage | What must be true | Who controls it |
|---|---|---|
| **Relevance** | The target must emit behaviour that is actually diagnostic of the trait | the target + the trait |
| **Availability** | That behaviour must be observable by this judge, in this channel | the situation / the medium |
| **Detection** | The judge must actually notice it | the judge |
| **Utilization** | The judge must use it correctly | the judge |

The brackets separate the environment side from the perceiver side; Funder's point is that the multiplication makes the separation less clean than it looks — "they are both part of the same interactive system."

**The multiplicativity is the theory.** Funder's own worked example: *"if each term were to represent 90% fidelity, then overall accuracy would be .66; if each term were to represent 50% fidelity, then total accuracy would only be .06."* Four links at 50% each yield 6% — which is roughly the *r²* the image literature actually reports. **RAM predicts the observed ceiling from first principles.** Any zero anywhere zeroes the product: *"All the relevant cues in the world are no help if the judge does not perceive and use them; even the most astute judge is helpless in the face of a lack of relevant cues."*

Funder also flags what RAM does *not* cover: the method by which the judgment is elicited (questionnaire, Q-sort, free response) introduces its own error and "lies outside of the RAM model at present." Directly relevant to LLM outputs, where the response format is doing unmeasured work.

### 2.2 The four moderators **[FORMALISM]**

Funder's Table 1 maps each moderator onto the process variables it acts through:

| Moderator | Specific characteristic | RAM stage it acts on |
|---|---|---|
| **Good judge** | perceptiveness | detection |
| | judgmental ability | utilization |
| | (non)defensiveness | detection, utilization |
| **Good target** | activity level | availability |
| | consistency, scalability | relevance |
| | ingenuousness | availability, relevance |
| **Good trait** | visibility, frequency | availability |
| | operant/respondent | relevance |
| | (non)evaluativeness | availability, relevance |
| **Good information** | quantity (e.g. acquaintance) | availability |
| | quality (e.g. relationship) | relevance |

The six pairwise interactions have names: Judge × Trait = **expertise**; Judge × Target = **relationship**; Judge × Information = **sensitivity**; Trait × Target = **palpability**; Trait × Information = **diagnosticity**; Target × Information = **divulgence**.

### 2.3 What RAM predicts about photographs **[FORMALISM → EMPIRICAL]**

**Why Extraversion is perceptible but not inferable.** This is the sharpest thing RAM says about our problem, and it turns on the *relevance/availability* distinction.

Funder: *"a trait like sociability, which is revealed by frequent positive social interaction, is easier to judge than a trait like ruminates and daydreams, which must be inferred from verbal statements or, even more ambiguously, from dreamy looks, distracted responses, and the like, any of which could have other meanings as well or instead."*

Extraversion wins **availability**: it is enacted in public, at high frequency, in the exact channel a camera captures — smiling, energetic posture, being surrounded by people, being photographed at all. Report 01's feature tables say the same thing from the data side: face count and "does this image contain people" are the highest-value features in the whole corpus.

But availability is not relevance, and Funder is explicit that the two can dissociate: *"talkativeness is a highly visible, available behavioural cue but is also ambiguous because it might be relevant to sociability, nervousness, dominance, or a complicated combination of all of these traits."* The photographic analogue is precise: **a smile is highly available and weakly relevant.** It is emitted by extraverts, by agreeable people, by emotionally stable people, by religious people, by people who like the photographer, and by everyone who has been told to smile. In Naumann et al. smiling carried a significant *utilization* coefficient for **every one of the ten traits judged** — a cue used for everything is diagnostic of nothing.

So: Extraversion is **perceptible** (the cues are there, and observers converge — consensus .81 on Facebook, .39/.31 in rooms) but only weakly **inferable** (accuracy .39–.46 at best, .22–.25 typically), because the same available cues are relevant to several traits at once. Perceptibility drives consensus; relevance drives accuracy; conflating them is how you get a confident wrong answer.

**Why Neuroticism is the worst case.** It fails *availability* (internal states leave few reliable physical traces) and it fails on **evaluativeness**: Funder notes that "traits that are extremely desirable or undesirable tend to yield lower self–other agreement" (John & Robins, 1994) because self-presentation distorts both availability and relevance. Neuroticism is undesirable, so it is suppressed in display *and* biased in the self-report criterion. Both ends of the correlation are corrupted. Every study in this document puts Neuroticism last: rooms .14/.19 and .08/.36; Facebook consensus .48, accuracy .13 n.s.; photographs .17–.18; Instagram (Osterholz) it is the trait that improved most and still trails.

**Good information.** Quantity: acquaintances who have known targets ~1 year beat strangers who saw a single 5-minute videotape (Funder & Colvin 1988, and a long list of replications). Quality: Andersen (1984) — listening to someone talk about *thoughts and feelings* yields more accurate judgment than listening to the same person talk about *activities and hobbies*. Snyder & Ickes (1985), confirmed by Funder & Colvin (1991) — **unstructured** situations, where behaviour is free to vary, are more informative than structured ones.

⇒ **IG.** Three hard implications.

1. **An Instagram grid is a high-availability, low-relevance, highly-structured, activities-and-hobbies channel.** It is the *worst* quadrant of Funder's "good information" on three of four dimensions. What it has going for it is quantity — many posts over time — and quantity is the weakest of the four moderators.
2. **Report the RAM chain per claim.** For every inference the analysis makes, be able to say which behaviour is relevant, whether the grid makes it available, which cue detects it, and how it is being used. Claims that cannot survive that walk-through get dropped, not hedged.
3. **Exploit the moderators you can actually move.** You cannot make the target more ingenuous or the trait more visible. You *can* improve detection (systematic coding beats gestalt impression) and utilization (weight cues by published validity, not by salience). Those are the two stages the analyst owns; the other two belong to the account.

---

## 3. Thin slices

### 3.1 The meta-analysis **[EMPIRICAL]**

> Ambady, N., & Rosenthal, R. (1992). Thin slices of expressive behavior as predictors of interpersonal consequences: A meta-analysis. *Psychological Bulletin, 111*(2), 256–274.

**38 independent results from 44–45 studies**, all using observations under 5 minutes, predicting objective outcomes in social and clinical psychology.

- **Overall mean effect size r = .39** (unweighted); weighted M = .41; **95% CI .34–.48**; 99% CI .31–.51; 99.9% CI .28–.54. Median .30; Q1 .22, Q3 .52; min .10, max .87. **100% of the 38 results were positive.** Combined Stouffer Z = 22.56.
- **Fail-safe N = 7,110** studies averaging *p* = .50 would be needed to null the result.
- **No lab bias:** results co-authored by Rosenthal *r* = .38, by his former students .40, by other laboratories .39 — homogeneous, *F*(2,35) = .04.
- BESD: *r* = .39 means correct classification ~70% of the time against ~30% without the slice.

**By exposure length (Table 4)** — the headline finding:

| Slice length | *r* |
|---|---|
| 0–30 s | .33 |
| 30–60 s | .44 |
| 60–120 s | .39 |
| 120–180 s | .24 |
| 180–240 s | .39 |
| 240–300 s | .45 |

Linear contrast on exposure length **Z = .03, n.s.** Contrast of <30 s against the other five bands **Z = −.11, n.s.** *"Judgments from very brief segments of behavior (under half a minute in length) may be as accurate as judgments from longer segments (up to 5 min long)."*

**By channel (Table 5, 65 results):**

| Channel | *n* | *r* |
|---|---|---|
| Face + body | 12 | **.54** |
| Face + speech | 3 | .41 |
| Face | 5 | .40 |
| Speech | 8 | .36 |
| Body + speech | 2 | .33 |
| Transcripts | 6 | .29 |
| Body | 2 | .28 |
| Face, body and speech | 15 | .28 |
| Tone of voice | 12 | .26 |

Face + body is the best channel in the entire meta-analysis. Adding speech to face+body *lowered* accuracy across studies (.54 → .28, n.s.); within the three studies that manipulated it directly, face+body+speech (.42) beat face+body alone (.24), and excluding those studies face+body alone was .62 vs .24 with speech. The direction is unstable but the authors' reading is that "too much information was confusing or distracting to the judges."

**Other moderators:** clinical outcomes .41, deception detection .31, general social .47 (linear contrast n.s.). Field studies .47 vs laboratory .32 (n.s.). Nonverbal only .45 vs verbal+nonverbal .35 (n.s.). Neither number of judges, number of subjects, nor judge gender related to accuracy.

**Against "thick" slices:** OSS assessment study .26; Holt & Luborsky psychiatric competence .31 (supervisor) / .30 (peer); Feldman's teacher-effectiveness meta-analysis — self-report personality .07, student ratings .41, colleague ratings .33; combined median for thick-slice methods **.31**, against **.39** for thin slices. None of the contrasts were significant. *"Ratings from thin slices of behavior are apparently as good a predictor of teaching effectiveness as other measures. This result is quite surprising because colleagues and students have access to so much more information."*

> Ambady, N., & Rosenthal, R. (1993). Half a minute: Predicting teacher evaluations from thin slices of nonverbal behavior and physical attractiveness. *Journal of Personality and Social Psychology, 64*(3), 431–441.
> — The best-known single demonstration: strangers' judgments from muted 30-, 15- and 6-second clips predicted end-of-semester student evaluations. Prediction from 2-second vs 5-second slices did not differ; 10-second prediction was numerically stronger but not significantly so.

### 3.2 The crucial correction for personality **[EMPIRICAL]**

Ambady & Rosenthal's *r* = .39 is for **objective outcomes** (clinical status, deception, teacher evaluations) — not for Big Five accuracy against a self+informant criterion. Reading .39 as "you can judge personality at .39 from a glance" is the most common misuse of the paper. The right number comes from:

> Carney, D. R., Colvin, C. R., & Hall, J. A. (2007). A thin slice perspective on the accuracy of first impressions. *Journal of Research in Personality, 41*(5), 1054–1072.

334 judges, 30 targets, slices of 5 / 20 / 45 / 60 / 300 s drawn from the first, third or fifth minute of a 5-minute interaction. Criterion = average of self, friend and parent NEO. *n* per exposure condition: 82, 74, 73, 77, 24.

**Table 2 — accuracy by construct and slice length**

| Construct | Overall | 5 s | 20 s | 45 s | 60 s | 300 s | Linearity *t* |
|---|---|---|---|---|---|---|---|
| Extraversion | **.42** | .22 | .41 | .46 | .52 | **.55** | 2.73** |
| Negative affect | .32 | .31 | .35 | .31 | .33 | .28 | −.51 |
| Conscientiousness | .28 | .21 | .26 | .28 | .34 | .39 | 2.06* |
| Intelligence | .22 | .24 | .20 | .22 | .24 | .21 | −.22 |
| Neuroticism | .21 | .14 | .19 | .25 | .22 | .29 | 1.46 |
| Positive affect | .20 | .06 (n.s.) | .28 | .25 | .20 | .26 | 1.29 |
| Openness | .17 | .10 | .22 | .20 | .16 | .21 | .74 |
| Agreeableness | .11 | .04 (n.s.) | .09 | .12 | .17 | .21 | 1.63† |
| **Overall** | **.25** | **.17** | **.25** | **.26** | **.28** | **.31** | 4.74*** |

**Three findings that matter more than the headline.**

1. **Accuracy *does* rise with exposure, but the slope is shallow and it saturates.** 5 s → 300 s takes overall accuracy from .17 to .31, a 60-fold increase in exposure for an 82% gain in *r*. The authors' conclusion: **60 seconds is the optimal ratio of accuracy to slice length.**
2. **The gain is trait-specific.** Extraversion and Conscientiousness have significant linear slopes; negative affect and intelligence are *flat* — 5 seconds is as good as 5 minutes. Agreeableness and positive affect are literally at zero after 5 seconds and only become significant with more.
3. **Slice *location* matters as much as slice length** (Table 4). Accuracy from the first / third / fifth minute: positive affect .11 / .21 / .26; negative affect .24 / .31 / .42; extraversion .29 / .51 / .4x; neuroticism .19 / .18 / .22. **Later behaviour is more diagnostic than earlier behaviour**, presumably because self-presentational control decays.

⇒ **IG.** (a) **A grid is a very long thin slice, and the returns are logarithmic.** Report 01 says performance rises monotonically with images per user and recommends a floor of ~20. Carney et al. explains why the curve flattens: you are re-sampling the same expressive channel. Do not promise that analysing 500 posts is materially better than analysing 60. (b) **Order and recency are cues.** The "later is more diagnostic" result argues for weighting recent posts, and for treating the *earliest* posts (maximum self-presentational control, account launch) as least diagnostic. (c) **Face + body is the highest-yield channel in the entire meta-analytic record.** A grid dominated by product flat-lays and text graphics has amputated the best channel — and you should say so in the output rather than inferring the same traits at the same confidence. (d) The channel ordering also warns against naive fusion: adding speech to face+body did not reliably help. Adding captions to images may not either; test it, don't assume it.

---

## 4. Self-verification vs. self-enhancement in online self-presentation **[CONTESTED]**

This is the crux question for whether a grid is signal or performance. The two theoretical poles:

- **Self-enhancement / idealized virtual identity.** People are motivated to present themselves as they wish to be. Self-presentation aims at the ideal self (Baumeister 1982: people are "guided by the desire to make one's public image equivalent to one's ideal self"; Schlenker 1980; Higgins 1987). Content analyses of MySpace supported it (Manago et al. 2008).
- **Self-verification / extended real life.** People are motivated to have others see them as they see themselves, even when the self-view is negative (Swann 1981 onward). Applied to online profiles: OSNs are simply another social context in which real personality is enacted, and idealization is *hard* because profiles contain reputational information the owner does not control (wall posts, tags) and because friends provide accountability.

> Kwang, T., & Swann, W. B., Jr. (2010). Do people embrace praise even when they feel unworthy? A review of critical tests of self-enhancement versus self-verification. *Personality and Social Psychology Review, 14*(3), 263–280.
> — For people with positive self-views the two motives coincide; they diverge only for negative self-views. This matters for our case: **on the traits where a commercial account owner has a positive self-view, verification and enhancement predict the same display, and the two theories are empirically indistinguishable from the grid alone.**

### 4.1 The pro-signal case

> Back, M. D., Stopfer, J. M., Vazire, S., Gaddis, S., Schmukle, S. C., Egloff, B., & Gosling, S. D. (2010). Facebook profiles reflect actual personality, not self-idealization. *Psychological Science, 21*(3), 372–374. https://doi.org/10.1177/0956797609360756

236 OSN users aged 17–22: **US Facebook N = 133 (81 F)**, recruited on the UT Austin campus; **German StudiVZ/SchuelerVZ N = 103 (86 F)**, recruited by Germany-wide advertisement. Profiles were saved before OSNs were mentioned, so owners could not alter them. Observers: **9 (US) and 10 (German)** undergraduate research assistants, no time limit. Criterion: US = self + **four** well-acquainted friends on the TIPI; German = **self-reports only** (BFI-10 + NEO-FFI). Ideal-self measured by rephrasing the same instruments to "describe yourself as you ideally would like to be." Idealization = partial correlation of ideal-self with observer ratings, controlling for the criterion. Samples z-standardized and pooled after GLM found no significant sample interactions.

**Table 1 (average observer / single observer)**

| Trait | Consensus ICC | Accuracy *r* | Accuracy *r*<sub>partial</sub> | Ideal-self *r* | **Self-idealization *r*<sub>partial</sub>** |
|---|---|---|---|---|---|
| Extraversion | .81*** / .31*** | .39*** / .25*** | .32*** / .21*** | .24** / .14*** | **.01 / .00** |
| Agreeableness | .59*** / .13*** | .22** / .11** | .20* / .11** | .13 / .08* | **.08 / .04** |
| Conscientiousness | .77*** / .27*** | .27** / .17*** | .26** / .16*** | .16 / .08* | **−.02 / −.01** |
| Neuroticism | .48*** / .09*** | .13 / .06 | .13 / .06* | .05 / .03 | **.11 / .04** |
| Openness | .72*** / .23*** | .41*** / .24*** | .37*** / .21*** | .12 / .04 | **.11 / .06** |

Footnote 1: the criterion and ideal-self were themselves correlated at mean *r* = .28 (N .08, E .36, O .33, A .22, C .26) — i.e. **people's ideals track their actual traits**, which is the mechanism that makes the whole debate slippery.

Conclusion as written: accuracy strongest for Extraversion (matching face-to-face) and Openness (matching personal environments), lowest for Neuroticism; *"people are not using their OSN profiles to promote an idealized virtual identity."*

**Limitations the paper itself lists** and that a careful reader should weight: only 17–22-year-olds, only two platforms, only the Big Five, only one form of impression management, no analysis of *which* profile components (photos vs. preferences) carried the signal, and no target moderators such as self-monitoring. Add two the paper does not list: **the German criterion had no informant reports at all** (it is self-report vs. self-report, which cannot detect self-enhancement in the criterion itself); and **2009 Facebook is not 2026 Instagram** — it was a semi-closed network of real-life acquaintances, with the accountability mechanism the authors explicitly credit for suppressing idealization. That mechanism is much weaker on a public commercial Instagram account.

### 4.2 The pro-performance case

> Gosling, S. D., Gaddis, S., & Vazire, S. (2007). Personality impressions based on Facebook profiles. *ICWSM 2007*, Boulder, CO.

The *same lab, same platform, three years earlier*, with a stronger criterion (self weighted 1/5, four well-acquainted friends 4/5) and an explicit self-enhancement test. 133 profiles from 165 targets (33 groups of five friends); 9 observer RAs, ~16 h of rating each over 5 weeks; up to 10 photos per profile included.

| Trait | Consensus ICC(2,1) | Observer accuracy | Single-observer accuracy | Meta-accuracy |
|---|---|---|---|---|
| Extraversion | .30 | **.46** | .28 | **.45** |
| Agreeableness | .09 | .20 | .09 | .18 |
| Conscientiousness | .18 | .27 | .15 | .06 |
| Emotional Stability | .05 | **−.13** | −.05 | .08 |
| Openness | .16 | .39 | .18 | .18 |
| **Mean** | **.15** | **.23** | **.13** | — |

**Self-enhancement (Table 2, standardized β at Step 2):**

| Trait | Criterion β | **Ideal-self β** |
|---|---|---|
| Extraversion | .28 | .17 |
| Agreeableness | .22 | .04 |
| Conscientiousness | .21 | .10 |
| Emotional Stability | −.10 | **.27** |
| Openness | .31 | **.26** |

**Emotional Stability and Openness remained significantly predicted by the ideal self after removing reality.** On the trait with *negative* accuracy (ES = −.13), the ideal self is the *only* thing driving observer impressions. That is self-enhancement, measured, on Facebook, by Gosling and Vazire, published three years before the paper that concluded there was none.

The two results are not formally contradictory — different samples, criteria and analyses — but the "no idealization" headline is considerably narrower than it is usually quoted as being. **The honest summary: identity claims are enhanced on the traits people most want to claim (Extraversion, Agreeableness on websites; Emotional Stability and Openness on Facebook), and accurate on the traits with hard-to-fake behavioural correlates.** See also Vazire & Gosling (2004) §1.5: websites enhanced on Extraversion (β = .24) and Agreeableness (β = .34) specifically.

**Meta-accuracy** is a third finding worth carrying: **profile owners knew how they came across only for Extraversion (r = .45).** For Conscientiousness (.06), Emotional Stability (.08), Openness (.18) and Agreeableness (.18) they had essentially no idea. This is the single most commercially useful psychological fact in this document — see §10.

> Harris, E., & Bardey, A. C. (2019). Do Instagram profiles accurately portray personality? An investigation into idealized online self-presentation. *Frontiers in Psychology, 10*, 871.
> — Mixed-methods, **very small**: 4 Instagram account holders rated by 65 observers, plus 6 interviews. Reported a general *lack* of observer agreement, halo effects, and significant one-sample-*t* divergences between observer and self ratings on most traits, with idealization occurring idiosyncratically per account. Concluded Instagram profiles do **not** accurately portray personality. **Weight this lightly**: 4 targets cannot support a between-target correlation, so this is not comparable evidence to Back et al. — it is a signal that the Instagram case may differ, not a demonstration that it does.

> Osterholz, S., Mosel, E. I., & Egloff, B. (2023). #Insta personality. *Journal of Personality, 91*(3). (Detailed in report 01 §5.3.)
> — The properly powered Instagram answer: 102 users with self **and** informant criteria, 100 observers, full lens design. Accuracy **.44 (Extraversion) down to .25 (Conscientiousness)**. Instagram is *not* noise. It is also not better than a bedroom.

⇒ **IG.** The evidence supports a **trait-conditional** answer, not a global one. (a) On **Extraversion and Openness**, an Instagram grid is signal: replicated across Facebook (.39/.41), websites (.38/.63), rooms (.24–.65), Instagram (.44), photographs (.42/.35). (b) On **Emotional Stability and Agreeableness**, it is performance: these are the traits where ideal-self β survives controlling for reality, and where cue validity collapses. **Do not output a "how emotionally stable / how warm is this person" read.** (c) On **Conscientiousness**, it is medium and context-bound (accuracy .27 Facebook, .43 websites, .24–.33 rooms, .25 Instagram, −.03 to .12 photographs) — the one trait whose cue-validity vector replicated across contexts, so it survives transfer better than the others, but from a low base. (d) A **commercial** account has a stronger enhancement motive and weaker accountability than the student personal profiles all this work is based on. Every idealization estimate here should be read as a **lower bound** for a business account.

---

## 5. Identity claims vs. behavioural residue **[FORMALISM]**

> Gosling, Ko, Mannarelli & Morris (2002), §1.3 above — the source of the distinction.

Four mechanisms link a person to the environment they occupy:

| Mechanism | Definition | Example (physical) | Example (Instagram) |
|---|---|---|---|
| **Self-directed identity claims** | symbolic statements made by the occupant *for their own benefit*, to reinforce their self-views | a pebble from a favourite beach; a poster with private meaning | a saved highlight nobody watches; a recurring motif with no engagement payoff |
| **Other-directed identity claims** | symbols with shared meanings, deployed to tell others how one wishes to be regarded | a Martin Luther King poster; university memorabilia | the bio, the highlight covers, the curated grid layout, the brand-values post |
| **Interior behavioural residue** | physical traces of behaviour *performed in that space* | an alphabetised CD collection; charcoal sketches on the floor | posting cadence and time-of-day; caption length consistency; reply behaviour; editing consistency across 200 posts |
| **Exterior behavioural residue** | traces of behaviour performed *elsewhere* | a snowboard and a ski pass; an opera programme and a plane ticket | geotags; repeated co-appearing people; visible workspace, equipment, inventory; seasonal patterns |

Gosling et al. are careful that the four are not mutually exclusive: *"the snowboard may indeed reflect exterior behaviours, but the occupant's decision to display the snowboard (rather than stow it in a closet) may also reflect a desire to make identity claims."*

**Two-step inference process, with a stereotype bypass.** Observers infer (1a) the behaviour that created the evidence, then (2a) the disposition underlying the behaviour. Stereotypes can intervene at either step — activated by the residue itself (1b) or by the inferred behaviour (2b). Stereotype-based inferences differ from the others in that *"observers using stereotypes may draw conclusions about traits for which they have no direct evidence."*

### Which one is an Instagram photo?

**Overwhelmingly an other-directed identity claim.** A published post is selected, framed, edited, captioned, timed and — crucially — *published*, which is the defining act of an other-directed claim. Report 03's central finding is the same one from the marketing side: the literature validates reading the staging, not the stager.

**But that is not fatal, and here is the evidence why.** Personal websites (Vazire & Gosling 2004) are close to *pure* identity claims — no residue at all, every pixel chosen — and they produced the **highest accuracy correlations of any medium in this document** (mean .42; Openness .63; Conscientiousness .43). Identity claims are informative because the claim is made *by the person whose traits generated the claim*. Claiming is itself behaviour. What claims are bad at is precisely the thing you would expect: traits the person has a motive to misrepresent — which is why website enhancement showed up on Extraversion and Agreeableness and nowhere else.

**Residue on Instagram is real but thin, and it lives in the metadata, not the image.** The behavioural-residue channel on a grid consists of:

- posting cadence, regularity, and gaps (interior residue — a repeated act, per Gosling's own argument that *"to have an organized office it is not sufficient to organize the office just once"*);
- consistency of editing, framing, palette and template across many posts (interior residue: a repeated act, and much harder to fake across 200 posts than across 5);
- who recurs in the photographs, and how (exterior residue);
- what the background accidentally shows — workspace, stock, equipment, home, vehicle (exterior residue, and the closest thing on a grid to a bedroom);
- what is *never* shown despite obvious opportunity.

⇒ **IG.** (a) **Label every cue in your inventory as claim or residue, and treat them as separate evidence classes with different discount rates.** Claims are strong evidence about *positioning* and weak evidence about *the person*; residue is the reverse. (b) The most valuable residue on a grid is **aggregate consistency across many posts**, not the content of any post — Gosling's "multiple acts" argument is the reason a grid beats a photo. Design the pipeline to compute over the sequence, not just over the images. (c) **The stereotype bypass (steps 1b/2b) is the failure mode to instrument against.** Its signature is a claim about a trait for which no cue in your inventory provides evidence. Build the check as a rule: *no output claim without a named cue in the inventory.* (d) The distinction is also the honest way to describe the product to a client: "this reads the claim the account is making, and cross-checks it against the residue" is both accurate and more valuable than "this reads the owner's personality."

---

## 6. Signalling theory: costly signals vs. cheap talk **[FORMALISM]**

> Zahavi, A. (1975). Mate selection — a selection for a handicap. *Journal of Theoretical Biology, 53*(1), 205–214.
> Spence, M. (1973). Job market signaling. *Quarterly Journal of Economics, 87*(3), 355–374.
> Donath, J. (2007). Signals in social supernets. *Journal of Computer-Mediated Communication, 13*(1), 231–251. https://doi.org/10.1111/j.1083-6101.2007.00394.x

Donath's is the application to social network profiles, and it is the sharpest available lens on "signal or performance."

**The two signal types.**

- **Assessment signals** are *inherently* reliable, because producing the signal requires possessing the quality. Donath: *"Lifting a 500-pound weight is a reliable signal of strength; a weaker person simply cannot do it."*
- **Conventional signals** have no inherent connection between form and meaning, and are therefore cheap to fake. Donath, on profiles specifically: *"The self-descriptions in online profiles are mostly conventional signals — it is just as easy to type 24 or 62 as it is to enter one's actual age."*

**The reliability condition.** *"For a signal to be reliable, the costs of deceptively producing the signal must outweigh the benefits."* Not "costly," but **differentially costly to the faker.**

**The handicap principle applied to display.** *"Only someone who has an excess of a given resource can afford to expend it for communicative display."* And Donath's essential caveat, which is where most social-media reasoning goes wrong: *"these costly signals are only reliable in the domain of the cost. The owner of an expensive car may use it to signal both wealth and attractiveness, but its high price only guarantees that the owner is wealthy."*

**Applied to social network profiles:**

- **Friend/follower lists** gain reliability from social context — *"The network context can clarify ambiguous presentation, moderate an extreme performance, and confirm an ambitious one"* — but verifying them (tracing the network, detecting fake friends, spotting comments added en masse) is time-consuming, and Donath's central argument is that the *cost of verification* determines how reliable a signal is in practice.
- **Public comments** are reliable grooming signals: *"The cost in time is a signal of the resources one is willing to commit to this relationship."*
- **Information fashion** — being early to a trend — signals position in a cultural network, because early adoption is costly and the fashion keeps moving.

### Ranking Instagram displays by fakeability

| Display | Signal type | Cost to fake | Reliable about |
|---|---|---|---|
| Bio text, stated values, stated location | conventional | ~zero | nothing |
| A single aspirational photo | conventional | low | nothing |
| Follower count | conventional (purchasable) | low in money | nothing without engagement cross-check |
| Consistent visual quality across 200 posts | approaching assessment | high in time/skill | production capability, conscientiousness-in-role |
| Sustained posting cadence over years | assessment (time-cost) | high in time | commitment, operational stability |
| Comment replies at volume | assessment (Donath's grooming cost) | high in time | actual investment in the audience |
| Engagement *ratio* consistent with follower count | assessment | hard to fake jointly | genuine reach |
| Physical inventory / workspace / equipment visible across many posts | assessment (capital cost) | high in money | actual operational scale |
| Repeated third parties (staff, customers, collaborators) visible over time | assessment (social cost) | very high | real relationships, real trade |
| Early adoption of a format/trend | information fashion | moderate | network position |

**The key move: the reliable inferences are all in the "domain of the cost."** A grid with two years of daily, consistently produced, well-lit posts reliably signals *sustained productive capacity*. It does **not** reliably signal that the owner is warm, conscientious in general, or emotionally stable — those are outside the domain of the cost, and Donath's caveat about the expensive car applies exactly.

⇒ **IG.** (a) **Rank every cue by fakeability before weighting it.** A pipeline that treats the bio and the two-year cadence as equally informative is misweighted by orders of magnitude. (b) **The cheapest and most reliable analyses are cross-checks between signals that are hard to fake *jointly***: follower count vs. engagement rate; stated scale vs. visible inventory; claimed cadence vs. actual timestamps; claimed niche vs. what actually recurs. Joint fakes are much costlier than single fakes, which is precisely Donath's point about verification cost. (c) **Restrict every conclusion to the domain of the cost.** "This account demonstrably sustains X posts/week at Y production quality" is warranted. "Therefore the owner is disciplined" is not. (d) This gives report 03's finding a theoretical home: the reason "product-in-hand shots buy purchase intent while front-facing selfies buy likes" is a signalling asymmetry — the product-in-hand shot carries an assessment component (you must actually have the product) that the selfie does not.

---

## 7. Impression formation, the halo effect, and the "kernel of truth" debate

### 7.1 Halo **[EMPIRICAL]**

> Thorndike, E. L. (1920). A constant error in psychological ratings. *Journal of Applied Psychology, 4*(1), 25–29.
> — Officers rated 137 aviation cadets on supposedly independent qualities. The inter-trait correlations were *"too high and too even."* Thorndike concluded that even expert judges *"are unable to treat an individual as a compound of independent qualities"* and that ratings were coloured by *"a marked tendency to think of the person in general as rather good or rather inferior."* He named it the halo effect.

> Nisbett, R. E., & Wilson, T. D. (1977). The halo effect: Evidence for unconscious alteration of judgments. *Journal of Personality and Social Psychology, 35*(4), 250–256.
> — Two videotaped interviews with the *same* instructor, warm in one and cold in the other. Subjects who saw the warm version rated his appearance, mannerisms and accent as *appealing*; those who saw the cold version rated the identical attributes as *irritating*. **Subjects were unaware of the influence.** Global evaluation contaminates attribute judgment even when there is enough information for independent assessment, and introspection does not detect it.

> Eagly, A. H., Ashmore, R. D., Makhijani, M. G., & Longo, L. C. (1991). What is beautiful is good, but…: A meta-analytic review of research on the physical attractiveness stereotype. *Psychological Bulletin, 110*(1), 109–128.
> — Overall attractiveness stereotype **r ≈ .28** (k ≈ 76 samples). Crucially it is **not uniform**: largest for **social competence**; intermediate for potency, adjustment and intellectual competence; **near zero for integrity and concern for others.** The stereotype is specifically about sociability, which is exactly the trait that photographs already carry real signal about — so attractiveness halo and genuine extraversion cue-validity are confounded in every photo study.

> Langlois, J. H., Kalakanis, L., Rubenstein, A. J., Larson, A., Hallam, M., & Smoot, M. (2000). Maxims or myths of beauty? A meta-analytic and theoretical review. *Psychological Bulletin, 126*(3), 390–423.
> — Attractive children and adults are judged more positively **even by people who know them**, and are *treated* more positively. Halo is not confined to strangers, which means it contaminates the informant criterion too.

⇒ **IG.** (a) **Attractiveness of the person and production quality of the images are the two halo carriers on a grid, and they are correlated with each other and with the aesthetic that makes the account look "professional."** If you do not measure and control for them, they will drive your output. (b) Nisbett & Wilson's result generalises to models: an LLM asked for ten trait ratings from one grid will produce ten correlated ratings, and its stated reasoning will not reveal that it did. **Rating each trait in a separate call, from a separate cue list, is a cheap and effective halo control.** (c) Eagly's non-uniformity is actionable: if halo mostly inflates *social competence*, then an extraversion/sociability read from an attractive, well-produced account is the single least trustworthy output in the whole pipeline — and it is the one clients most want.

### 7.2 The kernel-of-truth debate, honestly stated **[CONTESTED]**

There are two distinct literatures that get conflated, and separating them is most of the work.

**(a) Kernel of truth in *facial/appearance* inferences — the physiognomy question.**

> Foo, Y. Z., Sutherland, C. A. M., Burton, N. S., Nakagawa, S., & Rhodes, G. (2022). Accuracy in facial trustworthiness impressions: Kernel of truth or modern physiognomy? A meta-analysis. *Personality and Social Psychology Bulletin, 48*(11), 1580–1596.
> — **Face-level r = .14; perceiver-level r = .27.** Both significant, both characterised by the authors as *"unlikely to be of practical utility."* Accuracy varied by domain: aggressiveness and sexual unfaithfulness stronger; agreeableness, criminality, financial reciprocity and honesty weaker. The authors' verdict: a **limited kernel of truth, not a licence for physiognomy**, plus flags for Western-sample dominance and reporting-standards problems.

> Todorov, A., Funk, F., & Olivola, C. Y. (2015). Response to Bonnefon et al.: Limited "kernels of truth" in facial inferences. *Trends in Cognitive Sciences, 19*(8), 422–423.
> — Against Bonnefon, Hopfensitz & De Neys' more optimistic reading. Todorov's position: consensus about what a face communicates is high and stable; accuracy is low; and *"the existence of a consensus attribute judgement for a particular person's appearance does not mean that it holds any truth about their personality."* When age, ethnicity and gender are controlled, attributions from faces carry little validity.

**(b) Stereotype accuracy — a different and much stronger claim.**

> Jussim, L., Crawford, J. T., & Rubinstein, R. S. (2015). Stereotype (in)accuracy in perceptions of groups and individuals. *Current Directions in Psychological Science, 24*(6), 490–497.
> Jussim, L., Crawford, J. T., Anglin, S. M., Chambers, J., Stevens, S. T., & Cohen, F. (2016). Stereotype accuracy: One of the largest and most replicable effects in all of social psychology. In *Handbook of Prejudice, Stereotyping, and Discrimination* (2nd ed.). Psychology Press.
> — Over 50 studies of demographic, national, political and other stereotypes. Consensual stereotype–reality correspondence correlations are frequently **.4 to .9**, against a field where (per Richard, Bond & Stokes-Zoota 2003) **fewer than 5% of all effects exceed r = .50**. Jussim's benchmark: *r* ≥ .40 ≈ right at least 70% of the time.

**The two facts that keep this honest, and that Jussim himself states:**

1. **Accuracy of a group-level stereotype does not transfer to accuracy about an individual.** A stereotype can track a group mean well and still predict any given member poorly, because within-group variance swamps between-group variance for nearly every psychological trait. This is the whole ballgame for a profiler: you are always judging an individual.
2. **Not all stereotypes are accurate.** The Terracciano/McCrae national-character work is the standing counterexample: consensual beliefs about national character showed essentially **no** correspondence to aggregated personality data from those nations.

> Terracciano, A., et al. (2005). National character does not reflect mean personality trait levels in 49 cultures. *Science, 310*(5745), 96–100.

**Where this leaves us.** Both sides are right about different objects. Stereotypes about *categories* often carry substantial truth. Inferences about *this face*, *this person*, from *appearance*, carry *r* ≈ .14–.27. And the harder problem is that the two are entangled: much of the individual-level accuracy that *is* observed is the stereotype doing the work, correctly, at group level — which is why Gosling et al. found sex and race stereotypes partially mediating both consensus and accuracy in bedrooms, and why controlling for age/ethnicity/gender collapses facial validity.

⇒ **IG.** (a) The defensible framing is **"the kernel is real and it is small."** Do not claim physiognomy; do not claim zero either, because the meta-analytic estimate is not zero. Anchor to *r* ≈ .14–.27 for appearance-based individual inference. (b) **Test whether your own pipeline is just running a demographic stereotype**: rerun with age/gender/ethnicity information removed or controlled, and see how much accuracy survives. If most of it evaporates, you have built a demographic classifier with a personality label on it — which is report 05's headline legal exposure, not just a validity problem. (c) The group/individual distinction is the sentence to put in the client-facing output: *"this is a distributional statement about accounts like this one, not a claim about this person."*

---

## 8. Why observers agree with each other more than with the target

### 8.1 The structure **[FORMALISM]**

Consensus (observer ↔ observer) and accuracy (observer ↔ criterion) are separate parameters, and consensus systematically exceeds accuracy. Every dataset in this document:

| Study / medium | Mean consensus | Mean accuracy | Ratio |
|---|---|---|---|
| Zero acquaintance (Kenny 1994, 9–10 studies) | .12 | .25* | — |
| Offices (Gosling 2002) | .34 | .22 | 1.5× |
| Bedrooms (Gosling 2002) | .34 | .37 | 0.9× |
| Personal websites (Vazire & Gosling 2004) | .27 | .42 (agg.) / .27 (single) | 1.0× single |
| Facebook (Gosling et al. 2007) | .15 | .23 (agg.) / .13 (single) | 1.2× single |
| Facebook (Back et al. 2010) | .67 agg. / **.21 single** | .28 agg. / **.17 single** | 1.3× single |
| **LLMs on social media text (Marengo et al. 2025)** | **.58–.83** | **.18–.31** | **~3×** |

\* Kenny's accuracy figure is aggregated-observer; his consensus figure is pairwise, so the two are not directly comparable. **The comparison that is apples-to-apples is single-observer consensus vs. single-observer accuracy**, and there the gap is consistent.

### 8.2 The shared-stereotype account **[EMPIRICAL]**

> Kenny, D. A. (1994). *Interpersonal Perception: A Social Relations Analysis.* New York: Guilford.
> Kenny, D. A., Albright, L., Malloy, T. E., & Kashy, D. A. (1994). Consensus in interpersonal perception: Acquaintance and the Big Five. *Psychological Bulletin, 116*(2), 245–258.
> Kenny, D. A. (2004). PERSON: A general model of interpersonal perception. *Personality and Social Psychology Review, 8*(3), 265–280.

- Review of **32 studies**: consensus correlations range from zero to about .3, **highest for Extraversion**; overall roughly **.20 at zero acquaintance rising to about .40 at long-term acquaintance**.
- The counterintuitive finding: **consensus does not straightforwardly increase with acquaintance.** Kenny's explanation is a two-force model — *"agreement increases because perceivers better know the target. However, agreement decreases because the effect of shared stereotypes and the effect of agreement about inconsistency decrease as perceivers become better acquainted."*
- The PERSON model names the components: **P** (target's actual personality), **N** (norm × overlap), **S** (shared stereotype), among others. **At zero acquaintance, essentially the entire ~.20 consensus derives from S, not from P.**
- The Weighted Average Model parameter Kenny calls **"similar meaning systems"** — the degree to which observers agree on what a piece of information *means* — is what Gosling et al. (2002) invoke to explain room consensus: if observers all agree that stacked papers mean conscientious, consensus is high whether or not stacked papers actually mean conscientious.

**Cronbach's decomposition** is the other half of the answer:

> Cronbach, L. J. (1955). Processes affecting scores on "understanding of others" and "assumed similarity." *Psychological Bulletin, 52*(3), 177–193.
> Furr, R. M. (2008). A framework for profile similarity: Integrating similarity, normativeness, and distinctiveness. *Journal of Personality, 76*(5), 1267–1316.
> Biesanz, J. C. (2010). The social accuracy model of interpersonal perception. *Multivariate Behavioral Research, 45*(5), 853–885.

Cronbach showed that an accuracy correlation is a composite of four things:

| Component | What it measures |
|---|---|
| **Elevation** | is the perceiver globally positive or negative? |
| **Differential elevation** | does the perceiver rank *targets* correctly overall? |
| **Stereotype accuracy** | does the perceiver know how people *in general* score on each trait? |
| **Differential accuracy** | does the perceiver get *this* target's distinctive profile right, once the general profile is removed? |

Only **differential elevation** and **differential accuracy** are "real" accuracy in the sense a profiler means. The modern restatement (Furr, Biesanz) is **normative accuracy** (knowing the average person) vs. **distinctive accuracy** (knowing *this* person). **A judge who simply outputs the population mean profile for every target scores well on stereotype/normative accuracy and zero on distinctive accuracy** — and an undecomposed correlation will not distinguish that judge from a good one.

### 8.3 This explains the LLM result exactly

Report 01 §6.5 (Marengo, Montag & Settanni 2025): 1,214 Italian Facebook users, two years of posts, Gemini 1.5 Pro and GPT-4o. **Cross-model agreement r = .58–.83; two-year test–retest .44–.60; convergent validity with self-report .18–.31** (Openness .31, Extraversion .27, Agreeableness .24, Conscientiousness .23, Neuroticism .18). Systematic bias: underestimates Agreeableness and Conscientiousness, overestimates Extraversion.

Read through §8.1–8.2, this is not a surprising finding, it is the *predicted* one:

- **High cross-model agreement = high $R_s$ + shared S.** Models are perfectly consistent in applying their policy, and they share a stereotype because they were trained on overlapping text. In lens terms: $R_s ≈ 1$, $G$ modest.
- **The gap between .58–.83 and .18–.31 is the size of the S component.** It is the same phenomenon as human zero-acquaintance consensus of .20 with near-zero P — just much larger, because models are far more consistent than people and share a far more homogeneous stereotype.
- **The systematic direction of the bias (over-Extraversion, under-Agreeableness/Conscientiousness) is a mean-level shift**, i.e. *elevation* error in Cronbach's sense — which does not show up in a correlation at all, and would be invisible if you only reported *r*.

⇒ **IG.** (a) **Never report inter-model or inter-run agreement as a validity statistic.** It measures $R_s$ and S, not $G$. If your evaluation section contains an agreement number and no criterion number, it is measuring the wrong thing. (b) **Decompose your accuracy.** At minimum, check whether your outputs beat the trivial baseline of "predict the population mean profile for every account." If they do not, you have a stereotype generator. (c) **Run the same account through the pipeline more than once and check elevation drift separately from rank-order stability** — they are different failure modes with different fixes. (d) When a client says "I ran it three times and it said the same thing, so it's reliable," the correct response is that reliability is $R_s$, and $R_s = 1$ is compatible with $G = 0$. That sentence is the single most useful thing in this document for managing expectations.

---

## 9. Folk heuristics with no support **[NO SUPPORT]**

### 9.1 "You flaunt what you lack" / compensation

The folk claim: conspicuous display of X indicates a deficit in X. Displays of wealth mean insecurity about money; displays of the relationship mean the relationship is failing; displays of confidence mean the absence of it.

**There is no general literature supporting this as a between-person diagnostic.** What exists is three adjacent bodies of work, none of which licenses the inference:

**(a) Narcissism and selfies — real, small, and unstable.**

> McCain, J. L., & Campbell, W. K. (2018). Narcissism and social media use: A meta-analytic review. *Psychology of Popular Media Culture, 7*(3), 308–327.
> — 62 samples, **N = 13,430**. Grandiose narcissism relates positively to all four indices — time spent, frequency of status updates, number of friends/followers, and **frequency of posting selfies** — with **r = .11 to .20**. Culture and platform significantly moderated the results. **Vulnerable narcissism was not significantly related to social media use** (rs = .05–.42, small samples, uncertain).

*r* = .11–.20 is 1–4% of variance. It supports a population-level statement ("narcissistic people post marginally more selfies") and supports **nothing** at the individual level ("this person posts selfies, therefore they are narcissistic"). The base-rate error is the whole problem: P(selfie | narcissist) ≠ P(narcissist | selfie), and with r ≈ .15 the posterior barely moves.

> Frederick, C., & Zhang, T. (2019). Narcissism and social media usage: Is there no longer a relationship? *Journal of Articles in Support of the Null Hypothesis, 16*(1), 23–xx.
> — N = 397 MTurk adults, mean age 29; NPI + Self-Consciousness Scale + social media use survey. **Narcissism was not significantly related to social media use.** Published in a null-results journal precisely because the field's file drawer is the issue.

Note also the *opposite*-direction finding that is much better supported: narcissism is **detectable from appearance** at *r* = .25 (Vazire et al. 2008, §1.4) via expensive/stylish clothes, preparation effort and attractiveness. So narcissism is a *readable* trait — just not readable from "posts a lot of selfies."

**(b) Compensatory / false self-presentation — correlational, self-report, and not a display heuristic.** There is a body of work linking low self-esteem, low trait authenticity and social anxiety to *self-reported* false self-presentation online, and to problematic social media use. All of it is (i) cross-sectional, (ii) measured by asking people whether they present falsely, and (iii) about the *relationship between two self-reports*, not about a cue an observer can read off a grid. It does not establish that any observable display feature indicates insecurity.

**(c) The one genuinely good study, and what it actually says.**

> Emery, L. F., Muise, A., Dix, E. L., & Le, B. (2014). Can you tell that I'm in a relationship? Attachment and relationship visibility on Facebook. *Personality and Social Psychology Bulletin, 40*(11), 1466–1479.
> — Three studies. **Between persons:** anxiously attached individuals reported *high* desired relationship visibility; avoidant individuals *low*. **Within persons (daily diary, Study 3):** on days when people felt more insecure about their partner's feelings, they made their relationship more visible.

This is the closest thing to evidence for a compensation display — and note carefully what it is. It is a **within-person, state-level, day-to-day** effect measured against a same-day self-report of felt insecurity. It says: *when this person feels less secure than usual, this person posts more about the relationship today.* It does **not** say that a person who posts more about their relationship than other people do is more insecure than other people — that is the between-person claim, and the between-person result is that anxious attachment predicts *desired* visibility (a trait-consistent claim, not a compensatory one). Converting the within-person finding into a between-person diagnostic is an ecological-fallacy error, and it is exactly the error the folk heuristic commits.

**(d) The related "poor get richer" / social compensation hypothesis** — that socially anxious or introverted people compensate online — has generally lost to the "rich get richer" hypothesis in the internet-and-wellbeing literature (see report 02). Extraverts are more active online, not less. Compensation as a general account of online display does not have the evidence.

### 9.2 Other unsupported reads, for completeness

| Folk inference | Status |
|---|---|
| Warm colour palette / cheerful aesthetic ⇒ warm, agreeable person | **[NO SUPPORT]** — directly measured and invalid (Gosling et al. 2002 bedrooms: Agreeableness utilization .26–.66 across cues, validity ≈ 0, vector *r* = **−.23**) |
| Neat, well-produced grid ⇒ conscientious person | **[WEAK]** — valid in male-target photographs (.33 neat) and in *rooms* (.27–.35), **zero validity in female-target photographs**, and photograph-level accuracy for C is −.03 to .12. Rooms ≠ grids. |
| Distinctive/unusual aesthetic ⇒ open person | **[SUPPORTED, small]** — one of the few cues valid in three independent contexts: offices .30, bedrooms .35, photographs (distinctive dress, valid). Plus **variety > quantity** (books .44, magazines .51). |
| Reading political orientation from aesthetic | **[NO SUPPORT]** — Naumann et al. found **no valid appearance cue** for political orientation, while observers confidently used three. |
| Reading emotional stability / anxiety from display | **[NO SUPPORT / ACTIVELY MISLEADING]** — the trait with the worst consensus (.05–.48), worst accuracy (−.13 to .19 in most media), and the one where the **ideal self**, not reality, drove observer impressions (β = .27, Gosling et al. 2007). |
| Follower count as evidence of anything | **[NO SUPPORT]** — a conventional signal, purchasable, per Donath. Only interpretable jointly with engagement. |
| "The account looks professional, so the owner is competent" | **[HALO]** — Thorndike 1920, Nisbett & Wilson 1977, Eagly et al. 1991. The specific inflated dimension is *social competence*. |

⇒ **IG.** (a) **Put a named blocklist in the system prompt / spec**, not just a general instruction to be careful. The inferences above have been measured and failed; naming them is cheaper and more reliable than hoping the model declines. (b) When a client asks for the compensation read — and they will, because it is the most seductive thing a profiler can offer — the honest answer is the Emery result: *the effect that exists is within-person and day-to-day, and cannot be recovered from a single view of a grid.* (c) The narcissism case is the template for how to handle every "small but real" effect: state the population-level correlation, state that r = .15 does not move an individual posterior, and refuse the individual claim.

---

## 10. The synthesis: what a good analyst carries in their head

**The five-question walk-through, applied to every claim the analysis makes.**

1. **What is the distal variable?** Name it precisely. "Extraversion (self+informant composite)" is a distal variable. "Vibe" is not.
2. **What is the cue?** Name the observable. If you cannot name it, you are in Gosling's stereotype bypass (step 1b/2b) and the claim is unsupported by construction.
3. **What is the cue's validity?** Cite a number or say "unknown." An unknown-validity cue caps $R_e$ at unknown, and every downstream claim inherits that.
4. **Is this cue a claim or a residue, and how costly is it to fake?** Claims are informative about positioning; residue and assessment signals are informative about the person and the operation. Restrict the conclusion to the domain of the cost.
5. **Would three observers who share my stereotype agree with me, and would that agreement mean anything?** If the answer is "yes" and "no," you are measuring $R_s$ and S, not $G$.

**The numbers to have memorised.**

| Quantity | Value | Source |
|---|---|---|
| Single photograph, spontaneous pose, mean over 10 traits | **.25** aggregated / **.17** single observer | Naumann 2009 |
| Single photograph, expression suppressed | **.14** / **.09** | Naumann 2009 |
| Best trait from a photograph (Extraversion) | **.39–.42** | Naumann 2009 |
| Narcissism from one photograph | **.25** (informant benchmark .39) | Vazire 2008 |
| Full Instagram account, human observers | **.25–.44** | Osterholz 2023 |
| Facebook profile | **.13–.41** agg., **.06–.25** single | Back 2010 |
| Personal website (pure identity claim) | **.27–.63** agg. | Vazire & Gosling 2004 |
| Bedroom (pure residue + claims, no person) | **.20–.65** | Gosling 2002 |
| Thin slice, 5 s of video, Big Five mean | **.17** | Carney 2007 |
| Thin slice, 300 s of video, Big Five mean | **.31** | Carney 2007 |
| Thin slice meta-analysis, objective outcomes | **.39** (95% CI .34–.48) | Ambady & Rosenthal 1992 |
| Face from appearance, trustworthiness | **.14** face-level / **.27** perceiver-level | Foo 2022 |
| Attractiveness halo | **≈.28**, concentrated on social competence | Eagly 1991 |
| Zero-acquaintance consensus | **.12–.20** | Kenny 1994 |
| Average effect in all of social/personality psychology | **.21** | Richard, Bond & Stokes-Zoota 2003 |
| LLM agreement with other LLMs vs. with the person | **.58–.83** vs **.18–.31** | Marengo 2025 |
| Achievement in psychology lens tasks vs. business | **.22** vs **.50** | Kaufmann 2013 |

**The trait ordering, which is the most robust fact in the whole corpus.** Across offices, bedrooms, websites, Facebook, Instagram, photographs, videos and 50 ms video: **Openness ≈ Extraversion > Conscientiousness > Agreeableness ≈ Neuroticism.** Extraversion wins in dynamic/social channels; Openness wins in environmental/aesthetic channels. Instagram is an environmental/aesthetic channel with a social overlay, which is why Osterholz found both at the top. Agreeableness and Neuroticism should be treated as **not readable** and excluded from output, not reported with a caveat.

**The one commercially valuable asymmetry.** Meta-accuracy on Facebook was **.45 for Extraversion and .06–.18 for everything else** (Gosling et al. 2007). **People know how extraverted they come across and have essentially no idea how they come across on anything else.** This is the same shape as report 01's finding that the selfie/product dissociation is "a diagnostic most account owners cannot make about themselves." The product is not "we know who you are." The product is **"we can tell you what your grid says, which you cannot see, because you are inside it."** That claim is theoretically grounded, empirically supported, and does not require any accuracy about the person at all.

---

## References

**Lens model and formalism**
1. Brunswik, E. (1956). *Perception and the Representative Design of Psychological Experiments.* Berkeley: University of California Press.
2. Hursch, C. J., Hammond, K. R., & Hursch, J. L. (1964). Some methodological considerations in multiple-cue probability studies. *Psychological Review, 71*(1), 42–60.
3. Hammond, K. R., Hursch, C. J., & Todd, F. J. (1964). Analyzing the components of clinical inference. *Psychological Review, 71*(6), 438–456.
4. Tucker, L. R. (1964). A suggested alternative formulation in the developments by Hursch, Hammond, and Hursch, and by Hammond, Hursch, and Todd. *Psychological Review, 71*(6), 528–530.
5. Karelaia, N., & Hogarth, R. M. (2008). Determinants of linear judgment: A meta-analysis of lens model studies. *Psychological Bulletin, 134*(3), 404–426. (See also the 2008 correction.)
6. Kaufmann, E., Reips, U.-D., & Wittmann, W. W. (2013). A critical meta-analysis of lens model studies in human judgment and decision-making. *PLOS ONE, 8*(11), e83528.

**Lens applications: environments, appearance, online**
7. Gosling, S. D., Ko, S. J., Mannarelli, T., & Morris, M. E. (2002). A room with a cue: Personality judgments based on offices and bedrooms. *JPSP, 82*(3), 379–398.
8. Naumann, L. P., Vazire, S., Rentfrow, P. J., & Gosling, S. D. (2009). Personality judgments based on physical appearance. *PSPB, 35*(12), 1661–1671.
9. Borkenau, P., & Liebler, A. (1992). Trait inferences: Sources of validity at zero acquaintance. *JPSP, 62*(4), 645–657.
10. Vazire, S., & Gosling, S. D. (2004). e-Perceptions: Personality impressions based on personal websites. *JPSP, 87*(1), 123–132.
11. Vazire, S., Naumann, L. P., Rentfrow, P. J., & Gosling, S. D. (2008). Portrait of a narcissist: Manifestations of narcissism in physical appearance. *JRP, 42*(6), 1439–1447.
12. Gosling, S. D., Gaddis, S., & Vazire, S. (2007). Personality impressions based on Facebook profiles. *ICWSM 2007.*
13. Osterholz, S., Mosel, E. I., & Egloff, B. (2023). #Insta personality. *Journal of Personality, 91*(3). (See report 01 §5.3.)

**Realistic Accuracy Model**
14. Funder, D. C. (1995). On the accuracy of personality judgment: A realistic approach. *Psychological Review, 102*(4), 652–670.
15. Funder, D. C. (1999). *Personality Judgment: A Realistic Approach to Person Perception.* Academic Press.
16. Funder, D. C., & Sneed, C. D. (1993). Behavioral manifestations of personality: An ecological approach to judgmental accuracy. *JPSP, 64*(3), 479–490.
17. Letzring, T. D., & Funder, D. C. (2019). The Realistic Accuracy Model. In *The Oxford Handbook of Accurate Personality Judgment.* OUP.
18. John, O. P., & Robins, R. W. (1994). Accuracy and bias in self-perception: Individual differences in self-enhancement and the role of narcissism. *JPSP, 66*(1), 206–219.

**Thin slices**
19. Ambady, N., & Rosenthal, R. (1992). Thin slices of expressive behavior as predictors of interpersonal consequences: A meta-analysis. *Psychological Bulletin, 111*(2), 256–274.
20. Ambady, N., & Rosenthal, R. (1993). Half a minute: Predicting teacher evaluations from thin slices of nonverbal behavior and physical attractiveness. *JPSP, 64*(3), 431–441.
21. Carney, D. R., Colvin, C. R., & Hall, J. A. (2007). A thin slice perspective on the accuracy of first impressions. *JRP, 41*(5), 1054–1072.
22. Hall, J. A., Andrzejewski, S. A., Murphy, N. A., Schmid Mast, M., & Feinstein, B. A. (2008). Accuracy of judging others' traits and states. *JRP, 42*(6), 1476–1489.

**Self-presentation online**
23. Back, M. D., Stopfer, J. M., Vazire, S., Gaddis, S., Schmukle, S. C., Egloff, B., & Gosling, S. D. (2010). Facebook profiles reflect actual personality, not self-idealization. *Psychological Science, 21*(3), 372–374.
24. Harris, E., & Bardey, A. C. (2019). Do Instagram profiles accurately portray personality? *Frontiers in Psychology, 10*, 871.
25. Swann, W. B., Jr. (1987). Identity negotiation: Where two roads meet. *JPSP, 53*(6), 1038–1051.
26. Kwang, T., & Swann, W. B., Jr. (2010). Do people embrace praise even when they feel unworthy? *PSPR, 14*(3), 263–280.
27. Manago, A. M., Graham, M. B., Greenfield, P. M., & Salimkhan, G. (2008). Self-presentation and gender on MySpace. *Journal of Applied Developmental Psychology, 29*(6), 446–458.
28. Baumeister, R. F. (1982). A self-presentational view of social phenomena. *Psychological Bulletin, 91*(1), 3–26.
29. Goffman, E. (1959). *The Presentation of Self in Everyday Life.* Doubleday.

**Signalling**
30. Zahavi, A. (1975). Mate selection — a selection for a handicap. *Journal of Theoretical Biology, 53*(1), 205–214.
31. Spence, M. (1973). Job market signaling. *QJE, 87*(3), 355–374.
32. Donath, J. (2007). Signals in social supernets. *JCMC, 13*(1), 231–251.

**Halo, impressions, stereotype accuracy**
33. Thorndike, E. L. (1920). A constant error in psychological ratings. *Journal of Applied Psychology, 4*(1), 25–29.
34. Nisbett, R. E., & Wilson, T. D. (1977). The halo effect: Evidence for unconscious alteration of judgments. *JPSP, 35*(4), 250–256.
35. Eagly, A. H., Ashmore, R. D., Makhijani, M. G., & Longo, L. C. (1991). What is beautiful is good, but… *Psychological Bulletin, 110*(1), 109–128.
36. Langlois, J. H., et al. (2000). Maxims or myths of beauty? A meta-analytic and theoretical review. *Psychological Bulletin, 126*(3), 390–423.
37. Foo, Y. Z., Sutherland, C. A. M., Burton, N. S., Nakagawa, S., & Rhodes, G. (2022). Accuracy in facial trustworthiness impressions: Kernel of truth or modern physiognomy? *PSPB, 48*(11), 1580–1596.
38. Todorov, A., Funk, F., & Olivola, C. Y. (2015). Response to Bonnefon et al.: Limited "kernels of truth" in facial inferences. *TiCS, 19*(8), 422–423.
39. Jussim, L., Crawford, J. T., & Rubinstein, R. S. (2015). Stereotype (in)accuracy in perceptions of groups and individuals. *Current Directions, 24*(6), 490–497.
40. Jussim, L., et al. (2016). Stereotype accuracy: One of the largest and most replicable effects in all of social psychology. In *Handbook of Prejudice, Stereotyping, and Discrimination* (2nd ed.).
41. Terracciano, A., et al. (2005). National character does not reflect mean personality trait levels in 49 cultures. *Science, 310*(5745), 96–100.

**Consensus vs. accuracy**
42. Kenny, D. A. (1994). *Interpersonal Perception: A Social Relations Analysis.* Guilford.
43. Kenny, D. A., Albright, L., Malloy, T. E., & Kashy, D. A. (1994). Consensus in interpersonal perception: Acquaintance and the Big Five. *Psychological Bulletin, 116*(2), 245–258.
44. Kenny, D. A. (2004). PERSON: A general model of interpersonal perception. *PSPR, 8*(3), 265–280.
45. Albright, L., Kenny, D. A., & Malloy, T. E. (1988). Consensus in personality judgments at zero acquaintance. *JPSP, 55*(3), 387–395.
46. Cronbach, L. J. (1955). Processes affecting scores on "understanding of others" and "assumed similarity." *Psychological Bulletin, 52*(3), 177–193.
47. Furr, R. M. (2008). A framework for profile similarity. *Journal of Personality, 76*(5), 1267–1316.
48. Biesanz, J. C. (2010). The social accuracy model of interpersonal perception. *Multivariate Behavioral Research, 45*(5), 853–885.
49. Richard, F. D., Bond, C. F., Jr., & Stokes-Zoota, J. J. (2003). One hundred years of social psychology quantitatively described. *Review of General Psychology, 7*(4), 331–363.
50. Marengo, D., Montag, C., & Settanni, M. (2025). Inferring personality from social media activity using LLMs. *Journal of Personality.* (See report 01 §6.5.)

**Compensation and narcissism**
51. McCain, J. L., & Campbell, W. K. (2018). Narcissism and social media use: A meta-analytic review. *Psychology of Popular Media Culture, 7*(3), 308–327.
52. Frederick, C., & Zhang, T. (2019). Narcissism and social media usage: Is there no longer a relationship? *JASNH, 16*(1).
53. Emery, L. F., Muise, A., Dix, E. L., & Le, B. (2014). Can you tell that I'm in a relationship? Attachment and relationship visibility on Facebook. *PSPB, 40*(11), 1466–1479.
54. Buffardi, L. E., & Campbell, W. K. (2008). Narcissism and social networking web sites. *PSPB, 34*(10), 1303–1314.
