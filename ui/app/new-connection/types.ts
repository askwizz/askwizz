export const AVAILABLE_SOURCES = ["CONFLUENCE", "JIRA"] as const;
export type Source = (typeof AVAILABLE_SOURCES)[number];

export type SourceProperty = {
  title: string;
  icon: JSX.Element;
  disabled: boolean;
};
