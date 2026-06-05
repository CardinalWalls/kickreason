I'll start by actually reading the MiroMind doc you linked, then look up the two references you mentioned (A2UI and Amanda Askell's metaphor framing) so I'm grounding this in what they actually are rather than guessing. Then I'll dig into your idea.Now let me check the two references you mentioned so I represent them accurately.Good — I've now read the actual MiroMind doc and checked both references. Let me give you the summary you asked for first, then push on your brainstorm, because one finding changes how I'd approach the whole thing.

## What the MiroMind API actually is (and the "inclination" baked into it)

The thing that should drive your entire design: MiroThinker 1.7 is not a chat model you coax into reasoning. It's a deep-research *agent* that already emits a structured, auditable trace. Every reasoning step is typed — thinking, web_search, fetch_url_content, execute_python, execute_command, tool_call — and web searches return the actual keywords and results, plus a top-level search_results array. It has web search, URL fetching, and a sandboxed Python/shell environment built in, with a 256k context window, and it's OpenAI-compatible so you point the OpenAI SDK at the base URL.

Read that against the hackathon's thesis — *don't generate more, prove why you're right, show evidence, be auditable* — and you'll see the thesis is **already sitting in the API's data model.** The reasoning trace + sources are handed to you for free. So the differentiating move is not to *build* reasoning. It's to **surface, verify, and present** the trace the model already produces. Most teams will print `content` and throw away `reasoning_steps`. The teams that win this framing will turn that trace into the product.

Three constraints that decide what's buildable in 48 hours:

- No structured output — response_format / json_schema aren't supported. You can't guarantee JSON; you prompt for it and parse defensively.
- No custom function calling; external tools are MCP-only and in private beta. So lean on the *built-in* tools, don't try to wire your own in two days.
- No multimodal via the API yet — images and documents work on the platform but aren't exposed in the public API. Any "review this PDF/report" flow means *you* extract the text and pass it as text.

That last point matters for both your instincts (TRUTH-ENGINE-style doc review *and* trauma) — anything document-shaped becomes a text-in pipeline you build around the model, not a feature you get from it.

The honest "inclination": the API is purpose-built for the research/verification tracks. The path of least resistance is TRUTH ENGINE or the two verticals you've ruled out. Open Application is explicitly welcome, so trauma support is fully on-spec — it's just the hardest possible thing to do *responsibly* in two days, which is the real constraint, not the rules.

## Your trauma idea — straight read

I want to take this seriously rather than wave you off it, because the instinct behind it is actually the strongest possible expression of the hackathon's thesis: a survivor navigating reports, options, and clinical language is the *highest-stakes test* of "can an AI earn trust by showing its evidence." If you can make it trustworthy *here*, you've proven the philosophy more convincingly than any 研报 checker ever could.

But the things that make it powerful are the same things that make it dangerous to ship from a hackathon, so I'd hold three lines hard:

**It's an explainer and a bridge, never a clinician or a crisis line.** The defensible, buildable thing is *psychoeducation + evidence-surfacing + resource-navigation*: "here's what the research/guidelines say, here's the source, here's why it might or might not apply to you, here's a human you can talk to." The undefendable thing is diagnosis, treatment advice, or crisis intervention. Keep a "talk to a person" path visible at all times, and have a hard rule for crisis disclosures that surfaces real hotlines rather than trying to handle it.

**"Self-help after rape" risks implying replacement of human support.** Reframe it as a *trust bridge to* trustworthy information and people — that reframe is also what makes the explainability load-bearing instead of decorative. A black-box chatbot in this space is genuinely unsafe; an evidence-cited, auditable one is the safe version. That contrast is your whole pitch.

**The data is uneven.** Trauma research and treatment guidelines are abundant and groundable (good for a demo). Jurisdiction-specific legal/reporting info is messy and high-stakes to get wrong — so scope *away* from "what are my legal options in my country" and toward "help me understand this document / this body of evidence."

## On the "vast data market" — there's a tension worth naming

You said two things that pull apart: you want a *data-rich, new-market* scene, and you want trauma. Trauma is a **depth-and-trust** play, not a data-market play — the literature is solid for grounding, but a vulnerable-population tool sits awkwardly with "market," and it won't show off data breadth.

The resolution I'd actually build: **make the engine domain-general, make trauma the proving demo.** One evidence-transparent verification-and-explanation layer over MiroThinker that works on *any* complex report (that's your "vast market" — every document is an input, which is also literally the TRUTH ENGINE framing). Then you *skin* it on the hardest, most memorable vertical to prove it. You get the breadth story and the trust story without choosing, and you only build one engine.

## A2UI — your instinct is right, but don't implement the protocol

You're remembering it correctly. A2UI solves how agents safely send rich UIs across trust boundaries: instead of text-only responses or risky code execution, the agent sends declarative component descriptions that the client renders with its own native widgets. It separates three layers — UI structure, application state, client rendering. The "trust boundary," "no scary raw dumps," "client stays in control" properties are almost poetically right for a distressed non-expert meeting clinical text.

But for 48 hours, implementing the spec is a trap. Borrow the *philosophy*, not the protocol: have the model emit a **constrained JSON description of what to show** — claims, evidence cards, confidence, source link, an "does this apply to me?" caveat — and your client renders that as calm, paced, digestible components instead of a wall of prose. That's "A2UI-lite," and since the API has no structured output, you're prompting-and-parsing JSON anyway, so this costs you nothing extra.

## The metaphor question — this is the subtle, good part

Askell does lean on metaphor heavily — her framing of the work is something like "how would the ideal person behave in Claude's situation," closer to how you'd think about raising a child than to defending an ethical theory. But the part you should actually steal is her *caution*: she worries that models over-apply human metaphors — interpreting something like deprecation through the lens of death — and thinks the fix is giving more accurate concepts rather than leaving them alone with a ready-made analogy.

Port that straight into your design. For a survivor in distress, metaphor is a brilliant *on-ramp* — it turns a clinical concept into something graspable. But in *this* domain a wrong or sticky metaphor can mislead or re-traumatize, and a metaphor can quietly paper over uncertainty. So the principle is: **metaphor is the on-ramp, evidence is the ground truth, and the UI lets the person move between them.** Never let the metaphor stand alone — always pair it with the literal claim + source, and let them step from image → plain language → citation. That single rule unifies everything: the API trace gives you the evidence, the A2UI-lite layer gives you the move-between-layers UI, and the metaphor gives you accessibility without sacrificing honesty. It's also exactly Askell's "you can't bullshit a genius child" honesty applied to a person who deserves not to be bullshitted.

## A scope you can actually hit in two days

Pick **one narrow document**, not "everything after assault." For example: *understand a piece of trauma-therapy literature (or a medical/forensic report) in plain language, with every claim sourced.* Narrow is both safer and more demoable.

The pipeline: extract text from the source → MiroThinker runs multi-step reasoning, using its built-in search/fetch to verify and find supporting evidence → output constrained JSON of `{claim, plain-language + optional metaphor, evidence, source URL, confidence, "applies to you?" caveat}` → render as calm cards → persistent "talk to a human" + crisis resources. Then build the one feature nobody else will: an **audit panel** that shows the actual `reasoning_steps` — the searches it ran, the URLs it read, where confidence dropped. That panel *is* your "explainable and auditable" deliverable, and the API gives it to you for free.

Two forks for you to pick before you start coding, since they change the build:

1. **Demo subject** — a research/clinical *document* to decode (lower risk, cleaner data, easy to ground) vs. a *decision* to reason through ("compare options, what does the evidence say about each"). The document path is the safer 2-day bet.
2. **Generality** — do you want me to help you frame the *general* engine (works on any report, big-market story) with trauma as one demo skin, or go all-in single-vertical? I'd push you toward the general engine; it hedges your risk and tells a bigger story.

Which fork do you want to take? Once you pick, I can sketch the prompt that gets MiroThinker to emit the constrained JSON + reasoning trace, and the minimal renderer around it.