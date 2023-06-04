import React from "react";
import Link from "next/link";

import { buttonVariants } from "@/components/ui/button";
import { Icons } from "@/components/icons";

export default function NewConnectionButton() {
  return (
    <div className={`${buttonVariants({ size: "lg" })} gap-2`}>
      <Icons.plusSquare className="h-6 w-6" />
      <Link href={"/new-connection"}>New connection</Link>
    </div>
  );
}
