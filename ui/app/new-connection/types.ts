export const AVAILABLE_SOURCES = ["CONFLUENCE", "JIRA"] as const;
export type Source = (typeof AVAILABLE_SOURCES)[number];
