import { Box, Typography } from "@mui/material";
import { Routes } from "../router";
import { Link } from "react-router-dom";
import Search from "./Search";

export default function Home() {
  return (
    <>
      <Typography fontFamily={"Roboto"} fontWeight={500} variant="h4">
        Connect your knowledge
      </Typography>
      <Box
        style={{
          borderStyle: "solid",
          borderColor: "black",
        }}
      >
        <Link to={Routes.AtlassianConnect}>Atlassian(Jira, Confluence)</Link>
      </Box>
      <Search />
    </>
  );
}
