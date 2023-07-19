"use client";

import { useEffect, useState } from "react";

import useGetAuthToken from "@/hooks/useGetAuthToken";

import { Icons } from "../icons";
import { Passage } from "./types";

type PassageProps = {
  passage: Passage;
  setPassageText: (text: string, textHash: string) => void;
};

export default function PassageText({ passage, setPassageText }: PassageProps) {
  const token = useGetAuthToken();
  const [text, setText] = useState(
    passage.text || "Error: original text not found / fetched",
  );
  const getPassageText = () => {
    const fetchPassageText = async () => {
      const headers = new Headers();
      headers.append("Content-Type", "application/json;charset=utf-8");
      headers.append("Authorization", `Bearer ${token}`);
      return await fetch("/api/passage/text", {
        method: "POST",
        headers,
        body: JSON.stringify({
          connection_id: passage.metadata.connection_id,
          config: {
            confluence: {
              passage_hash: passage.metadata.reference.text_hash,
              page_path: passage.metadata.reference.confluence?.page_path,
            },
          },
        }),
      });
    };
    fetchPassageText().then(async (response) => {
      const responseText = (await response.json()) as string;
      setText(responseText);
      setPassageText(responseText, passage.metadata.reference.text_hash);
    });
  };

  useEffect(() => {
    getPassageText();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="mt-1 flex flex-col">
      <div className="grid auto-cols-max grid-flow-col items-center gap-3">
        <div className="flex flex-row items-center">
          <Icons.flame width={16} />
          <span>{`${(passage.score * 100).toFixed(1)}%`}</span>
        </div>
      </div>
      <span className="my-1">{text}</span>
    </div>
  );
}
