import { useEffect, useMemo, useState } from "react";

import useGetAuthToken from "@/hooks/useGetAuthToken";

import { Passage } from "../types";

export enum SendMessageType {
  AUTH = "AUTH",
  QUERY = "QUERY",
}

enum ReceiveMessageType {
  CLEAR = "CLEAR",
  ANSWER = "ANSWER",
}

export const getSendMessage = (messageType: SendMessageType, message: string) =>
  JSON.stringify({
    kind: messageType,
    message,
  });

const parseMessage = (message: string) =>
  JSON.parse(message) as { kind: ReceiveMessageType; message: string };

export default function useProvideAnswer(
  setAnswer: React.Dispatch<React.SetStateAction<string>>,
  references: Passage[] | undefined,
  search: string,
) {
  const token = useGetAuthToken();
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!token) return;
    // Next does not support websocket protocol rewrites atm https://github.com/vercel/next.js/discussions/38057
    const newWs = new WebSocket(
      `ws://${process.env.API_HOST ?? "api"}:8000/api/answer/ws`,
    );
    newWs.onopen = () => {
      if (!token) return;
      newWs.send(getSendMessage(SendMessageType.AUTH, token));
    };
    newWs.onmessage = function (event) {
      const message = parseMessage(event.data);
      setAnswer((oldAnswer) => oldAnswer.concat(message.message));
    };
    setWs(newWs);
  }, [setAnswer, token]);

  const canAskForAnswer = useMemo(
    () => (references ? references?.every((ref) => ref.text) : false),
    [references],
  );

  useEffect(() => {
    if (!canAskForAnswer || !ws) return;
    const message = JSON.stringify({
      query: search,
      texts: references?.map((reference) => reference.text),
    });
    ws.send(getSendMessage(SendMessageType.QUERY, message));
  }, [canAskForAnswer, ws, search, references]);

  return ws;
}
