"use client";

import { useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import ConfluenceForm from "./ConfluenceForm";
import { AVAILABLE_SOURCES, Source } from "./types";

const formSchema = z.object({
  name: z.string().min(2, "Too short").max(80, "Too long"),
  configuration: z.object({
    atlassian: z.object({
      atlassian_email: z.string().email("Invalid email address"),
      atlassian_token: z.string(),
      atlassian_domain: z.string(),
    }),
  }),
  source: z.enum(AVAILABLE_SOURCES),
});

export type FormSchema = z.infer<typeof formSchema>;

export default function AtlassianForm() {
  const { getToken } = useAuth();

  const form = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      configuration: {
        atlassian: {
          atlassian_token: "",
          atlassian_email: "",
          atlassian_domain: "",
        },
      },
      source: AVAILABLE_SOURCES[0],
    },
  });

  const currentSource = form.watch("source");

  useEffect(() => {
    if (process.env.NEXT_PUBLIC_DEBUG === "true") {
      form.setValue(
        "configuration.atlassian.atlassian_email",
        "maximeduvalsy@gmail.com",
      );
      form.setValue(
        "configuration.atlassian.atlassian_token",
        "ATATT3xFfGF0LIyG73Yf66DBMLqkDaGaEykYY9WS_noptQ5vQf5Ir-8UUa7_8pfBuwCRpOcg2rAACUj6OoMHXBT7nAW9cXcs0XHc0KTsOBtttm6tM3DtXCcD1EERJ9PqUoi8tlpOi6KQzEGcXQOLakzVsopcKjnyh-2k6UIFpOl-cfKgJsAfN0U=717F7F23",
      );
      form.setValue("name", "newconnection");
      form.setValue("source", "CONFLUENCE");
      form.setValue(
        "configuration.atlassian.atlassian_domain",
        "bpc-ai.atlassian.net",
      );
    }
  }, []);

  function onSubmit(values: FormSchema) {
    const submitForm = async () => {
      const token = await getToken();
      if (!token) return;
      const headers = new Headers();
      headers.append("Content-Type", "application/json;charset=utf-8");
      headers.append("Authorization", `Bearer ${token}`);
      console.log(values);
      return fetch("/api/new-connection", {
        headers,
        method: "POST",
        body: JSON.stringify(values),
      });
    };
    submitForm();
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name of the connection</FormLabel>
              <FormControl>
                <Input placeholder="" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormItem>
          <FormLabel>Connection type</FormLabel>
          <Select
            value={currentSource}
            onValueChange={(source) =>
              form.setValue("source", source as Source)
            }
            defaultValue={AVAILABLE_SOURCES[0]}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select connection type" />
            </SelectTrigger>
            <SelectContent>
              {AVAILABLE_SOURCES.map((source) => (
                <SelectItem key={source} value={source}>
                  {source.toLocaleLowerCase()}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </FormItem>

        {currentSource === "CONFLUENCE" && <ConfluenceForm form={form} />}

        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
