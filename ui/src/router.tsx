import { createBrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import ErrorPage from "./pages/ErrorPage";
import AtlassianConnect from "./pages/AtlassianConnect";

export enum Routes {
  "AtlassianConnect" = "/connect/atlassian",
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    errorElement: <ErrorPage />,
    children: [],
  },
  {
    path: Routes.AtlassianConnect,
    element: <AtlassianConnect />,
  },
]);

export default router;
