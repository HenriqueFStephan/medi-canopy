export type ProjectCategory = 'medicinal' | 'recreativo' | 'fibra' | 'agricultura';

export interface CannabisProjectTheme {
  bg: string;
  surface: string;
  accent: string;
  text: string;
  muted: string;
  border: string;
  tagBg: string;
  tagText: string;
  fontHeading: string;
}

export interface CannabisProject {
  id: string;
  name: string;
  shortName: string;
  organization: string;
  location: string;
  website: string;
  description: string;
  highlights: string[];
  categories: ProjectCategory[];
  theme: CannabisProjectTheme;
}

const CATEGORY_LABELS: Record<ProjectCategory, string> = {
  medicinal: 'Medicinal',
  recreativo: 'Recreativo',
  fibra: 'Fibra',
  agricultura: 'Agricultura',
};

export function categoryLabel(category: ProjectCategory): string {
  return CATEGORY_LABELS[category];
}

/** Curated Brazilian public cannabis initiatives (issue #12). */
export const CANNABIS_PROJECTS: CannabisProject[] = [
  {
    id: 'abrace-esperanca',
    name: 'ABRACE Esperança',
    shortName: 'ABRACE',
    organization: 'Associação Brasileira de Apoio Cannabis Esperança',
    location: 'João Pessoa, PB',
    website: 'https://abraceesperanca.org.br/',
    description:
      'Primeira associação de pacientes autorizada judicialmente a cultivar cannabis medicinal no Brasil. ' +
      'Oferece óleos e pomadas a associados, acolhimento humanizado, laboratório próprio e apoio jurídico.',
    highlights: [
      'Cultivo legalizado desde 2017 com autorização judicial',
      'Museu da Cannabis e programa de isenção social',
      'Mais de 50 mil associados em todo o país',
    ],
    categories: ['medicinal'],
    theme: {
      bg: 'linear-gradient(135deg, #0f5132 0%, #198754 55%, #75b798 100%)',
      surface: 'rgba(255, 255, 255, 0.97)',
      accent: '#ffc107',
      text: '#1a3328',
      muted: '#4a6358',
      border: 'rgba(25, 135, 84, 0.25)',
      tagBg: 'rgba(25, 135, 84, 0.12)',
      tagText: '#146c43',
      fontHeading: "'Source Sans 3', system-ui, sans-serif",
    },
  },
  {
    id: 'cedican-ufsc',
    name: 'CEDICAN',
    shortName: 'CEDICAN',
    organization: 'Centro de Desenvolvimento e Inovação Canábica — UFSC',
    location: 'Curitibanos, SC',
    website: 'https://cedican.paginas.ufsc.br/',
    description:
      'Centro de referência da UFSC com autorização judicial para cultivo agroecológico de cannabis. ' +
      'Fomenta pesquisa veterinária, linhagens medicinais e a cadeia industrial do cânhamo no Brasil.',
    highlights: [
      'Única universidade brasileira com licença judicial para pesquisa veterinária canabinoide',
      'Foco em cânhamo têxtil, celulose e biocombustíveis de baixo carbono',
      'Polo de inovação no interior catarinense com parceiros industriais',
    ],
    categories: ['medicinal', 'fibra', 'agricultura'],
    theme: {
      bg: 'linear-gradient(135deg, #002244 0%, #004080 50%, #0066cc 100%)',
      surface: 'rgba(255, 255, 255, 0.98)',
      accent: '#ffd700',
      text: '#0a2540',
      muted: '#4a6078',
      border: 'rgba(0, 64, 128, 0.22)',
      tagBg: 'rgba(0, 64, 128, 0.1)',
      tagText: '#003d7a',
      fontHeading: "'DM Serif Display', Georgia, serif",
    },
  },
];
