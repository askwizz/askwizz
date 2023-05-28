import { CssBaseline, ThemeProvider } from "@mui/material";
import theme from "./theme";

import { RouterProvider } from "react-router-dom";
import router from "./router";

function App() {
  return (
    <>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </>
  );
}

export default App;
