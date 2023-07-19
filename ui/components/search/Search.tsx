"use client";

import { useCallback, useState } from "react";

import useGetAuthToken from "@/hooks/useGetAuthToken";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { Separator } from "../ui/separator";
import DocumentResult from "./DocumentResult";
import useGroupResponseByDocument from "./hooks/useGroupResponseByDocument";
import useKeyboardShortcut from "./hooks/useKeyboardShortcut";
import useProvideAnswer from "./hooks/useProvideAnswer";
import { JsonResponse } from "./types";
import Loader from "../loader/Loader";

export default function Search() {
  const [search, setSearch] = useState("What is a bad bank ?");
  const [textInput, setTextInput] = useState("What is a bad bank ?");
  const [response, setResponse] = useState<JsonResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const token = useGetAuthToken();

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

  const handleClickOnSearch = useCallback(() => {
    setSearch(textInput);
    const payloadData = { query: textInput };
    const fetchSearchResults = async () => {
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
  }, [token, textInput]);

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
        {loading && (
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
