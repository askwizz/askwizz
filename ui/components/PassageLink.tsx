"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { PassageMetadata } from "./Search";

type PassageLinkProps = {
  passage: PassageMetadata;
};

export default function PassageLink({ passage }: PassageLinkProps) {
  const { getToken } = useAuth();
  const [text, setText] = useState("");
  const displayedText = text || "Loading...";

  const fetchText = () => {
    const data = {
      connection_id: passage.connection_id,
      config: {
        confluence: {
          passage_hash: passage.reference.text_hash,
          page_path: passage.reference.confluence?.page_path ?? "",
        },
      },
    };

    const fetchPassageText = async () => {
      const token = await getToken();
      const headers = new Headers();
      headers.append("Content-Type", "application/json;charset=utf-8");
      headers.append("Authorization", `Bearer ${token}`);
      return await fetch("/api/passage/text", {
        method: "POST",
        headers,
        body: JSON.stringify(data),
      });
    };

    fetchPassageText()
      .then((fetchedText) => fetchedText.text())
      .then((fetchedText) => {
        setText(fetchedText);
      });
  };

  return (
    <TooltipProvider delayDuration={200} skipDelayDuration={0}>
      <Tooltip>
        <TooltipTrigger>
          <Button
            onMouseEnter={() => {
              fetchText();
            }}
          >
            <Link href={passage.link} rel="noopener" target="_blank">
              link
            </Link>
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          <p className="w-100 max-w-xl">{displayedText}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
