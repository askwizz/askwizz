import { useMemo } from "react";
import { groupBy, sortBy } from "lodash";

import { Passage } from "../types";

export default function useGroupResponseByDocument(
  references: Passage[] | undefined,
) {
  const responseGroupedByDocument = useMemo(() => {
    return sortBy(
      Object.entries(
        groupBy(references, (reference) => reference.metadata.document_link),
      ).map(([document_link, references]) => {
        const sectionPassages = sortBy(
          Object.entries(
            groupBy(references, (reference) => reference.metadata.link),
          ).map(([sectionLink, passagesWithSameLink]) => ({
            sectionLink,
            passagesWithSameLink: sortBy(
              passagesWithSameLink,
              (passage) => -passage.score,
            ),
            score: Math.min(...passagesWithSameLink.map((p) => -p.score)),
          })),
          (section) => section.score,
        );
        return {
          passages: sectionPassages,
          document_link,
          score: Math.min(...sectionPassages.map((p) => p.score)),
        };
      }),
      (document) => document.score,
    );
  }, [references]);

  return responseGroupedByDocument;
}
