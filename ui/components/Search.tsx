"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type JsonResponse = {
  answer: string;
  references: {
    metadata: {
      id: string;
      source: string;
      title: string;
    };
    page_content: string;
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
      connection_name: "newconnection",
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
        />
        <Button type="submit" onClick={handleClickOnSearch}>
          Search
        </Button>
      </div>
      <div className="flex h-32 w-full flex-col space-x-2 ">
        {loading && <span>Loading...</span>}
        {response?.references?.map((result) => (
          <div key={result.page_content} className="flex flex-col">
            <span className="font-bold">
              Page title: {result.metadata.title}
            </span>
            <span>{result.page_content}</span>
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
        ))}
      </div>
    </div>
  );
}
