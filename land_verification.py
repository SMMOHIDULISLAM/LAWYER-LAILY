from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlparse


@dataclass(frozen=True)
class VerificationStep:
    title: str
    purpose: str
    official_url: str
    user_evidence: tuple[str, ...]
    limitations: str


LAND_CHECKS: tuple[VerificationStep, ...] = (
    VerificationStep(
        "Mutation / নামজারি",
        "Compare the mutation case, order, khatian, dag, area, ownership chain, and responsible land office record.",
        "https://mutation.land.gov.bd/",
        ("Mutation application or case number", "Certified mutation order", "Current khatian and dag details", "Identity and deed-chain documents"),
        "A mutation entry is not by itself conclusive proof of title; verify the registered deed chain, possession, court orders, acquisition, and encumbrances.",
    ),
    VerificationStep(
        "Land development tax / দাখিলা",
        "Check whether the receipt is generated for the matching holding, khatian, mouza, dag, taxpayer, period, and amount.",
        "https://ldtax.gov.bd/",
        ("Receipt or dakhila number", "Holding number", "Tax year or period", "Khatian, mouza, dag, area, and taxpayer name"),
        "Payment evidence supports tax-payment history; it does not independently establish ownership or eliminate competing claims.",
    ),
    VerificationStep(
        "Mouza map and field measurement",
        "Locate the mouza, sheet, dag/plot, adjoining plots, scale, orientation, and recorded area before any field survey.",
        "https://map.land.gov.bd/",
        ("District, upazila, mouza, sheet number", "Dag or plot number", "Certified map copy where required", "Licensed surveyor's field measurements and boundary marks"),
        "A digital zoning/map view may be informational. Legal boundary determination requires the applicable certified record and competent survey or authority process.",
    ),
    VerificationStep(
        "Record-of-rights and settlement cross-check",
        "Compare current and historical khatians, survey type, dag changes, area, tenants, and record lineage.",
        "https://eporcha.gov.bd/",
        ("Certified khatian or porcha", "CS/SA/RS/BS or applicable survey reference", "Dag conversion or plot history", "Settlement office record and certified copies"),
        "Online availability or a downloaded image is not equivalent to a certified copy. Check seals, issuing office, record identifiers, and source retrieval date.",
    ),
)


def checklist_text(steps: Iterable[VerificationStep] = LAND_CHECKS) -> list[str]:
    return [step.title for step in steps]


def validate_land_checks(steps: Iterable[VerificationStep] = LAND_CHECKS) -> list[str]:
    """Return configuration errors without treating an online portal as title proof."""
    errors: list[str] = []
    seen_titles: set[str] = set()
    for step in steps:
        if not step.title.strip():
            errors.append("A land-check step has no title")
        if step.title in seen_titles:
            errors.append(f"Duplicate land-check title: {step.title}")
        seen_titles.add(step.title)
        parsed = urlparse(step.official_url)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{step.title} has an invalid HTTPS official URL")
        if not step.user_evidence:
            errors.append(f"{step.title} has no evidence requirements")
        if not step.limitations.strip():
            errors.append(f"{step.title} has no limitation statement")
    return errors


def red_flags() -> tuple[str, ...]:
    return (
        "Portal result has no matching official reference, case, holding, khatian, or receipt number.",
        "Names, parentage, dag, area, mouza, survey type, or dates differ across documents.",
        "Receipt is only a screenshot, edited PDF, forwarded message, or unverifiable QR/link.",
        "Mutation is relied upon without checking the registered deed chain, inheritance, possession, and litigation.",
        "Map measurement is made from an image without scale, sheet identity, field control points, or competent survey.",
        "A third party asks for credentials, OTP, unofficial payment, or access outside the government portal.",
    )
