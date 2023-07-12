"use client";

import { Icons } from "../icons";
import { Passage } from "./types";

type PassageProps = {
  passage: Passage;
};

export default function PassageText({ passage }: PassageProps) {
  const textDisplayed = passage.text || "Error: original text not found";

  return (
    <div className="mt-1 flex flex-col">
      <div className="grid auto-cols-max grid-flow-col items-center gap-3">
        <div className="flex flex-row items-center">
          <Icons.flame width={16} />
          <span>{`${(passage.score * 100).toFixed(1)}%`}</span>
        </div>
      </div>
      <span className="my-1">{textDisplayed}</span>
    </div>
  );
}
