import Search from "@/components/search/Search";

export default function IndexPage() {
  return (
    <section className="container flex flex-col gap-6 pb-8 pt-6">
      <div className="flex flex-row items-center justify-center">
        <Search />
      </div>
    </section>
  );
}
