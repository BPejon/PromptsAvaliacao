# TABLE II: Data source description.

| Source | Description |
| --- | --- |
| Web and Internet content | High-quality web crawl datasets containing billions of pages from diverse internet sources, including news articles, blogs, and general web content. These datasets undergo extensive cleaning and deduplication processes to ensure text quality for language model training. |
| Books and literary works | Digitized collections of books spanning various genres, languages, and time periods. Sources include public domain texts, open-access libraries, and e-book platforms, providing rich narrative content and diverse writing styles. |
| Encyclopedias and knowledge bases | Structured knowledge repositories like Wikipedia and other encyclopedic sources across multiple languages. These provide factual, well-organized information on diverse topics with consistent formatting and citation standards. |
| Academic and research resources | Peer-reviewed papers, preprints, theses, and scholarly publications from repositories like arXiv and academic databases. These sources offer technical, specialized content with rigorous methodology and domain expertise. |
| Social media and forums | User-generated content from platforms like Reddit and Stack Exchange, capturing conversational language, community discussions, and Q&A formats that reflect natural human communication patterns. |
| Integration of existing datasets | Curated collections that combine and refine multiple existing open-source datasets, leveraging previous data curation efforts to create comprehensive training corpora. |
| Scientific databases | Specialized repositories containing structured scientific data including biomedical literature, protein sequences, chemical compounds, clinical trials, astronomical observations, and materials science data from authoritative institutions. |
| Patent databases | Technical documentation from global patent offices including USPTO, EPO, and WIPO, containing detailed descriptions of innovations, technical specifications, and claims across various technological domains. |
| Comprehensive multi-source integration | Large-scale datasets that aggregate content from multiple source types (web, books, code, academic papers) to create diverse, balanced training corpora. |
| Other sources | Additional specialized or proprietary content sources that don’t fit into the above categories, potentially including domain-specific databases, institutional archives, or unique text collections. |

# TABLE III: Data type description.

| Type | Description |
| --- | --- |
| Raw text | A broad umbrella for any string-serializable content, e.g., natural language plus tables, sequences, code, logs, etc. Used for language modeling or domain pretraining without explicit prompts/answers or paired media. |
| Text QA | Text-only question-answer pairs, optionally with supporting passages, supervising reading comprehension or factual reasoning. |
| Text QA with CoT | Text QA augmented with explicit multi-step explanations or derivations alongside the final answer. |
| VQA | Visual question-answering pairs, where each image is with a question and the corresponding answer. |
| VQA (multi-image) | A question grounded on two or more related images, requiring cross-image comparison, temporal alignment, or aggregation. |
| VQA with CoT | VQA data augmented with step-by-step rationales or intermediate reasoning traces in addition to the final answer. |
| Image-text | Image-text pairs, where the text contains description (e.g., captions, reports) for alignment, captioning, retrieval, or representation learning. |
| Video-text | Video-text pairs, where the text contains description (e.g., subtitles, transcripts, narrations) for alignment, captioning, retrieval, or representation learning. |
| Classification, regression, generation, etc. | For numeric/matrix/graph records lacking natural-language pairing, annotate by supervised objective. |

# TABLE IV: Summary of pre-training and post-training datasets for scientific LLMs/MLLMs. [link] directs to dataset websites.

| Scientific Domain | Dataset | Subdomain | Modality | Purpose | Type | Release | Language | Source | Annotation Pipeline | Human Annotators | Human Tasks | Auto-annotation Tools | Size |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Life Sciences | MIRAGE [190] [link] | Agriculture | Biological entity photos | SFT | VQA (multi-image) | 2025.06 | EN | Scientific databases | Semi-automated | N/A | Data generation | GPT-4.1 | 37,512 |
|  | CROP [722] [link] | Agriculture | Academic papers | SFT | Text QA | 2024.09 | EN, ZH | Academic and research resources | Semi-automated | N/A | Data generation | GPT-4 | 211,909 |
|  | ToT-Biology [link] | General Biology | Biomedical QA | SFT, CoT | Text QA with CoT | 2025.01 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 23,000 |
|  | BioASQ10b-factoid [768] [link] | General Biology | Clinical dialogue | SFT | Text QA | 2023.07 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 1.25K |
|  | ReasonMed [733] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT, CoT | Text QA with CoT | 2025.06 | EN | Comprehensive multi-source inte- gration | Automated | N/A | N/A | Qwen-2.5-72B, DeepSeek-R1- Distill-Llama-70B, HuatuoGPT-o1-70B | 194,925 |
|  | Open-PMC-18M [868] [link] | Healthcare and Medical Sciences | CT, CFP | Pre-training | Image-text | 2025.06 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 25,000,000 |
|  | ReXVQA [869] [link] | Healthcare and Medical Sciences | X-ray | SFT | VQA | 2025.06 | EN | Integration of existing datasets | Semi-automated | 3 | Data review | GPT-4o, ClinicalBERT, MedEmbed | 613,277 |
|  | RexGradient-160K [870] [link] | Healthcare and Medical Sciences | X-ray | Pre-training, SFT | Image-text | 2025.05 | EN | Scientific databases | Manual | N/A | N/A | N/A | 160K |
|  | AlphaMed19K [871] [link] | Healthcare and Medical Sciences | Biomedical QA | SFT, CoT | Text QA | 2025.05 | EN | Integration of existing datasets | Automated | N/A | Data generation and review | N/A | 19,178 |
|  | Derm1M [872] [link] | Healthcare and Medical Sciences | Dermatological images | Pre-training | Image-text | 2025.3 | EN | Social media and forums, Aca- demic and research resources | Automated | N/A | N/A | DenseNet, DINO, GPT-4o, Whisper | 1,029,761 |
|  | MedVideoCap-55K [663] [link] | Healthcare and Medical Sciences | Medical videos | Pre-training, SFT | Video-text | 2025.04 | EN | Web and Internet content | Automated | N/A | Data review | GPT-4o | 55,803 |
|  | medical-o1-reasoning-SFT [543] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT, CoT | Text QA with CoT | 2025.04 | EN, ZH | Comprehensive multi-source inte- gration | Automated | N/A | N/A | DeepSeek-R1 | 90,200 |
|  | GMAI-Reasoning10K [545] [link] | Healthcare and Medical Sciences | CT, Dermatology, Endoscopy, Histopathology, MRI, Microscopy, PET, US, X-ray, etc. | CFP, OCT, SFT | VQA | 2025.04 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4o | 17,004 |
|  | MedReason [732] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT, CoT | Text QA with CoT | 2025.03 | EN | Comprehensive multi-source inte- gration | Automated | N/A | N/A | N/A | 32,682 |
|  | GEMeX-VQA [873] [link] | Healthcare and Medical Sciences | X-ray | Pre-training, SFT | VQA | 2025.03 | EN | Integration of existing datasets | Semi-automated | N/A | Data review | OpenBioLLM-70B, GPT-4o | 1,601,615 |
|  | MIMIC-Diff-VQA [795] [link] | Healthcare and Medical Sciences | X-ray | SFT | VQA (multi-image) | 2025.02 | EN | Scientific databases | Semi-automated | 3 | Data generation and review | ScispaCy | 630,633 |
|  | ICG-CXR [874] [link] | Healthcare and Medical Sciences | X-ray | SFT | VQA (multi-image) | 2025.03 | EN | Scientific databases | Automated | N/A | Data generation and review | GPT-4 | 11,439 |
|  | VL-Health [875] [link] | Healthcare and Medical Sciences | CT, CFP, MRI, Microscopy, OCT, US, | X-ray Pre-training, SFT | Image-text, VQA | 2025.02 | EN, ZH | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4o | 1,548,847 |
|  | BIOMEDICA [203] [link] | Healthcare and Medical Sciences | Academic papers | Pre-training | Raw text | 2025.01 | EN | Academic and research resources | Semi-automated | 7 | Data review | N/A | 2,400,000 |
|  | AfriMed-QA v2 [876] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2024.11 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | N/A | N/A | 15,275 |
|  | GMAI-VL-5.5M [541] [link] | Healthcare and Medical Sciences | CT, Dermatology, Endoscopy, Histopathology, MRI, Microscopy, PET, US, X-ray, etc. | CFP, OCT, SFT | VQA, Text QA | 2024.11 | EN, ZH | Comprehensive multi-source inte- gration | Semi-automated | 5 | Data review | GPT-4o | 5.5M |
|  | OphVL [664] [link] | Healthcare and Medical Sciences | Ophthalmic Surgical Video | Pre-training | Video-text | 2024.11 | EN | Web and Internet content | Automated | N/A | Data generation and review | SurgicBERTa, GPT- 4o | 375,198 |
|  | Bora-v1 [877] [link] | Healthcare and Medical Sciences | Endoscopy, MRI, Microscopy, US | SFT | Video-text | 2024.10 | EN | Integration of existing datasets | Automated | N/A | Data review | N/A | 4,897 |
|  | MedSyn [878] [link] | Healthcare and Medical Sciences | Clinical documentation | Pre-training | Raw text | 2024.08 | RU | Academic and research resources | Automated | N/A | N/A | GPT-4, Medical Knowledge Graph | 41,200 |
|  | RealMedQA [879] [link] | Healthcare and Medical Sciences | Biomedical QA | SFT | Text QA | 2024.08 | EN | Encyclopedias and knowledge bases | Semi-automated | 6 | Data generation and review | GPT-3.5-turbo | 1,200 |
|  | MedTrinity-25M [880] [link] | Healthcare and Medical Sciences | CT, MRI, X-ray, Histopathology, etc. | Pre-training | Image-text, VQA | 2024.08 | EN | Integration of existing datasets, Sci- entific databases | Automated | N/A | N/A | N/A | 25,000,000 |
|  | MedPix-single [881] [link] | Healthcare and Medical Sciences | CT, MRI, US, X-ray | Pre-training | Image-text | 2024.07 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 59,000 |
|  | BIMCV-R [882] [link] | Healthcare and Medical Sciences | CT | Pre-training | Image-text | 2024.07 | EN | Scientific databases | Semi-automated | 20+ | Data review | GPT-4 | 8,069 |
|  | MIMIC-Ext-MIMIC-CXR-VQA [883] [link] | Healthcare and Medical Sciences | X-ray | Pre-training, SFT | VQA | 2024.07 | EN | Integration of existing datasets | Semi-automated | 4 | Data review | GPT-4 | 377,391 |
|  | EHRXQA [703] [link] | Healthcare and Medical Sciences | X-ray | Pre-training, SFT | VQA | 2024.07 | EN | Integration of existing datasets | Semi-automated | 4 | Data review | GPT-4 | 46,152 |
|  | CheXpertPlus [656] [link] | Healthcare and Medical Sciences | X-ray | Pre-training | Image-text | 2024.06 | EN | Scientific databases | Semi-automated | 10 | Data generation and review | CheXbert, Radgraph | 223,228 |
|  | PubMedVision [540] [link] | Healthcare and Medical Sciences | CT, Endoscopy, CFP, Infrared Reflectance, MRI, Microscopy, OCT, US, X-ray | SFT | VQA | 2024.06 | EN | Academic and research resources | Automated | N/A | N/A | GPT-4, GPT-4V, SentenceBERT | 1,294,092 |
|  | MediQ [653] [link] | Healthcare and Medical Sciences | EHR | SFT | Text QA | 2024.06 | EN | Academic and research resources | Automated | N/A | N/A | GPT-3.5, LLaMA-3 | 2,545 |
|  | HuatuoGPT2-SFT-GPT4-140K [42] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2024.06 | ZH | Other sources | Automated | N/A | Data generation and review | GPT-4 | 140,000 |
|  | Asclepius-Synthetic-Clinical-Notes [link] | Healthcare and Medical Sciences | EHR | SFT | Text QA | 2024.06 | EN | Academic and research resources | Semi-automated | N/A | Data generation | GPT-3.5 | 158,114 |
|  | Know Medical Dialogues [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2024.06 | EN | Web and Internet content | Automated | N/A | N/A | N/A | 480 |
|  | Duvel [link] | Healthcare and Medical Sciences | Academic papers | SFT | Classification | 2024.05 | EN | Scientific databases | Semi-automated | N/A | Data generation | ALAMBIC | 6,553 |
|  | SkinCAP [884] [link] | Healthcare and Medical Sciences | Dermatology | Pre-training | Image-text | 2024.05 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 4,000 |
|  | MM-Retinal [885] [link] | Healthcare and Medical Sciences | CFP, FFA, OCT | Pre-training, SFT | Image-text | 2024.05 | EN, ZH | Academic and research resources | Semi-automated | 6 | Data review | N/A | 4,349 |
|  | M3D-Data (caption) [659] [link] | Healthcare and Medical Sciences | CT, Clinical reports | Pre-training, SFT | Image-text, Text QA, VQA | 2024.04 | EN | Scientific databases, Integration of existing datasets | Semi-automated | N/A | Data generation and review | GPT-4V | 120,092 |
|  | M3D-Data (instruction) [659] [link] | Healthcare and Medical Sciences | CT, Clinical reports | SFT | Image-text, Text QA, VQA | 2024.04 | EN | Scientific databases, Integration of existing datasets | Semi-automated | N/A | Data generation and review | GPT-4V | 58,180 |
|  | RadGenome-Chest CT [886] [link] | Healthcare and Medical Sciences | CT | Pre-training, SFT | VQA, Image-text | 2024.04 | EN | Academic and research resources | Semi-automated | N/A | Data review | SAT, GPT-4, GPT-2 | 1,965,000 |
|  | CXR-LLM [link] | Healthcare and Medical Sciences | X-ray | SFT | VQA | 2024.03 | EN | Integration of existing datasets | Semi-automated | N/A | Data generation | GPT-4 | 104,892 |
|  | MedChatZH [887] [link] | Healthcare and Medical Sciences | Clinical dialogue | Pre-training, SFT | Text QA | 2024.03 | ZH | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation | N/A | 2,068,823 |
|  | Mental health chatbot dataset [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2024.02 | EN | Web and Internet content | Automated | N/A | N/A | N/A | 172 |
|  | StatPearls [888] [link] | Healthcare and Medical Sciences | Academic papers | Pre-training | Raw text | 2024.02 | EN | Scientific databases | Automated | N/A | N/A | N/A | 301,202 |
|  | Quilt-Instruct [889] [link] | Healthcare and Medical Sciences | Histopathology | SFT | VQA | 2024.02 | EN | Web and Internet content | Semi-automated | N/A | Data review | GPT-4-turbo | 107,131 |
|  | SHADR [673] [link] | Healthcare and Medical Sciences | EHR | SFT | Classification | 2024.01 | EN | Scientific databases | Semi-automated | N/A | Data review | GPT-3.5 | 446 |
|  | RJUA-QA [890] [link] | Healthcare and Medical Sciences | Dianosis report, Clinical dialogue | SFT | Text QA | 2023.12 | ZH | Other sources | Manual | N/A | Data generation and review | N/A | 1,705 |
|  | RP3D-DiagDS [773] [link] | Healthcare and Medical Sciences | CT, MRI, X-ray US, Fluoroscopy, etc. | Pre-training | Classification | 2023.12 | EN | Scientific databases | Semi-automated | N/A | Data generation and review | Custom crawlers, GPT-4 | 40,936 |
|  | PMC-Inline [657] [link] | Healthcare and Medical Sciences | CT, MRI, PET, US, X-ray | Pre-training | Image-text | 2023.11 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 11,000,000 |
|  | ROCOv2 [660] [link] | Healthcare and Medical Sciences | CT, MRI, PET, US, X-ray | Pre-training, SFT | Image-text | 2023.11 | EN | Academic and research resources | Semi-automated | N/A | N/A | fastText, MedCAT | 80,080 |
|  | PMC-CaseReport [657] [link] | Healthcare and Medical Sciences | X-ray | SFT | Image-text, VQA | 2023.11 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 1,100,000 |
|  | MedMD [657] [link] | Healthcare and Medical Sciences | CT, MRI, PET, US, X-ray | Pre-training, SFT | Image-text, VQA | 2023.11 | EN | Academic and research resources | Semi-automated | 8 | Data review | ChatGPT | 16,000,000 |
|  | Taiyi-Instruction-Data-001 [891] [link] | Healthcare and Medical Sciences | Dianosis report, Clinical dialogue, Academic papers, etc. | EMR, Pre-training, SFT | Text QA | 2023.11 | EN, ZH | Integration of existing datasets | Automated | N/A | Data review | N/A | 1,114,315 |
|  | MTS-DIALOG [892] [link] | Healthcare and Medical Sciences | Clinical dialogue | Pre-training | Text QA | 2023.11 | EN | Academic and research resources | Semi-automated | 12 | Data generation and review | GPT-4o | 23,977 |
|  | MTS-Dialog [892] [link] | Healthcare and Medical Sciences | Clinical dialogue | Pre-training | Raw text | 2023.11 | EN | Patent databases | Semi-automated | 9 | Data generation and review | OPUS-MT, BART | 1,701 |
|  | Clinical Guidelines [38] [link] | Healthcare and Medical Sciences | Clinical guidelines | Pre-training | Text QA with CoT | 2023.11 | EN | Scientific databases | Semi-automated | N/A | Data review | S2ORC, GROBID | 38,000 |
|  | INSPECT [893] [link] | Healthcare and Medical Sciences | CT | Pre-training | Image-text | 2023.11 | EN | Scientific databases | Semi-automated | N/A | Data review, Data generation | Clinical Longformer | 23,248 |
|  | AeroPath [894] [link] | Healthcare and Medical Sciences | CT | Agent | Segmentation | 2023.11 | EN | Scientific databases | Semi-automated | 2 | Data review | 3D Slicer | 27 (CT scans) |
|  | MORFITT [895] [link] | Healthcare and Medical Sciences | Clinical papers | Pre-training | Classification | 2023.11 | FR | Academic and research resources | Manual | N/A | Data review | N/A | 3,556 |
|  | NoteChat [702] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.10 | EN | Integration of existing datasets | Automated | N/A | N/A | N/A | 207,000 |
|  | ChiMed-VL [896] [link] | Healthcare and Medical Sciences | X-ray, CT, MRI, etc. | Pre-training, SFT | Image-text, Text QA | 2023.10 | ZH, EN | Integration of existing datasets | Automated | N/A | N/A | GPT-3.5 | 1,049,455 |
|  | OncQA [897] [link] | Healthcare and Medical Sciences | Dianosis report | SFT | Text QA | 2023.10 | EN | Other sources | Manual | 6 | Data generation and review | GPT-4 | 156 |
|  | SDOH-NLI [898] [link] | Healthcare and Medical Sciences | Clinical notes | Pre-training | Classification | 2023.10 | EN | Integration of existing datasets | Manual | N/A | Data generation | N/A | 21.1K |
|  | CMtMedQA [899] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.08 | ZH | Other sources | Automated | N/A | Data review | N/A | 68,000 |
|  | DISC-Med-SFT [900] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.08 | ZH | Integration of existing datasets | Semi-automated | N/A | Data review | GPT-3.5, GPT-4 | 470,000 |
|  | Healix-V1 [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.07 | EN | Comprehensive multi-source inte- gration | N/A | N/A | N/A | N/A | 796,239 |
|  | Medical Cord19 [589] [link] | Healthcare and Medical Sciences | Academic papers | Pre-training | Raw text | 2023.07 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 250,000 |
|  | Pile-PubMed Central [651] [link] | Healthcare and Medical Sciences | Academic papers | Pre-training | Raw text | 2023.07 | EN | Academic and research resources | Automated | N/A | Data generation | N/A | N/A |
|  | AGCT [901] [link] | Healthcare and Medical Sciences | Biomedical knowledge base | Pre-training | Raw text | 2023.07 | EN, FR | Scientific databases | Automated | N/A | N/A | Custom generation | 421,216 |
|  | Synthetic CSAW 100k Mammograms [902] [link] | Healthcare and Medical Sciences | Mammography | SFT | Image-text | 2023.07 | EN | Scientific databases | Automated | N/A | N/A | Diffusion Model | 100K |
|  | Quilt-1M [150] [link] | Healthcare and Medical Sciences | Histopathology | Pre-training, SFT | Image-text | 2023.06 | EN | Academic and research resources, Web and Internet content, Other sources | Automated | N/A | N/A | N/A | 1,000,000 |
|  | LLaVA-Med [903] [link] | Healthcare and Medical Sciences | CT, Histopathology, MRI, Microscopy, US, X-ray | PET, Pre-training, SFT | VQA, Image-text | 2023.06 | EN | Comprehensive multi-source inte- gration | Automated | N/A | N/A | GPT-4 | 630,000 |
|  | ShenNong-TCM-Dataset [904] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT, CoT | Text QA | 2023.06 | ZH | Comprehensive multi-source inte- gration | Automated | N/A | Data generation | ChatGPT | 113,000 |
|  | PMC-VQA [905] [link] | Healthcare and Medical Sciences | CT, CFP, Histopathology, MRI, Microscopy, US, X-ray | SFT | VQA | 2023.05 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 226,946 |
|  | ChatMed-Consult-Dataset [906] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.05 | ZH | Web and Internet content | Automated | N/A | Data generation | GPT-3.5-Turbo | 549,000 |
|  | QiZhenGPT-20k [907] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.05 | ZH | Other sources | Automated | N/A | Data generation | N/A | 20,000 |
|  | Huatuo-26M [908] [link] | Healthcare and Medical Sciences | Biomedical QA | Pre-training, SFT | Text QA | 2023.05 | EN | Encyclopedias and knowledge bases | Semi-automated | N/A | Data review | Bert, T5 | 26,000,000 |
|  | Huatuo26M-Lite [908] [link] | Healthcare and Medical Sciences | Clinical dialogue, Dianosis report | Pre-training, SFT | Text QA | 2023.05 | ZH | Web and Internet content | Semi-automated | N/A | Data review | ChatGPT | 177,703 |
|  | Visual Med-Alpaca [link] | Healthcare and Medical Sciences | CT, CFP, Histopathology, MRI, Microscopy, US, X-ray | SFT | VQA | 2023.04 | EN | Scientific databases | Automated | N/A | N/A | GPT-3.5 | 54,000 |
|  | MedAlpaca [520] [link] | Healthcare and Medical Sciences | Clinical dialogue, Academic papers | Pre-training, SFT | Raw text, Text QA | 2023.04 | EN | Comprehensive multi-source inte- gration | Automated | N/A | Data generation and review | N/A | 860,076 |
|  | Med-ChatGLM [909] [link] | Healthcare and Medical Sciences | Biomedical knowledge base | SFT | Text QA | 2023.04 | ZH | Integration of existing datasets | Automated | N/A | Data generation | GPT-3.5 | 7,622 |
|  | PMC-OA [204] [link] | Healthcare and Medical Sciences | CT, Dermatology, Endoscopy, Histopathol- ogy, Microscopy, MRI, OCT, PET, X-ray | Pre-training | Image-text | 2023.03 | EN | Academic and research resources | Automated | N/A | Data generation and review | ResNet101 (DocFigure), ResNet34 (DETR MedICaT), PMC- CLIP | 1,646,592 |
|  | ChatDoctor [647] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2023.03 | EN | Other sources | Semi-automated | N/A | Data generation and review | N/A | 115,000 |
|  | WikiMedQA [910] [link] | Healthcare and Medical Sciences | Clinical Reports | SFT | Text QA | 2023.03 | EN | Web and Internet content | Semi-automated | N/A | N/A | SentenceBERT, BioLinkBERT | 111,895 |
|  | MIMIC-IV [672] [link] | Healthcare and Medical Sciences | EHR | Pre-training, SFT | Raw text | 2023.01 | EN | Scientific databases | Semi-automated | N/A | N/A | Transformer-DeID | 364,627 |
|  | BioRED [650] [link] | Healthcare and Medical Sciences | Academic papers | Pre-training | Classification | 2022.09 | EN | Scientific databases | Semi-automated | 6 | Data generation and review | PubTator | 500 |
|  | ViHealthQA [911] [link] | Healthcare and Medical Sciences | Biomedical QA | SFT | Text QA | 2022.06 | VI | Social media and forums | Manual | N/A | Data generation | N/A | 10,015 |
|  | MedMCQA [450] [link] | Healthcare and Medical Sciences | Medical exams | SFT | Text QA | 2022.03 | EN | Books and literary works | Automated | N/A | Data generation | N/A | 193,155 |
|  | PMC-Patients-ReCDS [912] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2022.02 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 293,000 |
|  | PMC-Patients [913] [link] | Healthcare and Medical Sciences | Clinical report | Pre-training | Raw text | 2022.02 | EN | Scientific databases | Semi-automated | N/A | Data review | PubMedBERT, BioLinkBERT | 167,000 |
|  | CMCQA [914] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2022.01 | ZH | Web and Internet content | Automated | N/A | Data review | N/A | 1,294,753 |
|  | IMCS-V2 [915] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2022.01 | ZH | Other sources | Manual | N/A | Data generation and review | N/A | 4,116 |
|  | MLEC-QA [916] [link] | Healthcare and Medical Sciences | Biomedical QA | SFT | Raw text | 2021.11 | ZH | Academic and research resources | Semi-automated | N/A | Data generation and review | N/A | 136,236 |
|  | ImageClef-VQA Med 2021 [917] [link] | Healthcare and Medical Sciences | CT, MRI, US, X-ray | SFT | VQA | 2021.09 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 4,500 |
|  | BioLeaflets [918] [link] | Healthcare and Medical Sciences | Package leaflets | Pre-training | Raw text | 2021.09 | EN | Web and Internet content | Semi-automated | N/A | Data generation | Stanza, Amazon Comprehend Medical | 1,067 |
|  | MedGPT-5k-ko [655] [link] | Healthcare and Medical Sciences | Clinical trials, EHR, Medical forum, Medi- cal textbooks | SFT | Classification, Text QA | 2021.06 | ZH | Scientific databases, Books and lit- erary works, Web and Internet con- tent, Comprehensive multi-source integration | Manual | 3 | Data generation and review | N/A | 149,141 |
|  | CBLUE [919] [link] | Healthcare and Medical Sciences | Clinical trials, EHR, Medical forum, Medi- cal textbooks | SFT | Classification, Text QA | 2021.06 | ZH | Scientific databases, Books and lit- erary works, Web and Internet con- tent, Comprehensive multi-source integration | Manual | 3 | Data generation and review | N/A | 149,141 |
|  | MedDG [920] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2021.05 | ZH | Web and Internet content | Automated | N/A | Data generation and review | N/A | 100,000 |
|  | SLAKE [772] [link] | Healthcare and Medical Sciences | CT, MRI, X-ray | SFT | VQA | 2021.02 | EN, ZH | Academic and research resources | Automated | N/A | N/A | N/A | 11,958 |
|  | Chinese-medical-dialogue-data [921] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2021.02 | ZH | Other sources | N/A | N/A | N/A | N/A | 792,099 |
|  | DeepEyeNet [658] [link] | Healthcare and Medical Sciences | CFP, FFA | Pre-training | Image-text | 2021.01 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 15,709 |
|  | AIforCOVID [922] [link] | Healthcare and Medical Sciences | X-ray | Pre-training, SFT | Image-text | 2020.12 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 820 |
|  | MedICaT [661] [link] | Healthcare and Medical Sciences | CT, Endoscopy, Histopathology, MRI, Mi- croscopy, PET, US, X-ray | Pre-training, SFT | Image-text | 2020.10 | EN | Academic and research resources | Semi-automated | 7 | Data generation | ResNet101- DocFigure, ScispaCy | 217,060 |
|  | ImageClef-VQA Med 2020 [923] [link] | Healthcare and Medical Sciences | CT, MRI, US, X-ray | SFT | VQA | 2020.09 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 4,000 |
|  | MedQA [521] [link] | Healthcare and Medical Sciences | Medical exams | SFT | Text QA | 2020.09 | EN, ZH | Scientific databases | Manual | N/A | Data generation and review | N/A | 61,097 |
|  | MedDialog-CN [701] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2020.07 | ZH | Web and Internet content | Automated | N/A | Data review | N/A | 1,100,000 |
|  | MEDIQA-AnS [798] [link] | Healthcare and Medical Sciences | Consumer health QA | SFT | Text QA | 2020.05 | EN, ZH | Web and Internet content | Semi-automated | 2 | Data generation | Custom crawlers | 156 |
|  | MedDialog [649] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2020.04 | EN, ZH | Web and Internet content | Automated | N/A | N/A | Custom crawlers | 14,668,058 |
|  | PathVQA [149] [link] | Healthcare and Medical Sciences | Histopathology | SFT | VQA | 2020.03 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 19,654 |
|  | RetinaRocks [link] | Healthcare and Medical Sciences | CFP | Pre-training, SFT | Image-text | 2019.12 | EN | Other sources | Manual | N/A | Data generation | N/A | 4,000 |
|  | MedQuAD [924] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2019.10 | EN | Web and Internet content | Automated | N/A | N/A | Custom crawlers | 47,441 |
|  | ImageClef-VQA Med 2019 [925] [link] | Healthcare and Medical Sciences | CT, MRI, US, X-ray | SFT | VQA | 2019.09 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 15,292 |
|  | PubMedQA [449] [link] | Healthcare and Medical Sciences | Academic papers | SFT | Text QA | 2019.09 | EN | Web and Internet content | Semi-automated | N/A | Data generation and review | N/A | 212,300 |
|  | PubMedQA instruction [449] [link] | Healthcare and Medical Sciences | Academic papers | SFT | Text QA | 2019.09 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 1K |
|  | MIMIC-CXR [153] [link] | Healthcare and Medical Sciences | X-ray | Pre-training | Image-text | 2019.08 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 227,835 |
|  | MIMIC-Extract [652] | Healthcare and Medical Sciences | EHR | Pre-training | Text QA | 2019.07 | EN | Scientific databases | Automated | N/A | N/A | N/A | 2,000,000 |
|  | webMedQA [926] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2019.03 | ZH | Web and Internet content | Automated | N/A | Data review | N/A | 63,284 |
|  | VQA-RAD [704] [link] | Healthcare and Medical Sciences | CT, MRI, PET, US, X-ray | SFT | VQA | 2018.11 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 1,793 |
|  | cMedQA2 [927] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2018.11 | ZH | Web and Internet content | Automated | N/A | Data review | N/A | 108,000 |
|  | ROCO [928] [link] | Healthcare and Medical Sciences | CT, MRI, PET, US, X-ray | Pre-training, SFT | Image-text | 2018.09 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 81,000 |
|  | emrQA [929] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2018.09 | EN | Integration of existing datasets | Semi-automated | N/A | N/A | N/A | 455,000 |
|  | ImageClef-VQA Med 2018 [930] [link] | Healthcare and Medical Sciences | CT, MRI, US, Unknown, X-ray | SFT | VQA | 2018.06 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 6,413 |
|  | LiveQA [931] [link] | Healthcare and Medical Sciences | Consumer health QA | SFT | Text QA | 2018.02 | EN | Scientific databases | Automated | N/A | Data review | N/A | 634 |
|  | LiveQA trec2017 [648] [link] | Healthcare and Medical Sciences | Clinical dialogue | SFT | Text QA | 2017.08 | EN | Academic and research resources | Semi-automated | N/A | Data review | N/A | 634 |
|  | OpenI [154] [link] | Healthcare and Medical Sciences | X-ray | Pre-training | Image-text | 2016.03 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 3,955 |
|  | Retina Image Bank [link] | Healthcare and Medical Sciences | CFP, FFA | Pre-training, SFT | Image-text | 2012.08 | EN | Other sources | Manual | N/A | Data generation | N/A | 30,452 |
|  | William Hoyt ImageText [link] | Healthcare and Medical Sciences | CFP | Pre-training | Image-text | 2004.03 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 856 |
|  | Pima [654] [link] | Healthcare and Medical Sciences | EHR | SFT | Classification | 1988.11 | EN | Scientific databases | Manual | N/A | N/A | N/A | 691 |
|  | COVID-19-Data-Hub [932] [link] | Healthcare and Medical Sciences | Global pandemic data (cases, vaccines, poli- cies, etc.) | Pre-training, RAG | Classification, Regression | 2020.07 | EN | Comprehensive multi-source inte- gration | Automated | N/A | N/A | R package | N/A |
|  | BEACON [695] [link] | Molecular and Cellular Biology | RNA sequence | SFT | Raw text | 2024.06 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | N/A | 870,883 |
|  | SPICE [625] [link] | Molecular and Cellular Biology | SMILES | Pre-training, RAG | Classification, Regression | 2024.03 | EN | Scientific databases | Semi-automated | N/A | Data generation and review | N/A | 113,999 |
|  | PubChemSTM [627] [link] | Molecular and Cellular Biology | SMILES | Pre-training, SFT | Raw text | 2024.01 | EN | Academic and research resources | Semi-automated | N/A | Data generation | SciBERT, spaCy | 281,000 |
|  | SourceData [933] [link] | Molecular and Cellular Biology | Academic papers | Pre-training | VQA | 2023.10 | EN | Academic and research resources | Semi-automated | N/A | Data review | PubMedBERT, BioLinkBERT, GPT-4o | 62,543 |
|  | Mol-Instructions [696] [link] | Molecular and Cellular Biology | Biomolecular instructions | SFT | Text QA | 2023.06 | EN | Comprehensive multi-source inte- gration | Automated | N/A | Data review | GPT-3.5 | 2,043,000 |
|  | PCdes [626] [link] | Molecular and Cellular Biology | SMILES | Pre-training, SFT | Raw text | 2022.12 | EN | Academic and research resources | Automated | N/A | N/A | Custom crawlers | 12,000 |
|  | MoMu [628] [link] | Molecular and Cellular Biology | Graph | Pre-training, SFT | Raw text | 2022.12 | EN | Academic and research resources | Automated | N/A | N/A | OGB | 15,613 |
|  | PEER [694] [link] | Molecular and Cellular Biology | Protein sequence | SFT | Classification, Regression | 2022.10 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | N/A | 329,922 |
|  | BioGPT [934] [link] | Molecular and Cellular Biology, Healthcare and Medical Sciences | Biomedical domain pretraining corpus | Pre-training, SFT | Raw text | 2022.08 | EN | Scientific databases, Academic and research resources | Automated | N/A | N/A | Moses tokenizer, fastBPE | 15M |
|  | DISEASES [802] [link] | Molecular and Cellular Biology, Healthcare and Medical Sciences, Multi-omics | Disease-gene associations | SFT, RAG | Classification | 2015.01 | EN | Academic and research resources, Integration of existing datasets, Sci- entific databases | Semi-automated | N/A | Data generation and review | NER tagger | 8,336,442 |
|  | BioReason [421] [link] | Molecular and Cellular Biology, Multi-omics | DNA sequence, KEGG pathways, Gene vari- ants | SFT, CoT | Text QA with CoT | 2025.05 | EN | Scientific databases, Academic and research resources | Semi-automated | N/A | N/A | Custom scripts | 87,620 |
|  | GeneChat [636] [link] | Multi-omics | Nucleotide sequence | Pre-training | Text QA | 2025.06 | EN | Scientific databases | N/A | N/A | Data generation | N/A | 47,275 |
|  | Genomics instructions [510] [link] | Multi-omics | Nucleotide sequence | SFT | Text QA | 2025.04 | EN | Academic and research resources | N/A | N/A | Data generation | N/A | 4,954,234 |
|  | scMMGPT data [639] [link] | Multi-omics | scRNA-seq | Pre-training, SFT | scRNA-seq-text | 2025.03 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 467K |
|  | OPI [697] [link] | Multi-omics | Protein | SFT | Text QA | 2025.03 | EN | Scientific databases | Semi-automated | N/A | Data generation | GPT-3.5 | 1,640,000 |
|  | OpenGenome2 [488] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2025.02 | EN | Integration of existing datasets | N/A | N/A | N/A | N/A | 8,800B (nucleotides) |
|  | Seq2Func [635] [link] | Multi-omics | Nucleotide sequence | SFT | Text QA | 2025.02 | EN | Scientific databases | Automated | N/A | Data generation | N/A | 297,000 |
|  | DNA2Image [635] [link] | Multi-omics | Nucleotide sequence | SFT | Generation | 2025.02 | EN | Scientific databases | Automated | N/A | Data generation | N/A | 43,200 |
|  | LLaMA-Gene (protein) [40] [link] | Multi-omics | Protein sequence | Pre-training, SFT | Text QA | 2024.12 | EN | Scientific databases | N/A | N/A | Data generation | N/A | 62,918 |
|  | LLaMA-Gene (DNA) [40] [link] | Multi-omics | DNA sequence | Pre-training, SFT | Text QA | 2024.12 | EN | Scientific databases | N/A | N/A | Data generation | N/A | 178,551 |
|  | OpenGenome [487] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2024.11 | EN | Integration of existing datasets | N/A | N/A | N/A | N/A | 300B (nucleotides) |
|  | The 1000G [318] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2024.10 | EN | Scientific databases | N/A | N/A | N/A | N/A | 20,500B (nucleotides) |
|  | Multispecies dataset [318] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2024.10 | EN | Scientific databases | N/A | N/A | N/A | N/A | 174B (nucleotides) |
|  | NT Benchmark [318] [link] | Multi-omics | Nucleotide sequence | SFT | Classification | 2024.10 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 493,242 |
|  | ProteinLMDataset [642] [link] | Multi-omics | Protein sequence | Pre-training | Raw text | 2024.06 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 893,000 |
|  | RNAcentral [640], [935] [link] | Multi-omics | RNA sequence | Pre-training | Raw text | 2024.05 | EN | Scientific databases | N/A | N/A | N/A | N/A | 23M |
|  | RNA-QA [640] [link] | Multi-omics | RNA sequence | SFT | Text QA | 2024.05 | EN | Academic and research resources | Automated | N/A | N/A | GPT-4o | 407,616 |
|  | ProCoT [698] [link] | Multi-omics | Biomedical QA | SFT, CoT | Text QA with CoT | 2024.05 | EN | Scientific databases, Academic and research resources | Semi-automated | N/A | Data generation and review | embedding-based fil- tering | 4,967,723 |
|  | UniProtKB/Swiss-Prot [936] | Multi-omics | Protein sequence | Pre-training | Raw text | 2023.11 | EN | Scientific databases | N/A | N/A | N/A | N/A | 570K |
|  | Multi-species genome [317] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2023.06 | EN | Integration of existing datasets | N/A | N/A | N/A | N/A | 32.49B (nucleotides) |
|  | Genomic Benchmark [937] [link] | Multi-omics | Nucleotide sequence | SFT | Classification | 2023.05 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 699,116 |
|  | CELLxGENE scRNA-seq Collection [512] [link] | Multi-omics | scRNA-seq | Pre-training | Gene Expression-pretrain | 2023.05 | EN | Scientific databases | N/A | N/A | N/A | N/A | 33 M |
|  | Human Pancreas [938] [link] | Multi-omics | scRNA-seq | SFT | Classification | 2023.01 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 10,600 |
|  | scFoundation Dataset [939] [link] | Multi-omics | scRNA-seq | Pre-training | Gene Expression-pretrain | 2022.10 | EN | Scientific databases | N/A | N/A | N/A | N/A | 50M |
|  | Human genome [631] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2021.02 | EN | Scientific databases | N/A | N/A | N/A | N/A | 2.75B (nucleotides) |
|  | GPD [940] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2021.02 | EN | Scientific databases | N/A | N/A | N/A | N/A | 142,809 |
|  | Myeloid [941] [link] | Multi-omics | scRNA-seq | SFT | Classification | 2021.02 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 9,748 |
|  | Human Cell Atlas Dataset [942] [link] | Multi-omics | scRNA-seq | SFT | Classification | 2021.02 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 84,363 |
|  | GVD [943] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2019.07 | EN | Scientific databases | N/A | N/A | N/A | N/A | 13,203B |
|  | Multiple Sclerosis [944] [link] | Multi-omics | scRNA-seq | SFT | Classification | 2019.07 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 7,844 |
|  | PanglaoDB [945] [link] | Multi-omics | scRNA-seq | Pre-training | Gene Expression-pretrain | 2018.11 | EN | Scientific databases | N/A | N/A | N/A | N/A | 1,126,580 |
|  | Zheng68k [946] [link] | Multi-omics | scRNA-seq | SFT | Classification | 2016.07 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 68,450 |
|  | GRCh38/hg38 [633] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2013.12 | EN | Scientific databases | N/A | N/A | N/A | N/A | 3.1B (nucleotides) |
|  | Biology-Instructions [700] [link] | Multi-omics | DNA, RNA, Protein sequence | SFT | Text QA | 2024.12 | EN | Academic and research resources | Semi-automated | N/A | Data generation | GPT-4o, Claude-3.5- sunnet | 3.3 M |
|  | TCPA [629] [link] | Multi-omics | Protein sequence | Pre-training | Raw text | 2013.09 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 4,379 |
|  | NCBI-GenBank [94] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2012.11 | EN | Scientific databases | N/A | N/A | N/A | N/A | 5,000B (nucleotides) |
|  | GRCh37/hg19 [633] [link] | Multi-omics | Nucleotide sequence | Pre-training | Raw text | 2009.02 | EN | Scientific databases | N/A | N/A | N/A | N/A | 3.1B (nucleotides) |
|  | Neuro-3D [710] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2025.03 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 720 |
|  | Things-MEG [708] [link] | Neuroscience | MEG | Pre-training, SFT | Classification | 2023.04 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 22,248 |
|  | Things-EEG2 [706] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2022.11 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 16,740 |
|  | SHU [718] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2022.08 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 11,988 |
|  | Things-fMRI [708] [link] | Neuroscience | fMRI | Pre-training, SFT | Classification | 2022.07 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 8,740 |
|  | NSD-Imagery [709] [link] | Neuroscience | fMRI | Pre-training, SFT | Classification | 2022.07 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 2,304 |
|  | HMC [713] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2022.03 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 154 |
|  | Things-EEG1 [705] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2022.01 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 22,248 |
|  | NSD [707] [link] | Neuroscience | fMRI | Pre-training, SFT | Classification | 2021.09 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 70,566 |
|  | ZuCo2 [712] [link] | Neuroscience | EEG | Pre-training, SFT | Text QA | 2019.11 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 739 |
|  | DIR [947] [link] | Neuroscience | fMRI | Pre-training, SFT | Classification | 2019.01 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 6,000 |
|  | Workload [721] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2018.12 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 1080 |
|  | ZuCo1 [711] [link] | Neuroscience | EEG | Pre-training, SFT | Text QA | 2018.11 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 1,107 |
|  | SEED-IV [720] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2018.02 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 143,610 |
|  | TUSL [717] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2018.01 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 245 |
|  | TUEV [716] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2015.12 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 112,237 |
|  | TUAB [716] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2015.12 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 409,083 |
|  | SEED [719] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2015.05 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 144,851 |
|  | Sleep-EDF [714] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 2013.10 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 197 |
|  | SHHS [715] [link] | Neuroscience | EEG | Pre-training, SFT | Classification | 1998.01 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 6,441 |
|  | repoDB [803] [link] | Pharmacy, Healthcare and Medical Sciences | Drug-disease relationships, Clinical trials | RAG | Classification, Text QA | 2017.03 | EN | Scientific databases | Automated | N/A | N/A | scripts | 15,648 |
| Chemistry | MOSES [606] [link] | Biochemistry | SMILES | Pre-training | Raw text | 2020.07 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 1,936,962 |
|  | ChemBL [216] [link] | Biochemistry | SMILES | Pre-training | Raw text | 2012.01 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 1,961,462 |
|  | ChemRxivQuest [948] [link] | General Chemistry | Academic papers | Pre-training, SFT | Text QA | 2025.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 970 |
|  | ScholarChemQA [105] [link] | General Chemistry | Academic papers | Pre-training, SFT | Text QA | 2025.02 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 40K |
|  | SMolInstruct [689] [link] | General Chemistry | SMILES | SFT | Text QA | 2024.08 | EN | Scientific databases | Semi-automated | N/A | Data generation and review | GPT-4 | 3.3M |
|  | ChemNLP [949] [link] | General Chemistry | Text | Pre-training, SFT | Classification | 2023.01 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 110,342 |
|  | PMO [214] [link] | General Chemistry | SMILES | Pre-training, SFT | Raw text | 2022.05 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 10K |
|  | ZINC [215] [link] | General Chemistry | SMILES | Pre-training | Raw text | 2012.10 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 250K |
|  | DeepProtein [950] [link] | Pharmacy | Protein sequence, SMILES | Pre-training, SFT | Raw text | 2025.05 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 78K |
|  | TrialBench [753] [link] | Pharmacy | SMILES, Disease code | Pre-training, SFT | Raw text | 2024.09 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 470K |
|  | TDC2 [951] [link] | Pharmacy | SMILES, Protein sequence, Genome se- quence | Pre-training, SFT | Classification, Regression, Genera- tion | 2024.09 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 3.4B (tokens) |
|  | SBDDBench [952] [link] | Pharmacy | Text, Protein sequence, SMILES | Pre-training, SFT | Protein-ligand | 2022.06 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 5K |
|  | TOP [953] [link] | Pharmacy | SMILES | Pre-training, SFT | Raw text | 2022.02 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 12K |
|  | TDC [243] [link] | Pharmacy | SMILES, Protein sequence, Genome se- quence | Pre-training, SFT | Classification, Regression, Genera- tion | 2021.06 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 0.2B (tokens) |
|  | DeepPurpose [610] [link] | Pharmacy | Protein sequence, SMILES | Pre-training, SFT | Raw text | 2020.12 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 5,074 |
|  | DrugBank [954] [link] | Pharmacy | SMILES | Pre-training, SFT | Raw text | 2018.01 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 18K |
|  | DrugCentral [955] [link] | Pharmacy | SMILES | Pre-training, SFT | Raw text | 2017.01 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 4,995 |
|  | USPTO [612] | Synthetic Chemistry | SMILES | Pre-training, SFT | Generation | 2015.07 | EN | Patent databases | Manual | N/A | Data generation and review | N/A | 1,939,253 |
| Physics | MM-PhyQA [735] [link] | General Physics | High-school exams | SFT, CoT | VQA with CoT | 2024.04 | EN | Web and Internet content | Manual | N/A | Data generation and review | AFL 3.0 | 3,825 |
|  | PIQA [680] [link] | General Physics | Text | SFT | Text QA | 2020.01 | EN | Other sources | Semi-automated | AFLite | Data generation and review | N/A | 19,838 |
| Astronomy | AstroLLaVA [562] [Link] | Astronomy | General dialog, Astronomical images | SFT | VQA | 2025.04 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4 | 29,783 |
|  | AstroPT [669] [Link] | Astronomy | Astronomical images | Pre-training | Regression | 2024.05 | EN | Web and Internet content, Scientific databases | Automated | N/A | Data review | DESI Legacy Survey API | 8.6M (tokens) |
|  | Astro-NER [725] Link | Astronomy | Academic papers | SFT | Text QA | 2024.05 | EN | Academic and research resources | Semi-automated | 4 | Data generation and review | GPT-3.5 | 5000 |
|  | AstroLLaMA-chat [723] [Link] | Astronomy | Academic papers | SFT | Text QA | 2024.01 | EN | Academic and research resources | Manual | N/A | Data review | N/A | 10,356 |
|  | AstroLLaMA [561] [Link] | Astronomy | Academic papers | SFT | Text QA | 2023.09 | EN | Academic and research resources, Web and Internet content | Manual | N/A | Data review | N/A | 9.5M |
|  | ATel [956] Link | Astronomy | Academic papers | SFT | Text QA | 2023.05 | EN | Academic and research resources | Manual | N/A | Data review | N/A | 234 |
|  | AstroBERT [667][Link] | Astronomy | Academic papers | Pre-training | Raw text | 2022.11 | EN | Academic and research resources | Automated | 12 | Data generation and review | N/A | 3.8B (tokens) |
|  | AstroMLab 4 [566] [Link] | Astronomy | Academic papers | SFT | Text QA | 2025.05 | EN | Integration of existing datasets | Automated | N/A | Data generation and review | Gemini-1.5-Pro | 250,000 preprints |
|  | AstroMLab 3 [563] [Link] | Astronomy | Academic papers | SFT | Text QA | 2025.04 | EN | Academic and research resources | Automated | N/A | Data generation and review | Gemini-1.5-Pro | 3.3B (tokens) |
|  | AstroMLab 2 [724] [Link] | Astronomy | Academic papers | SFT | Text QA | 2024.09 | EN | Academic and research resources | Automated | N/A | Data generation and review | Gemini-1.5-Pro | 10,356 |
|  | Starwhisper-pilsar [780] Link | Astrophysics | Text, pulsar diagnostic plots, pulsars | signals SFT | Classification | 2024.04 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | DeepSeek-VL-7B, InternVL2-40B | 106,674 |
|  | PAPERCLIP [781] [Link] | Astrophysics | synthetic conversation text, Astronomical images | SFT | Image-text | 2024.03 | EN | Academic and research resources | Automated | N/A | Data review | Mixtral-8x7B- Instruct | 31,859 |
| Materials Science | ChEBI-20-MM [692] [link] | Materials Science | InChI, IUPAC, SELFIES, Molecular | image SFT | Text QA | 2025.01 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 29,706 |
|  | Materials Project Trajectory [620] [link] | Materials Science | CIF | Pre-training | Raw text | 2023.07 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 1,580,395 |
|  | DigiMOF [618] [link] | Materials Science | CIF | Pre-training | Raw text | 2023.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 15,501 |
|  | Novel Materials Discovery (NOMAD) [619] [link] | Materials Science | CIF | Pre-training | Raw text | 2023.03 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 4,341,443 |
|  | MOFX-DB (hMOF) [957] [link] | Materials Science | CIF | Pre-training | Raw text | 2023.02 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 160,000 |
|  | MatScholar [624] [link] | Materials Science | Academic papers | Pre-training | Raw text | 2022.07 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 5M |
|  | Pfeiffer et al. Chemical composition [623] [link] | Materials Science | Chemical Composition | Pre-training | Raw text | 2022.03 | EN | Comprehensive multi-source inte- gration | Manual | N/A | Data generation and review | N/A | 14,884 |
|  | Pfeiffer et al. Mechanical Properties [623] [link] | Materials Science | Numerical property | Pre-training | Raw text | 2022.03 | EN | Comprehensive multi-source inte- gration | Manual | N/A | Data generation and review | N/A | 1,278 |
|  | ChEBI-20 [691] [link] | Materials Science | Scientific instruction | SFT | Text QA | 2021.11 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 29709 |
|  | ZINC [622] [link] | Materials Science | SMILES | Pre-training | Raw text | 2020.12 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 230M |
|  | JARVIS-DFT [621] [link] | Materials Science | InChI, IUPAC, SELFIES | Pre-training | Raw text | 2020.11 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 41,000 |
|  | MOSES [690] [link] | Materials Science | SMILES | SFT | Text QA | 2020.11 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 1.6M |
|  | QMOF [617] [link] | Materials Science | CIF | Pre-training | Raw text | 2020.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 20,000 |
|  | Warwick Electron Microscopy Datasets [693] [link] | Materials Science | STEM image, TEM image, TEM exit wave- function | SFT | VQA | 2020.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 135395 |
|  | CoRE MOF 2019 [616] [link] | Materials Science | CIF | Pre-training | Raw text | 2019.12 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 14,000 |
|  | Inorganic Crystal Structure Database (ICSD) [615] [link] | Materials Science | CIF | Pre-training | Raw text | 2019.10 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 318,901 |
|  | US Patent Office (USPTO) [217] [link] | Materials Science | SMILES | Pre-training | Raw text | 2017.06 | EN | Patent databases | Manual | N/A | Data generation and review | N/A | 2,830,616 |
|  | Open Quantum Materials Database (OQMD) [614] [link] | Materials Science | CIF | Pre-training | Raw text | 2014.11 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 1,317,811 |
|  | Materials Project [70] [link] | Materials Science | CIF | Pre-training | Raw text | 2013.07 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 577,813 |
| Earth Science | WeatherQA [728] [link] | Atmosphere | Remote sensing, Science QA | SFT | VQA | 2024.06 | EN | Scientific databases | Semi-automated | 4 | Data review | GPT-4 | 8,511 |
|  | SeafloorAI [729] [link] | Hydrosphere | Sonar images, Text | SFT | VQA | 2024.11 | EN | Scientific databases | Semi-automated | 4 | Data review | GPT-4 | 7M |
|  | TEOChatlas [578] [link] | Lithosphere | Remote sensing | SFT | VQA | 2025.01 | EN | Scientific databases | Automated | N/A | Data generation | N/A | 554K |
|  | EarthVQA [727] [link] | Lithosphere | Remote sensing, Science QA | SFT | VQA | 2023.12 | EN | Scientific databases | Automated | N/A | Data generation | ArcGIS toolbox | 208K |
|  | Geochat [588] [link] | Lithosphere | Remote sensing, Science QA | SFT | VQA | 2023.11 | EN | Scientific databases | Automated | N/A | Data generation | Vicuna-v1.5 | 306K |
|  | FloodNet [726] [link] | Lithosphere | Remote sensing, Science QA | SFT | VQA | 2021.05 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 11K |
|  | GeoSignal [567] [link] | Lithosphere, Hydrosphere, Atmo- sphere | Remote sensing, Science QA | SFT | Text QA | 2023.06 | EN | Encyclopedias and knowledge bases, Academic and research resources, Scientific databases, Comprehensive multi-source integration | Semi-automated | 10 | Data review | GPT-4 | 39,749 |
|  | GeoLLaVA-8k [573] [link] | Remote Sensing | Remote sensing | SFT | Image-text, VQA | 2025.05 | EN | Academic and research resources | Semi-automated | 35 | Data generation and review | GPT-4o | 81,367 |
|  | EVAttrs-95k [570] [link] | Remote Sensing | Remote sensing, Object property | SFT | Image-text, VQA | 2025.03 | EN | Academic and research resources | Semi-automated | N/A | Data generation and review | Qwen2-VL-72B, GPT-4o | 95.1K |
|  | VersaD [958] [link] | Remote Sensing | Remote sensing | Pre-training | Image-text | 2024.11 | EN | Academic and research resources | Automated | N/A | N/A | Gemini-Vision | 1.4M |
|  | RSVP [571] [link] | Remote Sensing | Remote sensing | SFT | Image-text, VQA | 2024.10 | EN | Integration of existing datasets, Academic and research resources | Automated | N/A | N/A | GPT-4V, DINOv2- ViT L/14, CLIP- ConvNeXt | 3.65M |
|  | FIT-RS [959] [link] | Remote Sensing | Remote sensing, Relation graph, etc. | SFT | Image-text, VQA | 2024.07 | EN | Integration of existing datasets, Academic and research resources | Semi-automated | N/A | Data generation | TinyLLaVA-3.1B, GPT-4, GPT-3.5, CLIP-ViT-L14 | 1,415K |
|  | VRSBench [797] [link] | Remote Sensing | Remote sensing | SFT | Image-text, VQA | 2024.06 | EN | Academic and research resources | Semi-automated | N/A | Data review | GPT-4V | 142,390 |
|  | MMRS-1M [960] [link] | Remote Sensing | Remote sensing, Optical, SAR, Infrared, | etc. SFT | Image-text, VQA | 2024.03 | EN | Integration of existing datasets | Automated | N/A | N/A | N/A | 1.06M |
|  | ChatEarthNet [961] [link] | Remote Sensing | Remote sensing, Optical, Multi-band | SFT | Image-text | 2024.02 | EN | Scientific databases | Semi-automated | N/A | Data review | GPT-3.5, GPT-4V | 173,488 |
|  | LHRS-Align [962] [link] | Remote Sensing | Remote sensing | Pre-training | Image-text | 2024.02 | EN | Scientific databases | Automated | N/A | N/A | Vicuna-v1.5-13B | 1.15M |
|  | LHRS-Instruct [962] [link] | Remote Sensing | Remote sensing | SFT | Image-text, VQA | 2024.02 | EN | Integration of existing datasets, Academic and research resources | Semi-automated | N/A | Data review | Vicuna-v1.5-13B, GPT-4 | 12K |
|  | RS5M [730] [link] | Remote Sensing | Remote sensing | Pre-training | Image-text | 2024.01 | EN | Scientific databases | Automated | N/A | N/A | CLIP | 5.07M |
|  | SkyEye-968k [963] [link] | Remote Sensing | Remote sensing | SFT | Image-text, Video-text, VQA | 2024.01 | EN | Integration of existing datasets | Semi-automated | N/A | Data review | N/A | 968K |
|  | SkyScript [731] [link] | Remote Sensing | Remote sensing | Pre-training | Image-text | 2023.12 | EN | Academic and research resources, Scientific databases | Automated | N/A | N/A | CLIP, Logistic Re- gression model | 2.6M |
|  | RSICap [784] [link] | Remote Sensing | Remote sensing | SFT | Image-text | 2023.07 | EN | Academic and research resources | Manual | 5 | Data generation, Data review | N/A | 2.5K |
| General Science | NaturalReasoning [685] [link] | Multidisciplinary (incl. Physics) | Text | SFT | Text QA with CoT | 2025.02 | EN | Web and Internet content, Books and literary works, Academic and research resources | Semi-automated | N/A | Data review | LLaMA-70B | 2.8M |
|  | Nemotron-Science [684] [link] | Multidisciplinary (incl. Physics) | Text with formulae and code | SFT, RLHF | Text QA with CoT | 2025.05 | EN | Social media and forums, Academic and research resources, Books and literary works | Semi-automated | N/A | Data review | DeepSeek-R1 | 2.7M |
|  | Galactica [30] [link] | Multidisciplinary (incl. Chemistry) | Text (incl. formulas, code) | Pre-training | Raw text | 2022.11 | EN | Webpages | Fully-automated | N/A | Data generation and review | Custom crawlers, PDF parsers | 106B tokens |
|  | SciBERT [24] [link] | Multidisciplinary (incl. Physics) | Academic papers | Pre-training | Raw text | 2019.09 | EN | Academic and research resources | Automated | N/A | Data generation | Crawlers, text pro- cessing tools | 3.3B (tokens) |
|  | ArXivCap [604] [link] | Physics, Biology, etc. | Paper figures | Pre-training | Image-text | 2024.05 | EN | Academic and research resources | Semi-automated | 7 | Data review | PDF parsers | 6.4M |
|  | SCP-116K [686] [link] | Physics, Chemistry, Biology, etc. | Text with formulae | SFT | Text QA with CoT | 2025.01 | EN | Academic and research resources, Books and literary works | Semi-automated | N/A | Data review | PDF parsers, OCR, LaTeX rendering | 116.8K |
|  | MegaScience [964] [link] | Medicine, Physics, Chemistry, Bi- ology | Science textbooks | SFT | Text QA with CoT | 2024.08 | EN | Web and Internet content, Books and literary works, Integration of existing datasets | Semi-automated | N/A | Data review | Llama3.3-70B- Instruct, DeepSeek- V3, BGE-large-en- v1.5 | 651,840 |

# TABLE V: Summary of evaluation datasets for scientific LLMs/MLLMs. [link] directs to dataset websites.

| Scientific Domain | Dataset | Subdomain | Modality | Level | Type | Release | Language | Source | Annotation Pipeline | Human Annotators | Human Tasks | Auto-annotation Tools | Size | Evaluation Type | Metrics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | SeedBench [777] [link] | Agriculture | Breeding literature | Expert | Text QA | 2025.05 | EN, ZH | Academic and research resources | Semi-automated | N/A | Data generation and review | GPT-4 | 2,264 | MCQ, Open- ended | Acc, F1, ROUGE |
|  | AgEval [189] [link] | Agriculture | Plant stress phenotyping photos and annotations | Expert | VQA | 2025.01 | EN | Scientific databases | N/A | N/A | N/A | N/A | 1,200 | Classification, Regression | F1, NMAE |
|  | AgXQA [104] [link] | Agriculture | Agricultural extension records | Expert | Text QA | 2024.10 | EN | Academic and research resources | Semi-automated | N/A | N/A | N/A | 2,186 | Open-ended | EM, F1 |
|  | Fundus-MMBench [965] [link] | Healthcare and Medical Sciences | CFP | Expert | VQA | 2025.07 | EN | Integration of existing datasets | Manual | N/A | Data review | N/A | 620 | MCQ | Acc |
| Life Science | ReXVQA [869] [link] | Healthcare and Medical Sciences | X-ray | N/A | VQA | 2025.06 | EN | Integration of existing datasets | Semi-automated | 3 | Data review | GPT-4o, ClinicalBERT, MedEmbed | 40,557 | MCQ | Acc |
|  | HealthBench [771] [link] | Healthcare and Medical Sciences | Clinical dialogue, Medical task re- quests, Medical record summariza- tion, etc. | Expert | Text QA | 2025.05 | EN | Comprehensive multi-source inte- gration | Semi-automated | 262 | Data generation and review | GPT-o1, GPT-4.1 | 5,000 | Open-ended | Customized rubric crite- rion |
|  | MedAlpaca [520] [link] | Healthcare and Medical Sciences | Biomedical knowledge base | Expert | Text QA | 2025.03 | EN | Web and Internet content | Semi-automated | N/A | Data review | GPT-3.5-Turbo | 374 | MCQ | Acc |
|  | GEMeX-VQA [873] [link] | Healthcare and Medical Sciences | X-ray | N/A | VQA | 2025.03 | EN | Integration of existing datasets | Semi-automated | N/A | Data review | OpenBioLLM-70B, GPT-4o | 3,960 | MCQ, True/False, Open-ended | Acc |
|  | MIMIC-Diff-VQA [795] [link] | Healthcare and Medical Sciences | X-ray | Expert | VQA (multi-image) | 2025.02 | EN | Scientific databases | Semi-automated | 3 | Data generation and review | ScispaCy | 70,070 | MCQ, Open- ended | BLEU, METEOR, ROUGE-L, CIDEr |
|  | MedAgentBench [775] [link] | Healthcare and Medical Sciences | EHR, Lab results, Diagnosis codes, Medication orders | Expert | Text QA | 2025.01 | EN | Academic and research resources | Manual | 2 | Data generation and review | N/A | 300 | Open-ended | Success rate |
|  | MedXpertQA [770] [link] | Healthcare and Medical Sciences | CT, ECG, Histopathology, MRI, US, X-ray, etc. | Expert | VQA, Text QA | 2025.01 | EN | Academic and research resources | Semi-automated | N/A | Data generation and review | GPT-4o, Claude | 4,460 | MCQ | Acc |
|  | OpenMM-Medical [966] [link] | Healthcare and Medical Sciences | CT, Dermatology, Endoscopy, CFP, MRI, Microscopy, X-ray, etc. | N/A | VQA | 2025.01 | EN, ZH | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4o | 88,996 | MCQ | Acc |
|  | Asclepius [967] [link] | Healthcare and Medical Sciences | CT, Dermatology, CFP, Histopathology, MRI, Microscopy, OCT, X-ray, etc. | N/A | VQA, Image-text | 2024.11 | EN | Comprehensive multi-source inte- gration | Semi-automated | 34 | Data generation and review | ChatGPT, GPT-4V, GPT-4o | 3,232 | MCQ | Acc |
|  | ClinicalBench [968] [link] | Healthcare and Medical Sciences | EHR | N/A | Text QA | 2024.11 | EN | Integration of existing datasets | N/A | N/A | N/A | N/A | N/A | MCQ | F1, AUROC |
|  | WorldMedQA-V [969] [link] | Healthcare and Medical Sciences | Dermatology, Microscopy, X-ray, etc. | N/A | VQA | 2024.10 | EN, JA, ES, HE, PT | Academic and research resources | Semi-automated | N/A | Data review | GPT-4o, Gemini Flash1-5, Yi-VL- 34B | 568 | MCQ | Acc |
|  | CRAFT-BioQA [970] [link] | Healthcare and Medical Sciences | Biomedical QA | N/A | Text QA | 2024.09 | EN | Academic and research resources | Automated | N/A | N/A | N/A | N/A | MCQ | Acc |
|  | MedTrinity-25M [880] [link] | Healthcare and Medical Sciences | CT, MRI, X-ray, Histopathology, etc. | Expert | Image-text, VQA | 2024.08 | EN | Integration of existing datasets, Sci- entific databases | Automated | N/A | N/A | N/A | 100,000 | Open-ended | Acc |
|  | GMAI-MMBench [971] [link] | Healthcare and Medical Sciences | CT, Dermatology, Endoscopy, CFP, Histopathology, MRI, Microscopy, OCT, PET, US, X-ray, etc. | N/A | VQA | 2024.08 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4o | 26k | MCQ | Acc |
|  | SlideBench [151] [link] | Healthcare and Medical Sciences | Histopathology | N/A | VQA | 2024.11 | EN | Scientific databases | Semi-automated | N/A | Data generation and review | GPT-4o | 16k | MCQ, Open- ended | Acc, BLEU |
|  | Bio-ML [972] [link] | Healthcare and Medical Sciences | Ontology data | Expert | Text QA | 2024.07 | EN | Encyclopedias and knowledge bases | Semi-automated | N/A | Data generation and review | N/A | 25,270 | Retrieval | F1 |
|  | MedBench [769] [link] | Healthcare and Medical Sciences | Dianosis report, Clinical dialogue, EHR | Expert | Text QA | 2024.06 | ZH | Integration of existing datasets | Manual | N/A | Data generation | N/A | 300,901 | MCQ, Open- ended | BLEU, ROUGE-L, F1, Acc |
|  | ClinicalLab [801] [link] | Healthcare and Medical Sciences | Clinical notes | Expert | Text QA | 2024.06 | EN, ZH | Other sources | Manual | N/A | Data generation and review | GPT-4 | 1,500 | Open-ended | DWR, DIFR, CDR, Ac- ceptability, Acc, BLEU, ROUGE, BERTScore |
|  | AgentClinic-NEJM [776] [link] | Healthcare and Medical Sciences | Clinical dialog, Diagnosis report, CT, Dermatology, Histopathology, etc. | Expert | VQA | 2024.05 | EN | Academic and research resources, Comprehensive multi-source inte- gration | Automated | N/A | N/A | N/A | 120 | Open-ended | Acc, Patient compliance, Consultation ratings |
|  | AgentClinic-Lang [776] [link] | Healthcare and Medical Sciences | Medical exams | Expert | Text QA | 2024.05 | EN, ES, FA, FR, HI, KO, ZH | Academic and research resources, Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4 | 749 | Open-ended | Acc, Patient compliance, Consultation ratings |
|  | AgentClinic-MedQA [776] [link] | Healthcare and Medical Sciences | Medical exams | Expert | Text QA | 2024.05 | EN | Academic and research resources, Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4 | 215 | Open-ended | Acc, Patient compliance, Consultation ratings |
|  | AgentClinic-MIMIC-IV [776] [link] | Healthcare and Medical Sciences | EHR | Expert | Text QA | 2024.05 | EN | Scientific databases | Semi-automated | N/A | Data review | GPT-4 | 200 | Open-ended | Acc, Patient compliance, Consultation ratings |
|  | AgentClinic-Spec [776] [link] | Healthcare and Medical Sciences | Medical exams | Expert | Text QA | 2024.05 | EN | Integration of existing datasets | Semi-automated | N/A | N/A | GPT-4 | 260 | Open-ended | Acc, Patient compliance, Consultation ratings |
|  | M3D-Bench [659] [link] | Healthcare and Medical Sciences | CT, Clinical reports | Expert | Image-text, Text QA, VQA | 2024.04 | EN | Scientific databases, Integration of existing datasets | Semi-automated | N/A | Data generation and review | GPT-4V | 1,235 | MCQ, Open- ended, Retrieval | Acc, BLEU, ROUGE |
|  | AMOS-MM [155] [link] | Healthcare and Medical Sciences | CT | Expert | Image-text, VQA | 2024.04 | EN, ZH | Integration of existing datasets, Sci- entific databases | N/A | N/A | N/A | N/A | 2300 | Open-ended, MCQ | Acc |
|  | CMtMedQA [529] [link] | Healthcare and Medical Sciences | Clinical dialogue | Expert | Text QA | 2024.03 | ZH | Books and literary works | Semi-automated | 6 | Data review | GPT-3.5, CMeKG, RLHF-Label-Tool | 70k | Open-ended | GPT-4 score |
|  | Medbullets [973] [link] | Healthcare and Medical Sciences | Medical exams | N/A | Text QA | 2024.02 | EN | Social media and forums | Automated | N/A | Data review | N/A | 618 | MCQ | ROUGE-L, BERTScore, CTC, G-Eval, BARTScore+ |
|  | RareBench [774] [link] | Healthcare and Medical Sciences | EHR, Medical history, Lab tests | Expert | Text QA | 2024.02 | EN, ZH | Scientific databases, Academic and research resources, Other sources | Manual | N/A | Data generation and review | N/A | 2,185 | Open-ended | Precision, Recall, F1, Me- dian Rank, etc. |
|  | OmniMedVQA [796] [link] | Healthcare and Medical Sciences | CT, Dermatology, Endoscopy, CFP, Histopathology, MRI, Microscopy, OCT, PET, US, X-ray, etc. | N/A | VQA | 2024.02 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4 | 127,995 | MCQ | Acc |
|  | MultiMedEval [974] [link] | Healthcare and Medical Sciences | CT, Dermatology, CFP, Histopathology, MRI, Microscopy, OCT, US, X-ray, etc. | N/A | VQA | 2024.02 | EN | Integration of existing datasets | Semi-automated | N/A | Data review | CheXbert, GPT, Rad- Graph | 60k | MCQ | Acc |
|  | Fhirfly Medical Questions [link] | Healthcare and Medical Sciences | Biomedical QA | N/A | Text QA | 2024.01 | EN | Academic and research resources | Semi-automated | N/A | Data review | N/A | 25,102 | True/False | Acc |
|  | RP3D-DiagDS [773] [link] | Healthcare and Medical Sciences | CT, MRI, X-ray, US, Fluoroscopy, etc. | Expert | Classification | 2023.12 | EN | Scientific databases | Semi-automated | N/A | Data generation and review | Custom crawlers, GPT-4 | 40,936 | True/False | AUROC, AP |
|  | NEJM-AI Benchmarking [975] [link] | Healthcare and Medical Sciences | Medical exams | Expert | Text QA | 2023.11 | EN | Academic and research resources | Automated | N/A | N/A | NLTK, Regex | 858 | MCQ | Acc, BLEU, WER, Cosine |
|  | MORFITT [895] [link] | Healthcare and Medical Sciences | Clinical papers | Expert | Classification | 2023.11 | FR | Academic and research resources | Manual | N/A | Data review | N/A | 1,560 | Classification | Precision, Rappel, F1 |
|  | SourceData [933] [link] | Healthcare and Medical Sciences | Gene/protein entities | Expert | Raw text | 2023.10 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 620,000 | NER | Precision, Recall, F1 |
|  | SDOH-NLI [898] [link] | Healthcare and Medical Sciences | Clinical notes | Expert | Classification | 2023.10 | EN | Integration of existing datasets | Manual | N/A | Data generation | N/A | 4.21k | Classification | Precision, Recall, F1 |
|  | HealthsearchQA [15] [link] | Healthcare and Medical Sciences | Consumer health QA | Expert | Text QA | 2023.08 | EN | Web and Internet content | Semi-automated | N/A | Data review | N/A | 3,173 | Open-ended | Factuality, Comprehen- sion, Reasoning, Possible harm and bias |
|  | CMB-Exam [815] [link] | Healthcare and Medical Sciences | Medical exams | Expert | Text QA | 2023.08 | ZH | Web and Internet content | Semi-automated | N/A | Data review | N/A | 280,839 | MCQ | Acc |
|  | CMB-Clin [815] [link] | Healthcare and Medical Sciences | Medical exams | Expert | Text QA | 2023.08 | ZH | Books and literary works | Semi-automated | N/A | Data review | N/A | 208 | Open-ended | Fluency, Relevance, Com- pleteness, Proficiency |
|  | MultiMedBench [976] [link] | Healthcare and Medical Sciences | CT, Dermatology, Histopathology, Microscopy, MRI, X-ray, etc. | N/A | Text QA, VQA | 2023.07 | Mixed | Integration of existing datasets | N/A | N/A | N/A | N/A | 1M | N/A | Acc, ROUGE-L, BLEU, F1-RadGraph, F1 |
|  | GPT-4 BiasBenchmark [977] [link] | Healthcare and Medical Sciences | Clinical trials | Expert | Text QA | 2023.07 | EN | Academic and research resources | Semi-automated | N/A | Data generation and review | GPT-4 | 213 | Open-ended | Acc |
|  | Lavita Medical QA [978] [link] | Healthcare and Medical Sciences | Clinical guidelines | N/A | Text QA | 2023.07 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 11,500 | MCQ | Acc |
|  | BioASQ10b-factoid [768] [link] | Healthcare and Medical Sciences | Clinical dialogue, PubMed snippets | Expert | Text QA | 2023.07 | EN | Scientific databases, Academic and research resources | Manual | N/A | Data generation and review | N/A | 166 | Open-ended | Acc, MRR |
|  | MedNERF [979] [link] | Healthcare and Medical Sciences | Drug Prescription | Expert | Classification | 2023.06 | FR | Other sources | Manual | N/A | Data generation and review | N/A | 100 | NER | F1 |
|  | WikiMedQA [910] [link] | Healthcare and Medical Sciences | Clinical reports | Expert | Text QA | 2023.03 | EN | Web and Internet content | Semi-automated | N/A | N/A | SentenceBERT, BioLinkBERT | 5,893 | MCQ | Acc |
|  | BioASQ [768] [link] | Healthcare and Medical Sciences | Biomedical Documents | Expert | Text QA | 2022.12 | EN | Academic and research resources | Manual | 21 | Data generation and review | N/A | 4,721 | Open-ended | Acc |
|  | BioRED [650] [link] | Healthcare and Medical Sciences | Biomedical papers | N/A | Classification | 2022.09 | EN | Scientific databases | Semi-automated | 6 | Data generation and review | PubTator | 100 | NER | Precision, Recall, F1 |
|  | BioLeaflets [918] [link] | Healthcare and Medical Sciences | Package leaflets | Expert | Raw text | 2021.09 | EN | Web and Internet content | Semi-automated | N/A | Data generation | Stanza, Amazon Comprehend Medical | 134 | Generation | SacreBLEU, ROUGE-L, BERTScore, BLEURT, MoverScore-21 |
|  | CBLUE [919] [link] | Healthcare and Medical Sciences | Clinical trials, EHR, Medical fo- rum, Medical textbooks | N/A | Classification, Text QA | 2021.06 | ZH | Comprehensive multi-source inte- gration | Manual | 3 | Data generation and review | N/A | 46,729 | NER, Open- ended, Retrieval | Acc, F1 |
|  | SLAKE [772] [link] | Healthcare and Medical Sciences | CT, MRI, X-ray | N/A | VQA | 2021.02 | EN, ZH | Academic and research resources | Automated | N/A | N/A | N/A | 2,070 | MCQ, Open- ended | Acc |
|  | MEDIQA-AnS [798] [link] | Healthcare and Medical Sciences | Consumer health QA | Undergraduate | Text QA | 2020.09 | EN | Web and Internet content | Manual | 2 | Data generation | N/A | 708 | Open-ended | ROUGE, BLEU |
|  | RadVisDial (G) [980] [link] | Healthcare and Medical Sciences | X-ray | N/A | VQA | 2020.07 | EN | Integration of existing datasets | Semi-automated | 2 | Data generation | NegBio, CheXpert | 91k | MCQ | Acc |
|  | CORD-19 [589] [link] | Healthcare and Medical Sciences | Academic papers | N/A | Text QA | 2020.03 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 280K | Retrieval, QA | MRR, Acc |
|  | PathVQA [149] [link] | Healthcare and Medical Sciences | Histopathology | Expert | VQA | 2020.03 | EN | Academic and research resources | Automated | N/A | N/A | CoreNLP | 6,012 | MCQ, Open- ended | BLEU, Exact-match, F1 |
|  | MedQuAD [924] [link] | Healthcare and Medical Sciences | Patient educational materials | Undergraduate | Text QA | 2019.11 | EN | Web and Internet content | Semi-automated | 2 | Data generation | MetaMap Lite, UMLS lookup | 47,457 | Open-ended | Acc, F1, MRR |
|  | Pubmed Causal [981] [link] | Healthcare and Medical Sciences | Biomedical papers | N/A | Classification | 2019.11 | EN | Scientific databases | Manual | N/A | Data generation | N/A | 2,446 | Classification | Acc, F1 |
|  | PubMedQA instruction [449] [link] | Healthcare and Medical Sciences | Clinical dialogue | Expert | Text QA | 2019.09 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 273k | Classification | Acc |
|  | VQA-RAD [704] [link] | Healthcare and Medical Sciences | CT, MRI, PET, US, X-ray | N/A | VQA | 2018.11 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 451 | MCQ, Open- ended | Acc, BLEU |
|  | Pima [654] [link] | Healthcare and Medical Sciences | EHR | Expert | Classification | 1988.11 | EN | Scientific databases | Manual | N/A | N/A | N/A | 77 | Classification | AUROC |
|  | TOMG-Bench [762] [link] | Molecular and Cellular Biology | Molecule | Expert | Text QA | 2024.12 | EN | Scientific databases | Automated | N/A | N/A | N/A | 45,000 | Open-ended | Success Rate, Similarity, Novelty, Validity |
|  | MoleculeQA [763] [link] | Molecular and Cellular Biology | Molecule | Expert | Text QA | 2024.11 | EN | Scientific databases | Manual | 2 | Data generation and review | N/A | 62,000 | MCQ | Acc |
|  | BEACON [695] [link] | Molecular and Cellular Biology | RNA sequence | N/A | Raw text | 2024.06 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | N/A | 96,283 | Classification, Regression | F1, AUROC, Precision, R2, MSE, PCC |
|  | GeneHop [982] [link] | Molecular and Cellular Biology | Multi-hop genomic QA | N/A | Text QA | 2023.04 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 150 | Open-ended | Acc |
|  | PCdes [626] [link] | Molecular and Cellular Biology | SMILES | N/A | Text QA | 2022.12 | EN | Academic and research resources | Automated | N/A | N/A | Custom crawlers | 3,000 | Retrieval | Acc, Recall |
|  | PEER [694] [link] | Molecular and Cellular Biology | Protein sequence | Expert | Classification, Regression | 2022.10 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | N/A | 115,281 | Classification, Regression | Acc, RMSE, Precision, PCC |
|  | BioPreDyn-bench [983] [link] | Molecular and Cellular Biology | Time-series (simulation data) | Expert | Regression | 2015.02 | EN | Academic and research resources | N/A | N/A | N/A | 6 | 6 | Open-ended | NRMSE |
|  | MicroVQA [146] [link] | Molecular and Cellular Biology, Healthcare and Medical Sciences | Microscopy | Expert | VQA | 2025.03 | EN | Academic and research resources | Semi-automated | 12 | Data generation and review | GPT-4o | 1042 | MCQ | Acc |
|  | DISEASES [802] [link] | Molecular and Cellular Biology, Healthcare and Medical Sciences, Multi-omics | Disease-gene associations | Expert | Classification | 2015.01 | EN | Academic and research resources, Integration of existing datasets, Sci- entific databases | Semi-automated | N/A | Data generation and review | NER tagger | 8,336,442 | Open-ended, True/False, Retrieval | Precision, Recall, F1, AU- ROC, AUPRC |
|  | LAB-Bench [764] [link] | Molecular and Cellular Biology, Multi- omics, Neuroscience | Research problems | N/A | Text QA | 2024.07 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 2,457 | MCQ | Acc |
|  | BioProBench [984] [link] | Molecular and Cellular Biology, Multi- omics, Pharmacy, Neuroscience, etc. | Protocol | N/A | Text QA | 2025.05 | EN | Academic and research resources | Semi-automated | N/A | Data review | N/A | 556,171 | Open-ended | Acc, F1, EM, BLEU |
|  | Genome-Bench [766] [link] | Multi-omics | Research problems | N/A | Text QA | 2025.06 | EN | Academic and research resources | N/A | N/A | Data generation and review | GPT-4 Turbo, GPT- 4o | 3,332 | MCQ | Acc |
|  | GeneChat-test [636] [link] | Multi-omics | Nucleotide sequence | N/A | Text QA | 2025.06 | EN | Scientific databases | N/A | N/A | Data generation | N/A | N/A | Open-ended | BLUE, METEOR |
|  | GeneChat [636] [link] | Multi-omics | Nucleotide sequence | N/A | Text QA | 2025.06 | EN | Scientific databases | N/A | N/A | Data generation | N/A | 2,973 | Open-ended | BLEU, METEOR |
|  | Genomics instructions [510] [link] | Multi-omics | Nucleotide sequence | N/A | Text QA | 2025.04 | EN | Academic and research resources | N/A | N/A | Data generation | N/A | 403,814 | Classification, Regression | F1, MCC, AUROC, PCC |
|  | BixBench [985] [link] | Multi-omics | Genomics transcriptomics text | Expert | Text QA | 2025.03 | EN | Academic and research resources | Semi-automated | Data and review | generation 53 | Claude 3.5 Sonnet | 296 | Open-ended, MCQ | Acc |
|  | Seq2Func [937] [link] | Multi-omics | Nucleotide sequence | N/A | Text QA | 2025.02 | EN | Scientific databases | Automated | N/A | Data generation | N/A | 33,000 | MCQ | MCC, F1 |
|  | DNA2Image [937] [link] | Multi-omics | Nucleotide sequence | N/A | Generation | 2025.02 | EN | Scientific databases | Automated | N/A | Data generation | N/A | 4,800 | Generation | Invalid percentage, F1 |
|  | DNA Long Bench [986] [link] | Multi-omics | DNA sequence | N/A | Classification, Regression | 2025.01 | EN | Scientific databases; Academic and research resources | Automated | N/A | N/A | N/A | 213,416 | Classification, Regression | SCC, PCC, AUROC |
|  | LLaMA-Gene (protein) [40] [link] | Multi-omics | Protein sequence | N/A | Text QA | 2024.12 | EN | Scientific databases | N/A | N/A | Data generation | N/A | 6,991 | Open-ended | Acc |
|  | LLaMA-Gene (DNA) [40] [link] | Multi-omics | DNA sequence | N/A | Text QA | 2024.12 | EN | Scientific databases | N/A | N/A | Data generation | N/A | 19,839 | Open-ended | Acc |
|  | NT Benchmark [318] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2024.10 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 38,822 | MCQ | MCC |
|  | BioinformaticsBench [987] [link] | Multi-omics | Textbook | Undergraduate | Text QA | 2024.06 | EN | Books and literary works, Aca- demic and research resources | Semi-automated | 4 | N/A | GPT-3.5, GPT-4, GPT-4 Turbo | 602 | MCQ, True/False, Open-ended | Acc |
|  | genomics-long-range- benchmark [761] [link] | Multi-omics | Nucleotide sequence | N/A | Classification, Regression | 2024.05 | EN | Academic and research resources | N/A | N/A | N/A | N/A | N/A | Classification, Regression | MCC |
|  | RNA-QA [640] [link] | Multi-omics | RNA sequence | N/A | Text QA | 2024.05 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 121 K | Open-ended | Precision, Recall, F1, ROUGE |
|  | BioinfoBench [988] [link] | Multi-omics | RNA sequence | Undergraduate | Text QA | 2023.10 | EN | Other sources | Semi-automated | N/A | Data review | ChatGPT | 200 | MCQ | Acc, Perplexity, Next- token likelihood |
|  | BioCoder [120] [link] | Multi-omics | Codes | Undergraduate | Text QA | 2023.08 | EN | Integration of existing datasets, Academic and research resources | Automated | N/A | N/A | N/A | 2522 | Open-ended | Acc |
|  | SpeciesClassification [989] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2023.06 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 5 species genomes | MCQ | Acc |
|  | GUE Benchmark [317] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2023.06 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 80,648 | MCQ | MCC, F1 |
|  | Genomic Benchmark [937] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2023.05 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 191,589 | MCQ | Acc, F1 |
|  | GeneTuring [765] [link] | Multi-omics | Biomedical knowledge base | N/A | Text QA | 2023.03 | EN | Academic and research resources | N/A | N/A | Data generation | GPT-2, BioGPT, BioMedLM, GPT-3, ChatGPT, New Bing | 600 | MCQ | Acc |
|  | Human Pancreas [938] [link] | Multi-omics | scRNA-seq | N/A | Classification | 2023.01 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 4,218 | Classification | Acc, Precision, Recall, F1 |
|  | Myeloid [941] [link] | Multi-omics | scRNA-seq | N/A | Classification | 2021.02 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 3,430 | Classification | Acc, Precision, Recall, F1 |
|  | Human Cell Atlas Dataset [942] [link] | Multi-omics | scRNA-seq | N/A | Classification | 2021.02 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 84,363 | Classification | Acc, F1 |
|  | Human enhancers Ensembl [760] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2021.01 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 154,842 | MCQ | MCC |
|  | Human regulatory En- sembl [760] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2021.01 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 289,061 | MCQ | MCC |
|  | Human ocr Ensembl [760] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2021.01 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 174,756 | MCQ | MCC |
|  | Multiple Sclerosis [944] [link] | Multi-omics | scRNA-seq | N/A | Classification | 2019.07 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 13,468 | Classification | Acc, Precision, Recall, F1 |
|  | APARENT [804] [link] | Multi-omics | Nucleotide sequence | N/A | Regression | 2019.06 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 8,000 | Regression | R2 |
|  | Human enhancers Cohn [937] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2018.02 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 27,791 | MCQ | MCC |
|  | Human non-TATA promot- ers [990] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2017.02 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 36,131 | MCQ | MCC |
|  | Zheng68k [946] [link] | Multi-omics | scRNA-seq | N/A | Classification | 2016.07 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 68,450 | Classification | Acc, F1 |
|  | Drosophila enhancers Stark [991] [link] | Multi-omics | Nucleotide sequence | N/A | Classification | 2014.06 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 6,914 | MCQ | MCC |
|  | COMET [307] [link] | Multi-omics | DNA, RBA, Protein Sequence/Residue | N/A | Classification, Regression | 2024.12 | EN | Academic and research resources | N/A | N/A | N/A | N/A | 1.22M | Classification, Regression | R2, PCC, F1, SCC |
|  | AdaBrain-Bench [992] [link] | Neuroscience | EEG | N/A | Classification | 2025.07 | EN | Integration of existing datasets | N/A | N/A | N/A | N/A | N/A | Open-ended | Acc, AUROC, AUPRC, F1, PCC, R2 |
|  | FDA Pharmaceuticals FAQ [993] [link] | Pharmacy | FAQ-style text | Expert | Text QA | 2023.03 | EN | Web and Internet content | Automated | N/A | N/A | N/A | 1,681 | MCQ | Acc |
|  | repoDB [803] [link] | Pharmacy, Healthcare and Medical Sci- ences | Drug-disease relationships, Clinical trial outcomes | Expert | Classification, Text QA | 2017.03 | EN | Scientific databases | Automated | N/A | N/A | scripts | 15,648 | MCQ, Retrieval | AUROC, AUPRC, Acc |
| Chemistry | OmniGenBench [994] [link] | Biochemistry, Multi-omics | DNA sequence, RNA sequence, TF binding, etc. | N/A | Classification | 2025.05 | N/A | Integration of existing datasets, Academic and research resources | N/A | N/A | N/A | N/A | N/A | N/A | AUROC, F1, RMSE, R2 |
|  | MOSES [606] [link] | Biochemistry | SMILES | Expert | Raw text | 2020.07 | EN | Academic and research resources | Manual | N/A | Data review | N/A | 1,936,962 | Generation | Chemical validity, Drug- likeness |
|  | ChEMBL [216] [link] | Biochemistry | SMILES | Expert | Raw text | 2012.01 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 1.96M | Generation | Chemical validity, Drug- likeness |
|  | ChemRxivQuest [948] [link] | General Chemistry | Academic papers | Expert | Text QA | 2025.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | NA | 970 | Open-ended | Acc |
|  | ScholarChemQA [105] [link] | General Chemistry | Academic papers | Expert | Text QA | 2025.02 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 40K | MCQ | Acc |
|  | ChemSafetyBench [752] | General Chemistry | Text | Expert | Raw text | 2024.11 | EN | Academic and research resources | Automated | N/A | Data generation and review | NA | 30K+ | Open-ended | Acc, Recall, Precision, F1, safety/quality score, etc. |
|  | ChemEval [751] | General Chemistry | Text | Expert | Raw text | 2024.09 | EN | Academic and research resources | Automated | N/A | Data generation and review | NA | unknown tasks) | (42 Open-ended | Acc, BLEU-2, F1, etc. |
|  | ChemNLP [949] [link] | General Chemistry | Text | Secondary school | Text QA | 2023.01 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 27.6K | Classification, NER, Generation | Acc, ROUGE |
|  | ZINC [215] [link] | General Chemistry | SMILES | Expert | Raw text | 2012.10 | EN | Academic and research resources | Manual | N/A | Data review | N/A | 250K | Generation | Chemical validity, Drug- likeness |
|  | PMO [214] [link] | General Chemistry | SMILES | Expert | Raw text | 2022.05 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 10K | Open-ended | target property, Chemical validity, Drug-likeness |
|  | DeepProtein [950] [link] | Pharmacy | Protein sequence, SMILES | Expert | Raw text | 2025.05 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 78K | Classification, Regression | Acc, MAE, F1, AUPRC, AUROC, R2, etc. |
|  | TrialBench [753] [link] | Pharmacy | SMILES, Disease code | Expert | Raw text | 2024.09 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 470K | Open-ended | F1, Recall, Precision, MSE, etc. |
|  | TDC2 [951] [link] | Pharmacy | SMILES, Protein sequence, Genome sequence | Expert | Raw text | 2024.09 | EN | Academic and research resources | Manual | N/A | Data generation and review | NA | 3.4B tokens | Open-ended | F1, Recall, Precision, MSE, etc. |
|  | PCQM4Mv2 [995] [link] | Pharmacy | Molecular graph | N/A | Regression | 2022.11 | EN | Academic and research resources | Automated | N/A | N/A | N/A | 3,746,619 | Regression | MAE |
|  | SBDDBench [952] [link] | Pharmacy | Protein sequence, SMILES | Expert | Protein-ligand | 2022.06 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 5K | Open-ended | binding affinity, Chemical validity, Drug-likeness |
|  | GEOM [996] [link] | Pharmacy | 3D conformation | N/A | Regression | 2022.04 | EN | Academic and research resources | Automated | N/A | N/A | CREST (GFN2- xTB) | 37M confor- mations | Regression | MAE, RMSD |
|  | TOP [953] [link] | Pharmacy | SMILES | Expert | Raw text | 2022.02 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 12K | Open-ended | F1, Recall, AUPRC, etc. |
|  | TDC [243] [link] | Pharmacy | SMILES, Protein sequence, Genome sequence | Expert | Raw text | 2021.06 | EN | Academic and research resources | Manual | N/A | Data generation and review | NA | 0.2B tokens | Open-ended | F1, Recall, Precision, MSE, etc. |
|  | DeepPurpose [610] [link] | Pharmacy | Protein sequence, SMILES | Expert | Raw text | 2020.12 | EN | Academic and research resources | Automated | N/A | Data generation and review | N/A | 5,074 | Classification, Regression | MSE, PCC, F1, AUROC, AUPRC, etc. |
|  | DrugBank [954] [link] | Pharmacy | SMILES | Expert | Raw text | 2018.01 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 17.47K | Open-ended | Acc |
|  | USPTO [612] | Synthetic Chemistry | SMILES | Expert | Raw text | 2015.07 | EN | Patent databases | Manual | N/A | Data generation and review | NA | 1,939,253 | Open-ended | Acc, F1, MSE, etc. |
|  | FSReD [222] [link] | General Physics | Text | Expert | Text QA | 2019.05 | EN | Comprehensive multi-source inte- gration | Automated | N/A | Data review | N/A | 120 | Regression | MSE, Exact Match |
|  | PIQA [680] [link] | General Physics | Text | Primary school | Text QA | 2020.01 | EN | Other sources | Semi-automated | N/A | Data generation and review | N/A | 2,000 | MCQ | Acc |
|  | SRBench [746] [link] | General Physics | Text | N/A | Text QA | 2021.07 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | N/A | 252 | Open-ended | Acc, Simplicity, Exact Match |
|  | PROST [737] [link] | General Physics | Text | N/A | Text QA | 2021.08 | EN | Other sources | Semi-automated | 4 | Data generation | N/A | 18,736 | MCQ | Acc |
| Physics | MM-PhyQA [735] [link] | Kinematics, Mechanics, Electrostatics and Current Electricity, Thermodynam- ics, Optics, Magnetism, etc. | Text | High school | VQA with CoT | 2024.04 | EN | Comprehensive multi-source inte- gration | Semi-automated | 8+ | Data generation and review | ChatGPT | 675 | MCQ | Acc, ROUGE |
|  | MVBench [750] [link] | General Physics | Video | N/A | Video QA | 2024.05 | EN | Comprehensive multi-source inte- gration | Automated | 0 | Data review | N/A | 4,000 | MCQ | Acc |
|  | UGPhysics [740] [link] | Mechanics, Thermodynamics, Electro- magnetism, Modern Physics | Text (problem statements, equa- tions, reasoning) | Undergraduate | Text QA | 2025.01 | EN, ZH | Academic and research resources | Semi-automated | N/A | Data generation and review | GPT-4o | 11,040 | MCQ, Open- ended, True/False, Retrieval | Acc |
|  | PhysReason [739] [link] | Mechanics, Electromagnetism, Ther- modynamics, etc. | Text (problem statements, equa- tions), Diagrams (physics illustra- tions) | Undergraduate, Graduate, Expert | Text QA, VQA | 2025.02 | EN | Comprehensive multi-source inte- gration | Semi-automated | 4 | Data generation and review | GPT-4 | 1,200 | MCQ | Acc |
|  | TPBench [744] [link] | Cosmology, High Energy Theory, Gen- eral Relativity, Astrophysics, Electro- magnetism, Quantum Mechanics, Me- chanics, etc. | Text | N/A | Text QA | 2025.02 | N/A | Other sources | Manual | N/A | Data generation and review | N/A | 57 | Open-ended | Acc, AI-based Holistic Grading |
|  | PHYSICS [742] [link] | Mechanics, Electromagnetism, Ther- modynamics, Optics, etc. | Text (problem statements, equa- tions, reasoning), Diagrams (illus- trations, charts, experimental se- tups) | Undergraduate | Text QA, VQA | 2025.03 | EN | Comprehensive multi-source inte- gration | Manual | N/A | Data generation and review | N/A | 1,297 | Open-ended | Acc |
|  | PhysicsArena [681] [link] | Mechanics, Electromagnetism, Ther- modynamics, etc. | Text (problem statements, equa- tions, reasoning), Diagrams (illus- trations, charts, experimental se- tups) | Expert | Text QA, VQA | 2025.05 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | N/A | 5,100 | Open-ended | Acc |
|  | PHYBench [745] [link] | Mechanics, Electricity, Thermodynam- ics, Optics, Modern Physics, etc. | Research problems | Undergraduate | Text QA | 2025.05 | EN | Comprehensive multi-source inte- gration | Semi-automated | 178 | Data generation and review | o1, DeepSeek-R1 | 500 | Open-ended | EED |
|  | PhyX [741] [link] | Mechanics, Quantum Mechanics, Thermodynamics, Electromagnetism, Atomic Physics, etc. | Text (problem statements, equa- tions, reasoning), Diagrams (illus- trations, charts, experimental se- tups) | Undergraduate | Text QA, VQA | 2025.05 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | GPT-4o | 3,000 | MCQ, Open- ended | Acc |
|  | PhysUniBench [738] [link] | Mechanics, Electromagnetism, Optics, Atomic Physics, etc. | Text (problem statements, equa- tions), Diagrams (physics illustra- tions) | Undergraduate | VQA | 2025.06 | EN, ZH | Comprehensive multi-source inte- gration | Manual | N/A | Data generation and review | N/A | 3,304 | Open-ended, MCQ | Acc |
|  | IntPhys 2 [748] [link] | General Physics | Video, Text (scene parameters, ob- ject categories, trajectories, physi- cal attributes) | N/A | Video QA | 2025.06 | N/A | Other sources | Semi-automated | N/A | Data generation and review | N/A | 1,400 | Open-ended | Acc |
|  | MVP-Bench [749] [link] | General Physics | Video | N/A | Video QA | 2025.06 | EN | Encyclopedias and knowledge bases | Semi-automated | N/A | Data generation and review | OpenAI CLIP (ViT- L/14) | 55,000 | Open-ended | Acc |
|  | SeePhys [743] [link] | Mechanics, Electromagnetism, Parti- cle Physics, Optics=, Astrophysics, Thermodynamics, Quantum Mechan- ics, etc. | Text (problem statements, equa- tions), Diagrams (physics illustra- tions) | Secondary school, Un- dergraduate, Graduate | VQA | 2025.07 | EN,ZH | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data generation and review | GPT-4o | 2,000 | Open-ended | Acc |
| Astronomy | Astro-QA [779] [link] | Astronomy | Astronomy Olympiad competitions, Astronomy exams, Online encyclopedias | Undergraduate | Text QA | 2025.06 | Mixed | Comprehensive multi-source inte- gration | Manual | 30+ | Data generation and review | N/A | 3,082 | Open-ended | DGscore, BLEU, ROUGE, chrF |
|  | Astrovisbench [997] [link] | Astronomy | Galaxy images | Expert | VQA | 2025.06 | EN | Comprehensive multi-source inte- gration | Semi-automated | 6 | Data review | GPT-4o, Claude 3.5 Sonnet | 432 | Open-ended | VIscore, Image error level, Expert evaluation |
|  | AstroMLab 1 [778] [link] | Astronomy | Academic papers | Expert | Text QA | 2024.11 | EN | Academic and research resources | Automated | N/A | Data review | Gemini-1.5-Pro | 4,425 | MCQ | Acc |
|  | AstroPT [669] [link] | Astronomy | Astronomical images | Expert | Image-text | 2024.05 | EN | Web and Internet content, Scientific databases | Automated | N/A | Data review | DESI Legacy Survey API | 8.6 M | Classification | PCC, Acc |
|  | Astro-NER [725] [link] | Astronomy | Academic papers | Expert | Text QA | 2024.05 | EN | Academic and research resources | Semi-automated | 4 | Data generation and review | GPT-3.5 | 5,000 | Open-ended | Precision, Recall, F1 |
|  | AstroLLaMA [561] [link] | Astronomy | Academic papers | Expert | Text QA | 2023.09 | EN | Academic and research resources,Web and Internet content | Manual | N/A | Data review | N/A | 9.5 M | Open-ended | Perplexity, Cosine similar- ity |
|  | ATel [956] [link] | Astronomy | Academic papers | Expert | Text QA | 2023.05 | EN | Academic and research resources | Manual | N/A | Data review | N/A | 234 | Open-ended | Acc |
|  | PhyE2Es [220] [link] | Astrophysics | Text with formulae | Expert | Raw text | 2025.03 | EN | Scientific databases | Automated | N/A | Data generation and review | OpenLLAMA-2-3B | 8,000 | Regression | Acc, Numerical precision, Formula complexity, For- mula depth |
|  | Pathfinder Dataset [782] [link] | Astrophysics | Academic papers, ADS | Expert | Text QA with CoT | 2024.11 | EN | Web and Internet content, Aca- demic and research resources | Automated | 36+ | Data generation and review | text-embedding-3- small | 385,166 | Open-ended | Acc, MRR, Recall, NDCG, relevance score |
|  | Starwhisper-pilsar [780] [link] | Astrophysics | Pulsar diagnostic plots, Pulsars sig- nals | Expert | VQA | 2024.04 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | DeepSeek-VL-7B, InternVL2-40B | 106,674 | Open-ended | Acc, Recall, Precision, F1, etc. |
|  | PAPERCLIP [781] [link] | Astrophysics | Synthetic conversation, Astronomi- cal images | Expert | Text QA | 2024.03 | EN | Academic and research resources,Scientific databases | Automated | N/A | Data generation and review | Mixtral-8x7B- Instruct | 31,859 | Open-ended | Acc |
| Materials Science | CheMatAgent [119] [link] | Materials Science | Scientific instruction | Expert | Text QA | 2025.06 | EN | Other sources | Manual | N/A | Data generation and review | N/A | 137 | Open-ended | Acc |
|  | ChEBI-20-MM [692] [link] | Materials Science | InChI, IUPAC, SELFIES, Science QA, Molecular Image | Expert | Text QA | 2025.01 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 3,300 | Open-ended | BLEU, ROUGE, METEOR, CIDEr |
|  | LLM4MatBench [756] [link] | Materials Science | CIF, Chemical composition, Nu- merical property | Expert | Text QA | 2024.10 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 1.9M | Open-ended | Acc |
|  | MatText [998] [link] | Materials Science | Chemical composition, Numerical property | Expert | Text QA | 2024.08 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 2,000,000 | Open-ended | MAE, AUROC |
|  | MatBookQA [757] [link] | Materials Science | Science QA | Expert | Text QA | 2024.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 650 | Open-ended | Acc |
|  | MaSCQA [108] [link] | Materials Science | Science QA | Expert | Text QA | 2023.08 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 650 | Open-ended | Acc |
|  | MatSci-NLP [999] [link] | Materials Science | Chemical composition, Numerical property | Expert | Text QA | 2023.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 169,197 | Open-ended | Acc, F1 |
|  | ChEBI-20 [691] [link] | Materials Science | Scientific instruction | Expert | Text QA | 2021.11 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 3,301 | Open-ended | BLEU, ROUGE, METEOR, CIDEr |
|  | MOSES [690] [link] | Materials Science | SMILES | Expert | Text QA | 2020.11 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 176,000 | Open-ended | Uniqueness, Validity, Frag, Scaff, SNN |
|  | MatBench [71] [link] | Materials Science | CIF, Numerical property, Chemical composition | Expert | Text QA | 2020.09 | EN | Scientific databases | Manual | N/A | Data generation and review | N/A | 408,062 | Open-ended | MAE, AUROC |
|  | GuacaMol [758] [link] | Materials Science | SMILES | Expert | Text QA | 2019.03 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 2M | Open-ended | Validity, Uniqueness, Novelty |
|  | MoleculeNet [218] [link] | Materials Science | SMILES | Expert | Text QA | 2017.03 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 700,000 | Open-ended | AUROC, AUPRC, RMSE, MAE |
|  | MaCBench [207] [link] | Materials Science, Chemistry | Science QA, AFM Image | Expert | VQA | 2024.11 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 628 | Open-ended | Acc |
|  | MMSci [75] [link] | Materials Science, Chemistry | Science QA | Graduate | VQA | 2024.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 742,273 | Open-ended | Acc |
|  | ClimaQA [671] [link] | Atmosphere | Textbooks | Expert | Text QA | 2025.03 | EN | Books and literary works | Semi-automated |  | Data review | GPT-4o | 3,633 | MCQ, Open- ended | Acc, BLEU, etc. |
|  | WeatherQA [728] [link] | Atmosphere | Remote sensing, Science QA | Expert | VQA (multi-image) | 2024.06 | EN | Scientific databases | Semi-automated | 4 | Data review |  | 600 | MCQ, Open- ended | Acc, F1, BLEU, etc. |
|  | ClimateBERT [783] [link] | Atmosphere | Corporate annual reports, Sustain- ability reports | Secondary school | Text QA | 2022.12 | EN | Web and Internet content | Manual | 4+ | Data review | Prodigy | 320 | MCQ | Acc |
|  | OceanBench [569] [link] | Hydrosphere | Academic papers | Expert | Text QA | 2024.09 | EN | Academic and research resources | Automated | 10+ | Data review | GPT-4, GPT-3.5 | 13,000 | Open-ended | Win Rate |
|  | OmniEarth-Bench [786] [link] | Hydrosphere, Biosphere, Lithosphere, Atmosphere, Cryosphere | Remote sensing, Science QA | Expert | VQA with CoT (multi-image) | 2025.05 | EN | Integration of existing datasets | Manual | 40+ | Data generation and review |  | 29,779 | MCQ | Acc, Precision, Recall, F1 |
| Earth Science | MSEarth [152] [link] | Hydrosphere, Biosphere, Lithosphere, Atmosphere, Cryosphere | Academic papers | Expert | VQA with CoT | 2025.05 | EN | Academic and research resources | Semi-automated | 20+ | Data review | GPT-4o | 11,500 | MCQ, Open- ended | BLEU, BERTScore, Acc |
|  | EarthSE [670] [link] | Hydrosphere, Biosphere, Lithosphere, Atmosphere, Cryosphere | Academic papers | Expert | Text QA with CoT | 2025.05 | EN | Academic and research resources | Semi-automated | 20+ | Data review | GPT-4o | 10,000 | Open-ended | Acc |
|  | GeoBench [567] [link] | Lithosphere | Science QA | Expert | Text QA | 2023.06 | EN | Web and Internet content, Aca- demic and research resources | Semi-automated | 10+ | Data review |  | 2,516 | MCQ, Open- ended | Acc, GPTScore |
|  | XLRS-Bench [785] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2025.03 | EN, ZH | Academic and research resources | Semi-automated | 55 | Data generation and review | GPT-4o | 32,389 | MCQ, Open- ended | Acc, IoU, BLEU, etc. |
|  | LRS-VQA [552] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2025.03 | EN | Academic and research resources | Automated | N/A | N/A | Qwen2-VL, GPT-4V | 7,333 | Open-ended | Acc |
|  | MME-RealWorld-RS [1000] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2024.08 | EN, ZH | Academic and research resources | Manual | N/A | Data generation and review | N/A | 3,738 | MCQ | Acc |
|  | VRSBench [797] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2024.06 | EN | Academic and research resources | Semi-automated | N/A | Data review | GPT-4V | 62,917 | Open-ended | Acc, IoU, BLEU, etc. |
|  | GeoChat [588] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2023.11 | EN | Academic and research resources, Integration of existing datasets | Automated | N/A | N/A | Vicuna | 10K | Open-ended | Acc, IoU, METEOR |
|  | RSIEval [784] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2023.07 | EN | Academic and research resources | Manual | 5 | Data generation and review | N/A | 1,036 | Open-ended | Acc, BLEU, ROUGE, etc. |
|  | DIOR-RSVG [805] [link] | Remote Sensing | Remote sensing | N/A | Image-text | 2022.10 | EN | Academic and research resources | Semi-automated | N/A | Data review | N/A | 17,402 | Open-ended | IoU |
|  | NWPU-Captions [1001] [link] | Remote Sensing | Remote sensing | N/A | Image-text | 2022.08 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 31,500 | Open-ended | BLEU, METEOR, etc. |
|  | RSVQA-HRBEN [794] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2020.05 | EN | Scientific databases | Automated | N/A | N/A | N/A | 77,232 | Open-ended | Acc |
|  | RSVQA-LRBEN [794] [link] | Remote Sensing | Remote sensing | N/A | Image-text, VQA | 2020.05 | EN | Scientific databases | Automated | N/A | N/A | N/A | 1,066,316 | Open-ended | Acc |
|  | RSICD [1002] [link] | Remote Sensing | Remote sensing | N/A | Image-text | 2017.12 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 10,921 | Open-ended | BLEU, METEOR, CIDEr |
|  | UCM-Captions [1002] [link] | Remote Sensing | Remote sensing | N/A | Image-text | 2016.07 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 2,100 | Open-ended | BLEU, METEOR, CIDEr |
|  | Sydney-Captions [1002] [link] | Remote Sensing | Remote sensing | N/A | Image-text | 2016.07 | EN | Academic and research resources | Manual | N/A | Data generation | N/A | 613 | Open-ended | BLEU, METEOR, CIDEr |

# TABLE VI: Summary of general science evaluation datasets for scientific LLMs/MLLMs. [link] directs to dataset websites.

| Dataset | Scientific Domain | Modality | Type | Release | Language | Source | Annotation Pipeline | Human Annotators | Human Tasks | Auto-annotation Tools | Size | Level | Evaluation Type | Metrics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MMMU [789] [link] | Science (Biology, Chemistry, Geography, Math, Physics), Health & Medicine (Basic Medical Science, Clinical Medicine, Diagnostics, Pharmacy, Public Health), Tech & Engineering (Materials, etc.) | Scientific VQA, MRI, CT, X-ray, etc. | VQA | 2023.11 | EN | Comprehensive multi-source inte- gration | Semi-automatic | 50 | Data review | Claude, GPT-4, | GPT-4V 11,550 | Expert | MCQ | Acc |
| MMMU Pro [790] [link] | Science (Biology, Chemistry, Geography, Math, Physics), Health & Medicine (Basic Medical Science, Clinical Medicine, Diagnostics, Pharmacy, Public Health), Tech & Engineering (Materials, etc.) | Scientific VQA, MRI, CT, X-ray, etc. | VQA | 2023.11 | EN | Comprehensive multi-source inte- gration | Semi-automatic | N/A | Data review | Claude, GPT-4, | GPT-4V 5,190 | Expert | MCQ | Acc |
| ScienceQA [106] [link] | Biology, Earth Science, Physics, Chemistry, Geography, etc. | Scientific query, Scientific instruc- tion, Science textbooks and litera- ture | VQA | 2022.01 | EN | Books and literary works | Manual | 9+ | Data generation and review | ViT, GPT-2 | 21.2k | Primary school, Secondary school | MCQ | Acc |
| SciQA [107] [link] | Material Science, Chemistry, Life sci- ences | Scientific query | Text QA | 2023.05 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 2,565 | Expert | Open-ended | Acc |
| Scicode [121] [link] | Material Science, Biology, Chemistry, Physics, Mathematics | Scientific Instruction | Text QA | 2024.08 | EN | Academic and research resources | Manual | N/A | Data generation and review | N/A | 338 | Expert | Open-ended | pass@1 |
| CURIE [109] [link] | Materials Science, Life Sciences, Physics, Earth Science | Scientific query | VQA | 2025.04 | EN | Integration of existing datasets | Manual | N/A | Data generation and review | N/A | 580 | Expert | Open-ended | Acc |
| TheoremQA [1003] [link] | Physics, Mathematics | Theorems | Text QA | 2023.12 | EN | Books and literary works, Encyclo- pedias and knowledge bases | Manual | N/A | Data generation and review | N/A | 800 | Undergraduate, Expert | Open-ended | Acc |
| SciBench [441] [link] | Physics, Chemistry | Science QA | Text QA | 2023.09 | EN | Books and literary works | Manual | 7 | Data review | N/A | 695 | Undergraduate | Open-ended | Acc |
| JEEBench [1004] [link] | Physics, Chemistry | Science Exams | Text QA | 2023.12 | EN | Other sources | Semi-automated | N/A | Data generation and review | N/A | 515 | Expert | MCQ | Acc |
| MMLU [1005] [link] | Physics (College Physics, Conceptual Physics, High School Physics), Chem- istry (College Chemistry, High School Chemistry), Biology (College Biology, High School Biology) | Science QA | Text QA | 2020.09 | EN | Books and literary works | Manual | 7 | Data generation and review | N/A | 15.9k | Secondary School, Undergraduate, Expert | MCQ | Acc |
| C-Eval [787] [link] | Chemistry (College Chemistry, High School Chemistry, Middle School Chemistry), Physics (College Physics, High School Physics, Middle School Physics), Biology (High School Biology, Middle School Biology), Medicine (Veterinary Medicine, Basic Medicine, Clinical Medicine, Physician), Earth Science (High School Geography, Middle School Geography) | Exam questions, Chinese educa- tional assessments | Text QA | 2023.05 | ZH | Books and literary works | Manual | 12 | Data generation and review | N/A | 13.9k | Primary school, Secondary school, Undergraduate | MCQ | Acc |
| GPQA [457] [link] | Chemistry, Biology, Physics | Graduate-level scientific questions | Text QA | 2023.11 | EN | Other sources | Manual | 8 | Data generation and review | N/A | 448 | Expert | MCQ | Acc |
| ArXivQA [604] [link] | Physics (Accelerator Physics, High En- ergy Physics - Lattice, Mathematical Physics, etc.), Chemistry (Chemical Physics), Biology (Quantitative Biol- ogy), Material (Materials Theory) | scientific figure question-answer | Text QA | 2024.05 | EN, ZH | Other sources | Semi-automated | N/A | Data generation and review | GPT-4V | 249,587 | Expert | MCQ | Acc |
| Xiezhi [1006] [link] | Agronomy (Crop Science, Veterinary Medicine), Science (Chemistry, Physics), Medicine (Traditional Chinese Medicine) | Professional exams | Text QA | 2024.05 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | ChatGPT, | Llama-7B 250k | Expert | MCQ | Acc |
| SuperGPQA [791] [link] | Medicine, Science, Agriculture | Graduate Disciplines QA | Text QA | 2025.02 | EN | Other sources | Semi-automatic | 80+ | Data generation and review | N/A | 26.5k | Expert | MCQ | Acc |
| BMMR [1007] [link] | Health (Medicine, Pharmacy, etc.), Natural Sciences (Physics, Biology, etc.), Agriculture | Image, College-level visual ques- tion answering, OCR-based QA | VQA | 2025.07 | EN, ZH | Web and Internet content, Books and literary works, Integration of existing datasets | Semi-automated | N/A | Data generation and review | N/A | 109,449 | Primary school, Undergraduate, Secondary school | MCQ | Acc |
| OlympiadBench [736] [link] | Physics, Mathematics | QA from math and physics compe- titions, Image | Text QA, VQA | 2024.02 | ZH, EN | Other sources | Semi-automated | 14 | Data generation and review | N/A | 8.5k | Expert | Open-ended | Acc |
| LLM-SRBench [747] [link] | LSR-Synth (Chemistry, Biology, Physics, Material Science), LSR- Transform | Structured Data | text | 2025.04 | EN | Comprehensive multi-source inte- gration | Fully-automated | 0 | Data generation and review | N/A | 239 | Expert | Open-ended | Exact Match, MSE |
| HLE [462] [link] | Biology (Marine Biology, Molecular Biology, Computational Biology, Ecol- ogy, etc.), Chemistry (Chemical En- gineering, Biochemistry, etc.), Physics (Biophysics), Materials Science | Organic reaction analysis, Molecu- lar text, Chemical equations, Med- ical question answering, Textbook QA, etc. | Text QA | 2025.01 | EN | Academic and research resources | Manual | nearly 1000 | Data generation and review | GPT-4o | 2,500 | Expert | MCQ, Open- ended | Acc, Calibration Error |
| SFE [443] [link] | Astronomy, Chemistry, Life Science, Materials Science, Earth Science | Protein structure, RNA structure, Molecular structure, etc. | VQA | 2025.06 | EN, ZH | Scientific databases, Academic and research resources | Manual | N/A | Data generation and review | GPT-4o | 1,660 | Expert | MCQ, Open- ended | Exact Match, LLM-as-a- Judge score, BERTScore, IoU |
| SciEval [792] [link] | Chemistry, Physics, Biology | Text (equations, molecules, chemi- cal reactions, scientific QA, etc.) | Text QA | 2023.08 | EN | Comprehensive multi-source inte- gration | Semi-automated | N/A | Data review | GPT-4 | 18,000 | Undergraduate, Graduate | MCQ, Open- ended, | True/False Acc, BLEU, MSE |
| SciKnowEval [442] [link] | Chemistry, Physics, Biology, Materials Science | Textbook QA, Literature QA, SMILES, IUPAC, Equations, etc. | Text QA, Classifica- tion, Regression | 2024.06 | EN | Comprehensive multi-source inte- gration, Academic and research re- sources, Scientific databases, Inte- gration of existing datasets | Semi-automated | N/A | Data review | GPT-4o, Claude3, LLaMA, | GPT-3.5, Qwen 70,203 | Undergraduate, Graduate, Expert | MCQ, True/False, Open-ended | Acc, F1, BLEU, ROUGE, Smith-Waterman, Tanimoto |
| AGIEval [788] [link] | Chemistry (GK-chemistry), Physics (GK-physics), Biology (GK-biology), Geography (GK-geography) | Textbook, Literature, SMILES, IU- PAC, Equations, etc. | Text QA | 2023.09 | EN, ZH | Academic and research resources, Integration of existing datasets | Semi-automated | N/A | Data review | ChatGPT, GPT-4 | 8,062 | Secondary school, Undergraduate | MCQ, Open- ended | Acc, EM |
| ScienceAgentBench [83] [link] | Bioinformatics, Computational chem- istry, Geographical information sci- ence, Psychology & cognitive neuro- science | Microscopy images, SMILES strings, Geospatial data, EEG, ECG, IMU, etc. | VQA | 2024.10 | EN | Academic and research resources, Integration of existing datasets | Manual | 9 | Data generation and review | N/A | 102 tasks | Expert | Open-ended | VER, SR, Code- BERTScore, GPT-4o Judge |

# TABLE VII: Summary of scientific large language models. [link] directs to model websites.

| Scientific Domain | Models | Domain | Parameters | Base LLM | Modality encoder | Release | Open-source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| General-purpose | Galactica [30] [link] | General Science | 120B | N/A | N/A | 2022.11 | ✓ |
|  | DARWIN [448] [link] | General Science | 7B | LLaMA-7B, Vicuna-7B | N/A | 2023.08 | ✓ |
|  | FORGE [1008] [link] | General Science | 26B | GPT-NeoX | N/A | 2023.11 | ✓ |
|  | SciGLM [41] [link] | General Science | 6B /32B | ChatGLM3 | N/A | 2024.01 | ✓ |
|  | SciDFM [451] [link] | General Science | 18.2B-A5.6B | N/A | N/A | 2024.09 | ✓ |
|  | OmniScience [452] [link] | General Science | 70B | LLaMA-3.1 | N/A | 2025.03 | ✗ |
|  | Intern-S1 [47] [link] | General Science | 241B-A28B/8B | Qwen3-235B-A22B, Qwen3-8B | InternViT-6B, InternViT-300M | 2025.08 | ✓ |
| Physics | MechGPT [485] [link] | Mechanics | 13B /70B | LLaMA-2 | N/A | 2023.10 | ✓ |
|  | Xiwu [466] [link] | High Energy Physics | 7B /13B | LLaMA, Vicuna, ChatGLM, Grok- 1 | N/A | 2024.04 | ✓ |
|  | Poseidon [464] [link] | Partial Differential Equations | 0.02B /0.2B /0.6B | scOT | N/A | 2024.05 | ✓ |
|  | L3M [1009] [link] | Astrophysics | 0.5B | Qwen2.5-0.5B-Instruct | N/A | 2025.06 | ✗ |
| Chemistry | ChemLLM [20] [link] | Chemistry, Pharmacy | 7B | InternLM2 | N/A | 2024.06 | ✓ |
|  | LLM-RDF [1010] | Chemistry, chemical synthesis | N/A | GPT-4 | N/A | 2024.11 | ✓ |
|  | InstructMol [468] [link] | Biochemistry, Chemistry, Pharmacy | 7B | LLaMA | molecular graph encoder | 2024.12 | ✓ |
|  | ChemDFM [469] [link] | Chemistry (molecular design), Chemistry | 13B | LLaMA-2 | N/A | 2025.07 | ✓ |
|  | ChemMLLM [200] [link] | Chemistry (molecular design), Pharmacy | 34B | Lumina-mGPT-34B-512 | VQGAN | 2025.08 | ✓ |
|  | Chemma [1011] | Chemistry, Organic Chemistry | 7B | LLaMA-2 | N/A | 2025.07 | ✓ |
|  | Chem3DLLM [470] | Chemistry (Molecular Design), Pharmacy | 7B | Qwen2-7B | ESM-Encoder | 2025.08 | ✓ |
| Materials Science | SMILES-BERT [471] [link] | Materials Science | 30M | BERT-small | N/A | 2019.09 | ✓ |
|  | MolGPT [480] [link] | Materials Science | N/A | N/A | N/A | 2022.05 | ✓ |
|  | MOFormer [1012] | Materials Science | N/A | N/A | N/A | 2022.10 | ✗ |
|  | MatBert-bandgap [474] [link] | Materials Science | 110M | MatBERT | N/A | 2023.03 | ✓ |
|  | Regression Transformer [475] [link] | Materials Science | N/A | N/A | N/A | 2023.04 | ✓ |
|  | MolXPT [477] [link] | Materials Science | N/A | GPT-2 | N/A | 2023.05 | ✓ |
|  | xyztransformer [481] [link] | Materials Science | N/A | N/A | N/A | 2023.05 | ✓ |
|  | polyBERT [472] [link] | Materials Science | N/A | DeBERTa | N/A | 2023.07 | ✓ |
|  | GPT-MolBERTa [479] | Materials Science | N/A | RoBERTa | N/A | 2023.10 | ✗ |
|  | ChemRLformer [1013] | Materials Science | N/A | N/A | N/A | 2023.10 | ✗ |
|  | CrystaLLM [1014] [link] | Materials Science | 70B | LLaMA-2 70B | N/A | 2024.02 | ✓ |
|  | MatText [1015] [link] | Materials Science | N/A | BERT | N/A | 2024.06 | ✓ |
|  | ChatMOF [1016] [link] | Materials Science | N/A | GPT-4, GPT-3.5-turbo, and GPT- 3.5-turbo-16k | N/A | 2024.06 | ✓ |
|  | LHS2RHS [483] | Materials Science | N/A | N/A | N/A | 2024.10 | ✗ |
|  | RHS2LHS [483] | Materials Science | N/A | N/A | N/A | 2024.10 | ✗ |
|  | TGT2CEQ [483] | Materials Science | N/A | N/A | N/A | 2024.10 | ✗ |
|  | CrystaLLM [482] [link] | Materials Science | 200M | GPT-2 | N/A | 2024.12 | ✓ |
|  | molT5-large [1017] [link] | Materials Science | 770M | T5-large | N/A | 2024.12 | ✓ |
|  | Qwen2-KG [476] [link] | Materials Science | 72B | Qwen2-72B | N/A | 2025.02 | ✓ |
|  | LLM-Prop [1018] [link] | Materials Science | 37M | T5-small | N/A | 2025.06 | ✓ |
|  | Crystal Synthesis LLM [484] [link] | Materials Science | 8B | LLaMA-3-8B | N/A | 2025.07 | ✓ |
| Life Sciences | ShizhenGPT [1019] [link] | Healthcare and Medical Sciences | 7B /32B | Qwen2.5 | Qwen2.5-VL vision encoder, Whisper-large-v3 | 2025.08 | ✓ |
|  | ProGen2 [498] [link] | Proteomics | 6.4B /2.7B /764M /151M | N/A | N/A | 2022.06 | ✓ |
|  | BioGPT [934] [link] | Healthcare and Medical Sciences, General Biology | 347M | GPT-2 | N/A | 2022.10 | ✓ |
|  | ESM-2 [490] [link] | Proteomics | 15B /3B /650M /150M/35M / | 8M N/A | N/A | 2023.03 | ✓ |
|  | OphGLM [1020] [link] | Healthcare and Medical Sciences | 6B | ChatGLM-6B | ConvNext | 2023.03 | ✓ |
|  | MedAlpaca [520] [link] | Healthcare and Medical Sciences | 7B /13B | LLaMA | N/A | 2023.04 | ✓ |
|  | DoctorGLM [584] [link] | Healthcare and Medical Sciences | 6B | ChatGLM-6B | N/A | 2023.04 | ✓ |
|  | PMC-LLaMA [1021] [link] | Healthcare and Medical Sciences | 13B | LLaMA | N/A | 2023.04 | ✓ |
|  | scGPT [512] [link] | Multi-omics | 30k /300k /3M /33M | N/A | N/A | 2023.04 | ✓ |
|  | Med-PaLM [31] [link] | Healthcare and Medical Sciences | N/A | PaLM | N/A | 2023.05 | ✗ |
|  | Med-PaLM 2 [1022] [link] | Healthcare and Medical Sciences | N/A | PaLM 2 | N/A | 2023.05 | ✗ |
|  | GatorTronS [16] [link] | Healthcare and Medical Sciences | 345M /3.9B /8.9B | GPT-3 | N/A | 2023.05 | ✓ |
|  | GatorTronGPT [1023] [link] | Healthcare and Medical Sciences | 5B /20B | GPT-3 | N/A | 2023.05 | ✓ |
|  | HuatuoGPT [524] [link] | Healthcare and Medical Sciences | 7B /13B | Baichuan-7B, Ziya-LLaMA-13B- Pretrain-v1 | N/A | 2023.05 | ✓ |
|  | BiomedGPT [1024] [link] | Healthcare and Medical Sciences | 33M /93M /182M | OFA | VQ-GAN | 2023.05 | ✓ |
|  | ClinicalGPT [1025] [link] | Healthcare and Medical Sciences | 7B | BLOOM-7B | N/A | 2023.06 | ✓ |
|  | GENA-LM [1026] [link] | Molecular and Cell Biology, Multi-omics | 110M /336M | BERT | N/A | 2023.06 | ✓ |
|  | NYUTron [1027] [link] | Healthcare and Medical Sciences, Neuroscience, Pharmacy | 190M | BERT | N/A | 2023.06 | ✓ |
|  | ChatDoctor [1028] [link] | Healthcare and Medical Sciences | 7B | LLaMA | N/A | 2023.06 | ✓ |
|  | SoulChat [1029] [link] | Neuroscience, Healthcare and Medical Sciences | 6B | ChatGLM-6B | N/A | 2023.07 | ✓ |
|  | DNAGPT [1030] [link] | Molecular and Cell Biology, Multi-omics | 3B | GPT | N/A | 2023.07 | ✓ |
|  | Med-Flamingo [539] [link] | Healthcare and Medical Sciences | 9B | Openflamingo | Openflamingo | 2023.07 | ✓ |
|  | DISC-MedLLM [900] [link] | Healthcare and Medical Sciences | 13B | Baichuan-13B | N/A | 2023.08 | ✓ |
|  | IvyGPT [1031] [link] | Healthcare and Medical Sciences | 33B | LLaMA-33B | N/A | 2023.08 | ✗ |
|  | Zhongjing [529] [link] | Healthcare and Medical Sciences | 13B | Ziya-LLaMA-13B-V1 | N/A | 2023.08 | ✓ |
|  | Radiology-Llama2 [538] [link] | Healthcare and Medical Sciences | 7B | LLaMA-2 | N/A | 2023.08 | ✓ |
|  | RadFM [1032] [link] | Healthcare and Medical Sciences | 9B | MedLLaMA-13B | 3D ViT | 2023.08 | ✓ |
|  | CPLLM [1033] [link] | Healthcare and Medical Sciences | 13B | Llama2-13B | N/A | 2023.09 | ✓ |
|  | DRG-LLaMA [1034] [link] | Healthcare and Medical Sciences | 7B | LLaMA-7B | N/A | 2023.09 | ✓ |
|  | MindGPT [557] [link] | Neuroscience, Healthcare and Medical Sciences | 124M | GPT-2 | CLIP-ViT-B/32 | 2023.09 | ✗ |
|  | BioinspiredLLM [1035] [link] | General Biology, Molecular and Cell Biology, Pro- teomics | 13B | LLaMA-2 | N/A | 2023.09 | ✓ |
|  | Qilin-Med [1036] [link] | Healthcare and Medical Sciences | 7B | Baichuan-7B | N/A | 2023.10 | ✗ |
|  | CXR-LLAVA [537] [link] | Healthcare and Medical Sciences | 7B | LLaMA-2 | CLIP ViT-L/16 | 2023.10 | ✓ |
|  | InstructProtein [1037] | Proteomics | 1.3B | OPT-1.3B | N/A | 2023.10 | ✗ |
|  | ChiMed-GPT [526] [link] | Healthcare and Medical Sciences | 13B | Ziya-13B-v2 | N/A | 2023.11 | ✓ |
|  | HuatuoGPT-II [42] [link] | Healthcare and Medical Sciences | 7B/13B | Baichuan2-7B-Base, Baichuan2- 13B-Base | N/A | 2023.11 | ✓ |
|  | Taiyi-LLM [1038] [link] | Healthcare and Medical Sciences | 7B | Qwen-7B-base | N/A | 2023.11 | ✓ |
|  | Meditron [38] [link] | Healthcare and Medical Sciences | 7B /70B | LLaMA-2 | N/A | 2023.11 | ✓ |
|  | MAIRA-1 [1039] [link] | Healthcare and Medical Sciences | 7B | Vicuna-7B | RAD-DINO | 2023.11 | ✓ |
|  | MAIRA-2 [1040] [link] | Healthcare and Medical Sciences | 7B | Vicuna-7B-v1.5 | RAD-DINO | 2023.11 | ✓ |
|  | Neuro-GPT [560] [link] | Neuroscience, Healthcare and Medical Sciences | 124M | GPT-2 | EEG Encoder | 2023.11 | ✓ |
|  | PLLaMa [550] [link] | Molecular and Cell Biology, General Biology | 7B /13B | LLaMA-2 | N/A | 2024.01 | ✓ |
|  | EEG-GPT [553] [link] | Neuroscience | N/A | GPT-3 | EEG Encoder | 2024.01 | ✗ |
|  | BioMistral [517] [link] | Healthcare and Medical Sciences, Molecular and Cell Biology | 7B | Mistral-7B-Instruct-v0.1 | N/A | 2024.02 | ✓ |
|  | MMed-LLaMA 3 [1041] [link] | Healthcare and Medical Sciences | 8B | LLaMA 3 | N/A | 2024.02 | ✓ |
|  | ProLLaMA [1042] [link] | Proteomics | 7B | LLaMA-2 | N/A | 2024.02 | ✓ |
|  | ProtLLM [1043] [link] | Proteomics | 7B | LLaMA-7B | ProtST (protein) | 2024.03 | ✓ |
|  | BrainGPT [552] [link] | Neuroscience | 7B | Mistral-7B | N/A | 2024.03 | ✓ |
|  | Apallo [523] [link] | Healthcare and Medical Sciences | 0.5B /1.8B /2B /6B /7B | Qwen | N/A | 2024.03 | ✓ |
|  | Med-Gemini [1044] [link] | Healthcare and Medical Sciences | N/A | Gemini 1.5 Pro | Custom encoders (multimodal) | 2024.04 | ✗ |
|  | UMBRAE [555] [link] | Neuroscience | 7B | Vicuna-7B | CLIP-ViT/L-14 (vision), Encoder (fMRI) | 2024.04 | ✓ |
|  | SeedLLM [546] [link] | Agronomy | 7B | Qwen2.5 | N/A | 2024.04 | ✗ |
|  | Alphafold3 [1045] [link] | Molecular and Cell Biology, Proteomics, Pharmacy, Neuroscience | N/A | N/A | Input Feature Embedder | 2024.05 | ✗ |
|  | DrugLLM [6] [link] | Pharmacy | 7B | LLaMA 7B | N/A | 2024.05 | ✗ |
|  | LLaVA-Med [536] [link] | Healthcare and Medical Sciences | N/A | Vicuna-7B | Clip ViT-L/14 | 2024.05 | ✓ |
|  | CareGPT [1046] [link] | Healthcare and Medical Sciences | 7B | LLaMA-2 | N/A | 2024.05 | ✓ |
|  | ProtT3 [1047] [link] | Proteomics | N/A | Galactica 1.3B | ESM-2 (protein) | 2024.05 | ✓ |
|  | MolecularGPT [511] [link] | Molecular and Cell Biology | N/A | LLaMA | N/A | 2024.06 | ✓ |
|  | HuatuoGPT-Vision [540] [link] | Healthcare and Medical Sciences | 7B /34B | Qwen2-7B | Qwen Image Encoder (vision) | 2024.06 | ✓ |
|  | NeuroLM [554] [link] | Neuroscience | 254M/500M/1.7B | GPT-2 | Encoder (EEG) | 2024.08 | ✓ |
|  | RNAGPT [640] [link] | Molecular and Cell Biology, Multi-omics | 8B | LLaMA-3 | RNA-FM sequence encoder (RNA) | 2024.10 | ✗ |
|  | AgroGPT [551] [link] | Agronomy | 3B /7B | LLaVA-1.5, Mipha | CLIP-ViT-L/14 (vision), SigLIP | 2024.10 | ✓ |
|  | LLaMA-Gene [40] [link] | Molecular and Cell Biology, Proteomics | 7B | LLaMA-7B | N/A | 2024.11 | ✓ |
|  | GMAI-VL [541] [link] | Healthcare and Medical Sciences | 7B | InternLM | Image Encoder (vision) | 2024.11 | ✓ |
|  | HuatuoGPT-o1 [543] [link] | Healthcare and Medical Sciences | 7B /8B /70B /72B | LLaMA-3.1, Qwen2.5 | N/A | 2024.12 | ✓ |
|  | Evolla [509] [link] | Proteomics | 10B /80B | LLaMA-3 8B | Saprot (protein) | 2025.01 | ✓ |
|  | UniMind [559] | Neuroscience | 7B | InternLM2.5 | Encoder (EEG) | 2025.01 | ✗ |
|  | NatureLM [43] [link] | Pharmacy, Molecular and Cell Biology, Proteomics, Material | 46.7B | Mixtral 8x7B | N/A | 2025.02 | ✗ |
|  | MindLLM [558] [link] | Neuroscience, Healthcare and Medical Sciences | 7B | Vicuna-7B | Encoder (fMRI) | 2025.02 | ✓ |
|  | MedVLM-R1 [1048] [link] | Healthcare and Medical Sciences | 2B | Qwen2-VL | Qwen Image Encoder (vision) | 2025.02 | ✓ |
|  | AlphaGenome [1049] [link] | Molecular and Cell Biology, Multi-omics | N/A | N/A | N/A | 2025.05 | ✓ |
|  | ChatNT [510] [link] | Molecular and Cell Biology, Proteomics, Multi-omics | 7B | Vicuna-7B | Nucleotide Transformer v2 (DNA) | 2025.06 | ✓ |
|  | Lingshu [1050] [link] | Healthcare and Medical Sciences | 7B /32B | Qwen | N/A | 2025.06 | ✓ |
|  | PodGPT [1051] [link] | Healthcare and Medical Sciences | N/A | Gemma, Mixtral, LLaMA | N/A | 2025.07 | ✓ |
|  | MedGemma [542] [link] | Healthcare and Medical Sciences | 4B /27B | Gemma 3 | SigLip Image Encoder (vision) | 2025.07 | ✓ |
| Astronomy | AstroLLaMA-2-7B [561] [link] | Astronomy | 7B | Llama-2 LLM | N/A | 2023.09 | ✓ |
|  | AstroLLaMA-3-8B [724] [link] | Astronomy | 8B | LLaMA-2-7B LLM | N/A | 2024.09 | ✓ |
|  | AstroLLaMA-2-70B [724] [link] | Astronomy | 70B | LLaMA-2-7B LLM | N/A | 2024.09 | ✓ |
|  | AstroSage-LLaMA-3.1-8B [563] [link] | Astronomy | 8B | Llama-3.1-8B LLM | N/A | 2025.04 | ✓ |
|  | AstroLLaVa-7B [562] [link] | Astronomy | 7B | LLaVA 1.5 LLM | CLIP-ViT/L-14 (vision) | 2025.04 | ✓ |
|  | AstroSage-LLaMA-3.1-70B [566] [link] | Astronomy | 70B | Llama-3.1-70B LLM | N/A | 2025.05 | ✓ |
| Earth Science | OceanGPT [569] [link] | Hydrosphere, Biosphere, Lithosphere, Remote Sens- ing | 7B | LLama, Qwen | N/A | 2023.03 | ✓ |
|  | K2 [567] [link] | Lithosphere, Remote Sensing | 7B | LLama | N/A | 2023.08 | ✓ |
|  | GeoChat [588] [link] | Remote Sensing, Lithosphere | 7B | Vicuna-v1.5 | N/A | 2023.11 | ✓ |
|  | SkyEyeGPT [963] [link] | Remote Sensing | 7B | N/A | N/A | 2024.01 | ✓ |
|  | TeoChat [578] [link] | Remote Sensing, Lithosphere | 7B | Vdieo-LLaVA | N/A | 2024.10 | ✓ |
|  | EarthMarker [571] [link] | Remote Sensing | 13B | LLaMA-2 | N/A | 2024.11 | ✓ |
|  | EarthDial [574] [link] | Remote Sensing | 4B | Phi-3-mini | N/A | 2024.12 | ✓ |
|  | GeoPixel [572] [link] | Remote Sensing, Lithosphere | 7B | IXC-2.5 | N/A | 2025.01 | ✓ |
|  | EagleVision [570] [link] | Remote Sensing | 1B/2B/4B/7B | Qwen2-VL-72B, GPT-4o | N/A | 2025.03 | ✓ |
|  | ClimateChat [568] [link] | Lithosphere, Climate | 7B | jiuZhou | N/A | 2025.03 | ✓ |
|  | GeoGPT [1052] [link] | Lithosphere, Remote Sensing | 70B | Llama3.1-70B, Qwen2.5-72B | N/A | 2025.04 | ✓ |
|  | GeoLLaVA-8K [573] [link] | Remote Sensing, Lithosphere | 7B | LongVA | N/A | 2025.05 | ✓ |
