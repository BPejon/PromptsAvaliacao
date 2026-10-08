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

# A Survey on 3D Gaussian Splatting

**Abstract**—3D Gaussian splatting (GS) has emerged as a transformative technique in explicit radiance field and computer graphics. This innovative approach, characterized by the use of millions of learnable 3D Gaussians, represents a significant departure from mainstream neural radiance field approaches, which predominantly use implicit, coordinate-based models to map spatial coordinates to pixel values. 3D GS, with its explicit scene representation and differentiable rendering algorithm, not only promises real-time rendering capability but also introduces unprecedented levels of editability. This positions 3D GS as a potential game-changer for the next generation of 3D reconstruction and representation. In the present paper, we provide the first systematic overview of the recent developments and critical contributions in the domain of 3D GS. We begin with a detailed exploration of the underlying principles and the driving forces behind the emergence of 3D GS, laying the groundwork for understanding its significance. A focal point of our discussion is the practical applicability of 3D GS. By enabling unprecedented rendering speed, 3D GS opens up a plethora of applications, ranging from virtual reality to interactive media and beyond. This is complemented by a comparative analysis of leading 3D GS models, evaluated across various benchmark tasks to highlight their performance and practical utility. The survey concludes by identifying current challenges and suggesting potential avenues for future research. Through this survey, we aim to provide a valuable resource for both newcomers and seasoned researchers, fostering further exploration and advancement in explicit radiance field.

**Index Terms**—3D Gaussian Splatting, Explicit Radiance Field, Real-time Rendering, Scene Understanding

## 1 INTRODUCTION

The objective of image based 3D scene reconstruction is to convert a collection of views or videos capturing a scene into a digital 3D model that can be computationally processed, analyzed, and manipulated. This hard and long-standing problem is fundamental for machines to comprehend the complexity of real-world environments, facilitating a wide array of applications such as 3D modeling and animation, robot navigation, historical preservation, augmented/virtual reality, and autonomous driving.

The journey of 3D scene reconstruction began long before the surge of deep learning, with early endeavors focusing on light fields and basic scene reconstruction methods [1]–[3]. These early attempts, however, were limited by their reliance on dense sampling and structured capture, leading to significant challenges in handling complex scenes and lighting conditions. The emergence of structure-from-motion [4] and subsequent advancements in multi-view stereo [5] algorithms provided a more robust framework for 3D scene reconstruction. Despite these advancements, such methods struggled with novel-view synthesis and texture loss. NeRF represents a quantum leap in this progression. By leveraging deep neural networks, NeRF enabled the direct mapping of spatial coordinates to color and density. The success of NeRF hinged on its ability to create continuous, volumetric scene functions, producing results with unprecedented fidelity. However, as with any burgeoning technology, this implementation came at a cost: i) Computational Intensity. NeRF based methods are computationally intensive [6]–[9], often requiring extensive training times and substantial resources for rendering, especially for high-resolution outputs. ii) Editability. Manipulating scenes represented implicitly is challenging, since direct modifications to the neural network's weights are not intuitively related to changes in geometric or appearance properties of the scene.

Fig. 1. The number of published papers and official GitHub stars on 3D GS. The set of statistics is sourced from # Papers and # GitHub Stars.

It is in this context that 3D Gaussian splatting (GS) [10] emerges, not merely as an incremental improvement but as a paradigm-shifting approach that redefines the boundaries of scene representation and rendering. While NeRF excelled in creating photorealistic images, the need for faster, more efficient rendering methods was becoming increasingly apparent, especially for applications (e.g., virtual reality and autonomous driving) that are highly sensitive to latency. 3D GS addressed this need by introducing an advanced, explicit scene representation that models a scene using millions of learnable 3D Gaussians in space. Unlike the implicit, coordinate-based models [11], [12], 3D GS employs an explicit representation and highly parallelized workflows, facilitating more efficient computation and rendering. The innovation of 3D GS lies in its unique blend of the benefits of differentiable pipelines and point-based rendering techniques [13]–[17]. By representing scenes with learnable 3D Gaussians, it preserves the strong fitting capability of continuous volumetric radiance fields, essential for high-quality image synthesis, while simultaneously avoiding the computational overhead associated with NeRF based methods (e.g., computationally expensive ray-marching, and unnecessary calculations in empty space).

The introduction of 3D GS is not just a technical advancement; it represents a fundamental shift in how we approach scene representation and rendering in computer vision and graphics. By enabling real-time rendering capabilities without compromising on visual quality, 3D GS opens up a plethora of possibilities for applications ranging from virtual reality and augmented reality to real-time cinematic rendering and beyond [18]–[21]. This technology holds the promise of not only enhancing existing applications but also enabling new ones that were previously unfeasible due to computational constraints. Furthermore, 3D GS's explicit scene representation offers unprecedented flexibility to control the objects and scene dynamics, a crucial factor in complex scenarios involving intricate geometries and varying lighting conditions [22]–[24]. This level of editability, combined with the efficiency of the training and rendering process, positions 3D GS as a transformative force in shaping future developments in relevant fields.

In an effort to assist readers in keeping pace with the swift evolution of 3D GS, we provide the first survey on 3D GS, which presents a systematic and timely collection of the most significant literature on the topic. Given that 3D GS is a very recent innovation (Fig. 1), this survey focuses in particular on its principles, and the diverse developments and contributions that have emerged since its introduction. The selected follow-up works are primarily sourced from top-tier conferences, to provide a thorough and up-to-date (Dec. 2024) analysis of the theoretical foundations, remarkable developments, and burgeoning applications of 3D GS. Acknowledging the nascent yet rapidly evolving nature of 3D GS, this survey is inevitably a biased view, but we strive to offer a balanced perspective that reflects both the current state and the future potential of this field. Our aim is to encapsulate the primary research trends and serve as a valuable resource for both researchers and practitioners eager to understand and contribute to this rapidly evolving domain. The distinctions of this survey from existing literature [25]–[28] are evident in the following aspects:

We provide the first systematic and comprehensive review that examines 3D GS from a macro-level perspective by establishing clear taxonomies and frameworks. This high-level systematization helps researchers identify trends and potential directions that might not be apparent from paper-specific reviews. Our organizational structure serves as a roadmap for understanding how different approaches relate to and build upon each other within the 3D GS ecosystem.

This paper is the first and only survey to thoroughly delve into the theoretical background and fundamental principles of 3D GS. The comprehensive coverage makes the field more approachable for newcomers while providing valuable insights for experienced researchers.

Fig. 2. Structure of the overall review.

To ensure our survey remains relevant and offer long-term value in this rapidly evolving field, we maintain two dynamic GitHub repositories: one that follows our survey's organizational structure and another that includes comprehensive performance comparisons with analysis data.

A summary of the structure of this article can be found in Fig. 2, which is presented as follows: Sec. 2 provides a brief background on problem formulation, terminology, and related research domains. Sec. 3 introduces the essential insights of 3D GS, encompassing the rendering process with learned 3D Gaussians and the optimization details (i.e., how to learn 3D Gaussians) of 3D GS. Sec. 4 presents several fruitful directions that aim to improve the capabilities of the original 3D GS. Sec. 5 unveils the diverse application areas and tasks where 3D GS has made significant impacts, showcasing its versatility. Sec. 6 conducts performance comparison and analysis. Finally, Sec. 7 and 8 highlight the open questions for further research and conclude the survey.

## 2 BACKGROUND

In this section, we first provide a brief formulation of radiance fields (Sec. 2.1), including both implicit and explicit ones. Sec. 2.2 further establishes linkages with relevant rendering algorithms and terminologies. For a comprehensive overview of radiance fields, scene reconstruction and representation, and rendering methods, please see the excellent surveys [29]–[33] for more insights.

### 2.1 Radiance Field

**Implicit Radiance Field.** An implicit radiance field represents light distribution in a scene without explicitly defining the geometry of the scene. In the deep learning era, neural networks are often used to learn a continuous volumetric scene representation [34], [35]. The most prominent example is NeRF [12]. In NeRF (Fig. 3a), one or more MLPs are used to map a set of spatial coordinates \((x,y,z)\) and viewing directions \((\theta,\phi)\) to color \(c\) and volume density \(\sigma\):

$$
(c,\sigma)\leftarrow \mathrm{MLP}(x,y,z,\theta,\phi). \quad (1)
$$

This format allows for a differentiable and compact representation of complex scenes, albeit often at the cost of high computational load due to volumetric ray marching. Note that typically, the color \(c\) is direction-dependent, whereas the volume density \(\sigma\) is not [12].

**Explicit Radiance Field.** An explicit radiance field directly represents the distribution of light in a discrete spatial structure, such as a voxel grid or a set of points [36], [37]. Each element in this structure stores the radiance information for its respective location. This allows for direct and often faster access to radiance data but at the cost of higher memory usage and potentially lower resolution. Similar to the implicit radiance field, the explicit one is written as:

$$
(c,\sigma)\leftarrow \mathrm{DataStructure}(x,y,z,\theta,\phi), \quad (2)
$$

where DataStructure could be in the format of volumes, point clouds, etc. DataStructure encodes directional color in two main ways. One is encoding high-dimensional features that are subsequently decoded by a lightweight MLP. Another one is directly storing coefficients of directional basis functions, such as spherical harmonics or spherical Gaussians, where the final color is computed as a function of these coefficients and the viewing direction.

**3D Gaussian Splatting: Best-of-Both Worlds.** 3D GS [10] is an explicit radiance field with the advantages of implicit radiance fields. Concretely, it leverages the strengths of both paradigms by utilizing learnable 3D Gaussians as the basis elements of DataStructure. Note that 3D GS encodes the opacity \(\alpha\) directly for each Gaussian, as opposed to approaches of first establishing density \(\sigma\) and then computing opacity based on that density. As in previous reconstruction work, 3D Gaussians are optimized under the supervision of multi-view images to represent the scene. Such a 3D Gaussian based differentiable pipeline combines the benefits of neural network based optimization and explicit, structured data storage. This hybrid approach aims to achieve real-time, high-quality rendering and requires less training time, particularly for complex scenes and high-resolution outputs.

### 2.2 Context and Terminology

Volumetric rendering aims to transform a 3D volumetric representation into an image by integrating radiance along camera rays. A camera ray \(r(t)\) can be parameterized as: \(r(t)=o+td,t\in[t_{\mathrm{near}},t_{\mathrm{far}}]\), where \(\pmb{o}\) represents the ray origin (camera center), \(d\) is the ray direction, and \(t\) indicates the distance along the ray between near and far clipping planes. The pixel color \(C(r)\) is computed through a line integral along the ray \(r(t)\), mathematically expressed as [12]:

$$
C(r)=\int_{t_{\mathrm{near}}}^{t_{\mathrm{far}}}T(t)\sigma(r(t))c(r(t),d)dt, \quad (3)
$$

where \(\sigma(r(t))\) is the volume density at point \(r(t)\), \(c(r(t),d)\) is the color at that point, and \(T(t)\) is the transmittance. Raymarching directly approximates the volumetric rendering integral by systematically "stepping" along a ray and sampling the scene's properties at discrete intervals. NeRF [12] shares the same spirit of ray-marching and introduces importance sampling and positional encoding to improve the quality of synthesized images. While providing high-quality results, ray-marching is computationally expensive, especially for high-resolution images.

Point-based rendering represents another class of rendering algorithms, of which 3D GS introduces a notable implementation. Its simplest form [38] rasterizes point clouds with a fixed size, which introduces drawbacks such as holes and rendering artifacts. Seminal works addressed these limitations through various methods, including: i) splatting point primitives with a spatial extent [14], [15], [39], [40], and ii) more recently, embedding neural features directly into points for subsequent network-based rendering [41], [42]. 3D GS uses 3D Gaussian as the point primitive that contains explicit attributes (e.g., color and opacity) instead of implicit neural features. The rendering approach, i.e., point-based \(\alpha\)-blending (exemplified in Eq. 5), shares the same image formation model as NeRF-style volumetric rendering (Eq. 3) [10], but demonstrates substantial speed advantages. This advantage originates from fundamental algorithmic differences. NeRFs approximate a line integral along a ray for each pixel, requiring expensive sampling. Point-based methods render point clouds using rasterization, which inherently benefits from parallel computational strategies [43].

## 3 3D GAUSSIAN SPLATTING: PRINCIPLES

3D GS offers a breakthrough in real-time, high-resolution image rendering, without relying on deep neural networks. This section aims to provide essential insights of 3D GS. We first elaborate on how 3D GS synthesizes an image given well-constructed 3D Gaussians in Sec. 3.1, i.e., the forward process of 3D GS. Then, we introduce how to obtain well-constructed 3D Gaussians for a given scene in Sec. 3.2, i.e., the optimization process of 3D GS.

### 3.1 Rendering with Learned 3D Gaussians

Consider a scene represented by (millions of) optimized 3D Gaussians. The objective is to generate an image from a specified camera pose. Recall that NeRFs approach this task through computationally demanding volumetric ray-marching, sampling 3D space points per pixel. Such a paradigm struggles with high-resolution image synthesis, failing to achieve real-time rendering, especially for platforms with limited computing resources [10].

Fig. 3. NeRFs vs. 3D GS. (a) NeRF samples along the ray and then queries the MLP to obtain corresponding colors and densities, which can be seen as a backward mapping (ray tracing). (b) In contrast, 3D GS projects all 3D Gaussians into the image space (i.e., splatting) and then performs parallel rendering, which can be viewed as a forward mapping (rasterization). Best viewed in color.

By contrast, 3D GS begins by projecting these 3D Gaussians onto a pixel-based image plane, a process termed "splatting" [39], [40] (see Fig. 3b). Afterwards, 3D GS sorts these Gaussians and computes the value for each pixel. As shown in Fig. 3, the rendering of NeRFs and 3D GS can be viewed as an inverse process of each other. In what follows, we begin with the definition of a 3D Gaussian, which is the minimal element of the scene representation in 3D GS. Next, we describe how these 3D Gaussians can be used for differentiable rendering. Finally, we introduce the acceleration technique used in 3D GS, which is the key to fast rendering.

**Properties of 3D Gaussian.** A 3D Gaussian is characterized by its center (position) \(\mu\), opacity \(\alpha\), 3D covariance matrix \(\pmb{\Sigma}\), and color \(c\). \(c\) is represented by spherical harmonics for view-dependent appearance. All the properties are learnable and optimized through back-propagation.

**Frustum Culling.** Given a specified camera pose, this step determines which 3D Gaussians are outside the camera's frustum. By doing so, 3D Gaussians outside the given view will not be involved in the subsequent computation.

**Splatting.** In this step, 3D Gaussians (ellipsoids) in 3D space are projected into 2D image space (ellipses). The projection proceeds through two transformations: first, transforming 3D Gaussians from world coordinates to camera coordinates using the viewing transformation, and subsequently splatting these Gaussians into 2D image space via an approximation of the projective transformation. Mathematically, given the 3D covariance matrix \(\pmb{\Sigma}\) describing a 3D Gaussian's spatial distribution, and the viewing transformation matrix \(\mathbf{W}\), the 2D covariance matrix \(\pmb{\Sigma}^{\prime}\) characterizing the projected 2D Gaussian is computed through:

$$
\pmb{\Sigma}^{\prime}=J\pmb{W}\pmb{\Sigma}\pmb{W}^{\top}\pmb{J}^{\top}, \quad (4)
$$

where \(J\) is the Jacobian of the affine approximation of the projective transformation [10], [39]. One might wonder why the standard camera intrinsics based projective transformation is not used here. This is because its mappings are not affine and therefore cannot directly project \(\pmb{\Sigma}\). 3D GS adopts an affine one proposed in [39] which approximates the projective transformation using the first two terms (including \(J\)) of the Taylor expansion (see Sec. 4.4 in [39]).

**Rendering by Pixels.** Before delving into the final version of 3D GS which utilizes several techniques to boost parallel computation, we first elaborate on its simpler form to offer insights into its basic working mechanism. Given the position of a pixel \(\pmb{x}\), its distance to all overlapping Gaussians, i.e., the depths of these Gaussians, can be computed through the viewing transformation matrix \(\mathbf{W}\), forming a sorted list of Gaussians \(\mathcal{N}\). Then, \(\alpha\)-blending is adopted to compute the final color of this pixel:

$$
C=\sum_{n=1}^{|\mathcal{N}|}c_{n}\alpha_{n}^{\prime}\prod_{j=1}^{n-1}(1-\alpha_{j}^{\prime}), \quad (5)
$$

where \(c*{n}\) is the learned color. The final opacity \(\alpha*{n}^{\prime}\) is the multiplication result of the learned opacity \(\alpha\_{n}\) and the Gaussian, defined as follows:

$$
\alpha_{n}^{\prime}=\alpha_{n}\times\exp\big(-\frac{1}{2}(\pmb{x}^{\prime}-\pmb{\mu}_{n}^{\prime})^{\top}\pmb{\Sigma}_{n}^{\prime -1}(\pmb{x}^{\prime}-\pmb{\mu}_{n}^{\prime})\big), \quad (6)
$$

where \(\pmb{x}^{\prime}\) and \(\mu\_{n}^{\prime}\) are coordinates in the projected space. It is a reasonable concern that the rendering process described could be slower compared to NeRFs, given that generating the required sorted list is hard to parallelize. Indeed, this concern is justified; rendering speeds can be significantly impacted when utilizing such a simplistic, pixel-by-pixel approach. To achieve real-time rendering, 3D GS makes several concessions to accommodate parallel computation.

**Tiles (Patches).** To avoid the cost computation of deriving Gaussians for each pixel, 3D GS shifts the precision from pixel-level to patch-level detail, which is inspired by tile-based rasterization [43]. Concretely, 3D GS initially divides the image into multiple non-overlapping patches (tiles). Fig. 4b provides an illustration of tiles. Each tile comprises \(16\times16\) pixels as suggested in [10]. 3D GS further determines which tiles intersect with these projected Gaussians. Given that a projected Gaussian may cover several tiles, a logical method involves replicating the Gaussian, assigning each copy an identifier (i.e., a tile ID) for the relevant tile.

Fig. 4. An illustration of the forward process of 3D GS (see Sec. 3.1). (a) The splatting step projects 3D Gaussians into image space. (b) 3D GS divides the image into multiple non-overlapping patches, i.e., tiles. (c) 3D GS replicates the Gaussians which cover several tiles, assigning each copy an identifier, i.e., a tile ID. (d) By rendering the sorted Gaussians, we can obtain all pixels within the tile. Note that the computational workflows for pixels and tiles are independent and can be done in parallel. Best viewed in color.

**Parallel Rendering.** After replication, 3D GS combines the respective tile ID with the depth value obtained from the view transformation for each Gaussian. This results in an unsorted list of bytes where the upper bits represent the tile ID and the lower bits signify depth. By doing so, the sorted list can be directly utilized for rendering (i.e., alpha compositing). Fig. 4c and Fig. 4d provide the visual demonstration of such concepts. It's worth highlighting that rendering each tile and pixel occurs independently, making this process highly suitable for parallel computations. An additional benefit is that each tile's pixels can access a common shared memory and maintain an uniform read sequence (Fig. 5), enabling parallel execution of alpha compositing with increased efficiency. In the official implementation of the original paper [10], the framework regards the processing of tiles and pixels as analogous to the blocks and threads, respectively, in CUDA programming architecture.

Fig. 5. An illustration of the tile based parallel (at the pixel-level) rendering. All the pixels within a tile (Tile1 here) access the same ordered Gaussian list stored in a shared memory for rendering. As the system processes each Gaussian sequentially, every pixel in the tile evaluates the Gaussian's contribution according to the distance (i.e., the exp term in Eq. 6). Therefore, the rendering for a tile can be completed by iterating through the list of Gaussians just once. The computation for the red Gaussian follows a similar way and is omitted here for simplicity.

In a nutshell, 3D GS introduces several approximations during rendering to enhance computational efficiency while maintaining a high standard of image synthesis quality.

### 3.2 Optimization of 3D Gaussian Splatting

At the heart of 3D GS lies an optimization procedure devised to construct a copious collection of 3D Gaussians that accurately captures the scene's essence, thereby facilitating free-viewpoint rendering. On the one hand, the properties of 3D Gaussians should be optimized via differentiable rasterization to fit the textures of a given scene. On the other hand, the number of 3D Gaussians that can represent a given scene well is unknown in advance. We will introduce how to optimize the properties of each Gaussian in Sec. 3.2.1 and how to adaptively control the density of the Gaussians in Sec. 3.2.2. The two procedures are interleaved within the optimization workflow. Since there are many manually set hyperparameters in the optimization process, we omit the notations of most hyperparameters for clarity.

#### 3.2.1 Parameter Optimization

- **Loss Function.** Once the synthesis of the image is completed, the difference between the rendered image and ground truth can be measured. All the learnable parameters are optimized by stochastic gradient descent using the \(\ell_1\) and D-SSIM loss functions:

$$
\mathcal{L}=(1-\lambda)\mathcal{L}_1+\lambda\mathcal{L}_{\mathrm{D-SSIM}}, \quad (7)
$$

where \(\lambda\in[0,1]\) is a weighting factor.

- **Parameter Update.** Most properties of a 3D Gaussian can be optimized directly through back-propagation. It is essential to note that directly optimizing the covariance matrix \(\Sigma\) can result in a non-positive semi-definite matrix, which would not adhere to the physical interpretation typically associated with covariance matrices. To circumvent this issue, 3D GS chooses to optimize a quaternion \(\pmb{q}\) and a 3D vector \(s\). Here \(\pmb{q}\) and \(s\) represent rotation and scale, respectively. This approach allows the covariance matrix \(\pmb{\Sigma}\) to be reconstructed as follows:

$$
\pmb{\Sigma}=\pmb{R}\pmb{S}\pmb{S}^{\top}\pmb{R}^{\top}, \quad (8)
$$

where \(R\) is the rotation matrix derived from the quaternion \(\pmb{q}\) and \(s\) is the scaling matrix given by \(\mathrm{diag}(s)\). As seen, there is a complex computational graph to obtain the opacity \(\alpha\_{i}\), i.e., \(\pmb{q}\) and \(s\mapsto\pmb{\Sigma},\pmb{\Sigma}\mapsto\pmb{\Sigma}^{\prime}\), and \(\pmb{\Sigma}^{\prime}\mapsto\alpha\). To avoid the cost of automatic differentiation, 3D GS derives the gradients for \(\pmb{q}\) and \(s\) so as to compute them directly during optimization.

#### 3.2.2 Density Control

- **Initialization.** 3D GS starts with the initial set of sparse points from SfM or random initialization. Note that a good initialization is essential to convergence and reconstruction quality [44]. Afterwards, point densification and pruning are adopted to control the density of 3D Gaussians.

- **Point Densification.** In the point densification phase, 3D GS adaptively increases the density of Gaussians to better capture the details of a scene. This process focuses on areas with missing geometric features or regions where Gaussians are too spread out. The densification procedure will be performed at regular intervals (i.e., after a certain number of training iterations), focusing on those Gaussians with large view-space positional gradients (i.e., above a specific threshold). It involves either cloning small Gaussians in under-reconstructed areas or splitting large Gaussians in over-reconstructed regions. For cloning, a copy of the Gaussian is created and moved towards the positional gradient. For splitting, a large Gaussian is replaced with two smaller ones, reducing their scale by a specific factor. This step seeks an optimal distribution and representation of Gaussians in 3D space, enhancing the overall quality of the reconstruction.

- **Point Pruning.** The point pruning stage involves the removal of superfluous or less impactful Gaussians, which can be viewed as a regularization process. It is executed by eliminating Gaussians that are virtually transparent (with \(\alpha\) below a specified threshold) and those that are excessively large in either world-space or view-space. In addition, to prevent unjustified increases in Gaussian density near input

## 4 3D GAUSSIAN SPLATTING: DIRECTIONS

Though 3D GS has achieved impressive milestones, significant room for improvement remains, e.g., data and hardware requirement, rendering and optimization algorithm, and applications in downstream tasks. In the subsequent sections, we seek to elaborate on select extended versions. These are: i) 3D GS for Sparse Input [45]–[55] (Sec. 4.1), ii) Memory-efficient 3D GS [56]–[64] (Sec. 4.2), iii) Photorealistic 3D GS [65]–[80] (Sec. 4.3), iv) Improved Optimization Algorithms [22], [77], [81]–[86] (Sec. 4.4), v) 3D Gaussian with More Properties [87]–[93] (Sec. 4.5), vi) Hybrid Representation [94]–[96] (Sec. 4.6), and vii) New Rendering Algorithm (Sec. 4.7). While we have carefully selected several key directions, we acknowledge that it is inevitably a biased view. A more comprehensive collection is given in Github.

### 4.1 3D GS for Sparse Input

A notable issue of 3D GS is the emergence of artifacts in areas with insufficient observational data. This challenge is a prevalent limitation in radiance field rendering, where sparse data often leads to inaccuracies in reconstruction. From a practical perspective, reconstructing scenes from limited viewpoints is of significant interest, particularly for the potential to enhance functionality with minimal input.

Existing methods can be categorized into two primary groups. i) Regularization based methods introduce additional constraints such as depth information to enhance the detail and global consistency [46], [49], [51], [55]. For example, DNGaussian [49] introduced a depth-regularized approach to address the challenge of geometry degradation in sparse input. FSGS [46] devised a Gaussian Unpooling process for initialization and also introduced depth regularization. MVSplat [51] proposed a cost volume representation so as to provide geometry cues. Unfortunately, when dealing with a limited number of views, or even just one, the efficacy of regularization techniques tends to diminish, which leads to ii) generalizability based methods that use learned priors [47], [48], [53], [97]. One approach involves synthesizing additional views through generative models, which can be seamlessly integrated into existing reconstruction pipelines [98]. However, this augmentation strategy is computationally intensive and inherently bounded by the capabilities of the used generative model. Another well-known paradigm employs feed-forward Gaussian model to directly generates the properties of a set of 3D Gaussians. This paradigm typically requires multiple views for training but can reconstruct 3D scenes with only one input image. For instance, PixelSplat [47] proposed to sample Gaussians from dense probability distributions. Splatter Image [48] introduced a 2D image-to-image network that maps an input image to a 3D Gaussian per pixel. However, as the generated pixel-aligned Gaussians are distributed nearly evenly in the space, they struggle to represent high-frequency details and smoother regions with an appropriate number of Gaussians.

The challenge of 3D GS for sparse inputs centers on the modeling of priors, whether through depth information, generative models, or feed-forward Gaussian models. The fundamental trade-off lies between overfitting to available views and using learned priors for generalization. Future research could explore adaptive mechanisms for controlling this trade-off, potentially through learned confidence measures, context-aware prior selection, user preferences, etc. In addition, while current methods focus on static scenes, extending these approaches to dynamic scenarios presents an exciting frontier for investigation, particularly in handling temporal consistency and motion-induced artifacts.

### 4.2 Memory-efficient 3D GS

While 3D GS demonstrates remarkable capabilities, its scalability poses significant challenges, particularly when juxtaposed with NeRF-based methods. The latter benefits from the simplicity of storing merely the parameters of a learned MLP. This scalability issue becomes increasingly acute in the context of large-scale scene management, where the computational and memory demands escalate substantially. Consequently, there is an urgent need to optimize memory usage in both model training and storage.

Recent research has pursued two primary directions to address memory efficiency. First, several approaches focus on reducing the number of 3D Gaussians [58], [62], [63]. These methods either employ strategic pruning of low-impact Gaussians, such as the volume-based masking [58], or represent neighboring Gaussians using the same properties stored within a "local anchor" obtained by clustering [22], hash-grid [62], etc. Second, researchers have developed methods for compressing Gaussian's properties [58], [61], [62]. For instance, Niedermayr et al. [61] compressed color and Gaussian parameters into compact codebooks, using sensitivity measures for effective quantization and fine-tuning. HAC [62] predicted the probability of each quantized attribute using Gaussian distributions and then devise an adaptive quantization module. These directions are not mutually exclusive; instead, one framework might use a hybrid approach combining multiple strategies.

While current compression techniques have achieved significant storage reduction ratios (often by factors of 10-\(20\times\)), several challenges remain. The field particularly needs advances in memory efficiency during the training phase, potentially through quantization-aware training protocols, the development of scene-agnostic, reusable codebooks, etc. Furthermore, optimizing the trade-off between compression efficiency and visual fidelity remains an open problem.

### 4.3 Photorealistic 3D GS

The current rendering pipeline of 3D GS (Sec. 3.1) is straightforward and involves several drawbacks. For instance, the simple visibility algorithm may lead to a drastic switch in the depth/blending order of Gaussians [10]. The visual fidelity of rendered images, including aspects such as aliasing, reflections, and artifacts, can be further optimized.

Recent research has focused on addressing three main aspects of visual quality, with aliasing being specific to 3D GS's rendering algorithm, while reflection and blur handling represent broader challenges in 3D reconstruction. i) Aliasing. Due to the discrete sampling paradigm (viewing each pixel as a single point instead of an area), 3D GS is susceptible to aliasing when dealing with varying resolutions, which leads to blurring or jagged edges. Solutions emerged at both training and inference stages. Researchers developed training-time improvements from the sampling rate perspective and introduced schemes such as multi-scale Gaussians [67], 2D Mip filter [65], and conditioned logistic function [78]. Inference-time solutions, such as 2D scale-adaptive filtering [80], offer enhanced fidelity that can be integrated into any existing 3D GS frameworks. ii) Reflection. Achieving realistic rendering of reflective materials is a hard, long-standing problem in 3D scene reconstruction. Recent works have introduced various approaches to model reflective materials [68], [73], [99] and enable relightable Gaussian representation [23], though achieving physically accurate specular effects remains challenging. iii) Blur. While 3D GS excels on carefully curated datasets, real-world captures often suffer from blurs such as motion blur and defocus blur. Recent approaches explicitly incorporated blur modeling during training, employing techniques such as coarse-to-fine kernel optimization [74] and photometric bundle adjustment [75] to address this challenge.

While the approximations made in 3D GS (Sec. 3.1) contribute to its computational efficiency, they also lead to aliasing, difficulties in illumination estimation, etc. Current solutions, though impressive, typically address individual problems rather than providing a universal solution. A practical intermediate approach involves first detecting specific issues (e.g., aliasing, blur) and then applying targeted optimization strategies. The ultimate goal remains developing an advanced reconstruction system that overcomes these limitations, either through fundamental improvements to 3D GS or through brand-new architectures.

### 4.4 Improved Optimization Algorithms

The optimization of 3D GS presents several challenges that affect the quality of reconstruction. These include issues with convergence speed, visual artifacts from improper Gaussians, and the need for better regularization during optimization. The raw optimization method (Sec. 3.2) might lead to overreconstruction in some regions while underrepresenting others, resulting in blur and visual inconsistencies.

Three main directions stand out for improving the optimization of 3D GS. i) Additional Regularization (e.g., frequency [84] and geometry [22], [77]). Geometry-aware approaches have been particularly successful, preserving scene structure through the incorporation of local anchor points [22], depth and surface constraints [100]–[102], Gaussian volumes [103], etc. ii) Optimization Procedure Enhancement [44], [101], [104]. While the original strategy of density control (Sec. 3.2.2) has proven valuable, considerable room for improvement remains. For example, GaussianPro [44] addresses the challenge of dense initialization in textureless surfaces and large-scale scenes through an advanced Gaussian densification strategy. iii) Constraint Relaxation. Reliance on external tools/algorithms can introduce errors and cap the system's performance potential. For instance, SfM, commonly used in the initialization process, is error-prone and struggle with complex scenes. Recent works have begun exploring COLMAP-free approaches utilizing stream continuity [81], [105], potentially enabling learning from internet-scale unposed video datasets.

Though impressive, existing methods primarily concentrate on optimizing Gaussians to accurately reconstruct scenes from scratch, neglecting a challenging yet promising solution which reconstructs scenes in a few-shot manner through established "meta representations". Such solution could enable adaptive meta-learning strategies that combine scene-specific and general knowledge. See "learning physical priors from large-scale data" in Sec. 7 for further insights.

### 4.5 3D Gaussian with More Properties

Despite impressive, the properties of 3D Gaussian (Sec. 3.1) are designed to be used for novel-view synthesis only. By augmenting 3D Gaussian with additional properties, such as linguistic [87]–[89], semantic/instance [90]–[92], and spatial-temporal [93] properties, 3D GS demonstrates its considerable potential to revolutionize various domains.

Here we list several interesting applications using 3D Gaussians with specially designed properties. i) Language Embedded Scene Representation [87]–[89]. Due to the high computational and memory demands of current language-embedded scene representations, Shi et al. [87] proposed a quantization scheme that augments 3D Gaussian with streamlined language embeddings instead of the original high-dimensional embeddings. This method also mitigated semantic ambiguity and enhanced the precision of open-vocabulary querying by smoothing out semantic features across different views, guided by uncertainty values. ii) Scene Understanding and Editing [90]–[92]. Feature 3DGS [90] integrated 3D GS with feature field distillation from 2D foundation models. By learning a lower-dimensional feature field and applying a lightweight convolutional decoder for upsampling, Feature 3DGS achieved faster training and rendering speeds while enabling high-quality feature field distillation, supporting applications like semantic segmentation and language-guided editing. iii) Spatiotemporal Modeling [93], [106]. To capture the complex spatial and temporal dynamics of 3D scenes, Yang et al. [93] conceptualized spacetime as a unified entity and approximates the spatiotemporal volume of dynamic scenes using a collection of 4D Gaussians. The proposed 4D Gaussian representation and corresponding rendering pipeline are capable of modeling arbitrary rotations in space and time and allow for end-to-end training.

### 4.6 Hybrid Representation

Rather than augmenting 3D Gaussian with additional properties, another promising avenue of adapting to downstream tasks is to introduce structured information (e.g., spatial MLPs and grids) tailored for specific applications.

Next we showcase various fascinating uses of 3D GS with specially devised structured information. i) Facial Expression Modeling. Considering the challenge of creating high-fidelity 3D head avatars under sparse view conditions, Gaussian Head Avatar [96] introduced controllable 3D Gaussians and an MLP-based deformation field. Concretely, it captured detailed facial expressions and dynamics by optimizing neutral 3D Gaussians alongside the deformation field, thus ensuring both detail fidelity and expression accuracy. ii) Spatiotemporal Modeling. Yang et al. [94] proposed to reconstruct dynamic scenes with deformable 3D Gaussians. The deformable 3D Gaussians are learned in a canonical space, coupled with a deformation field (i.e., a spatial MLP) that models the spatial-temporal dynamics. The proposed method also incorporated an annealing smoothing training mechanism to enhance temporal smoothness without additional computational costs. iii) Style Transfer. Saroha et al. [107] proposed GS in style, an advanced approach for real-time neural scene stylization. To maintain a cohesive stylized appearance across multiple views without compromising on rendering speed, they used pre-trained 3D Gaussians coupled with a multi-resolution hash grid and a small MLP to produce stylized views. In a nutshell, incorporating structured information can serve as a complementary part for adapting to tasks that are incompatible with the sparsity and disorder of 3D Gaussians.

### 4.7 New Rendering Algorithm for 3D Gaussians

While the rasterization-based pipeline of 3D GS offers impressive real-time performance, it still suffers from the inherent limitations, including inefficient handling of highly distorted cameras (crucial for robotics), secondary rays (for optical effects like reflections and shadows), and stochastic ray sampling (needed in various existing pipelines). In addition, the assumptions that Gaussians do not overlap and can be sorted accurately using only centers are often violated in practice, leading to temporal artifacts when camera movement changes sorting order.

Recent works [108]–[110] explored ray tracing based rendering algorithms as an alternative. For instance, GaussianTracer [108] introduced a new ray tracing implementation for Gaussian primitives, and devised several accelerating strategies according to the uneven density and interleaved nature of Gaussians. EVER [109] devised a physically accurate, constant density ellipsoid representation that allows for the exact computation of the volume rendering integral, rather than relying on somewhat satisfactory approximations. This advancement eliminates popping artifacts.

Thanks to the fundamental paradigm shift, several exciting possibilities might emerge, including advanced optical effects (reflection, refraction, shadows, global illumination, etc.), support for complex camera models (highly-distorted lenses, rolling shutter effects, etc.), physically accurate rendering with true directional appearance evaluation (vs. tile based approximation), and more. While these capabilities currently come with additional computational costs, they provide essential building blocks for future research in inverse rendering, physical material modeling, relighting, and complex scene reconstruction.

## 5 APPLICATION AREAS AND TASKS

Building on the rapid advancements in 3D GS, a wide range of innovative applications has emerged across multiple domains (Fig. 6) such as robotics (Sec. 5.1), dynamic scene reconstruction and representation (Sec. 5.2), generation and editing (Sec. 5.3), avatar (Sec. 5.4), medical systems (Sec. 5.5), large-scale scene reconstruction (Sec. 5.6), physics (Sec. 5.7), and even other scientific disciplines [24], [174]–[176]. Here, we highlight key examples that underscore the transformative impact and potential of 3D GS and offer a more comprehensive collection in Github.

Fig. 6. Typical applications benefited from GS (Sec. 5). Some images are borrowed from [132], [135], [146], [156], [166] and redrawn.

### 5.1 Robotics

The evolution of scene representation in robotics has been profoundly shaped by the emergence of NeRF, which revolutionized dense mapping and environmental interaction through implicit neural models. However, NeRF's computational cost poses a critical bottleneck for real-time robotic applications. The shift from implicit to explicit representation not only accelerates optimization but also unlocks direct access to spatial and structural scene data, making 3D GS a transformative tool for robotics. Its ability to balance high-fidelity reconstruction with computational efficiency positions 3D GS as a cornerstone for advancing robotic perception, manipulation, and navigation in dynamic, real-world environments.

The integration of GS into robotic systems has yielded significant advancements across three core domains. In SLAM, GS-based methods [111]–[117], [123], [124], [177]–[182] excel in real-time dense mapping but face inherent trade-offs. Visual SLAM frameworks, particularly RGBD variants [112], [114], [178], leverage depth supervision for geometric fidelity but falter in low-texture or motion-degraded environments. RGB-only approaches [113], [115], [183] circumvent depth sensors but grapple with scale ambiguity and drift. Multi-sensor fusion strategies, such as LiDAR integration [159], [177], [182], enhance robustness in unstructured settings at the cost of calibration complexity. Semantic SLAM [116], [117], [123] extends scene understanding through object-level semantics but struggles with scalability due to lighting sensitivity in color-based methods or computational overhead in feature-based methods. 3D GS based manipulation [118]–[122] bypasses the need for auxiliary pose estimation in NeRF-based methods, enabling rapid single-stage tasks like grasping in static environments via geometric and semantic attributes encoded in Gaussian properties. Multi-stage manipulation [118], [120], where environmental dynamics demand real-time map updates, requires explicit modeling of dynamic adjustments (e.g., object motions and interactions), material compliance, etc.

The advancement of 3D GS in robotics faces three pivotal challenges. First, adaptability in dynamic and unstructured environments remains critical: real-world scenes are rarely static, requiring systems to continuously update representations amid motion, occlusions, and sensor noise without sacrificing accuracy. Second, current semantic mapping methods rely on costly, scene-specific optimization processes, limiting generalizability and scalability for real-world deployment. Third, unlike NeRF based systems which can use MLP parameters as input features for downstream decision-making, 3D Gaussians' inherent lack of spatial order complicates feature aggregation, with no standardized framework yet established. Bridging the gap between high-fidelity reconstruction and actionable semantic/physical understanding will define the next frontier for 3D GS, moving beyond passive mapping towards embodied intelligence.

### 5.2 Dynamic Scene Reconstruction

Dynamic scene reconstruction refers to the process of capturing and representing the three-dimensional structure and appearance of a scene that changes over time [184]–[187]. This involves creating a digital model that accurately reflects the geometry, motion, and visual aspects of the objects in the scene as they evolve. Dynamic scene reconstruction is crucial in various applications, e.g., VR/AR, 3D animation, and autonomous driving [188]–[190].

The key to adapt 3D GS to dynamic scenes is the modeling of temporal dimension which allows for the representation of scenes that change over time. 3D GS based methods [93]–[95], [106], [125]–[130], [191]–[199] for dynamic scene reconstruction can generally be divided into two main categories as discussed in Sec. 4.5 and Sec. 4.6. The first category utilizes additional fields like spatial MLPs or grids to model deformation (Sec. 4.6). For example, Yang et al. [94] first proposed deformable 3D Gaussians tailored for dynamic scenes. These 3D Gaussians are learned in a canonical space and can be used to model spatial-temporal deformation with an implicit deformation field (implemented as an MLP). GaGS [132] devised the voxelization of a set of Gaussian distributions, followed by the use of sparse convolutions to extract geometry-aware features, which are then utilized for deformation learning. On the other hand, the second category is based on the idea that scene changes can be encoded into the 3D Gaussian representation with a specially designed rendering process (Sec. 4.5). For instance, Luiten et al. [125] introduced dynamic 3D Gaussians to model dynamic scenes by keeping the properties of 3D Gaussians unchanged over time while allowing their positions and orientations to change. Yang et al. [93] designed a 4D Gaussian representation, where additional properties are used to represent 4D rotations and spherical harmonic, to approximate the spatial-temporal volume of scenes.

While 3D GS advances dynamic scene reconstruction by modeling per-Gaussian deformations, its reliance on fine-grained primitives limits scalability and robustness. Current methods struggle to balance computational efficiency and precision: small-scale reconstructions unify dynamic and static elements but become intractable in large environments, often requiring manual priors to segment regions—a barrier in unstructured settings. Furthermore, the absence of object-level motion reasoning leads to artifacts and poor generalization over long sequences. Future work might prioritize object-centric frameworks that hierarchically group Gaussians into persistent entities, enabling efficient large-scale reconstruction through inherent motion disentanglement (dynamic vs. static).

### 5.3 Generation and Editing

Content generation and editing represent two fundamental and inherently interconnected capabilities in modern AI systems. While generation enables the synthesis of novel digital content from scratch or conditional inputs [200]–[202], editing provides the crucial ability to refine, adapt, and manipulate existing content with precise control [203]. Together, these capabilities revolutionize creative workflows by combining initial content creation with iterative refinement, enabling applications from professional content production to interactive consumer tools.

Recent advances in generation [133]–[138], [204]–[227] have led to the emergence of three main approaches. Optimization based methods [133], [134], [204] distill diffusion priors (gradients) to guide 3D model updates with the score functions. While these methods demonstrate impressive fidelity, they face significant computational overhead due to the necessity of comparing multiple viewpoints during the optimization process. Reconstruction based methods [135], [225], [227] reframe the generation problem as a multiview reconstruction task utilizing pre-trained multi-view diffusion models. Although this approach offers an intuitive and straightforward solution, it grapples with fundamental limitations in maintaining view consistency. The lack of strict geometric constraints across different viewpoints often results in inconsistent surface geometry and degraded texture quality, particularly in regions with complex visual features. Direct 3D generation methods train diffusion models on 3D representations [138], [220], [226]. While the learned 3D diffusion models facilitate multi-view consistency, the demanding computational costs impede the expansion of training scales necessary for improved generative diversity.

Current editing works [90]–[92], [126]–[128], [140]–[143], [228]–[239] fall into two primary classes. The first class leverages 2D image-editing models (e.g., diffusion-based editors) to iteratively refine 3D Gaussians. Early efforts [141], [142], [233] adopt optimization- or reconstruction-based strategies akin to methods in generation, but introduce task-specific control signals. However, naively applying 2D edits independently across views often introduces multi-view inconsistencies. Subsequent works [140], [238]–[240] mitigate this through iterative refinement or cross-view attention, albeit at increased computational costs for alignment. A notable challenge is unintended object deformations, attributed to the weak 3D geometric priors in 2D editing models and the difficulty of reconciling 2D edits with underlying 3D structures. The second class exploits the explicit nature of 3D GS to enable direct manipulation based on embedded properties such as semantics [91], [92], [143], [232] and key points [128]. However, this class remains underexplored due to essential challenges: the lack of inherent ordering of Gaussians complicates the design of efficient indexing schemes, while editing attributes (e.g., texture and geometry) requires careful regularization and alignment to preserve plausibility.

### 5.4 Avatar

Avatars, the digital representations of users in virtual spaces, bridge physical and digital realms, enabling immersive interaction, identity expression, and remote collaboration. Spanning entertainment (gaming, virtual influencers), enterprise (AI agents, virtual meetings), healthcare, and education, they underpin metaverse economies. Advances in AR and VR amplify their role in redefining social, industrial, and creative landscapes.

3D GS has emerged as a powerful tool for human avatar reconstruction, primarily advancing along two directions: full-body modeling and head-centric modeling. For full-body avatars [139], [144]–[147], [241]–[252], the current methods typically anchor 3D Gaussians in a canonical space and deform them via parametric body models (e.g., SMPL) or cage-based rigging to model dynamic motions. These approaches adopt a hybrid deformation strategy: linear blend skinning handles rigid skeletal transformations such as joint rotations, while pose-conditioned deformation fields account for secondary non-rigid effects like muscle jiggles. For head avatars [23], [148]–[151], [253]–[256], the emphasis shifts to modeling intricate facial expressions, fine-grained geometry (e.g., wrinkles, hair [257]), and dynamic speech-driven animations. Techniques mainly combine parametric morphable face models (e.g., FLAME) with deformable 3D Gaussians, employing diffusion strategies and expression-aware deformation fields to disentangle rigid head poses from non-rigid facial movements. Both directions exploit the speed advantage and editability of 3D GS to enable efficient training, real-time rendering, and precise control over deformations, while addressing challenges in cross-frame correspondence, topology flexibility, and multi-view consistency.

Reconstruction in challenging scenes (e.g., occlusions, sparse single-view inputs, or loose clothing) and enhancing avatar interactivity represent critical challenges and opportunities. Parametric model-free methods, which bypass predefined priors by learning skinning weights directly from data, show promise for such scenarios. Complementary to this, generative models can mitigate ambiguities inherent in underconstrained settings. Further integrating physics-based constraints might bridge the gap between static reconstructions and responsive, lifelike interactions, unlocking applications in AR, embodied AI, etc.

### 5.5 Endoscopic Scene Reconstruction

Surgical 3D reconstruction represents a fundamental task in robot-assisted minimally invasive surgery, aimed at enhancing intraoperative navigation, preoperative planning, and educational simulations through precise modeling of dynamic surgical scenes. Pioneering the integration of dynamic radiance fields into this domain, recent advancements have focused on surmounting the inherent challenges of single-viewpoint video reconstructions such as occlusions by surgical instruments and sparse viewpoint diversity within the confined spaces of endoscopic exploration [258]–[260]. Despite the progress, the call for high fidelity in tissue deformability and topological variation remains, coupled with the pressing demand for faster rendering to bridge the utility in applications sensitive to latency [152]–[154]. This synthesis of immediacy and precision in reconstructing deformable tissues from endoscopic videos is essential in propelling robotic surgery towards reduced patient trauma and AR/VR applications, ultimately fostering a more intuitive surgical environment and nurturing the future of surgical automation and robotic proficiency.

Endoscopic scene reconstruction introduces distinct challenges compared to general dynamic scenes, including sparse training data from limited camera mobility in narrow cavities, frequent tool occlusions obscuring critical regions, and single-view geometry ambiguities. Existing approaches mainly used additional depth guidance to infer the geometry of tissues [152]–[154]. For instance, EndoGS [154] integrated depth-guided supervision with spatial-temporal weight masks and surface-aligned regularization terms to enhance the quality and speed of 3D tissue rendering while addressing tool occlusion. EndoGaussian [153] introduced two new strategies: holistic Gaussian initialization for dense initialization and spatiotemporal Gaussian tracking for modeling surface dynamics. Zhao et al. [155] argued that these methods suffer from under-reconstruction and proposed to alleviate this problem from frequency perspectives. In addition, EndoGSLAM [156] and Gaussian Pancake [157] devised SLAM systems for endoscopic scenes and showed significant speed advantages.

Advancing endoscopic 3D reconstruction requires targeted efforts in both data and dynamics modeling. Data limitations arise from single-viewpoint videos, which produce ill-posed reconstruction problems due to instrument occlusions and constrained camera mobility, leaving critical tissue regions unobserved. While depth estimators provide temporary workarounds, integrating multi-view camera systems addresses the root cause. In addition, existing datasets often feature truncated sequences (e.g., \(4\sim8s\) in EndoNeRF [258]), which fail to capture prolonged tissue deformation dynamics or complex surgical workflows. Extending temporal coverage to include longer, clinically representative sequences would benefit downstream applications as aforementioned. Modeling limitations persist in current methods, which often represent tissue dynamics at the Gaussian level rather than object- or 3D region-level. This reduces their capacity to encode semantically meaningful anatomical interactions and deserves further explorations.

### 5.6 Large-scale Scene Reconstruction

Large-scale scene reconstruction is a critical component in fields such as autonomous driving, aerial surveying, and AR/VR, demanding both photorealistic visual quality and real-time rendering capabilities. Before the emergence of 3D GS, the task has been approached using NeRF based methods, which, while effective for smaller scenes, often fall short in detail and rendering speed when scaled to larger areas (e.g., over \(1.5km^2\)). Though 3D GS has demonstrated considerable advantages over NeRFs, the direct application of 3D GS to large-scale environments introduces significant challenges. 3D GS requires an immense number of Gaussians to maintain visual quality over extensive areas, leading to prohibitive GPU memory demands and considerable computational burdens during rendering. For instance, a scene spanning \(2.7km^2\) may require over 20 million Gaussians, pushing the limits of even the most advanced hardware (e.g., NVIDIA A100 with 40GB memory) [163].

To address the highlighted challenges, researchers have made significant strides in two key areas: i) For training, a divide-and-conquer strategy [162]–[165] has been adopted, which segments a large scene into multiple, independent cells. This facilitates parallel optimization for expansive environments. With the same spirit, Zhao et al. [161] proposed a distributed implementation of 3D GS training. An additional challenge lies in maintaining visual quality, as large-scale scenes often feature textureless surfaces that can hamper the effectiveness of optimization such as Gaussian initialization and density control (Sec. 3.2). Enhancing the optimization algorithm presents a viable solution to mitigate this issue [44], [164]. ii) Regarding rendering, the adoption of the Level of Details (LoD) technique from computer graphics has proven instrumental. LoD adjusts the complexity of 3D scenes to balance visual quality with computational efficiency. Current implementations involve feeding only the essential Gaussians to the rasterizer [164], or designing explicit LoD structures like the Octree [165] and hierarchy [162]. Furthermore, integrating extra input modalities like LiDAR can further enhanced the reconstruction process [158]–[160].

One prominent challenge in large-scale scene reconstruction lies in handling sparse or incomplete capture data, which can be mitigated through few-shot adaptation schemes (see Sec. 4.1) or generalizable priors (see "learning physical priors from large-scale data" in Sec. 7). Meanwhile, memory and computational bottlenecks can be addressed via distributed learning strategies [161], such as parameter partitioning across GPU clusters and parallel batched multi-view optimization.

### 5.7 Physics

The simulation of complex real-world dynamics, such as seed dispersal or fluid motion, is pivotal for applications spanning virtual reality, animation, and scientific modeling, where realism hinges on accurate physical behavior. Advances in video diffusion models have driven progress in 4D content generation, yet these methods might produce visually plausible results that violate fundamental physical laws. 3D GS emerges as a promising solution by embedding physical constraints and properties into scene representations, enabling both visually convincing and physically coherent simulations.

Existing methods differ in how they formulate and integrate physics-based priors into their frameworks. The most common approach is employing physics simulation engines (e.g., MLS-MPM [268]) to guide the dynamics generation. The material point method [268] and position based dynamics [269] — numerical methods used in computer graphics for simulating deformations in materials like fluids, granular media, and fracturing solids — have been extensively explored by the community through various customizations [21], [143], [166]–[171]. Analytical material models, such as mass-spring systems, have also demonstrated success in approximating deformations by explicitly encoding material properties into 3D Gaussians [172]. Across these methods, 3D Gaussians are treated as discrete particles (with one exception [173] using a continuous representation) and serve as computational units within the chosen simulator. Unknown material properties or physical parameters are typically learned through video-based supervision from conditional generative models.

Despite advancements in physics based 3D GS frameworks, critical limitations persist. Current systems struggle to unify diverse physical behaviors (e.g., rigid, elastic, or soft-body dynamics) into cohesive simulations, handle complex multi-object interactions without manual intervention, and model scene-level interactions such as environmental feedback and dynamic lighting changes. Integrating adaptive physics engines capable of multi-object and multi-material interactions, developing new simulation architectures that are compatible with priors learned from large-scale data, and expanding datasets to encompass diverse materials and dynamic scenarios are equally vital.

## 6 PERFORMANCE COMPARISON

In this section, we provide more empirical evidence by presenting the performance of several 3D GS algorithms that we previously discussed. The diverse applications of 3D GS across numerous tasks, coupled with the custom-tailored algorithmic designs for each task, render a uniform comparison of all 3D GS algorithms across a single task or dataset impracticable. For comprehensiveness, we provide a collection of representative datasets in Table 2 according to our analysis in Sec. 5. Due to the limited space, we have chosen several representative tasks for an in-depth performance evaluation. The performance scores are primarily sourced from the original papers, except where indicated otherwise. We also maintain a Github repository for this section.

### 6.1 Performance Benchmarking: Localization

The localization task in SLAM involves determining the precise position and orientation of a robot or device within an environment, typically using sensor data.

**Dataset:** Replica [261] dataset is a collection of 18 highly detailed 3D indoor scenes. These scenes are not only visually realistic but also offer comprehensive data including dense meshes, high-quality HDR textures, and detailed semantic information for each element. Following [262], three sequences about rooms and five sequences about offices are used for the evaluation.

**Benchmarking Algorithms:** For performance comparison, we involve four recent 3D GS based algorithms [111]–[114] and six typical SLAM methods [262]–[267].

**Evaluation Metric:** The root mean square error (RMSE) of the absolute trajectory error (ATE) is a commonly used metric in evaluating SLAM systems [275], which measures the root mean square of the Euclidean distances between the estimated and true positions over the entire trajectory.

**Result:** As shown in Table 1, the recent 3D Gaussians based localization algorithms have a clear advantage over existing NeRF based dense visual SLAM. For example, SplaTAM [112] achieves a trajectory error improvement of \(\sim50\%\), decreasing it from \(0.52\mathrm{cm}\) to \(0.36\mathrm{cm}\) compared to the previous state-of-the-art (SOTA) [266]. We attribute this to the dense and accurate 3D Gaussians reconstructed for scenes, which can handle the noise of real sensors. This reveals that effective scene representations can improve the accuracy of localization tasks.

**TABLE 1** Comparison of localization methods (\(\S6.1\)) on Replica [261] (static scenes), in terms of absolute trajectory error (ATE, cm). (The three best scores are marked in red, blue, and green, respectively. These notes also apply to the other tables.)

| Method                      |  GS | Room0 | Room1 | Room2 | Office0 | Office1 | Office2 | Office3 | Office4 | Average |
| --------------------------- | --: | ----: | ----: | ----: | ------: | ------: | ------: | ------: | ------: | ------: |
| iMAP [262] (ICCV21)         |     |  3.12 |  2.54 |  2.31 |    1.69 |    1.03 |    3.99 |    4.05 |    1.93 |    2.58 |
| Vox-Fusion [263] (ISMAR22)  |     |  1.37 |  4.70 |  1.47 |    8.48 |    2.04 |    2.58 |    1.11 |    2.94 |    3.09 |
| NICE-SLAM [264] (CVPR22)    |     |  0.97 |  1.31 |  1.07 |    0.88 |    1.00 |    1.06 |    1.10 |    1.13 |    1.06 |
| ESLAM [265] (CVPR23)        |     |  0.71 |  0.70 |  0.52 |    0.57 |    0.55 |    0.58 |    0.72 |    0.63 |    0.63 |
| Point-SLAM [266] (ICCV23)   |     |  0.61 |  0.41 |  0.37 |    0.38 |    0.48 |    0.54 |    0.69 |    0.72 |    0.52 |
| Co-SLAM [267] (CVPR23)      |     |  0.70 |  0.95 |  1.35 |    0.59 |    0.55 |    2.03 |    1.56 |    0.72 |    1.00 |
| Gaussian-SLAM [114] (arXiv) |   ✓ |  3.35 |  8.74 |  3.13 |    1.11 |    0.81 |    0.78 |    1.08 |    7.21 |    3.27 |
| GSSLAM [113] (CVPR24)       |   ✓ |  0.47 |  0.43 |  0.31 |    0.70 |    0.57 |    0.31 |    0.31 |    3.20 |    0.79 |
| GS-SLAM [111] (CVPR24)      |   ✓ |  0.48 |  0.53 |  0.33 |    0.52 |    0.41 |    0.59 |    0.46 |    0.70 |    0.50 |
| SplaTAM [112] (CVPR24)      |   ✓ |  0.31 |  0.40 |  0.29 |    0.47 |    0.27 |    0.29 |    0.32 |    0.55 |    0.36 |

**TABLE 2** Collection of representative datasets for 3D GS. Here PC represents point clouds.

| Name                   | Type      | # Sample        | Task                         |
| ---------------------- | --------- | --------------- | ---------------------------- |
| Tanks&Temples [270]    | RGB       | 14              | Novel View Synthesis         |
| RealEstate10K [271]    | RGB       | 1,000           | Novel View Synthesis         |
| DeepBlending [272]     | RGB       | 19              | Novel View Synthesis         |
| LLFF [273]             | RGB       | 8               | Novel View Synthesis         |
| NeRF [12]              | RGB       | 8               | Novel View Synthesis         |
| ACID [274]             | RGB       | 700+            | Novel View Synthesis         |
| Mip-NeRF 360 [8]       | RGB       | 9               | Novel View Synthesis         |
| TUM RGB-D [275]        | RGB-D     | 39              | Robotics                     |
| KITTI [276]            | RGB-D&PC  | 11              | Robotics                     |
| ScanNet [277]          | RGB-D     | 1,513           | Robotics                     |
| Replica [261]          | RGB-D     | 18              | Robotics                     |
| Waymo [278]            | RGB-D&PC  | 1,150           | Robotics                     |
| nuScenes [279]         | RGB-D&PC  | 1,000           | Robotics                     |
| RLBench [280]          | RGB       | 100             | Robotics                     |
| Robomimic [281]        | RGB       | 800             | Robotics                     |
| D-NeRF [184]           | RGB       | 8               | Dynamic Scene Reconstruction |
| HyperNeRF [185]        | RGB       | 6               | Dynamic Scene Reconstruction |
| NeRF-DS [282]          | RGB       | 8               | Dynamic Scene Reconstruction |
| CoNeRF [283]           | RGB       | 7               | Generation and Editing       |
| SPI-NeRF [284]         | RGB       | 10              | Generation and Editing       |
| Tensor4D [285]         | RGB       | 4               | Generation and Editing       |
| OmniObject3D [286]     | 3D Object | 3D Object 6,000 | Generation and Editing       |
| Objaverse [287]        | 3D Object | 3D Object 800K+ | Generation and Editing       |
| People-Snapshot [288]  | RGB       | 24              | Avatar                       |
| VOCASET [289]          | RGB       | 12              | Avatar                       |
| THUman [290]           | RGB       | 200             | Avatar                       |
| THUman2.0 [291]        | RGB-D     | 500             | Avatar                       |
| ZJU-Mocap [292]        | RGB       | 9               | Avatar                       |
| H3DS [293]             | RGB       | 23              | Avatar                       |
| THUman3.0 [294]        | 3D Scan   | 22              | Avatar                       |
| SCARED [295]           | RGB-D     | 9               | Medical                      |
| EndoNeRF [298]         | RGB       | 2               | Medical                      |
| X3D [296]              | X-ray     | 15              | Medical                      |
| CityNeRF [297]         | RGB       | 12              | Large-scale Reconstruction   |
| Waymo Block-NeRF [298] | RGB&PC    | 1               | Large-scale Reconstruction   |
| UrbanBIS [299]         | RGB&PC    | 6               | Large-scale Reconstruction   |
| GauU-Scene [160]       | RGB&PC    | 1               | Large-scale Reconstruction   |

### 6.2 Performance Benchmarking: Static Scenes

Rendering focuses on transforming computer-readable information (e.g., 3D objects in the scene) to pixel-based images. This section focuses on evaluating the quality of rendering results in static scenes.

**Dataset:** The same dataset as in Sec. 6.1, i.e., Replica [261], is used for comparison. The testing views are the same as those collected by [262].

**TABLE 3** Comparison of mapping methods (§6.2) on Replica [261] (static scenes), in terms of PSNR, SSIM, and LPIPS. The results for FPS are taken from [113] using one 4090 GPU.

| Method                      |  GS | Metric | Room0 | Room1 | Room2 | Office0 | Office1 | Office2 | Office3 | Office4 | Average |  FPS |
| --------------------------- | --: | ------ | ----: | ----: | ----: | ------: | ------: | ------: | ------: | ------: | ------: | ---: |
| NICE-SLAM [264] (CVPR22)    |     | PSNR↑  | 22.12 | 22.47 | 24.52 |   29.07 |   30.34 |   19.66 |   22.23 |   24.94 |   24.42 | 0.54 |
|                             |     | SSIM↑  |  0.69 |  0.76 |  0.81 |    0.87 |    0.89 |    0.80 |    0.80 |    0.86 |    0.81 |      |
|                             |     | LPIPS↓ |  0.33 |  0.27 |  0.21 |    0.23 |    0.18 |    0.23 |    0.21 |    0.20 |    0.23 |      |
| Vox-Fusion [263] (ISMAR22)  |     | PSNR↑  | 22.39 | 22.36 | 23.92 |   27.79 |   29.83 |   20.33 |   23.47 |   25.21 |   24.41 | 2.17 |
|                             |     | SSIM↑  |  0.68 |  0.75 |  0.80 |    0.86 |    0.88 |    0.79 |    0.80 |    0.85 |    0.80 |      |
|                             |     | LPIPS↓ |  0.30 |  0.27 |  0.23 |    0.24 |    0.18 |    0.24 |    0.21 |    0.20 |    0.24 |      |
| Point-SLAM [266] (ICCV23)   |     | PSNR↑  | 32.40 | 34.08 | 35.50 |   38.26 |   39.16 |   33.99 |   33.48 |   33.49 |   35.17 | 1.33 |
|                             |     | SSIM↑  |  0.97 |  0.98 |  0.98 |    0.98 |    0.99 |    0.96 |    0.96 |    0.98 |    0.97 |      |
|                             |     | LPIPS↓ |  0.11 |  0.12 |  0.11 |    0.10 |    0.12 |    0.16 |    0.13 |    0.14 |    0.12 |      |
| SplaTAM [112] (CVPR24)      |   ✓ | PSNR↑  | 32.86 | 33.89 | 35.25 |   38.26 |   39.17 |   31.97 |   29.70 |   31.81 |   34.11 |    - |
|                             |     | SSIM↑  |  0.98 |  0.97 |  0.98 |    0.98 |    0.98 |    0.97 |    0.95 |    0.95 |    0.97 |      |
|                             |     | LPIPS↓ |  0.07 |  0.10 |  0.08 |    0.09 |    0.09 |    0.10 |    0.12 |    0.15 |    0.10 |      |
| GS-SLAM [111] (CVPR24)      |   ✓ | PSNR↑  | 31.56 | 32.86 | 32.59 |   38.70 |   41.17 |   32.36 |   32.03 |   32.92 |   34.27 |    - |
|                             |     | SSIM↑  |  0.97 |  0.97 |  0.97 |    0.99 |    0.99 |    0.98 |    0.97 |    0.97 |    0.97 |      |
|                             |     | LPIPS↓ |  0.09 |  0.07 |  0.09 |    0.05 |    0.03 |    0.09 |    0.11 |    0.11 |    0.08 |      |
| GSSLAM [113] (CVPR24)       |   ✓ | PSNR↑  | 34.83 | 36.43 | 37.49 |   39.95 |   42.09 |   36.24 |   36.70 |   36.07 |   37.50 |  769 |
|                             |     | SSIM↑  |  0.95 |  0.96 |  0.96 |    0.97 |    0.98 |    0.96 |    0.96 |    0.96 |    0.96 |      |
|                             |     | LPIPS↓ |  0.07 |  0.08 |  0.07 |    0.07 |    0.06 |    0.08 |    0.07 |    0.10 |    0.07 |      |
| Gaussian-SLAM [114] (arXiv) |   ✓ | PSNR↑  | 34.31 | 37.28 | 38.18 |   43.97 |   43.56 |   37.39 |   36.48 |   40.19 |   38.90 |    - |
|                             |     | SSIM↑  |  0.99 |  0.99 |  0.99 |    1.00 |    0.99 |    0.99 |    0.99 |    1.00 |    0.99 |      |
|                             |     | LPIPS↓ |  0.08 |  0.07 |  0.07 |    0.04 |    0.07 |    0.08 |    0.08 |    0.07 |    0.07 |      |

### 6.3 Performance Benchmarking: Dynamic Scenes

This section focuses on evaluating the rendering quality in dynamic scenes.

**Dataset:** D-NeRF [184] dataset includes videos with 50 to 200 frames each, captured from unique viewpoints. It features synthetic, animated objects in complex scenes, with non-Lambertian materials. The dataset provides 50 to 200 training images and 20 test images per scene, designed for evaluating models in the monocular setting. The testing views are the same as the original paper [184].

**Benchmarking Algorithms:** For performance comparison, we involve five recent papers that model dynamic scenes with 3D GS [93]–[95], [126], [132], as well as six NeRF based approaches [37], [184], [187], [302]–[304].

**Evaluation Metric:** The same metrics as in Sec. 6.2, i.e., PSNR, SSIM [300], and LPIPS [301], are used for evaluation.

**Result:** From Table 4 we can observe that 3D GS based methods outperform existing SOTAs by a clear margin. The static version of 3D GS [10] fails to reconstruct dynamic scenes, resulting in a sharp drop in performance. By modeling the dynamics, D-3DGS [94] outperforms the SOTA method, FFDNeRF [187], by 6.83dB in terms of PSNR. These results indicate the effectiveness of introducing additional properties or structured information to model the deformation of Gaussians so as to model the scene dynamics.

**TABLE 4** Comparison of reconstruction methods (§6.3) on D-NeRF [184] (dynamic scenes), in terms of PSNR, SSIM, and LPIPS. \* denotes results reported in [95].

| Method                       | GS  | PSNR↑ | SSIM↑ | LPIPS↓ |
| ---------------------------- | --- | ----: | ----: | -----: |
| D-NeRF [184] (CVPR21)        |     | 30.50 |  0.95 |   0.07 |
| TiNeuVox-B [302] (ISCA22)    |     | 32.67 |  0.97 |   0.04 |
| KPlanes [37] (CVPR23)        |     | 31.61 |  0.97 |      - |
| HexPlane-Slim [303] (CVPR23) |     | 32.68 |  0.97 |   0.02 |
| FFDNeRF [187] (ICCV23)       |     | 32.68 |  0.97 |   0.02 |
| MSTH [304] (NeurIPS23)       |     | 31.34 |  0.98 |   0.02 |
| 3D GS\* [10] (TOC23)         | ✓   | 23.19 |  0.93 |   0.08 |
| 4DGS [93] (ICLR24)           | ✓   | 34.09 |  0.98 |      - |
| D-GS [95] (CVPR24)           | ✓   | 34.05 |  0.98 |   0.02 |
| GaGS [132] (CVPR24)          | ✓   | 37.36 |  0.99 |   0.01 |
| CoGS [126] (CVPR24)          | ✓   | 37.90 |  0.98 |   0.02 |
| D-3DGS [94] (CVPR24)         | ✓   | 39.51 |  0.99 |   0.01 |

### 6.4 Performance Benchmarking: Human Avatar

Human avatar modeling aims to create the model of human avatars from a given multi-view video.

**Dataset:** ZJU-MoCap [292] is a prevalent benchmark in human modeling from videos, captured with 23 synchronized cameras at a \(1024\times1024\) resolution. Six subjects (i.e., 377, 386, 387, 392, 393, and 394) are used for evaluation [305]. The same testing views following [306] are adopted.

**Benchmarking Algorithms:** For performance comparison, we involve three recent papers which model human avatar with 3D GS [145], [146], [249], as well as six human rendering approaches [292], [305]–[309].

**Evaluation Metric:** PSNR, SSIM [300], and LPIPS* [301] are used for measuring RGB rendering performance. Here LPIPS* equals to LPIPS \(\times1000\).

**TABLE 5** Comparison of reconstruction methods (§6.4) on ZJU-MoCap [292] (avatar), in terms of PSNR, SSIM, and LPIPS. The results for non-GS methods are taken from [146].

| Method                     | GS  | PSNR↑ | SSIM↑ | LPIPS\*↓ |
| -------------------------- | --- | ----: | ----: | -------: |
| NeuralBody [292] [CVPR32]  |     | 29.03 |  0.96 |    42.47 |
| AnimNeRF [307] [ICCV21]    |     | 29.77 |  0.96 |    46.89 |
| PixelNeRF [308] [ICCV21]   |     | 24.71 |  0.89 |   121.86 |
| NHP [309] [NeurIPS21]      |     | 28.25 |  0.95 |    64.77 |
| HumanNeRF [305] [CVPR22]   |     | 30.66 |  0.97 |    33.38 |
| Instant-NVR [306] [CVPR23] |     | 31.01 |  0.97 |    38.45 |
| GauHuman [145] [CVPR24]    | ✓   | 31.34 |  0.97 |    30.51 |
| 3DGS-Avatar [249] [CVPR24] | ✓   | 30.61 |  0.97 |    29.58 |
| GART [146] [CVPR24]        | ✓   | 32.22 |  0.98 |    29.21 |

### 6.5 Performance Benchmarking: Surgical Scenes

3D reconstruction from endoscopic video is critical to robotic-assisted minimally invasive surgery, enabling pre-operative planning, training through AR/VR simulations, and intraoperative guidance.

**Dataset:** EndoNeRF [258] dataset presents a specialized collection of stereo camera captures, comprising two samples of in-vivo prostatectomy. It is tailored to represent real-world surgical complexities, including challenging scenes with tool occlusion and pronounced non-rigid deformation. The same testing views as in [260] are used.

**Benchmarking Algorithms:** For performance comparison, we involve three recent papers which reconstruct dynamic 3D endoscopic scenes with GS [152], [153], [155], as well as three NeRF-based surgical reconstruction approaches [258]–[260].

**Evaluation Metric:** PSNR, SSIM [300], and LPIPS [301] are adopted for evaluation. In addition, the requirement for GPU memory is also reported.

**Result:** Table 6 shows that introducing the explicit representation of 3D Gaussians leads to several significant improvements. For instance, EndoGaussian [153] outperforms a strong baseline, LerPlane-32k [259], among all metrics. In particular, EndoGaussian demonstrates an approximate 224-fold increase in speed while consumes just 10% of the GPU resources. These impressive results attest to the efficiency of GS-based methods, which not only expedite processing but also minimize GPU load, thus easing the demands on hardware. Such attributes are vitally significant for real-world surgical application deployment, where optimized resource usage can be a key determinant of practical utility.

**TABLE 6** Comparison of reconstruction methods (§6.5) on EndoNeRF [258] (surgical scenes), in terms of PSNR, SSIM, and LPIPS. The results for non-GS methods are taken from [153]. FPS and GPU usage for training (Mem.) are measured using one 4090 GPU [153].

| Method                        | GS  | PSNR↑ | SSIM↑ | LPIPS↓ |   FPS↑ | Mem.↓ |
| ----------------------------- | --- | ----: | ----: | -----: | -----: | ----: |
| EndoNeRF [258] [MICCAI22]     |     | 36.06 |  0.93 |   0.09 |   0.04 |  19GB |
| EndoSurf [260] [MICCAI23]     |     | 36.53 |  0.95 |   0.07 |   0.04 |  17GB |
| LerPlane-9k [259] [MICCAI23]  |     | 35.00 |  0.93 |   0.08 |   0.91 |  20GB |
| LerPlane-32k [259] [MICCAI23] |     | 37.38 |  0.95 |   0.05 |   0.87 |  20GB |
| Endo-4DGS [152] [MICCAI24]    | ✓   | 37.00 |  0.96 |   0.05 |      - |   4GB |
| EndoGaussian [153] [arXiv]    | ✓   | 37.85 |  0.96 |   0.05 | 195.09 |   2GB |
| HFGS [155] [BMVC24]           | ✓   | 38.14 |  0.97 |   0.03 |      - |     - |

## 7 FUTURE RESEARCH DIRECTIONS

As impressive as those follow-ups work on 3D GS are, and as much as those fields have been or might be revolutionized by 3D GS, there is a general agreement that 3D GS still has considerable room for improvement.

- **Physics- and Semantics-aware Scene Representation.** As a new, explicit scene representation technique, 3D Gaussian offers transformative potential beyond merely enhancing novel-view synthesis. It has the potential to pave the way for simultaneous advancements in scene reconstruction and understanding by devising physics- and semantics-aware 3D GS systems. While significant progress has been made in physics (Sec. 5.7) and semantics [310]–[315] individually, there remains considerable untapped potential in their synergistic integration. This is poised to revolutionize a range of fields and downstream applications. For instance, incorporating prior knowledge such as the general shape of objects can reduce the need for extensive training viewpoints [47], [48] while improving geometry/surface reconstruction [77], [316]. A critical metric for assessing scene representation is the quality of its generated scenes, which encompasses challenges in geometry, texture, and lighting fidelity [66], [128], [141]. By merging physical principles and semantic information within the 3D GS framework, one can expect that the quality will be enhanced, thereby facilitating dynamics modeling [21], [166], editing [90], [92], generation [133], [134], and beyond. In a nutshell, pursuing this advanced and versatile scene representation opens up new possibilities for innovation in computational creativity and practical applications across diverse domains.

- **Learning Physical Priors from Large-scale Data.** As we explore the potential of physics- and semantics-aware scene representations, leveraging large-scale datasets to learn generalizable, physical priors emerges as a promising direction. The goal is to model the inherent physical properties and dynamics embedded within real-world data, transforming them into actionable insights that can be applied across various domains such as robotics and visual effects. Establishing a learning framework for extracting these generalizable priors enables the application of these insights to specific tasks in a few-shot manner. For instance, it allows for rapid adaptation to new objects and environments with minimal data input. Furthermore, integrating physical priors can enhance not only the accuracy and quality of generated scenes but also their interactive and dynamic qualities. This is particularly valuable in AR/VR environments, where users interact with virtual objects that behave in ways consistent with their real-world counterparts. However, the existing body of work on capturing and distilling physics-based knowledge from extensive 2D and 3D datasets remains sparse. Notable efforts in related area include the continuum mechanics based GS systems (Sec. 5.7), and the generalizable Gaussian representation based on multi-view stereo [317].

- **Modeling Internal Structures of Objects with 3D GS.** Despite the ability of 3D GS to produce highly photorealistic renderings, modeling internal structures of objects (e.g., for a scanned object in computed tomography) within the current GS framework presents a notable challenge. Due to the splatting and density control process, the current representation of 3D Gaussian is unorganized and cannot align well with the object's actual internal structures. Moreover, there is a strong preference in various applications to depict objects as volumes (e.g., computed tomography). However, the disordered nature of 3D GS makes volume modeling particularly difficult. Li et al. [318] used 3D Gaussians with density control as the basis for the volumetric representation and did not involve the splatting process. X-Gaussian [319] involves the splatting process for fast training and inference but cannot generate volumetric representation. Using 3D GS to model the internal structures of objects remains unanswered and deserves further exploration.

- **3D GS for Simulation in Autonomous Driving and beyond.** Collecting real-world datasets for autonomous driving is both expensive and logistically challenging, yet crucial for training effective image-based perception systems. To mitigate these issues, simulation emerges as a cost-effective alternative, enabling the generation of synthetic datasets across diverse environments. However, the development of simulators capable of producing photorealistic and diverse synthetic data is fraught with challenges. These include achieving a high level of quality, accommodating various control methods, and accurately simulating a range of lighting conditions. While early efforts [188]–[190] in reconstructing urban/street scenes with 3D GS have been encouraging, they are just the tip of the iceberg in terms of the full capabilities. There remain numerous critical aspects to be explored, such as the integration of user-defined object models, the modeling of physics-aware scene changes (e.g., the rotation of vehicle wheels), and the enhancement of controllability and quality (e.g., in varying lighting conditions). Mastery of these capabilities would not only advance autonomous systems but also redefine computational understanding of physical spaces - a leap with implications for world models, spatial intelligence, embodied AI, and beyond.

- **Empowering 3D GS with More Possibilities.** Despite the significant potential of 3D GS, the full scope of applications for 3D GS remains largely untapped. A promising avenue for exploration involves augmenting 3D Gaussians with additional attributes (e.g., linguistic and spatiotemporal properties as mentioned in Sec. 4.5) and introducing structured information (e.g., spatial MLPs and grids as mentioned in Sec. 4.6), tailored for specific applications. Moreover, recent studies have begun to unveil the capability of 3D GS in several domains, e.g., point cloud registration [320], image representation and compression [60], and fluid synthesis [171]. These findings highlight a significant opportunity for interdisciplinary scholars to explore 3D GS further.

## 8 CONCLUSIONS

To the best of our knowledge, this survey presents the first comprehensive overview of 3D GS, a groundbreaking technique revolutionizing explicit radiance fields, computer graphics, and computer vision. It delineates the paradigm shift from traditional NeRF based methods, spotlighting the advantages of 3D GS in real-time rendering and enhanced editability. Our in-depth analysis and extensive quantitative studies demonstrate the superiority of 3D GS in practical applications, particularly those highly sensitive to latency. We offer insights into principles, prospective research directions, and the unresolved challenges within this domain. Overall, 3D GS stands as a transformative technology, poised to significantly influence future advancements in 3D reconstruction and representation. This survey is intended to serve as a foundational resource, propelling further exploration and progress in this rapidly evolving field.

## References

[1] S. J. Gortler, R. Grzeszczuk, R. Szeliski, and M. F. Cohen, “The lumigraph,” in Seminal Graphics Papers: Pushing the Boundaries, Volume 2, 2023, pp. 453–464.

[2] M. Levoy and P. Hanrahan, “Light field rendering,” in Seminal Graphics Papers: Pushing the Boundaries, Volume 2, 2023, pp. 441–452.

[3] C. Buehler, M. Bosse, L. McMillan, S. Gortler, and M. Cohen, “Unstructured lumigraph rendering,” in Seminal Graphics Papers: Pushing the Boundaries, Volume 2, 2023, pp. 497–504.

[4] N. Snavely, S. M. Seitz, and R. Szeliski, “Photo tourism: exploring photo collections in 3d,” in ACM Trans. Graph., 2006, pp. 835–846.

[5] M. Goesele, N. Snavely, B. Curless, H. Hoppe, and S. M. Seitz, “Multi-view stereo for community photo collections,” in Proc. IEEE Int. Conf. Comput. Vis., 2007, pp. 1–8.

[6] S. J. Garbin, M. Kowalski, M. Johnson, J. Shotton, and J. Valentin, “Fastnerf: High-fidelity neural rendering at 200fps,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 14 346–14 355.

[7] C. Reiser, S. Peng, Y. Liao, and A. Geiger, “Kilonerf: Speeding up neural radiance fields with thousands of tiny mlps,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 14 335–14 345.

[8] J. T. Barron, B. Mildenhall, D. Verbin, P. P. Srinivasan, and P. Hedman, “Mip-nerf 360: Unbounded anti-aliased neural radiance fields,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 5470–5479.

[9] T. Müller, A. Evans, C. Schied, and A. Keller, “Instant neural graphics primitives with a multiresolution hash encoding,” ACM Trans. Graph., vol. 41, no. 4, pp. 1–15, 2022.

[10] B. Kerbl, G. Kopanas, T. Leimkühler, and G. Drettakis, “3d gaussian splatting for real-time radiance field rendering,” ACM Trans. Graph., vol. 42, no. 4, 2023.

[11] V. Sitzmann, J. Thies, F. Heide, M. Nießner, G. Wetzstein, and M. Zollhofer, “Deepvoxels: Learning persistent 3d feature embeddings,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2019, pp. 2437–2446.

[12] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “Nerf: Representing scenes as neural radiance fields for view synthesis,” in Proc. Eur. Conf. Comput. Vis., 2020, pp. 405–421.

[13] H. Pfister, M. Zwicker, J. Van Baar, and M. Gross, “Surfels: Surface elements as rendering primitives,” in Proceedings of the 27th annual conference on Computer graphics and interactive techniques, 2000, pp. 335–342.

[14] M. Zwicker, H. Pfister, J. Van Baar, and M. Gross, “Surface splatting,” in Proceedings of the 28th annual conference on Computer graphics and interactive techniques, 2001, pp. 371–378.

[15] L. Ren, H. Pfister, and M. Zwicker, “Object space ewa surface splatting: A hardware accelerated approach to high quality point rendering,” in Comput. Graph. Forum, no. 3, 2002, pp. 461–470.

[16] W. Yifan, F. Serena, S. Wu, C. Öztireli, and O. Sorkine-Hornung, “Differentiable surface splatting for point-based geometry processing,” ACM Trans. Graph., vol. 38, no. 6, pp. 1–14, 2019.

[17] O. Wiles, G. Gkioxari, R. Szeliski, and J. Johnson, “Synsin: Endto-end view synthesis from a single image,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2020, pp. 7467–7477.

[18] D. Kalkofen, E. Mendez, and D. Schmalstieg, “Comprehensible visualization for augmented reality,” IEEE Trans. Vis. Comput. Graph., vol. 15, no. 2, pp. 193–204, 2008.

[19] A. Patney, M. Salvi, J. Kim, A. Kaplanyan, C. Wyman, N. Benty, D. Luebke, and A. Lefohn, “Towards foveated rendering for gazetracked virtual reality,” ACM Trans. Graph., vol. 35, no. 6, pp. 1–12, 2016.

[20] R. Albert, A. Patney, D. Luebke, and J. Kim, “Latency requirements for foveated rendering in virtual reality,” ACM Transactions on Applied Perception, vol. 14, no. 4, pp. 1–13, 2017.

[21] Y. Jiang, C. Yu, T. Xie, X. Li, Y. Feng, H. Wang, M. Li, H. Lau, F. Gao, Y. Yang et al., “Vr-gs: A physical dynamics-aware interactive gaussian splatting system in virtual reality,” arXiv preprint arXiv:2401.16663, 2024.

[22] T. Lu, M. Yu, L. Xu, Y. Xiangli, L. Wang, D. Lin, and B. Dai, “Scaffold-gs: Structured 3d gaussians for view-adaptive rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[23] S. Saito, G. Schwartz, T. Simon, J. Li, and G. Nam, “Relightable gaussian codec avatars,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[24] T. Zhang, K. Huang, W. Zhi, and M. Johnson-Roberson, “Darkgs: Learning neural illumination and 3d gaussians relighting for robotic exploration in the dark,” in Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst., 2024.

[25] B. Fei, J. Xu, R. Zhang, Q. Zhou, W. Yang, and Y. He, “3d gaussian splatting as new era: A survey,” IEEE Trans. Vis. Comput. Graph., 2024.

[26] A. Dalal, D. Hagen, K. G. Robbersmyr, and K. M. Knausgård, “Gaussian splatting: 3d reconstruction and novel view synthesis, a review,” IEEE Access, 2024.

[27] Y. Bao, T. Ding, J. Huo, Y. Liu, Y. Li, W. Li, Y. Gao, and J. Luo, “3d gaussian splatting: Survey, technologies, challenges, and opportunities,” arXiv preprint arXiv:2407.17418, 2024.

[28] T. Wu, Y.-J. Yuan, L.-X. Zhang, J. Yang, Y.-P. Cao, L.-Q. Yan, and L. Gao, “Recent advances in 3d gaussian splatting,” Comput. Vis. Media, pp. 1–30, 2024.

[29] L. Kobbelt and M. Botsch, “A survey of point-based techniques in computer graphics,” Comput. Graph., vol. 28, no. 6, pp. 801–814, 2004.

[30] Y. Xie, T. Takikawa, S. Saito, O. Litany, S. Yan, N. Khan, F. Tombari, J. Tompkin, V. Sitzmann, and S. Sridhar, “Neural fields in visual computing and beyond,” in Comput. Graph. Forum, no. 2, 2022, pp. 641–676.

[31] W. Wang, Y. Yang, and Y. Pan, “Visual knowledge in the big model era: Retrospect and prospect,” arXiv preprint arXiv:2404.04308, 2024.

[32] A. Tewari, J. Thies, B. Mildenhall, P. Srinivasan, E. Tretschk, W. Yifan, C. Lassner, V. Sitzmann, R. Martin-Brualla, S. Lombardi et al., “Advances in neural rendering,” in Comput. Graph. Forum, no. 2, 2022, pp. 703–735.

[33] X.-F. Han, H. Laga, and M. Bennamoun, “Image-based 3d object reconstruction: State-of-the-art and trends in the deep learning era,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 43, no. 5, pp. 1578–1604, 2019.

[34] L. Mescheder, M. Oechsle, M. Niemeyer, S. Nowozin, and A. Geiger, “Occupancy networks: Learning 3d reconstruction in function space,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2019, pp. 4460–4470.

[35] J. J. Park, P. Florence, J. Straub, R. Newcombe, and S. Lovegrove, “Deepsdf: Learning continuous signed distance functions for shape representation,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2019, pp. 165–174.

[36] C. Sun, M. Sun, and H.-T. Chen, “Direct voxel grid optimization: Super-fast convergence for radiance fields reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 5459–5469.

[37] S. Fridovich-Keil, G. Meanti, F. R. Warburg, B. Recht, and A. Kanazawa, “K-planes: Explicit radiance fields in space, time, and appearance,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 12 479–12 488.

[38] J. P. Grossman and W. J. Dally, “Point sample rendering,” in Render. Tech., 1998, pp. 181–192.

[39] M. Zwicker, H. Pfister, J. Van Baar, and M. Gross, “Ewa volume splatting,” in Proceedings Visualization, 2001. VIS’01., 2001, pp. 29–538.

[40] ——, “Ewa splatting,” IEEE Trans. Vis. Comput. Graph., vol. 8, no. 3, pp. 223–238, 2002.

[41] K.-A. Aliev, A. Sevastopolsky, M. Kolos, D. Ulyanov, and V. Lempitsky, “Neural point-based graphics,” in Proc. Eur. Conf. Comput. Vis., 2020, pp. 696–712.

[42] D. Rückert, L. Franke, and M. Stamminger, “Adop: Approximate differentiable one-pixel point rendering,” ACM Trans. Graph., vol. 41, no. 4, pp. 1–14, 2022.

[43] C. Lassner and M. Zollhofer, “Pulsar: Efficient sphere-based neural rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2021, pp. 1440–1449.

[44] K. Cheng, X. Long, K. Yang, Y. Yao, W. Yin, Y. Ma, W. Wang, and X. Chen, “Gaussianpro: 3d gaussian splatting with progressive propagation,” in Proc. ACM Int. Conf. Mach. Learn., 2024.

[45] H. Xiong, S. Muttukuru, R. Upadhyay, P. Chari, and A. Kadambi, “Sparsegs: Real-time 360 {\deg} sparse view synthesis using gaussian splatting,” arXiv preprint arXiv:2312.00206, 2023.

[46] Z. Zhu, Z. Fan, Y. Jiang, and Z. Wang, “Fsgs: Real-time fewshot view synthesis using gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024.

[47] D. Charatan, S. Li, A. Tagliasacchi, and V. Sitzmann, “pixelsplat: 3d gaussian splats from image pairs for scalable generalizable 3d reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[48] S. Szymanowicz, C. Rupprecht, and A. Vedaldi, “Splatter image: Ultra-fast single-view 3d reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[49] J. Li, J. Zhang, X. Bai, J. Zheng, X. Ning, J. Zhou, and L. Gu, “Dngaussian: Optimizing sparse-view 3d gaussian radiance fields with global-local depth normalization,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[50] A. Swann, M. Strong, W. K. Do, G. S. Camps, M. Schwager, and M. Kennedy III, “Touch-gs: Visual-tactile supervised 3d gaussian splatting,” arXiv preprint arXiv:2403.09875, 2024.

[51] Y. Chen, H. Xu, C. Zheng, B. Zhuang, M. Pollefeys, A. Geiger, T.-J. Cham, and J. Cai, “Mvsplat: Efficient 3d gaussian splatting from sparse multi-view images,” in Proc. Eur. Conf. Comput. Vis., 2024.

[52] C. Wewer, K. Raj, E. Ilg, B. Schiele, and J. E. Lenssen, “latentsplat: Autoencoding variational gaussians for fast generalizable 3d reconstruction,” arXiv preprint arXiv:2403.16292, 2024.

[53] Y. Xu, Z. Shi, W. Yifan, H. Chen, C. Yang, S. Peng, Y. Shen, and G. Wetzstein, “Grm: Large gaussian reconstruction model for efficient 3d reconstruction and generation,” arXiv preprint arXiv:2403.14621, 2024.

[54] Q. Shen, X. Yi, Z. Wu, P. Zhou, H. Zhang, S. Yan, and X. Wang, “Gamba: Marry gaussian splatting with mamba for single view 3d reconstruction,” arXiv preprint arXiv:2403.18795, 2024.

[55] J. Zhang, J. Li, X. Yu, L. Huang, L. Gu, J. Zheng, and X. Bai, “Corgs: Sparse-view 3d gaussian splatting via co-regularization,” in Proc. Eur. Conf. Comput. Vis., 2024.

[56] Z. Fan, K. Wang, K. Wen, Z. Zhu, D. Xu, and Z. Wang, “Lightgaussian: Unbounded 3d gaussian compression with 15x reduction and 200+ fps,” arXiv preprint arXiv:2311.17245, 2023.

[57] K. Navaneet, K. P. Meibodi, S. A. Koohpayegani, and H. Pirsiavash, “Compact3d: Compressing gaussian splat radiance field models with vector quantization,” arXiv preprint arXiv:2311.18159, 2023.

[58] J. C. Lee, D. Rho, X. Sun, J. H. Ko, and E. Park, “Compact 3d gaussian representation for radiance field,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[59] W. Morgenstern, F. Barthel, A. Hilsmann, and P. Eisert, “Compact 3d scene representation via self-organizing gaussian grids,” arXiv preprint arXiv:2312.13299, 2023.

[60] X. Zhang, X. Ge, T. Xu, D. He, Y. Wang, H. Qin, G. Lu, J. Geng, and J. Zhang, “Gaussianimage: 1000 fps image representation and compression by 2d gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024.

[61] S. Niedermayr, J. Stumpfegger, and R. Westermann, “Compressed 3d gaussian splatting for accelerated novel view synthesis,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[62] Y. Chen, Q. Wu, J. Cai, M. Harandi, and W. Lin, “Hac: Hash-grid assisted context for 3d gaussian splatting compression,” in Proc. Eur. Conf. Comput. Vis., 2024.

[63] P. Papantonakis, G. Kopanas, B. Kerbl, A. Lanvin, and G. Drettakis, “Reducing the memory footprint of 3d gaussian splatting,” in I3D, 2024, pp. 1–17.

[64] G. Fang and B. Wang, “Mini-splatting: Representing scenes with a constrained number of gaussians,” arXiv preprint arXiv:2403.14166, 2024.

[65] Z. Yu, A. Chen, B. Huang, T. Sattler, and A. Geiger, “Mipsplatting: Alias-free 3d gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024, pp. 19 447–19 456.

[66] J. Gao, C. Gu, Y. Lin, H. Zhu, X. Cao, L. Zhang, and Y. Yao, “Relightable 3d gaussian: Real-time point cloud relighting with brdf decomposition and ray tracing,” arXiv preprint arXiv:2311.16043, 2023.

[67] Z. Yan, W. F. Low, Y. Chen, and G. H. Lee, “Multi-scale 3d gaussian splatting for anti-aliased rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[68] Y. Jiang, J. Tu, Y. Liu, X. Gao, X. Long, W. Wang, and Y. Ma, “Gaussianshader: 3d gaussian splatting with shading functions for reflective surfaces,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[69] B. Lee, H. Lee, X. Sun, U. Ali, and E. Park, “Deblurring 3d gaussian splatting,” arXiv preprint arXiv:2401.00834, 2024.

[70] D. Malarz, W. Smolak, J. Tabor, S. Tadeja, and P. Spurek, “Gaussian splitting algorithm with color and opacity depended on viewing direction,” arXiv preprint arXiv:2312.13729, 2023.

[71] L. Bolanos, S.-Y. Su, and H. Rhodin, “Gaussian shadow casting for neural characters,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[72] L. Radl, M. Steiner, M. Parger, A. Weinrauch, B. Kerbl, and M. Steinberger, “Stopthepop: Sorted gaussian splatting for viewconsistent real-time rendering,” ACM Trans. Graph., 2024.

[73] Z. Yang, X. Gao, Y. Sun, Y. Huang, X. Lyu, W. Zhou, S. Jiao, X. Qi, and X. Jin, “Spec-gaussian: Anisotropic view-dependent appearance for 3d gaussian splatting,” arXiv preprint arXiv:2402.15870, 2024.

[74] C. Peng, Y. Tang, Y. Zhou, N. Wang, X. Liu, D. Li, and R. Chellappa, “Bags: Blur agnostic gaussian splatting through multiscale kernel modeling,” arXiv preprint arXiv:2403.04926, 2024.

[75] L. Zhao, P. Wang, and P. Liu, “Bad-gaussians: Bundle adjusted deblur gaussian splatting,” arXiv preprint arXiv:2403.11831, 2024.

[76] H. Dahmani, M. Bennehar, N. Piasco, L. Roldao, and D. Tsishkou, “Swag: Splatting in the wild images with appearanceconditioned gaussians,” arXiv preprint arXiv:2403.10427, 2024.

[77] Y. Li, C. Lyu, Y. Di, G. Zhai, G. H. Lee, and F. Tombari, “Geogaussian: Geometry-aware gaussian splatting for scene rendering,” arXiv preprint arXiv:2403.11324, 2024.

[78] Z. Liang, Q. Zhang, W. Hu, Y. Feng, L. Zhu, and K. Jia, “Analyticsplatting: Anti-aliased 3d gaussian splatting via analytic integration,” arXiv preprint arXiv:2403.11056, 2024.

[79] O. Seiskari, J. Ylilammi, V. Kaatrasalo, P. Rantalankila, M. Turkulainen, J. Kannala, E. Rahtu, and A. Solin, “Gaussian splatting on the move: Blur and rolling shutter compensation for natural camera motion,” arXiv preprint arXiv:2403.13327, 2024.

[80] X. Song, J. Zheng, S. Yuan, H.-a. Gao, J. Zhao, X. He, W. Gu, and H. Zhao, “Sa-gs: Scale-adaptive gaussian splatting for trainingfree anti-aliasing,” arXiv preprint arXiv:2403.19615, 2024.

[81] Y. Fu, S. Liu, A. Kulkarni, J. Kautz, A. A. Efros, and X. Wang, “Colmap-free 3d gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[82] J. Jung, J. Han, H. An, J. Kang, S. Park, and S. Kim, “Relaxing accurate initialization constraint for 3d gaussian splatting,” arXiv preprint arXiv:2403.09413, 2024.

[83] M. Yu, T. Lu, L. Xu, L. Jiang, Y. Xiangli, and B. Dai, “Gsdf: 3dgs meets sdf for improved rendering and reconstruction,” arXiv preprint arXiv:2403.16964, 2024.

[84] J. Zhang, F. Zhan, M. Xu, S. Lu, and E. Xing, “Fregs: 3d gaussian splatting with progressive frequency regularization,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[85] L. Huang, J. Bai, J. Guo, and Y. Guo, “Gs++: Error analyzing and optimal gaussian splatting,” arXiv preprint arXiv:2402.00752, 2024.

[86] J. Li, L. Cheng, Z. Wang, T. Mu, and J. He, “Loopgaussian: Creating 3d cinemagraph with multi-view images via eulerian motion field,” arXiv preprint arXiv:2404.08966, 2024.

[87] J.-C. Shi, M. Wang, H.-B. Duan, and S.-H. Guan, “Language embedded 3d gaussians for open-vocabulary scene understanding,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[88] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, “Langsplat: 3d language gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[89] X. Zuo, P. Samangouei, Y. Zhou, Y. Di, and M. Li, “Fmgs: Foundation model embedded 3d gaussian splatting for holistic 3d scene understanding,” arXiv preprint arXiv:2401.01970, 2024.

[90] S. Zhou, H. Chang, S. Jiang, Z. Fan, Z. Zhu, D. Xu, P. Chari, S. You, Z. Wang, and A. Kadambi, “Feature 3dgs: Supercharging 3d gaussian splatting to enable distilled feature fields,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[91] M. Ye, M. Danelljan, F. Yu, and L. Ke, “Gaussian grouping: Segment and edit anything in 3d scenes,” in Proc. Eur. Conf. Comput. Vis., 2024.

[92] J. Cen, J. Fang, C. Yang, L. Xie, X. Zhang, W. Shen, and Q. Tian, “Segment any 3d gaussians,” arXiv preprint arXiv:2312.00860, 2023.

[93] Z. Yang, H. Yang, Z. Pan, X. Zhu, and L. Zhang, “Real-time photorealistic dynamic scene representation and rendering with 4d gaussian splatting,” in Proc. Int. Conf. Learn. Represent., 2024.

[94] Z. Yang, X. Gao, W. Zhou, S. Jiao, Y. Zhang, and X. Jin, “Deformable 3d gaussians for high-fidelity monocular dynamic scene reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[95] G. Wu, T. Yi, J. Fang, L. Xie, X. Zhang, W. Wei, W. Liu, Q. Tian, and X. Wang, “4d gaussian splatting for real-time dynamic scene rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[96] Y. Xu, B. Chen, Z. Li, H. Zhang, L. Wang, Z. Zheng, and Y. Liu, “Gaussian head avatar: Ultra high-fidelity head avatar via dynamic gaussians,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[97] S. Szymanowicz, E. Insafutdinov, C. Zheng, D. Campbell, J. F. Henriques, C. Rupprecht, and A. Vedaldi, “Flash3d: Feedforward generalisable 3d scene reconstruction from a single image,” arXiv preprint arXiv:2406.04343, 2024.

[98] K. Sargent, Z. Li, T. Shah, C. Herrmann, H.-X. Yu, Y. Zhang, E. R. Chan, D. Lagun, L. Fei-Fei, D. Sun et al., “Zeronvs: Zero-shot 360degree view synthesis from a single image,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024, pp. 9420–9429.

[99] J. Meng, H. Li, Y. Wu, Q. Gao, S. Yang, J. Zhang, and S. Ma, “Mirror-3dgs: Incorporating mirror reflections into 3d gaussian splatting,” arXiv preprint arXiv:2404.01168, 2024.

[100] H. Chen, C. Li, and G. H. Lee, “Neusg: Neural implicit surface reconstruction with 3d gaussian splatting guidance,” arXiv preprint arXiv:2312.00846, 2023.

[101] Z. Yu, T. Sattler, and A. Geiger, “Gaussian opacity fields: Efficient and compact surface reconstruction in unbounded scenes,” arXiv preprint arXiv:2404.10772, 2024.

[102] B. Zhang, C. Fang, R. Shrestha, Y. Liang, X. Long, and P. Tan, “Rade-gs: Rasterizing depth in gaussian splatting,” arXiv preprint arXiv:2406.01467, 2024.

[103] A. Chen, H. Xu, S. Esposito, S. Tang, and A. Geiger, “Lara: Efficient large-baseline radiance fields,” arXiv preprint arXiv:2407.04699, 2024.

[104] E. Ververas, R. A. Potamias, J. Song, J. Deng, and S. Zafeiriou, “Sags: Structure-aware 3d gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024, pp. 221–238.

[105] C. Smith, D. Charatan, A. Tewari, and V. Sitzmann, “Flowmap: High-quality camera poses, intrinsics, and depth via gradient descent,” arXiv preprint arXiv:2404.15259, 2024.

[106] Y. Lin, Z. Dai, S. Zhu, and Y. Yao, “Gaussian-flow: 4d reconstruction with dynamic 3d gaussian particle,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[107] A. Saroha, M. Gladkova, C. Curreli, T. Yenamandra, and D. Cremers, “Gaussian splatting in style,” arXiv preprint arXiv:2403.08498, 2024.

[108] N. Moenne-Loccoz, A. Mirzaei, O. Perel, R. de Lutio, J. Martinez Esturo, G. State, S. Fidler, N. Sharp, and Z. Gojcic, “3d gaussian ray tracing: Fast tracing of particle scenes,” ACM Trans. Graph., vol. 43, no. 6, pp. 1–19, 2024.

[109] A. Mai, P. Hedman, G. Kopanas, D. Verbin, D. Futschik, Q. Xu, F. Kuester, J. T. Barron, and Y. Zhang, “Ever: Exact volumetric ellipsoid rendering for real-time view synthesis,” arXiv preprint arXiv:2410.01804, 2024.

[110] J. Condor, S. Speierer, L. Bode, A. Bozic, S. Green, P. Didyk, and A. Jarabo, “Don’t splat your gaussians: Volumetric ray-traced primitives for modeling and rendering scattering and emissive media,” ACM Trans. Graph., 2025.

[111] C. Yan, D. Qu, D. Wang, D. Xu, Z. Wang, B. Zhao, and X. Li, “Gs-slam: Dense visual slam with 3d gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[112] N. Keetha, J. Karhade, K. M. Jatavallabhula, G. Yang, S. Scherer, D. Ramanan, and J. Luiten, “Splatam: Splat, track & map 3d gaussians for dense rgb-d slam,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[113] H. Matsuki, R. Murai, P. H. Kelly, and A. J. Davison, “Gaussian splatting slam,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[114] V. Yugay, Y. Li, T. Gevers, and M. R. Oswald, “Gaussian-slam: Photo-realistic dense slam with gaussian splatting,” arXiv preprint arXiv:2312.10070, 2023.

[115] H. Huang, L. Li, H. Cheng, and S.-K. Yeung, “Photo-slam: Realtime simultaneous localization and photorealistic mapping for monocular, stereo, and rgb-d cameras,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[116] M. Li, S. Liu, and H. Zhou, “Sgs-slam: Semantic gaussian splatting for neural dense slam,” in Proc. Eur. Conf. Comput. Vis., 2024.

[117] Y. Ji, Y. Liu, G. Xie, B. Ma, and Z. Xie, “Neds-slam: A novel neural explicit dense semantic slam framework using 3d gaussian splatting,” arXiv preprint arXiv:2403.11679, 2024.

[118] G. Lu, S. Zhang, Z. Wang, C. Liu, J. Lu, and Y. Tang, “Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation,” arXiv preprint arXiv:2403.08321, 2024.

[119] J. Abou-Chakra, K. Rana, F. Dayoub, and N. Sünderhauf, “Physically embodied gaussian splatting: A realtime correctable world model for robotics,” in Proc. Annu. Conf. Robot Learn., 2024.

[120] O. Shorinwa, J. Tucker, A. Smith, A. Swann, T. Chen, R. Firoozi, M. D. Kennedy, and M. Schwager, “Splat-mover: Multi-stage, open-vocabulary robotic manipulation via editable gaussian splatting,” in Proc. Annu. Conf. Robot Learn., 2024.

[121] M. Ji, R.-Z. Qiu, X. Zou, and X. Wang, “Graspsplats: Efficient manipulation with 3d feature splatting,” arXiv preprint arXiv:2409.02084, 2024.

[122] Y. Zheng, X. Chen, Y. Zheng, S. Gu, R. Yang, B. Jin, P. Li, C. Zhong, Z. Wang, L. Liu et al., “Gaussiangrasper: 3d language gaussian splatting for open-vocabulary robotic grasping,” arXiv preprint arXiv:2403.09637, 2024.

[123] S. Zhu, R. Qin, G. Wang, J. Liu, and H. Wang, “Semgaussslam: Dense semantic gaussian splatting slam,” arXiv preprint arXiv:2403.07494, 2024.

[124] Z. Peng, T. Shao, Y. Liu, J. Zhou, Y. Yang, J. Wang, and K. Zhou, “Rtg-slam: Real-time 3d reconstruction at scale using gaussian splatting,” ACM Trans. Graph., 2024.

[125] J. Luiten, G. Kopanas, B. Leibe, and D. Ramanan, “Dynamic 3d gaussians: Tracking by persistent dynamic view synthesis,” in Proc. Int. Conf. 3D Vis., 2024.

[126] H. Yu, J. Julin, Z. Á. Milacski, K. Niinuma, and L. A. Jeni, “Cogs: Controllable gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[127] R. Shao, J. Sun, C. Peng, Z. Zheng, B. Zhou, H. Zhang, and Y. Liu, “Control4d: Efficient 4d portrait editing with text,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[128] Y.-H. Huang, Y.-T. Sun, Z. Yang, X. Lyu, Y.-P. Cao, and X. Qi, “Sc-gs: Sparse-controlled gaussian splatting for editable dynamic scenes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[129] D. Das, C. Wewer, R. Yunus, E. Ilg, and J. E. Lenssen, “Neural parametric gaussians for monocular non-rigid object reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[130] Z. Li, Z. Chen, Z. Li, and Y. Xu, “Spacetime gaussian feature splatting for real-time dynamic view synthesis,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[131] J. Sun, H. Jiao, G. Li, Z. Zhang, L. Zhao, and W. Xing, “3dgstream: On-the-fly training of 3d gaussians for efficient streaming of photo-realistic free-viewpoint videos,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[132] Z. Lu, X. Guo, L. Hui, T. Chen, M. Yang, X. Tang, F. Zhu, and Y. Dai, “3d geometry-aware deformable gaussian splatting for dynamic view synthesis,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[133] J. Tang, J. Ren, H. Zhou, Z. Liu, and G. Zeng, “Dreamgaussian: Generative gaussian splatting for efficient 3d content creation,” in Proc. Int. Conf. Learn. Represent., 2024.

[134] T. Yi, J. Fang, J. Wang, G. Wu, L. Xie, X. Zhang, W. Liu, Q. Tian, and X. Wang, “Gaussiandreamer: Fast generation from text to 3d gaussians by bridging 2d and 3d diffusion models,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[135] J. Tang, Z. Chen, X. Chen, T. Wang, G. Zeng, and Z. Liu, “Lgm: Large multi-view gaussian model for high-resolution 3d content creation,” in Proc. Eur. Conf. Comput. Vis., 2024.

[136] S. Zhou, Z. Fan, D. Xu, H. Chang, P. Chari, T. Bharadwaj, S. You, Z. Wang, and A. Kadambi, “Dreamscene360: Unconstrained textto-3d scene generation with panoramic gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024.

[137] Z. Li, Y. Chen, L. Zhao, and P. Liu, “Controllable text-to-3d generation via surface-aligned gaussian splatting,” arXiv preprint arXiv:2403.09981, 2024.

[138] Y. Mu, X. Zuo, C. Guo, Y. Wang, J. Lu, X. Wu, S. Xu, P. Dai, Y. Yan, and L. Cheng, “Gsd: View-guided gaussian splatting diffusion for 3d reconstruction,” in Proc. Eur. Conf. Comput. Vis., 2024.

[139] Y. Jiang, Z. Shen, P. Wang, Z. Su, Y. Hong, Y. Zhang, J. Yu, and L. Xu, “Hifi4g: High-fidelity human performance rendering via compact gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[140] Y. Wang, Q. Wu, G. Zhang, and D. Xu, “Gscream: Learning 3d geometry and feature consistent gaussian splatting for object removal,” in Proc. Eur. Conf. Comput. Vis., 2024.

[141] Y. Chen, Z. Chen, C. Zhang, F. Wang, X. Yang, Y. Wang, Z. Cai, L. Yang, H. Liu, and G. Lin, “Gaussianeditor: Swift and controllable 3d editing with gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[142] J. Fang, J. Wang, X. Zhang, L. Xie, and Q. Tian, “Gaussianeditor: Editing 3d gaussians delicately with text instructions,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[143] R.-Z. Qiu, G. Yang, W. Zeng, and X. Wang, “Feature splatting: Language-driven physics-based scene synthesis and editing,” arXiv preprint arXiv:2404.01223, 2024.

[144] Z. Li, Z. Zheng, L. Wang, and Y. Liu, “Animatable gaussians: Learning pose-dependent gaussian maps for high-fidelity human avatar modeling,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[145] S. Hu and Z. Liu, “Gauhuman: Articulated gaussian splatting from monocular human videos,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[146] J. Lei, Y. Wang, G. Pavlakos, L. Liu, and K. Daniilidis, “Gart: Gaussian articulated template models,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[147] Y. Yuan, X. Li, Y. Huang, S. De Mello, K. Nagano, J. Kautz, and U. Iqbal, “Gavatar: Animatable 3d gaussian avatars with implicit mesh learning,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[148] Z. Zhou, F. Ma, H. Fan, and Y. Yang, “Headstudio: Text to animatable head avatars with 3d gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024.

[149] S. Qian, T. Kirschstein, L. Schoneveld, D. Davoli, S. Giebenhain, and M. Nießner, “Gaussianavatars: Photorealistic head avatars with rigged 3d gaussians,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[150] H. Dhamo, Y. Nie, A. Moreau, J. Song, R. Shaw, Y. Zhou, and E. Pérez-Pellitero, “Headgas: Real-time animatable head avatars via 3d gaussian splatting,” arXiv preprint arXiv:2312.02902, 2023.

[151] J. Li, J. Zhang, X. Bai, J. Zheng, X. Ning, J. Zhou, and L. Gu, “Talkinggaussian: Structure-persistent 3d talking head synthesis via gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024.

[152] Y. Huang, B. Cui, L. Bai, Z. Guo, M. Xu, and H. Ren, “Endo4dgs: Distilling depth ranking for endoscopic monocular scene reconstruction with 4d gaussian splatting,” in Proc. Int. Conf. Med. Image Comput. Comput. Assist. Interv., 2024.

[153] Y. Liu, C. Li, C. Yang, and Y. Yuan, “Endogaussian: Gaussian splatting for deformable surgical scene reconstruction,” arXiv preprint arXiv:2401.12561, 2024.

[154] L. Zhu, Z. Wang, Z. Jin, G. Lin, and L. Yu, “Deformable endoscopic tissues reconstruction with gaussian splatting,” arXiv preprint arXiv:2401.11535, 2024.

[155] H. Zhao, X. Zhao, L. Zhu, W. Zheng, and Y. Xu, “Hfgs: 4d gaussian splatting with emphasis on spatial and temporal highfrequency components for endoscopic scene reconstruction,” arXiv preprint arXiv:2405.17872, 2024.

[156] K. Wang, C. Yang, Y. Wang, S. Li, Y. Wang, Q. Dou, X. Yang, and W. Shen, “Endogslam: Real-time dense reconstruction and tracking in endoscopic surgeries using gaussian splatting,” arXiv preprint arXiv:2403.15124, 2024.

[157] S. Bonilla, S. Zhang, D. Psychogyios, D. Stoyanov, F. Vasconcelos, and S. Bano, “Gaussian pancakes: Geometrically-regularized 3d gaussian splatting for realistic endoscopic reconstruction,” arXiv preprint arXiv:2404.06128, 2024.

[158] K. Wu, K. Zhang, Z. Zhang, S. Yuan, M. Tie, J. Wei, Z. Xu, J. Zhao, Z. Gan, and W. Ding, “Hgs-mapping: Online dense mapping using hybrid gaussian representation in urban scenes,” arXiv preprint arXiv:2403.20159, 2024.

[159] C. Wu, Y. Duan, X. Zhang, Y. Sheng, J. Ji, and Y. Zhang, “Mmgaussian: 3d gaussian-based multi-modal fusion for localization and reconstruction in unbounded scenes,” in Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst., 2024.

[160] B. Xiong, Z. Li, and Z. Li, “Gauu-scene: A scene reconstruction benchmark on large scale 3d reconstruction dataset using gaussian splatting,” arXiv preprint arXiv:2401.14032, 2024.

[161] H. Zhao, H. Weng, D. Lu, A. Li, J. Li, A. Panda, and S. Xie, “On scaling up 3d gaussian splatting training,” arXiv preprint arXiv:2406.18533, 2024.

[162] B. Kerbl, A. Meuleman, G. Kopanas, M. Wimmer, A. Lanvin, and G. Drettakis, “A hierarchical 3d gaussian representation for realtime rendering of very large datasets,” ACM Trans. Graph., vol. 44, no. 3, 2024.

[163] Y. Liu, H. Guan, C. Luo, L. Fan, J. Peng, and Z. Zhang, “Citygaussian: Real-time high-quality large-scale scene rendering with gaussians,” in Proc. Eur. Conf. Comput. Vis., 2024.

[164] J. Lin, Z. Li, X. Tang, J. Liu, S. Liu, J. Liu, Y. Lu, X. Wu, S. Xu, Y. Yan et al., “Vastgaussian: Vast 3d gaussians for large scene reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[165] K. Ren, L. Jiang, T. Lu, M. Yu, L. Xu, Z. Ni, and B. Dai, “Octreegs: Towards consistent real-time rendering with lod-structured 3d gaussians,” arXiv preprint arXiv:2403.17898, 2024.

[166] T. Xie, Z. Zong, Y. Qiu, X. Li, Y. Feng, Y. Yang, and C. Jiang, “Physgaussian: Physics-integrated 3d gaussians for generative dynamics,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[167] F. Liu, H. Wang, S. Yao, S. Zhang, J. Zhou, and Y. Duan, “Physics3d: Learning physical properties of 3d gaussians via video diffusion,” arXiv preprint arXiv:2406.04338, 2024.

[168] P. Borycki, W. Smolak, J. Waczyńska, M. Mazur, S. Tadeja, and P. Spurek, “Gasp: Gaussian splatting for physic-based simulations,” arXiv preprint arXiv:2409.05819, 2024.

[169] T. Huang, Y. Zeng, H. Li, W. Zuo, and R. W. Lau, “Dreamphysics: Learning physical properties of dynamic 3d gaussians with video diffusion priors,” in Proc. AAAI Conf. Artif. Intell., 2025.

[170] T. Zhang, H.-X. Yu, R. Wu, B. Y. Feng, C. Zheng, N. Snavely, J. Wu, and W. T. Freeman, “Physdreamer: Physics-based interaction with 3d objects via video generation,” in Proc. Eur. Conf. Comput. Vis., 2024, pp. 388–406.

[171] Y. Feng, X. Feng, Y. Shang, Y. Jiang, C. Yu, Z. Zong, T. Shao, H. Wu, K. Zhou, C. Jiang et al., “Gaussian splashing: Dynamic fluid synthesis with gaussian splatting,” arXiv preprint arXiv:2401.15318, 2024.

[172] L. Zhong, H.-X. Yu, J. Wu, and Y. Li, “Reconstruction and simulation of elastic objects with spring-mass 3d gaussians,” in Proc. Eur. Conf. Comput. Vis., 2024.

[173] Y. Shao, M. Huang, C. C. Loy, and B. Dai, “Gausim: Registering elastic objects into digital world by gaussian simulator,” arXiv preprint arXiv:2412.17804, 2024.

[174] S. Zhang, H. Zhao, Z. Zhou, G. Wu, C. Zheng, X. Wang, and W. Liu, “Togs: Gaussian splatting with temporal opacity offset for real-time 4d dsa rendering,” arXiv preprint arXiv:2403.19586, 2024.

[175] R. Wu, Z. Zhang, Y. Yang, and W. Zuo, “Dual-camera smooth zoom on mobile phones,” arXiv preprint arXiv:2404.04908, 2024.

[176] H. Li, Y. Gao, D. Zhang, C. Wu, Y. Dai, C. Zhao, H. Feng, E. Ding, J. Wang, and J. Han, “Ggrt: Towards generalizable 3d gaussians without pose priors in real-time,” arXiv preprint arXiv:2403.10147, 2024.

[177] S. Hong, J. He, X. Zheng, H. Wang, H. Fang, K. Liu, C. Zheng, and S. Shen, “Liv-gaussmap: Lidar-inertial-visual fusion for real-time 3d radiance field map rendering,” arXiv preprint arXiv:2401.14857, 2024.

[178] S. Sun, M. Mielle, A. J. Lilienthal, and M. Magnusson, “Highfidelity slam using gaussian splatting with rendering-guided densification and regularized optimization,” in Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst., 2024.

[179] F. Tosi, Y. Zhang, Z. Gong, E. Sandström, S. Mattoccia, M. R. Oswald, and M. Poggi, “How nerfs and 3d gaussian splatting are reshaping slam: a survey,” arXiv preprint arXiv:2402.13255, 2024.

[180] T. Deng, Y. Chen, L. Zhang, J. Yang, S. Yuan, D. Wang, and W. Chen, “Compact 3d gaussian splatting for dense visual slam,” arXiv preprint arXiv:2403.11247, 2024.

[181] J. Hu, X. Chen, B. Feng, G. Li, L. Yang, H. Bao, G. Zhang, and Z. Cui, “Cg-slam: Efficient dense rgb-d slam in a consistent uncertainty-aware 3d gaussian field,” arXiv preprint arXiv:2403.16095, 2024.

[182] X. Lang, L. Li, H. Zhang, F. Xiong, M. Xu, Y. Liu, X. Zuo, and J. Lv, “Gaussian-lic: Photo-realistic lidar-inertial-camera slam with 3d gaussian splatting,” arXiv preprint arXiv:2404.06926, 2024.

[183] E. Sandström, K. Tateno, M. Oechsle, M. Niemeyer, L. Van Gool, M. R. Oswald, and F. Tombari, “Splat-slam: Globally optimized rgb-only slam with 3d gaussians,” arXiv preprint arXiv:2405.16544, 2024.

[184] A. Pumarola, E. Corona, G. Pons-Moll, and F. Moreno-Noguer, “D-nerf: Neural radiance fields for dynamic scenes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2021, pp. 10 318–10 327.

[185] K. Park, U. Sinha, P. Hedman, J. T. Barron, S. Bouaziz, D. B. Goldman, R. Martin-Brualla, and S. M. Seitz, “Hypernerf: a higher-dimensional representation for topologically varying neural radiance fields,” ACM Trans. Graph., vol. 40, no. 6, pp. 1–12, 2021.

[186] K. Park, U. Sinha, J. T. Barron, S. Bouaziz, D. B. Goldman, S. M. Seitz, and R. Martin-Brualla, “Nerfies: Deformable neural radiance fields,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 5865–5874.

[187] X. Guo, J. Sun, Y. Dai, G. Chen, X. Ye, X. Tan, E. Ding, Y. Zhang, and J. Wang, “Forward flow for novel view synthesis of dynamic scenes,” in Proc. IEEE Int. Conf. Comput. Vis., 2023, pp. 16 022–16 033.

[188] X. Zhou, Z. Lin, X. Shan, Y. Wang, D. Sun, and M.-H. Yang, “Drivinggaussian: Composite gaussian splatting for surrounding dynamic autonomous driving scenes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[189] Y. Yan, H. Lin, C. Zhou, W. Wang, H. Sun, K. Zhan, X. Lang, X. Zhou, and S. Peng, “Street gaussians for modeling dynamic urban scenes,” in Proc. Eur. Conf. Comput. Vis., 2024.

[190] H. Zhou, J. Shao, L. Xu, D. Bai, W. Qiu, B. Liu, Y. Wang, A. Geiger, and Y. Liao, “Hugs: Holistic urban 3d scene understanding via gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024, pp. 21 336–21 345.

[191] A. Kratimenos, J. Lei, and K. Daniilidis, “Dynmf: Neural motion factorization for real-time dynamic view synthesis with 3d gaussian splatting,” arXiv preprint arXiv:2312.00112, 2023.

[192] R. Shaw, J. Song, A. Moreau, M. Nazarczuk, S. Catley-Chandar, H. Dhamo, and E. Perez-Pellitero, “Swags: Sampling windows adaptively for dynamic 3d gaussian splatting,” arXiv preprint arXiv:2312.13308, 2023.

[193] Y. Liang, N. Khan, Z. Li, T. Nguyen-Phuoc, D. Lanman, J. Tompkin, and L. Xiao, “Gaufre: Gaussian deformation fields for real-time dynamic novel view synthesis,” arXiv preprint arXiv:2312.11458, 2023.

[194] K. Katsumata, D. M. Vo, and H. Nakayama, “An efficient 3d gaussian representation for monocular/multi-view dynamic scenes,” arXiv preprint arXiv:2311.12897, 2023.

[195] Z. Guo, W. Zhou, L. Li, M. Wang, and H. Li, “Motion-aware 3d gaussian splatting for efficient dynamic scene reconstruction,” arXiv preprint arXiv:2403.11447, 2024.

[196] J. Bae, S. Kim, Y. Yun, H. Lee, G. Bang, and Y. Uh, “Per-gaussian embedding-based deformation for deformable 3d gaussian splatting,” arXiv preprint arXiv:2404.03613, 2024.

[197] J. Lei, Y. Weng, A. Harley, L. Guibas, and K. Daniilidis, “Mosca: Dynamic gaussian fusion from casual videos via 4d motion scaffolds,” arXiv preprint arXiv:2405.17421, 2024.

[198] Q. Wang, V. Ye, H. Gao, J. Austin, Z. Li, and A. Kanazawa, “Shape of motion: 4d reconstruction from a single video,” arXiv preprint arXiv:2407.13764, 2024.

[199] Y. Duan, F. Wei, Q. Dai, Y. He, W. Chen, and B. Chen, “4drotor gaussian splatting: towards efficient novel view synthesis for dynamic scenes,” in Proc. ACM Spec. Interest Group Comput. Graph. Interact. Tech., 2024, pp. 1–11.

[200] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. WardeFarley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial networks,” Communications of the ACM, vol. 63, no. 11, pp. 139–144, 2020.

[201] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” in Proc. Adv. Neural Inf. Process. Syst., 2020, pp. 6840–6851.

[202] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, “High-resolution image synthesis with latent diffusion models,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 10 684–10 695.

[203] L. Zhang, A. Rao, and M. Agrawala, “Adding conditional control to text-to-image diffusion models,” in Proc. IEEE Int. Conf. Comput. Vis., 2023, pp. 3836–3847.

[204] Z. Chen, F. Wang, and H. Liu, “Text-to-3d using gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[205] Y. Liang, X. Yang, J. Lin, H. Li, X. Xu, and Y. Chen, “Luciddreamer: Towards high-fidelity text-to-3d generation via interval score matching,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[206] X. Liu, X. Zhan, J. Tang, Y. Shan, G. Zeng, D. Lin, X. Liu, and Z. Liu, “Humangaussian: Text-driven 3d human generation with gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[207] X. Yang, Y. Chen, C. Chen, C. Zhang, Y. Xu, X. Yang, F. Liu, and G. Lin, “Learn to optimize denoising scores for 3d generation: A unified and improved diffusion prior on nerf and 3d gaussian splatting,” arXiv preprint arXiv:2312.04820, 2023.

[208] Z.-X. Zou, Z. Yu, Y.-C. Guo, Y. Li, D. Liang, Y.-P. Cao, and S.-H. Zhang, “Triplane meets gaussian splatting: Fast and generalizable single-view 3d reconstruction with transformers,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[209] H. Ling, S. W. Kim, A. Torralba, S. Fidler, and K. Kreis, “Align your gaussians: Text-to-4d with dynamic 3d gaussians and composed diffusion models,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[210] J. Ren, L. Pan, J. Tang, C. Zhang, A. Cao, G. Zeng, and Z. Liu, “Dreamgaussian4d: Generative 4d gaussian splatting,” arXiv preprint arXiv:2312.17142, 2023.

[211] Y. Yin, D. Xu, Z. Wang, Y. Zhao, and Y. Wei, “4dgen: Grounded 4d content generation with spatial-temporal consistency,” arXiv preprint arXiv:2312.17225, 2023.

[212] J. Zhang, Z. Tang, Y. Pang, X. Cheng, P. Jin, Y. Wei, W. Yu, M. Ning, and L. Yuan, “Repaint123: Fast and high-quality one image to 3d generation with progressive controllable 2d repainting,” arXiv preprint arXiv:2312.13271, 2023.

[213] Z. Pan, Z. Yang, X. Zhu, and L. Zhang, “Fast dynamic 3d object generation from a single-view video,” arXiv preprint arXiv:2401.08742, 2024.

[214] D. Xu, Y. Yuan, M. Mardani, S. Liu, J. Song, Z. Wang, and A. Vahdat, “Agg: Amortized generative 3d gaussians for single image to 3d,” arXiv preprint arXiv:2401.04099, 2024.

[215] C. Yang, S. Li, J. Fang, R. Liang, L. Xie, X. Zhang, W. Shen, and Q. Tian, “Gaussianobject: Just taking four images to get a high-quality 3d object with gaussian splatting,” arXiv preprint arXiv:2402.10259, 2024.

[216] F. Barthel, A. Beckmann, W. Morgenstern, A. Hilsmann, and P. Eisert, “Gaussian splatting decoder for 3d-aware generative adversarial networks,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. Worksh., 2024.

[217] L. Jiang and L. Wang, “Brightdreamer: Generic 3d gaussian generative framework for fast text-to-3d synthesis,” arXiv preprint arXiv:2403.11273, 2024.

[218] W. Zhuo, F. Ma, H. Fan, and Y. Yang, “Vividdreamer: Invariant score distillation for hyper-realistic text-to-3d generation,” in Proc. Eur. Conf. Comput. Vis., 2024.

[219] Z. Wu, C. Yu, Y. Jiang, C. Cao, F. Wang, and X. Bai, “Sc4d: Sparse-controlled video-to-4d generation and motion transfer,” arXiv preprint arXiv:2404.03736, 2024.

[220] X. He, J. Chen, S. Peng, D. Huang, Y. Li, X. Huang, C. Yuan, W. Ouyang, and T. He, “Gvgen: Text-to-3d generation with volumetric representation,” in Proc. Eur. Conf. Comput. Vis., 2024.

[221] X. Yang and X. Wang, “Hash3d: Training-free acceleration for 3d generation,” arXiv preprint arXiv:2404.06091, 2024.

[222] J. Kim, J. Koo, K. Yeo, and M. Sung, “Synctweedies: A general generative framework based on synchronized diffusions,” arXiv preprint arXiv:2403.14370, 2024.

[223] Q. Feng, Z. Xing, Z. Wu, and Y.-G. Jiang, “Fdgaussian: Fast gaussian splatting from single image via geometric-aware diffusion model,” arXiv preprint arXiv:2403.10242, 2024.

[224] H. Li, H. Shi, W. Zhang, W. Wu, Y. Liao, L. Wang, L.-h. Lee, and P. Zhou, “Dreamscene: 3d gaussian-based text-to-3d scene generation via formation pattern sampling,” arXiv preprint arXiv:2404.03575, 2024.

[225] L. Melas-Kyriazi, I. Laina, C. Rupprecht, N. Neverova, A. Vedaldi, O. Gafni, and F. Kokkinos, “Im-3d: Iterative multiview diffusion and reconstruction for high-quality 3d generation,” in Proc. ACM Int. Conf. Mach. Learn., 2024.

[226] B. Zhang, Y. Cheng, J. Yang, C. Wang, F. Zhao, Y. Tang, D. Chen, and B. Guo, “Gaussiancube: Structuring gaussian splatting using optimal transport for 3d generative modeling,” arXiv preprint arXiv:2403.19655, 2024.

[227] Y.-C. Lee, Y.-T. Chen, A. Wang, T.-H. Liao, B. Y. Feng, and J.-B. Huang, “Vividdream: Generating 3d scene with ambient dynamics,” arXiv preprint arXiv:2405.20334, 2024.

[228] J. Huang and H. Yu, “Point’n move: Interactive scene object manipulation on gaussian splatting radiance fields,” arXiv preprint arXiv:2311.16737, 2023.

[229] K. Lan, H. Li, H. Shi, W. Wu, Y. Liao, L. Wang, and P. Zhou, “2d-guided 3d gaussian segmentation,” arXiv preprint arXiv:2312.16047, 2023.

[230] J. Zhuang, D. Kang, Y.-P. Cao, G. Li, L. Lin, and Y. Shan, “Tipeditor: An accurate 3d editor following both text-prompts and image-prompts,” arXiv preprint arXiv:2401.14828, 2024.

[231] B. Dou, T. Zhang, Y. Ma, Z. Wang, and Z. Yuan, “Cosseggaussians: Compact and swift scene segmenting 3d gaussians,” arXiv preprint arXiv:2401.05925, 2024.

[232] X. Hu, Y. Wang, L. Fan, J. Fan, J. Peng, Z. Lei, Q. Li, and Z. Zhang, “Semantic anything in 3d gaussians,” arXiv preprint arXiv:2401.17857, 2024.

[233] F. Palandra, A. Sanchietti, D. Baieri, and E. Rodolà, “Gsedit: Efficient text-guided editing of 3d objects via gaussian splatting,” arXiv preprint arXiv:2403.05154, 2024.

[234] Q. Gu, Z. Lv, D. Frost, S. Green, J. Straub, and C. Sweeney, “Egolifter: Open-world 3d segmentation for egocentric perception,” arXiv preprint arXiv:2403.18118, 2024.

[235] W. Lyu, X. Li, A. Kundu, Y.-H. Tsai, and M.-H. Yang, “Gaga: Group any gaussians via 3d-aware memory bank,” arXiv preprint arXiv:2404.07977, 2024.

[236] Z. Liu, H. Ouyang, Q. Wang, K. L. Cheng, J. Xiao, K. Zhu, N. Xue, Y. Liu, Y. Shen, and Y. Cao, “Infusion: Inpainting 3d gaussians via learning depth completion from diffusion prior,” arXiv preprint arXiv:2404.11613, 2024.

[237] D. Zhang, Z. Chen, Y.-J. Yuan, F.-L. Zhang, Z. He, S. Shan, and L. Gao, “Stylizedgs: Controllable stylization for 3d gaussian splatting,” arXiv preprint arXiv:2404.05220, 2024.

[238] Q. Zhang, Y. Xu, C. Wang, H.-Y. Lee, G. Wetzstein, B. Zhou, and C. Yang, “3ditscene: Editing any scene via language-guided disentangled gaussian splatting,” arXiv preprint arXiv:2405.18424, 2024.

[239] J. Wu, J.-W. Bian, X. Li, G. Wang, I. Reid, P. Torr, and V. A. Prisacariu, “Gaussctrl: Multi-view consistent text-driven 3d gaussian splatting editing,” in Proc. Eur. Conf. Comput. Vis., 2024, pp. 55–71.

[240] Y. Wang, X. Yi, Z. Wu, N. Zhao, L. Chen, and H. Zhang, “Viewconsistent 3d editing with gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024, pp. 404–420.

[241] R. Jena, G. S. Iyer, S. Choudhary, B. Smith, P. Chaudhari, and J. Gee, “Splatarmor: Articulated gaussian splatting for animatable humans from monocular rgb videos,” arXiv preprint arXiv:2311.10812, 2023.

[242] K. Ye, T. Shao, and K. Zhou, “Animatable 3d gaussians for high-fidelity synthesis of human motions,” arXiv preprint arXiv:2311.13404, 2023.

[243] A. Moreau, J. Song, H. Dhamo, R. Shaw, Y. Zhou, and E. PérezPellitero, “Human gaussian splatting: Real-time rendering of animatable avatars,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[244] M. Kocabas, J.-H. R. Chang, J. Gabriel, O. Tuzel, and A. Ranjan, “Hugs: Human gaussian splats,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[245] R. Abdal, W. Yifan, Z. Shi, Y. Xu, R. Po, Z. Kuang, Q. Chen, D.Y. Yeung, and G. Wetzstein, “Gaussian shell maps for efficient 3d human generation,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[246] S. Zheng, B. Zhou, R. Shao, B. Liu, S. Zhang, L. Nie, and Y. Liu, “Gps-gaussian: Generalizable pixel-wise 3d gaussian splatting for real-time human novel view synthesis,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[247] L. Hu, H. Zhang, Y. Zhang, B. Zhou, B. Liu, S. Zhang, and L. Nie, “Gaussianavatar: Towards realistic human avatar modeling from a single video via animatable 3d gaussians,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[248] H. Pang, H. Zhu, A. Kortylewski, C. Theobalt, and M. Habermann, “Ash: Animatable gaussian splats for efficient and photoreal human rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[249] Z. Qian, S. Wang, M. Mihajlovic, A. Geiger, and S. Tang, “3dgsavatar: Animatable avatars via deformable 3d gaussian splatting,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[250] H. Jung, N. Brasch, J. Song, E. Perez-Pellitero, Y. Zhou, Z. Li, N. Navab, and B. Busam, “Deformable 3d gaussian splatting for animatable human avatars,” arXiv preprint arXiv:2312.15059, 2023.

[251] M. Li, J. Tao, Z. Yang, and Y. Yang, “Human101: Training 100+ fps human gaussians in 100s from 1 view,” arXiv preprint arXiv:2312.15258, 2023.

[252] M. Li, S. Yao, Z. Xie, K. Chen, and Y.-G. Jiang, “Gaussianbody: Clothed human reconstruction via 3d gaussian splatting,” arXiv preprint arXiv:2401.09720, 2024.

[253] J. Xiang, X. Gao, Y. Guo, and J. Zhang, “Flashavatar: Highfidelity digital avatar rendering at 300fps,” arXiv preprint arXiv:2312.02214, 2023.

[254] Y. Chen, L. Wang, Q. Li, H. Xiao, S. Zhang, H. Yao, and Y. Liu, “Monogaussianavatar: Monocular gaussian point-based head avatar,” arXiv preprint arXiv:2312.04558, 2023.

[255] Z. Zhao, Z. Bao, Q. Li, G. Qiu, and K. Liu, “Psavatar: A pointbased morphable shape model for real-time head avatar creation with 3d gaussian splatting,” arXiv preprint arXiv:2401.12900, 2024.

[256] A. Rivero, S. Athar, Z. Shu, and D. Samaras, “Rig3dgs: Creating controllable portraits from casual monocular videos,” arXiv preprint arXiv:2402.03723, 2024.

[257] H. Luo, M. Ouyang, Z. Zhao, S. Jiang, L. Zhang, Q. Zhang, W. Yang, L. Xu, and J. Yu, “Gaussianhair: Hair modeling and rendering with light-aware gaussians,” arXiv preprint arXiv:2402.10483, 2024.

[258] Y. Wang, Y. Long, S. H. Fan, and Q. Dou, “Neural rendering for stereo 3d reconstruction of deformable tissues in robotic surgery,” in Proc. Int. Conf. Med. Image Comput. Comput. Assist. Interv., 2022, pp. 431–441.

[259] C. Yang, K. Wang, Y. Wang, X. Yang, and W. Shen, “Neural lerplane representations for fast 4d reconstruction of deformable tissues,” in Proc. Int. Conf. Med. Image Comput. Comput. Assist. Interv., 2023, pp. 46–56.

[260] R. Zha, X. Cheng, H. Li, M. Harandi, and Z. Ge, “Endosurf: Neural surface reconstruction of deformable tissues with stereo endoscope videos,” in Proc. Int. Conf. Med. Image Comput. Comput. Assist. Interv., 2023, pp. 13–23.

[261] J. Straub, T. Whelan, L. Ma, Y. Chen, E. Wijmans, S. Green, J. J. Engel, R. Mur-Artal, C. Ren, S. Verma et al., “The replica dataset: A digital replica of indoor spaces,” arXiv preprint arXiv:1906.05797, 2019.

[262] E. Sucar, S. Liu, J. Ortiz, and A. J. Davison, “imap: Implicit mapping and positioning in real-time,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 6229–6238.

[263] X. Yang, H. Li, H. Zhai, Y. Ming, Y. Liu, and G. Zhang, “Voxfusion: Dense tracking and mapping with voxel-based neural implicit representation,” in IEEE International Symposium on Mixed and Augmented Reality, 2022, pp. 499–507.

[264] Z. Zhu, S. Peng, V. Larsson, W. Xu, H. Bao, Z. Cui, M. R. Oswald, and M. Pollefeys, “Nice-slam: Neural implicit scalable encoding for slam,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 12 786–12 796.

[265] M. M. Johari, C. Carta, and F. Fleuret, “Eslam: Efficient dense slam system based on hybrid representation of signed distance fields,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 17 408–17 419.

[266] E. Sandström, Y. Li, L. Van Gool, and M. R. Oswald, “Point-slam: Dense neural point cloud-based slam,” in Proc. IEEE Int. Conf. Comput. Vis., 2023, pp. 18 433–18 444.

[267] H. Wang, J. Wang, and L. Agapito, “Co-slam: Joint coordinate and sparse parametric encodings for neural real-time slam,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 13 293–13 302.

[268] Y. Hu, Y. Fang, Z. Ge, Z. Qu, Y. Zhu, A. Pradhana, and C. Jiang, “A moving least squares material point method with displacement discontinuity and two-way rigid body coupling,” ACM Trans. Graph., vol. 37, no. 4, pp. 1–14, 2018.

[269] M. Müller, B. Heidelberger, M. Hennix, and J. Ratcliff, “Position based dynamics,” Journal of Visual Communication and Image Representation, vol. 18, no. 2, pp. 109–118, 2007.

[270] A. Knapitsch, J. Park, Q.-Y. Zhou, and V. Koltun, “Tanks and temples: Benchmarking large-scale scene reconstruction,” ACM Trans. Graph., vol. 36, no. 4, pp. 1–13, 2017.

[271] T. Zhou, R. Tucker, J. Flynn, G. Fyffe, and N. Snavely, “Stereo magnification: learning view synthesis using multiplane images,” ACM Trans. Graph., vol. 37, no. 4, pp. 1–12, 2018.

[272] P. Hedman, J. Philip, T. Price, J.-M. Frahm, G. Drettakis, and G. Brostow, “Deep blending for free-viewpoint image-based rendering,” ACM Trans. Graph., vol. 37, no. 6, pp. 1–15, 2018.

[273] B. Mildenhall, P. P. Srinivasan, R. Ortiz-Cayon, N. K. Kalantari, R. Ramamoorthi, R. Ng, and A. Kar, “Local light field fusion: Practical view synthesis with prescriptive sampling guidelines,” ACM Trans. Graph., vol. 38, no. 4, pp. 1–14, 2019.

[274] A. Liu, R. Tucker, V. Jampani, A. Makadia, N. Snavely, and A. Kanazawa, “Infinite nature: Perpetual view generation of natural scenes from a single image,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 14 458–14 467.

[275] J. Sturm, N. Engelhard, F. Endres, W. Burgard, and D. Cremers, “A benchmark for the evaluation of rgb-d slam systems,” in Proc. IEEE/RSJ Int. Conf. Intell. Robot. Syst., 2012, pp. 573–580.

[276] A. Geiger, P. Lenz, and R. Urtasun, “Are we ready for autonomous driving? the kitti vision benchmark suite,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2012, pp. 3354–3361.

[277] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, “Scannet: Richly-annotated 3d reconstructions of indoor scenes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2017, pp. 5828–5839.

[278] P. Sun, H. Kretzschmar, X. Dotiwalla, A. Chouard, V. Patnaik, P. Tsui, J. Guo, Y. Zhou, Y. Chai, B. Caine et al., “Scalability in perception for autonomous driving: Waymo open dataset,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2020, pp. 2446–2454.

[279] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A multimodal dataset for autonomous driving,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2020, pp. 11 621–11 631.

[280] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” IEEE Robotics and Automation Letters, vol. 5, no. 2, pp. 3019–3026, 2020.

[281] A. Mandlekar, D. Xu, J. Wong, S. Nasiriany, C. Wang, R. Kulkarni, L. Fei-Fei, S. Savarese, Y. Zhu, and R. Martı́n-Martı́n, “What matters in learning from offline human demonstrations for robot manipulation,” in Proc. Annu. Conf. Robot Learn., 2022, pp. 1678–1690.

[282] Z. Yan, C. Li, and G. H. Lee, “Nerf-ds: Neural radiance fields for dynamic specular objects,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 8285–8295.

[283] K. Kania, K. M. Yi, M. Kowalski, T. Trzciński, and A. Tagliasacchi, “Conerf: Controllable neural radiance fields,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 18 623–18 632.

[284] A. Mirzaei, T. Aumentado-Armstrong, K. G. Derpanis, J. Kelly, M. A. Brubaker, I. Gilitschenski, and A. Levinshtein, “Spin-nerf: Multiview segmentation and perceptual inpainting with neural radiance fields,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 20 669–20 679.

[285] R. Shao, Z. Zheng, H. Tu, B. Liu, H. Zhang, and Y. Liu, “Tensor4d: Efficient neural 4d decomposition for high-fidelity dynamic reconstruction and rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 16 632–16 642.

[286] T. Wu, J. Zhang, X. Fu, Y. Wang, J. Ren, L. Pan, W. Wu, L. Yang, J. Wang, C. Qian et al., “Omniobject3d: Large-vocabulary 3d object dataset for realistic perception, reconstruction and generation,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 803–814.

[287] M. Deitke, D. Schwenk, J. Salvador, L. Weihs, O. Michel, E. VanderBilt, L. Schmidt, K. Ehsani, A. Kembhavi, and A. Farhadi, “Objaverse: A universe of annotated 3d objects,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 13 142–13 153.

[288] T. Alldieck, M. Magnor, W. Xu, C. Theobalt, and G. Pons-Moll, “Video based reconstruction of 3d people models,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2018, pp. 8387–8397.

[289] D. Cudeiro, T. Bolkart, C. Laidlaw, A. Ranjan, and M. J. Black, “Capture, learning, and synthesis of 3d speaking styles,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2019, pp. 10 101–10 111.

[290] Z. Zheng, T. Yu, Y. Wei, Q. Dai, and Y. Liu, “Deephuman: 3d human reconstruction from a single image,” in Proc. IEEE Int. Conf. Comput. Vis., 2019, pp. 7739–7749.

[291] T. Yu, Z. Zheng, K. Guo, P. Liu, Q. Dai, and Y. Liu, “Function4d: Real-time human volumetric capture from very sparse consumer rgbd sensors,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2021, pp. 5746–5756.

[292] S. Peng, Y. Zhang, Y. Xu, Q. Wang, Q. Shuai, H. Bao, and X. Zhou, “Neural body: Implicit neural representations with structured latent codes for novel view synthesis of dynamic humans,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2021, pp. 9054–9063.

[293] E. Ramon, G. Triginer, J. Escur, A. Pumarola, J. Garcia, X. Giro-i Nieto, and F. Moreno-Noguer, “H3d-net: Few-shot high-fidelity 3d head reconstruction,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 5620–5629.

[294] Z. Su, T. Yu, Y. Wang, and Y. Liu, “Deepcloth: Neural garment representation for shape and style editing,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 2, pp. 1581–1593, 2022.

[295] M. Allan, J. Mcleod, C. Wang, J. C. Rosenthal, Z. Hu, N. Gard, P. Eisert, K. X. Fu, T. Zeffiro, W. Xia et al., “Stereo correspondence and reconstruction of endoscopic data challenge,” arXiv preprint arXiv:2101.01133, 2021.

[296] Y. Cai, J. Wang, A. Yuille, Z. Zhou, and A. Wang, “Structureaware sparse-view x-ray 3d reconstruction,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024, pp. 11 174–11 183.

[297] Y. Xiangli, L. Xu, X. Pan, N. Zhao, A. Rao, C. Theobalt, B. Dai, and D. Lin, “Bungeenerf: Progressive neural radiance field for extreme multi-scale scene rendering,” in Proc. Eur. Conf. Comput. Vis. Springer, 2022, pp. 106–122.

[298] M. Tancik, V. Casser, X. Yan, S. Pradhan, B. Mildenhall, P. P. Srinivasan, J. T. Barron, and H. Kretzschmar, “Block-nerf: Scalable large scene neural view synthesis,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 8248–8258.

[299] G. Yang, F. Xue, Q. Zhang, K. Xie, C.-W. Fu, and H. Huang, “Urbanbis: a large-scale benchmark for fine-grained urban building instance segmentation,” in Proc. ACM Spec. Interest Group Comput. Graph. Interact. Tech., 2023, pp. 1–11.

[300] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: from error visibility to structural similarity,” IEEE Trans. Image Process., vol. 13, no. 4, pp. 600–612, 2004.

[301] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The unreasonable effectiveness of deep features as a perceptual metric,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2018, pp. 586–595.

[302] J. Fang, T. Yi, X. Wang, L. Xie, X. Zhang, W. Liu, M. Nießner, and Q. Tian, “Fast dynamic radiance fields with time-aware neural voxels,” in SIGGRAPH Asia, 2022, pp. 1–9.

[303] A. Cao and J. Johnson, “Hexplane: A fast representation for dynamic scenes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 130–141.

[304] F. Wang, Z. Chen, G. Wang, Y. Song, and H. Liu, “Masked spacetime hash encoding for efficient dynamic scene reconstruction,” in Proc. Adv. Neural Inf. Process. Syst., 2023.

[305] C.-Y. Weng, B. Curless, P. P. Srinivasan, J. T. Barron, and I. Kemelmacher-Shlizerman, “Humannerf: Free-viewpoint rendering of moving people from monocular video,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2022, pp. 16 210–16 220.

[306] C. Geng, S. Peng, Z. Xu, H. Bao, and X. Zhou, “Learning neural volumetric representations of dynamic humans in minutes,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2023, pp. 8759–8770.

[307] S. Peng, J. Dong, Q. Wang, S. Zhang, Q. Shuai, X. Zhou, and H. Bao, “Animatable neural radiance fields for modeling dynamic human bodies,” in Proc. IEEE Int. Conf. Comput. Vis., 2021, pp. 14 314–14 323.

[308] A. Yu, V. Ye, M. Tancik, and A. Kanazawa, “pixelnerf: Neural radiance fields from one or few images,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2021, pp. 4578–4587.

[309] Y. Kwon, D. Kim, D. Ceylan, and H. Fuchs, “Neural human performer: Learning generalizable radiance fields for human performance rendering,” in Proc. Adv. Neural Inf. Process. Syst., 2021, pp. 24 741–24 752.

[310] J. Wang, Z. Zhang, Q. Zhang, J. Li, J. Sun, M. Sun, J. He, and R. Xu, “Query-based semantic gaussian field for scene representation in reinforcement learning,” arXiv preprint arXiv:2406.02370, 2024.

[311] Y. Qu, S. Dai, X. Li, J. Lin, L. Cao, S. Zhang, and R. Ji, “Goi: Find 3d gaussians of interest with an optimizable open-vocabulary semantic-space hyperplane,” arXiv preprint arXiv:2405.17596, 2024.

[312] Y. Ji, H. Zhu, J. Tang, W. Liu, Z. Zhang, Y. Xie, L. Ma, and X. Tan, “Fastlgs: Speeding up language embedded gaussians with feature grid mapping,” arXiv preprint arXiv:2406.01916, 2024.

[313] G. Liao, J. Li, Z. Bao, X. Ye, J. Wang, Q. Li, and K. Liu, “Clip-gs: Clip-informed gaussian splatting for real-time and view-consistent 3d semantic understanding,” arXiv preprint arXiv:2404.14249, 2024.

[314] S. Choi, H. Song, J. Kim, T. Kim, and H. Do, “Click-gaussian: Interactive segmentation to any 3d gaussians,” arXiv preprint arXiv:2407.11793, 2024.

[315] S. Ji, G. Wu, J. Fang, J. Cen, T. Yi, W. Liu, Q. Tian, and X. Wang, “Segment any 4d gaussians,” arXiv preprint arXiv:2407.04504, 2024.

[316] A. Guédon and V. Lepetit, “Sugar: Surface-aligned gaussian splatting for efficient 3d mesh reconstruction and high-quality mesh rendering,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2024.

[317] T. Liu, G. Wang, S. Hu, L. Shen, X. Ye, Y. Zang, Z. Cao, W. Li, and Z. Liu, “Fast generalizable gaussian splatting reconstruction from multi-view stereo,” in Proc. Eur. Conf. Comput. Vis., 2024.

[318] Y. Li, X. Fu, S. Zhao, R. Jin, and S. K. Zhou, “Sparse-view ct reconstruction with 3d gaussian volumetric representation,” arXiv preprint arXiv:2312.15676, 2023.

[319] Y. Cai, Y. Liang, J. Wang, A. Wang, Y. Zhang, X. Yang, Z. Zhou, and A. Yuille, “Radiative gaussian splatting for efficient x-ray novel view synthesis,” in Proc. Eur. Conf. Comput. Vis., 2024.

[320] J. Chang, Y. Xu, Y. Li, Y. Chen, and X. Han, “Gaussreg: Fast 3d registration with gaussian splatting,” in Proc. Eur. Conf. Comput. Vis., 2024.

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