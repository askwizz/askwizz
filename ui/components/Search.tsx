"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import useWebSocket from "react-use-websocket";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { Separator } from "./ui/separator";

type Reference = {
  metadata: {
    id: string;
    source: string;
    title: string;
  };
  page_content: string;
};

type Message =
  | {
      type: "answer";
      answer: string;
    }
  | {
      type: "documents";
      documents: string[];
    };

export default function Search() {
  const [search, setSearch] = useState("What is a bad bank ?");
  const [references, setReferences] = useState<Reference[]>([]);
  const [answer, setAnswer] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const { sendMessage, lastMessage } = useWebSocket(
    "ws://localhost:8000/api/search",
  );

  useEffect(() => {
    if (lastMessage !== null) {
      setLoading(false);
      const parsedMessage: Message = JSON.parse(lastMessage.data);
      if (parsedMessage.type === "answer") {
        setAnswer((oldAnswer) => oldAnswer.concat(parsedMessage.answer));
      } else {
        setReferences((oldReferences) =>
          oldReferences.concat(
            parsedMessage.documents.map((d) => JSON.parse(d)),
          ),
        );
      }
    }
  }, [lastMessage]);

  useEffect(() => {
    const keyboardHandler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        handleClickOnSearch();
      }
    };
    document.addEventListener("keydown", keyboardHandler);
    return () => document.removeEventListener("keydown", keyboardHandler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleClickOnSearch = () => {
    const data = {
      query: search,
      connection_name: "newconnection",
      generate_answer: true,
    };

    setReferences([]);
    setAnswer("");
    setLoading(true);
    sendMessage(JSON.stringify(data));
  };

  return (
    <div className="flex w-full flex-col items-center">
      <div className="flex w-full max-w-2xl space-x-2">
        <Input
          className=""
          type="search"
          placeholder="What is my company's policy..."
          maxLength={1000}
          onChange={(e) => setSearch(e.target.value)}
          value={search}
        />
        <Button type="submit" onClick={handleClickOnSearch}>
          Search
        </Button>
      </div>
      <div className="mt-8 flex h-32 w-full flex-col">
        {loading && <span>Loading...</span>}
        {references.length > 0 && (
          <>
            <span className="font-bold">Answer</span>
            <span>{answer && answer}...</span>
          </>
        )}
        {references?.map((result) => (
          <div key={result.page_content} className="flex flex-col">
            <Separator className="my-2" />
            <div className="my-2 flex flex-row items-center space-x-2">
              <span className="font-bold">
                Page title: {result.metadata.title}
              </span>
              <div>
                <Button>
                  <Link
                    href={result.metadata.source}
                    rel="noopener"
                    target="_blank"
                  >
                    link
                  </Link>
                </Button>
              </div>
            </div>
            <span>{result.page_content}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
