"use client";

import Link from "next/link";
import { Tooltip } from "@radix-ui/react-tooltip";

import { formatDate } from "@/lib/dates";
import { SourceProperties } from "@/app/new-connection/constants";

import { Icons } from "../icons";
import { Separator } from "../ui/separator";
import { TooltipContent, TooltipProvider, TooltipTrigger } from "../ui/tooltip";
import PassageText from "./PassageText";
import { Document, DocumentType, Passage } from "./types";

type DocumentResultProps = {
  document: Document;
};

export const getDocumentTitle = (passage: Passage) => {
  if (passage.metadata.filetype === DocumentType.CONFLUENCE) {
    const confluence = passage.metadata.reference.confluence;
    return (
      <span>
        <span className="mr-2 font-bold">{confluence?.space_name}</span>
        <span className="italic">{confluence?.page_title}</span>
      </span>
    );
  }
};

export const getPassageTitle = (passage: Passage) => {
  if (passage.metadata.filetype === DocumentType.CONFLUENCE) {
    const confluence = passage.metadata.reference.confluence;
    return (
      <span className="text-sm font-bold">
        {confluence?.section || "Introduction"}
      </span>
    );
  }
};

export const getDocumentIcon = (document: Document) => {
  const documentType =
    document.passages[0].passagesWithSameLink[0].metadata.filetype;
  return SourceProperties[documentType].icon;
};

export default function DocumentResult({ document }: DocumentResultProps) {
  const firstPassage = document.passages[0].passagesWithSameLink[0];
  const documentTitle = getDocumentTitle(firstPassage);
  const documentLink = firstPassage.metadata.document_link;
  return (
    <div className="mb-2 block">
      <Link href={document.document_link} rel="noopener" target="_blank">
        <div className="flex items-center">
          {getDocumentIcon(document)}
          <div className="ml-2 flex flex-col">
            <span>{documentTitle}</span>
            <span className="mb-1 text-xs underline">{documentLink}</span>
            <div className="grid auto-cols-max grid-flow-col items-center gap-2 text-xs">
              <TooltipProvider delayDuration={200} skipDelayDuration={0}>
                <Tooltip>
                  <TooltipTrigger>
                    <div className="grid auto-cols-max grid-flow-col items-center gap-2">
                      <Icons.calendarPlus width={16} />
                      {formatDate(firstPassage.metadata.created_at)}
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <span>Date of creation of the document</span>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <Separator className="w-1" color="red" orientation="vertical" />
              <TooltipProvider delayDuration={200} skipDelayDuration={0}>
                <Tooltip>
                  <TooltipTrigger>
                    <div className="grid auto-cols-max grid-flow-col items-center gap-2">
                      <Icons.contact width={16} />
                      {firstPassage.metadata.creator}
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <span>Creator</span>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <Separator className="w-1" color="red" orientation="vertical" />
              <TooltipProvider delayDuration={200} skipDelayDuration={0}>
                <Tooltip>
                  <TooltipTrigger>
                    <div className="grid auto-cols-max grid-flow-col items-center gap-2">
                      <Icons.fileClock width={16} />
                      {formatDate(firstPassage.metadata.last_update)}
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <span>Last document update</span>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <Separator className="w-1" color="red" orientation="vertical" />
              <TooltipProvider delayDuration={200} skipDelayDuration={0}>
                <Tooltip>
                  <TooltipTrigger>
                    <div className="grid auto-cols-max grid-flow-col items-center gap-2">
                      <Icons.calendarSearch width={16} />
                      {formatDate(firstPassage.metadata.indexed_at)}
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <span>Date of document indexing</span>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </div>
        </div>
      </Link>
      <div className="ml-6 mt-2">
        <table>
          <tbody>
            {document.passages.map((sectionPassages) => {
              const firstSectionPassage =
                sectionPassages.passagesWithSameLink[0];
              return (
                <tr key={sectionPassages.sectionLink}>
                  <td className="px-2">
                    <Link
                      href={sectionPassages.sectionLink}
                      rel="noopener"
                      target="_blank"
                    >
                      <div className="flex flex-row items-center justify-between">
                        <span>{getPassageTitle(firstSectionPassage)}</span>
                        <div className="flex flex-row items-center">
                          <Icons.quote width={16} />
                          <span className="mt-2 text-sm">
                            {sectionPassages.passagesWithSameLink.length}
                          </span>
                        </div>
                      </div>
                    </Link>
                    <div className="ml-4 text-xs">
                      {sectionPassages.passagesWithSameLink.map((passage) => {
                        return (
                          <PassageText
                            key={passage.passage_id}
                            passage={passage}
                          />
                        );
                      })}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
