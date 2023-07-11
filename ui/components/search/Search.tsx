"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { groupBy, sortBy } from "lodash";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { Separator } from "../ui/separator";
import DocumentResult from "./DocumentResult";
import { JsonResponse } from "./types";

export default function Search() {
  const [search, setSearch] = useState("");
  const [response, setResponse] = useState<JsonResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const { getToken } = useAuth();

  const payloadData = useMemo(
    () => ({
      query: search,
      generate_answer: false,
    }),
    [search],
  );

  const handleClickOnSearch = useCallback(() => {
    const fetchSearchResults = async () => {
      const token = await getToken();
      const headers = new Headers();
      headers.append("Content-Type", "application/json;charset=utf-8");
      headers.append("Authorization", `Bearer ${token}`);
      return await fetch("/api/search", {
        method: "POST",
        headers,
        body: JSON.stringify(payloadData),
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
  }, [getToken, payloadData]);

  useEffect(() => {
    const keyboardHandler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        handleClickOnSearch();
      }
    };
    document.addEventListener("keydown", keyboardHandler);
    return () => document.removeEventListener("keydown", keyboardHandler);
  }, [handleClickOnSearch]);

  const responseGroupedByDocument = useMemo(() => {
    return sortBy(
      Object.entries(
        groupBy(
          response?.references,
          (reference) => reference.metadata.document_link,
        ),
      ).map(([document_link, references]) => {
        const sectionPassages = sortBy(
          Object.entries(
            groupBy(references, (reference) => reference.metadata.link),
          ).map(([sectionLink, passagesWithSameLink]) => ({
            sectionLink,
            passagesWithSameLink: sortBy(
              passagesWithSameLink,
              (passage) => -passage.score,
            ),
            score: Math.min(...passagesWithSameLink.map((p) => -p.score)),
          })),
          (section) => section.score,
        );
        return {
          passages: sectionPassages,
          document_link,
          score: Math.min(...sectionPassages.map((p) => p.score)),
        };
      }),
      (document) => document.score,
    );
  }, [response?.references]);

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
        {responseGroupedByDocument.map((document) => (
          <div key={document.document_link} className="flex flex-col">
            <Separator className="my-2" />
            <DocumentResult document={document} />
          </div>
        ))}
      </div>
    </div>
  );
}
