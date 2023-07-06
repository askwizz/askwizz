"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { PassageMetadata } from "./Search";

type PassageLinkProps = {
  passage: PassageMetadata;
};

export default function PassageLink({ passage }: PassageLinkProps) {
  return (
    <TooltipProvider delayDuration={200} skipDelayDuration={0}>
      <Tooltip>
        <TooltipTrigger>
          <Button>
            <Link href={passage.link} rel="noopener" target="_blank">
              link
            </Link>
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          <p>Content</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
