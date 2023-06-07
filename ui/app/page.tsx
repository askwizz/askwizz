import Search from "@/components/Search";

export default function IndexPage() {
  return (
    <section className="container flex flex-col gap-6 pb-8 pt-6">
      <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
        AskWizz: Connect your knowledge
      </h1>
      <div className="flex flex-row items-center justify-center">
        <Search />
      </div>
    </section>
  );
}
