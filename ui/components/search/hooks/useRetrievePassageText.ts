"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";

import { PassageMetadata } from "../types";

export default function useRetrievePassageText(
  passageMetadata: PassageMetadata,
) {
  const [text, setText] = useState("");
  const { getToken } = useAuth();

  const fetchText = () => {
    const data = {
      connection_id: passageMetadata.connection_id,
      config: {
        confluence: {
          passage_hash: passageMetadata.reference.text_hash,
          page_path: passageMetadata.reference.confluence?.page_path ?? "",
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

  return { fetchText, text };
}
