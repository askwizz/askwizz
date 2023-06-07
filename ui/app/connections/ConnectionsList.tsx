"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";

import ConnectionCard from "./ConnectionCard";
import { Connection } from "./types";

export default function ConnectionsList() {
  const { getToken } = useAuth();
  const [connections, setConnections] = useState<Connection[]>([]);

  const fetchConnections = async () => {
    const token = await getToken();
    const headers = new Headers();
    headers.append("Content-Type", "application/json;charset=utf-8");
    headers.append("Authorization", `Bearer ${token}`);
    const response = await fetch("/api/connections", {
      method: "GET",
      headers,
    });
    const parsedResponse = await response.json();
    setConnections(parsedResponse);
  };

  useEffect(() => {
    fetchConnections();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-4">
      {connections.map((connection) => {
        return (
          <ConnectionCard
            fetchConnections={fetchConnections}
            connection={connection}
            key={connection.id}
          />
        );
      })}
    </div>
  );
}
