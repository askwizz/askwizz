import React from "react";

import AtlassianForm from "./AtlassianForm";

export default function Page() {
  return (
    <section className="container flex flex-col gap-6 pb-8 pt-6">
      <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
        Create a new connection
      </h1>
      <AtlassianForm />
    </section>
  );
}
