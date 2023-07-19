import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";

export default function useGetAuthToken() {
  const { getToken } = useAuth();
  const [token, setToken] = useState<string | null>(null);
  useEffect(() => {
    const getTokenValue = async () => {
      const authToken = await getToken();
      setToken(authToken);
    };
    getTokenValue();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return token;
}
