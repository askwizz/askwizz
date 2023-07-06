import { Source } from "../new-connection/types";

type ConnectionStatus = "ACTIVE" | "INDEXING";

export type Connection = {
  created_at: string;
  indexed_at: string;
  domain: string;
  id_: string;
  name: string;
  status: ConnectionStatus;
  source: Source;
  documents_count: number;
  passages_count: number;
};
