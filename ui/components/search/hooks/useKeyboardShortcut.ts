import { useEffect } from "react";

export default function useKeyboardShortcut({
  handleClickOnSearch,
}: {
  handleClickOnSearch: () => void;
}) {
  useEffect(() => {
    const keyboardHandler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        handleClickOnSearch();
      }
    };
    document.addEventListener("keydown", keyboardHandler);
    return () => document.removeEventListener("keydown", keyboardHandler);
  }, [handleClickOnSearch]);
}
