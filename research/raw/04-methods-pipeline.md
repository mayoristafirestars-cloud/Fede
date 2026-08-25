# Technical Methods for Photo-Set → Profile Pipelines
### An engineering blueprint: classic computational aesthetics, deep features, VLM profiling, aggregation, evaluation, and prompting

*Compiled 2026-08-23. Every number, formula and model name below is traced to a primary source listed in §8.*

---

## 0. Executive orientation

The literature splits into four generations, and a modern VLM pipeline should deliberately steal from all four:

| Gen | Years | Representation | Typical model | Typical effect size (Pearson/Spearman r vs self-report) |
|---|---|---|---|---|
| G1 Computational aesthetics | 2006–2014 | 56–114 hand-crafted features | SVM / LASSO / ElasticNet | r ≈ 0.10–0.26 |
| G2 Deep transfer features | 2015–2019 | fc7/penultimate 4096-d, ImageNet-1k + Places365 probabilities, tag vocabularies | ElasticNet ensemble | r ≈ 0.15–0.30 |
| G3 Zero-shot CLIP / prompt probing | 2021–2023 | CLIP embedding + text-prompt attribute axes | cosine similarity / linear probe | comparable to G2, far cheaper |
| G4 VLM (GPT-4V/4o, Gemini, Claude, LLaVA/Qwen-VL) | 2023–2026 | natural-language rubric judgments | zero-shot prompting | r ≈ 0.29 (text); ratings ~50% MC accuracy but only ~10% *grounded* |

**The single most important empirical fact in this literature**: models predict *attributed* (observer-perceived) personality far better than *self-assessed* personality. Segalin et al. report Spearman ρ up to **0.68 for attributed** traits vs **≤0.26 for self-assessed** on the identical feature set and identical corpus [S17]. In the same study, only **8.3%** of the 82 features correlated significantly with self-assessments while **48.5%** correlated significantly with attributions. Any product built on this should be honest that it models *impression*, not *personality*.

---

## 1. Classic computational-aesthetics feature sets

### 1.0 Preprocessing conventions used across all these papers

- Resize (Machajdik & Hanbury resize and **crop away borders** before anything else) [M10].
- Convert RGB → HSV (a *cylindrical* coordinate space). H ∈ [0,360°) is angular; S, V ∈ [0,1].
- Segment once, reuse: Segalin/Datta use **mean-shift** (EDISON implementation); Machajdik & Hanbury use **waterfall segmentation** (alternating sequential filter size 3, hierarchy level 2). Nearly every "region" feature depends on this one segmentation, so it is the biggest source of implementation variance between papers.

### 1.1 HSV statistics (5 features in Segalin's set)

- `use_of_light` = mean of V channel = (1/KL)·Σ V(k,l). Underexposed/overexposed photos are considered aesthetically poor. This is *identical* to Datta's f1.
- `avg_S` = mean of S = chromatic purity.
- `std_S`, `std_V`.
- **Hue circular variance** — hue is an angle so the arithmetic mean is meaningless. Use circular statistics:

```
A = Σ_k Σ_l cos(H_kl)
B = Σ_k Σ_l sin(H_kl)
R = 1 − (1/(K·L))·sqrt(A² + B²)
```

R → 0 means all pixels share one hue (monochrome); R → 1 means hues are spread around the wheel. Segalin explicitly *does not* compute mean hue because it "cannot be associated to an intensity attribute, being an angular measure" [S17]. Datta *does* (f4, f5) and admits "the interpretation of such a feature is not as clear" [D06]. **Recommendation: use circular variance, and a saturation-weighted circular mean, not a raw mean hue.**

Guntuku et al. extend this to a 32-d colour block: mean+SD of H,S,V; `h_count` (number of distinct hues) and `log(h_count)`; a normalised **12-bin hue histogram**; and a 6-bin coarse hue histogram (yellow, green, cyan, blue, magenta, red) [G18].

### 1.2 Valdez & Mehrabian emotion coordinates (Pleasure–Arousal–Dominance), 3 features

Derived from a controlled study where 250 people rated single colour patches on the PAD scale. The canonical equations (Machajdik & Hanbury Eq. 1–3, using Y = brightness, S = saturation) [M10]:

```
Pleasure   =  0.69·Y + 0.22·S
Arousal    = −0.31·Y + 0.60·S
Dominance  =  0.76·Y + 0.32·S
```

⚠️ **Known transcription divergence.** Segalin et al. print `Dominance = −0.76·V̄ + 0.32·S̄` (negative) [S17]; Guntuku et al. print `Dominance = 0.76·Brightness + 0.32·Saturation` **and** `Arousal = 0.31·Brightness + 0.60·Saturation` (positive) [G18]. Machajdik & Hanbury, closest to the psychology source, use +0.76 for Dominance and −0.31 for Arousal. **Use Machajdik's signs.** Do not silently inherit a sign error from a reimplementation; it flips the correlation direction of a whole feature.

### 1.3 Colorfulness — two incompatible definitions in circulation

**(a) Hasler & Süsstrunk (2003)** — the fast one, the one everyone means by "the colorfulness metric" [HS03]. Compute opponent channels directly in sRGB:

```
rg = R − G
yb = 0.5·(R + G) − B
σ_rgyb = sqrt(σ_rg² + σ_yb²)
μ_rgyb = sqrt(μ_rg² + μ_yb²)
C = σ_rgyb + 0.3 · μ_rgyb
```

Correlates >90% with human colorfulness ratings on their study set. Interpretation anchors from the original 7-point-scale fit (values in the same units as C): ~0 not colourful, ~15 slightly, ~33 moderately, ~45 averagely, ~59 quite, ~82 highly colourful. Cheap enough to run on every image; ~5 lines of numpy.

**(b) Datta's EMD colorfulness (f2)** — the one Segalin and Machajdik actually use [D06]:
1. Partition RGB into **64 cubes** (4 equal partitions per axis).
2. D1 = the ideal uniform distribution: frequency 1/64 in every cube.
3. D2 = the empirical frequency of the image's pixels across those 64 cubes.
4. Ground distance d(a,b) = ‖rgb2luv(c_a) − rgb2luv(c_b)‖ between cube geometric centres, converted to **LUV** (Machajdik uses CIELUV likewise).
5. `f2 = emd(D1, D2, {d(a,b)})`.

These are *not* interchangeable — (a) is a spread-of-opponent-colour measure, (b) is a distance-from-uniform-colour-occupancy measure, and Segalin's set even inverts the reported convention (`high = 1/8.16`, `low = 1/16.7`). If you re-implement, compute **both** and label them distinctly.

### 1.4 Colour names (11 features)

Assign every pixel to one of the **11 basic colour terms** — black, blue, brown, grey, green, orange, pink, purple, red, white, yellow — using van de Weijer et al.'s learned colour-naming model (which is trained to mimic how humans label chromatic information, and beats naive HSV thresholding). Feature = the fraction of pixels per class (11 values summing to 1) [S17][M10]. This is one of the most *human-interpretable* feature families and one of the strongest correlates in PsychoFlickr (orange ρ=0.45 with attributed Agreeableness, ρ=−0.56 with attributed Neuroticism).

### 1.5 Itten contrasts (20 features) — Machajdik & Hanbury only

Itten's colour sphere: 12 fundamental hues on the equator, 5 luminance levels along meridians, 3 saturation levels along the radius = 180 distinct colours. Procedure [M10]:
1. Waterfall-segment the image; compute mean H, S, V per region.
2. Map each region into the Itten model via **fuzzy membership functions** (Wang Wei-ning's definitions) so a region is e.g. "dark / low-saturation / green".
3. Compute contrasts over regions, **weighted by relative region size**:
   - *Contrast of light and dark*: size-weighted SD over the brightness membership functions of all regions.
   - *Contrast of saturation*: same construction on saturation memberships.
   - *Contrast of hue*: vector-based hue spread.
   - *Contrast of complements*: pairwise hue differences using the wheel-safe metric `d = min(|h_i − h_j|, 360 − |h_i − h_j|)`; a value near 180° indicates strong complementary contrast.
   - *Contrast of warm and cold*: assign each region 3 memberships w_t (t=1 cold, 2 neutral, 3 warm; neutral = 1 − (warm+cold)); pairwise strength = `Σ_t w_t(r1)w_t(r2) / sqrt(Σ_t w_t(r1)² · Σ_t w_t(r2)²)`. Also record total warm area and total cold area.
   - *Simultaneous contrast* = essentially the absence of complementary contrast.
   - *Contrast of extension* was **not** implemented ("insufficient understanding of its definition").
   - *Harmony*: build a 12-bin hue histogram (Itten wheel bins), discard bins with <5% support (typically leaving 3–4 dominant hues), connect their wheel positions into a polygon, and measure harmony as the difference between that polygon's internal angles and those of a regular polygon with the same number of vertices.
4. Record the **average and the maximum** of each contrast → 20 features.

### 1.6 Composition features

| Feature | Definition | Dim |
|---|---|---|
| Edge pixels | Fraction of pixels lying on a **Canny** edge | 1 |
| Level of detail | Number of segments after mean-shift (Segalin) / waterfall (Machajdik). Low for minimalist images, high for cluttered ones | 1 |
| Average region size | Mean segment area ÷ total image area | 1 |
| Rule of thirds | Mean of S and of V (and hue, in Datta) over the **central 1/9 block** | 2–3 |
| Low depth of field | High-frequency wavelet energy in the central blocks vs the whole frame | 3 (H,S,V) |
| Dynamics | Hough-transform line slopes classified static vs slant, weighted by length | 6 |
| Image size / aspect ratio | f22 = X+Y; f23 = X/Y | 1–2 |

**Rule of thirds, exact form** (Segalin Eq. 5; Datta f5–f7) — note the 9/(KL) normaliser because the inner block is 1/9 of the image:

```
f_S = (9/(K·L)) · Σ_{k=K/3}^{2K/3} Σ_{l=L/3}^{2L/3} S(k,l)
```

**Low depth-of-field indicator, exact form** (Datta f53–f55; Segalin Eq. 4). Split the image into 16 equal blocks M1…M16 in row-major order; the four *central* blocks are M6, M7, M10, M11. Let w3 = {w3^HL, w3^LH, w3^HH} be the level-3 (finest / high-frequency) wavelet coefficients of the hue channel:

```
DOF_H = Σ_{(k,l) ∈ M6∪M7∪M10∪M11} w3(k,l)  /  Σ_{i=1..16} Σ_{(k,l) ∈ Mi} w3(k,l)
```

High DOF_H ⇒ sharp centre, blurred surround ⇒ macro/portrait/telephoto shot. Repeat for S and V channels. **Judgeable by eye**: "is the subject sharp while the background is soft?"

**Dynamics** (Machajdik only): detect lines with the Hough transform; classify a line as *static* if its tilt θ satisfies (−15° < θ < 15°) or (75° < θ < 105°), else *slant/dynamic*; weight by line length. Output = proportion static, proportion dynamic (absolute and relative), total length of static lines, total length of dynamic lines. Art-theory rationale: horizontals = calm, verticals = dignity, slants = dynamism, many directions = chaos.

### 1.7 Texture features

**Daubechies wavelet textures (9 or 12 features).** Three-level 2D-DWT on **each** of H, S, V separately. At level i ∈ {1,2,3} you get horizontal (LH), vertical (HL) and diagonal (HH) sub-bands, written w_i^h, w_i^v, w_i^d. The feature is the mean magnitude of the high-frequency coefficients (Datta Eq. for f10–f18; Machajdik Eq. 4; Segalin Eq. 6):

```
wf_i = ( Σ_{k,l} w_i^h(k,l) + Σ_{k,l} w_i^v(k,l) + Σ_{k,l} w_i^d(k,l) )
       / ( |w_i^h| + |w_i^v| + |w_i^d| )
```

where |·| is the spatial area of the sub-band. That is 3 levels × 3 channels = **9 features**, plus **3 more** as the per-channel sum across levels (`f19 = f10+f11+f12`, etc.) = **12 total**. High values ⇒ grainy/high edge density; low ⇒ smooth/out-of-focus.

**Tamura (3 features).** Tamura et al. proposed six; everyone uses the first three: coarseness, contrast, directionality [S17][M10].
Coarseness `F_crs`, exactly:
1. For every pixel (n0,n1) average over neighbourhoods of size 2^k × 2^k (k = 1…5, i.e. 2×2 … 32×32):
   `A_k(n0,n1) = (1/2^{2k}) ΣΣ X(n0 − 2^{k−1} + i, n1 − 2^{k−1} + j)`
2. Differences between non-overlapping neighbourhoods on opposite sides:
   `E_k^h = |A_k(n0 + 2^{k−1}, n1) − A_k(n0 − 2^{k−1}, n1)|`, similarly `E_k^v`
3. `S(n0,n1) = argmax_{k=1..5} max_{d∈{h,v}} E_k^d(n0,n1)`
4. `F_crs = (1/(N0·N1)) Σ 2^{S(n0,n1)}`

Contrast and directionality follow Tamura's standard definitions on grey-level images.

**GLCM (12 features).** Grey-Level Co-occurrence Matrix per HSV channel; from each matrix extract **contrast, correlation, energy, homogeneity** → 4 × 3 channels = 12 [S17][M10]. Correlation ranges in [−1,1]; energy in (0,1] with 1 = perfectly uniform texture.

**Grey distribution entropy (1 feature).** Convert to grey; for each pixel compute the grey-level histogram over a **9×9** neighbourhood and its entropy; sum all entropies and divide by image size. Low = uniform intensity [S17].

### 1.8 GIST (24 features in Segalin's set; 512 in the canonical form)

Oliva & Torralba's holistic "spatial envelope" scene descriptor [OT01]. Canonical implementation: grayscale, resize to 128×128 (or 256×256), convolve with a Gabor filter bank of **4 scales × 8 orientations = 32 filters**, average each filter's magnitude response over a **4×4 spatial grid** → 32 × 16 = **512 dimensions** (×3 for colour = 1536). Segalin compresses this to **24 "GIST channels"** [S17]. GIST is the cheapest way to encode "what kind of scene layout is this" (open/closed, natural/man-made, rough/smooth) without object recognition — but in 2026 Places365 does the same job better and more interpretably (§2.2).

### 1.9 Content features

- **Faces**: Segalin uses a single feature = number of faces, and notes it was *extracted manually* over all 60,000 pictures [S17] — worth knowing, because a modern detector will not reproduce their exact numbers. Machajdik uses Viola–Jones: number of frontal faces + relative size of the largest face (2 features).
- **Skin**: number of skin pixels + relative skin amount w.r.t. face size (2 features), via a static YCbCr threshold model. Originally a nude-art detector.

### 1.10 Datta et al. 2006 — the full f1…f56 [D06]

| Feature | Definition |
|---|---|
| f1 | Average pixel intensity of V = "use of light" |
| f2 | EMD colorfulness vs uniform 64-cube distribution in LUV (§1.3b) |
| f3 | Average saturation |
| f4 | Average hue (acknowledged as weakly interpretable) |
| f5, f6, f7 | Rule-of-thirds: mean H, S, V over the inner 1/9 rectangle |
| f8, f9 | **Familiarity**: mean IRM (Integrated Region Matching) distance to the top-20 and top-100 nearest images in an anchor database. Higher = more unusual/original |
| f10–f12 | Hue wavelet features, levels 1–3 |
| f13–f15 | Saturation wavelet features, levels 1–3 |
| f16–f18 | Intensity wavelet features, levels 1–3 |
| f19, f20, f21 | Per-channel sums of the three levels |
| f22 | Size = X + Y |
| f23 | Aspect ratio = X / Y |
| f24 | Number of the 5 largest connected patches with \|s_i\| ≥ XY/100 |
| f25 | Number of K-Means colour clusters in LUV (chosen dynamically by image complexity) |
| f26–f30 | Mean H of each of the top-5 patches |
| f31–f35 | Mean S of each of the top-5 patches |
| f36–f40 | Mean V of each of the top-5 patches |
| f41–f45 | Relative size of each of the top-5 patches = \|s_i\|/(XY) |
| f46 | Σ_i Σ_j \|h_i − h_j\| over the 5 patch hues — colour spread around the wheel |
| f47 | Σ_i Σ_j l(\|h_i − h_j\|) where l(k)=k if k≤180°, else 360−k — complementarity |
| f48–f52 | Coarse position of each patch centroid: 10r + c on the 3×3 grid |
| f53, f54, f55 | Low-DOF indicators for H, S, V (§1.6 formula) |
| f56 | **Shape convexity**: segment into patches p_k with \|p_k\| ≥ XY/200; compute convex hull g(p_k); `f56 = (1/XY) · Σ_k I(\|p_k\|/\|g(p_k)\| ≥ 0.8) · \|p_k\|` — the fraction of the image covered by approximately convex homogeneous regions |

**Datta's results** (worth quoting when calibrating expectations): 3,581 photo.net images, classes split at aesthetics score >5.8 (high) vs <4.2 (low), balanced to 1,664 samples, RBF-SVM, 5-fold CV. **Best single feature = f31 (mean saturation of the largest patch) at 59.3% accuracy.** Filter+wrapper selection of 15 features {f31, f1, f54, f28, f43, f25, f22, f17, f15, f20, f2, f9, f21, f23, f6} reached **70.12% accuracy** (precision 68.08% high / 72.31% low). Accuracy rises monotonically with the minimum number of unique human ratings per photo and with the inter-class gap δ — i.e. **most of the apparent difficulty is ground-truth noise, not model capacity.** That lesson transfers directly to personality work.

### 1.11 Segalin et al.'s 82-feature set (PsychoFlickr) — the one to copy [S17]

| Category | Feature | d |
|---|---|---|
| Color | HSV statistics (mean S, SD of S and V, hue circular variance, use of light) | 5 |
| Color | Emotion-based (valence, arousal, dominance) | 3 |
| Color | Color diversity (EMD vs uniform histogram in CIELUV) | 1 |
| Color | Color names (11 basic colours) | 11 |
| Composition | Edge pixels (Canny) | 1 |
| Composition | Level of detail (# mean-shift regions) | 1 |
| Composition | Average region size | 1 |
| Composition | Low depth of field (H, S, V) | 3 |
| Composition | Rule of thirds (S, V of inner rectangle) | 2 |
| Composition | Image size | 1 |
| Texture | Grey distribution entropy | 1 |
| Texture | Wavelet textures (3 levels × 3 channels + 3 sums) | 12 |
| Texture | Tamura (coarseness, contrast, directionality) | 3 |
| Texture | GLCM (contrast, correlation, energy, homogeneity × HSV) | 12 |
| Texture | GIST descriptors | 24 |
| Content | Number of faces | 1 |
| | **Total** | **82** |

Deliberately **excludes** SIFT/HOG because "they do not account for aesthetic preferences," and excludes semantic content except face count "to make the process more robust with respect to the wide semantic variability of Flickr images."

### 1.12 Machajdik & Hanbury's 114-feature emotion set [M10]

| Category | Feature | # |
|---|---|---|
| Color | Saturation, Brightness (means) | 2 |
| Color | Pleasure, Arousal, Dominance | 3 |
| Color | Hue (vector mean + angular dispersion, saturation-weighted and unweighted) | 4 |
| Color | Colorfulness (EMD) | 1 |
| Color | Color names | 11 |
| Color | Itten (avg + max of each contrast, harmony, hue count, hue spread, warm/cold area) | 20 |
| Color | Wang Wei-ning histograms (factor1 ×10, factor2 ×7, factor3 ×2) | 19 |
| Color | Area statistics (very dark/dark/middle/light/very light, high/mid/low saturation, warm, cold) | 10 |
| Texture | Tamura (coarseness, contrast, directionality) | 3 |
| Texture | Wavelet textures | 12 |
| Texture | GLCM | 12 |
| Composition | Level of detail (waterfall segment count) | 1 |
| Composition | Low depth of field (H, S, V) | 3 |
| Composition | Dynamics (static/dynamic line slopes, absolute and relative, lengths) | 6 |
| Composition | Rule of thirds (mean S, V, H of inner rectangle) | 3 |
| Content | Faces (count, relative size of largest) | 2 |
| Content | Skin (pixel count, relative amount w.r.t. face size) | 2 |
| | **Total** | **114** |

Evaluated on three sets: **IAPS-Subset** (394 of the International Affective Picture System images, categorised into discrete emotions), **ArtPhoto** (807 artistic photographs, emotion label = the uploading artist's own search-term category), and **Abstract Paintings** (280 peer-rated by ~230 people, ~14 ratings each; 228 retained after dropping images with inconclusive votes). The design of the abstract-painting set is a good template: *drop items where human raters disagree*, rather than forcing a majority label.

---

## 2. Deep-feature approaches

### 2.1 ImageNet object tags and generic CNN features

- **Generic penultimate features**: extract the 4096-d fc7 activations of an ImageNet-trained network (Segalin used Caffe + the AlexNet-style "ImageNet network" trained on 1.3M images for ILSVRC-2012 [S17b]; Guntuku used VGGNet-16/19 [G18]). In Segalin's Facebook study these were **the single best-performing family**, beating hand-crafted aesthetics.
- **Object probabilities**: the 1000-way softmax over ImageNet classes, used directly as a 1000-d feature.
- Guntuku's verdict is important and non-obvious: **CNN_Obj (ImageNet+Places probabilities) wins for *profile* images; CNN_Gen (penultimate) and open-vocabulary tags win for *posted* images**, "because posted images contain a very diverse array of objects and subjects — as opposed to profile pictures — which are best captured by general image content features. CNN_Obj are not as good predictors probably due to the lack of diversity of the ImageNet categories, which do not include usual objects and subjects encountered in social media images" [G18]. **ImageNet-1k is a bad ontology for social photos.**

### 2.2 Scene understanding: Places365

Places365-Standard: **1.8M training images, 365 scene categories**, part of the 10M-image Places database [Z18]. Available pretrained backbones: AlexNet, ResNet18, ResNet50, DenseNet161 (PyTorch); AlexNet, GoogLeNet, VGG16, ResNet152 (Caffe). Fine-tuned ResNet152 reaches **85.08% top-5** on Places365-Standard val.

The critical practical artefact is `run_placesCNN_unified.py`, which emits four things per image:
1. **Indoor/outdoor (IO)** binary — derived from a per-category IO label vector.
2. **Top-k of 365 scene categories** with probabilities.
3. **Scene attributes** — a linear regressor `W_attribute` over the penultimate features projecting into the **102 SUN scene attributes** (Patterson & Hays); the demo prints the top ~9, e.g. "no horizon, enclosed area, man-made, socializing, indoor lighting, cloth, congregating, eating, working".
4. **Class Activation Map** for where the evidence is.

Those 102 SUN attributes are exceptionally well suited as an interpretable, aggregate-able per-user vector (mean over a user's photos → "this person's photos are 62% outdoor, high on 'natural light', 'open area', 'vacationing'"). **This is the single best off-the-shelf mid-level vocabulary in the classic stack.**

### 2.3 Face detection and attribute analysis

The image-personality literature relies heavily on faces because face count alone carries the strongest single classic signal: in PsychoFlickr, **number of faces ↔ attributed Extraversion ρ = 0.53**, and ↔ attributed Neuroticism ρ = −0.28 [S17].

Feature families used by Liu, Preoţiuc-Pietro et al. (ICWSM 2016) on 66,502 Twitter profile pictures, via **Face++** and **EmoVu** APIs [L16]:
- **Image type** (5 features): number of faces; whether the profile picture is a Twitter default; binary "exactly one face"; binary "multiple faces". *Despite being only 5 features, this was the most useful category for prediction on the large dataset.*
- **Image demographics**: estimated age, gender, race (Asian / Black / White).
- **Facial presentation**: face ratio (face area ÷ image area), glasses (reading/sun), subject-to-sensor closeness, **3-D head pose (pitch, roll, yaw)**, eye openness.
- **Facial expressions** (14 features): Ekman's six (anger, disgust, fear, joy, sadness, surprise) + neutral, plus composites — *expressiveness* = max of the six basics; *positive mood* = max of {joy, surprise}; *negative mood* = max of the four negatives; *valence* = mean of positive and negative mood; plus Face++ *smiling degree*.

**Detection-coverage reality check** (plan for this): Face++ found ≥1 face in only **36,402 / 66,502 (55%)** profile images, and EmoVu produced emotion scores for only **26,234 / 66,502 (39%)** — "low image quality, very small face, or the face being obstructed or not facing the camera." Their handling: **impute the sample mean when a feature could not be extracted**, and add an explicit missingness indicator. A modern pipeline should treat "no face detected" as a *feature*, not a failure.

For a self-hosted stack in 2026: RetinaFace/SCRFD or MediaPipe for detection, InsightFace/ArcFace embeddings for identity clustering (see §4.6), and **FairFace** [KJ21] for demographics if you must — 108,501 images, 7 balanced race groups (White, Black, Indian, East Asian, Southeast Asian, Middle East, Latino), reported **gender 94%, race 93.7% White / 75.4% non-White, age-group only ~60%** accuracy, with cross-domain 95.7% gender / 81.5% race. Note the ~34-point White-vs-non-White race gap and the poor age performance: these are *the* numbers to cite when refusing to expose demographic inference as a product feature.

### 2.4 Aesthetic scoring models: NIMA

NIMA (Talebi & Milanfar, IEEE TIP 2018) [TM18] replaced binary "good/bad photo" classification with **distribution prediction**. Train on **AVA** (≈255,500 images, each rated by ~200 people on a 1–10 scale); the head is a 10-way softmax over score buckets; the loss is the closed-form squared **Earth Mover's Distance**:

```
EMD(p, p̂) = ( (1/N) · Σ_{k=1..N} |CDF_p(k) − CDF_p̂(k)|^r )^(1/r)
```

with N = 10 ordered buckets and r = 2 for training (r = 1 for reporting). Softmax guarantees equal mass. Output = mean score (Σ i·p̂_i) **and** SD (a free, useful "how controversial is this photo" signal).

Reported on the AVA test set:

| Model | Binary acc. | LCC (mean score) | SRCC (mean score) | LCC (SD) | SRCC (SD) | EMD |
|---|---|---|---|---|---|---|
| NIMA(MobileNet) | 80.36% | 0.518 | 0.510 | 0.152 | 0.137 | 0.081 |
| NIMA(VGG16) | 80.60% | 0.610 | 0.592 | 0.205 | 0.202 | 0.052 |
| NIMA(Inception-v2) | **81.51%** | **0.636** | **0.612** | **0.233** | **0.218** | **0.050** |

MobileNet is only ~1 point behind on binary accuracy at a fraction of the cost — fine for bulk pre-scoring of a large photo set.

### 2.5 VLM-native aesthetic/quality scoring: Q-Align

Q-Align (ICML 2024) [QA24] is the modern replacement for NIMA and the **key trick to steal for any VLM rating task**: don't ask the model for a number. Fine-tune / prompt it to emit one of **five discrete text-defined levels** ("bad, poor, fair, good, excellent"), read the **token log-probabilities** of those five level words, softmax them, and take the **probability-weighted average** to recover a continuous score. This is the LMM analogue of NIMA's distribution head. It attains SOTA on IQA, IAA and VQA under the plain LMM architecture and generalises better cross-dataset; the unified ONEALIGN model handles all three. **Applies verbatim to trait rating: ask for a Likert word, harvest the distribution, weight-average.** It also gives you an uncertainty estimate for free (entropy of the 5-way distribution).

### 2.6 CLIP embeddings and zero-shot attribute probing

Standard recipe [R21]:
1. Encode the image → `v` (normalised).
2. Encode a set of text prompts describing each attribute value → `t_c` (normalised).
3. Score = cosine(v, t_c), softmaxed with the learned temperature.

Two techniques that matter:
- **Prompt engineering + ensembling**: average the *embeddings* of many paraphrased templates ("a photo of a {}", "a bad photo of a {}", …) and cache the result. This adds **~5 points on average across 36 datasets** vs a bare class name — essentially free accuracy.
- **Linear probe > zero-shot** when you have any labels. Zero-shot CLIP beats a fully-supervised ResNet-50 linear probe on 16/27 datasets, but a *CLIP* linear probe beats zero-shot CLIP nearly everywhere.

For a photo-set profiler, the highest-value use is **bipolar attribute axes**: define opposing prompt pairs ("a candid snapshot" vs "a carefully composed photograph"; "a photo taken indoors at night" vs "a photo taken outdoors in daylight"; "a picture of a large group of friends" vs "a picture of one person alone") and take the signed difference of similarities. This gives continuous, cheap, dense, *nameable* axes that aggregate well over N photos and can be validated independently of the VLM.

Two published cautions: CLIP misclassifies images of Black individuals at a higher rate (~14%) than other racial groups (<8%), and CLIP-family social-trait judgments of faces reproduce human *stereotype* structure rather than any validated trait signal [SP24].

### 2.7 Open-vocabulary tags and adjective-noun pairs

- **Imagga auto-tagging API** as used by Guntuku: take the **top-10 predicted tags** per image (the vendor's own recommendation), build a bag-of-tags, then **drop any tag occurring fewer than 200 times in the corpus**, leaving **1,299 distinct tags** [G18]. The frequency floor is the important detail — it is what stops the long tail from generating spurious correlations.
- **SentiBank / Adjective-Noun Pairs (ANPs)**: ~1,200 visual concepts of the form "beautiful sky", "creepy doll", built for visual sentiment; a good intermediate vocabulary between raw objects and abstract traits.
- **2026 equivalent**: an open-vocabulary detector (OWLv2 / Grounding DINO) or a VLM captioner is strictly more expressive; but keep the frequency floor and keep the vocabulary *closed at analysis time* so features are comparable across users.

---

## 3. VLM-based profiling, 2023–2026

### 3.1 The headline numbers

| Study | Input | Model | Result |
|---|---|---|---|
| Peters & Matz, *PNAS Nexus* 2024 [PM24] | Facebook status text | GPT-3.5 / GPT-4 zero-shot | **r = 0.29 avg** (range 0.22–0.33) vs self-reported Big Five — "similar to supervised ML models specifically trained to infer personality" |
| Personality Computing survey 2025 [PC25] | mixed | supervised SOTA | avg r ≈ 0.30 (WASSA2024), baseline 0.133 |
| Same survey, perception meta-analysis | mixed | computer systems ρ = 0.30 vs **human judges ρ = 0.38** | machines still behind humans at *perception* |
| Interview benchmark 2025 [IB25] | 555 semi-structured interviews + BFI-10 | GPT-5-Mini, GPT-4.1-Mini, Llama, DeepSeek, zero-shot + CoT | **high internal consistency across repeated runs but weak alignment with self-report, r ≤ 0.27** |
| Staab et al., ICLR 2024 [ST24] | Reddit comment text | 9 LLMs | **85% top-1 / 95.8% top-3** on personal attributes (location, income, sex) at **100× lower cost and 240× faster** than human annotators; text anonymisation and model alignment both failed as mitigations |
| Web-browsing LLMs 2025 [WB25] | live social profiles | GPT-4o, o3, Llama-3-8B-Web | gender most reliable; **age hardest**; political orientation least accurate |

**Read those two rows together**: *demographics and stated facts* are inferred with alarming accuracy; *latent psychological traits* are inferred at r ≈ 0.2–0.3 — real, but explaining under 10% of variance. Build the product around the first only if you intend to, and price the second honestly.

### 3.2 The decisive VLM-specific result: MM-OCEAN and the "prejudice gap"

MM-OCEAN [MO26] is the most directly relevant recent benchmark. **1,104 videos from ChaLearn First Impressions V2**, 5,320 multiple-choice questions across 7 cognitive categories, ~13.5K human-verified behavioural observations, 5,520 trait analyses, timestamped cue annotations over four perceptual channels (Expression, Action, Audio, Background). **27 models** evaluated: 13 proprietary (GPT-5.5, Gemini 3 Flash, Claude Opus 4.6) and 14 open-source (Qwen3.5-397B, Llama-4-Maverick, InternVL3), with standardised prompts and uniform frame sampling.

Three-tier protocol — **T1 rate → T2 reason → T3 ground the cue**:

| Tier | Metric | Mean |
|---|---|---|
| T1 Rating | accuracy | 50.1% (MAE 0.61) |
| T2 Reasoning | AI-as-judge, 4 dimensions | 6.17 / 10 |
| T3 Cue grounding | accuracy | 39.4% |

Four diagnostic failure rates, defined as conditional probabilities:

- **Prejudice Rate (PR) ≈ 51.3%** — *right rating, ungrounded cues*. Over half of correct trait ratings are correct without any grounded visual evidence.
- **Confabulation Rate (CR) ≈ 52%** — plausible-sounding reasoning citing the wrong evidence.
- **Integration-failure Rate (IR) ≈ 46%** — correct cues retrieved, wrong trait rating derived.
- **Holistic-Grounding Rate (HR) ≈ 10.4%** — all three tiers correct. Best model (Gemini 3 Flash) reaches only **33.5%**.

Per-category bottlenecks: spatial localisation 30.7% and micro-expression detection 34.6% are far harder than temporal-causal reasoning 64.8%. Proprietary−open-source gap on cue retrieval: **ΔT3 = −26.6 points**.

Model archetypes worth designing around: **"Confident Raters"** (strong T1, collapse on T2/T3) vs **"Cautious Reasoners"** (weak T1, strong grounding).

> **The engineering takeaway**: a VLM's trait rating being *right* is nearly uninformative about whether it is *reasoning*. If your product shows evidence to users, you must verify the evidence separately from the rating — a rating-only eval will pass a system that is ~50% stereotype.

### 3.3 Known failure modes and what fixes them

| Failure mode | Evidence | Mitigation with published support |
|---|---|---|
| **Sycophancy / answer flipping** | Under social pressure, **40–75% of initially correct answers flip** in medical VLMs across 16 models and 7 pressure types [EB25]. SYCON-Bench measures Turn-of-Flip and Number-of-Flip [SY25]. | **Third-person framing reduces sycophancy by up to 63.8%**; reasoning-optimised and larger models resist better. Never let the user's stated hypothesis about themselves enter the judging prompt. |
| **Stereotyping** | VLMs encode occupation/gender/race stereotypes; GRAS benchmarks gender, race, age and **Monk Skin Tone**; FOCUS uses face-only counterfactuals (480 images, 6 occupations × 10 race-gender groups). **Higher faithfulness does not imply lower bias** [GRAS25][FOCUS26]. | Counterfactual probing: swap the demographic-bearing region/prompt and require the trait output to be invariant. Report the delta. |
| **Hallucinated confidence** | LLMs are "poorly calibrated when reporting their own confidence" [XI24]. MM-OCEAN's 51% prejudice rate is the visual analogue. | Q-Align-style token-probability scoring (§2.5) instead of verbalised numbers; self-consistency (coherence among sampled generations correlates with correctness). |
| **Prompt / rubric sensitivity** | Semantically-preserving prompt edits substantially alter judgments; reordering options induces **serial-position bias**; changing rubric or attribute order creates **anchoring** shifts in the score distribution [JJ25]. | Fix the rubric text; randomise item order across runs and average; report divergence — **>20–25% divergence signals the rubric needs recalibration**. |
| **Multi-image collapse** | Controlled analysis across LLaVA-OV (0.5/1.5/7/72B), Qwen2-VL (2/7B), InternVL2 (2/8B), Qwen3-VL-8B: accuracy falls from **79.0% with 1 query image to 66.5% with 34 distractors**; inter-image attention *diminishes in deeper layers*; models "primarily behave as single-image models", peaking when the vision-token sequence matches 1–2 images [MI26]. | **Do not stuff N photos into one prompt.** Score per-image, aggregate outside the model (§4). |
| **Aggregation/tracking breakdown** | Degradation begins "even with just 2–3 images containing target objects" when information is *distributed* [MI26]. | Same. |

### 3.4 Calibration techniques worth implementing

1. **Token-distribution scoring (Q-Align)** — constrain output to k ordered level words, softmax their logprobs, take the weighted mean and the entropy. Gives a continuous score *and* a calibrated-ish uncertainty in one forward pass.
2. **Self-consistency** — sample m ≥ 5 judgments at T > 0; the mean is the estimate, the SD is the uncertainty. Coherence across samples is the empirically strongest correctness signal [XI24].
3. **Post-hoc affine recalibration** — on a held-out labelled set, fit `ŷ_cal = a·ŷ + b` per trait (or isotonic regression). Because VLM trait outputs are typically range-compressed and centred high, this alone recovers a surprising amount of correlation.
4. **Abstention / selective prediction** — hallucination detection lets the system emit "I don't know", "significantly improving overall system reliability" [AB25]. Set a coverage target (e.g. answer on 70% of items) and tune the uncertainty threshold to it; report accuracy-at-coverage, not accuracy alone.
5. **Bias-corrected judging / IRT** — the 2025–26 frontier applies confidence intervals accounting for imperfect judge sensitivity/specificity, and item-response theory *to the rubric items themselves*, to find which items are too easy, too ambiguous, or too judge-sensitive [RV26].

---

## 4. Aggregation: from N photos to ONE profile

This is the least-documented and most consequential design decision. The literature offers seven distinct strategies, and Segalin et al. benchmarked six of them head-to-head on identical data.

### 4.1 Mean feature pooling (the default)

Guntuku et al.: "for liked and posted images we perform a **mean feature pooling** of all liked and posted images each across all images per user" [G18]. Simple, robust, and what almost everyone does. Corpus scale for calibration:

| Dataset | Modality | Total images | Mean / user | Median / user |
|---|---|---|---|---|
| PsychoFlickr | Posts | 72,997 | 247 | 170 |
| PsychoFlickr | Likes | 60,001 | 203 | 200 |
| Cross-linked Flickr | Posts | 60,381 | 175 | 56 |
| Cross-linked Flickr | Likes | 28,658 | 83 | 45 |
| Cross-linked Twitter | Posts | 73,576 | 213 | 199 |
| Cross-linked Twitter | Likes | 29,030 | 84 | 82 |

**Extend the mean**: for every scalar feature also carry **SD, median, and selected quantiles (p10, p90)**. Mean colour saturation tells you the palette; *variance* of saturation tells you whether the person shoots one consistent look or ranges wildly — which is arguably the more trait-like signal and is thrown away by mean-only pooling. Reece & Danforth chose a different granularity entirely: aggregate to **per-person, per-day units of observation** (18,513 aggregated units from 43,950 posts by 166 people), which preserves within-person temporal variation while smoothing single-photo noise [RD17].

### 4.2 Quantise to counts, then use a topic model

Segalin's key move: **quantise each of the 82 features into Q uniform, non-overlapping intervals** whose boundaries are computed on the training set. Each picture then becomes a vector of counts (a bag-of-features), and each user becomes a **bag of 200 such pictures** [S17]. This unlocks the whole topic-model toolbox.

### 4.3 The six Multiple-Instance Regression aggregators, benchmarked

Each user u is a bag B_u of favourite pictures with one label y_u per trait. Final regression in every case is linear with **LASSO** (L1) regularisation, `ŷ_u = Σ_k β_k x_u^k`, minimising MSE:

| Method | Aggregation mechanism |
|---|---|
| **Naive-MIR** | Feed *every* picture of the bag to the regressor; average. Assumes all pictures carry task-relevant information. |
| **cit-kNN** | For a test bag, find its R nearest-neighbour training bags *and* its C nearest "citers" (training bags that have B_u among their C nearest neighbours); average their scores. No regression step. |
| **Clust-Reg** | k-means the training-bag images into C centroids; for each bag, average the images falling in each cluster → C prototypes; regress. |
| **Topic-Sum** | Sum topic assignments over the bag. |
| **Gen-MoG** | Fit a C-component Gaussian mixture over training images; `Z_u(c) = Σ_{t ∈ B_u} p(c|t)` — soft assignment of every image to every component. Regress on Z_u. |
| **Gen-LDA** | Fit LDA over the quantised bags-of-features; represent a test bag by its Dirichlet parameters α_u; regress on α_u. **Best overall performer.** |
| **Counting Grid (CG)** | Embed each image on a 2-D smooth manifold grid (E1×E2 ≪ N); a bag becomes a distribution of locations on the grid, smoothed with a **5×5 window**; regress on the flattened grid. |

Hyper-parameter search ranges actually used: cit-kNN C ∈ [4,10], R ∈ [2,8]; Clust-Reg / Gen-MoG C ∈ {5,10,20,…,100}; Topic-Sum / Gen-LDA K ∈ {50,70,90,110,130,150}; CG grid ∈ {20×20, 25×25, …, 65×65}.

**Findings that generalise** [S17]:
- The **weakest** methods (cit-kNN, Clust-Reg) are precisely those that make **hard decisions to exclude part of the bag**. The best combine soft generative assignment with sparsity-controlled regression.
- **Naive-MIR performs well**, confirming that *all* images in a bag influence the attributed traits — either because every picture shapes each judge's impression, or because different judges are influenced by different subsets and the averaged attribution therefore depends on all of them.
- Best performance ≈ **ρ 0.6–0.68 on attributed traits** (Gen-LDA best overall; CG and Gen-MoG close); **≤0.26 on self-assessed**. Extraversion is the best-predicted trait on both (most socially oriented ⇒ leaves the most observable traces); Openness is worst (judges themselves are most uncertain about it).

**Design implication for a VLM pipeline**: *do not select "the most representative photos" and discard the rest.* Soft-weight everything. If you must subsample for cost, sample randomly/stratified, don't cherry-pick.

### 4.4 How many photos are needed?

This is directly measured in exactly one place. Segalin et al. plot performance vs **test-bag size** and **training-bag size** [S17]:

> "In both cases, the performance grows with the number of pictures, but **statistically significant performances can still be achieved with small bag sizes, i.e. 5 in the case of the training set and 1 in the case of the test set.**"

Performance rises from ρ ≈ 0.2–0.3 at very small bag sizes toward ρ ≈ 0.6–0.7 and is essentially saturating by ~150–200 pictures. Practical reading: **1 photo yields a signal; ~20–30 gets you most of the way; ~100–200 saturates.** Below ~10 photos, report wide uncertainty and suppress fine-grained claims.

Supporting evidence from adjacent work:
- Liu et al. required users to have posted **≥50 tweets** before trusting a text-derived personality estimate [L16].
- Split-half reliability of social-media-derived trait estimates ranges **r = 0.84–0.88** when enough content is present [SM23] — that is the ceiling your aggregation should be measured against.
- Guntuku ran every experiment with **100 randomised dataset splits** and reported SD < 0.001 — the right way to demonstrate that an aggregate estimate is stable [G18].

**Concrete recommendation**: implement a **bootstrap over the user's own photos**. Resample the photo set with replacement B = 200 times, re-aggregate, and report the 5th–95th percentile of each trait score. If that interval spans more than ~1 point on a 5-point scale, do not display a point estimate. This is cheap (aggregation is post-hoc) and it converts "how many photos are enough" from a guess into a per-user measurement.

### 4.5 Temporal / sequence modelling

Little of the image-personality literature models time explicitly; the one clean pattern is Reece & Danforth's **per-person-per-day aggregation** [RD17], which turns a photo stream into a longitudinal panel and permits Bayesian logistic regression with uninformative priors on per-day units. Crucially, their depression result **held when restricted to posts made *before* first clinical diagnosis** — a genuine prospective validation design that image-profiling work should imitate: split a user's timeline and check that early photos predict a later-measured outcome.

Practical temporal features worth carrying per user:
- Posting cadence: posts/week, burstiness (inter-post interval CV), longest gap.
- Circadian: histogram of EXIF/post hour-of-day.
- **Drift**: cosine distance between the mean CLIP embedding of the earliest third and the latest third of the set — a direct measure of "has this person's visual world changed".
- Seasonality and location spread (EXIF GPS, if present — and note that this is exactly the attribute VLMs infer far too well, §3.1).

### 4.6 Reposts, memes, and non-original content

Nothing in the classic literature handles this, and it is a serious validity threat: a feature set computed over a user's *reposted memes* measures the meme factory's aesthetics, not the user's. Build an explicit provenance filter:

1. **Near-duplicate / repost detection.** Perceptual hashing (pHash, dHash) catches exact and lightly-transformed duplicates cheaply, but "performance drastically declines for near-duplicate and transformed scenarios, especially with geometric modifications like rotation or cropping"; **CNN/CLIP embedding similarity consistently outperforms hashing on near-duplicates and transformed images** because it captures semantic rather than pixel structure [ND25]. Use pHash as a fast pre-filter and CLIP-embedding cosine (threshold tuned on a held-out set) as the decider. Cross-user duplicate detection is the strongest repost signal: an image that appears in many unrelated users' sets is not that user's.
2. **Meme classification.** MemeTector-style classifiers separate memes from regular images by detecting the meme *template structure* (impact-font caption bands, screenshot borders, aspect-ratio quantisation) [MT23]. Cheap heuristic proxies: detected overlaid text area fraction (any OCR), exact-JPEG-recompression artefacts, non-camera aspect ratios, missing EXIF.
3. **EXIF as provenance.** Presence of camera make/model/lens/ISO/focal length is strong evidence of an original capture; its absence is weak evidence of a repost (platforms strip EXIF). Screenshot detection: exact device screen dimensions.
4. **Self-authorship signals.** Face-identity clustering (ArcFace embeddings + clustering) identifies the account's *modal* face; photos containing it are near-certainly self-related. Selfie detection can additionally key on arm-along-the-frame-perimeter geometry [SEL17].
5. **Handling, not just detection.** Do not simply delete non-original images — *route* them. Reposts and memes are informative about **taste and identity signalling** (this is precisely what PsychoFlickr's "favourite pictures" measure), just not about the person's environment, appearance or behaviour. Keep three buckets — **originals / reposts-and-memes / ambiguous** — and compute the feature aggregate separately in each, then let the profile cite which bucket each claim rests on.

### 4.7 Why aggregation must happen *outside* the VLM

Restating §3.3 as a design rule, because it is the crux: current VLMs "primarily behave as single-image models," inter-image attention diminishes in deeper layers, accuracy on distributed information drops from 79.0% → 66.5% under 34 distractors, and degradation begins at 2–3 images [MI26]. Therefore:

> **Score each photo independently with the VLM into a fixed structured schema; aggregate the structured records with ordinary statistics; then use a second, text-only LLM pass over the aggregate table to write the profile.** Never ask a VLM to look at 100 photos and summarise a person.

This also happens to be the architecture that makes the whole thing auditable: every claim in the final profile traces to specific rows of the per-photo table.

---

## 5. Evaluation

### 5.1 Ground-truth instruments actually used

| Instrument | Items | Used by |
|---|---|---|
| **BFI-10** | 10 (2 per trait, one reverse-keyed) — fillable in under a minute | Segalin PsychoFlickr, both self-assessment and attribution versions [S17] |
| **IPIP** (International Personality Item Pool) | variable (20–300) | Segalin Facebook / myPersonality [S17b] |
| **100-item questionnaire** | 100 | Youyou/Kosinski/Stillwell, n = 86,220 [YK15] |
| **BFI-44 / TIPI / IPIP-NEO-120** | 44 / 10 / 120 | general |

The survey literature warns explicitly: "**very short measures of personality may substantially increase both the Type 1 and Type 2 error rates**" [PC25]. BFI-10 is convenient but its unreliability directly caps the correlation you can observe — an attenuation ceiling, not a model failure. If you collect ground truth, use BFI-44 or IPIP-NEO-60 minimum, and **report the instrument's own reliability so readers can disattenuate**.

Also expect **social desirability bias**: "people taking personality tests often try to present themselves in a certain way" [PC25].

### 5.2 Self-assessed vs attributed personality — the central gap

Two different constructs, routinely conflated:

- **Automatic Personality Recognition (APR)**: predict the target's *self-report*.
- **Automatic Personality Perception (APP)**: predict what *observers* attribute to the target.

PsychoFlickr's attribution protocol is the template [S17]: **12 independent assessors**, each viewing the **200 favourite pictures** of each of **300 users**, each filling the attribution-worded BFI-10; the 12 ratings averaged per user. Inter-rater agreement measured with **Krippendorff's α** — the reported values are the honest ones to quote: **Extraversion 0.32, Agreeableness 0.17, Neuroticism 0.22**, with Openness lowest of all. These are "comparable to those observed in the literature for **zero-acquaintance** scenarios." Segalin's Facebook study reports α = **0.34 (Extraversion)** and **0.26 (Neuroticism)** from 23 raters over 150 users [S17b].

Two consequences:
1. **Trait predictability tracks inter-rater agreement.** "The performance tends to be better for traits where α is higher." You cannot predict a consensus that does not exist.
2. **The self/attributed gap is not model error, it is construct difference.** "When the users self-assess their personality, they take into account information that is not available in the favourite pictures — personal history, inner state, education, etc." [S17]

The psychological theory that organises this is **Vazire's Self–Other Knowledge Asymmetry (SOKA) model** [V10]: traits vary along **visibility** (detectable by an outside observer) and **evaluativeness** (socially desirable/undesirable). The self is more accurate for **low-visibility** traits (thoughts, feelings — e.g. Neuroticism); others are more accurate for **highly evaluative** traits (e.g. Intellect), where self-report is distorted by ego. SOKA's four quadrants — open area / blind spot / hidden area / unknown area — are the right conceptual frame for telling a user *which* of your outputs they should and should not believe about themselves.

Also note the human comparison: computer systems reach ρ ≈ 0.30 on perception vs **human judges at ρ ≈ 0.38** [PC25] — machines have *not* surpassed humans at perception, even though Youyou et al. showed computers beat close acquaintances at *recognition* from Facebook Likes [YK15] and Segalin's classifier beat average human raters from a single profile picture [S17b].

### 5.3 Cross-validation practice

- **Leave-One-User-Out** (PsychoFlickr): train on all pictures except those belonging to one user; predict that user; iterate. Hyper-parameters tuned by nested CV inside the training set only. This preserves a rigorous train/test separation *at the user level* while using the whole corpus for evaluation [S17].
- **10-fold CV with folds at the user level**, Pearson r reported across folds (Guntuku, Liu) [G18][L16].
- **Averaged hold-out**: 75/25 split, **10 repetitions with reshuffled partitions**, accuracy and F1 averaged (Segalin Facebook) [S17b].
- **Class balancing before splitting**: for the mean/quartile split tasks, find the larger class (N) and the smaller (M), subsample N to M, then split — reducing 11,736 images to ~7,000 per trait [S17b].
- **Repeat with randomised splits and report SD**: Guntuku ran everything 100× and reported SD < 0.001 [G18].
- **Significance**: F-statistic (ANOVA) with p-values; t-test against chance; **Bonferroni correction** for the multiple-comparison problem in correlation tables [S17b].

**The two cardinal leakage sins in this domain**, both easy to commit:
1. **Splitting by image instead of by user** — two photos from the same user in train and test makes the task partly identity re-recognition.
2. **Feature quantisation / normalisation boundaries computed on the full corpus.** Segalin explicitly derives the Q interval boundaries "in the training set" [S17]. Any per-corpus z-scoring, PCA, or histogram binning must be fit inside the fold.

A third, less-obvious one: **correlation-based feature selection performed before the split.** Segalin's Facebook study selects features "that resulted statistically significant" per trait (e.g. **248 of 4,096 CNN features** retained for Extraversion) — this is legitimate only if the selection is redone inside each training fold.

### 5.4 What a plausible result looks like

Concrete numbers so that a suspiciously good result can be recognised:

| Study | Task | Result |
|---|---|---|
| Segalin, Facebook profile pics, n=11,736 [S17b] | binary, mean split | acc **0.55–0.56**, F1 0.55–0.57 |
| Same, quartile split (Q1 vs Q3) | binary | acc **0.60–0.62** — higher because near-mean cases are genuinely unrecognisable |
| Same, best feature family | CNN alone | O .59 C .60 E **.61** A .60 N .59 |
| Same, best combination | CA+CNN+IATO | O .61 C .60 E **.62** A .60 N .60 — **combining four families buys ~1 point over CNN alone** |
| Liu, Twitter profile pics, n=66,502 [L16] | ElasticNet, 10-fold | all traits r > .145; **conscientiousness best at r = .189** |
| Same, TwitterSurvey n=429 | ElasticNet | all traits significant except agreeableness; combined r ≈ .190 (O) |
| Datta, aesthetics [D06] | 5-fold SVM | best single feature 59.3%; 15 selected features **70.12%** |

Liu et al. put this in context: "psychological variables typically have a **correlational upper-bound around .3 – .4**" [L16]. **Anything reporting r > 0.5 against genuine self-report from images alone should be presumed to have leakage or to be predicting attribution rather than self-report.**

Liu et al. also report a sobering negative result on their small survey sample: "a total of only **3 significant correlations at p < .01 and none at p < .001** ... obtained from a total of **260 tests**, we cannot consider any of these correlations as being robust to randomness." Small-n image-personality studies are essentially noise generators.

### 5.5 The stereotype critique — state it, then design against it

The critique, in its strongest published forms:

1. **The correlations are with *attribution*, not *traits*.** Segalin's own numbers make the case: 48.5% of features correlate with attributed traits, 8.3% with self-reports [S17]. The model is a good model of *judges*.
2. **Machine "trait" judgments reproduce human stereotype structure.** Social-perception probing of VLMs on face stimuli finds the models reproduce human first-impression structure rather than validated trait signal [SP24]; and features from face-recognition networks predict human *appearance-bias* scores for deliberately manipulated faces but **not** for randomly generated faces — i.e. they track the stereotype, not the person [AB21].
3. **The predictor may be socioeconomic, not psychological.** "What AI actually captures is not necessarily personality but presentation... People who invest in more polished photos might invest more in their careers or have more resources, so algorithms may be detecting **wealth rather than conscientiousness**."
4. **MM-OCEAN quantifies it for VLMs**: 51.3% prejudice rate — over half of correct trait ratings have no grounded evidence [MO26].
5. **Cultural specificity.** Machajdik & Hanbury note up front that colour-emotion mapping "must consider theories about the use of colours, cognitive models and involve cultural and anthropological backgrounds ... people from different cultures or backgrounds might perceive and interpret the same colour pattern quite differently" [M10]. The whole colour-emotion layer is calibrated on Western art theory and Valdez & Mehrabian's Western subject pool.
6. **The survey's verdict**: "associations between image characteristics (colour, composition) and Big Five traits could reflect cultural or contextual stereotypes rather than personality-trait relationships" [PC25].

**Design responses that actually address it** (rather than adding a disclaimer):
- **Control for demographics.** Liu et al. compute **partial correlations controlling for age and gender**, and regress traits on the *residual* after adjusting for age and gender, because "demographic traits are known to affect both personality features and text-derived outcomes" [L16]. Do this. If a "trait" signal vanishes when age and gender are partialled out, it was a demographic stereotype.
- **Counterfactual invariance testing.** Swap the demographic-bearing content (FOCUS-style face-only counterfactuals from real photos: 480 images, 6 occupations × 10 race-gender groups) and require trait outputs to be invariant; report the measured delta as a first-class metric [FOCUS26].
- **Separate rating from grounding in evaluation** (MM-OCEAN's three tiers). Never report T1 accuracy alone.
- **Prefer describing over diagnosing.** "These photos are mostly outdoors, in groups, warm-toned, low detail" is verifiable. "This person is high in Extraversion" is a stereotype-laden leap the data does not license at r ≈ 0.2.

### 5.6 Ethics and scope

Segalin et al. state the dual-use plainly: "the experiments show that aesthetic preferences allow the inference of data that people do not necessarily intend to share (the self-assessed traits in this case)" [S17]. Staab et al. show anonymisation and alignment currently fail as mitigations [ST24]. Practical positions worth adopting: never surface race/ethnicity inference (FairFace's own 93.7%/75.4% gap makes it indefensible); treat age and location as high-risk; make the profile subject-facing and revocable; and log which photos drove each claim so the subject can contest it.

---

## 6. Prompting patterns that improve VLM judgment reliability

Each pattern below is tied to the specific failure mode it addresses.

### 6.1 Structured rubric with anchored ordinal levels

Replace free-form scoring with **k discrete, text-defined levels with written anchors** — the Q-Align construction [QA24]. Not "rate extraversion 1–100" but:

```
For the SINGLE image above, choose exactly one label for CUE: "social density".
  alone      — exactly one person, or no people
  pair       — two people
  small_group— 3 to 5 people
  crowd      — 6 or more people
  none       — no people are visible
```

Why: ordinal text levels exploit the model's language prior far better than numeric scales; and if you have logprob access you can softmax the k level tokens and take the **probability-weighted mean** for a continuous score plus a free entropy-based uncertainty. Rubric-based evaluation is also where reliability is measurable — item-response theory over rubric items identifies which items are too ambiguous or too judge-sensitive [RV26].

**Anchor every level with an observable, not an inference.** "Crowd" is observable. "Sociable" is not.

### 6.2 Forced evidence citation — observe before you judge

MM-OCEAN's three tiers are directly implementable as a prompt structure [MO26]. Force the order **observe → cite → rate**, and make the citation a *required field that is separately checkable*:

```
Return JSON with these fields, IN THIS ORDER:
1. "observations": 3-6 literal, verifiable statements about what is visible.
   Each must be something two people looking at this image would agree on.
   Forbidden: any adjective about the photographer's character, mood, or intent.
2. "cues": for each rubric dimension, the exact observation index/indices that
   support it, or null if no observation supports it.
3. "ratings": for each dimension, one of the anchored levels; if the "cues"
   field for that dimension is null, the rating MUST be "insufficient_evidence".
```

The hard constraint in step 3 is the point: it converts MM-OCEAN's 51% prejudice rate from an invisible property into a refused output. Ordering matters — asking for the rating first and the justification second produces post-hoc rationalisation (the confabulation mode, CR ≈ 52%).

Because the observations are literal, they can be **verified independently** — by a second model, by CLIP zero-shot probes (§2.6), or by the classic detectors (face count, Places365 indoor/outdoor, NIMA score). Disagreement between the VLM's stated observation and a deterministic detector is a high-precision hallucination alarm.

### 6.3 Per-item scoring, then external aggregation

Follow §4.7: one image per call, fixed schema, no cross-image reasoning inside the model. Aggregate with statistics you control (mean, SD, quantiles, counts, bootstrap CIs). Then a **final text-only pass** over the aggregate table writes the profile.

Benefits: sidesteps the multi-image collapse (79.0% → 66.5%) [MI26]; makes every profile claim traceable to rows; makes the pipeline cacheable and incrementally updatable when new photos arrive; and lets you cheaply run the per-image step m times for self-consistency.

Practical schema per image (this is the artefact worth designing carefully):

```json
{
  "image_id": "...",
  "provenance": {"original|repost|meme|ambiguous": "...", "exif_camera": true,
                 "overlay_text_fraction": 0.0, "dup_cluster_id": null},
  "scene": {"places365_top3": [...], "indoor_outdoor": "...", "sun_attributes": [...]},
  "people": {"face_count": 0, "modal_identity_present": false, "expression": "..."},
  "capture": {"framing": "...", "subject_distance": "...", "time_of_day": "..."},
  "aesthetic": {"nima_mean": 0.0, "nima_sd": 0.0, "colorfulness_hs": 0.0,
                "mean_saturation": 0.0, "mean_brightness": 0.0, "hue_circ_var": 0.0},
  "observations": ["..."],
  "cue_links": {"dimension": [0, 2]},
  "ratings": {"dimension": {"level": "...", "confidence": 0.0}},
  "abstained": ["dimension_x"]
}
```

### 6.4 Self-consistency

Sample m ≥ 5 judgments per image at T ≈ 0.7. Report the modal/mean level and the dispersion. "Coherence among sampled generations is correlated with correctness" — this is the mechanism behind self-consistency and the most reliable confidence signal available without logprobs [XI24]. Combine with §6.1: if you *have* logprobs, one call with the level-token distribution is cheaper than m samples; if you don't (many API surfaces), self-consistency is the substitute.

**Randomise the order of rubric items across the m samples.** Reordering options induces serial-position bias, and attribute ordering introduces anchoring effects that "systematically shift score distributions" [JJ25]; averaging over permutations cancels it. Track the **divergence rate** across permutations — **>20–25% divergence is the published signal that the rubric needs recalibrating** rather than the model being wrong [RV26].

### 6.5 Abstention and uncertainty

- Give every dimension an explicit `insufficient_evidence` level and make it *reachable* (see §6.2's hard constraint). Abstention "significantly improves overall system reliability" [AB25].
- Report **accuracy at coverage**, not raw accuracy. Tune the uncertainty threshold to a target coverage on a held-out set.
- Do **not** trust verbalised numeric confidence on its own — LLMs "still tend to be poorly calibrated when reporting their own confidence" [XI24]. Prefer distribution-derived (§2.5) or sampling-derived (§6.4) uncertainty, and apply post-hoc affine/isotonic recalibration per dimension.
- Propagate uncertainty to the profile level: a trait whose bootstrap CI over the user's photos spans more than ~1 Likert point should be rendered as a range or omitted (§4.4).

### 6.6 Anti-sycophancy and neutral framing

- **Third-person framing reduces sycophancy by up to 63.8%** [SY25]. Judge "the person who took these photographs", not "you"/"me"/"the user". Never include the subject's self-description, their guess about their own traits, or any prior profile in the judging prompt — only in the final write-up pass, and even there flag agreement/disagreement rather than resolving it.
- Do not re-ask after a disagreement. Between 40% and 75% of initially correct VLM answers flip under at least one form of social pressure [EB25]. If you need a second opinion, get it from an **independent** sample or a different model, not from a follow-up turn.
- Strip identity-leaking context from the judging prompt: filename, handle, bio, caption, prior conclusions.

### 6.7 Refusing unsupported inferences

Enumerate an explicit refusal list in the system prompt and enforce it schematically, not just by instruction:

- Never infer race/ethnicity (FairFace: 93.7% White vs 75.4% non-White accuracy [KJ21]).
- Never infer sexual orientation, religion, health/mental-health status, disability, or political affiliation from images.
- Age and precise location only if explicitly in scope, with a stated error band (age-group accuracy ≈ 60% [KJ21]; web-browsing LLMs find age the *hardest* attribute [WB25]).
- No inference about a person other than the account owner.
- **Structural enforcement**: omit those fields from the output schema entirely. A field that does not exist cannot be hallucinated into.

### 6.8 Counterfactual bias probing as a routine check

Adopt FOCUS-style face-only counterfactuals [FOCUS26] and GRAS-style multi-attribute sweeps (gender, race, age, **Monk Skin Tone**) [GRAS25] as a regression test on the rubric itself: hold the scene constant, vary the demographic-bearing region, and require the trait ratings to be invariant. Report Δ per dimension. Remember the finding that "higher faithfulness does not guarantee lower bias" — grounding and fairness must be audited jointly.

---

## 7. Recommended pipeline

```
INGEST
  └─ EXIF extraction, dedup (pHash pre-filter → CLIP-embedding cosine)
  └─ Provenance router: original / repost-meme / ambiguous  (§4.6)
  └─ Face-identity clustering → modal identity  (§4.6)

PER-IMAGE, DETERMINISTIC (cheap, run on everything)
  └─ Colour block: HSV stats + hue circular variance + PAD (Machajdik signs)
     + Hasler-Süsstrunk C + Datta-EMD colorfulness + 11 colour names   (§1.1-1.4)
  └─ Composition: Canny edge fraction, mean-shift segment count & mean size,
     rule-of-thirds S/V, low-DOF H/S/V, aspect ratio                    (§1.6)
  └─ Texture: 12 wavelet, 3 Tamura, 12 GLCM, grey entropy               (§1.7)
  └─ Places365 (ResNet50): indoor/outdoor + top-5 of 365 + top-9 of 102
     SUN attributes                                                     (§2.2)
  └─ Faces: count, largest-face ratio, pose, expression, missingness flag(§2.3)
  └─ NIMA(MobileNet or Inception-v2): mean + SD                         (§2.4)
  └─ CLIP: embedding + ~30 bipolar prompt-ensembled attribute axes      (§2.6)

PER-IMAGE, VLM (one image per call, structured schema)
  └─ observe → cite → rate, hard "insufficient_evidence" constraint     (§6.2)
  └─ anchored ordinal levels; logprob-weighted score if available       (§6.1, 2.5)
  └─ m=5 self-consistency samples with permuted item order              (§6.4)
  └─ cross-check stated observations against the deterministic detectors(§6.2)

AGGREGATE (outside any model)
  └─ per bucket (original / repost / ambiguous), and per time-third
  └─ mean, SD, median, p10/p90, counts; quantised BoF + LDA topics if
     enough data                                                        (§4.1-4.3)
  └─ bootstrap B=200 over the user's photos → 5th-95th percentile CIs   (§4.4)
  └─ temporal: cadence, circadian histogram, CLIP drift                 (§4.5)

CALIBRATE & GUARD
  └─ partial out age & gender; drop dimensions that vanish              (§5.5)
  └─ affine/isotonic recalibration per dimension on held-out labels     (§3.4)
  └─ counterfactual invariance probe; report Δ                          (§6.8)
  └─ suppress any dimension whose CI spans >1 Likert point              (§4.4)

WRITE (text-only LLM over the aggregate table)
  └─ every claim cites aggregate rows and photo IDs
  └─ describe-don't-diagnose; report ranges, not points
  └─ label outputs as *impression* (attributed), not *trait*            (§5.2)
```

**Expected performance envelope, stated honestly**: against genuine self-report, r ≈ 0.15–0.30 per trait; against consensus observer attribution, r ≈ 0.4–0.68; grounded (right rating *and* right evidence) ≈ 10–35% of items. Anything better than that from photos alone is a bug.

---

## 8. Sources

- **[D06]** Datta, Joshi, Li, Wang. *Studying Aesthetics in Photographic Images Using a Computational Approach.* ECCV 2006, LNCS 3953, 288–301. http://infolab.stanford.edu/~wangz/project/imsearch/Aesthetics/ECCV06/
- **[HS03]** Hasler, Süsstrunk. *Measuring Colourfulness in Natural Images.* IS&T/SPIE Electronic Imaging 2003. https://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf
- **[M10]** Machajdik, Hanbury. *Affective Image Classification using Features Inspired by Psychology and Art Theory.* ACM MM 2010, 83–92. https://www.imageemotion.org/machajdik_hanbury_affective_image_classification.pdf
- **[OT01]** Oliva, Torralba. *Modeling the Shape of the Scene: A Holistic Representation of the Spatial Envelope.* IJCV 42(3):145–175, 2001.
- **[S17]** Segalin, Perina, Cristani, Vinciarelli. *The Pictures we Like are our Image: Continuous Mapping of Favorite Pictures into Self-Assessed and Attributed Personality Traits.* IEEE Trans. Affective Computing 8(2):268–285, 2017. https://www.dcs.gla.ac.uk/~vincia/papers/submissionV1.pdf
- **[S17b]** Segalin, Celli, Polonio, Kosinski, Stillwell, Sebe, Cristani, Lepri. *What your Facebook Profile Picture Reveals about your Personality.* ACM MM 2017. https://arxiv.org/abs/1708.01292
- **[G18]** Riahi Samani, Guntuku, Ebrahimi Moghaddam, Preoţiuc-Pietro, Ungar. *Cross-platform and cross-interaction study of user personality based on images on Twitter and Flickr.* PLOS ONE 13(7):e0198660, 2018.
- **[L16]** Liu, Preoţiuc-Pietro, Riahi Samani, Ebrahimi Moghaddam, Ungar. *Analyzing Personality through Social Media Profile Picture Choice.* ICWSM 2016. https://www.sas.upenn.edu/~danielpr/files/persimages16icwsm.pdf
- **[RD17]** Reece, Danforth. *Instagram photos reveal predictive markers of depression.* EPJ Data Science 6:15, 2017.
- **[F16]** Ferwerda, Schedl, Tkalcic. *Using Instagram Picture Features to Predict Users' Personality.* MMM 2016 (113 participants, 22,398 pictures).
- **[SK16]** Skowron, Ferwerda, Tkalcic, Schedl. *Fusing Social Media Cues: Personality Prediction from Twitter and Instagram.* WWW 2016 Companion.
- **[Z18]** Zhou, Lapedriza, Khosla, Oliva, Torralba. *Places: A 10 Million Image Database for Scene Recognition.* IEEE TPAMI 2018. Code/models: https://github.com/CSAILVision/places365
- **[TM18]** Talebi, Milanfar. *NIMA: Neural Image Assessment.* IEEE TIP 27(8):3998–4011, 2018. https://arxiv.org/abs/1709.05424
- **[QA24]** Wu et al. *Q-Align: Teaching LMMs for Visual Scoring via Discrete Text-Defined Levels.* ICML 2024. https://arxiv.org/abs/2312.17090
- **[R21]** Radford et al. *Learning Transferable Visual Models From Natural Language Supervision (CLIP).* ICML 2021.
- **[KJ21]** Kärkkäinen, Joo. *FairFace: Face Attribute Dataset for Balanced Race, Gender, and Age.* WACV 2021. https://arxiv.org/abs/1908.04913
- **[PM24]** Peters, Matz. *Large language models can infer psychological dispositions of social media users.* PNAS Nexus 3(6):pgae231, 2024. https://arxiv.org/abs/2309.08631
- **[ST24]** Staab, Vero, Balunović, Vechev. *Beyond Memorization: Violating Privacy via Inference with Large Language Models.* ICLR 2024. https://arxiv.org/abs/2310.07298
- **[MO26]** *Perception or Prejudice: Can MLLMs Go Beyond First Impressions of Personality?* (MM-OCEAN benchmark), arXiv 2605.22109.
- **[MI26]** *More Images, More Problems? A Controlled Analysis of VLM Failure Modes.* arXiv 2601.07812.
- **[PC25]** *Twenty Years of Personality Computing: Threats, Challenges and Future Directions.* arXiv 2503.02082.
- **[IB25]** *Evaluating LLM Alignment on Personality Inference from Real-World Interview Data.* arXiv 2509.13244; and *Can LLMs Infer Personality from Real World Conversations?* arXiv 2507.14355.
- **[WB25]** *Web-Browsing LLMs Can Access Social Media Profiles and Infer User Demographics.* arXiv 2507.12372.
- **[XI24]** Xiong, Hu, Lu, Li, Fu, He, Hooi. *Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs.* ICLR 2024.
- **[SY25]** *SYCON-Bench: Measuring Sycophancy of Language Models in Multi-turn Free-form Conversations.* Findings of EMNLP 2025. https://github.com/JiseungHong/SYCON-Bench
- **[EB25]** *EchoBench: Benchmarking Sycophancy in Medical Large Vision-Language Models.* arXiv 2509.20146; *Benchmarking and Mitigating Sycophancy in Medical VLMs*, arXiv 2509.21979.
- **[JJ25]** *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge.* ACL/IJCNLP 2025.
- **[RV26]** *Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias.* arXiv 2606.19544.
- **[AB25]** VLM hallucination/abstention line: *Detect Before You Leap: Mirage Detection in Vision-Language Models*, arXiv 2606.00435; *Global Context or Local Detail? Adaptive Visual Grounding for Hallucination Mitigation*, arXiv 2604.24396.
- **[SP24]** *Social Perception of Faces in a Vision-Language Model.* arXiv 2408.14435.
- **[GRAS25]** *Ask Me Again Differently: GRAS for Measuring Bias in Vision Language Models on Gender, Race, Age, and Skin Tone.* arXiv 2508.18989.
- **[FOCUS26]** *Measuring Social Bias in Vision-Language Models with Face-Only Counterfactuals from Real Photos.* arXiv 2601.06931.
- **[AB21]** *A set of distinct facial traits learned by machines is not predictive of appearance bias in the wild.* AI and Ethics, 2021.
- **[V10]** Vazire. *Who Knows What About a Person? The Self–Other Knowledge Asymmetry (SOKA) Model.* JPSP 98(2):281–300, 2010.
- **[YK15]** Youyou, Kosinski, Stillwell. *Computer-based personality judgments are more accurate than those made by humans.* PNAS 112(4):1036–1040, 2015 (n = 86,220, 100-item questionnaire).
- **[K20]** Kachur et al. *Assessing the Big Five personality traits using real-life static facial images.* Scientific Reports 10:8487, 2020 (conscientiousness r ≈ .360 men / .335 women; mean effect size .243).
- **[ND25]** *Effective near-duplicate image detection using perceptual hashing and deep learning.* IP&M, 2025; *Comparative Evaluation of Perceptual Hashing and Deep Embedding Methods for Robust and Efficient Image Deduplication*, Electronics 15(7):1493.
- **[MT23]** *MemeTector: enforcing deep focus for meme detection.* Int. J. Multimedia Information Retrieval, 2023.
- **[SEL17]** *A Selfie is Worth a Thousand Words: Mining Personal Patterns behind User Selfie-posting Behaviours.* arXiv 1702.08097.
- **[SM23]** *How social media expression can reveal personality.* Frontiers in Psychiatry 14:1052844, 2023 (split-half r = .84–.88).
