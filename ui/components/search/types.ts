export enum DocumentType {
  "CONFLUENCE" = "CONFLUENCE",
}

export type ConfluenceReference = {
  chunk_group: string;
  chunk_id: string;
  domain: string;
  end_index: number;
  page_path: string;
  page_title: string;
  section: string;
  space_key: string;
  space_name: string;
  start_index: number;
};

export type PassageMetadata = {
  indexed_at: string;
  created_at: string;
  last_update: string;
  creator: string;
  link: string;
  document_link: string;
  reference: {
    confluence?: ConfluenceReference;
    text_hash: string;
  };
  filetype: DocumentType;
  connection_id: string;
  indexor: string;
};

export type Passage = {
  metadata: PassageMetadata;
  score: number;
  passage_id: number;
  text: string;
};

export type JsonResponse = {
  answer: string;
  references: Passage[];
};

export type Document = {
  passages: {
    sectionLink: string;
    passagesWithSameLink: Passage[];
    score: number;
  }[];
  document_link: string;
  score: number;
};
