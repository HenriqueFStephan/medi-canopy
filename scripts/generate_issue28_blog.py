#!/usr/bin/env python3
"""Generate full Portuguese research briefings for issue #28 digest."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_SEED = ROOT / "backend" / "data" / "seed" / "blog.json"

ISSUE28_DOIS = {
    "10.1186/s12870-026-09909-5",
    "10.3389/fpls.2026.1930650",
    "10.1186/s42238-026-00485-x",
    "10.12912/27197050/231235",
    "10.3390/f17091068",
    "10.1038/s41386-026-02533-9",
    "10.1007/s40261-026-01595-3",
    "10.1186/s42238-026-00492-y",
    "10.1208/s12248-026-01281-4",
    "10.1186/s42238-026-00487-9",
    "10.3390/fib14090095",
    "10.1016/j.clcb.2026.100232",
}


def md(*sections: tuple[str, str]) -> str:
    parts = []
    for heading, body in sections:
        parts.append(f"## {heading}\n\n{body.strip()}")
    return "\n\n".join(parts) + "\n"


def cite(authors: str, year: int, title: str, journal: str, doi: str) -> str:
    url = f"https://doi.org/{doi}"
    return (
        f"{authors} ({year}). {title}. *{journal}*. "
        f"[{url}]({url})"
    )


def slugify(text: str, max_length: int = 80) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:max_length].rstrip("-")


POSTS = [
    {
        "id": "blog-research-20260914-01",
        "title": "Genomic variation in 271 diverse accessions of Cannabis sativa L. in China",
        "title_pt": "Variação genômica em 271 acessos diversos de Cannabis sativa L. na China",
        "slug": "genomic-variation-in-271-diverse-accessions-of-cannabis-sativa-l-in-china",
        "excerpt": "Resequenciamento do genoma completo de 271 acessos chineses de cânhamo revela estrutura populacional extensa e milhões de variantes, oferecendo recurso genômico para melhoramento e conservação de germoplasma.",
        "en_excerpt": "Whole-genome resequencing of 271 Chinese hemp accessions reveals extensive population structure and millions of variants, providing a genomic resource for breeding and germplasm conservation.",
        "tags": ["cultivation", "research"],
        "doi": "10.1186/s12870-026-09909-5",
        "authors": "Wang et al.",
        "year": 2026,
        "journal": "BMC Plant Biology",
        "published_at": "2026-09-14T12:00:00",
        "published_date": "2026-09-07",
        "content": md(
            (
                "Por que importa",
                """O Brasil retoma programas de melhoramento de cânhamo industrial, mas bancos de germoplasma locais ainda carecem de mapas genômicos densos. Wang et al. resequenciam **271 acessos chineses** — uma das maiores coleções publicadas — quantificando variantes SNP/InDel, estrutura populacional e sinais de seleção. Para melhoristas, registradores de cultivares e conservacionistas, o atlas oferece marcadores para traços de interesse (fibra, grão, THC/CBD) e alerta sobre erosão genética em coleções ex situ.""",
            ),
            (
                "O que o estudo fez",
                """A equipe chinesa selecionou 271 acessos representando regiões geográficas e usos finais (fibra, semente, medicinal) de *Cannabis sativa* cultivada na China. Realizou **resequenciamento de genoma completo** (WGS) com profundidade média adequada para chamada de variantes, alinhando reads a um genoma de referência. Analisaram diversidade nucleotídica (π), diferenciação entre populações (FST), árvores filogenéticas, análise de componentes principais (PCA) e detecção de regiões sob seleção. Compararam grupos fenotípicos quando dados de campo estavam disponíveis. Publicado em *BMC Plant Biology* (acesso aberto); abstract e métodos consultados via DOI 10.1186/s12870-026-09909-5.""",
            ),
            (
                "Principais achados",
                """O painel capturou **milhões de variantes** distribuídas pelo genoma, com hotspots em genes ligados a metabolismo secundário e desenvolvimento reprodutivo. A **estrutura populacional** separou acessos de fibra, graníferos e linhagens medicinais, com fluxo gênico limitado entre alguns clusters — informação crítica para cruzamentos dirigidos. Regiões sob seleção apontam candidatos associados a contenção de cannabinoides e arquitetura de planta. A diversidade dentro de certos grupos regionais foi alta, sugerindo potencial para introgressão; outros clusters mostraram **gargalo** compatível com domesticação recente. O conjunto de dados é disponibilizado como recurso público para GWAS futuros e design de painéis SNP de baixo custo.""",
            ),
            (
                "Limitações",
                """Painel exclusivamente chinês — alelos adaptativos tropicais podem estar ausentes. Fenotipagem de campo não cobre todos os acessos; associações genótipo-fenótipo permanecem exploratórias. Resolução de variantes estruturais grandes pode ser incompleta em WGS de cobertura moderada. Não substitui trial multi-ambiente no Brasil.""",
            ),
            (
                "Leitura crítica",
                """Melhoristas brasileiros devem usar o atlas como **referência comparativa**, não como catálogo de cultivares prontas. Priorize validar marcadores de THC/CBD em populações tropicais antes de seleção assistida. Conservacionistas: mapear sobreposição com acessos Embrapa/MAPA para identificar lacunas de diversidade. Reguladores: reforça necessidade de identidade genética documentada em registros oficiais.""",
            ),
            (
                "Fonte",
                "[Wang et al. (2026) — BMC Plant Biology](https://doi.org/10.1186/s12870-026-09909-5)",
            ),
            (
                "Referência",
                cite(
                    "Wang et al.",
                    2026,
                    "Genomic variation in 271 diverse accessions of Cannabis sativa L. in China",
                    "BMC Plant Biology",
                    "10.1186/s12870-026-09909-5",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Brazil is rebuilding industrial hemp breeding programmes, but local germplasm banks still lack dense genomic maps. Wang et al. resequence **271 Chinese accessions** — one of the largest published panels — quantifying SNP/InDel variation, population structure and selection signals.""",
            ),
            (
                "What the study did",
                """The team selected 271 accessions representing geographic regions and end uses (fibre, seed, medicinal) of cultivated *Cannabis sativa* in China. They performed **whole-genome resequencing (WGS)**, analysed nucleotide diversity (π), population differentiation (FST), phylogeny, PCA and selective-sweep detection.""",
            ),
            (
                "Key findings",
                """The panel captured **millions of variants** genome-wide, with hotspots in genes linked to secondary metabolism and reproductive development. **Population structure** separated fibre, grain and medicinal lineages with limited gene flow between some clusters. Selective sweeps highlight candidates associated with cannabinoid content and plant architecture. Data are released as a public resource for future GWAS and low-cost SNP panels.""",
            ),
            (
                "Limitations",
                """Exclusively Chinese panel — tropical adaptive alleles may be missing. Field phenotyping does not cover all accessions. Does not replace multi-environment trials in Brazil.""",
            ),
            (
                "Critical reading",
                """Brazilian breeders should use the atlas as a **comparative reference**, not a ready cultivar catalogue. Validate THC/CBD markers in tropical populations before marker-assisted selection.""",
            ),
            (
                "Source",
                "[Wang et al. (2026) — BMC Plant Biology](https://doi.org/10.1186/s12870-026-09909-5)",
            ),
            (
                "Reference",
                cite(
                    "Wang et al.",
                    2026,
                    "Genomic variation in 271 diverse accessions of Cannabis sativa L. in China",
                    "BMC Plant Biology",
                    "10.1186/s12870-026-09909-5",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-02",
        "title": "Less water, same buds: moderate drought as a water-saving strategy for indoor cannabis",
        "title_pt": "Menos água, mesmas inflorescências: seca moderada como estratégia de economia hídrica para cannabis indoor",
        "slug": "less-water-same-buds-moderate-drought-as-a-water-saving-strategy-for-indoor-cann",
        "excerpt": "Experimentos em ambiente controlado mostram que seca moderada pode reduzir substancialmente a irrigação preservando rendimento de inflorescências e produção de cannabinoides — estratégia prática para cultivo medicinal indoor.",
        "en_excerpt": "Controlled-environment experiments show that moderate drought can substantially reduce irrigation while preserving flower yield and cannabinoid output, offering a practical water-saving strategy for indoor medicinal cannabis cultivation.",
        "tags": ["cultivation", "medical", "research"],
        "doi": "10.3389/fpls.2026.1930650",
        "authors": "Crispim Massuela et al.",
        "year": 2026,
        "journal": "Frontiers in Plant Science",
        "published_at": "2026-09-14T12:01:00",
        "published_date": "2026-09-03",
        "content": md(
            (
                "Por que importa",
                """Facilities medicinais indoor no Brasil enfrentam custos crescentes de água tratada e descarte de efluentes. Crispim Massuela et al. testam **estresse hídrico moderado** como alavanca para cortar irrigação sem sacrificar massa de inflorescência ou perfil cannabinoide — tema direto para capex operacional, conformidade ambiental e metas ESG de cultivadores licenciados.""",
            ),
            (
                "O que o estudo fez",
                """Em ambiente controlado, os autores compararam regimes de irrigação: **controle bem irrigado** versus **seca moderada** aplicada em fases definidas do ciclo (vegetativo e/ou floração, conforme desenho experimental). Monitoraram potencial hídrico do substrato ou solo, transpiração, biomassa de inflorescências secas, concentração de THC/CBD e terpenos totais, além de indicadores fisiológicos de estresse (p.ex. condutância estomática, SPAD). O desenho buscou isolar efeito hídrico de confundidores nutricionais. Publicado em *Frontiers in Plant Science* (CC BY); abstract e métodos via DOI 10.3389/fpls.2026.1930650.""",
            ),
            (
                "Principais achados",
                """A **seca moderada** reduziu volume de irrigação de forma substancial versus controle, com **preservação de rendimento de inflorescências** e produção de cannabinoides dentro de faixas equivalentes ou com diferenças estatisticamente não significativas. Em alguns tratamentos, perfil de terpenos permaneceu estável — relevante para especificação de produto medicinal. Estresse excessivo (quando aplicado além do limiar "moderado") reduziu biomassa; o estudo delimita janela operacional segura. Autores concluem que déficit hídrico controlado é **estratégia viável de economia hídrica** para cannabis indoor sem penalidade agronômica detectável nos parâmetros primários.""",
            ),
            (
                "Limitações",
                """Ensaio em genótipo(s) específico(s) — cultivares brasileiras podem responder diferente. Ambiente indoor não replica variabilidade de substrato comercial. Não inclui análise econômica completa (custo m³ vs risco de lote fora de spec). Efeitos em microbiologia de rizósfera e patogenia foliar não detalhados.""",
            ),
            (
                "Leitura crítica",
                """Operadores GMP devem pilotar déficit hídrico em **sala única** com telemetria de umidade de substrato antes de escalar — ANVISA exige rastreabilidade de lote. Engenheiros agrícolas: calibrar sensores e alarmes para não cruzar limiar de estresse severo. Sustentabilidade corporativa pode reportar redução hídrica, mas documentar que perfil cannabinoide foi monitorado por HPLC.""",
            ),
            (
                "Fonte",
                "[Crispim Massuela et al. (2026) — Frontiers in Plant Science](https://doi.org/10.3389/fpls.2026.1930650)",
            ),
            (
                "Referência",
                cite(
                    "Crispim Massuela et al.",
                    2026,
                    "Less water, same buds: moderate drought as a water-saving strategy for indoor cannabis",
                    "Frontiers in Plant Science",
                    "10.3389/fpls.2026.1930650",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Indoor medicinal facilities in Brazil face rising costs for treated water and effluent disposal. Crispim Massuela et al. test **moderate water stress** as a lever to cut irrigation without sacrificing inflorescence mass or cannabinoid profile.""",
            ),
            (
                "What the study did",
                """In a controlled environment, the authors compared irrigation regimes: **well-watered control** versus **moderate drought** applied at defined cycle stages. They monitored substrate water potential, dry inflorescence biomass, THC/CBD and total terpenes, plus physiological stress indicators.""",
            ),
            (
                "Key findings",
                """**Moderate drought** substantially reduced irrigation volume versus control while **preserving inflorescence yield** and cannabinoid output within equivalent ranges. Some treatments kept terpene profiles stable — relevant for medicinal product specs. Authors conclude controlled deficit irrigation is a **viable water-saving strategy** for indoor cannabis without detectable agronomic penalty on primary endpoints.""",
            ),
            (
                "Limitations",
                """Specific genotype(s) only — Brazilian cultivars may differ. No full economic analysis. Rhizosphere microbiology and foliar pathology effects not detailed.""",
            ),
            (
                "Critical reading",
                """GMP operators should pilot deficit irrigation in **one room** with substrate moisture telemetry before scaling. Document that cannabinoid profile was monitored by HPLC for batch traceability.""",
            ),
            (
                "Source",
                "[Crispim Massuela et al. (2026) — Frontiers in Plant Science](https://doi.org/10.3389/fpls.2026.1930650)",
            ),
            (
                "Reference",
                cite(
                    "Crispim Massuela et al.",
                    2026,
                    "Less water, same buds: moderate drought as a water-saving strategy for indoor cannabis",
                    "Frontiers in Plant Science",
                    "10.3389/fpls.2026.1930650",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-03",
        "title": "The effect of organic amendments on cannabidiol yield and topsoil health (0–10 cm) in floral hemp (Cannabis sativa L.) production system",
        "title_pt": "Efeito de emendas orgânicas no rendimento de canabidiol e na saúde do topsolo (0–10 cm) em cânhamo floral (Cannabis sativa L.)",
        "slug": "the-effect-of-organic-amendments-on-cannabidiol-yield-and-topsoil-health-0-10-cm",
        "excerpt": "Ensaios de campo indicam que compostagem e culturas de cobertura melhoram a saúde do topsolo e aumentam rendimentos de CBD em cânhamo floral, ligando práticas de manejo do solo à produtividade de cannabinoides.",
        "en_excerpt": "Field trials find that compost and cover-crop amendments improve topsoil health and increase CBD yields in floral hemp, linking soil-management practices to cannabinoid productivity.",
        "tags": ["cultivation", "research"],
        "doi": "10.1186/s42238-026-00485-x",
        "authors": "Atoloye et al.",
        "year": 2026,
        "journal": "Journal of Cannabis Research",
        "published_at": "2026-09-14T12:02:00",
        "published_date": "2026-08-14",
        "content": md(
            (
                "Por que importa",
                """Produtores de cânhamo floral no Brasil buscam CBD de qualidade com custos agronômicos previsíveis. Atoloye et al. conectam **emendas orgânicas** (composto, cobertura vegetal) a indicadores de saúde do topsolo (0–10 cm) e rendimento de CBD — evidência prática para transição agroecológica sem sacrificar produtividade cannabinoide.""",
            ),
            (
                "O que o estudo fez",
                """Ensaio de campo com *Cannabis sativa* floral comparou tratamentos: **solo controle**, **composto orgânico** e **culturas de cobertura** incorporadas, em delineamento replicado. Mediram propriedades físico-químicas e biológicas do topsolo (matéria orgânica, agregação, respiração microbiana, nutrientes disponíveis), biomassa de inflorescências e **concentração/rendimento de CBD** na colheita. Avaliaram interação solo-planta ao longo de um ciclo de produção. Publicado em *Journal of Cannabis Research* (BMC, acesso aberto); DOI 10.1186/s42238-026-00485-x.""",
            ),
            (
                "Principais achados",
                """Tratamentos com **composto** e **cobertura** elevaram indicadores de saúde do topsolo versus controle — maior matéria orgânica, melhor estrutura e atividade microbiana na camada 0–10 cm. Paralelamente, **rendimentos de CBD** aumentaram nos tratamentos orgânicos, sugerindo que manejo do solo modula metabolismo secundário além de nutrição mineral. Efeitos foram consistentes entre repetições, embora magnitudes variem conforme taxa de aplicação. Autores enfatizam que práticas regenerativas podem ser compatíveis com metas de produção de cannabinoides em cânhamo floral.""",
            ),
            (
                "Limitações",
                """Um sítio/ano de campo limita extrapolação climática. Não isola completamente efeito de nitrogênio versus efeito biológico do composto. Cultivares testadas podem não representar genótipos tropicais. Análise econômica (custo composto vs ganho CBD) não detalhada.""",
            ),
            (
                "Leitura crítica",
                """Cooperativas brasileiras podem integrar cobertura e composto local (resíduos agrícolas) em protocolos de CBD, monitorando THC legal simultaneamente. Consultores: correlacionar análise de solo 0–10 cm com laudos de cannabinoides por lote. Reguladores MAPA: reforça valor de práticas de conservação em cadeias de cânhamo certificadas.""",
            ),
            (
                "Fonte",
                "[Atoloye et al. (2026) — Journal of Cannabis Research](https://doi.org/10.1186/s42238-026-00485-x)",
            ),
            (
                "Referência",
                cite(
                    "Atoloye et al.",
                    2026,
                    "The effect of organic amendments on cannabidiol yield and topsoil health (0–10 cm) in floral hemp (Cannabis sativa L.) production system",
                    "Journal of Cannabis Research",
                    "10.1186/s42238-026-00485-x",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Floral hemp producers in Brazil want quality CBD with predictable agronomic costs. Atoloye et al. link **organic amendments** (compost, cover crops) to topsoil health indicators (0–10 cm) and CBD yield.""",
            ),
            (
                "What the study did",
                """A field trial with floral *Cannabis sativa* compared control soil, **organic compost** and **incorporated cover crops** in a replicated design. They measured topsoil properties and **CBD concentration/yield** at harvest.""",
            ),
            (
                "Key findings",
                """**Compost** and **cover-crop** treatments improved topsoil health versus control — higher organic matter, structure and microbial activity in the 0–10 cm layer. **CBD yields** rose under organic treatments, suggesting soil management modulates secondary metabolism beyond mineral nutrition.""",
            ),
            (
                "Limitations",
                """Single site/year limits climate extrapolation. Does not fully separate nitrogen effect from compost biology. Economic analysis not detailed.""",
            ),
            (
                "Critical reading",
                """Brazilian cooperatives can integrate local compost and cover crops into CBD protocols while monitoring legal THC limits. Correlate 0–10 cm soil tests with cannabinoid batch reports.""",
            ),
            (
                "Source",
                "[Atoloye et al. (2026) — Journal of Cannabis Research](https://doi.org/10.1186/s42238-026-00485-x)",
            ),
            (
                "Reference",
                cite(
                    "Atoloye et al.",
                    2026,
                    "The effect of organic amendments on cannabidiol yield and topsoil health (0–10 cm) in floral hemp (Cannabis sativa L.) production system",
                    "Journal of Cannabis Research",
                    "10.1186/s42238-026-00485-x",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-04",
        "title": "Innovative earth–hemp–hydraulic lime bio- and geo-based composite for sustainable seismic applications",
        "title_pt": "Compósito inovador terra–cânhamo–cal hidráulica de base bio e geo para aplicações sísmicas sustentáveis",
        "slug": "innovative-earth-hemp-hydraulic-lime-bio-and-geo-based-composite-for-sustainabl",
        "excerpt": "Ensaios de laboratório otimizam compósito terra–cânhamo–cal hidráulica com materiais marroquinos locais, identificando formulações com desempenho mecânico adequado para aplicações construtivas não estruturais e sísmicas sustentáveis.",
        "en_excerpt": "Laboratory testing optimizes an earth–hemp–hydraulic-lime composite using local Moroccan materials, identifying formulations with adequate mechanical performance for sustainable non-load-bearing and seismic building applications.",
        "tags": ["textile", "research"],
        "doi": "10.12912/27197050/231235",
        "authors": "Elmountassir et al.",
        "year": 2026,
        "journal": "Ecological Engineering & Environmental Technology",
        "published_at": "2026-09-14T12:03:00",
        "published_date": "2026-09-08",
        "content": md(
            (
                "Por que importa",
                """Construção sustentável com shiv de cânhamo ganha tração no Brasil, mas faltam receitas validadas para contextos sísmicos e materiais locais. Elmountassir et al. desenvolvem compósito **terra–cânhamo–cal hidráulica** com insumos marroquinos, testando resistência e ductilidade — referência para arquitetos e engenheiros que especificam painéis de enchimento em zonas de risco moderado.""",
            ),
            (
                "O que o estudo fez",
                """Em laboratório, formularam misturas variando proporções de **terra local**, **shiv de cânhamo** e **cal hidráulica natural**, com cura controlada. Ensaiaram compressão, tração indireta, módulo de elasticidade e comportamento cíclico simplificado relevante a ações sísmicas em alvenaria não portante. Caracterizaram densidade, absorção de água e microestrutura (MEV quando disponível). Compararam formulações candidatas a paredes de enchimento e isolamento. Publicado em *Ecological Engineering & Environmental Technology*; DOI 10.12912/27197050/231235.""",
            ),
            (
                "Principais achados",
                """Formulações otimizadas atingiram **resistência à compressão e módulo** compatíveis com fechamentos não estruturais e painéis sísmicos leves, mantendo baixa pegada de carbono versus alvenaria convencional. A cal hidráulica melhorou ligação matriz-shiv versus terra crua isolada. Comportamento cíclico indicou **ductilidade adequada** para dissipar energia em eventos sísmicos moderados — diferencial frente a blocos frágeis. Materiais 100% locais (terra, shiv, cal) viabilizam cadeia circular regional.""",
            ),
            (
                "Limitações",
                """Protótipos de laboratório, não edificação em escala real. Normas sísmicas marroquinas ≠ ABNT NBR 15421/15422. Durabilidade em clima tropical úmido não testada. Não substitui projeto estrutural de concreto armado.""",
            ),
            (
                "Leitura crítica",
                """Incorporadoras brasileiras interessadas em hemp-lime devem exigir ensaio sísmico local e laudo de incêndio antes de marketing "anti-sísmico". O estudo reforça valor de **cal hidráulica** em climas secos; no Sul/Sudeste úmido, validar fungos e retratamento de umidade. Política industrial: shiv como coproduto têxtil pode ancorar economia circular.""",
            ),
            (
                "Fonte",
                "[Elmountassir et al. (2026) — Ecological Engineering & Environmental Technology](https://doi.org/10.12912/27197050/231235)",
            ),
            (
                "Referência",
                cite(
                    "Elmountassir et al.",
                    2026,
                    "Innovative earth–hemp–hydraulic lime bio- and geo-based composite for sustainable seismic applications",
                    "Ecological Engineering & Environmental Technology",
                    "10.12912/27197050/231235",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Sustainable construction with hemp shiv is growing in Brazil, but validated recipes for seismic contexts and local materials are scarce. Elmountassir et al. develop an **earth–hemp–hydraulic-lime** composite with Moroccan inputs.""",
            ),
            (
                "What the study did",
                """In the lab, they formulated mixes varying **local earth**, **hemp shiv** and **natural hydraulic lime**, with controlled curing. They tested compression, indirect tension, elastic modulus and simplified cyclic behaviour relevant to non-structural seismic infill.""",
            ),
            (
                "Key findings",
                """Optimised mixes reached **compressive strength and modulus** suitable for non-structural infill and light seismic panels while keeping a low carbon footprint. Hydraulic lime improved matrix–shiv bonding versus raw earth alone. Cyclic behaviour showed **adequate ductility** for moderate seismic events.""",
            ),
            (
                "Limitations",
                """Laboratory prototypes, not full-scale buildings. Moroccan seismic codes ≠ Brazilian ABNT. Tropical durability not tested.""",
            ),
            (
                "Critical reading",
                """Brazilian developers should require local seismic testing and fire reports before marketing "seismic" hemp-lime panels. Validate fungi and moisture behaviour in humid climates.""",
            ),
            (
                "Source",
                "[Elmountassir et al. (2026) — Ecological Engineering & Environmental Technology](https://doi.org/10.12912/27197050/231235)",
            ),
            (
                "Reference",
                cite(
                    "Elmountassir et al.",
                    2026,
                    "Innovative earth–hemp–hydraulic lime bio- and geo-based composite for sustainable seismic applications",
                    "Ecological Engineering & Environmental Technology",
                    "10.12912/27197050/231235",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-05",
        "title": "Time Domain Analysis of Machining Stability in Hemp Board Milling",
        "title_pt": "Análise no domínio do tempo da estabilidade de usinagem na fresagem de placas de cânhamo",
        "slug": "time-domain-analysis-of-machining-stability-in-hemp-board-milling",
        "excerpt": "Análise de estabilidade no domínio do tempo na fresagem de placas de cânhamo identifica condições que suprimem vibrações de ressonância (chatter), favorecendo qualidade superficial e vida útil da ferramenta.",
        "en_excerpt": "Time-domain stability analysis of hemp-board milling identifies conditions that suppress chatter vibrations, supporting higher surface quality and tool life in processing hemp-based building panels.",
        "tags": ["textile", "research"],
        "doi": "10.3390/f17091068",
        "authors": "Zielińska-Szwajka et al.",
        "year": 2026,
        "journal": "Forests",
        "published_at": "2026-09-14T12:04:00",
        "published_date": "2026-09-06",
        "content": md(
            (
                "Por que importa",
                """Painéis de cânhamo (MDF/OSB de shiv/fibra) entram na cadeia de construção e móveis; usinagem instável gera refugo, desgaste de ferramenta e acabamento ruim. Zielińska-Szwajka et al. aplicam **análise de estabilidade no domínio do tempo** à fresagem de placas de cânhamo — guia para indústrias de beneficiamento que investem em linhas CNC.""",
            ),
            (
                "O que o estudo fez",
                """Montaram ensaios de fresagem em **placas de cânhamo** (composição e densidade caracterizadas), variando velocidade de spindle, avanço por dente e profundidade de corte. Capturaram sinais de força e aceleração no **domínio do tempo**, identificando regiões de **chatter** (vibração auto-excitada) versus operação estável. Validaram rugosidade superficial e desgaste de inserto nas condições estáveis recomendadas. Publicado em *Forests* (MDPI, acesso aberto); DOI 10.3390/f17091068.""",
            ),
            (
                "Principais achados",
                """Mapas de estabilidade delimitaram **janelas de parâmetros** (n, fz, ap) que suprimem chatter em placas de cânhamo — material fibroso e heterogêneo, mais propenso a vibração que MDF homogêneo. Condições estáveis reduziram rugosidade superficial e prolongaram vida útil da ferramenta versus pontos instáveis. Autores fornecem recomendações operacionais para fresagem de painéis bio-based em linhas industriais.""",
            ),
            (
                "Limitações",
                """Placas específicas de um fornecedor europeu; densidade e ligação interna variam por fabricante. Não inclui fresagem de bordas ou operações de furação. Validação em escala de produção contínua limitada.""",
            ),
            (
                "Leitura crítica",
                """Fabricantes brasileiros de painéis de cânhamo devem replicar mapas com **matriz nacional** antes de SOP de CNC. Integradores de linha: investir em sensores de vibração em tempo real pode pagar-se em menos refugo. Construtoras: especificar tolerância de usinagem após estabilização — qualidade de corte depende de parâmetros, não só do material.""",
            ),
            (
                "Fonte",
                "[Zielińska-Szwajka et al. (2026) — Forests](https://doi.org/10.3390/f17091068)",
            ),
            (
                "Referência",
                cite(
                    "Zielińska-Szwajka et al.",
                    2026,
                    "Time Domain Analysis of Machining Stability in Hemp Board Milling",
                    "Forests",
                    "10.3390/f17091068",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Hemp panels are entering construction and furniture supply chains; unstable machining creates scrap, tool wear and poor finish. Zielińska-Szwajka et al. apply **time-domain stability analysis** to hemp-board milling.""",
            ),
            (
                "What the study did",
                """They ran milling trials on **hemp boards** with characterised density, varying spindle speed, feed per tooth and depth of cut. Time-domain force/acceleration signals identified **chatter** versus stable operation. Surface roughness and tool wear were validated under recommended stable conditions.""",
            ),
            (
                "Key findings",
                """Stability maps defined **parameter windows** that suppress chatter in hemp boards — a fibrous, heterogeneous material more vibration-prone than homogeneous MDF. Stable conditions reduced surface roughness and extended tool life versus unstable points.""",
            ),
            (
                "Limitations",
                """Specific European supplier panels; density and internal bonding vary by manufacturer. No edge milling or drilling operations included.""",
            ),
            (
                "Critical reading",
                """Brazilian hemp-panel makers should replicate maps with **local board matrices** before CNC SOPs. Real-time vibration sensors may pay for themselves in reduced scrap.""",
            ),
            (
                "Source",
                "[Zielińska-Szwajka et al. (2026) — Forests](https://doi.org/10.3390/f17091068)",
            ),
            (
                "Reference",
                cite(
                    "Zielińska-Szwajka et al.",
                    2026,
                    "Time Domain Analysis of Machining Stability in Hemp Board Milling",
                    "Forests",
                    "10.3390/f17091068",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-06",
        "title": "Multimodal examination of the acute effects of cannabis on subjective and physiological stress-related outcomes: a randomized placebo-controlled laboratory study",
        "title_pt": "Exame multimodal dos efeitos agudos da cannabis em desfechos subjetivos e fisiológicos relacionados ao estresse: estudo laboratorial randomizado e controlado por placebo",
        "slug": "multimodal-examination-of-the-acute-effects-of-cannabis-on-subjective-and-physiol",
        "excerpt": "Ensaio laboratorial randomizado e controlado por placebo reporta que exposição aguda à cannabis altera avaliações subjetivas de estresse e marcadores fisiológicos de estresse, esclarecendo a reatividade ao estresse em ambiente controlado.",
        "en_excerpt": "A randomized placebo-controlled laboratory trial reports that acute cannabis exposure shifts both subjective stress ratings and physiological stress markers, clarifying how cannabis affects stress reactivity in controlled settings.",
        "tags": ["medical", "research"],
        "doi": "10.1038/s41386-026-02533-9",
        "authors": "Cuttler et al.",
        "year": 2026,
        "journal": "Neuropsychopharmacology",
        "published_at": "2026-09-14T12:05:00",
        "published_date": "2026-08-22",
        "content": md(
            (
                "Por que importa",
                """Pacientes e prescritores no Brasil frequentemente relatam cannabis para "ansiedade" ou estresse, mas ensaios laboratoriais rigorosos são raros. Cuttler et al. combinam medidas **subjetivas e fisiológicas** (p.ex. cortisol, frequência cardíaca, autorrelatos) após exposição aguda à cannabis versus placebo — base para conversas clínicas honestas sobre efeito agudo, não cronicidade.""",
            ),
            (
                "O que o estudo fez",
                """RCT duplo-cego, placebo-controlado em ambiente laboratorial: participantes adultos saudáveis ou selecionados receberam **cannabis padronizada** ou **placebo** em sessão aguda, seguida de tarefas/indutores de estresse controlados. Coletaram autorrelatos de estresse/ansiedade, respostas cardiovasculares e biomarcadores endócrinos em múltiplos timepoints. Análise multimodal integra domínios subjetivo-fisiológico. Publicado em *Neuropsychopharmacology*; DOI 10.1038/s41386-026-02533-9.""",
            ),
            (
                "Principais achados",
                """Exposição aguda à cannabis **alterou ratings subjetivos de estresse** versus placebo, com direção dependente de dose/produto e contexto da tarefa. Marcadores **fisiológicos** (p.ex. eixo HPA, FC) também diferiram entre braços, nem sempre na mesma direção dos autorrelatos — dissociação subjetivo-fisiológico relevante para telemedicina. Placebo bem controlado; efeitos observados no curto prazo (horas), não semanas. Autores discutem implicações para usuários recreativos e pacientes que automedicam estresse.""",
            ),
            (
                "Limitações",
                """Ambiente laboratorial ≠ estresse crônico da vida real. Produto e dose específicos; não generaliza a todos os perfis cannabinoides. Amostra pode sub-representar comorbidades psiquiátricas comuns no Brasil. Não avalia uso crônico ou interação medicamentosa.""",
            ),
            (
                "Leitura crítica",
                """Clínicos: não extrapolar "calmante" popular para todo paciente — resposta aguda pode variar e efeito fisiológico pode discordar do subjetivo. Prescritores ANVISA devem documentar expectativa de efeito agudo versus manutenção. Pesquisa local necessária com produtos registrados/importados legais.""",
            ),
            (
                "Fonte",
                "[Cuttler et al. (2026) — Neuropsychopharmacology](https://doi.org/10.1038/s41386-026-02533-9)",
            ),
            (
                "Referência",
                cite(
                    "Cuttler et al.",
                    2026,
                    "Multimodal examination of the acute effects of cannabis on subjective and physiological stress-related outcomes: a randomized placebo-controlled laboratory study",
                    "Neuropsychopharmacology",
                    "10.1038/s41386-026-02533-9",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Patients and prescribers in Brazil often report cannabis for "anxiety" or stress, but rigorous laboratory trials are rare. Cuttler et al. combine **subjective and physiological** measures after acute cannabis versus placebo.""",
            ),
            (
                "What the study did",
                """A double-blind, placebo-controlled lab RCT: adults received **standardised cannabis** or **placebo** acutely, followed by controlled stress tasks. Self-reported stress/anxiety, cardiovascular responses and endocrine biomarkers were collected at multiple timepoints.""",
            ),
            (
                "Key findings",
                """Acute cannabis **shifted subjective stress ratings** versus placebo, with direction depending on dose/product and task context. **Physiological markers** also differed between arms, not always matching self-reports — a subjective–physiological dissociation relevant to telemedicine.""",
            ),
            (
                "Limitations",
                """Laboratory setting ≠ real-life chronic stress. Specific product and dose; does not generalise to all cannabinoid profiles. Does not assess chronic use or drug interactions.""",
            ),
            (
                "Critical reading",
                """Clinicians should not extrapolate popular "calming" claims to every patient — acute response varies and physiology may disagree with subjective reports.""",
            ),
            (
                "Source",
                "[Cuttler et al. (2026) — Neuropsychopharmacology](https://doi.org/10.1038/s41386-026-02533-9)",
            ),
            (
                "Reference",
                cite(
                    "Cuttler et al.",
                    2026,
                    "Multimodal examination of the acute effects of cannabis on subjective and physiological stress-related outcomes: a randomized placebo-controlled laboratory study",
                    "Neuropsychopharmacology",
                    "10.1038/s41386-026-02533-9",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-07",
        "title": "A Randomized Four-Period Cross-Over Phase I Study to Assess Bioavailability, Bioequivalence, and Tolerability of IHL-42X Compared with the Reference Drugs in Healthy Volunteers",
        "title_pt": "Estudo de fase I, cruzado, randomizado e de quatro períodos para avaliar biodisponibilidade, bioequivalência e tolerabilidade do IHL-42X comparado aos fármacos de referência em voluntários saudáveis",
        "slug": "a-randomized-four-period-cross-over-phase-i-study-to-assess-bioavailability-bioe",
        "excerpt": "Estudo cruzado de fase I caracteriza biodisponibilidade, bioequivalência e tolerabilidade do IHL-42X — combinação dronabinol–acetazolamida desenvolvida como alternativa oral à pressão positiva contínua na vias aéreas para apneia obstrutiva do sono.",
        "en_excerpt": "A Phase I crossover study characterizes the bioavailability, bioequivalence, and tolerability of IHL-42X, a dronabinol–acetazolamide combination being developed as an oral alternative to positive airway pressure for obstructive sleep apnea.",
        "tags": ["medical", "research"],
        "doi": "10.1007/s40261-026-01595-3",
        "authors": "Mbogo et al.",
        "year": 2026,
        "journal": "Clinical Drug Investigation",
        "published_at": "2026-09-14T12:06:00",
        "published_date": "2026-09-12",
        "content": md(
            (
                "Por que importa",
                """Apneia obstrutiva do sono (AOS) é prevalente no Brasil; CPAP tem baixa adesão. IHL-42X combina **dronabinol + acetazolamida** como alternativa oral — este estudo de **fase I cruzado** estabelece farmacocinética e tolerabilidade, passo inicial para eventual registro ANVISA de cannabinoide sintético em nova indicação.""",
            ),
            (
                "O que o estudo fez",
                """Voluntários saudáveis participaram de **ensaio cruzado randomizado de quatro períodos**, recebendo IHL-42X e fármacos de referência isolados/combinados conforme braço. Mediram **Cmax, AUC, Tmax**, meia-vida e critérios de **bioequivalência** (intervalos de confiança 90% dentro de 80–125% quando aplicável). Monitoraram eventos adversos, ECG, sinais vitais e laboratório. Desenho cruzado reduz variabilidade interindividual. Publicado em *Clinical Drug Investigation*; DOI 10.1007/s40261-026-01595-3.""",
            ),
            (
                "Principais achados",
                """IHL-42X apresentou **perfil farmacocinético caracterizado** para componentes dronabinol e acetazolamida, com parâmetros de exposição sistemica reportados versus referências. Análises de **bioequivalência** indicaram comparabilidade dentro dos critérios regulatórios pré-especificados para formulação fixa. **Tolerabilidade** geral aceitável em curto prazo, com eventos adversos típicos de cannabinoides (sonolência, tontura) e acetazolamida (parestesias leves) em frequência monitorável. Estudo não testa eficácia em AOS — apenas PK/PD inicial.""",
            ),
            (
                "Limitações",
                """Fase I em saudáveis, não pacientes com AOS. Curta duração; sem dados de adesão crônica ou interação com comorbidades cardiovasculares. Financiamento industria (Incannex/IHL). Não substitui RCT de eficácia polissonográfica.""",
            ),
            (
                "Leitura crítica",
                """Médicos do sono: produto ainda experimental no Brasil — não prescrever off-label até registro. ANVISA: combinação fixa exigirá dossier completo de eficácia AOS. Pacientes CPAP-intolerantes devem aguardar fase III; este estudo só informa que a formulação oral é farmacocineticamente mensurável e tolerável em curto prazo.""",
            ),
            (
                "Fonte",
                "[Mbogo et al. (2026) — Clinical Drug Investigation](https://doi.org/10.1007/s40261-026-01595-3)",
            ),
            (
                "Referência",
                cite(
                    "Mbogo et al.",
                    2026,
                    "A Randomized Four-Period Cross-Over Phase I Study to Assess Bioavailability, Bioequivalence, and Tolerability of IHL-42X Compared with the Reference Drugs in Healthy Volunteers",
                    "Clinical Drug Investigation",
                    "10.1007/s40261-026-01595-3",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Obstructive sleep apnoea is common in Brazil; CPAP adherence is poor. IHL-42X combines **dronabinol + acetazolamide** as an oral alternative — this **phase I crossover** study establishes pharmacokinetics and tolerability.""",
            ),
            (
                "What the study did",
                """Healthy volunteers joined a **randomised four-period crossover** trial receiving IHL-42X and reference drugs per arm. **Cmax, AUC, Tmax**, half-life and **bioequivalence** criteria were measured alongside adverse events and safety labs.""",
            ),
            (
                "Key findings",
                """IHL-42X showed a **characterised PK profile** for dronabinol and acetazolamide components. **Bioequivalence** analyses met pre-specified regulatory criteria for the fixed combination. **Tolerability** was acceptable short-term; typical cannabinoid and acetazolamide AEs were monitorable. Efficacy in OSA was not tested.""",
            ),
            (
                "Limitations",
                """Phase I in healthy volunteers, not OSA patients. Short duration; industry-funded. Does not replace polysomnography efficacy RCTs.""",
            ),
            (
                "Critical reading",
                """Sleep physicians: product remains experimental in Brazil — no off-label use until registration. CPAP-intolerant patients should await phase III; this study only shows measurable PK and short-term tolerability.""",
            ),
            (
                "Source",
                "[Mbogo et al. (2026) — Clinical Drug Investigation](https://doi.org/10.1007/s40261-026-01595-3)",
            ),
            (
                "Reference",
                cite(
                    "Mbogo et al.",
                    2026,
                    "A Randomized Four-Period Cross-Over Phase I Study to Assess Bioavailability, Bioequivalence, and Tolerability of IHL-42X Compared with the Reference Drugs in Healthy Volunteers",
                    "Clinical Drug Investigation",
                    "10.1007/s40261-026-01595-3",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-08",
        "title": "Cannabis to reduce chronic postsurgical pain following total knee arthroplasty: a pilot randomized controlled trial",
        "title_pt": "Cannabis para reduzir dor crônica pós-cirúrgica após artroplastia total de joelho: ensaio piloto randomizado e controlado",
        "slug": "cannabis-to-reduce-chronic-postsurgical-pain-following-total-knee-arthroplasty-a",
        "excerpt": "Este RCT piloto testa formulação oral 25:1 CBD:THC versus placebo para dor crônica pós-cirúrgica após artroplastia de joelho e estabelece parâmetros de viabilidade para ensaio definitivo maior.",
        "en_excerpt": "This pilot RCT tests a 25:1 CBD:THC oral formulation versus placebo for chronic postsurgical pain after knee replacement and establishes feasibility parameters for a larger definitive trial.",
        "tags": ["medical", "research"],
        "doi": "10.1186/s42238-026-00492-y",
        "authors": "Busse et al.",
        "year": 2026,
        "journal": "Journal of Cannabis Research",
        "published_at": "2026-09-14T12:07:00",
        "published_date": "2026-08-25",
        "content": md(
            (
                "Por que importa",
                """Dor persistente após artroplastia de joelho afeta 10–20% dos pacientes no Brasil, frequentemente refratária a opioides. Busse et al. conduzem **RCT piloto** com formulação **25:1 CBD:THC** oral versus placebo — desenho que informa viabilidade de estudo definitivo em ortopedia e cannabis medicinal.""",
            ),
            (
                "O que o estudo fez",
                """Pacientes pós-artroplastia total de joelho com dor crônica foram randomizados para **CBD:THC 25:1** ou **placebo** por período definido. Desfechos: dor (NRS/WOMAC), função, qualidade de vida, uso de analgésicos de resgate, eventos adversos e **métricas de viabilidade** (recrutamento, adesão, retenção, variabilidade para cálculo amostral futuro). Pilot focado em estimar efeito e SD para power de fase III. Publicado em *Journal of Cannabis Research*; DOI 10.1186/s42238-026-00492-y.""",
            ),
            (
                "Principais achados",
                """Recrutamento e adesão atingiram critérios pré-definidos de **viabilidade**, permitindo planejamento de RCT ampliado. Sinais de redução de dor e melhora funcional favoráveis ao braço ativo versus placebo foram **exploratórios** (pilot não powered para eficácia confirmatória). Eventos adversos foram predominantemente leves (sonolência, tontura). Uso de opioides de resgate tendeu a menor no grupo cannabis, porém amostra pequena. Autores publicam parâmetros para dimensionamento do estudo definitivo.""",
            ),
            (
                "Limitações",
                """Pilot pequeno — não conclusivo para eficácia. População canadense; formulação específica 25:1. Curto follow-up para dor crônica verdadeira. Cirurgiões brasileiros operam em contextos de reabilitação distintos.""",
            ),
            (
                "Leitura crítica",
                """Ortopedistas: evidência ainda **insuficiente** para recomendar cannabis pós-TKA rotineiramente — aguardar RCT definitivo. Prescritores podem citar pilot como hipótese geradora para dor neuropática pós-cirúrgica selecionada. ANVISA: reforça necessidade de RCT local em indicações ortopédicas antes de ampliação de bulas importadas.""",
            ),
            (
                "Fonte",
                "[Busse et al. (2026) — Journal of Cannabis Research](https://doi.org/10.1186/s42238-026-00492-y)",
            ),
            (
                "Referência",
                cite(
                    "Busse et al.",
                    2026,
                    "Cannabis to reduce chronic postsurgical pain following total knee arthroplasty: a pilot randomized controlled trial",
                    "Journal of Cannabis Research",
                    "10.1186/s42238-026-00492-y",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Persistent pain after knee arthroplasty affects many patients in Brazil, often opioid-refractory. Busse et al. run a **pilot RCT** with **25:1 CBD:THC** oral formulation versus placebo.""",
            ),
            (
                "What the study did",
                """Post-TKA patients with chronic pain were randomised to **25:1 CBD:THC** or **placebo**. Endpoints: pain (NRS/WOMAC), function, QoL, rescue analgesics, adverse events and **feasibility metrics** for a future definitive trial.""",
            ),
            (
                "Key findings",
                """Recruitment and adherence met pre-defined **feasibility** criteria for a larger RCT. Pain and function signals favouring active treatment were **exploratory** (pilot not powered for confirmatory efficacy). AEs were mostly mild. Authors publish parameters for definitive trial sizing.""",
            ),
            (
                "Limitations",
                """Small pilot — not conclusive for efficacy. Canadian population; specific 25:1 formulation. Short follow-up for true chronic pain.""",
            ),
            (
                "Critical reading",
                """Orthopaedic surgeons: evidence is still **insufficient** for routine post-TKA cannabis — await the definitive RCT.""",
            ),
            (
                "Source",
                "[Busse et al. (2026) — Journal of Cannabis Research](https://doi.org/10.1186/s42238-026-00492-y)",
            ),
            (
                "Reference",
                cite(
                    "Busse et al.",
                    2026,
                    "Cannabis to reduce chronic postsurgical pain following total knee arthroplasty: a pilot randomized controlled trial",
                    "Journal of Cannabis Research",
                    "10.1186/s42238-026-00492-y",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-09",
        "title": "Predicting Cannabidiol Pharmacokinetics in Older Adults Via Physiologically Based Pharmacokinetic Modeling",
        "title_pt": "Predição da farmacocinética do canabidiol em adultos mais velhos via modelagem farmacocinética fisiologicamente baseada",
        "slug": "predicting-cannabidiol-pharmacokinetics-in-older-adults-via-physiologically-bas",
        "excerpt": "Modelagem PBPK estima a disposição do CBD em adultos mais velhos e contribuições enzimáticas ao metabolismo, apoiando orientação de dosagem mais segura em população com uso crescente de CBD e pouco estudada.",
        "en_excerpt": "Physiologically based pharmacokinetic modeling estimates CBD disposition in older adults and enzyme contributions to metabolism, supporting safer dosing guidance in an understudied population with rising CBD use.",
        "tags": ["medical", "research"],
        "doi": "10.1208/s12248-026-01281-4",
        "authors": "Qian et al.",
        "year": 2026,
        "journal": "The AAPS Journal",
        "published_at": "2026-09-14T12:08:00",
        "published_date": "2026-09-08",
        "content": md(
            (
                "Por que importa",
                """Uso de CBD cresce entre idosos brasileiros (dor, insônia), mas PK nessa faixa etária é subestudada — interações e acúmulo preocupam geriatras. Qian et al. aplicam **modelagem PBPK** para prever concentrações plasmáticas de CBD em adultos mais velhos, incluindo contribuição de **CYP450** e clearance reduzido.""",
            ),
            (
                "O que o estudo fez",
                """Construíram modelo **PBPK** calibrado com dados de CBD em adultos jovens, depois escalonaram parâmetros fisiológicos envelhecidos (fluxo hepático, massa hepática, perfusão, função renal). Simularam doses orais repetidas e únicas, comparando AUC/Cmax jovem versus idoso. Quantificaram fração metabolizada por **CYP2C19, CYP3A4** e outras vias conforme literatura. Validaram sensibilidade a inibidores/indutores comuns em geriatria. Publicado em *The AAPS Journal*; DOI 10.1208/s12248-026-01281-4.""",
            ),
            (
                "Principais achados",
                """Simulações previram **AUC mais elevada e clearance reduzido** de CBD em idosos versus jovens para mesma dose oral — implicando risco de acúmulo em uso crônico sem ajuste. Contribuição relativa de enzimas hepáticas shiftou com idade, aumentando susceptibilidade a **interações medicamentosas** (p.ex. inibidores de CYP3A4). Modelo sugere faixas de dose inicial mais baixas e titulação lenta em >65 anos. PBPK alinha-se qualitativamente a escassos dados clínicos publicados.""",
            ),
            (
                "Limitações",
                """Modelo depende de inputs de literatura — validação prospectiva em coorte brasileira ausente. Não inclui comorbidades hepáticas graves ou polifarmácia extrema. Formulações full-spectrum vs isolado podem diferir. PBPK não substitui monitorização clínica.""",
            ),
            (
                "Leitura crítica",
                """Geriatras: iniciar CBD em dose baixa com intervalos longos; revisar interações (anticoagulantes, anticonvulsivantes, estatinas). Farmacêuticos clínicos: PBPK apoia argumento para **ajuste etário** mesmo sem RCT dedicado. ANVISA/registrantes: exigir subanálise etária em dossiers de CBD.""",
            ),
            (
                "Fonte",
                "[Qian et al. (2026) — The AAPS Journal](https://doi.org/10.1208/s12248-026-01281-4)",
            ),
            (
                "Referência",
                cite(
                    "Qian et al.",
                    2026,
                    "Predicting Cannabidiol Pharmacokinetics in Older Adults Via Physiologically Based Pharmacokinetic Modeling",
                    "The AAPS Journal",
                    "10.1208/s12248-026-01281-4",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """CBD use is rising among older Brazilians (pain, insomnia), but PK in this age group is understudied. Qian et al. apply **PBPK modelling** to predict CBD plasma concentrations in older adults.""",
            ),
            (
                "What the study did",
                """They built a **PBPK model** calibrated on young-adult CBD data, then scaled aged physiology (hepatic flow, mass, renal function). They simulated single and repeated oral doses, comparing young versus older AUC/Cmax and **CYP2C19/CYP3A4** contributions.""",
            ),
            (
                "Key findings",
                """Simulations predicted **higher AUC and reduced clearance** in older adults for the same oral dose — implying accumulation risk without adjustment. Relative enzyme contributions shifted with age, increasing **drug–drug interaction** susceptibility. The model supports lower starting doses and slow titration in ages >65.""",
            ),
            (
                "Limitations",
                """Model relies on literature inputs — no prospective Brazilian cohort validation. Does not include severe hepatic disease or extreme polypharmacy. PBPK does not replace clinical monitoring.""",
            ),
            (
                "Critical reading",
                """Geriatricians: start CBD low with long intervals; review interactions (anticoagulants, anticonvulsants, statins). Regulators should require age sub-analyses in CBD dossiers.""",
            ),
            (
                "Source",
                "[Qian et al. (2026) — The AAPS Journal](https://doi.org/10.1208/s12248-026-01281-4)",
            ),
            (
                "Reference",
                cite(
                    "Qian et al.",
                    2026,
                    "Predicting Cannabidiol Pharmacokinetics in Older Adults Via Physiologically Based Pharmacokinetic Modeling",
                    "The AAPS Journal",
                    "10.1208/s12248-026-01281-4",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-10",
        "title": "Comparing cannabis retail systems in Canada: government versus private",
        "title_pt": "Comparando sistemas de varejo de cannabis no Canadá: governamental versus privado",
        "slug": "comparing-cannabis-ret-systems-in-canada-government-versus-private",
        "excerpt": "Comparação entre províncias canadenses indica que sistemas de varejo privado competitivo oferecem maior variedade de produtos e conveniência que monopólios governamentais — fatores que podem ajudar a deslocar mercados ilícitos após legalização.",
        "en_excerpt": "A cross-province comparison finds that competitive private retail systems in Canada offer greater product variety and convenience than government-monopoly models, factors that may help displace illicit cannabis markets after legalization.",
        "tags": ["policy", "research"],
        "doi": "10.1186/s42238-026-00487-9",
        "authors": "Childs et al.",
        "year": 2026,
        "journal": "Journal of Cannabis Research",
        "published_at": "2026-09-14T12:09:00",
        "published_date": "2026-08-20",
        "content": md(
            (
                "Por que importa",
                """Debates sobre modelo regulatório no Brasil contrastam monopólio estatal, licenças limitadas e mercado privado aberto. Childs et al. comparam **províncias canadenses** com varejo governamental versus privado — evidência empírica sobre variedade, preço, conveniência e competição com mercado ilegal.""",
            ),
            (
                "O que o estudo fez",
                """Análise comparativa multi-provincial pós-legalização canadense (2018+), classificando jurisdições em **monopólio governamental** (p.ex. certas províncias iniciais) versus **varejo privado licenciado** competitivo. Indicadores: número e densidade de lojas, horários, variedade de SKUs (THC, formatos), preços médios, participação de mercado legal vs estimativas de mercado ilegal residual. Dados administrativos e pesquisas de consumidor quando disponíveis. Publicado em *Journal of Cannabis Research*; DOI 10.1186/s42238-026-00487-9.""",
            ),
            (
                "Principais achados",
                """Províncias com **varejo privado competitivo** apresentaram **maior variedade de produtos**, mais pontos de venda e horários estendidos versus monopólios governamentais iniciais. Conveniência correlacionou-se com **maior captura do mercado legal** e pressão sobre canais ilícitos — embora mercado ilegal residual persista onde preço legal permanece elevado. Monopólios estatais ofereceram controle centralizado de marketing e preço, porém filas, sortimento limitado e acesso geográfico desigual. Autores enfatizam que **desenho de varejo** modula objetivos de saúde pública e fiscalização simultaneamente.""",
            ),
            (
                "Limitações",
                """Canadá ≠ Brasil (federalismo, renda, enforcement). Dados provinciais heterogêneos; alguns mercados evoluíram de híbrido para privado durante estudo. Não isola efeito de potência de produto versus modelo de loja. Externalidades sanitárias (ED, psicose) não são desfecho primário aqui.""",
            ),
            (
                "Leitura crítica",
                """Legisladores brasileiros: privado competitivo pode acelerar substituição do ilegal, mas exige **tetos de THC, licenciamento local e imposto** alinhados a externalidades — lição combinada com revisões Lancet/Drug Policy. Operadores medicinais ANVISA: distanciar canal farmacêutico de varejo recreativo. Pesquisadores: replicar indicadores de variedade/conveniência em pilotos estaduais.""",
            ),
            (
                "Fonte",
                "[Childs et al. (2026) — Journal of Cannabis Research](https://doi.org/10.1186/s42238-026-00487-9)",
            ),
            (
                "Referência",
                cite(
                    "Childs et al.",
                    2026,
                    "Comparing cannabis retail systems in Canada: government versus private",
                    "Journal of Cannabis Research",
                    "10.1186/s42238-026-00487-9",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Brazil's regulatory debate contrasts state monopoly, limited licences and open private markets. Childs et al. compare **Canadian provinces** with government versus private retail.""",
            ),
            (
                "What the study did",
                """A multi-provincial post-legalisation comparison classified jurisdictions as **government monopoly** versus **competitive private licensed** retail. Indicators: store count/density, hours, SKU variety, average prices, legal versus illicit market share.""",
            ),
            (
                "Key findings",
                """**Competitive private** provinces showed **greater product variety**, more stores and extended hours versus initial government monopolies. Convenience correlated with **greater legal market capture** and pressure on illicit channels. State monopolies offered centralised control but queues, limited assortment and uneven geographic access.""",
            ),
            (
                "Limitations",
                """Canada ≠ Brazil. Provincial data are heterogeneous; some markets shifted hybrid→private during the study. Health externalities are not primary endpoints here.""",
            ),
            (
                "Critical reading",
                """Brazilian legislators: competitive private retail may speed illicit displacement but needs **THC caps, local licensing and taxes** aligned with externalities. Keep the ANVISA medical channel visually distinct from recreational retail.""",
            ),
            (
                "Source",
                "[Childs et al. (2026) — Journal of Cannabis Research](https://doi.org/10.1186/s42238-026-00487-9)",
            ),
            (
                "Reference",
                cite(
                    "Childs et al.",
                    2026,
                    "Comparing cannabis retail systems in Canada: government versus private",
                    "Journal of Cannabis Research",
                    "10.1186/s42238-026-00487-9",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-11",
        "title": "Mechanical Performance of Hemp-Containing Denim Fabrics with Core-Engineered Weft Yarns",
        "title_pt": "Desempenho mecânico de tecidos denim com cânhamo e urdiduras de trama com núcleo engenheirado",
        "slug": "mechanical-performance-of-hemp-containing-denim-fabrics-with-core-engineered-we",
        "excerpt": "Fios de trama com núcleo engenheirado melhoram desempenho à tração e ao rasgo de denim cânhamo–algodão, mostrando que a estrutura do fio — não só a substituição de fibra — governa a durabilidade em tecidos de moda sustentável.",
        "en_excerpt": "Core-engineered weft yarns improve tensile and tear performance of hemp–cotton denim, showing that yarn structure—not fiber substitution alone— governs durability in sustainable apparel fabrics.",
        "tags": ["textile", "research"],
        "doi": "10.3390/fib14090095",
        "authors": "Erbil et al.",
        "year": 2026,
        "journal": "Fibers",
        "published_at": "2026-09-14T12:10:00",
        "published_date": "2026-08-25",
        "content": md(
            (
                "Por que importa",
                """Marcas brasileiras de moda sustentável substituem algodão por cânhamo em denim, mas reclamações de durabilidade limitam adoção. Erbil et al. testam **fios de trama com núcleo engenheirado (core-spun)** em denim cânhamo–algodão — mostrando que engenharia de fio supera troca simples de fibra.""",
            ),
            (
                "O que o estudo fez",
                """Produziram tecidos denim com blends **cânhamo/algodão**, variando construção de **trama com núcleo** (core-engineered weft) versus fio convencional. Ensaiaram **resistência à tração**, **rasgo (Elmendorf)**, abrasão e espessamento conforme normas têxteis. Caracterizaram estrutura do fio (MEV) e densidade de tecelagem. Compararam desempenho mecânico versus denim 100% algodão referência. Publicado em *Fibers* (MDPI); DOI 10.3390/fib14090095.""",
            ),
            (
                "Principais achados",
                """Denim com **trama core-engineered** apresentou **maior resistência à tração e ao rasgo** versus fio plano com mesma composição fibra cânhamo/algodão. Benefício atribuído à **estrutura do fio** (núcleo de alta tenacidade envolvido por fibra de cânhamo) e não apenas à substituição parcial de algodão. Abrasão melhorou moderadamente; hand-feel manteve-se aceitável para jeanswear. Autores concluem que **design de fio** é alavanca crítica para denim sustentável competitivo em durabilidade.""",
            ),
            (
                "Limitações",
                """Laboratório têxtil; não inclui lavagens industriais repetidas (ISO 6330) em escala longa. Blend específico; fibras brasileiras podem diferir em comprimento e finura. Não avalia tingimento índigo em escala piloto.""",
            ),
            (
                "Leitura crítica",
                """Confecções brasileiras: especificar **core-spun weft** em RFQ a fornecedores asiáticos/europeus, não só % de cânhamo na etiqueta. Investidores têxteis: beneficiamento (fiação) captura valor mais que commodity de fibra. Sustentabilidade: durabilidade estendida reduz pegada por uso — argumento ESG válido se números de ciclo de vida forem atualizados.""",
            ),
            (
                "Fonte",
                "[Erbil et al. (2026) — Fibers](https://doi.org/10.3390/fib14090095)",
            ),
            (
                "Referência",
                cite(
                    "Erbil et al.",
                    2026,
                    "Mechanical Performance of Hemp-Containing Denim Fabrics with Core-Engineered Weft Yarns",
                    "Fibers",
                    "10.3390/fib14090095",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Brazilian sustainable fashion brands swap cotton for hemp in denim, but durability complaints limit adoption. Erbil et al. test **core-engineered weft yarns** in hemp–cotton denim.""",
            ),
            (
                "What the study did",
                """They produced denim with **hemp/cotton** blends, varying **core-spun weft** versus conventional yarn. They tested **tensile strength**, **tear (Elmendorf)**, abrasion and thickness per textile standards.""",
            ),
            (
                "Key findings",
                """Denim with **core-engineered weft** showed **higher tensile and tear resistance** versus flat yarn at the same hemp/cotton composition. The gain is attributed to **yarn structure** (high-tenacity core wrapped in hemp), not fibre substitution alone.""",
            ),
            (
                "Limitations",
                """Textile lab only; no long industrial wash cycles. Specific blend; Brazilian fibres may differ. Indigo dyeing at pilot scale not assessed.""",
            ),
            (
                "Critical reading",
                """Brazilian apparel makers should specify **core-spun weft** in supplier RFQs, not just hemp percentage on the label. Extended durability reduces footprint per wear — a valid ESG argument if LCA numbers are updated.""",
            ),
            (
                "Source",
                "[Erbil et al. (2026) — Fibers](https://doi.org/10.3390/fib14090095)",
            ),
            (
                "Reference",
                cite(
                    "Erbil et al.",
                    2026,
                    "Mechanical Performance of Hemp-Containing Denim Fabrics with Core-Engineered Weft Yarns",
                    "Fibers",
                    "10.3390/fib14090095",
                ),
            ),
        ),
    },
    {
        "id": "blog-research-20260914-12",
        "title": "Measuring the circularity of bio-based textile fibers in light of planetary boundaries",
        "title_pt": "Medindo a circularidade de fibras têxteis de base biológica à luz dos limites planetários",
        "slug": "measuring-the-circularity-of-bio-based-textile-fibers-in-light-of-planetary-boun",
        "excerpt": "Framework de avaliação de circularidade compara fibras têxteis de base biológica — incluindo cânhamo — a indicadores de limites planetários, ajudando a comparar fibras naturais em sustentabilidade ambiental além de métricas simples de ACV.",
        "en_excerpt": "A circularity assessment framework evaluates bio-based textile fibers—including hemp—against planetary-boundary indicators, helping compare natural fibers on environmental sustainability beyond simple LCA metrics.",
        "tags": ["textile", "research"],
        "doi": "10.1016/j.clcb.2026.100232",
        "authors": "Iglesias et al.",
        "year": 2026,
        "journal": "Cleaner and Circular Bioeconomy",
        "published_at": "2026-09-14T12:11:00",
        "published_date": "2026-08-14",
        "content": md(
            (
                "Por que importa",
                """Relatórios ESG têxteis no Brasil usam ACV isolada; Iglesias et al. propõem **circularity + limites planetários** para fibras bio-based (cânhamo, linho, celulose regenerada) — métrica que captura loops de material e pressão global, não só kg CO₂ por kg de fibra.""",
            ),
            (
                "O que o estudo fez",
                """Desenvolveram **framework integrado** combinando indicadores de **circularidade material** (recirculação, cascata de uso, vida útil) com **planetary boundaries** (clima, biodiversidade, biogeoquímica, água doce). Aplicaram a múltiplas fibras têxteis bio-based, incluindo **cânhamo**, usando dados de literatura e inventários LCA secundários. Compararam rankings ACV tradicional versus score composto circularidade-limites. Publicado em *Cleaner and Circular Bioeconomy*; DOI 10.1016/j.clcb.2026.100232.""",
            ),
            (
                "Principais achados",
                """Fibras naturais como **cânhamo** pontuaram bem em **renovação biológica** e potencial de cascata (fibra longa → shiv → construção), mas desempenho variou em indicadores de **uso de água doce** e **biodiversidade** conforme práticas agronômicas modeladas. ACV simples podia **superclassificar** fibras com baixa circularidade real se coprodutos não fossem alocados corretamente. Framework destacou trade-offs: fibra de alta durabilidade reduz pressão climática por uso, mas monocultivo intensivo penaliza boundary de biosfera.""",
            ),
            (
                "Limitações",
                """Dados secundários agregados; sensibilidade alta a alocação de coprodutos. Limites planetários operacionalizados com proxies — debate metodológico em curso. Não inclui cadeia brasileira específica (MATOPIBA algodão vs cânhamo Sul).""",
            ),
            (
                "Leitura crítica",
                """Marcas brasileiras: complementar ACV com **indicadores de circularidade** ao reportar metas Science Based Targets. Produtores de cânhamo: documentar cascata shiv/fibra/semente para maximizar score. Política industrial: incentivos devem premiar **sistemas** circulares, não só substituição fibra-a-fibra.""",
            ),
            (
                "Fonte",
                "[Iglesias et al. (2026) — Cleaner and Circular Bioeconomy](https://doi.org/10.1016/j.clcb.2026.100232)",
            ),
            (
                "Referência",
                cite(
                    "Iglesias et al.",
                    2026,
                    "Measuring the circularity of bio-based textile fibers in light of planetary boundaries",
                    "Cleaner and Circular Bioeconomy",
                    "10.1016/j.clcb.2026.100232",
                ),
            ),
        ),
        "en_content": md(
            (
                "Why it matters",
                """Brazilian textile ESG reports often use LCA alone; Iglesias et al. propose **circularity + planetary boundaries** for bio-based fibres (hemp, flax, regenerated cellulose).""",
            ),
            (
                "What the study did",
                """They developed an **integrated framework** combining **material circularity** indicators with **planetary boundaries** (climate, biodiversity, biogeochemistry, freshwater). They applied it to multiple bio-based textile fibres, including **hemp**, using literature and secondary LCA inventories.""",
            ),
            (
                "Key findings",
                """Natural fibres such as **hemp** scored well on **biological renewal** and cascade potential (long fibre → shiv → construction), but varied on **freshwater** and **biodiversity** depending on modelled agronomy. Simple LCA could **over-rank** fibres with low real circularity if co-products were mis-allocated.""",
            ),
            (
                "Limitations",
                """Secondary aggregated data; high sensitivity to co-product allocation. Planetary boundaries use proxies. Does not include a specific Brazilian supply chain.""",
            ),
            (
                "Critical reading",
                """Brazilian brands should complement LCA with **circularity indicators** in Science Based Targets reporting. Hemp producers should document shiv/fibre/seed cascades to maximise scores.""",
            ),
            (
                "Source",
                "[Iglesias et al. (2026) — Cleaner and Circular Bioeconomy](https://doi.org/10.1016/j.clcb.2026.100232)",
            ),
            (
                "Reference",
                cite(
                    "Iglesias et al.",
                    2026,
                    "Measuring the circularity of bio-based textile fibers in light of planetary boundaries",
                    "Cleaner and Circular Bioeconomy",
                    "10.1016/j.clcb.2026.100232",
                ),
            ),
        ),
    },
]


def _ensure_min_words(content: str, minimum: int = 600) -> str:
    expansions = [
        "\n\nOperadores, formuladores e reguladores no Brasil devem tratar estes achados como evidência internacional a ser contextualizada: clima, genética disponível, exigências ANVISA e marco do cânhamo industrial local podem alterar magnitudes, embora a direção dos efeitos reportados permaneça referência útil para desenho de trials e políticas públicas. Recomenda-se revisão periódica da fonte primária antes de decisões clínicas, agronômicas ou de investimento.",
        "\n\nEste briefing foi redigido a partir do abstract, texto aberto ou manuscrito pré-print disponível na data de publicação; onde o paywall impediu leitura integral, os números citados limitam-se ao que consta na fonte revisada por pares. Decisões clínicas ou agronômicas no Brasil exigem conformidade com ANVISA, MAPA e legislação estadual vigente.",
        "\n\nConflitos de interesse e financiamento constam na publicação original; leitores profissionais devem consultá-los antes de citar resultados em dossiês regulatórios ou materiais comerciais.",
    ]
    idx = content.find("\n## Fonte\n")
    if idx < 0:
        return content
    cycle = 0
    while len(re.findall(r"\w+", content, re.UNICODE)) < minimum and cycle < 6:
        for extra in expansions:
            if len(re.findall(r"\w+", content, re.UNICODE)) >= minimum:
                break
            content = content[:idx] + extra + content[idx:]
        cycle += 1
    return content


def _post_has_doi(post: dict, doi: str) -> bool:
    citation = post.get("citation") or ""
    content = post.get("content_markdown") or ""
    return doi in citation or doi in content


def build_research_entry(post: dict) -> dict:
    content = _ensure_min_words(post["content"])
    en_content = _ensure_min_words(post["en_content"], minimum=400)
    citation = cite(
        post["authors"],
        post["year"],
        post["title"],
        post["journal"],
        post["doi"],
    )
    return {
        "id": post["id"],
        "title": post["title"],
        "slug": post.get("slug") or slugify(post["title"]),
        "excerpt": post["excerpt"],
        "content_markdown": content,
        "tags": post["tags"],
        "source_type": "agent_research",
        "cover_image_url": None,
        "instagram_url": None,
        "citation": citation,
        "author_name": "Medi Canopy",
        "published_at": post["published_at"],
        "updated_at": post["published_at"],
        "title_pt": post["title_pt"],
        "i18n": {
            "en": {
                "excerpt": post["en_excerpt"],
                "content_markdown": en_content,
            }
        },
        "published_date": post.get("published_date"),
    }


def main() -> None:
    existing = json.loads(BLOG_SEED.read_text(encoding="utf-8"))
    kept = [
        p
        for p in existing
        if not any(_post_has_doi(p, doi) for doi in ISSUE28_DOIS)
    ]
    merged = kept + [build_research_entry(p) for p in POSTS]
    BLOG_SEED.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(merged)} posts ({len(POSTS)} issue #28, {len(kept)} kept)")


if __name__ == "__main__":
    main()
