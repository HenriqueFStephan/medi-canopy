export interface HubPartner {
  id: string;
  name: string;
  logoUrl: string;
  description: string;
  area: string;
  website: string;
  /** i18n key for the external link CTA; defaults to hub.visitSite */
  linkLabelKey?: 'hub.visitSite' | 'hub.visitInstagram';
}

export interface HubClient {
  id: string;
  name: string;
  logoUrl: string;
  description: string;
  /** Optional segment, e.g. tecnologia, indústria, pesquisa, saúde. */
  area?: string;
  website: string;
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
    id: 'associacao-om',
    name: 'OM – Associação Multidisciplinar em Práticas Integrativas',
    logoUrl: '/assets/partners/associacao-om.jpg',
    description: 'Cuidado especializado Humano e Animal. Informação e acesso ao tratamento.',
    area: 'Práticas Integrativas',
    website: 'https://www.instagram.com/associacaoom/',
    linkLabelKey: 'hub.visitInstagram',
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
export const HUB_CLIENTS: HubClient[] = [];
