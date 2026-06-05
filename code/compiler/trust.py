"""
trust.py — measures, in plain terms, whether the human stayed in charge.

For each decision in the conversation we log a few simple things and count them up.
No jargon: the output uses plain English keys. The whole idea in one sentence:

    A good collaborator OVERRIDES the AI when the AI is wrong, and RELIES on the AI
    when the AI is right. We just count how often each happened.

What we log per decision:
  - did the human change their position after seeing the AI's view?  (switched)
  - did the human end up agreeing with the AI?                       (agreed)
  - did the human actually look at the reasoning before deciding?    (checked)
  - once we know the real answer, was the AI right or wrong?         (ai_correct)

"Don't know yet" is allowed: when there is no confirmed right answer in the
conversation, that decision is counted as "no confirmed answer yet" instead of
being scored — we never pretend to know.
"""

def summarize(decisions):
    n = len(decisions)
    switched = sum(1 for d in decisions if d.get("switched"))
    agreed   = sum(1 for d in decisions if d.get("agreed"))
    checked  = sum(1 for d in decisions if d.get("rationale_expanded"))
    agreed_without_checking = sum(1 for d in decisions
                                  if d.get("agreed") and not d.get("rationale_expanded"))
    known = [d for d in decisions if d.get("ai_correct") is not None]
    relied_and_ai_was_right = sum(1 for d in known if d.get("ai_correct") and d.get("agreed"))
    overrode_and_ai_was_wrong = sum(1 for d in known
                                    if (d.get("ai_correct") is False) and (not d.get("agreed")))
    return {
        "decisions_logged": n,
        "times_human_changed_position_after_seeing_ai": switched,
        "times_human_agreed_with_ai": agreed,
        "times_human_looked_at_the_reasoning": checked,
        "times_human_agreed_without_looking": agreed_without_checking,
        "good_catches__overrode_ai_when_ai_was_wrong": overrode_and_ai_was_wrong,
        "good_trust__relied_on_ai_when_ai_was_right": relied_and_ai_was_right,
        "decisions_with_no_confirmed_answer_yet": n - len(known),
        "plain_reading": ("A healthy collaboration: the human overrides the AI when it's "
                          "wrong and relies on it when it's right. We only score a decision "
                          "once the real answer is known; otherwise we say 'no confirmed answer yet'."),
    }
