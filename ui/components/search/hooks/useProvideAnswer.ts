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
  ANSWER_STOP = "ANSWER_STOP",
}

export const getSendMessage = (messageType: SendMessageType, message: string) =>
  JSON.stringify({
    kind: messageType,
    message,
  });

const parseMessage = (message: string) =>
  JSON.parse(message) as { kind: ReceiveMessageType; message: string };

export default function useProvideAnswer(
  references: Passage[] | undefined,
  search: string,
) {
  const [answer, setAnswer] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const token = useGetAuthToken();
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!token) return;
    // Next does not support websocket protocol rewrites atm https://github.com/vercel/next.js/discussions/38057
    const newWs = new WebSocket(
      `ws://${process.env.NEXT_PUBLIC_API_HOST ?? "api"}:8000/api/answer/ws`,
    );
    newWs.onopen = () => {
      if (!token) return;
      newWs.send(getSendMessage(SendMessageType.AUTH, token));
    };
    newWs.onmessage = function (event) {
      const message = parseMessage(event.data);
      if (message.kind === ReceiveMessageType.ANSWER) {
        setLoading(false);
        setAnswer((oldAnswer) => oldAnswer.concat(message.message));
        return;
      }
    };
    setWs(newWs);
  }, [setAnswer, token]);

  const canAskForAnswer = useMemo(
    () => (references ? references?.every((ref) => ref.text) : false),
    [references],
  );

  useEffect(() => {
    if (!canAskForAnswer || !ws) {
      setLoading(false);
      return;
    }
    const message = JSON.stringify({
      query: search,
      texts: references?.map((reference) => reference.text),
    });
    ws.send(getSendMessage(SendMessageType.QUERY, message));
    setLoading(true);
  }, [canAskForAnswer, ws, search, references]);

  return { answer, loading };
}
