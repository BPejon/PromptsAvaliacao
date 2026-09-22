import json
import os
import re
from datetime import datetime
from pathlib import Path

from openai import OpenAI

from chamadas2 import (
    ARTIGO,
    create_deepseek_client,
    review_article,
)


OUTPUT_DIR = Path(__file__).resolve().parent
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
NUMBER_OF_REVIEWS = 3
RESULT_FOLDER_PATTERN = re.compile(r"^results_(\d{6})_(\d{2}:\d{2})$")

UNIFICATION_SYSTEM_PROMPT = """
You are a senior academic editor responsible for consolidating independent reviews of the same technical paper. You will receive three reviews produced using the same review prompt.

Produce a single final review that is rigorous and self-contained:

Internal procedure, to be used only for reasoning and not included in the output:
1. Extract the exact evaluation dimensions used across the three reviews. If dimensions are synonymous or overlapping, unify them under the clearest dimension name. Preserve all original dimensions that are distinct.
2. For each dimension, build an evidence map:
   - reviewer score(s);
   - specific comments;
   - supporting or contradicting evidence from the article;
   - whether the comment is pertinent, redundant, or contradicted by the paper.
3. Compare the three reviews dimension by dimension.
4. Do not mechanically average scores. Choose the integer score from 1 to 5 best justified by the body of evidence.
5. Merge all relevant comments and details. If a detail appears in only one review, include it when it is pertinent and not contradicted.
6. Resolve disagreements through balanced synthesis.
7. Do not invent facts, references, problems, sections, tables, or limitations. Remove repetition without removing useful specific details.
8. Write in English.

Output format:
First, include one JSON block with the final scores:
{
  "scores": {
    "<dimension_1>": <integer 1-5>,
    "<dimension_2>": <integer 1-5>,
    "<dimension_3>": <integer 1-5>
  }
}

Then provide the final review organized by dimension. For each dimension, use this structure:

## <Dimension>
Score: <integer 1-5>/5
Justification: <evidence-based synthesis, including why this score is better justified than conflicting scores>
Editorial recommendations: <specific, actionable recommendations for the authors>

Additional constraints:
- Preserve exactly the evaluation dimensions and assign an integer score from 1 to 5 for each dimension.
- If the reviews disagree, explain the final choice through the paper’s evidence, not through reviewer authority.
- Include concrete details when they improve precision, but remove redundant phrasing.
- Keep the final review self-contained: a reader should not need the three original reviews to understand the evaluation.

"""

def create_openai_client() -> OpenAI:
    api_key = ""
    if not api_key:
        raise RuntimeError("Defina a variável de ambiente OPENAI_API_KEY.")
    return OpenAI(api_key=api_key)


def create_results_folder() -> Path:
    folder_name = datetime.now().strftime("results_%d%m%y_%H:%M")
    results_folder = OUTPUT_DIR / folder_name
    results_folder.mkdir(parents=True, exist_ok=False)
    return results_folder


def parse_results_folder_timestamp(folder_name: str) -> datetime:
    match = RESULT_FOLDER_PATTERN.fullmatch(folder_name)
    if not match:
        raise ValueError(f"Nome de pasta inválido: {folder_name}")
    return datetime.strptime(f"{match.group(1)}_{match.group(2)}", "%d%m%y_%H:%M")


def find_latest_results_folder(now: datetime | None = None) -> Path:
    if now is None:
        now = datetime.now()

    candidates: list[tuple[float, Path]] = []
    for path in OUTPUT_DIR.iterdir():
        if not path.is_dir():
            continue
        try:
            timestamp = parse_results_folder_timestamp(path.name)
        except ValueError:
            continue
        delta_seconds = abs((now - timestamp).total_seconds())
        candidates.append((delta_seconds, path))

    if not candidates:
        raise FileNotFoundError("Nenhuma pasta results_DDMMYY_HH:MM foi encontrada.")

    return min(candidates, key=lambda item: item[0])[1]


def save_text(folder: Path, filename: str, content: str) -> None:
    (folder / filename).write_text(content, encoding="utf-8")


def unify_reviews(client: OpenAI, reviews_folder: Path) -> str:
    review_paths = sorted(reviews_folder.glob("revisao_[0-9]*.md"))
    if len(review_paths) != NUMBER_OF_REVIEWS:
        raise FileNotFoundError(
            f"A pasta '{reviews_folder.name}' deve conter {NUMBER_OF_REVIEWS} arquivos revisao_*.md; "
            f"foram encontrados {len(review_paths)}."
        )

    reviews = [path.read_text(encoding="utf-8") for path in review_paths]
    joined_reviews = "\n\n".join(
        f"===== REVIEW {index} =====\n{review}"
        for index, review in enumerate(reviews, start=1)
    )
    user_prompt = f"""
THREE INDEPENDENT REVIEWS:
{joined_reviews}

Now produce the single unified review according to the system instructions.
"""
    messages = [
        {"role": "system", "content": UNIFICATION_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        stream=False,
    )
    answer = response.choices[0].message.content or ""
    if not answer:
        raise RuntimeError("A API da OpenAI retornou uma resposta vazia.")
    return "\n".join(
        [
            "=" * 70,
            "AVALIAÇÃO UNIFICADA GERADA PELO ChatGPT",
            "=" * 70,
            answer,
            "",
            "=" * 70,
            "CHAMADA ENVIADA AO ChatGPT",
            "=" * 70,
            json.dumps(messages, ensure_ascii=False, indent=2),
            "",
            "=" * 70,
            "METADADOS PARA REPRODUTIBILIDADE",
            "=" * 70,
            f"Modelo solicitado: {OPENAI_MODEL}",
            f"Modelo usado: {getattr(response, 'model', OPENAI_MODEL)}",
            f"System fingerprint: {getattr(response, 'system_fingerprint', None) or '(não informado)'}",
        ]
    )


def main() -> None:
    
    deepseek_client = create_deepseek_client()
    results_folder = create_results_folder()

    for index in range(1, NUMBER_OF_REVIEWS + 1):
        answer = review_article(deepseek_client)[0]
        save_text(
            results_folder,
            f"revisao_{index}.md",
            answer,
        )
        print(f"Revisão {index} salva em {results_folder.name}/revisao_{index}.md")
       
    latest_folder = find_latest_results_folder()
    unified_review = unify_reviews(create_openai_client(), latest_folder)
    save_text(latest_folder, "revisao_unificada.md", unified_review)
    print(f"Avaliação unificada salva em {latest_folder.name}/revisao_unificada.md")


if __name__ == "__main__":
    main()
