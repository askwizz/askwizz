import { Icons } from "@/components/icons";

import { Source, SourceProperty } from "./types";

export const SourceProperties: Record<Source, SourceProperty> = {
  CONFLUENCE: {
    title: "Confluence",
    icon: <Icons.confluence width={20} />,
    disabled: false,
  },
  JIRA: {
    title: "Jira (coming soon...)",
    icon: <Icons.confluence width={20} />,
    disabled: true,
  },
};
