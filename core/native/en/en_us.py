"""American English — reglas de naturalización.

Contracciones estándar, reducciones informales (gonna, wanna, kinda)
y expresiones coloquiales seguras.

EXPERIMENTAL: some phrases may contain errors.
"""

from ..engine import Rule, RulePriority

RULES = [
    # ── Contracciones negativas (HIGH) ─────────────────────────────────
    Rule(
        r"\bdo not\b",
        "don't",
        priority=RulePriority.HIGH,
        description="Contraction: 'do not' → 'don't'",
    ),
    Rule(
        r"\bdoes not\b",
        "doesn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'does not' → 'doesn't'",
    ),
    Rule(
        r"\bdid not\b",
        "didn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'did not' → 'didn't'",
    ),
    Rule(
        r"\bis not\b",
        "isn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'is not' → 'isn't'",
    ),
    Rule(
        r"\bare not\b",
        "aren't",
        priority=RulePriority.HIGH,
        description="Contraction: 'are not' → 'aren't'",
    ),
    Rule(
        r"\bwas not\b",
        "wasn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'was not' → 'wasn't'",
    ),
    Rule(
        r"\bwere not\b",
        "weren't",
        priority=RulePriority.HIGH,
        description="Contraction: 'were not' → 'weren't'",
    ),
    Rule(
        r"\bhave not\b",
        "haven't",
        priority=RulePriority.HIGH,
        description="Contraction: 'have not' → 'haven't'",
    ),
    Rule(
        r"\bhas not\b",
        "hasn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'has not' → 'hasn't'",
    ),
    Rule(
        r"\bhad not\b",
        "hadn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'had not' → 'hadn't'",
    ),
    Rule(
        r"\bwill not\b",
        "won't",
        priority=RulePriority.HIGH,
        description="Contraction: 'will not' → 'won't'",
    ),
    Rule(
        r"\bwould not\b",
        "wouldn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'would not' → 'wouldn't'",
    ),
    Rule(
        r"\bshould not\b",
        "shouldn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'should not' → 'shouldn't'",
    ),
    Rule(
        r"\bcould not\b",
        "couldn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'could not' → 'couldn't'",
    ),
    Rule(
        r"\bmight not\b",
        "mightn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'might not' → 'mightn't'",
    ),
    Rule(
        r"\bmust not\b",
        "mustn't",
        priority=RulePriority.HIGH,
        description="Contraction: 'must not' → 'mustn't'",
    ),
    Rule(
        r"\bcannot\b",
        "can't",
        priority=RulePriority.HIGH,
        description="Contraction: 'cannot' → 'can't'",
    ),
    Rule(
        r"\bcan not\b",
        "can't",
        priority=RulePriority.HIGH,
        description="Contraction: 'can not' → 'can't'",
    ),
    # ── Contracciones sujeto + verbo (HIGH) ────────────────────────────
    Rule(
        r"\bI am\b",
        "I'm",
        priority=RulePriority.HIGH,
        description="Contraction: 'I am' → 'I'm'",
    ),
    Rule(
        r"\byou are\b",
        "you're",
        priority=RulePriority.HIGH,
        description="Contraction: 'you are' → 'you're'",
    ),
    Rule(
        r"\bhe is\b",
        "he's",
        priority=RulePriority.HIGH,
        description="Contraction: 'he is' → 'he's'",
    ),
    Rule(
        r"\bshe is\b",
        "she's",
        priority=RulePriority.HIGH,
        description="Contraction: 'she is' → 'she's'",
    ),
    Rule(
        r"\bit is\b",
        "it's",
        priority=RulePriority.HIGH,
        description="Contraction: 'it is' → 'it's'",
    ),
    Rule(
        r"\bwe are\b",
        "we're",
        priority=RulePriority.HIGH,
        description="Contraction: 'we are' → 'we're'",
    ),
    Rule(
        r"\bthey are\b",
        "they're",
        priority=RulePriority.HIGH,
        description="Contraction: 'they are' → 'they're'",
    ),
    Rule(
        r"\bI will\b",
        "I'll",
        priority=RulePriority.HIGH,
        description="Contraction: 'I will' → 'I'll'",
    ),
    Rule(
        r"\byou will\b",
        "you'll",
        priority=RulePriority.HIGH,
        description="Contraction: 'you will' → 'you'll'",
    ),
    Rule(
        r"\bhe will\b",
        "he'll",
        priority=RulePriority.HIGH,
        description="Contraction: 'he will' → 'he'll'",
    ),
    Rule(
        r"\bshe will\b",
        "she'll",
        priority=RulePriority.HIGH,
        description="Contraction: 'she will' → 'she'll'",
    ),
    Rule(
        r"\bwe will\b",
        "we'll",
        priority=RulePriority.HIGH,
        description="Contraction: 'we will' → 'we'll'",
    ),
    Rule(
        r"\bthey will\b",
        "they'll",
        priority=RulePriority.HIGH,
        description="Contraction: 'they will' → 'they'll'",
    ),
    Rule(
        r"\bI have\b",
        "I've",
        priority=RulePriority.HIGH,
        description="Contraction: 'I have' → 'I've'",
    ),
    Rule(
        r"\byou have\b",
        "you've",
        priority=RulePriority.HIGH,
        description="Contraction: 'you have' → 'you've'",
    ),
    Rule(
        r"\bwe have\b",
        "we've",
        priority=RulePriority.HIGH,
        description="Contraction: 'we have' → 'we've'",
    ),
    Rule(
        r"\bthey have\b",
        "they've",
        priority=RulePriority.HIGH,
        description="Contraction: 'they have' → 'they've'",
    ),
    Rule(
        r"\bI would\b",
        "I'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'I would' → 'I'd'",
    ),
    Rule(
        r"\byou would\b",
        "you'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'you would' → 'you'd'",
    ),
    Rule(
        r"\bhe would\b",
        "he'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'he would' → 'he'd'",
    ),
    Rule(
        r"\bshe would\b",
        "she'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'she would' → 'she'd'",
    ),
    Rule(
        r"\bwe would\b",
        "we'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'we would' → 'we'd'",
    ),
    Rule(
        r"\bthey would\b",
        "they'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'they would' → 'they'd'",
    ),
    Rule(
        r"\bI had\b",
        "I'd",
        priority=RulePriority.HIGH,
        description="Contraction: 'I had' → 'I'd'",
    ),
    # ── Reducciones informales (MEDIUM) ────────────────────────────────
    Rule(
        r"\bgive me\b",
        "gimme",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'give me' → 'gimme'",
    ),
    Rule(
        r"\bgoing to\b",
        "gonna",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'going to' → 'gonna'",
    ),
    Rule(
        r"\bwant to\b",
        "wanna",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'want to' → 'wanna'",
    ),
    Rule(
        r"\bkind of\b",
        "kinda",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'kind of' → 'kinda'",
    ),
    Rule(
        r"\bsort of\b",
        "sorta",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'sort of' → 'sorta'",
    ),
    Rule(
        r"\blot of\b",
        "lotta",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'lot of' → 'lotta'",
    ),
    Rule(
        r"\bI do not know\b",
        "idk",
        priority=RulePriority.CRITICAL,
        match_full=True,
        description="Reduction: 'I do not know' → 'idk'",
    ),
    Rule(
        r"\bdo not know\b",
        "dunno",
        priority=RulePriority.MEDIUM,
        description="Reduction: 'do not know' → 'dunno'",
    ),
    Rule(
        r"\bbecause\b",
        "cuz",
        priority=RulePriority.LOW,
        description="Reduction: 'because' → 'cuz'",
    ),
    Rule(
        r"\bthanks\b",
        "thx",
        priority=RulePriority.LOW,
        description="Reduction: 'thanks' → 'thx'",
    ),
    Rule(
        r"\bplease\b",
        "pls",
        priority=RulePriority.LOW,
        description="Reduction: 'please' → 'pls'",
    ),
    # ── Expresiones coloquiales (MEDIUM) ───────────────────────────────
    Rule(
        r"\bwhat is up\b",
        "what's up",
        priority=RulePriority.MEDIUM,
        description="Colloquial: 'what is up' → 'what's up'",
    ),
    Rule(
        r"\byou are welcome\b",
        "no problem",
        priority=RulePriority.MEDIUM,
        description="Colloquial: 'you are welcome' → 'no problem'",
    ),
    Rule(
        r"\bsee you later\b",
        "later",
        priority=RulePriority.MEDIUM,
        description="Colloquial: 'see you later' → 'later'",
    ),
    Rule(
        r"\bgoodbye\b",
        "see ya",
        priority=RulePriority.MEDIUM,
        description="Colloquial: 'goodbye' → 'see ya'",
    ),
]
