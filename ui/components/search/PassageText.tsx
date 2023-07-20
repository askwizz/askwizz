"use client";

import { useEffect, useState } from "react";

import { useQuery } from "@tanstack/react-query";

import { Icons } from "../icons";
import { Passage } from "./types";
import Loader from "../loader/Loader";
import { useGetToken } from "../contexts/TokenContext";

type PassageProps = {
  passage: Passage;
  setPassageText: (text: string, textHash: string) => void;
};

const fetchPassageText = async (token: string, body: string) => {
  const headers = new Headers();
  headers.append("Content-Type", "application/json;charset=utf-8");
  headers.append("Authorization", `Bearer ${token}`);
  const data = await fetch("/api/passage/text", {
    method: "POST",
    headers,
    body,
  });
  return data.json();
};

export default function PassageText({ passage, setPassageText }: PassageProps) {
  const token = useGetToken();
  const [text, setText] = useState(passage.text);
  const passageMetadata = passage.metadata;
  const passageHash = passageMetadata.reference.text_hash;
  const body = JSON.stringify({
    connection_id: passage.metadata.connection_id,
    config: {
      passage_hash: passage.metadata.reference.text_hash,
      confluence: {
        page_path: passage.metadata.reference.confluence?.page_path,
      },
    },
  });

  const { data: responseText } = useQuery({
    queryKey: ["passages", passageHash],
    queryFn: () => fetchPassageText(token, body),
    staleTime: Infinity,
    cacheTime: Infinity,
  });

  useEffect(() => {
    if (!responseText || passage.text) return;
    setText(responseText);
    setPassageText(responseText, passage.metadata.reference.text_hash);
  }, [responseText, passage, setPassageText]);

  return (
    <div className="mt-1 flex flex-col">
      <div className="grid auto-cols-max grid-flow-col items-center gap-3">
        <div className="flex flex-row items-center">
          <Icons.flame width={16} />
          <span>{`${(passage.score * 100).toFixed(1)}%`}</span>
        </div>
      </div>
      {text ? (
        <span className="my-1">{text}</span>
      ) : (
        <span className="my-1">
          <Loader />
        </span>
      )}
    </div>
  );
}
