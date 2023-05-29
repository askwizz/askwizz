import {
  Box,
  Button,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import randomWords from "random-words";
import Highlighter from "react-highlight-words";

const mockSize = 1000;
const mockDatabase = Array.from({ length: mockSize }, () =>
  randomWords(5).join(" ")
);

type JsonResponse = {
  matches: {
    metadata: any;
    index: string;
    rank: number;
    reference: string;
    score: number;
  }[];
};

export default function Search() {
  const [search, setSearch] = useState<string>("What color is the sky?");
  const [results, setResults] = useState<string[]>([]);

  const mockResults = (() => {
    if (!search) {
      return [];
    }
    const filteredResults = mockDatabase.filter((entry) =>
      entry.includes(search)
    );
    return filteredResults.slice(0, 10);
  })();

  const handleSearch = () => {
    const data = { prompt: search };
    const fetchSearchResults = async () => {
      return await fetch("/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
    };
    fetchSearchResults().then(async (response) => {
      const parsedResponse = (await response.json()) as JsonResponse;
      setResults(parsedResponse.matches.map((match) => match.reference));
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
          }}
          variant="contained"
        >
          Search
        </Button>
      </Box>
      <Typography variant="h5">Results</Typography>
      <nav aria-label="search results">
        <List>
          {results.map((result) => (
            <ListItem key={result}>
              <ListItemButton>
                <ListItemText>
                  <Highlighter
                    autoEscape={true}
                    searchWords={[search]}
                    textToHighlight={result}
                  />
                </ListItemText>
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </nav>
    </Box>
  );
}
