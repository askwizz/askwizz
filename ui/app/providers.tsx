"use client";

import { TokenContext } from "@/components/contexts/TokenContext";
import { ThemeProvider } from "@/components/theme-provider";
import useGetAuthToken from "@/hooks/useGetAuthToken";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { persistQueryClient } from "@tanstack/react-query-persist-client";

import React, { useEffect, useState } from "react";

export default function Providers({ children }: React.PropsWithChildren<{}>) {
  const [queryClient] = useState(() => new QueryClient());
  const [isPersisted, setIsPersisted] = useState(false);
  const token = useGetAuthToken();

  useEffect(() => {
    if (isPersisted) return;
    const localStoragePersister = createSyncStoragePersister({
      storage: window.localStorage,
    });
    persistQueryClient({
      queryClient,
      persister: localStoragePersister,
    });
    setIsPersisted(true);
  }, [isPersisted, queryClient]);

  if (!token) {
    return null;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryDevtools initialIsOpen={false} />
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        <TokenContext.Provider value={token}>{children}</TokenContext.Provider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
