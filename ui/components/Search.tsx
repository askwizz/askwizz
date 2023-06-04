import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Search() {
  return (
    <div className="flex w-full max-w-2xl items-center space-x-2">
      <Input
        className=""
        type="search"
        placeholder="What is my company's policy..."
        maxLength={1000}
      />
      <Button type="submit">Search</Button>
    </div>
  );
}
