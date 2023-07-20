"use client";

import { useCallback, useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { Separator } from "../ui/separator";
import DocumentResult from "./DocumentResult";
import useGroupResponseByDocument from "./hooks/useGroupResponseByDocument";
import useKeyboardShortcut from "./hooks/useKeyboardShortcut";
import useProvideAnswer from "./hooks/useProvideAnswer";
import { JsonResponse } from "./types";
import Loader from "../loader/Loader";
import { useGetToken } from "../contexts/TokenContext";
import { useQuery } from "@tanstack/react-query";

const fetchSearchResults = async (token: string, body: string) => {
  const headers = new Headers();
  headers.append("Content-Type", "application/json;charset=utf-8");
  headers.append("Authorization", `Bearer ${token}`);
  const data = await fetch("/api/search", {
    method: "POST",
    headers,
    body,
  });
  return data.json();
};

export default function Search() {
  const [shouldSearch, setShouldSearch] = useState(false);
  const [search, setSearch] = useState("");
  const [textInput, setTextInput] = useState("What is a bad bank ?");
  const [response, setResponse] = useState<JsonResponse | null>(null);

  const token = useGetToken();

  const setPassageText = (text: string, textHash: string) => {
    setResponse((prevResponse) => {
      if (!prevResponse) return prevResponse;
      const newReferences = prevResponse.references.map((reference) => {
        if (reference.metadata.reference.text_hash === textHash) {
          return { ...reference, text };
        }
        return reference;
      });
      return { ...prevResponse, references: newReferences };
    });
  };

  const payloadData = JSON.stringify({ query: search });
  const { data: parsedResponse, isFetching } = useQuery({
    queryFn: () => fetchSearchResults(token, payloadData),
    queryKey: ["search", search],
    enabled: shouldSearch,
    staleTime: 1000 * 60 * 60,
  });

  useEffect(() => {
    setResponse(parsedResponse);
  }, [parsedResponse]);

  const handleClickOnSearch = useCallback(() => {
    setSearch(textInput);
    setShouldSearch(true);
    setResponse(null);
  }, [textInput]);

  useKeyboardShortcut({ handleClickOnSearch });

  const { answer, loading: loadingAnswer } = useProvideAnswer(
    response?.references,
    search,
  );

  const responseGroupedByDocument = useGroupResponseByDocument(
    response?.references,
  );

  return (
    <div className="flex w-full flex-col items-center">
      <div className="flex w-full max-w-2xl space-x-2">
        <Input
          className=""
          type="search"
          placeholder="What is my company's policy..."
          maxLength={1000}
          onChange={(e) => setTextInput(e.target.value)}
          value={textInput}
        />
        <Button type="submit" onClick={handleClickOnSearch}>
          Search
        </Button>
      </div>
      {loadingAnswer && (
        <div className="flex h-full w-full justify-center">
          <Loader />
        </div>
      )}
      {answer && <div className="mt-8 text-sm">{answer}</div>}
      <div className="mt-4 flex h-32 w-full flex-col">
        {isFetching && (
          <div className="flex h-full w-full justify-center">
            <Loader />
          </div>
        )}
        {responseGroupedByDocument?.map((document) => (
          <div key={document.document_link} className="flex flex-col">
            <Separator className="my-2" />
            <DocumentResult
              document={document}
              setPassageText={setPassageText}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
