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
