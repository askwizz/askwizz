"use client";

import { useAuth } from "@clerk/nextjs";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Connection } from "./types";

export default function ConnectionCard({
  connection,
  fetchConnections,
}: {
  connection: Connection;
  fetchConnections: () => void;
}) {
  const { getToken } = useAuth();
  const { name, created_at: createdAt, status } = connection;
  const localDate = new Date(createdAt).toLocaleDateString();

  const deleteConnection = async (connectionId: string) => {
    const token = await getToken();
    const headers = new Headers();
    headers.append("Content-Type", "application/json;charset=utf-8");
    headers.append("Authorization", `Bearer ${token}`);
    return fetch(`/api/connections/${connectionId}`, {
      method: "DELETE",
      headers,
    });
  };

  const handleClickOnRemove = () => {
    deleteConnection(connection.id).finally(() => {
      fetchConnections();
    });
  };

  return (
    <Card className="flex flex-row items-center justify-between">
      <CardHeader>
        <CardTitle>{name}</CardTitle>
        <CardDescription>
          <Badge>Confluence</Badge>
        </CardDescription>
      </CardHeader>
      <div className="flex flex-row space-x-8">
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Created at</h5>
          <span>{localDate}</span>
        </div>
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Status</h5>
          <span>{status}</span>
        </div>
      </div>
      <Button onClick={handleClickOnRemove} className="mr-4">
        Remove
      </Button>
    </Card>
  );
}
