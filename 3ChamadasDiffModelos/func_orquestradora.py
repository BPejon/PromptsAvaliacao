import json
import os
from pathlib import Path

from openai import OpenAI

from chamadas_para_modelos import (
    PROJECT_ROOT,
    PROVIDERS,
    gerar_resultados,
    read_string_constant,
)


UNIFIER_SCRIPT = PROJECT_ROOT / "sistema3chamadasUnificadas" / "3chamadas1revisor.py"


def unify_results(results_folder: Path) -> Path:
    review_paths = [
        results_folder / f"resultado_{provider.name}.md" for provider in PROVIDERS
    ]
    missing_paths = [path for path in review_paths if not path.is_file()]
    if missing_paths:
        missing_files = ", ".join(str(path) for path in missing_paths)
        raise FileNotFoundError(f"Resultados individuais não encontrados: {missing_files}")

    reviews = [path.read_text(encoding="utf-8").strip() for path in review_paths]
    empty_paths = [
        path for path, review in zip(review_paths, reviews, strict=True) if not review
    ]
    if empty_paths:
        raise ValueError(
            "Resultados individuais vazios: "
            + ", ".join(str(path) for path in empty_paths)
        )

    unification_prompt = read_string_constant(
        UNIFIER_SCRIPT, "UNIFICATION_SYSTEM_PROMPT"
    )
    joined_reviews = "\n\n".join(
        f"===== REVIEW FROM {provider.name} =====\n{review}"
        for provider, review in zip(PROVIDERS, reviews, strict=True)
    )
    messages = [
        {"role": "system", "content": unification_prompt},
        {
            "role": "user",
            "content": (
                f"THREE INDEPENDENT REVIEWS:\n{joined_reviews}\n\n"
                "Now produce the single unified review according to the system instructions."
            ),
        },
    ]

    api_key = os.environ.get("QWENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Defina a variável de ambiente OPENAI_API_KEY para unificar.")
    model = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
    response = OpenAI(api_key=api_key).chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
    answer = response.choices[0].message.content
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("A API da OpenAI retornou uma avaliação unificada vazia.")

    unified_report = "\n".join(
        [
            "# Revisão unificada",
            "",
            answer.strip(),
            "",
            "---",
            "Modelo: ChatGPT",
            f"Modelo solicitado: {model}",
            f"Modelo usado: {getattr(response, 'model', model)}",
            "",
            "## Instruções enviadas para unificação",
            "",
            "```json",
            json.dumps(messages, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    output_path = results_folder / "revisao_unificado.md"
    output_path.write_text(unified_report, encoding="utf-8")
    return output_path


def func_orquestradora() -> Path:
    results_folder = gerar_resultados()
    unified_path = unify_results(results_folder)
    print(f"Revisão unificada salva em {unified_path}")
    return unified_path


if __name__ == "__main__":
    func_orquestradora()
