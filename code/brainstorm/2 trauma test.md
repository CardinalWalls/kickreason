

Probe A — the stale-guide audit (tests authority policy controllability; also is the product mechanic):
You are a verification engine for post-sexual-assault guidance in England & Wales.

AUTHORITY POLICY (strict):
- Tier 1 evidence sources: nhs.uk, rapecrisis.org.uk, gov.uk, cps.gov.uk, thesurvivorstrust.org
- You may read other sources but may NOT cite them as evidence.
- Every claim must end with [Tier 1 URL]. If Tier 1 sources don't settle a point, write UNVERIFIED — do not answer from other sites or memory.

DOCUMENT A (from a support guide published ~2014):
"Victims should report to police within days, as delay weakens any case. A forensic exam requires that the victim has not washed. Victim Support is the national service to contact."

TASK: Audit Document A against current Tier 1 sources. Output a table: Claim | Verdict (current/outdated/false) | What is true now | [URL]. Then list UNVERIFIED items. Max 300 words total.
Watch for: does it obey the whitelist or leak other domains; does it fabricate URLs; does the 300-word cap hold (your length complaint, tested directly).
Probe B — the supporter brief (tests the pivoted product + trauma-informed constraints):
ROLE: You write briefs for the SUPPORTER (friend/family) of a sexual assault survivor — never for the survivor directly.

SITUATION: Adult woman, England. Assaulted 3 days ago by a coworker. Has told only this one friend. Has showered. Undecided about police. No immediate danger.

CONSTRAINTS (from Rape Crisis supporter guidance): never suggest asking for details of the assault; present options, never decisions ("she can choose to..."); flag anything time-sensitive with an explicit window.

DELIVER, max one page:
1. SAY / DON'T SAY — 5 short lines each.
2. OPTIONS MAP — medical care, SARC/forensic, evidence preservation, reporting routes — one line each + [source URL] + time window if any.
3. ESCALATE IF — signs needing professional help, with the right contact.
4. UNVERIFIED — anything not groundable in nhs.uk / rapecrisis.org.uk / gov.uk / cps.gov.uk.
Watch for: whether the constraints hold under pressure, whether SARC/forensic time windows are correct and sourced, whether it stays one page.
Probe C — machine-readable two-layer output (tests buildability, since response_format isn't supported):
[Same situation as Probe B.]
Output ONLY valid JSON, nothing before or after:
{"cards":[{"id":1,"claim":"...","status":"verified|unverified","source_url":"...","time_window":"... or null","say_to_survivor":"one trauma-informed sentence, max 20 words"}],"escalation":{"needed":false,"reason":"...","contact":"..."},"trace_summary":["searched: ...","fetched: ...","compared: ..."]}
Max 10 cards.
Watch for: parseable JSON on the first try, and whether say_to_survivor gives you the short safe surface layer — that field is your survivor-facing product, distilled from the long trace you rightly said no survivor should read. Then rerun your original Probe 2 myths through Probe A's policy and score it: that's your benchmark.
If the team vetoes the vertical, the identical engine + prompts work with a swapped corpus — "my landlord/boss says X" rights-myth verification on GOV.UK/Citizens Advice is the lowest-risk twin. But run these three probes first; the results will tell you whether the supporter-brief shape holds, and I can help you turn whichever probe behaves best into the system prompt and demo script.

the probe result:
Probe A, I notice it runs really long time(medium): "| Claim from Document A | Verdict (current / outdated / false) | What is true now | [URL] |
| --- | --- | --- | --- |
| Victims should report to police within days, as delay weakens any case. | Outdated | There is **no time limit** for reporting sexual offences under the Sexual Offences Act 2003. You can report even if it happened long ago; your account is still evidence. Timing mainly affects the availability of forensic evidence, not whether the police can investigate or CPS can prosecute. [https://rapecrisis.org.uk/get-help/reporting-to-the-police/](https://rapecrisis.org.uk/get-help/reporting-to-the-police/) |
| A forensic exam requires that the victim has not washed. | Outdated | You are **advised** to try not to wash or change clothes immediately after an assault to help preserve forensic evidence, but you can still go to the police and seek help even if you have washed. Forensic examinations and medical support remain available; washing is not an absolute requirement bar. [https://www.nhs.uk/live-well/sexual-health/help-after-rape-and-sexual-assault/](https://www.nhs.uk/live-well/sexual-health/help-after-rape-and-sexual-assault/) |
| Victim Support is the national service to contact. | Outdated | Victim Support is an **independent national charity** supporting victims of crime in England & Wales, but it is not *the* single national service. There is also a government‑funded, national 24/7 Rape and Sexual Abuse Support Line led by Rape Crisis England & Wales, and other specialist national bodies and local services. [https://www.victimsupport.org.uk/](https://www.victimsupport.org.uk/) |

UNVERIFIED items: None. All claims in Document A are addressed and corrected by current Tier 1 sources."

Probe B(small): "{"cards":[{"id":1,"claim":"Survivors need clear, compassionate information after disasters to feel safer and less alone","status":"verified","source_url":"https://www.womenspress.com/talk-do-steps-to-get-from-crisis-response-to-community-healing/","time_window":"2026-05-12/2026-06-04","say_to_survivor":"You deserve clear information, at your own pace, with space for every feeling you’re having"},{"id":2,"claim":"Treating trauma as a short-term issue can harm survivors’ long-term recovery","status":"verified","source_url":"https://www.womenspress.com/talk-do-steps-to-get-from-crisis-response-to-community-healing/","time_window":"2026-05-12/2026-06-04","say_to_survivor":"What you’re feeling may last a while, and ongoing support is completely appropriate"},{"id":3,"claim":"Trauma-informed care focuses on asking “What happened to you?” instead of “What’s wrong with you?”","status":"verified","source_url":"https://reachlink.com/advice/trauma/trauma-informed-care/","time_window":"2026-05-20/2026-06-04","say_to_survivor":"Nothing about your reactions means you are broken; they make sense given what you’ve survived"},{"id":4,"claim":"Normalizing emotional reactions after disaster helps survivors feel less ashamed or isolated","status":"verified","source_url":"https://www.instagram.com/p/DYZI97RjGra/","time_window":"2026-05-16/2026-06-04","say_to_survivor":"Strong reactions after something this big are normal; there is nothing wrong with how you’re coping"},{"id":5,"claim":"Building on survivors’ existing strengths supports resilience and recovery","status":"verified","source_url":"https://www.instagram.com/p/DYZI97RjGra/","time_window":"2026-05-16/2026-06-04","say_to_survivor":"The strengths that got you through this far are still with you, even if they feel distant"},{"id":6,"claim":"After major incidents, coordinated messaging and internal communication improve response and support for affected communities","status":"verified","source_url":"https://www.linkedin.com/posts/joseph-wiltberger-08b02316a_really-glad-to-see-this-work-shared-at-the-activity-7465816701461282816-rQOE","time_window":"2026-05-29/2026-06-04","say_to_survivor":"Different teams are working together behind the scenes to better support your safety and recovery"},{"id":7,"claim":"Disaster Medical Assistance Teams can provide both medical care and trauma-informed emotional support after a disaster","status":"verified","source_url":"https://dev-housing.rice.edu/tutorials/how-the-disaster-medical-assistance-team-becomes-your-hope-after-a-disaster-7836861","time_window":"2026-05-14/2026-06-04","say_to_survivor":"Responders are here not just for your physical needs, but also to listen and support emotionally"},{"id":8,"claim":"Many survivors experience ongoing stress reactions even after immediate danger has passed","status":"verified","source_url":"https://www.facebook.com/firstrespondercenter/posts/we-wrapped-up-day-2-of-the-2026-mental-wellness-symposium-with-two-powerful-pres/1444974867668715/","time_window":"2026-06-03/2026-06-04","say_to_survivor":"Feeling on edge now that things are “over” is common; your nervous system needs time to settle"},{"id":9,"claim":"Trauma-informed community spaces and practices can make it easier for survivors to seek help","status":"verified","source_url":"https://www.womenspress.com/talk-do-steps-to-get-from-crisis-response-to-community-healing/","time_window":"2026-05-12/2026-06-04","say_to_survivor":"You deserve spaces where you’re believed, respected, and never pressured to share more than you want"},{"id":10,"claim":"Specialized training helps responders offer more trauma-informed, emotionally aware disaster support","status":"verified","source_url":"https://web.cvent.com/event/7e357e8d-ec87-4041-b517-834681dd293e/websitePage:081652c2-3817-4584-ab5f-de329e8e621d","time_window":"2026-05-21/2026-06-04","say_to_survivor":"People supporting you are increasingly trained to understand trauma and respond with care"}],"escalation":{"needed":false,"reason":"Current information concerns generalized post-disaster trauma support; no specific, imminent safety threats or individual crises identified","contact":"If you feel in danger or overwhelmed, contact local emergency services or a crisis line immediately"},"trace_summary":["searched: recent disaster response survivor support 2026 trauma informed messages","fetched: trauma-informed disaster and community healing resources from reputable organizations and events in 2026","compared: consistent themes on normalization, resilience, coordinated response, and survivor-centered communication across multiple sources"]}"

Probe C(medium): "### 1. SAY / DON’T SAY  

**SAY (to her):**  
- “I believe you, and none of this is your fault.”【16】  
- “You can choose what, if anything, you want to do next — I’ll back you.”【16】  
- “You don’t have to tell me any more than you want to.”【16】  
- “There are services like SARCs and Rape Crisis if you’d like to talk to someone confidentially.”【13】【3】  
- “If at any point you want medical advice or to think about reporting, we can look at options together.”【1】【13】  

**DON’T SAY (to her):**  
- “Why didn’t you tell anyone sooner?”【16】  
- “Why didn’t you fight back or run away?”【16】【15】  
- “Are you sure it was really rape/assault?”【16】  
- “You should report / not report to the police.”【13】  
- “I’m going to tell X about this so they can help,” without her clear consent (unless there is immediate danger).【16】  

---

### 2. OPTIONS MAP (you can name these and let *her* choose)

All of these are options, not instructions. You can offer to sit with her, look things up, or make a call *only if she wants you to*.

**Medical care (physical & sexual health)**  
- She can choose to contact a **Sexual Assault Referral Centre (SARC)** or NHS services for checks on injuries, STIs, pregnancy, and other health concerns. SARCs offer medical, practical and emotional support and can be accessed without going to the police【1】【3】.  
  - Info: NHS SARC finder – <https://www.nhs.uk/service-search/sexual-health-services/find-a-rape-and-sexual-assault-referral-centre/>【11】  
  - General NHS info: <https://www.nhs.uk/live-well/sexual-health/help-after-rape-and-sexual-assault/>【1】  
  - **Time‑sensitive:**  
    - **HIV PEP (post‑exposure prophylaxis)** — usually only offered up to **72 hours (3 days) after possible exposure**【26】. She is around this window now; if she wants to consider PEP, it’s urgent to seek medical advice *today*.  
    - **Emergency contraception** — some methods can be used up to **5 days after sex** (for example copper IUD)【30】; exact option depends on clinical assessment.

**SARC / forensic examination**  
- She can choose to attend a **SARC** for a forensic medical examination to collect evidence. She can do this **with or without talking to the police first**, and evidence can be stored if she prefers to decide about reporting later【13】【3】.  
  - Rape Crisis SARC info: <https://rapecrisis.org.uk/get-help/sexual-assault-referral-centres-sarcs/>【15】  
  - Rape Crisis “It happened recently”: <https://rapecrisis.org.uk/get-help/it-happened-recently/>【13】  
  - **Time‑sensitive:**  
    - Rape Crisis notes the **best chance of evidence being collected is in the first 72 hours (3 days)**【27】.  
    - However, their “It happened recently” page says **forensic evidence may still be available up to 7 days** after the assault【24】. She is on day 3, so still within both the “best chance” 72‑hour window and the broader 7‑day window.

**Evidence preservation (now that she has already showered)**  
- She can still choose to go to a SARC; **showering doesn’t rule out all evidence** and SARCs can also store clothing or other items if appropriate【13】【15】.  
- Even if she is unsure about police, she can choose a forensic exam with samples stored for possible future reporting【24】.  
  - Rape Crisis – self‑swab kits (to avoid): <https://rapecrisis.org.uk/news/our-position-on-self-swab-rape-kits/>【25】 explains why home “rape kits” are not recommended when compared with proper SARC exams.  
  - **Time‑sensitive:** forensic sampling can still be considered **up to 7 days** after the assault【24】.

**Reporting routes (if she ever wants to report)**  
- She can choose to:  
  - **Report to police directly**: call **101** (or **999** if she is in danger or there is an emergency)【23】【22】, or attend a police station in person【14】.  
  - **Go via a SARC**: attend a SARC first; they can help her think through options, store evidence and, if she chooses later, support a police report【24】【14】.  
  - **Get advocacy support first**: She can contact a local **Rape Crisis centre** or an **Independent Sexual Violence Adviser (ISVA)** to talk through what reporting might be like and get support whether she reports or not【14】【32】.  
- Key points from Rape Crisis on reporting【14】:  
  - It is **her choice** whether or not to report; she should not be pressured.  
  - There are **no time limits** in England and Wales for reporting offences like rape and sexual assault【24】, though earlier reporting can make some aspects of evidence and investigation easier.  
- Info:  
  - Reporting to the police (Rape Crisis): <https://rapecrisis.org.uk/get-help/reporting-to-the-police/>【14】  
  - CPS RASSO support overview: <https://www.cps.gov.uk/rasso-guide/what-support-available-help-you-0>【32】  

---

### 3. ESCALATE IF (when to involve professionals, and who)

As her supporter, you’re not expected to “fix” this. Your role is to notice when extra support is needed and help her reach it *if she wants to* (unless there is immediate risk).

**Emergency – act even if she isn’t asking you to**  
- **If she is in immediate physical danger** (e.g. the coworker is trying to contact or harm her, or you believe she is at serious risk):  
  - Call **999** (police)【22】【32】.  
- **If she is at immediate risk of seriously harming herself or someone else**:  
  - Call **999** or **111** (or local mental health crisis services via NHS) and say you’re worried about suicide/self‑harm after a sexual assault【1】.

**Urgent but not 999**  
- **Within 72 hours of the assault** (where she might want HIV PEP or emergency contraception) and she is unsure:  
  - Encourage her to **speak to a SARC, GP, or NHS 111 today**, and offer to help her call or look up numbers if she wants you to【13】【26】. (Name this as a time‑limited medical option, not a demand.)  
- **Marked changes in mental health** (e.g. can’t sleep at all, constant panic, intrusive flashbacks, overwhelming distress, talking about feeling “numb” or “not wanting to be here”) that persist or worsen:  
  - She can choose to contact her **GP** or NHS mental health services; you can suggest she also consider Rape Crisis counselling or support groups【16】【2】.  
  - Rape Crisis helpline: **24/7 Rape & Sexual Abuse Support Line 0808 500 2222** (England & Wales)【21】【34】.

**Specialist support / advocacy**  
- If she is thinking about reporting or already has contact with police, you can suggest she consider asking for an **ISVA** (Independent Sexual Violence Adviser) for ongoing advocacy and support【32】.  
  - Rape Crisis ISVA info: <https://rapecrisis.org.uk/get-help/support-and-services/advocacy-isvas/>【29】.  

---

### 4. UNVERIFIED (outside nhs.uk / rapecrisis.org.uk / gov.uk / cps.gov.uk)

The following points are **not** directly grounded in the specified sources and should be treated as general/common practice rather than confirmed guidance:

- Any detailed instructions about **how to deal with her employer or HR** beyond acknowledging that the perpetrator is a coworker. While UK law requires employers to take reasonable steps to prevent sexual harassment at work【41】【45】, specific steps for *her* to take with HR are not set out in the cited health/justice sources.  
- Exact **forensic time‑windows broken down by body site** (e.g. “oral evidence up to X hours, vaginal up to Y days”): different clinical leaflets and local SARC guidance vary; the only grounded figures here are: “best chance… in the first 72 hours” and “forensic evidence may be available up to 7 days” from Rape Crisis【27】【24】.  
- Any assumptions about **waiting times for counselling/ISVA services**; the CPS and Rape Crisis materials confirm that these services exist but do not give specific waiting‑time figures【32】【36】.  

You can safely lean on: NHS pages about sexual assault, Rape Crisis England & Wales, gov.uk guidance, and CPS RASSO materials for anything medical, forensic, reporting‑related or about specialist support.

---

### References

[1] Help after rape and sexual assault. <https://www.nhs.uk/live-well/sexual-health/help-after-rape-and-sexual-assault/>.  
[2] Impacts of sexual violence and abuse. <https://rapecrisis.org.uk/get-informed/about-sexual-violence/impacts-of-sexual-violence-and-abuse/>.  
[3] It happened recently. <https://rapecrisis.org.uk/get-help/it-happened-recently/>.  
[11] Find a rape and sexual assault referral centre. <https://www.nhs.uk/service-search/sexual-health-services/find-a-rape-and-sexual-assault-referral-centre/>.  
[13] It happened recently – sections on medical care, SARCs, evidence. <https://rapecrisis.org.uk/get-help/it-happened-recently/>.  
[14] Reporting to the police. <https://rapecrisis.org.uk/get-help/reporting-to-the-police/>.  
[15] SARCs – Sexual Assault Referral Centres. <https://rapecrisis.org.uk/get-help/sexual-assault-referral-centres-sarcs/>.  
[16] Supporting a survivor. <https://rapecrisis.org.uk/get-help/supporting-a-survivor/>.  
[21] Want to talk? (24/7 Support Line). <https://rapecrisis.org.uk/get-help/want-to-talk/>.  
[22] Reporting to the police – contact 101/999. <https://rapecrisis.org.uk/get-help/reporting-to-the-police/>.  
[23] Report rape, sexual assault and other sexual offences – Police.uk. <https://www.police.uk/ro/report/rsa/alpha-v1/v1/rape-sexual-assault-other-sexual-offences/>.  
[24] Reporting to the police – time limits and SARC use. <https://rapecrisis.org.uk/get-help/reporting-to-the-police/>.  
[25] Our position on self-swab ‘rape kits’. <https://rapecrisis.org.uk/news/our-position-on-self-swab-rape-kits/>.  
[26] HIV and AIDS – PEP and 72-hour window. <https://www.nhs.uk/conditions/hiv-and-aids/>.  
[27] SARCs – 72-hour best evidence statement. <https://rapecrisis.org.uk/get-help/sexual-assault-referral-centres-sarcs/>.  
[29] ISVAs – advocacy and support. <https://rapecrisis.org.uk/get-help/support-and-services/advocacy-isvas/>.  
[30] Timescales for medical care – Devon & Cornwall SARC. <https://sarchelp.co.uk/medical-staff/timescales-forensic-examination/>.  
[32] What support is available to help you – CPS RASSO guide. <https://www.cps.gov.uk/rasso-guide/what-support-available-help-you-0>.  
[34] 24/7 Rape and Sexual Abuse Support Line. <https://247sexualabusesupport.org.uk/>.  
[36] Rape Crisis England & Wales – written evidence on waiting times (context). <https://committees.parliament.uk/writtenevidence/140110/html/>.  
[41] Sexual harassment and harassment at work: technical guidance. <https://www.equalityhumanrights.com/guidance/sexual-harassment-and-harassment-work-technical-guidance>.  
[45] New protections from sexual harassment come into force. <https://www.gov.uk/government/news/new-protections-from-sexual-harassment-come-into-force>."

Don't take my ideas too serious, because it won't work during the 2 days without evidence. "I now think about make a little abstraction above the survivor case. 

The trust between ai and human needs interaction and metric, that I have read academic papers, that use the prediction data set(application\crime, etc) to do experiment. More recently is the A2UI benchmark. 
I think what I could do is a layer between the Miromind api and the user, with stage of progressive disclosure, which is the philosophy of skill. 
So am I doing a skill? No, I'm afraid its the skill that turns content into skills. 
And there will be a consumer, that is my audio agent, or the A2UI, or even a html(like skill2app). Personally I prefer audio agent, because it can give more constraints so that give the middle layer skill more data.
"

It could indeed a compiler. We are not have to do the rape crisis, nor A2UI, nor voice agent. 
We have to find a strategy to have a demo and a story to pass the hackthon submit. 

--
I am not interestied by your advice. 

We need come back to the hackthon rules in the first place. 

It have three lanes: 1 "AGENT system capable of autonomous learning and collaboration. The application scenarios are yours to explore, athe boundaries are yours to define."

This could suit me because it's more flexible.







"Skills. Build modular, reuseable skill plugins that developers around the world can intergrate into their own projects." I don't think our so called compiler will be helpful for developers around the world. I have my own interests, but if my idea must solve the skill problem, then we have to hand over the skill instead. 



"APPLICATION. The most open-ended track - software, hardware, or hybrid projects are all welcome. If your product solves real problems, strong user experience and commercial potential will be your greates advantage." I will doubt I can win in this lane. I don't have time to prove my value, nor compete with those proffesionals.



Addition lane MiroMind Deep Research. It have a specific theme focusing on "Deep Research + 推理透明". It's not like the 3 main to make something adorable, but to make a understanding\trust worthy 推理过程. 推理判断、投研结论、法律建议、政策分析，这些场景里，“对的答案+不可解释的过程” 基本不能用；“差一点的答案+完整可追溯的推理链” 反而能进生产。 Miromind 不是在做更聪明的 AI，而是在做让 AI 思考过程变得可见。 它将原本黑盒的推理过程拆解为清晰的链路，每一步判断都有依据，可以被追踪与验证。把 AI 的推理过程从黑盒变成可审视、可追踪、可被引用的链条。



The Miromind's Open application is what I choose to make the 推理透明 as the core ability, that must solve problem that need multi-step reasoning and decision explaining, not simply generate result.

It have to satisfy:





use MiroMind API;



show muti-step reasoning;



provide evidence or data source;



output need to explainable and auditable;

Three score metric:





Use case: if solve real and valuable scene 



design & tech bility



Demo is clear with the idea

To hand over:





200 words intro;



a video demo(important <= 3min, use 60s for a reasoning walkthrough for a real problem, giving steps\references\judgepoint);



a runable demo;



My notions:





only less than 1 day;



I wonder what's the mvp to make the Miromind api from a web searcher to a problem solver. The most important in "“对的答案+不可解释的过程” 基本不能用；“差一点的答案+完整可追溯的推理链” 反而能进生产。" is what is "进生产"。If i'm going to do the trauma-informed self-help agent or app, it have to find a standard that actually have some professionals can at least appreciate. It indeed relate to all part of medical\law\policy, etc, but more because of complex context.



I still havn't decide which one in the 3 main lane, that will decide our work focus.