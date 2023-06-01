import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Link,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";

type JsonResponse = {
  answer: string;
  references: {
    metadata: {
      id: string;
      source: string;
      title: string;
    };
    page_content: string;
  }[];
};

export default function Search() {
  const [search, setSearch] = useState<string>(
    "Which bank failed in the 90s ?"
  );
  const [response, setResponse] = useState<JsonResponse | null>(null);
  const [generateAnswer, setGenerateAnswer] = useState(false);

  const handleSearch = () => {
    const data = {
      query: search,
      confluence_space_key: "TW",
      generate_answer: generateAnswer,
    };
    const fetchSearchResults = async () => {
      return await fetch("/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
    };
    setResponse(null);
    fetchSearchResults().then(async (response) => {
      const parsedResponse = (await response.json()) as JsonResponse;
      setResponse(parsedResponse);
    });
  };

  return (
    <Box
      sx={{
        display: "flex",
        padding: "16px",
        flexDirection: "column",
      }}
    >
      <Box
        sx={{
          width: "100%",
          justifyContent: "center",
          display: "flex",
          alignItems: "center",
        }}
      >
        <Box
          sx={{
            width: "50%",
          }}
        >
          <TextField
            fullWidth
            id="search"
            label="Search"
            multiline
            onChange={(e) => setSearch(e.target.value)}
            type="search"
            value={search}
            variant="outlined"
          />
        </Box>
        <Button
          onClick={handleSearch}
          sx={{
            marginLeft: "16px",
            marginRight: "16px",
          }}
          variant="contained"
        >
          Search
        </Button>
        <FormGroup>
          <FormControlLabel
            control={
              <Checkbox
                checked={generateAnswer}
                onChange={(e) => {
                  setGenerateAnswer(e.target.checked);
                }}
              />
            }
            label="LLM answer"
          />
        </FormGroup>
      </Box>
      <Typography variant="h5">Results</Typography>
      <nav aria-label="search results">
        <List>
          <Typography>{response?.answer}</Typography>
          {response?.references?.map((result) => (
            <ListItem key={result.page_content}>
              <ListItemButton>
                <ListItemText>
                  <Box fontWeight={"bold"}>
                    Page title: {result.metadata.title}
                  </Box>
                  <Box>{result.page_content}</Box>
                  <Box>
                    <Link
                      href={result.metadata.source}
                      rel="noopener"
                      target="_blank"
                    >
                      link
                    </Link>
                  </Box>
                </ListItemText>
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </nav>
    </Box>
  );
}
