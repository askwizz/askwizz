"use client";

import { use, useEffect } from "react";
import { useAuth, useUser } from "@clerk/nextjs";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const formSchema = z.object({
  name: z.string().min(2, "Too short").max(50, "Too long"),
  email: z.string().email("Invalid email address"),
  token: z.string(),
});

type FormSchema = z.infer<typeof formSchema>;
type FormSchemaWithToken = FormSchema & { userToken: string };

export default function AtlassianForm() {
  const { isLoaded, userId, sessionId, getToken } = useAuth();

  const form = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      token: "",
      name: "",
    },
  });

  useEffect(() => {
    if (process.env.NEXT_PUBLIC_DEBUG === "true") {
      form.setValue("email", "maximeduvalsy@gmail.com");
      form.setValue("token", "test");
      form.setValue("name", "My connection");
    }
  }, []);

  function onSubmit(values: FormSchema) {
    const submitForm = async () => {
      const token = await getToken();
      console.log({ token });
      if (!token) return;
      const headers = new Headers();
      headers.append("Content-Type", "application/json;charset=utf-8");
      headers.append("Authorization", `Bearer ${token}`);
      const body = JSON.stringify(values);
      console.log({ values });
      return fetch("/api/new-connection", { headers, method: "POST", body });
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
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Atlassian email</FormLabel>
              <FormControl>
                <Input placeholder="john.smith@gmail.com" {...field} />
              </FormControl>
              <FormDescription>This is your Atlassian email</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="token"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Atlassian token</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>This is an Atlassian token</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
