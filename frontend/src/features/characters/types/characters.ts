export interface CharacterSummary {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface CharacterListParams {
  page: number;
  size: number;
  keyword: string;
}

export interface CharacterDetail {
  id: string;
  name: string;
  persona: string;
  createdAt: string;
  updatedAt: string;
}

export interface CharacterUpdatePayload {
  name: string;
  persona: string;
}
