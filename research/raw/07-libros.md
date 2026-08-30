# The Book-Length Literature on Reading People (and Accounts) from Photographs and Self-Presentation

## Conceptual scaffolding for image-based profiling — what to read, what to skim, what to distrust

Compiled 2026-08-30. Scope: **books and book-length reports only.** Papers and effect sizes are covered in `01-personality-images.md`, `03-marketing-profiling.md` and `04-methods-pipeline.md`. This file exists to supply the *frameworks* — the vocabulary for describing a pose, the epistemology for deciding what an image can and cannot license you to say, and the historical memory that stops you reinventing physiognomy with a GPU.

### Verdict labels used throughout

| Label | Meaning |
|---|---|
| **[R] Rigorous** | Scholarly monograph or textbook. Claims are sourced, hedged, and survive the replication era. Safe to build method on. |
| **[R-] Rigorous but dated / partial** | Sound within its frame, but the empirical base has moved or the frame is narrower than the blurb suggests. |
| **[P] Popular science, well-grounded** | Trade book by a working researcher describing their own real programme. Directionally trustworthy; the confidence exceeds the evidence at the margins. |
| **[P!] Popular science that overclaims** | Real research underneath, but the trade framing inflates effect sizes, generality, or the author's own centrality. Read the underlying papers, not the book. |
| **[C] Critique / polemic** | Argumentative rather than evidentiary. Valuable for reframing; do not cite as a finding. |
| **[M] Method reference** | A manual. Judge it by whether the procedures are operationalisable, not by whether the prose is interesting. |

---

# PART 0 — THE RANKED READING LIST

If you read nothing else, read these five, in this order. Each one **changes what you actually do**, not just what you believe.

## 1. Alexander Todorov — *Face Value: The Irresistible Influence of First Impressions* (Princeton University Press, 2017) **[R]**

**Why it is first.** This is the single book that most directly attacks the load-bearing assumption of the whole enterprise. Todorov spent two decades building the computational models of face-based trait impressions that are *the state of the art* — and his conclusion is that those impressions are highly reliable, highly consensual, cross-culturally patterned, extremely fast (34 ms of exposure suffices), and **largely invalid as descriptions of the person judged**. The impressions map the *perceiver's* stereotypes, not the target's traits.

**What it changes.** It forces you to split "what does this photo make people feel about this person/brand?" (a real, measurable, commercially useful question) from "what is this person actually like?" (mostly unanswerable from a face). Those two questions look identical in a brief and are completely different research objects. If your deliverable conflates them, you are selling physiognomy.

**Chapters that matter.** Part I on the history of physiognomy (Lavater, Galton's composite portraits, Lombroso) — this is the genealogy every "AI infers personality from faces" paper is unknowingly repeating. The chapters on the data-driven face model (valence/dominance two-dimensional structure of first impressions). The chapters on the accuracy question and on how incidental image properties — lighting, focal length, expression, angle, camera distance — swamp identity. Todorov's demonstration that *different photos of the same person* produce more variance in trait impressions than photos of *different people* is the most practically important finding in the book: it means a single-image inference is measuring the photographer, not the subject.

**Honest note.** Rigorous, and unusually honest about the limits of his own field. He is not a nihilist — he grants that some judgments (e.g., certain health and emotion cues) carry signal. The book is the correct calibration point.

---

## 2. Erving Goffman — *Gender Advertisements* (Harper & Row, 1979; orig. *Studies in the Anthropology of Visual Communication*, 1976) **[R-] / [M]**

**Why it is second.** It is the best worked example in existence of *reading poses in still images systematically*, and it predates every ML approach by fifty years. Goffman assembled ~500 advertisements and derived a coding scheme of recurring "gender displays" — the small ritualised body arrangements that images use to say something about relative status. His six families: **relative size**, **the feminine touch** (fingers caressing/tracing rather than grasping), **function ranking** (who is executing the instrumental action), **the family**, **the ritualization of subordination** (head cant, body cant, bashful knee bend, lying on the floor or bed, clowning), and **licensed withdrawal** (gaze averted, mouth covered, psychologically absent from the scene).

**What it changes.** It gives you a *finite, nameable, inter-rater-codable* vocabulary for what a body is doing in a frame. This is exactly what most Instagram-analysis work lacks: people say a feed feels "aspirational" or "approachable" with no coding scheme behind it. Goffman's categories can be applied to an Instagram grid in an afternoon and produce numbers two coders will agree on. Several dozen published replications since 1979 (Kang 1997; Bell & Milic 2002; Döring et al. on selfies) show the scheme travels — including to social media selfies, where the same displays recur at higher rates than in the ads Goffman studied.

**Chapters that matter.** The long essay "Gender Display" and then "Picture Frames" — the methodological preface where Goffman explains what an advertisement is evidence *of*. His answer is subtle and important: ads are not evidence about how people behave; they are **hyper-ritualisations** — standardised, exaggerated distillations of displays that already exist in social life. The same is true of an Instagram grid. It is a *performance of a type*, not a sample of behaviour.

**Honest note.** Rigorous in the qualitative-sociology sense, not the statistical one: Goffman never reports base rates, never sampled systematically, and picked pictures that made his point. His own methodological defence is that he is doing conceptual work, not estimation. Take the *scheme* and supply your own sampling and reliability statistics. Dated on gender politics in ways that are themselves interesting.

---

## 3. Lev Manovich — *Instagram and Contemporary Image* (self-published, 2017; free PDF at manovich.net; Spanish translation *Instagram y la imagen contemporánea*, DCCD-UAM Cuajimalpa, 2020) **[R] / [M]**

**Why it is third.** It is the only book-length work that does at scale exactly what this project does at small scale: computational analysis of Instagram imagery, from 16 million photos across 17 global cities, with the art-historical literacy to say what the patterns *mean*. Free, legally, in English and Spanish.

**What it changes.** Manovich's three-way typology — **casual** photos, **professional** photos, and **designed** photos ("Instagramism": the flat-lay, muted-palette, negative-space, consistently-graded aesthetic) — is the most useful single distinction for classifying a commercial account. It reframes the question from "what personality does this person have?" to "which visual convention is this account executing, and how competently?" That is a question images can actually answer. His treatment of the *feed as the unit of analysis* rather than the post — sequence, colour continuity, the grid as composition — is directly operational.

**Chapters that matter.** Part 2 ("Designed Photos / Instagramism") and Part 3 ("Platform, Aesthetics, Subjects") for the typology and the argument about aesthetic homogenisation. Part 1 for the methodological framing of what a large image corpus is evidence of. The visualisations themselves are the argument; look at them, don't just read.

**Honest note.** Rigorous in its measurement, essayistic in its interpretation, and Manovich is candid about which is which. Two real limitations: the data is 2012–2016, so it predates Stories, Reels, and the algorithmic feed's reshaping of aesthetics; and the sampling is city-based and hashtag-driven, so it is not a random sample of Instagram. Also read alongside his *Cultural Analytics* (MIT Press, 2020, 336pp) — a fuller statement of the method: representing culture as data, feature extraction, media visualisation, and a genuinely good extended discussion of sampling bias and the "cultural analytics" epistemology. *Cultural Analytics* is the methods book; *Instagram* is the worked example.

---

## 4. Kate Crawford — *Atlas of AI: Power, Politics, and the Planetary Costs of Artificial Intelligence* (Yale University Press, 2021) **[R]/[C]**, specifically **Chapter 5, "Affect"**

**Why it is fourth.** Chapter 5 is the definitive book-length demolition of automated inference of inner states from faces, and it is the exact intellectual ancestor of every commercial "AI reads personality/emotion from your photos" product. Crawford traces the lineage: Duchenne's electrical stimulation of facial muscles → Darwin's *Expression of the Emotions* → Silvan Tomkins → Paul Ekman's basic-emotions theory and FACS → military and DARPA funding → Affectiva and the modern affect-recognition industry. She then presents the contrary evidence, chiefly Lisa Feldman Barrett and colleagues' 2019 *Psychological Science in the Public Interest* review, which found that the mapping from facial configuration to emotional state is weak, context-dependent, and culturally variable — i.e., the industry's core premise is not supported.

**What it changes.** It gives you the *argument structure* for refusing a request. When someone asks you to infer emotional stability, trustworthiness, or "vibe as a person" from a grid, this chapter is the citation for why that is not a hard problem you haven't solved yet — it is a category error with a two-hundred-year track record.

**Chapters that matter.** Chapter 5 ("Affect") is essential. Chapter 4 ("Classification") is nearly as good on how training-set taxonomies smuggle in social judgment (the ImageNet "person" categories audit). Chapter 1 ("Earth") and Chapter 2 ("Labor") are excellent but off-topic for this project.

**Honest note.** Crawford is a critic, and the book is polemical by design — it is an "atlas" of harms and does not attempt a balanced accounting of AI's benefits. It is nonetheless well sourced and Chapter 5's empirical claims are the mainstream scientific position, not a fringe one. Do not cite *Atlas of AI* for technical claims about model architectures; do cite it for the affect-recognition critique.

---

## 5. Gillian Rose — *Visual Methodologies: An Introduction to Researching with Visual Materials*, 5th ed. (SAGE, 2022/2023, 480pp) **[M]/[R]**

**Why it is fifth.** Because it is the manual. Rose lays out the full menu of ways to analyse an image — compositional interpretation, content analysis, semiology, two flavours of discourse analysis, audience studies, participatory/photo-elicitation methods, and digital methods — and, critically, she organises them by her **"four sites × three modalities"** framework: meaning is made at the sites of *production*, of the *image itself*, of *circulation*, and of *audiencing*; each site has *technological*, *compositional*, and *social* modalities. This is a 12-cell grid you can run any brief through to find out which questions your data can actually answer.

**What it changes.** Most image-analysis briefs quietly ask a *production*-site question ("what is this person like?") using only *image*-site evidence. Rose's grid makes that mismatch visible immediately, and tells you what evidence you would need instead. The 5th edition's chapter **"Content Analysis and Cultural Analytics: Finding Patterns in What You See"** is the key one: it now explicitly bridges hand-coded content analysis and computational approaches, including Manovich's work, and gives the procedure — define the corpus, devise the categories, code the images, analyse the results — with reliability requirements attached.

**Chapters that matter.** Ch. 2 ("A Critical Visual Methodology") for the framework. Ch. 3 ("Understanding Visual Research Ethics") — genuinely useful, and specific about images of people found online. Ch. 6 ("Compositional Interpretation") for the vocabulary of the frame. Ch. 7 (content analysis / cultural analytics) as the core method. Ch. 12 ("Making Images as Research Data: Documentation, Elicitation and Participation") for photo elicitation. Ch. 13 ("Applying Digital Methods to Digital Images"), which is new and addresses Instagram and TikTok directly.

**Honest note.** Rigorous, current, and the standard text for a reason. It is a textbook: broad rather than deep, and it will not teach you to *do* computer vision. Its virtue is that it prevents category errors before you write any code.

### The five in one sentence each

- **Todorov**: face-based trait inference is reliable, consensual, and wrong.
- **Goffman**: here is a codable vocabulary for what bodies do in pictures.
- **Manovich**: here is what large-scale Instagram imagery actually looks like, measured.
- **Crawford (ch. 5)**: inferring inner states from faces is a two-century-old error, not a new capability.
- **Rose**: here is the grid that tells you which questions your images can answer.

---

# PART 1 — SELF-PRESENTATION THEORY

## 1.1 Erving Goffman — *The Presentation of Self in Everyday Life* (Univ. of Edinburgh Social Sciences Research Centre, 1956; Anchor/Doubleday, 1959) **[R]**

**Argument.** Social interaction is analysable as theatrical performance. People project a *definition of the situation*, others accept or challenge it, and the work of interaction is largely the collaborative maintenance of that definition. The key apparatus: **front region / back region** (frontstage/backstage), **personal front** (appearance and manner, as distinct from the *setting*), **dramaturgical discipline** and **dramaturgical loyalty**, **idealization** (performances over-communicate the values of the society), **impression management**, **teams** (performances are usually collective, not individual), and — the concept most often forgotten and most relevant here — **"expressions given" vs. "expressions given off."**

**Why it matters for this problem.** That last distinction *is* the analytic core of image-based profiling. "Given" = what the account intends to communicate (the caption, the curated grid, the brand claim). "Given off" = what leaks (the background of a product shot, the repeated location, the equipment visible, the number of staff in the frame, the resolution and consistency of the photography, whether the same tiles appear behind every flat-lay). A commercial Instagram profile is almost entirely "given"; the exploitable inferential signal is almost entirely in the "given off." Goffman also supplies the reason not to over-read: a performance is *designed* to be legible, so reading it correctly tells you about the intended audience and the performer's competence — not about their interior.

**Chapters that matter.** Ch. 1 "Performances" (idealization, dramaturgical discipline, misrepresentation); Ch. 3 "Regions and Region Behavior" (frontstage/backstage — the concept most abused in social media writing); Ch. 6 "The Arts of Impression Management"; and the Conclusion, where he is explicit that dramaturgy is a *framework*, not a claim that people are insincere.

**Honest note.** Rigorous as theory, entirely non-empirical in the modern sense — no sampling, no measurement, no falsifiable predictions. It is a lens, and its value is that it is the most productive lens anyone has built. Do not cite Goffman as evidence *that* something is true; cite him for *how to describe* what you observe. Note also that Goffman himself never wrote about mediated, asynchronous, permanent, audience-collapsed communication; every application to social media is an extension, and some extensions are strained.

## 1.2 Dramaturgy applied to social media

There is no single canonical book; the extension is spread across a handful of works.

- **Bernie Hogan, "The Presentation of Self in the Age of Social Media: Distinguishing Performances and Exhibitions Online"** (*Bulletin of Science, Technology & Society*, 2010) — not a book, but the most important single correction to naive Goffman-on-Facebook. Hogan argues that most social media content is not a *performance* (synchronous, situated, co-present) but an **exhibition**: artefacts submitted to a curated archive, later re-presented to unknown audiences by an algorithmic **"curator."** This distinction matters enormously for profiling. An Instagram grid is an exhibition. The audience is not present, the "performance" is asynchronous, and a third party (the ranking algorithm) selects what is shown. Inferring the performer's situational intent from an exhibition is a mistake Goffman would not have made.
- **Alice Marwick — *Status Update: Celebrity, Publicity, and Branding in the Social Media Age*** (Yale University Press, 2013) **[R]**. Ethnography of the San Francisco tech scene between the dot-com bust and the App Store. Introduces/consolidates **self-branding**, **micro-celebrity** (treating your audience as a fanbase and yourself as a product), and **life-streaming**. Her core argument is deflationary and useful: Web 2.0 did not flatten status, it produced new and highly unequal status hierarchies structured by race, class and gender. Chapters on self-branding and micro-celebrity are the relevant ones. Rigorous ethnography; the tech-scene specificity dates it, but the concepts hold.
- **Crystal Abidin — *Internet Celebrity: Understanding Fame Online*** (Emerald, 2018, SocietyNow series) **[R-]/[P]**. Short (~130pp), fast, and the best taxonomy available of *kinds* of online visibility: viral stars, meme personalities, "spotted and groomed investments," crowd-puller cameos, weaponized microcelebrity. Her concept of **"calibrated amateurism"** — the deliberate manufacture of amateur-looking, spontaneous-seeming content by professionals — is directly load-bearing for anyone trying to judge whether an account is a real small business or a produced brand. Concise to the point of thinness in places; the fieldwork behind it (her Singapore/SE Asia influencer ethnography) is solid.
- **Brooke Erin Duffy — *(Not) Getting Paid to Do What You Love: Gender, Social Media, and Aspirational Work*** (Yale University Press, 2017; new edition 2022) **[R]**. Interviews with women building fashion/beauty/lifestyle brands on Instagram and blogs. Coins **"aspirational labour"**: productive work performed now, unpaid, in hope of future social and economic capital. The relevant insight for profiling: the discourses of *authenticity*, *community* and *passion* that saturate commercial Instagram are **an occupational genre convention**, not evidence of the poster's disposition. When an account reads as "warm and authentic," that is very often a learned professional register.
- **Nancy K. Baym — *Personal Connections in the Digital Age*** (Polity, 2nd ed. 2015) **[R]**. The clearest survey of how mediation changes interpersonal cues — social presence, media richness, cues-filtered-out vs. hyperpersonal models. Chapter 3 ("Communication in digital spaces") is the best short treatment of what is *lost* when you only have images and text. Good conceptual hygiene for anyone about to over-read a photo.

---

# PART 2 — INSTAGRAM AND VISUAL SOCIAL MEDIA STUDIES

## 2.1 Tama Leaver, Tim Highfield & Crystal Abidin — *Instagram: Visual Social Media Cultures* (Polity, 2020, 264pp; Digital Media and Society series) **[R]**

**Argument.** The first scholarly monograph on Instagram as a platform. It treats Instagram simultaneously as infrastructure (owned by Facebook/Meta, with commercial imperatives that shape what is visible), as an aesthetic regime, as an ecology of adjacent apps, as an economy (influencers, brands, the "Instagram of everything"), and as a set of cultural practices with a lifespan from birth announcements to memorial accounts.

**Chapters.** Introduction; 1 **Platform**; 2 **Aesthetics**; 3 **Ecologies**; 4 **Economies**; 5 **Cultures**; 6 **Lifespans**; 7 "From the Instagram of Everything to the Everything of Instagram"; Appendix: Instagram Timeline.

**Which chapters matter here.** **Ch. 2 (Aesthetics)** — filters, the square, mobile photography conventions, the standardisation of the "Instagram look," and how platform affordances (originally filters, then editing tools, then Stories) produced visual conventions that people then read as personal style. This is the chapter that stops you attributing to a person what is attributable to a UI default. **Ch. 4 (Economies)** — the influencer/brand economy, sponsored content disclosure, engagement metrics and their manipulation; essential background for assessing a commercial account. **Ch. 5 (Cultures)** — subcultural visual practices, and how the same visual signal means different things in different communities. **Ch. 1 (Platform)** for the crucial reminder that what you can see is what Meta's API and ranking permit you to see, which is a sampling frame, not a population.

**Honest note.** Rigorous, well reviewed (LSE Review of Books, IJoC, Journal of Broadcasting & Electronic Media), and the right first book on Instagram. It is a survey — it synthesises rather than reports new data — and it is now five-plus years old, so it predates Reels' dominance, the recommendation-feed shift, and the current creator-economy structure. Nothing in it is wrong; some of it is no longer the whole picture.

## 2.2 Katrin Tiidenberg — *Selfies: Why We Love (and Hate) Them* (Emerald, 2018, SocietyNow) **[R-]/[P]**

**Argument.** A short, deliberately deflationary book. Tiidenberg argues that selfies are (a) not new — they sit in a long lineage of self-portraiture and vernacular photography; (b) not evidence of narcissism — the narcissism claim is repeatedly asserted and poorly evidenced, and the moral panic around selfies is heavily gendered; (c) meaning-making practices whose sense is *contextual and communal*, produced by circulation and reception rather than resident in the image.

**Chapters that matter.** "What Are Selfies?" (definition and history — useful for not treating a genre convention as a personality signal); the chapter on selfies and feeling; the chapter on norms and how they shift. The Conclusion is a good short statement of the anti-inferential position.

**Honest note.** Tiidenberg is a serious researcher (her ethnographic work on NSFW self-shooting communities is the substance behind this) but this is a short trade-adjacent book in a series designed for accessibility — light on data, heavy on synthesis. Her academic monograph *Body and Soul on the Internet* (Intellect, 2018) is the rigorous version. Read *Selfies* for the argument, cite the underlying work.

**Related, more scholarly:** Tiidenberg's co-authored *Selfies* entry work and the edited *Metaphors of Internet* (Peter Lang, 2020). Also **Jill Walker Rettberg, *Seeing Ourselves Through Technology*** (Palgrave, 2014) — **free open access** — on written, visual and quantitative self-representation, with a good short chapter on filters as "cultural filters."

## 2.3 Senft & Baym — the selfie special section

**Important correction: this is not a book.** Theresa M. Senft and Nancy K. Baym edited **"What Does the Selfie Say? Investigating a Global Phenomenon"**, a *feature section of the International Journal of Communication* 9 (2015), pp. 1588–1606 for the introduction, plus ~18 articles. It is open access at ijoc.org. The introduction is the single best short conceptual statement on selfies — it distinguishes the selfie as *object* from the selfie as *practice*, warns explicitly against reading selfies as symptoms of the poster's psychology, and introduces the "selfie as gesture" framing. Treat it as a book-length collection: it functions as one, it is free, and it is more rigorous than most selfie books.

The nearest genuine edited book in this space is **Adi Kuntsman (ed.), *Selfie Citizenship*** (Palgrave, 2017, open access) — political and activist uses of selfies. Narrower, but free.

## 2.4 Lev Manovich — *Cultural Analytics* (MIT Press, 2020, 336pp) **[R]/[M]**

Covered above as companion to *Instagram and Contemporary Image*. Structure: (I) studying culture; (II) representing culture as data; (III) exploring cultural data. Introduces **media visualisation** as a paradigm distinct from data visualisation — rather than reducing images to bar charts, you arrange the images themselves along measured dimensions so the corpus remains visible. For a project that has to *show* a client what a feed looks like as a whole, this is the most directly usable technique in any of these books. The chapters on sampling, on what "features" are, and on the difference between *cultural* analytics (open, exploratory) and *media* analytics (proprietary, commercial, optimisation-driven) are the most valuable. Rigorous, occasionally repetitive, and Manovich's habit of citing his own lab heavily is noticeable but not dishonest.

---

# PART 3 — FACE READING, FIRST IMPRESSIONS, AND ITS LIMITS

## 3.1 Alexander Todorov — *Face Value* (Princeton UP, 2017) **[R]**

See Part 0, #1. The anchor of this strand.

## 3.2 Daniel Kahneman — *Thinking, Fast and Slow* (Farrar, Straus and Giroux, 2011) **[P]**, with a large caveat

**Relevant content, not the whole book.** For this problem the useful parts are narrow and specific:

- **Ch. 7–8, "A Machine for Jumping to Conclusions" and "How Judgments Happen"** — **WYSIATI** ("What You See Is All There Is"). This is the mechanism behind bad profiling: coherence of the available evidence, not its quantity or quality, drives confidence. A tidy, aesthetically consistent grid produces a confident personality read *because it is coherent*, not because it is informative.
- **Ch. 9, "Answering an Easier Question"** — **attribute substitution**. Asked "is this business trustworthy?", the mind answers "does this feed look competent?" This is the single best description of what image-based profiling actually does.
- **Ch. 19–20, "The Illusion of Understanding" and "The Illusion of Validity"** — the direct warning. Subjective confidence in a judgment is a feeling about the coherence of the story, not a valid estimate of accuracy.
- **Ch. 21, "Intuitions vs. Formulas"** — the Meehl clinical-vs-statistical prediction literature, and the case for simple linear models over expert intuition. Relevant when deciding whether to hand-read a feed or code it.
- **Ch. 24, "The Engine of Capitalism"** — the planning fallacy and optimistic bias, relevant to how clients receive a profile.

**Honest note — this matters.** Chapter 4 ("The Associative Machine") and the social-priming material through the early chapters are **not reliable**. Schimmack, Heene and Kesavan's 2017 "Reconstruction of a Train Wreck" analysis found 11 of 12 cited priming studies had an R-Index below 50. Kahneman publicly conceded in the comments and later in print: "the experimental evidence for the ideas I presented in that chapter was significantly weaker than I believed when I wrote it... I placed too much faith in underpowered studies." The **core dual-process framing, anchoring, availability, loss aversion, and the illusion-of-validity material survive**; the priming periphery does not. Cite the chapters listed above; do not cite the priming chapter.

## 3.3 The physiognomy-revival critique

- **Sharrona Pearl — *About Faces: Physiognomy in Nineteenth-Century Britain*** (Harvard University Press, 2010, ~288pp) **[R]**. The best history. Pearl's argument is that physiognomy was not a fringe pseudoscience but a *mainstream visual literacy* — a way Victorians read strangers in a newly anonymous urban world, embedded in portraiture, caricature, theatre and, crucially, photography. Chapters: "Pocket physiognomy: sense in the city"; "Performing physiognomy"; "Portrait physiognomy"; "Caricature physiognomy"; **"Photographic physiognomy: through a mediated mirror"** — this one is the direct ancestor of the current problem, on how photography was believed to make character mechanically legible; and "Diagnostic physiognomy: from phrenology to fingerprints." Rigorous historical scholarship. The value: it shows that the *social conditions* that produce physiognomy — mass anonymity, a new imaging technology, a felt need to sort strangers fast — are exactly today's conditions. That is a better explanation for the physiognomic-AI revival than "the models got good."
- **Kate Crawford, *Atlas of AI*, ch. 5** — see Part 0, #4.
- **Wendy Hui Kyong Chun — *Discriminating Data: Correlation, Neighborhoods, and the New Politics of Recognition*** (MIT Press, 2021; paperback 2023, with mathematical illustrations by Alex Barnett) **[R]/[C]**. The deepest of the critiques and the least read. Chun's argument: **correlation itself** — the statistical machinery underwriting all prediction from data — was developed by Galton and Pearson *for eugenic purposes*, and carries that shape. Her central concept is **homophily** ("like attracts like"), which she shows is not a natural law of social life but a modelling assumption imported from 1950s segregated-housing research, and which recommender systems then *enforce* rather than discover. Polarization, she argues, is a design outcome, not a bug. Relevant chapters: the section on correlation and eugenics; the long treatment of homophily; the discussion of "recognition" and how classification systems produce the categories they claim to detect. Honest note: rigorous and original, but dense and theory-heavy — Galloway's *boundary 2* review is fair that the prose fights the reader. Worth the effort for the correlation/eugenics genealogy, which is not available elsewhere in book form.
- **Kashmir Hill — *Your Face Belongs to Us: A Secretive Start-Up's Quest to End Privacy as We Know It*** (Random House, 2023) **[P]**, high quality. Investigative journalism on Clearview AI — the company that scraped billions of public social media photos, including Instagram, to build a face search engine. Relevant not for its science but for the **operational reality**: it documents precisely what can be done with publicly posted photographs at scale, who does it, and what the legal exposure looks like (BIPA litigation, the Illinois settlement, EU/UK/Canada/Australia regulatory findings). If your work involves scraping public profile images, this is the book about what the downstream of that practice looks like. Well reported, appropriately hedged, not overclaiming.
- **Vinciane Despret / Lisa Feldman Barrett** — Barrett's ***How Emotions Are Made: The Secret Life of the Brain*** (Houghton Mifflin Harcourt, 2017) **[P!]** is the accessible statement of the theory of constructed emotion that underpins Crawford's ch. 5. Directionally correct and important — the classical "basic emotions" view really is in serious trouble — but Barrett is polemical about it and the trade framing ("everything you know about emotion is wrong") oversells the settledness of her own alternative. Read her 2019 *PSPI* review article instead if you need to cite.

## 3.4 Supporting reference

**Vicki Bruce & Andy Young — *Face Perception*** (Psychology Press, 2012) **[R]/[M]**. The textbook. If you need the actual cognitive science of how faces are processed — configural vs. featural processing, the Bruce & Young functional model, identity vs. expression pathways, the other-race effect — this is it. Dry, thorough, not about social media. Ch. 8–9 on social judgments from faces are the relevant ones.

---

# PART 4 — DIGITAL FOOTPRINTS AND PSYCHOMETRIC TARGETING

## 4.1 Michal Kosinski — no trade book exists

**Finding: Kosinski has not written a popular book.** His work in this area is entirely in journal articles (Kosinski, Stillwell & Graepel 2013 PNAS on Facebook Likes; Youyou, Kosinski & Stillwell 2015 PNAS on computer vs. human judgment; Wang & Kosinski 2018 JPSP on sexual orientation from faces; Kosinski 2021 *Scientific Reports* on political orientation from faces). What he *has* co-written is:

**John Rust, Michal Kosinski & David Stillwell — *Modern Psychometrics: The Science of Psychological Assessment*, 4th ed. (Routledge, 2021)** **[R]/[M]**. This is the substantive book-length statement of the Cambridge Psychometrics Centre position. The 4th edition adds new chapters on item response theory, computer adaptive testing, and — the relevant one — **the psychometric analysis of digital traces/footprints**. This is the right reference for understanding *what kind of measurement claim* the digital-footprint literature is making: it treats Likes, posts and images as items in a test, and applies classical and modern test theory to them. Reading this alongside the PNAS papers is far more informative than any trade book on the topic, because it makes explicit the reliability and validity framework the claims live inside — and therefore where they break. Rigorous, textbook-dry, and it is the honest version of what *Mindmasters* dramatises.

## 4.2 Sandra Matz — *Mindmasters: The Data-Driven Science of Predicting and Changing Human Behavior* (Harvard Business Review Press, 2025, 240pp; ISBN 9781647826314) **[P]**, tending to **[P!]** in places

**What it claims.** Matz (Columbia Business School; co-author with Kosinski and Stillwell of the 2017 PNAS psychological-targeting field experiments) argues that digital footprints — Likes, language, spending records, GPS traces, phone-sensor data — permit inference of psychological traits at accuracy comparable to or exceeding human acquaintances, and that *targeting communication to inferred traits measurably changes behaviour*. She then argues for a dual framing: the same capability that enables manipulation (Cambridge Analytica as "the tip of the iceberg") enables benefit — mental-health detection from linguistic and behavioural markers, better financial decisions, echo-chamber escape. The final third is prescriptive: data cooperatives, federated learning, differential privacy, individual agency over one's footprint.

**How well supported.** The core empirical claim rests on Matz, Kosinski, Nave & Stillwell (2017, *PNAS*), which ran three field experiments on Facebook with ~3.5 million people and found that persuasive appeals matched to inferred extraversion or openness produced up to **40% more clicks and 50% more purchases** than mismatched appeals. That study is real, large, and preregistration-adjacent — but read the numbers carefully: those are *relative* lifts on very small base rates in a single advertising context, matched vs. deliberately *mis*matched (not vs. a well-designed generic ad), on two of five traits, in beauty and app-install verticals. Eckles, Gordon & Johnson and others have raised methodological objections about the counterfactual. Subsequent replication and extension work has found smaller and more context-dependent effects. Matz's own later work is more measured than the book's framing.

**Honest note.** This is the best-informed trade book on the topic, written by someone who actually did the research, and the ethical framing is sincere rather than performative. But it is a Harvard Business Review Press trade book, and it carries the genre's characteristic inflation: the "mind-reading" framing, the confident extrapolation from advertising click-through to political and financial behaviour, and a chronic under-emphasis on the difference between *prediction accuracy at population level* (real, ~r = 0.3–0.4 for the best traits) and *actionable inference about an individual* (much weaker). **Read it for the landscape and the ethical argument; do not cite its effect claims — cite the 2017 PNAS paper and its critics directly.** Reviews at publication were near-uniformly positive and none engaged seriously with effect sizes, which is itself informative about the review ecosystem.

## 4.3 Christopher Wylie — *Mindf\*ck: Cambridge Analytica and the Plot to Break America* (Random House, 2019) **[P!]** — overclaiming

**What it claims.** Wylie, the pink-haired research director turned whistleblower, narrates the construction of Cambridge Analytica's psychographic apparatus — the Kogan/GSR "thisisyourdigitallife" app, the harvesting of ~87 million Facebook profiles, OCEAN scoring, and the deployment of trait-matched messaging in the 2016 US election and (contested) Brexit. His framing is that this constituted an information-warfare operation, developed from SCL Group's military psy-ops work, that materially altered electoral outcomes.

**Honest note.** The **factual core is real and important**: the data harvest happened, the Facebook platform policies permitted it, the company did build and sell psychographic products, and the resulting scandal produced the FTC's $5 billion Facebook settlement and the UK ICO investigation. The **causal claim is not supported.** Wylie is simultaneously whistleblower, self-promoter, and a principal architect of the thing he is denouncing, and the book's rhetorical structure requires the operation to have worked, because otherwise he is not a figure of historical consequence. He offers no evidence of vote change, because none exists.

## 4.4 Brittany Kaiser — *Targeted: The Cambridge Analytica Whistleblower's Inside Story* (Harper, 2019) **[P!]** — overclaiming, and less reliable than Wylie

Kaiser was CA's business development director. Her book is the sales-side account, and it is markedly more self-exculpatory than Wylie's; she was selling the psychographic product to clients while it was operating, and the book reads in places as a continuation of that pitch with the polarity flipped. Both Wylie and Kaiser are prominently featured in Netflix's *The Great Hack* (2019), of which *The Economist*'s review noted: "So credulous is *The Great Hack* that if Cambridge Analytica had not shut down, its bosses would be using the movie as a testimonial." That is the correct posture toward both books.

**What independent analysis actually concluded.** Three convergent findings:
1. **The UK Information Commissioner's Office** investigated for three years (Operation Elizabeth Denham; final report to DCMS Committee, October 2020) and concluded that CA's analytics were **not as sophisticated as claimed**, that it found no evidence CA was involved in the Brexit referendum beyond initial exploratory work, and that the models were in part "well-recognised processes using commonly available technology."
2. **Academic assessment** (e.g. Bakir, "Psychological Operations in Digital Political Campaigns: Assessing Cambridge Analytica's Psychographic Profiling and Targeting," *Frontiers in Communication* 5:67, 2020) documents the *attempted* deployment in detail but states explicitly that "a limitation of this study is its inability to demonstrate that deployment of such psy-ops campaigning tactics actually influenced targeted voters," and cites the broader literature finding that "impacts are minimal." Bakir's normative argument — that deceptive and opaque targeting violates democratic norms *regardless* of measured effect — is the defensible position, and is worth adopting.
3. **The microtargeting-effects literature generally** finds persuasion effects from political advertising that are small to zero (Kalla & Broockman's 2018 *APSR* meta-analysis of 49 field experiments found an average effect of persuasive campaign contact on candidate choice in general elections of approximately zero), and no credible study has isolated a CA-specific effect. Compare: Nickerson & Rogers on the gap between what campaigns believe about their data and what it delivers.

**The correct summary sentence:** Cambridge Analytica's data collection was real and unethical; its psychographic targeting product was oversold to its own clients, to journalists, and by its own whistleblowers; there is no evidence it changed an election outcome; and the ethical objection stands anyway.

## 4.5 Eitan Hersh — *Hacking the Electorate: How Campaigns Perceive Voters* (Cambridge University Press, 2015, 270pp) **[R]** — the skeptical counterweight

**Argument.** The most comprehensive empirical study of what campaigns actually know. Hersh's central finding, developed from state-by-state comparison of voter file contents: **campaigns' knowledge of voters comes overwhelmingly from public administrative records** — registration, party affiliation where states record it, turnout history, and in some states race — **not from commercial psychographic data**, which he shows is noisy, frequently wrong at the individual level, and adds little predictive value over the public records. His concept of the **"perceived voter"** is the key contribution: campaigns do not interact with voters, they interact with *data avatars* constructed from whatever records exist, and because record availability varies enormously by state, the same voter is perceived differently, and mobilised differently, in Florida than in Ohio.

**Why it matters here.** This is the empirical rebuttal to the entire Cambridge Analytica mythology, published *before* it. It is also directly transferable: substitute "Instagram grid" for "voter file" and the argument holds. **You are not profiling a person; you are constructing a perceived person from whatever traces the platform happens to expose, and the shape of that construct is determined by the platform's data regime, not by the person.** That reframing is the most useful single idea in this strand.

**Chapters that matter.** Ch. 2 on the data landscape and what voter files contain; Ch. 3–4 on the perceived-voter model and how record availability varies; Ch. 7 on the actual (limited) role of commercial data appends.

**Honest note.** Rigorous political science, well reviewed (Karpf in *Political Science Quarterly*). It is US-specific and pre-2016, so it does not address platform-side targeting (Facebook's own ad tools, lookalike audiences), which is a real and growing channel it could not have covered. Hersh's later *Politics Is for Power* (Scribner, 2020) is a different, more polemical book — good, but not for this problem.

## 4.6 Shoshana Zuboff — *The Age of Surveillance Capitalism* (PublicAffairs, 2019) **[C]**, read selectively

**Argument.** A new economic logic in which human experience is claimed as free raw material, rendered into **behavioural data**, of which a **"behavioural surplus"** beyond service improvement is fabricated into **prediction products** sold in **behavioural futures markets**; and in which the competitive dynamic drives from prediction toward *modification* of behaviour ("economies of action").

**Relevant part.** The concept of behavioural surplus is genuinely useful for this project — the observation that the exhaust of an activity (posting a product photo) becomes an input to prediction about the poster is precisely the mechanism at issue.

**Honest note — read critically.** Zuboff's book is long (700+pp), rhetorically heated, and has attracted serious scholarly objection: Morozov's ~16,000-word *Baffler* essay ("Capitalism's New Clothes") argues the framework is tautological and brackets capitalism itself; Blayne Haggart and others have documented weak engagement with the prior surveillance-studies literature (Gandy's *The Panoptic Sort*, 1993, made much of the argument first and is barely cited); Jansen & Pooley's "review of reviews" (2021) is a fair map of the reception. Take the vocabulary, not the historiography. If you want one rigorous alternative in the same space: **Nick Couldry & Ulises Mejias, *The Costs of Connection* (Stanford UP, 2019)**, which makes a sharper and better-sourced version of the argument with an explicit Global South and Latin American frame.

---

# PART 5 — ALGORITHMIC BIAS AND THE CRITIQUE OF INFERENCE

## 5.1 Solon Barocas, Moritz Hardt & Arvind Narayanan — *Fairness and Machine Learning: Limitations and Opportunities* (MIT Press, 2023; free at fairmlbook.org, CC BY-NC-ND) **[R]/[M]** — the most technically useful book in this section

**Argument.** The textbook. It treats fairness not as a slogan but as a set of formally specifiable, and provably incompatible, criteria. The core technical result every practitioner should know: **the impossibility theorem** — independence, separation and sufficiency (roughly: demographic parity, equalised odds, and calibration) cannot in general all hold simultaneously except in degenerate cases. Which means "make it fair" is not an instruction; you must choose which fairness you mean and defend the choice.

**Chapters that matter for this problem.** **Ch. 2 "Classification"** on the formal criteria and the impossibility result. **Ch. 1 / "When is automated decision making legitimate?"** on the prior question of whether a prediction should be made at all. **Ch. 3 "Relative notions of fairness"** and **Ch. 4 "Causality"** — the causal chapter is the one that clarifies why "the model is only using the photo, not race" is not a defence. **Ch. 6 "Legal and philosophical perspectives on discrimination"** — disparate treatment vs. disparate impact, and why proxies matter. **Ch. 8 "Datasets"** — measurement, construct validity, and the point that most fairness failures are *measurement* failures: the thing you claim to predict is not the thing your label encodes.

**Why it belongs in an image-profiling project.** The construct-validity discussion is the deepest available treatment of the exact failure mode here: "personality inferred from a grid" is a construct whose operationalisation (a model's output) may have almost no relation to the construct's name. Free, current, and technically precise.

## 5.2 Cathy O'Neil — *Weapons of Math Destruction* (Crown, 2016) **[P]**

**Argument.** Certain algorithmic systems are "WMDs" when they combine three properties: **opacity**, **scale**, and **damage** — plus, critically, **absent or corrupted feedback loops** that would otherwise correct them. Worked cases: teacher value-added models, recidivism scoring, predatory for-profit college advertising, credit and insurance scoring, personality tests in hiring (the Kronos/CVS case is directly relevant), scheduling software.

**Chapters that matter.** Ch. 6 ("Ineligible to Serve") on personality testing in hiring — the closest analogue to image-based personality profiling, and O'Neil's treatment of why the ADA problem arises is sharp. Ch. 4 ("Propaganda Machine") and Ch. 10 ("The Targeted Citizen") on advertising and micro-targeting.

**Honest note.** Well-grounded pop science by a former quant, and the three-criteria heuristic is genuinely portable. It is journalistic rather than analytical: cases are chosen to illustrate, effect sizes are rarely given, and the technical content is thin. It has been fairly criticised for occasionally treating "algorithm" as a synonym for "bad policy implemented at scale" — often true, but it blurs where the algorithm is the problem versus where it is the messenger. Read it for the framework, not the evidence.

## 5.3 Safiya Umoja Noble — *Algorithms of Oppression: How Search Engines Reinforce Racism* (NYU Press, 2018) **[R]**

**Argument.** Search results are not neutral reflections of the world but commercial products shaped by advertising economics, and they systematically reproduce racist and sexist representations — the founding example being the pornographic results returned for "black girls" in 2011. Noble's larger point is that **the presentation of algorithmic output as neutral is itself the mechanism of harm**: authority is transferred to the ranking without anyone taking responsibility for it.

**Chapters that matter.** Ch. 1–2 on searching for Black girls and the commercial logic behind results; Ch. 3 on searching for people and identities; Ch. 5 on the future of information culture and "technological redlining." Relevant here because image search and image classification carry the same representational politics: what a model returns for "professional," "trustworthy," or "attractive" is a compressed record of who has historically been depicted that way.

**Honest note.** Rigorous humanities/information-studies scholarship. Its central examples are from 2009–2016 and Google has since patched many of the specific queries, which some readers mistake for a refutation — it is not; the mechanism Noble identifies is structural, and the patching-in-response-to-press is itself part of her argument. Not a quantitative audit; do not expect measured rates.

## 5.4 Ruha Benjamin — *Race After Technology: Abolitionist Tools for the New Jim Code* (Polity, 2019) **[R]/[C]**

**Argument.** The **"New Jim Code"**: the employment of new technologies that reflect and reproduce existing inequities but are promoted and perceived as more objective or progressive than the discriminatory systems of a previous era. Benjamin's four-part taxonomy is the practically useful contribution: **engineered inequity** (explicitly discriminatory design), **default discrimination** (harm through inattention to existing social hierarchies), **coded exposure** (visibility as a double bind — being unseen by the system *and* being over-surveilled by it), and **technological benevolence** (fixes that deepen the problem while claiming to solve it).

**Chapter that matters most here.** **Ch. 3, "Coded Exposure: Are You Ready for Your Close-Up?"** — this is about *photography specifically*: Shirley cards and the calibration of colour film for white skin, the history of photographic chemistry as a racial technology, and its continuity into face detection and image classification. If you are building anything that processes photographs of people, this chapter is required and it is short.

**Honest note.** Rigorous within critical STS; it is an argumentative book with a stated political programme (abolitionist), which it does not hide. The empirical claims are well sourced; the conclusions are normative. Cite it for the framework and for the photographic history, which is factual.

## 5.5 Meredith Broussard — *Artificial Unintelligence* (MIT Press, 2018) and *More Than a Glitch* (MIT Press, 2023) **[P]**, both well grounded

**Argument.** *Artificial Unintelligence* names **"technochauvinism"**: the belief that technological solutions are inherently superior. Broussard is a data journalist *and* a former software developer, and the book's distinctive move is to actually build the failing systems herself and show them failing. *More Than a Glitch* extends this: bias in tech is not a bug to be patched but a property of the system, and the correct response is often to **not build the thing** rather than to make it more inclusive — she is explicit that "make facial recognition work equally well on everyone" can be the wrong goal.

**Relevant sections.** *More Than a Glitch* on facial recognition and on medical diagnostic algorithms; both books on the limits of what a classifier's output means. Broussard's chapter on her own breast-cancer AI experience in *More Than a Glitch* is a model of how to report on a system's accuracy honestly.

**Honest note.** Accessible, technically literate, and it does not overclaim — Broussard is careful to distinguish what she demonstrated from what she suspects. Thinner on theory than Benjamin or Chun. Good first book for a non-technical stakeholder.

## 5.6 Also worth having

- **Virginia Eubanks — *Automating Inequality*** (St. Martin's, 2018) **[R]/[P]**. Ethnography of automated decision systems in welfare, homelessness services and child protection. The Allegheny County chapter is the best account anywhere of what "predictive risk modelling about individuals" does to the people modelled. Directly relevant as a cautionary structure.
- **Catherine D'Ignazio & Lauren Klein — *Data Feminism*** (MIT Press, 2020; **free open access**) **[R]/[M]**. Seven principles; the most operational are "**examine power**," "**elevate emotion and embodiment**," "**consider context**" (the chapter arguing that data is never "raw" and that decontextualised data is the source of most misinterpretation), and "**make labor visible**." Ch. 5 ("Unicorns, Janitors, Ninjas, Wizards, and Rock Stars") and Ch. 6 ("The Numbers Don't Speak for Themselves") are the useful ones here. Practical, short, free.
- **Oscar Gandy — *The Panoptic Sort: A Political Economy of Personal Information*** (Westview, 1993; 2nd ed. Oxford UP, 2021) **[R]**. The book that made most of the surveillance-capitalism argument twenty-five years earlier, with more economics and less rhetoric. Cite this instead of Zuboff where you can.

---

# PART 6 — PERSONALITY PSYCHOLOGY, PROPERLY

## 6.1 David C. Funder — *The Personality Puzzle*, 9th ed. (W. W. Norton, 2022) **[R]/[M]**

**What it is.** The standard undergraduate personality textbook, organised by *paradigm* rather than chronology: trait, biological, psychoanalytic, humanistic/cross-cultural, cognitive/learning. Funder is unusual among textbook authors in being a leading researcher on the specific question of **accuracy of personality judgment**, and the book reflects it.

**Chapters that matter.** The trait chapters (roughly 4–7) for the Big Five, its derivation from lexical and factor-analytic work, its cross-cultural status, and — importantly — its limits. The chapter on **personality assessment** (S data, I data, L data, B data — Funder's four-source taxonomy) is the most useful single framework in this strand: it forces you to say *what kind of data* a claim rests on. An Instagram grid is **B data** (behavioural residue) at best, being used to make **S data**-shaped claims (self-report trait scores). That mismatch is the whole methodological problem, stated in four letters. The chapters on the person–situation debate and on judgment accuracy are the direct treatment.

**Honest note.** Rigorous, current, readable, appropriately hedged about replication problems (Funder has been a vocal reformer — his "Evaluating effect size in psychological research" with Ozer, 2019, is the standard citation for interpreting small correlations). It is a textbook: expensive, and broader than you need. Get an older edition cheaply; the trait and assessment material is stable.

## 6.2 David C. Funder — *Personality Judgment: A Realistic Approach to Person Perception* (Academic Press, 1999) **[R]**

**The book-length statement of the Realistic Accuracy Model (RAM).** This is the most important entry in this whole file for anyone who wants to know *under what conditions* judging a person from limited information can work.

**The model.** Accurate judgment requires four sequential stages, each a bottleneck: the target must **emit relevant** behaviour; the cue must be **available** to the judge; the judge must **detect** it; the judge must **utilise** it correctly. Failure at any stage caps accuracy, and because the stages are multiplicative, improvements at one stage have limited effect if another is the binding constraint.

**The four moderators.** RAM predicts accuracy is moderated by: **good judge** (some people are better at it), **good target** ("judgeable" people — those whose behaviour is consistent and whose self-presentation is congruent with their traits), **good trait** (highly visible traits like extraversion are judged far more accurately than internal ones like neuroticism), and **good information** (quantity *and* quality — more of the right kind, in the right context).

**Why this is the key framework for image-based profiling.** Apply RAM to an Instagram grid and it tells you, a priori, what you can expect:
- **Good trait**: extraversion and (partly) openness are visible in expressive behaviour and aesthetic choices; conscientiousness has weak but real cues in orderliness; **neuroticism and agreeableness are near-invisible** and any claim to read them from photos should be treated as noise. This prediction is confirmed repeatedly in the empirical image-personality literature.
- **Good information**: a curated commercial grid is *low-quality* information for trait inference precisely because it is curated — the emission stage is filtered by strategic self-presentation. Volume does not fix this; 500 posts of the same designed aesthetic contain roughly as much trait information as five.
- **Good target**: a business account presenting a brand persona is close to the definition of an *un*judgeable target.
- **Good judge**: the least-studied moderator, and the one where "the model" replaces the human.

**Honest note.** Rigorous, and the model has held up for twenty-five years — see Letzring & Funder's Oxford Handbook chapter for the current state. It is a 1999 academic monograph: dry, occasionally hard to find, pre-dates all social media. That does not matter; the framework is about information, not medium.

## 6.3 The "personality coefficient" ceiling — Walter Mischel, *Personality and Assessment* (Wiley, 1968; reissued Psychology Press/Routledge, 1996) **[R-]**

**Argument, and where the number comes from.** Mischel reviewed the personality-assessment literature and reported that correlations between personality measures and behavioural criteria assessed in a different medium clustered persistently around **r = .20 to .30**, a value he sardonically named the **"personality coefficient."** His conclusion — that trait measures are "undoubtedly significant for large samples of subjects but useless for the prediction of individual behavior" — triggered the person–situation debate and nearly ended trait psychology as a field.

**Why it belongs in this file.** Every claim about inferring personality from images should be read against this ceiling. If *self-report questionnaires designed for the purpose* correlate with behaviour at ~.30, an inference from photographs — several stages further from the construct — cannot plausibly exceed that, and empirically it does not (image-based personality prediction typically lands at r ≈ .10–.30 depending on trait, with extraversion and openness at the top). **A published r = .25 in this literature is not a weak result; it is roughly the theoretical maximum.** That reframing is important both for reading papers honestly and for not being impressed by vendors quoting accuracy figures without a baseline.

**Honest note.** Dated, and importantly *qualified* since. The .30 ceiling applies to **single-act criteria**; Epstein's aggregation work in the late 1970s showed that aggregating behaviour across occasions raises trait–behaviour correlations substantially (into the .5–.7 range), which is a genuine and often-forgotten rescue of the trait position. Fleeson's density-distributions work resolved much of the debate by showing that people have stable *distributions* of states. And Funder & Ozer (2019) argue convincingly that r = .20 is a *consequential* effect at scale even if useless for individual prediction — a distinction that maps exactly onto the difference between targeting an ad campaign and profiling a specific account. Read Mischel for the number and the argument; read Funder & Ozer for what the number means.

## 6.4 Daniel Nettle — *Personality: What Makes You the Way You Are* (Oxford University Press, 2007; Oxford Landmark Science reissue) **[P]**

**Argument.** A short, well-written popular account of the Big Five from an evolutionary-behavioural-ecology angle. Nettle's distinctive thesis is that trait variation persists because each trait involves **fitness trade-offs** — high extraversion buys mating and social opportunity at the cost of accident and instability; high neuroticism buys vigilance at the cost of distress; high openness buys creativity at the cost of psychosis risk — so no single optimum exists and variation is maintained.

**Chapters that matter.** One chapter per trait; the extraversion and neuroticism chapters are the best. The introductory chapters on where the Big Five came from (lexical hypothesis, factor analysis) are a clean short explanation of why there are five and what that does and does not mean.

**Honest note.** **Popular science, and the trade-off argument is speculative.** Nettle is a serious researcher and he flags the speculation, but the evolutionary explanations are post-hoc adaptive stories with thin direct evidence, and some of the behaviour-genetics discussion is dated (candidate-gene claims of that era largely failed to replicate; the field has moved to polygenic scores with small effects). Read it for the clearest short account of what the Big Five *are*; do not lean on the evolutionary chapters.

## 6.5 Samuel Gosling — *Snoop: What Your Stuff Says About You* (Basic Books, 2008) **[P]**, and directly on-topic

**Why it is here.** Gosling is the researcher behind the studies showing that observers rate strangers' personalities with above-chance accuracy from their **bedrooms and offices alone**, and he later co-authored much of the foundational work on personality and online profiles. *Snoop* is the trade account of that programme, and it is the closest existing book to "reading people from the visual traces they leave."

**The framework worth stealing.** Gosling's three-way classification of cues:
1. **Identity claims** — deliberate symbolic statements to self or others (posters, mottos, displayed awards). On Instagram: the bio, the highlight covers, the mission-statement post.
2. **Feeling regulators** — items arranged to manage one's own emotional state (photos of family, music, candles). Rarely visible in commercial accounts, which is itself diagnostic.
3. **Behavioural residue** — the physical traces of actual behaviour (wear patterns, mess, what is left out). **This is the category with the most inferential value and the least strategic control**, and it maps directly onto Goffman's "given off." On a business grid: the state of the workspace visible behind a product, the same three mugs recurring, the delivery boxes in the corner, the seasonal drift in a shop window.

Gosling also reports the crucial asymmetry: observers judge **conscientiousness and openness** relatively well from environments, **extraversion** poorly (because it is an interactional trait with little residue), and **agreeableness and neuroticism** essentially not at all. Note that this ordering is *different* from the ordering for face/photo-of-person judgments (where extraversion leads). That difference is a useful diagnostic about what kind of image you are looking at.

**Honest note.** Popular science, and it is written in a "here is a fun party trick" register that undersells the error bars — accuracy in these studies is real but modest (typically r ≈ .2–.4 for the good traits, near zero for the others), and Gosling reports this but does not let it dampen the tone. The underlying research (Gosling, Ko, Mannarelli & Morris, 2002, *JPSP*) is solid and replicated. Read the book, cite the paper.

## 6.6 Also useful

- **Nalini Ambady & John Skowronski (eds.), *First Impressions*** (Guilford, 2008) **[R]**. Edited scholarly volume; the definitive collection on thin-slice judgment. Ambady's own chapter and the chapters on accuracy vs. bias are the relevant ones. Note that some thin-slice findings have had replication difficulty; treat individual chapters case by case.
- **Robert Hogan / Brent Roberts** on socioanalytic theory: personality-as-reputation rather than personality-as-identity. Mostly in chapters and articles rather than books, but the framing — that "personality from the observer's side" *is* reputation, and reputation is a legitimate, measurable object — is the honest reframe for what image-based profiling can deliver. **Hogan, *Personality and the Fate of Organizations* (Lawrence Erlbaum, 2007)** is the short book-length statement. **[R-]**, opinionated.

---

# PART 7 — VISUAL RESEARCH METHODS IN SOCIAL SCIENCE

*The methods in this section are old, manual, slow, and frequently produce better and more defensible results than the ML approaches, because they force you to define your categories before you look.*

## 7.1 Gillian Rose — *Visual Methodologies*, 5th ed. (SAGE, 2022) **[M]/[R]**

See Part 0, #5. The organising text for this strand.

## 7.2 Theo van Leeuwen & Carey Jewitt (eds.) — *The Handbook of Visual Analysis* (SAGE, 2001) **[M]/[R]**

**What it is.** The methods handbook. Nine chapters, each a working method with worked examples: content analysis, historical analysis, structuralist analysis, iconography, psychoanalytic approaches, social semiotics, ethnomethodology, film and television analysis, and visual anthropology.

**The chapter that matters.** **Philip Bell, "Content Analysis of Visual Images" (Ch. 2).** This is the single best short statement of how to do quantitative content analysis on images: how to specify a **research question that content analysis can answer** (it answers "how often" and "in what proportion," never "what does this mean"); how to define **variables and their values** so that they are exhaustive and mutually exclusive; how to specify the **unit of analysis** (the image? the person in the image? the frame?); how to establish a **sampling frame**; and how to compute and report **inter-coder reliability** (Bell is clear that percentage agreement is insufficient and that a chance-corrected coefficient — Cohen's kappa, Krippendorff's alpha — is required). Bell's worked example uses magazine cover representations and explicitly builds on Goffman's categories.

**Why it is essential here.** Almost every "we analysed 200 Instagram posts" claim you will encounter fails Bell's criteria — no defined sampling frame, no operationalised variables, no second coder, no reliability statistic. Meeting them is not hard and it is the difference between an opinion and a finding. Apply Bell's checklist to your own pipeline and to anyone else's.

**Also in the volume.** Kress & van Leeuwen's own chapter on social-semiotic visual analysis; Iedema on film/TV; Diem-Wille on the psychoanalytic approach (skippable). **Honest note.** 2001, so nothing on digital or computational methods — pair it with Rose ch. 7 and Manovich. The content-analysis chapter has not been superseded.

## 7.3 Gunther Kress & Theo van Leeuwen — *Reading Images: The Grammar of Visual Design*, 3rd ed. (Routledge, 2021, 291pp) **[R]/[M]**

**Argument.** Images have a describable grammar. Building on Halliday's systemic-functional linguistics, Kress and van Leeuwen propose that visual composition realises three simultaneous "metafunctions":
- **Representational** — what is depicted: **narrative** structures (vectors between participants: who is acting on whom) vs. **conceptual** structures (classificatory, analytical, symbolic — the flat-lay product shot is a classic *analytical* process, showing part–whole relations).
- **Interactive** — the relationship constructed between image and viewer, via three systems that are **directly operational for reading Instagram photos**:
  - **Gaze/contact**: a **demand** image (depicted person looks at the viewer, establishing an imaginary relation and asking something of them) vs. an **offer** image (the person does not look out; they are offered as an item of information/contemplation).
  - **Size of frame / social distance**: close shot = intimate/personal; medium shot = social; long shot = impersonal. This is literally the grammar of how "approachable" a business account feels.
  - **Angle**: horizontal angle (frontal = involvement, "part of our world"; oblique = detachment, "their world, not ours") and **vertical angle** (high angle = viewer has power over the represented; eye level = equality; low angle = represented has power over the viewer).
- **Compositional** — how it is arranged: **information value** (left = Given/known, right = New; top = Ideal, bottom = Real — highly relevant to layouts and to the Instagram grid as a composed rectangle), **salience** (size, colour, contrast, focus), and **framing** (connection vs. disconnection of elements).

**Why it matters.** This is the most complete and most operationalisable vocabulary available for *what a photograph is doing to its viewer*. Combined with Goffman's pose categories and Bell's coding discipline, it gives you a full manual coding scheme for an Instagram grid that is theoretically motivated, reliably codable, and defensible — and it produces variables ("proportion of demand images," "median social distance," "modal vertical angle") that can then be correlated with engagement or compared across competitor accounts.

**Honest note.** Rigorous within social semiotics, but be clear about its epistemic status: it is a *descriptive grammar of visual convention within Western visual culture*, not a claim about universal perception or about the depicted person's psychology. Kress and van Leeuwen say this explicitly; readers routinely ignore it and treat "low angle = power" as a psychological fact. It is a convention. Also: the theory is asserted rather than empirically validated, and the 3rd edition's updates for digital media are lighter than they should be.

## 7.4 Photo elicitation

- **Douglas Harper, *Visual Sociology*** (Routledge, 2012) **[R]/[M]** — the standard text on the field, with the best treatment of photo elicitation (showing photographs to interviewees to generate talk). Harper's classic 2002 article "Talking about pictures: a case for photo elicitation" (*Visual Studies* 17(1)) is the short version and is widely available.
- **Why it matters here.** Photo elicitation is **the correct method for the question that image-analysis is usually being used to dodge.** If you want to know what an account's photos mean, showing the photos to the account's actual customers and asking is cheaper, faster, and vastly more valid than any inference from pixels. In a small-business context — a distributor, a shop — a twenty-minute elicitation session with five customers will beat a computer-vision pipeline on every dimension except scale. Include this in any methodology as the validation step.
- **Sarah Pink, *Doing Visual Ethnography*, 4th ed. (SAGE, 2021)** **[R]/[M]** — for the reflexive, participatory end; strong on ethics and on the researcher's own position in image-making. Ch. on digital and social media contexts is current.

## 7.5 A note on why the manual methods are often better

Three concrete reasons, worth stating in any methodology section:
1. **Construct definition precedes measurement.** A coding scheme forces you to say what "aspirational" means before you count it. A classifier lets you skip that step and inherit whatever the training labels meant.
2. **Reliability is reportable.** Two coders and a kappa is an auditable claim about measurement quality. "The model achieved 87% accuracy" is a claim about a benchmark, not about your corpus.
3. **The n is usually small anyway.** Most real briefs concern one account, or five competitors, or 200 posts. At that scale, manual coding is *faster* than building a pipeline, and it is the scale at which classifier error rates are least tolerable.

---

# PART 8 — MARKETING AND CONSUMER ANALYTICS

**Finding: there is no good book-length treatment of image analytics in marketing.** The field is three or four years old in publication terms and lives in journals. The honest answer is that the book-length material here is either (a) survey chapters in edited academic volumes, or (b) practitioner books whose analytics content is thin.

## 8.1 The best available: survey chapters, not books

- **Xiaohang (Flora) Feng, Shunyuan Zhang & Kannan Srinivasan, "Marketing Through the Machine's Eyes: Image Analytics and Interpretability,"** in *Artificial Intelligence in Marketing* (Review of Marketing Research vol. 20, Emerald, 2023). **[R]** The best single survey. Organises the literature on three axes: data type (image vs. video), model structure (**feature-level** — extract interpretable attributes then model them — vs. **pixel-level** — end-to-end deep models), and application (firm profit vs. consumer utility). The **feature-level vs. pixel-level distinction is the most important practical choice** in an image-analytics project: feature-level is interpretable, auditable, and defensible to a client; pixel-level is more accurate and explains nothing. For consulting work on small accounts, feature-level is almost always correct.
- **Liu, Dzyabura & Mizik**'s "Visual Listening In" (*Marketing Science*, 2020) and the **Journal of the Academy of Marketing Science** 2023 review "Beyond text: Marketing strategy in a world turned upside down" are the other entry points. Covered in `03-marketing-profiling.md`.
- **"Image Analytics in Marketing"** (chapter in *Handbook of Marketing Analytics* / Springer *Handbook of Marketing Decision Models* lineage) — useful bibliography, thin on method.

## 8.2 Psychographic segmentation — the practitioner canon, honestly assessed

- **Michael Solomon, *Consumer Behavior: Buying, Having, and Being*** (Pearson, 13th+ ed.) **[R-]/[M]**. The standard textbook. The chapters on lifestyle and psychographics, on the self and self-concept, and on symbolic consumption are the relevant ones. Reliable as a survey of what the field believes; note that psychographic segmentation's *predictive* track record is much weaker than textbooks imply.
- **VALS, PRIZM, Mosaic** — these have no good books; they have vendor documentation. The scholarly assessment is that geodemographic segmentation (PRIZM, Mosaic) has real predictive validity for consumption because it is essentially a proxy for income, life stage and location, whereas *psychographic* segmentation on attitudes and values adds little beyond demographics for most categories. Wells' 1975 *JMR* review "Psychographics: A Critical Review" is still the best single assessment and its criticisms — unreliable instruments, unreplicated segment structures, low predictive validity — have not been answered.
- **Mark Jeffery, *Data-Driven Marketing: The 15 Metrics Everyone in Marketing Should Know*** (Wiley, 2010) **[M]**. Not about images at all, but it is the most disciplined popular treatment of *which metrics are worth measuring* and how to tie them to outcomes. Useful as a corrective to vanity-metric analysis of accounts.
- **Byron Sharp, *How Brands Grow*** (Oxford UP, 2010) and *How Brands Grow Part 2* (2016) **[R-]**, deliberately included as an irritant. Sharp's empirical-generalisations position — that brand growth comes from **mental and physical availability** and **penetration** rather than from differentiation, loyalty or precise segmentation — is the most serious available challenge to the entire psychographic-profiling enterprise. If Sharp is right, most audience-profiling work is answering a question that does not drive growth. He overstates (the "differentiation doesn't matter" claim is stronger than his evidence, and Ehrenberg-Bass's data is heavily FMCG-weighted, which does not obviously transfer to small local businesses or niche B2B). But any profiling deliverable should be able to answer the Sharp objection, and most cannot.

## 8.3 Honest summary of this strand

For a working project, the marketing-books strand contributes **less than any other section in this file.** The rigorous content is in journals; the book-length content is practitioner material that mostly recycles frameworks (archetypes, colour psychology, content pillars) with no validation behind them. Use `03-marketing-profiling.md` and treat this section as background.

---

# PART 9 — SPANISH-LANGUAGE AND LATIN AMERICAN SOURCES

*Argentine and regional material, plus Spanish-language works that are standard in Southern Cone university curricula. Several are free.*

## 9.1 Paula Sibilia — *La intimidad como espectáculo* (Fondo de Cultura Económica, Buenos Aires, 2008, 325pp) **[R]** — the most valuable Spanish-language entry

**Argument.** Sibilia (Argentine, based at Universidade Federal Fluminense in Brazil) analyses the migration of the self from *interiority* to *exteriority*: the modern subject, built through introspective genres — the diary, the letter, psychoanalysis, the novel — is being displaced by a subject constituted through **public exhibition**. Her key terms: **la personalidad alterdirigida** (the other-directed personality, after Riesman), **el yo visible** (the self that exists by being seen), **el imperativo de la visibilidad**, and **el show del yo**. Her diagnosis is that this is not narcissism but a *mutación de las subjetividades* — a historical change in what a self is.

**Why it belongs at the top of this section.** Written in 2008 about blogs, fotologs, webcams and YouTube, it anticipates the Instagram condition precisely, and it does so from an explicitly Latin American vantage. For a project reading Argentine commercial accounts, it supplies the local conceptual vocabulary — and it is the book Argentine clients, journalists and academics will already have heard of.

**Chapters that matter.** The chapters on **"yo narrador"** and the history of self-narration; **"el ocaso del hombre interior"**; **"la desarticulación del yo"**; and the treatment of the *self-portrait* as a genre with a long history into which the selfie inserts itself. Her earlier *El hombre postorgánico* (FCE, 2005) is about bodies and biotechnology and is not needed here.

**Honest note.** Rigorous in the continental-theory register: Foucault, Deleuze, Sennett, Riesman, Barthes. Not empirical — no data, no coding, no sampling. It is a theoretical essay of high quality. Cite it for framing, never for a finding. Widely available in Argentina and in PDF through university repositories.

## 9.2 Lev Manovich — *Instagram y la imagen contemporánea* (trad. española, DCCD-UAM Cuajimalpa, 2020; free) **[R]**

The Spanish translation of Part 0, #3. Free, CC-licensed, and the fact that it exists in Spanish makes it the single most useful thing to hand an Argentine collaborator who needs to understand what computational Instagram analysis actually looks like. Also translated into Japanese and Farsi.

## 9.3 Silvia Rivera Cusicanqui — *Sociología de la imagen: miradas ch'ixi desde la historia andina* (Tinta Limón, Buenos Aires, 2015, 352pp) **[R]/[C]**

**Argument.** The Bolivian sociologist's method for reading images as historical and political documents — developed in the Taller de Historia Oral Andina and applied to colonial-era illustrations (Guamán Poma), photographs, murals and contemporary visual culture. **"Ch'ixi"** is her key concept: a state that is simultaneously two things without synthesis, a spotted grey that is neither black nor white — her model for Andean modernity and for reading images that carry contradictory meanings at once. She treats the image not as illustration of a text but as an autonomous source of knowledge, and she is explicit that reading images is a *decolonial practice* opposed to the extraction of data about people.

**Why it is here.** Two reasons. It is the major Latin American statement of visual sociology as a method, and it belongs in any regionally literate bibliography. And it is the sharpest available counterweight to the extractive posture of image-based profiling: her argument that images should be read *with* their subjects rather than *about* them is the intellectual foundation for the photo-elicitation move in §7.4, arrived at independently and from a very different politics.

**Honest note.** Rigorous but idiosyncratic; it is essayistic, aphoristic, and makes no attempt at replicable procedure. Do not expect a coding scheme. Free PDF available from Tinta Limón. Published in Buenos Aires by an Argentine press.

## 9.4 Marta Peirano — *El enemigo conoce el sistema: manipulación de ideas, personas e influencias después de la economía de la atención* (Debate, 2019) **[P]**

**Argument.** The best-selling Spanish-language book on data extraction and attention capture. Peirano (Spanish journalist) traces the infrastructural history — from ARPANET's design intentions to the current concentration — and argues that a network built for horizontal distribution has become an apparatus of surveillance and mass manipulation, with the attention economy as its engine. Covers Cambridge Analytica, dark patterns, addiction design, and information warfare.

**Honest note.** Popular, journalistic, well sourced, and genuinely good — but it is the Spanish-language equivalent of *Weapons of Math Destruction* plus Zuboff, and it carries the same tendency to treat "targeting was attempted" as "targeting worked." Peirano is notably credulous on Cambridge Analytica's efficacy; read §4.4 above alongside it. Excellent as a first book for a Spanish-speaking stakeholder; not a source. Her *Contra el futuro* (2022) on climate and technology is also good, off-topic here.

## 9.5 Natalia Zuazo — *Guerras de Internet: un viaje al centro de la red para entender cómo afecta tu vida* (Debate Argentina, 2015) and *Los dueños de Internet: cómo nos dominan los gigantes de la tecnología y qué hacer para cambiarlo* (Debate Argentina, 2018) **[P]**

**Argument.** Zuazo is an Argentine journalist specialising in politics and technology, and these are **the Argentine books** on the subject. *Guerras de Internet* denaturalises how the network works — infrastructure, governance, cables, control points — with Argentine and Latin American cases throughout. *Los dueños de Internet* is on platform concentration and what regulation could look like from a Latin American position.

**Honest note.** Popular journalism, competently done, locally grounded. No original research. Value is contextual: they explain the *Argentine* regulatory, infrastructural and political situation, which no anglophone book does, and they are the reference points a local audience will recognise.

## 9.6 Argentine data protection — legal references

- **Ley 25.326 de Protección de Datos Personales** (2000) and its regulatory decree, plus the **Agencia de Acceso a la Información Pública (AAIP)** dispositions. The statute predates social media entirely; it is built on a **registered-database** model that fits poorly with scraping and inference. Note the practical points: photographs of identifiable people are personal data; **inferred** data (a personality score derived from photos) is generally treated as personal data about the subject under the prevailing interpretation; and Art. 2's definition of *datos sensibles* does not map cleanly onto inferred psychological attributes, which is a live gap.
- **Pablo A. Palazzi, *La protección de los datos personales en la Argentina: ley 25.326 comentada y anotada con jurisprudencia*** (Errepar, 2004; and his subsequent commentary volumes with Astrea) **[M]**. The standard practitioner commentary. Dated on technology, still the reference on the statute and case law. Palazzi has continued publishing on habeas data, the right to be forgotten, and identity theft.
- **AAIP, *Proyecto de Ley de Protección de Datos: diversas miradas y un consenso — la necesidad de actualizar la legislación argentina*** (AAIP, 2023, free PDF at argentina.gob.ar) **[R-]**. A genuine book-length report, multi-author, on the reform bill sent to Congress in 2023 to replace Ley 25.326. This is the single best current source on where Argentine data protection is heading — including the treatment of automated decision-making, profiling (*elaboración de perfiles*), and biometric data, all modelled substantially on the GDPR. **If your work involves profiling Argentine accounts, this is the document that tells you what the rules are about to become.**
- **Fundación Vía Libre** (Córdoba; Beatriz Busaniche) — publishes free reports on AI, personal data and rights in Argentina, several under open licences and collected in the Ártica digital library. Their material on **automated decision-making and biometric surveillance in Argentina** (including the analysis of Buenos Aires' facial-recognition system, ultimately ruled unconstitutional in its implementation) is the best local critical work. Report-length rather than book-length, but substantive and free.

## 9.7 Byung-Chul Han — *Psicopolítica: neoliberalismo y nuevas técnicas de poder* (Herder, 2014) **[C]**

**Argument.** Power no longer works by repression (*biopolítica*) but by seduction and self-optimisation (*psicopolítica*): the subject exploits itself freely and believes itself free while doing so. Big Data functions as a "digital panopticon" in which data are surrendered voluntarily and enthusiastically, enabling prediction and pre-reflective conditioning. Related: *La sociedad de la transparencia* (Herder, 2013) on the compulsion to display, and *En el enjambre* (2014).

**Honest note.** **Philosophical polemic, not scholarship**, and it should be labelled as such. Han asserts rather than argues, cites almost nothing, is empirically indifferent, and repeats himself across books. He is also enormously influential in Spanish-language public discourse and is likely to be quoted at you. The *transparency* argument — that compulsory visibility is a form of control precisely because it feels like freedom — is genuinely useful for thinking about why businesses feel obliged to perform openness on Instagram. Read one of these books, not four, and do not cite him for anything factual.

## 9.8 Justo Villafañe — *Introducción a la teoría de la imagen* (Ediciones Pirámide, Madrid, 1985; 5th ed. 2001, 232pp) **[M]/[R-]**

**Argument.** The Spanish-language classic on **image analysis method**. Villafañe (Universidad Complutense) sets out to establish a methodology for studying images using only *iconic* categories — properties specific to images rather than borrowed from linguistics — organised around the two processes of **percepción** and **representación**. Includes an operational **modelo de análisis de la imagen**: identifying the *elementos morfológicos* (punto, línea, plano, textura, color, forma), *dinámicos* (tensión, ritmo), and *escalares* (dimensión, formato, escala, proporción), and the concept of *orden icónico*.

**Why it is here.** It is the reference used in Spanish-speaking communication faculties, so it is the shared vocabulary in that world; and its element-by-element analysis grid is a genuinely usable manual coding scheme for composition, complementary to Kress & van Leeuwen's semiotic one. Villafañe & Mínguez's *Principios de teoría general de la imagen* (Pirámide, 1996) is the fuller version.

**Honest note.** Dated (pre-digital), formalist, and its Gestalt-derived perceptual claims are the weakest part. The analytical grid survives the datedness.

## 9.9 Gaps in the Spanish-language literature — stated honestly

Searching thoroughly, **there is no good Spanish-language book on**: computational analysis of social media images; personality inference from digital traces; or empirically grounded Instagram analysis for business. What exists in Spanish is (a) translated anglophone material, (b) theory in the Sibilia/Han register, (c) journalism in the Peirano/Zuazo register, and (d) practitioner marketing books of low evidentiary value. The academic Spanish-language work on selfies and Instagram aesthetics is in journal articles and theses, not books — e.g. the Latin American communication journals, and the review literature around the Spanish translation of Manovich. If you need Spanish-language material for a client deliverable, the honest set is: **Sibilia + Manovich (trad.) + Zuazo + the AAIP 2023 report.**

---

# PART 10 — SUMMARY TABLE

| # | Book | Year / Publisher | Verdict | Use it for |
|---|---|---|---|---|
| 1 | Todorov, *Face Value* | 2017, Princeton UP | **[R]** | Why face-based trait inference fails; the photo-to-photo variance finding |
| 2 | Goffman, *Gender Advertisements* | 1979, Harper & Row | **[R-]/[M]** | A codable vocabulary of poses; hyper-ritualisation |
| 3 | Manovich, *Instagram and Contemporary Image* | 2017, self-pub (free; ES 2020) | **[R]/[M]** | Casual/professional/designed typology; the feed as unit |
| 4 | Crawford, *Atlas of AI* (ch. 5) | 2021, Yale UP | **[R]/[C]** | The affect-recognition demolition; how to refuse a brief |
| 5 | Rose, *Visual Methodologies* 5e | 2022, SAGE | **[M]/[R]** | Four sites × three modalities; content analysis procedure |
| 6 | Funder, *Personality Judgment* (RAM) | 1999, Academic Press | **[R]** | Good judge/target/trait/information — what is knowable |
| 7 | Barocas, Hardt & Narayanan, *Fairness and ML* | 2023, MIT (free) | **[R]/[M]** | Impossibility theorem; construct validity; causality |
| 8 | Hersh, *Hacking the Electorate* | 2015, Cambridge UP | **[R]** | The "perceived voter"; deflating psychographic hype |
| 9 | Goffman, *Presentation of Self* | 1959, Anchor | **[R]** | Given vs. given off — the core analytic distinction |
| 10 | Kress & van Leeuwen, *Reading Images* 3e | 2021, Routledge | **[R]/[M]** | Demand/offer, social distance, angle, Given/New |
| 11 | van Leeuwen & Jewitt (eds.), *Handbook of Visual Analysis* | 2001, SAGE | **[M]** | Bell ch. 2 — how to do image content analysis properly |
| 12 | Leaver, Highfield & Abidin, *Instagram* | 2020, Polity | **[R]** | Platform, aesthetics, economies of Instagram |
| 13 | Gosling, *Snoop* | 2008, Basic | **[P]** | Identity claims / feeling regulators / behavioural residue |
| 14 | Mischel, *Personality and Assessment* | 1968, Wiley | **[R-]** | The .30 personality-coefficient ceiling |
| 15 | Pearl, *About Faces* | 2010, Harvard UP | **[R]** | Physiognomy as historical visual literacy |
| 16 | Sibilia, *La intimidad como espectáculo* | 2008, FCE | **[R]** | The Spanish-language framing; el show del yo |
| 17 | Benjamin, *Race After Technology* (ch. 3) | 2019, Polity | **[R]/[C]** | Coded exposure; the racial history of photography |
| 18 | Chun, *Discriminating Data* | 2021, MIT | **[R]/[C]** | Correlation's eugenic genealogy; homophily as assumption |
| 19 | Rust, Kosinski & Stillwell, *Modern Psychometrics* 4e | 2021, Routledge | **[R]/[M]** | The honest measurement framework behind digital footprints |
| 20 | Matz, *Mindmasters* | 2025, HBR Press | **[P]→[P!]** | Landscape and ethics; **not** effect sizes |
| 21 | Hill, *Your Face Belongs to Us* | 2023, Random House | **[P]** | What scraping public photos leads to, operationally |
| 22 | Manovich, *Cultural Analytics* | 2020, MIT | **[R]/[M]** | Media visualisation; sampling in cultural corpora |
| 23 | Noble, *Algorithms of Oppression* | 2018, NYU | **[R]** | Ranking as commercial product, not mirror |
| 24 | O'Neil, *Weapons of Math Destruction* | 2016, Crown | **[P]** | The opacity/scale/damage heuristic; ch. 6 on hiring tests |
| 25 | Broussard, *More Than a Glitch* | 2023, MIT | **[P]** | Technochauvinism; when not to build |
| 26 | D'Ignazio & Klein, *Data Feminism* | 2020, MIT (free) | **[R]/[M]** | "Consider context"; the numbers don't speak |
| 27 | Marwick, *Status Update* | 2013, Yale UP | **[R]** | Self-branding and micro-celebrity as labour |
| 28 | Abidin, *Internet Celebrity* | 2018, Emerald | **[R-]/[P]** | Calibrated amateurism; taxonomy of online fame |
| 29 | Duffy, *(Not) Getting Paid…* | 2017, Yale UP | **[R]** | Authenticity as an occupational register |
| 30 | Tiidenberg, *Selfies* | 2018, Emerald | **[R-]/[P]** | Deflating the narcissism claim |
| 31 | Nettle, *Personality* | 2007, Oxford UP | **[P]** | The clearest short account of the Big Five |
| 32 | Kahneman, *Thinking, Fast and Slow* | 2011, FSG | **[P]** | WYSIATI, attribute substitution, illusion of validity — **not ch. 4** |
| 33 | Zuboff, *Age of Surveillance Capitalism* | 2019, PublicAffairs | **[C]** | Behavioural surplus (read Gandy or Couldry instead) |
| 34 | Wylie, *Mindf\*ck* / Kaiser, *Targeted* | 2019 | **[P!]** | What was *attempted*; **not** what worked |
| 35 | AAIP, *Proyecto de Ley de Protección de Datos* | 2023, AAIP (free) | **[R-]** | Where Argentine profiling law is heading |
| 36 | Peirano, *El enemigo conoce el sistema* | 2019, Debate | **[P]** | Spanish-language entry point (credulous on CA) |
| 37 | Zuazo, *Los dueños de Internet* | 2018, Debate AR | **[P]** | Argentine platform-power context |
| 38 | Rivera Cusicanqui, *Sociología de la imagen* | 2015, Tinta Limón | **[R]/[C]** | Decolonial visual method; reading *with* not *about* |
| 39 | Villafañe, *Introducción a la teoría de la imagen* | 1985/2001, Pirámide | **[M]/[R-]** | Spanish-language compositional analysis grid |
| 40 | Han, *Psicopolítica* | 2014, Herder | **[C]** | The transparency-as-control framing; cite nothing |

---

# PART 11 — THE BOOKS THAT OVERCLAIM, STATED PLAINLY

Asked to be discriminating, here is the blunt version.

**Overclaims materially:**
- **Wylie, *Mindf\*ck*** and **Kaiser, *Targeted*** — both require Cambridge Analytica's targeting to have worked for their authors to matter. The ICO investigation, the academic assessment (Bakir 2020), and the campaign-effects literature (Kalla & Broockman 2018) all point the other way. The data harvest was real; the mind-control was a sales pitch that the whistleblowers have an incentive to keep alive.
- **Matz, *Mindmasters*** — the best of the trade books on psychological targeting, written by a real researcher, and still inflated. It generalises from relative click-through lifts on matched-vs-mismatched Facebook ads to a general claim about predicting and changing human behaviour. Use it to map the field; cite Matz et al. 2017 *PNAS* and its critics for numbers.
- **Barrett, *How Emotions Are Made*** — right about the problem with basic-emotion theory, overconfident about her own replacement.
- **Kahneman, *Thinking, Fast and Slow*, chapter 4** — not the whole book, but that chapter and the social-priming material are not reliable and Kahneman said so himself.
- **Zuboff, *Age of Surveillance Capitalism*** — not fabricated, but rhetorically inflated, historically thin, and it under-credits twenty-five years of prior scholarship. Vocabulary yes, authority no.
- **Han, *Psicopolítica*** — aphorism presented as analysis. Influential, unfalsifiable, uncitable.
- **The practitioner marketing canon** (brand archetypes, colour psychology, "content pillars", VALS-style psychographics) — near-universally unvalidated. Useful as shared vocabulary with clients, worthless as evidence. Byron Sharp is the useful antidote, and he overclaims in the other direction.

**Popular but honest:** O'Neil, Broussard, Gosling, Nettle, Hill, Peirano, Zuazo, Tiidenberg, Abidin. Each of these is a working expert writing accessibly and flagging their own limits. Read them; verify against the underlying work before citing.

**Rigorous, safe to build method on:** Todorov, Funder (both), Rose, Bell-in-van-Leeuwen-&-Jewitt, Kress & van Leeuwen, Barocas/Hardt/Narayanan, Hersh, Leaver/Highfield/Abidin, Manovich (both), Pearl, Noble, Benjamin, Chun, Rust/Kosinski/Stillwell, Marwick, Duffy, Sibilia, Rivera Cusicanqui.

---

# PART 12 — WHAT THE BOOKS COLLECTIVELY IMPLY FOR METHOD

Six conclusions that fall out of reading across all of them:

1. **Separate the two questions.** "What does this image communicate to viewers?" is tractable, measurable, and commercially valuable (Todorov, Kress & van Leeuwen, Manovich). "What is the person behind it like?" is largely intractable from images (Todorov, Funder, Mischel). Every deliverable should answer the first and decline the second.

2. **Code the "given off," describe the "given."** The strategic surface of an account (Goffman's *given*) tells you about intended positioning and professional competence. The unintended residue (Goffman's *given off*, Gosling's *behavioural residue*) is where the weak-but-real inferential signal lives — workspace, recurring props, seasonal drift, production consistency, staffing visible in frame.

3. **Use a coding scheme with reliability, not a vibe or a classifier.** Bell's procedure, applied to Goffman's pose categories and Kress & van Leeuwen's interactive systems, gives defensible variables at the scale most briefs actually operate at. Report kappa.

4. **Expect r ≈ .2–.3 and say so.** Mischel's ceiling plus Funder's RAM predict, before any data collection, that extraversion and openness will be weakly readable and neuroticism and agreeableness will not be. This is not a failure of technique.

5. **Prefer feature-level to pixel-level.** Feng, Zhang & Srinivasan's distinction: interpretable features you can name and defend beat an end-to-end model you cannot explain, particularly at n = 200 posts and particularly when a client will ask "why."

6. **Validate by asking humans.** Photo elicitation (Harper, Rose ch. 12) is cheaper and more valid than any inference pipeline for the question "what does this feed communicate to your customers?" It is also the ethical form of the method — reading images *with* people rather than extracting claims *about* them (Rivera Cusicanqui).

---

*Prepared as part of the research series in `/home/user/Fede/research/raw/`. Companion files: `01-personality-images.md` (the empirical psychology literature), `03-marketing-profiling.md` (marketing science and practitioner frameworks), `04-methods-pipeline.md` (implementation), `05-ethics-legal.md` (ethics and law).*
