## Chamada para o Deepseek com alteração de ordem
## Quero ver se eu alterar a ordem das chamadas para o Deepseek, se isso altera a avaliação final. A ideia é que a ordem das chamadas não deveria alterar a avaliação final, mas quero testar isso.

import json
import os
from openai import OpenAI

# ============================================================
# CONFIGURAÇÃO FIXA (para reprodutibilidade)
# ============================================================
MODEL = "deepseek-v4-pro"          # ou "deepseek-v4-flash"
TEMPERATURE = 1.0                  # recomendado pela DeepSeek
TOP_P = 1.0                        # recomendado pela DeepSeek
REASONING_EFFORT = "high"          # "low", "high" ou "max"
THINKING_ENABLED = True            # ativa o raciocínio explícito
DEBUG = False                      # exibe detalhes da chamada quando True

# ============================================================
# LEITURA DO PROMPT E DO ARTIGO
# ============================================================
# Opção 1: definir diretamente no código
SYSTEM_PROMPT = """
You are an expert academic reviewer. For the given technical survey, assign integer scores (1–5) for the following seven dimensions. Your evaluation must be rigorous, evidence-driven, domain-aware, and consistent with the rubric below.
Evaluate the survey based on its stated scope, objectives, and framing.
"""

EVALUATION_PROMPT= """

# Evaluation Score Prompt

## 1. Accuracy & Evidence

**Question:** Are the survey's substantive claims, descriptions, comparisons, and conclusions internally consistent, appropriately qualified, and adequately supported by the evidence presented in the survey?

5: Claims are consistently precise, internally consistent, appropriately qualified, and supported by citations or other evidence presented in the survey. Results, methods, contributions, limitations, and conclusions are described without apparent contradictions or unjustified extrapolation.
4: Claims are generally precise, consistent, and appropriately supported, with only minor overstatements, ambiguities, or insufficiently qualified claims.
3: The survey is broadly coherent and plausible, but contains noticeable overgeneralizations, ambiguities, unsupported assertions, or conclusions that extend beyond the evidence presented.
2: Multiple substantive claims are weakly supported, internally inconsistent, substantially overgeneralized, or presented with more certainty than the evidence in the survey warrants.
1: The survey contains pervasive contradictions, unsupported assertions, implausible claims, or conclusions that substantially exceed or conflict with the evidence presented.

**Important:** Evaluate accuracy and evidential support based only on the content and evidence available in the survey. Do not assume that a claim is factually correct merely because it is stated confidently or accompanied by a plausible citation. Do not attempt to verify claims against external literature that is not provided.

Examples of problems to consider:
A study's method, findings, or contribution are described inconsistently within the survey.
A conclusion is substantially stronger than the evidence or discussion presented.
Quantitative results are reported inconsistently in different sections.
The survey makes broad claims about trends, superiority, or state of the art without sufficient support in the presented evidence.
Limitations or contradictory evidence discussed elsewhere in the survey are ignored when drawing conclusions.
Interpretations or hypotheses are presented as established findings without appropriate qualification.

## 2. Citation Integrity

**Question:** Are citations used consistently, appropriately, and sufficiently throughout the survey, based on the information available in the review itself?

5: Citations are consistently present where substantive claims require support, are clearly associated with the claims they are intended to support, and are used consistently throughout the survey. References and in-text citations appear internally consistent, with no apparent internal inconsistencies, duplication, or other systematic citation problems suggestive of fabricated references.
4: Citation practice is generally strong, with only minor omissions, ambiguities, bibliographic inconsistencies, or uneven citation density.
3: Citation practice is mixed. Some important claims are adequately cited, but others lack citations, use ambiguous citation placement, or show noticeable bibliographic inconsistencies.
2: Important claims frequently lack citations, citation placement is often unclear, or the bibliography and in-text citations contain multiple inconsistencies or irregularities.
1: Citation practice is seriously compromised, with pervasive missing citations, substantial inconsistencies between in-text citations and the reference list, apparent fabricated references, or widespread citation-related problems.

**Important:** Evaluate citation integrity only from information available in the survey. Do not assume that a cited source supports a claim unless this can be established from the survey itself. Do not penalize a citation simply because the cited source cannot be externally verified.

Examples of problems to consider:
Important substantive claims have no citation where one would reasonably be expected.
Citations are placed so ambiguously that it is unclear which claim they support.
In-text citations do not correspond consistently to entries in the reference list.
Author names, publication years, titles, or citation identifiers are inconsistent within the survey.
A reference is repeatedly invoked for claims that are substantially different, without sufficient explanation in the review.

## 3. Writing Quality & Editorial Consistency

**Question:** Is the survey professionally written, clear, coherent, and consistent in terminology, tone, and presentation?

5: Writing is polished, clear, coherent, and consistently professional. Terminology is well defined and used consistently; prose is appropriately academic; formatting and citation presentation are stable; stylistic variation is purposeful rather than mechanical.
4: Writing is generally clear and professional, with only isolated inconsistencies in terminology, phrasing, formatting, or tone.
3: Writing is understandable but contains noticeable inconsistencies in terminology, phrasing, formality, paragraph structure, or presentation.
2: Frequent stylistic or terminological inconsistencies reduce readability or give the survey an uneven or mechanically assembled appearance.
1: Writing is substantially unclear, poorly edited, unprofessional, or inconsistent, seriously impairing readability.

**Penalty:** Penalize the score only when inconsistencies are frequent and substantial enough to impair readability or interpretation, not for isolated lapses.

**Important:** Do not penalize minor stylistic variation when it improves clarity or appropriately reflects differences between sections.

Examples of problems to consider:
• Ambiguous, repetitive, fragmented, or difficult-to-follow prose.
• Inconsistent terminology, abbreviations, capitalization, notation, or naming conventions.
•  Duplicated references, inconsistent bibliographic entries for the same work, or references listed in the bibliography but never cited in the text.
• Figures, tables, or other numbered elements that are not referred to or discussed in the text.
• Figures or tables with inadequate captions or inconsistent numeration.

## 4. Coverage

**Question:** Does the survey appropriately cover the major concepts, approaches, subfields, and representative developments relevant to its stated scope?

5: Covers the major foundational and emerging areas required by the scope, with appropriate selectivity and balance. Important areas are represented through meaningful discussion rather than simple enumeration.
4: Covers most major areas and several relevant recent developments. Minor omissions or imbalances exist but do not substantially affect the survey.
3: Covers many relevant areas but is noticeably uneven, shallow, or incomplete. Some important areas are missing or insufficiently developed.
2: Covers only a limited subset of the relevant landscape, or gives disproportionate attention to selected areas while omitting several important ones.
1: Major areas are substantially omitted, misrepresented, or outdated relative to the stated scope.

**Penalty:** Penalize the score if the survey is dominated by long enumerations of topics or papers without meaningful prioritization, depth, or conceptual organization.

**Important:** Do not require a survey to cover every possible topic. Reward appropriate selection and completeness relative to the declared scope, not maximum breadth.

Examples of problems to consider:
• Important concepts, approaches, or subfields within the stated scope are omitted.
• Major or representative developments are insufficiently represented.
• Coverage is substantially unbalanced without justification.
• A relevant area is mentioned but not developed enough to support the survey's objective. 

## 5. Relevance

**Question:** Does the content consistently support the stated scope, objective, research question, and framing of the survey?

5: Virtually all substantive content directly advances the survey's purpose. Background material is concise and clearly motivated; topics that might initially appear peripheral are explicitly connected to the central scope.
4: Content is strongly aligned with the stated purpose, with only occasional unnecessary material or minor digressions.
3: The survey is generally relevant, but some sections are weakly connected to its purpose or contain excessive background or generic discussion.
2: Several sections are only loosely related to the stated objective, and generic or peripheral material substantially reduces focus.
1: Large portions of the survey diverge from its intended scope or purpose.

**Penalty:** Penalize the score if significant portions of the paper provide generic background that substitutes for domain-specific review, analysis, or synthesis.

**Important:** Do not penalize background information when it is necessary to establish concepts required to understand the survey.

Examples of problems to consider:
• Substantial discussion falls outside the stated scope or research question.
• Sections or paragraphs do not clearly contribute to the survey's objective.
• Background material is disproportionately extensive relative to its relevance.
• The survey introduces topics that are not connected back to its central framing. 

## 6. Structure

**Question:** Is the survey logically organized, well-sectioned, and progressively developed?

5: The organization reflects meaningful conceptual, methodological, historical, or thematic relationships. Ideas build progressively, dependencies are clear, and transitions support the overall argument.
4: The survey has a clear and readable structure, with logical sequencing and generally effective transitions.
3: The overall outline is reasonable, but some sections lack conceptual layering, contain abrupt transitions, or feel weakly connected.
2: Topics are frequently presented as a list rather than as a coherent structure; transitions and progression are weak or unclear.
1: The organization is substantially disorganized or incoherent, making the survey difficult to follow.

**Penalty:** Penalize the score if the organization is dominated by rigid, repetitive section templates or paper-by-paper descriptions without meaningful conceptual grouping or progression.

**Important:** A chronological, methodological, thematic, or other organizational strategy is acceptable when it is appropriate to the survey's purpose. Do not reward or penalize a particular organizational scheme merely for its form.
Visual and tabular elements should be appropriately positioned and integrated into the narrative. Flag atypical placement when figures or tables introduce detailed analysis before the relevant concepts have been developed, or introduce substantive new material in the Conclusions. Do not penalize atypical placement when the element serves a clear introductory or summarizing function and is appropriately discussed.

Examples of problems to consider:
• Sections or subsections appear in an illogical order.
• Important ideas are introduced without sufficient context or later than expected.
• The organization is primarily a sequence of paper-by-paper summaries rather than a coherent progression.
• Conclusions or transitions do not follow naturally from the preceding discussion. 

## 7. Synthesis

**Question:** Does the survey analyze and integrate prior work into meaningful categories, comparisons, relationships, trends, trade-offs, gaps, or conceptual frameworks?

5: Provides strong analytical synthesis of the literature. Identifies meaningful relationships, differences, trends, trade-offs, research gaps, or conceptual patterns and uses them to develop useful taxonomies, frameworks, comparisons, or design spaces.
4: Provides substantial synthesis and comparison. Related works are meaningfully grouped or contrasted, although some opportunities for deeper analysis remain.
3: Goes beyond simple description in places, but synthesis is uneven or relatively shallow. Some categories or comparisons are provided without fully developing their implications.
2: Provides little synthesis; most works or methods are described independently with limited discussion of relationships, differences, trade-offs, or trends.
1: Essentially an enumeration of papers, methods, or topics with no meaningful analytical integration.

**Reward:** Meaningful taxonomies, comparative tables, conceptual diagrams, design spaces, or analytical frameworks that improve understanding of relationships within the literature.

**Penalty:** Penalize the score if the survey predominantly describes works independently without meaningful connections, comparisons, grouping, or interpretation.

**Important:** Do not reward the mere presence of tables, figures, taxonomies, or frameworks. They count as evidence of synthesis only when they expose meaningful relationships, differences, trends, trade-offs, or gaps. A taxonomy should reflect meaningful distinctions in the literature rather than categories imposed arbitrarily by the survey.

Examples of problems to consider:
• The survey mainly summarizes individual studies without integrating them.
• Related approaches are not grouped into meaningful categories.
• Important similarities, differences, trade-offs, or relationships are not discussed.
• Trends, research gaps, or emerging directions are asserted without being derived from the reviewed literature.

## Review Policy

Penalize listing without depth, unsupported claims, citation misuse, generic background inflation, mechanical template repetition, and lack of conceptual integration.
Reward appropriate selectivity, meaningful coverage, conceptual synthesis, structured comparisons, analytical insight, accurate representation of prior work, and strong citation support.
Do not reward the mere presence of tables, figures, taxonomies, references, or formal language. Evaluate the quality and function of these elements.
Do not penalize a survey simply because it does not cover every possible topic. Judge coverage relative to the declared scope and purpose.
Do not assume that confident or fluent writing indicates factual accuracy.
Evaluate each criterion independently. Avoid allowing strengths or weaknesses in one dimension to automatically determine scores in another. When the same issue affects multiple dimensions, assess its distinct consequences for each dimension rather than automatically penalizing the survey multiple times. 
Use the full 1–5 scale when warranted. Do not assign extreme scores merely to create score variation.
Scores should reflect the quality of the survey, not the perceived quality of the language model that generated it.
Score calibration: Do not apply automatic score caps based on isolated weaknesses. A penalty should affect the score in proportion to the severity, frequency, and impact of the problem. A score of 3 should represent genuinely moderate or mixed quality, not serve as a default ceiling whenever a weakness is detected.
Do not let a single local problem determine the score for an entire criterion unless the problem is pervasive or materially affects the overall quality of that dimension.

## Evaluation Procedure

Your evaluation should follow two steps.

### Step 1: JSON Scores

Return a valid JSON dictionary with integer values from 1 to 5 for each criterion.
Example:

```json
{
  "accuracy_evidence": 4,
  "citation_integrity": 3,
  "writing_quality_consistency": 4,
  "coverage": 5,
  "relevance": 4,
  "structure": 4,
  "synthesis": 3
}
```

### Step 2: Evaluation Notes

First, provide a concise overall assessment of 2–5 sentences, identifying the most important strengths and weaknesses of the survey.
Then, for each of the seven criteria, provide:
Score: the assigned integer score;
Critical observations: the specific strengths and/or weaknesses that justify the score;
Evidence: concrete examples from the survey whenever possible.
Do not merely restate the rubric or the score. Explain why the survey received that score.
For Accuracy & Evidence and Citation Integrity, explicitly identify any claims, descriptions, or citations that appear unsupported, internally inconsistent, ambiguous, or potentially problematic based on the information available in the survey itself. Do not claim that a citation is mismatched or fabricated unless this can be established from the survey. 
The output must be in markdown format.

## Survey to Evaluate

Report Content:

"""


ARTIGO = r""" 

"""

def create_deepseek_client() -> OpenAI:
    """Cria o cliente DeepSeek usando a chave fornecida pelo ambiente."""
    api_key = ""
    if not api_key:
        raise RuntimeError("Defina a variável de ambiente DEEPSEEK_API_KEY.")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def review_article(
    client: OpenAI,
) -> tuple[str, str | None, object, list[dict[str, str]]]:
    """Executa uma revisão do artigo e retorna resposta, raciocínio e resposta bruta."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": EVALUATION_PROMPT},
        {"role": "user", "content": ARTIGO},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        reasoning_effort=REASONING_EFFORT,
        extra_body={"thinking": {"type": "enabled" if THINKING_ENABLED else "disabled"}},
        stream=False,
    )
    message = response.choices[0].message
    return (
        message.content,
    )


def format_review_output(
    answer: str,
    reasoning: str | None,
    response: object,
    messages: list[dict[str, str]],
) -> str:
    """Formata a resposta e, quando habilitado, os detalhes da chamada."""
    if not DEBUG:
        return answer or ""

    return "\n".join(
            [
                "=" * 70,
                "ANÁLISE GERADA PELO DeepSeek",
                "=" * 70,
                answer or "(resposta vazia)",
            "",
            "=" * 70,
            "RACIOCÍNIO (thinking / reasoning_content)",
            "=" * 70,
            reasoning or "(nenhum raciocínio retornado)",
            "",
            "=" * 70,
            "METADADOS PARA REPRODUTIBILIDADE",
            "=" * 70,
            f"Modelo solicitado: {MODEL}",
            f"Modelo usado: {getattr(response, 'model', MODEL)}",
            f"System fingerprint: {getattr(response, 'system_fingerprint', None) or '(não informado)'}",
            f"Reasoning effort: {REASONING_EFFORT}",
            f"Thinking enabled: {THINKING_ENABLED}",
            f"Temperature: {TEMPERATURE}",
            f"Top_p: {TOP_P}",
            "",
            "=" * 70,
            "CHAMADA ENVIADA AO DeepSeek",
            "=" * 70,
            json.dumps(messages, ensure_ascii=False, indent=2),
        ]
    )


if __name__ == "__main__":
    review, reasoning, response, messages = review_article(create_deepseek_client())
    print(format_review_output(review, reasoning, response, messages))