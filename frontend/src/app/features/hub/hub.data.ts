export interface HubPartner {
  id: string;
  name: string;
  logoUrl: string;
  description: string;
  area: string;
  website: string;
  /** i18n key for the external link CTA; defaults to hub.visitSite. */
  linkLabelKey?: 'hub.visitSite' | 'hub.visitInstagram' | 'hub.visitPlantManager';
}

export interface HubClientMediCanopyInvolvement {
  /** Role or service line, e.g. Gerente de Operações. */
  role: string;
  /** How Medi Canopy contributed to this client engagement. */
  description: string;
}

export interface HubClient {
  id: string;
  name: string;
  logoUrl: string;
  description: string;
  /** Optional segment, e.g. tecnologia, indústria, pesquisa, saúde. */
  area?: string;
  website: string;
  /** i18n key for the external link CTA; defaults to hub.visitSite. */
  linkLabelKey?: 'hub.visitSite' | 'hub.visit4TreesProjects';
  /** Optional block highlighting Medi Canopy's work for this client. */
  mediCanopyInvolvement?: HubClientMediCanopyInvolvement;
}

/**
 * Strategic partners in the Medi Canopy ecosystem.
 * Add new entries here as partnerships are formalized.
 *
 * Example:
 * {
 *   id: 'acme-tech',
 *   name: 'Acme Tech',
 *   logoUrl: '/assets/partners/acme-tech.svg',
 *   description: 'Breve descrição da parceria.',
 *   area: 'Tecnologia',
 *   website: 'https://acme.example.com',
 * }
 */
export const HUB_PARTNERS: HubPartner[] = [
  {
    id: 'green-growth',
    name: 'Green Growth',
    logoUrl: '/assets/partners/green-growth.png',
    description:
      'Consultoria jurídica e regulatória especializada em cannabis e cânhamo, oferecendo estruturação e inteligência regulatória para empresas do agro e da indústria. Atua na construção de operações com segurança jurídica, conformidade e visão de longo prazo.',
    area: 'Jurídico e Regulatório',
    website: 'https://greengrowth.group/',
  },
  {
    id: 'om-associacao',
    name: 'OM – Associação Multidisciplinar em Práticas Integrativas',
    logoUrl: '/assets/partners/om-associacao.png',
    description: 'Cuidado especializado Humano e Animal. Informação e acesso ao tratamento.',
    area: 'Práticas Integrativas',
    website: 'https://www.instagram.com/associacaoom/',
    linkLabelKey: 'hub.visitInstagram',
  },
  {
    id: 'plantmanager',
    name: 'PlantManager',
    logoUrl: '/assets/partners/plantmanager.png',
    description:
      'PlantManager é uma plataforma brasileira de gestão inteligente para a cadeia de Cannabis Medicinal e Industrial, oferecendo soluções para gestão, rastreabilidade e conformidade regulatória. A plataforma atende diferentes etapas e perfis da cadeia, incluindo cultivo, associações medicinais, genética e melhoramento, cânhamo industrial e operações de importação e distribuição.',
    area: 'Tecnologia',
    website: 'https://plantmanager.com.br/',
    linkLabelKey: 'hub.visitPlantManager',
  },
];

/**
 * Companies Medi Canopy has served or delivered projects for.
 * Add new entries here as the portfolio grows.
 *
 * Example:
 * {
 *   id: 'acme-corp',
 *   name: 'Acme Corp',
 *   logoUrl: '/assets/clients/acme-corp.svg',
 *   description: 'Breve descrição do projeto ou serviço realizado.',
 *   area: 'Tecnologia',
 *   website: 'https://acme.example.com',
 * }
 */
export const HUB_CLIENTS: HubClient[] = [
  {
    id: '4trees-cannabis-building',
    name: '4Trees Cannabis Building',
    logoUrl: '/assets/clients/4trees-cannabis-building.webp',
    description:
      'A 4Trees Cannabis Building é uma empresa canadense especializada em consultoria e suporte para operações de Cannabis, com atuação em planejamento de instalações, suporte operacional, documentação, desenvolvimento de projetos e cultivo indoor em conformidade. A empresa trabalha com soluções práticas voltadas à estruturação e operação de instalações de cultivo, do planejamento à produção.',
    area: 'Consultoria e Operações',
    website: 'https://4treesbuilding.ca/projects',
    linkLabelKey: 'hub.visit4TreesProjects',
    mediCanopyInvolvement: {
      role: 'Gerente de Operações e Desenvolvimento de Conteúdo Educacional',
      description:
        'A Medi Canopy atua junto à 4Trees Cannabis Building como Gerente de Operações e Desenvolvimento de Conteúdo Educacional, contribuindo para a estruturação e gestão de processos operacionais, organização de conhecimento técnico e desenvolvimento de materiais educacionais voltados à formação e capacitação de profissionais do setor de Cannabis.',
    },
  },
];
