"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { Separator } from "./ui/separator";

type JsonResponse = {
  answer: string;
  references: {
    metadata: {
      page_id: string;
      page_path: string;
      relative_path: string;
      title: string;
    };
    page_content: string;
  }[];
};

const getLinkFromMetadata = (
  metadata: JsonResponse["references"][0]["metadata"],
) => {
  const { page_path, relative_path } = metadata;
  return `https://bpc-ai.atlassian.net/wiki${page_path}${
    relative_path ? "#" : ""
  }${relative_path}`;
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
          <div key={result.page_content} className="flex flex-col">
            <Separator className="my-2" />
            <div className="my-2 flex flex-row items-center space-x-2">
              <span className="font-bold">
                Page title: {result.metadata.title}
              </span>
              <div>
                <Button>
                  <Link
                    href={getLinkFromMetadata(result.metadata)}
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
