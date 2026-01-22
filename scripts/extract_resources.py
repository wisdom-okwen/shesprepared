"""Utilities to convert new reference material into text resources for RAG."""
from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence, Tuple

try:  # Optional dependency for DOCX
    import docx2txt  # type: ignore
except ImportError:  # pragma: no cover
    docx2txt = None  # type: ignore

try:  # Optional dependency for PDF parsing
    import pdfplumber  # type: ignore
except ImportError:  # pragma: no cover
    pdfplumber = None  # type: ignore

try:  # Optional dependency for OCR of diagrams
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
except ImportError:  # pragma: no cover
    pytesseract = None  # type: ignore
    Image = None  # type: ignore

HAS_TESSERACT = bool(pytesseract and shutil.which("tesseract"))
OCR_WARNING_EMITTED = False

try:  # OpenAI client for summaries
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore

# Repository layout
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAG_ROOT = PROJECT_ROOT.parent / "shesprepared"
SOURCE_DIR = PROJECT_ROOT / "newresourcesforprepchatbot"
ADDITIONAL_SOURCE_DIR = RAG_ROOT / "utility" / "Fwd_ ShesPrEPared CB Additional Resources"
OUTPUT_DIR = RAG_ROOT / "resources" / "data"

DEFAULT_SUMMARY_MODEL = "gpt-4o-mini"
MAX_SUMMARY_WORDS = 180
DEFAULT_RESOLUTION = 200
LOW_TEXT_THRESHOLD = 120

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("extract_resources")


@dataclass(frozen=True)
class ResourceSpec:
    """Describes a single source document to process."""

    stem: str
    path: Path
    kind: str

    @property
    def output_prefix(self) -> Path:
        return OUTPUT_DIR / self.stem


class ExtractionError(RuntimeError):
    """Raised when a resource cannot be converted."""


class BaseExtractor:
    """Common functionality for concrete extractors."""

    def __init__(self, spec: ResourceSpec, resolution: int = DEFAULT_RESOLUTION) -> None:
        self.spec = spec
        self.resolution = resolution

    def run(self) -> Tuple[str, str]:
        raise NotImplementedError

    @staticmethod
    def _clean_text(parts: Iterable[str]) -> str:
        cleaned: List[str] = []
        for part in parts:
            snippet = (part or "").strip()
            if not snippet:
                continue
            cleaned.append(snippet)
        return "\n\n".join(cleaned)


class DocxExtractor(BaseExtractor):
    """Extract text content from DOCX files."""

    def run(self) -> Tuple[str, str]:
        if docx2txt is None:
            raise ExtractionError("docx2txt is required to process DOCX files. Install it first.")
        logger.info("Extracting DOCX text from %s", self.spec.path.name)
        text = docx2txt.process(str(self.spec.path))
        if text is None:
            raise ExtractionError(f"No text returned while reading {self.spec.path}")
        return text.strip(), ""


class PdfExtractor(BaseExtractor):
    """Extract narrative text and diagram text from PDF files."""

    def run(self) -> Tuple[str, str]:
        if pdfplumber is None:
            raise ExtractionError("pdfplumber is required to process PDF files. Install it first.")
        full_text: List[str] = []
        diagram_chunks: List[str] = []
        use_ocr = HAS_TESSERACT
        global OCR_WARNING_EMITTED
        if not use_ocr and (pytesseract or Image) and not OCR_WARNING_EMITTED:
            logger.warning("Tesseract binary not found; diagram OCR disabled.")
            OCR_WARNING_EMITTED = True
        try:
            with pdfplumber.open(str(self.spec.path)) as pdf:
                for index, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""
                    text = text.strip()
                    if text:
                        full_text.append(f"[Page {index}]\n{text}")
                    perform_ocr = use_ocr and ((len(text) < LOW_TEXT_THRESHOLD and (pytesseract and Image)) or page.images)
                    if perform_ocr:
                        try:
                            image = page.to_image(resolution=self.resolution).original
                        except Exception as err:  # pragma: no cover - rendering fallback
                            logger.debug("Failed to render page %s: %s", index, err)
                            continue
                        if pytesseract and Image:
                            try:
                                ocr_text = pytesseract.image_to_string(image)
                            except pytesseract.TesseractNotFoundError:
                                if not OCR_WARNING_EMITTED:
                                    logger.warning("Tesseract not found on PATH; skipping OCR for remaining pages.")
                                    OCR_WARNING_EMITTED = True
                                use_ocr = False
                                continue
                            ocr_text = ocr_text.strip()
                            if ocr_text:
                                diagram_chunks.append(f"[Page {index}]\n{ocr_text}")
        except Exception as exc:  # pragma: no cover - defensive logging
            raise ExtractionError(f"Failed to process {self.spec.path}: {exc}")
        return self._clean_text(full_text), self._clean_text(diagram_chunks)


def chunk_text(text: str, max_chars: int = 6000) -> List[str]:
    """Split text into manageable pieces for summarisation."""
    if not text:
        return []
    chunks: List[str] = []
    pointer = 0
    while pointer < len(text):
        chunk = text[pointer : pointer + max_chars]
        chunks.append(chunk.strip())
        pointer += max_chars
    return [c for c in chunks if c]


def _filter_lines(lines: List[str]) -> List[str]:
    stripped = [line.strip() for line in lines]
    counts = Counter(s for s in stripped if s)
    repeated = {s for s, count in counts.items() if count >= 3 and len(s.split()) <= 12}
    filtered: List[str] = []
    for original, clean in zip(lines, stripped):
        if not clean:
            filtered.append("")
            continue
        if clean in repeated:
            continue
        if re.fullmatch(r"[ivxlcdm]+", clean.lower()):
            continue
        filtered.append(clean)
    return filtered


def _is_list_block(block_lines: List[str]) -> bool:
    return all(
        line.startswith(("•", "-")) or re.match(r"^\d+[\.)]", line)
        for line in block_lines
    )


def _normalize_block(block: str) -> str:
    lines = [ln for ln in block.splitlines() if ln.strip()]
    if not lines:
        return ""
    lines = _filter_lines(lines)
    lines = [ln for ln in lines if ln.strip()]
    if not lines:
        return ""
    if _is_list_block(lines):
        return "\n".join(line.strip() for line in lines)
    merged: List[str] = []
    idx = 0
    length = len(lines)
    while idx < length:
        line = lines[idx].strip()
        if line.endswith("-") and idx + 1 < length:
            next_line = lines[idx + 1].strip()
            merged.append(f"{line[:-1]}{next_line}")
            idx += 2
            continue
        merged.append(line)
        idx += 1
    joined = " ".join(merged)
    joined = re.sub(r"\s+", " ", joined)
    return joined.strip()


def clean_narrative_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r", "")
    text = re.sub(r"\[Page\s+\d+\]\s*", "", text)
    lines = text.splitlines()
    lines = _filter_lines(lines)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    blocks = [block for block in text.split("\n\n") if block.strip()]
    normalized = [_normalize_block(block) for block in blocks]
    normalized = [block for block in normalized if block]
    return "\n\n".join(normalized).strip()


def clean_diagram_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r", "")
    text = re.sub(r"\[Page\s+\d+\]\s*", "", text)
    lines = text.splitlines()
    lines = _filter_lines(lines)
    text = "\n".join(line for line in lines if line.strip())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def summarise(text: str, client: Optional[Any], model: str = DEFAULT_SUMMARY_MODEL) -> str:
    """Create a concise summary via OpenAI."""
    if not text:
        return ""
    if client is None:
        logger.warning("OpenAI client unavailable; skipping summary.")
        return ""
    prompt = (
        "Summarize the following reference material so it fits under "
        f"{MAX_SUMMARY_WORDS} words. Highlight key findings, clinical guidance, "
        "and safety considerations. Use plain sentences, no bullet points."
    )
    chunks = chunk_text(text)
    summaries: List[str] = []
    for chunk in chunks:
        messages = [
            {"role": "system", "content": "You produce concise summaries for HIV prevention resources."},
            {"role": "user", "content": f"{prompt}\n\n{chunk}"},
        ]
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=400,
            )
            summary = response.choices[0].message.content.strip()
            if summary:
                summaries.append(summary)
        except Exception as exc:  # pragma: no cover - API failure fallback
            logger.warning("OpenAI summarisation failed: %s", exc)
            break
    return "\n\n".join(summaries).strip()


def write_output(prefix: Path, full_text: str, diagrams: str, summary: str) -> None:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    (prefix.with_name(f"{prefix.name}_full.txt")).write_text(full_text, encoding="utf-8")
    if diagrams:
        (prefix.with_name(f"{prefix.name}_diagrams.txt")).write_text(diagrams, encoding="utf-8")
    if summary:
        (prefix.with_name(f"{prefix.name}_summary.txt")).write_text(summary, encoding="utf-8")


def get_resources(selected: Optional[Sequence[str]] = None) -> List[ResourceSpec]:
    resources = [
        ResourceSpec(stem="10125_LENsources", path=SOURCE_DIR / "10125_LENsources.docx", kind="docx"),
        ResourceSpec(stem="Bekker_2024", path=SOURCE_DIR / "Bekker_2024.pdf", kind="pdf"),
        ResourceSpec(stem="Patel_2025_CDC", path=SOURCE_DIR / "Patel_2025_CDC.pdf", kind="pdf"),
        ResourceSpec(stem="PrEPWatchPage", path=SOURCE_DIR / "PrEPWatchPage.pdf", kind="pdf"),
        ResourceSpec(stem="WHOguidelines", path=SOURCE_DIR / "WHOguidelines.pdf", kind="pdf"),
        ResourceSpec(stem="gilead_sept", path=SOURCE_DIR / "gilead_sept.pdf", kind="pdf"),
        ResourceSpec(stem="prepwatch_112125", path=ADDITIONAL_SOURCE_DIR / "prepwatch_112125.docx", kind="docx"),
        ResourceSpec(stem="yeztugo_patient_pi", path=ADDITIONAL_SOURCE_DIR / "yeztugo_patient_pi.pdf", kind="pdf"),
        ResourceSpec(stem="yeztugo_safetyinfo", path=ADDITIONAL_SOURCE_DIR / "yeztugo_safetyinfo.pdf", kind="pdf"),
    ]
    if selected:
        selected_set = {stem.lower() for stem in selected}
        resources = [res for res in resources if res.stem.lower() in selected_set]
    missing = [str(res.path) for res in resources if not res.path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing source files: {missing}")
    return resources


def build_extractor(spec: ResourceSpec) -> BaseExtractor:
    if spec.kind == "docx":
        return DocxExtractor(spec)
    if spec.kind == "pdf":
        return PdfExtractor(spec)
    raise ValueError(f"Unsupported resource type: {spec.kind}")


def init_openai(disable_summary: bool) -> Optional[Any]:
    if disable_summary:
        return None
    if OpenAI is None:
        logger.warning("openai package not available; summaries disabled.")
        return None
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set; summaries disabled.")
        return None
    return OpenAI(api_key=api_key)


def process_resources(stems: Optional[Sequence[str]], disable_summary: bool) -> None:
    client = init_openai(disable_summary)
    for spec in get_resources(stems):
        logger.info("Processing %s", spec.path.name)
        extractor = build_extractor(spec)
        full_text, diagram_text = extractor.run()
        full_text = clean_narrative_text(full_text)
        diagram_text = clean_diagram_text(diagram_text)
        summary = summarise(full_text, client) if full_text else ""
        write_output(spec.output_prefix, full_text, diagram_text, summary)
        logger.info("Finished %s", spec.stem)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract reference material for RAG ingestion.")
    parser.add_argument(
        "stems",
        nargs="*",
        help="Optional list of resource stems to process (default: all).",
    )
    parser.add_argument(
        "--disable-summary",
        action="store_true",
        help="Skip OpenAI summarisation stage.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    process_resources(args.stems, args.disable_summary)


if __name__ == "__main__":
    main()
