"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import PassageLink from "./PassageLink";
import { Separator } from "./ui/separator";

const DOCUMENT_TYPES = ["CONFLUENCE"];
type DocumentType = (typeof DOCUMENT_TYPES)[number];

export type PassageMetadata = {
  title: string;
  indexed_at: string;
  created_at: string;
  last_update: string;
  creator: string;
  link: string;
  document_link: string;
  reference: {
    confluence?: {
      domain: string;
      page_path: string;
    };
  };
  filetype: DocumentType;
  connection_id: string;
  indexor: string;
};
type JsonResponse = {
  answer: string;
  references: {
    metadata: PassageMetadata;
    score: number;
    passage_id: number;
  }[];
};

export default function Search() {
  const [search, setSearch] = useState("What is a bad bank ?");
  const [response, setResponse] = useState<JsonResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const { getToken } = useAuth();

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
      connection_name: "From_CLI",
      generate_answer: false,
    };

    const fetchSearchResults = async () => {
      const token = await getToken();
      const headers = new Headers();
      headers.append("Content-Type", "application/json;charset=utf-8");
      headers.append("Authorization", `Bearer ${token}`);
      return await fetch("/api/search", {
        method: "POST",
        headers,
        body: JSON.stringify(data),
      });
    };
    setResponse(null);
    setLoading(true);
    fetchSearchResults()
      .then(async (response) => {
        const parsedResponse = (await response.json()) as JsonResponse;
        setResponse(parsedResponse);
      })
      .finally(() => setLoading(false));
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
        {response?.references?.map((result) => (
          <div key={result.passage_id} className="flex flex-col">
            <Separator className="my-2" />
            <div className="my-2 flex flex-row items-center space-x-2">
              <span className="font-bold">
                Page title: {result.metadata.title}
              </span>
              <div>
                <PassageLink passage={result.metadata} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
