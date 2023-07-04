"use client";

import { UseFormReturn } from "react-hook-form";

import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

import { FormSchema } from "./ConnectionForm";

type ConfluenceFormProps = {
  form: UseFormReturn<FormSchema>;
};

export default function ConfluenceForm({ form }: ConfluenceFormProps) {
  return (
    <>
      <FormField
        control={form.control}
        name="configuration.atlassian.atlassian_domain"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Atlassian domain</FormLabel>
            <FormControl>
              <Input placeholder="bpc-ai.atlassian.net" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="configuration.atlassian.atlassian_email"
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
        name="configuration.atlassian.atlassian_token"
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
    </>
  );
}
