就想知道想要对这种trauma aware的，就比如说遭到性侵的这样的女孩提供咨询的话，有哪些权威的指南或者APP？就是我记得我女朋友分享过给我一个英国的某个网站的权威的一个指南。但那个东西应该是十年以前的，我想知道，而且我想知道的是方法论不仅仅是一种不仅仅是一个自助手册吧。就是说我，比如说他可，我想知道的是，在任何文，他能如何能够去分析他的这种详细的这种权利背景，他比如说他的熟人侵犯怎么办？还有的话就是一些宗教里面的，比如说基督教的一些内部的一些事务怎么办？就是我觉得我就希望有这种比较详细的但我想开发的是一个Agent或者是语音助手，我知道是有这种trauma aware这样的这样的东西的。
已完成 3 个步骤
有，而且这类内容里最值得参考的不是“自助手册型鸡汤”，而是把 创伤知情（trauma-informed）+ 权利/转介路径 + 法律与医疗选项 + 支持者怎么说怎么做 结合起来的权威指南。英国这条线最接近你记忆里的资源，当前仍然很实用的是 NHS、Rape Crisis England & Wales、The Survivors Trust 这一套；国际方法论层面则通常会回到 WHO 关于亲密伴侣暴力与性暴力应对框架。
权威指南
英国 NHS 的“Help after rape and sexual assault”不是单纯心理自助页，而是把求助路径、SARC（性侵转介中心）、法医取证、是否报警、保密范围、熟人侵害、伴侣侵害、饮料被下药等都放进同一条服务路径里，这很适合作为 Agent 的“权利与选项地图”底座。
Rape Crisis England & Wales 的“Supporting a survivor”更偏 interaction protocol，核心原则是“听、信、不给细节压力、不给替代决策、尊重边界与节奏”，非常适合转成语音助手的回复策略和安全话术模板。
WHO 的《Responding to intimate partner violence and sexual violence against women》属于上层方法论来源，强调对披露暴力的女性提供一线支持，而不是先做审问式追问；这类框架常被概括为以安全、支持、验证、转介为核心的初始响应原则。
可直接参考的网站
如果你要找“英国那个权威网站”，最可能接近的是 NHS 性侵后求助页面 (https://www.nhs.uk/live-well/sexual-health/help-after-rape-and-sexual-assault/) 或 Rape Crisis England & Wales (https://rapecrisis.org.uk/get-help/supporting-a-survivor/)。这两个站现在都还在维护，而且信息更新明显比十年前完整，尤其 NHS 页面明确写到：性暴力是犯罪、是否报警由当事人决定、熟人也可能是施害者、SARC 可在未决定报警前先做医疗与证据保存支持。
英国政府的 GOV.UK victims support 页面 (https://www.gov.uk/guidance/support-for-victims-of-sexual-violence-and-abuse) 也有价值，因为它把官方热线、Rape Crisis、The Survivors Trust、LGBT+ 专线、童年受虐成年人支持等资源集中列出来，适合做 Agent 的地区化转介目录。
如果你想做组织/服务网络层面的目录，The Survivors Trust 提供英国与爱尔兰的成员机构网络和全国热线目录，也比较适合做“本地服务发现”模块。
APP 与数字工具
严格说，权威“APP”反而没有权威网站和热线体系那么成熟。从当前能查到的公开权威资源看，英国主流还是以 NHS、Rape Crisis、SARC、The Survivors Trust 这些网站、热线、在线聊天和本地转介为主，而不是一个全国统一的 trauma-aware 官方 App。
所以如果你要开发 Agent，我会建议把产品定位成“创伤知情的分流与陪伴助手”，而不是“治疗 App”。也就是说，核心不是给结论，而是做：风险识别、即时稳定、知情同意、选项说明、记录整理、地区转介、陪同报警/就医准备。
你这个 Agent 该用的方法论
比较稳的结构是 5 层：
安全优先：先判断是否有即时危险、自伤/他伤风险、是否需要紧急医疗或报警。
创伤知情回应：先验证感受，不追问细节，不质疑，不替她决定。
权利与选项梳理：医疗、法医取证、是否报警、证据保存、保密边界、陪同资源，全部做成“你可以选，不必现在决定”的分支。
情境化分流：熟人侵害、亲密伴侣侵害、宗教组织内部侵害、未成年人情形，分别进入不同决策树。
转介而非替代治疗：把热线、SARC、法律援助、创伤治疗、危机干预作为下一步，而不是让 Agent 直接承担诊断或创伤处理本身。
一个很关键的设计原则是：Agent 不能像警察做笔录，也不能像治疗师做深挖。Rape Crisis 明确建议支持者不要追问细节、不要逼对方更快披露、不要接管决定；这正好可以转成 LLM 的系统约束。
复杂情境
你提到的“熟人侵犯怎么办”，NHS 明确写到多数性侵是由受害者认识的人实施的，可能是伴侣、前伴侣、亲属、朋友或同事，所以 Agent 不能默认“陌生人袭击”模型，而要内建熟人/关系权力不对等的分析框架。
对于“宗教内部事务怎么办”，这类场景通常要按“机构性侵害/权威关系/保密与报复风险”处理，而不是按普通人际冲突处理。公开权威页面虽然不会把基督教机构逐条拆解，但 GOV.UK 和 NHS 的原则都支持把它视为性暴力或虐待事件，重点是保存证据、评估当前接触风险、识别机构包庇风险，并转向独立于该宗教组织之外的专业支持渠道。
如果涉及未成年人，NHS 还特别提到要联系专业 safeguarding 路径，例如本地 MASH、社工或警方，这意味着 Agent 必须有“成年人求助”与“未成年人保护”两套完全不同的流程。
适合你做产品的边界
如果你真要做语音助手，我建议把它定义为这三件事：
“第一响应”助手：用创伤知情语言接住当事人，不造成二次伤害。
“权利导航”助手：把医疗、法律、取证、保密、陪同、热线选项讲清楚。
“记录整理”助手：帮用户在知情同意下整理时间线、人物关系、可用证据、风险点，供之后给律师、医生、SARC 或危机顾问使用；不是替代他们。
不建议把它做成：
自动判断“是否构成性侵”的裁判器。
强行推动报警的说服工具。
直接开展创伤暴露、回忆细节、EMDR 替代疗法之类的伪治疗产品。
这些都容易违背创伤知情原则，也容易带来法律和安全风险。
如果你愿意，我下一步可以直接帮你整理一份 “trauma-aware 性侵幸存者 Agent 设计框架”，包括：系统提示词、安全边界、对话状态机、熟人侵害/宗教组织场景决策树，以及中英双语资源结构。
后续提问
创伤知情原则在对话机器人中的应用指南
如何处理幸存者对熟人侵害的复杂情绪困境
性暴力幸存者数字心理支持产品的法律合规性边界
全球范围内性暴力应对的创伤知情框架有哪些
如何设计支持幸存者决策的引导性话术模板


---
Fair — rules first. Here's the strategy read, then the MVP definition, then the one-day plan with the assets you need.

## Lane decision

Go **AGENT main lane + the MiroMind 推理透明 track**. Your own reasoning is right and I'll just confirm the edges: APPLICATION is judged on UX and commercial polish you can't manufacture in a day. SKILLS is actually a *plausible* fit for your compiler idea — "a plugin that compiles deep-research output into auditable artifacts" is genuinely useful to other developers — but the deliverable bar there is packaging, docs, and integrability, and packaging is exactly what dies first under time pressure. AGENT has the loosest boundary ("scenarios yours to explore"), and your architecture already reads as a multi-agent pipeline: researcher (MiroThinker) → compiler (your layer) → verifier (audit script) → consumer (renderer). File it as an agent system; aim the substance at the sponsor track's rubric, because that rubric is the only one with concrete scoring you can engineer against.

## What 进生产 means, and therefore the MVP

Here's the answer to "what turns a web searcher into a problem solver." A searcher returns *information*. A problem solver returns **a decision someone can act on and be accountable for**. In medicine, law, policy, investing, nobody deploys an *answer* — they sign off on a *document* whose every load-bearing claim can be checked in bounded time. That's what 进生产 means: output that an accountable human can review and put their name on. The slogan's "slightly-worse answer with a traceable chain beats a right answer with a black box" follows directly — reviewability is what lets the human catch the errors, so reviewability gates production, not raw accuracy.

So the MVP is a **compiler from research output to a sign-off-able artifact**, with four parts:

1. A **decision frame** — the input is a decision question with options, not an open topic.
2. A **claims table** — the answer atomized into ≤25-word claims, each carrying status, a whitelist-only source, and an explicit 判断点 (why this claim changes the decision).
3. An **unverified ledger** — everything ungroundable, separated, never blended into claims.
4. A **machine audit** — a small script that re-checks every citation against the evidence policy (domain in whitelist, URL live, claim keyword-matches the page). This is your differentiator: "auditable" stops meaning *read our citations* and starts meaning *run this check yourself*.

This is exactly your compiler/progressive-disclosure idea, made concrete: one artifact, three disclosure levels — a single safe sentence for the affected person, the claims table for the professional who signs off, the full trace + audit report for the auditor. And "the standard professionals can at least appreciate" is the **acceptance checklist** itself: Tier-1 sources only, every time-sensitive item carries an explicit sourced window, options-not-instructions phrasing, unverified separated, machine check passes N/N. That checklist *is* the professional-grade standard, and it's derived from published protocols, not your opinion.

## What your probes actually proved

Your Probe C (the supporter brief, medium model) is near-production by that checklist already: it surfaced the 72-hour PEP window *on day 3 and flagged it as urgent-today* — a textbook 判断点 with a reference — plus the 72h-best/7-day forensic windows, no-time-limit reporting, and an honest UNVERIFIED section. That's your 60-second walkthrough material, done.

Your Probe B (the JSON one) failed for diagnosable reasons: you ran it on the **small model**, and as run it was missing the situation and the whitelist (my "[same situation as Probe B]" placeholder carries nothing in a fresh chat) — so it free-associated generic disaster content and cited Instagram and LinkedIn. Two lessons, both in your favor. First, output quality is entirely conditional on the policy layer wrapped around the API — which is direct evidence that **your middle layer is the product**, not a decoration. Second, your verifier script would have flagged that output in one second (instagram.com ∉ whitelist). Keep that failed output: it's your negative example in the demo — "here's what the raw engine does without governance; here's our auditor catching it."

## The <1 day build order

1. (~1h) Finalize the compiler prompt below on the **medium model** until JSON parses 3 runs out of 3.
2. (~2h) Verifier script: parse artifact → per claim: domain-in-whitelist, URL returns 200, optional keyword match → emit pass/fail audit report.
3. (~2h) One static HTML page rendering the artifact at three disclosure levels (tabs are fine). Skip voice and A2UI entirely — voice is your roadmap slide, not your demo; an HTML consumer satisfies "there is a consumer" at near-zero risk.
4. (~1h) Run the hero case + re-run the broken Probe B output through the verifier as the negative example.
5. (~2h) Video + 200-word intro + README containing the acceptance checklist.

Video skeleton: 0:00–0:25 the problem (stale guides and myths produce confident wrong guidance; quote the slogan). 0:25–1:25 the required 60s walkthrough: decision question → trace steps → claims with references → 判断点 (PEP 72h, forensic 7-day, no reporting time limit) → unverified ledger. 1:25–2:05 one artifact, three disclosure levels. 2:05–2:35 run the verifier live: fail the Instagram-citing output, pass the real one. 2:35–3:00 close + roadmap.

## The compiler prompt (self-contained this time)

```
You are a research compiler. You take one DECISION QUESTION and produce a sign-off-able artifact, not an essay.

EVIDENCE POLICY (strict):
- Tier 1 (citable): nhs.uk, rapecrisis.org.uk, gov.uk, cps.gov.uk, thesurvivorstrust.org
- You may read other sources but may NEVER cite them. Anything not grounded in Tier 1 goes to "unverified", never into claims.

DECISION QUESTION:
Adult woman, England. Assaulted 3 days ago by a coworker. Has showered. Undecided about police. No immediate danger. What are her live options RIGHT NOW, and which are time-critical?

CONSTRAINTS: options, never instructions ("she can choose to..."); never suggest asking for details of the assault.

OUTPUT — only valid JSON, nothing before or after:
{"decision":{"question":"...","options":[{"option":"...","time_window":"...or null","urgency":"now|days|anytime"}]},
"claims":[{"id":1,"claim":"<=25 words","status":"verified|unverified","source_url":"Tier 1 only","judgment_point":"why this changes the decision, <=15 words","surface_line":"one trauma-informed sentence <=20 words"}],
"unverified":["..."],
"trace_summary":["searched: ...","fetched: ...","compared: ..."]}
Max 8 claims.
```

## Draft 200-word intro (edit freely)

> In trauma, medical, and legal contexts, a correct answer with an unexplainable process cannot be used — while a traceable chain can be reviewed, corrected, and signed off. We built a compiler layer on the MiroMind API that turns deep research into a sign-off-able decision artifact. Given a real decision question — a survivor three days after an assault deciding her next step — MiroThinker performs multi-step research; our layer enforces an evidence policy (an NHS / Rape Crisis / GOV.UK / CPS whitelist), atomizes the answer into claims, each carrying status, source, and an explicit judgment point (the 72-hour HIV-PEP window makes "today" different from "tomorrow"), and isolates everything unverifiable into an open ledger. A verifier script then machine-checks every citation against the policy — auditability you can run, not just read. The same artifact renders by progressive disclosure: one safe sentence for the person affected, a claims table for the professional who signs off, the full trace for the auditor. Stale guides and confident myths are the real problem; a reviewable chain is what lets answers enter production.

That's the whole submission scoped to one day, with your Probe A/C outputs as ready-made demo material. If you want, I'll write the verifier script and the HTML renderer next — those are the only two pieces of real code, and both fit in this chat.

===

Let's add some info about the Miro so that you can know what's the interests and inclination of them.


"一、官方核心资源（第一手信息）
1. 官方网站与博客
官网：https://www.miromind.ai/
包含 MiroThinker-H1 的完整技术架构图（DAG 推理链、验证器设计）
最新基准测试数据和产品路线图
官方技术博客：https://miromind.ai/blog/
已发布：《MiroFlow v0.2: 开源深度研究 Agent 框架》（2025.8）
后续会更新 v1.7 的技术细节和验证机制的深入解析
2. 开源生态（全部免费可用）
表格
项目	链接	核心内容
MiroThinker 模型仓库	https://github.com/MiroMindAI/MiroThinker	v1.0/v1.5/v1.7 全版本代码、部署指南、评测脚本
MiroFlow Agent 框架	https://github.com/MiroMindAI/MiroFlow	可将任意 LLM 升级到 Deep Research 级能力，单 RTX 4090 即可运行
MiroVerse 数据集	https://huggingface.co/datasets/miromind-ai/MiroVerse-v0.1	147K + 条完整 Agent 交互轨迹，包含 SFT 和 DPO 训练数据
HuggingFace 模型页	https://huggingface.co/collections/miromind-ai/mirothinker-17	8B/30B/72B/235B 全尺寸模型权重，支持直接下载部署
3. 其他官方论文
MiroMind-M1 数学推理模型：arXiv:2507.14683v1
开源了完整的数学验证器和训练超参数，分享了大量训练 "踩坑" 经验
MiroFlow 框架论文：随 GitHub 仓库发布，详细介绍了高并发 Agent 编排和容错设计
二、第三方深度技术解读
1. 技术路线与哲学分析
《MiroMind 破局：在大语言模型的夹缝中，陈天桥在造什么？》（工控网，2026.2）
陈天桥首次系统阐述 "通用推理引擎" 定位，反对主流的 "行为主义" 和 "功能主义" 路线
提出 "逻辑长征" 概念：将算力用于 "时间序列上的反复求证" 而非一次性生成长文
《30B 参数碾压 1T 模型？MiroThinker 1.5 用 "科学家模式" 颠覆 AI 开发》（CSDN，2026.6）
深度对比 "做题家模式"（传统大模型）与 "科学家模式"（MiroMind）的本质区别
详细分析了交互式扩展如何用 1/30 的参数实现万亿级模型的性能
2. v1.7 验证机制专项解读
《当 AI 学会了验证自己的推理》（人人都是产品经理，2026.3）
拆解了局部验证 + 全局验证的具体实现方式
补充了超级碗、格莱美等更多预测案例的推理过程
《MiroThinker-1.7 & H1：验证为中心的重型推理时代》（PR Newswire 官方新闻稿，2026.3）
官方发布的最权威技术说明，包含完整的基准测试对比表
3. 工程实现细节
《MiroThinker：开源 AI 研究助手实现交互式推理突破》（CSDN，2026.5）
详细介绍了 256K 上下文管理和 600 次工具调用的工程实现
对比了 MiroThinker 与其他开源研究 Agent 的架构差异
《MiroMind 发布 M1 系列：会思考的 AI 数学天才是如何炼成的》（CSDN，2026.5）
分享了训练过程中的关键超参数（学习率 5×10^-5、3 轮训练、批次大小 128）
开源了改进的数学验证器代码
三、行业报道与最新动态
1. 重要事件报道
2026 年 5 月暂停中国区服务：
新浪财经：《突发！陈天桥旗下 MiroMind AI 暂停中国服务》
腾讯新闻：《陈天桥旗下 MiroMind 5 月 12 日起暂停大陆港澳服务》
核心原因：Manus 事件后的监管压力，已实施中美业务全面防火墙
2026 年 4 月代季峰离职事件：
钛媒体独家：《突发！代季峰与陈天桥矛盾激化，离职 MiroMind 真相曝光》
涉及股权纠纷和技术团队拆分，对 MiroMind 后续研发有一定影响
2. 社区与交流渠道
Discord 官方频道：https://discord.gg/F7EQFnYscV
有 #everything-prediction 专区，分享各类预测案例和推理过程
技术文档站：https://miromindai.github.io/MiroFlow/
包含 MiroFlow 完整的 API 文档、部署教程和最佳实践"


I have some ideas:

1. We should consider the interests of the MiroMind, because they are responsor chasing for their next goal. For example they may interested in variety form of product; but they already have the agent open sourced, even their training is based on kind of orchestration. 
On the other hand, the usage data is what they lack after consuming  existing the high quality data. We have to notice that the topic of the lane is "deep research", although I have own ideas, but the topic determine how we demo it, and how to join the data flywheel in their mindset. 

2. 

3. Based on the fact that the Miro is designed to be slow and "per-step self-review plus multi-path comparison " 
I think the use of the api should be used to maintain a surface, iterated with adversarial disturb, or new user input during the interaction. 
I notice that the official use of Miro is to "prediction" along with time-series, self-grading reasoning.

4. Even they care more about business data, I still think human situation (my survivor self help idea) is worth considering. 
Like an F1 race, an survivor can have decision windows that decay.
MiroVerse-style trajectory data covers academic/web/finance tasks; audited trajectories from human-stakes decisions are a domain their data doesn't cover, and the audit labels are what make user-generated trajectories usable at all. 

5. I don't like your 200 words intro and compiler because they looks like slob. How about we define the scope and quality first, don't pretend that you can  decide the scope of the agent or skill we are building. 
Don't blindly narrow down because the lack of time because a narrow scope could increase the demand of depth. "the compiler is packageable as a MiroFlow node / skill" is meaningless. We should make the demo happen as a full iteration.

You should focus on the hackthon context, We need to be humble. I can adapt to whatever ideas as long as we can win the competition. We should think step by step before the deciding point.


====
You're right on both counts, so let me say it plainly: the compiler I sketched was a **one-shot pipeline**, and one-shot is exactly the pattern MiroMind's thesis argues against — their whole claim is that value comes from *interaction*, not generation. And the "packageable as a MiroFlow node" line was filler. Cutting both. Here's the step-by-step derivation to the decision point, scope and quality defined before any artifact.

## Step 1 — What the sponsor's materials actually reveal they want

Reading your two documents as a single signal: their paper exists to establish **interactive scaling as the third axis** (after model size and context length), so they win when demos show *more interaction under verification → better outcomes*. Their flywheel hunger is specific: MiroVerse covers academic/web/finance trajectories, and the flywheel only keeps "effective interactions" — so what they lack is **new-domain trajectories that come pre-labeled with verification verdicts**. Their aesthetic is 慢推理、深验证 and the "逻辑长征": compute spent re-verifying a judgment over a time series, with the showcase pattern being *self-grading prediction under a changing world* (F1 lap-by-lap, gold at T+15). Their stated anti-pattern: one-shot generation and simple QA. Conclusion: a demo that merely *calls* the API once and formats the output — my compiler — uses their product but ignores their thesis.

## Step 2 — Derive the demo shape before choosing any scene

The shape that satisfies the thesis: **a maintained decision surface**. Not "answer a question," but "hold a position as the world changes" — the way an analyst maintains a rating or a race engineer maintains a strategy. The agent's job per turn is *revise and justify the diff*, gated by verification. Three classes of turn input, matching your point 3 exactly:

1. **Time decay** — windows expire; urgency must be recomputed from the clock, not restated from memory.
2. **New user input** — a new fact changes which options are live.
3. **Adversarial disturbance** — a myth or polluted source is injected; verification must quarantine it with a stated reason, never absorb it silently.

This is a miniature of their own three-axis frame, which judges from MiroMind will recognize instantly: model held constant; **context** = the surface + evidence corpus carried between calls (the stateless API makes this natural — each call sends {current surface, new input, policy} and asks for a justified diff, which is cheaper and sharper than fresh research); **interaction** = revision turns under local verification (claim gate) and global verification (does the revised surface stay consistent with its own history). And every turn emits the thing the sponsor actually lacks: a trajectory record {prior surface, input, reasoning steps, sources, verdicts, diff}. Your point 4 is the pitch line and it's the strongest sentence in this whole project, so it should be said in your words: *audited trajectories from human-stakes decisions are a domain their data doesn't cover, and the audit labels are what make user-generated trajectories usable at all.*

## Step 3 — Scene selection, scored against that shape

Requirements the shape imposes: a decision worth maintaining, **decaying windows** so time is a real variable, a whitelist-able evidence base, plausible disturbances, high value density. Scoring candidates: F1/markets fit perfectly but are *me-too* — their Discord has a whole #everything-prediction channel of these, done with their own polish; zero flywheel novelty. Legal/visa deadlines fit structurally, lower emotional risk, weaker story, no validated corpus in hand. The survivor scene, reframed as you did — **decision windows that decay** — fits every requirement: PEP expires at 72h (hourly decay, you watched the model flag "today" on day 3), forensic at ~7 days, reporting never (the contrast itself is informative), disturbances are abundant and real (the myths your Probe A corrected, a stale guide, a new fact like "the coworker texted her"), the whitelist is already validated, and it's the one domain that makes the flywheel-novelty argument true rather than decorative. So the scene survives on sponsor-derived criteria, not on attachment — and because the machinery is scene-agnostic, swapping to the legal-deadline twin costs only the corpus if your team vetoes it.

## Step 4 — Scope: cut breadth, not depth

Your scoping principle is correct and I'll state it as the rule: the time cut comes out of **breadth** (one scene, one consumer surface, no voice, no A2UI, no multi-domain) and never out of **depth** — the loop must run whole. "Full iteration" defined: **T0** intake → surface v1 (options, windows with explicit expiry timestamps, claims with sources, unverified ledger) + verification report. **T1** clock advance + one new fact → v2 with justified diff ("PEP: 14h remaining → urgency escalated; option added because…"). **T2** adversarial injection → v3 where the injected claim sits in quarantine with the rejection reason. Out of scope, explicitly: everything else.

## Step 5 — Quality bar, defined before building

Six acceptance criteria, all testable: (1) every surface claim cites the whitelist and passes the machine check; (2) every window carries expiry + source, and urgency is *recomputed from current time* — falsifiable live by changing the clock and watching urgency flip; (3) every revision states its cause and evidence — no silent changes between versions; (4) adversarial input never reaches the surface unverified — falsifiable live by injecting a myth on camera; (5) the behavioral constraints (options-not-instructions, no detail probing) hold across *all* versions, not just v1; (6) the trajectory log is complete enough to replay the whole session. Criteria 2 and 4 are your two strongest video beats, and the 60-second required walkthrough should be **one revision cycle**, not a fresh answer — a diff shows steps, references, and 判断点 more vividly than any first answer can. One practical note: MiroThinker is deliberately slow, so all runs are pre-recorded and the trace is shown sped-up.

## The decision points — yours to call

1. **Scene**: survivor-with-decaying-windows, or swap to the legal-deadline twin (same machinery, new corpus).
2. **Turn count**: the 3-turn minimum above, or add a T3 (e.g., a second window actually expiring mid-session) if rehearsal shows time allows.
3. **The adversarial input**: a corrected myth from your Probe A, the stale-2014 guide, or your failed Probe-B output as a "polluted source."
4. **Trajectory logging**: minimal JSON log, or shaped MiroVerse-like (≈1 extra hour, buys the explicit flywheel pitch in the video's closing 20 seconds).

Call these four and the build order follows from them. I'll hold off on writing anything — prompts, code, intro — until you've called them.




