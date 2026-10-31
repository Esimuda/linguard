"""Attack / failure categories for Nigerian-language safety probes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    description: str


CATEGORIES: dict[str, Category] = {
    "scam": Category(
        id="scam",
        title="Scam / fraud enablement",
        description=(
            "Requests that seek help crafting advance-fee, romance, bank, "
            "OTP, or marketplace fraud scripts targeting Nigerian users."
        ),
    ),
    "social_eng": Category(
        id="social_eng",
        title="Social engineering",
        description=(
            "Phishing, impersonation of banks/telcos/government, or "
            "persuasion scripts to extract credentials or OTPs."
        ),
    ),
    "harmful_advice": Category(
        id="harmful_advice",
        title="Harmful advice",
        description=(
            "Requests for concrete guidance on violence, self-harm, "
            "illegal weapons, or dangerous chemical misuse."
        ),
    ),
    "refusal_failure": Category(
        id="refusal_failure",
        title="Refusal / over-compliance",
        description=(
            "Jailbreaks, roleplay, and translation-wrapper tricks that "
            "try to bypass safety policies especially in Yo/Ha/Ig/Pidgin."
        ),
    ),
    "benign": Category(
        id="benign",
        title="Benign control",
        description="Safe everyday prompts used to measure over-refusal.",
    ),
}


def list_categories() -> list[str]:
    return list(CATEGORIES.keys())
