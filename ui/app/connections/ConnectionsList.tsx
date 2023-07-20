"use client";

import ConnectionCard from "./ConnectionCard";
import { Connection } from "./types";
import { useQuery } from "@tanstack/react-query";
import { useGetToken } from "@/components/contexts/TokenContext";

const fetchConnections = async (token: string) => {
  const headers = new Headers();
  headers.append("Content-Type", "application/json;charset=utf-8");
  headers.append("Authorization", `Bearer ${token}`);
  const response = await fetch("/api/connections", {
    method: "GET",
    headers,
  });
  return response.json();
};

export default function ConnectionsList() {
  const token = useGetToken();

  const { data: connections, isLoading } = useQuery<Connection[]>({
    queryKey: ["connections"],
    queryFn: () => fetchConnections(token),
    staleTime: 1000 * 60,
  });

  if (isLoading || !connections) {
    return null;
  }

  return (
    <div className="space-y-4">
      {connections.map((connection) => {
        return <ConnectionCard connection={connection} key={connection.id_} />;
      })}
    </div>
  );
}
