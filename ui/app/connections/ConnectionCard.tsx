"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

import { Connection } from "./types";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useGetToken } from "@/components/contexts/TokenContext";

const deleteConnection = async (token: string, connectionId: string) => {
  const headers = new Headers();
  headers.append("Content-Type", "application/json;charset=utf-8");
  headers.append("Authorization", `Bearer ${token}`);
  return fetch(`/api/connections/${connectionId}`, {
    method: "DELETE",
    headers,
  });
};

export default function ConnectionCard({
  connection,
}: {
  connection: Connection;
}) {
  const queryClient = useQueryClient();
  const token = useGetToken();

  const {
    name,
    created_at: createdAt,
    status,
    indexed_at: indexedAt,
    source,
    documents_count,
    passages_count,
  } = connection;
  const getLocalDate = (date: string) => new Date(date).toLocaleDateString();

  const mutation = useMutation({
    mutationFn: (connectionId: string) => {
      return deleteConnection(token, connectionId);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["connections"] });
    },
  });

  const handleClickOnRemove = () => {
    mutation.mutate(connection.id_);
  };

  return (
    <Card className="flex flex-row items-center justify-between">
      <CardHeader>
        <CardTitle>{name}</CardTitle>
        <CardDescription>
          <Badge>{source}</Badge>
        </CardDescription>
      </CardHeader>
      <div className="flex flex-row space-x-8">
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Created at</h5>
          <span>{getLocalDate(createdAt)}</span>
        </div>
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Indexed at</h5>
          <span>{getLocalDate(indexedAt)}</span>
        </div>
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Status</h5>
          <span>{status}</span>
        </div>
        <Separator className="h-16" orientation="vertical" />
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Documents</h5>
          <span>{documents_count}</span>
        </div>
        <div className="flex flex-col py-2">
          <h5 className="font-semibold">Passages</h5>
          <span>{passages_count}</span>
        </div>
      </div>
      <Button onClick={handleClickOnRemove} className="mr-4">
        Remove
      </Button>
    </Card>
  );
}
