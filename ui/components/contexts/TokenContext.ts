import React, { useContext } from "react";

export const TokenContext = React.createContext<string>("");
TokenContext.displayName = "TokenContext";

export function useGetToken() {
  const token = useContext(TokenContext);
  return token;
}
