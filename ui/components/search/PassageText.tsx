"use client";

import { useState } from "react";

import { Icons } from "../icons";
import { Button } from "../ui/button";
import useRetrievePassageText from "./hooks/useRetrievePassageText";
import { Passage } from "./types";

type PassageProps = {
  passage: Passage;
};

export default function PassageText({ passage }: PassageProps) {
  const [didFetchText, setDidFetchText] = useState(false);
  const { fetchText, text } = useRetrievePassageText(passage.metadata);
  const textDisplayed = text || "Loading...";

  return (
    <div className="mt-1 flex flex-col">
      <div className="grid auto-cols-max grid-flow-col items-center gap-3">
        <div className="flex flex-row items-center">
          <Icons.flame width={16} />
          <span>{`${(passage.score * 100).toFixed(1)}%`}</span>
        </div>
        <Button
          onClick={() => {
            fetchText();
            setDidFetchText(true);
          }}
          className="bg-primary text-primary-foreground hover:bg-primary/90 h-6 px-2"
          disabled={didFetchText}
        >
          <Icons.downloadCloud />
        </Button>
      </div>
      {didFetchText && <span className="my-1">{textDisplayed}</span>}
    </div>
  );
}
