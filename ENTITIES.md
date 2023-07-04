# Document

Can be a pdf file, a confluence page, a JIRA ticket, a web page, an email...
Each document is split into passages.
A passage is a small (less than 500 characters) chunk of logical content.
A document generates passages with its content, and one passage for its title.

# Milvus schema (for passages)

**embedding**
meaning: vector of the text content of the passage
type: vector

**title**
meaning: title is generated from the document name and the section under which the passage exists, if it applies.
type: varchar

**indexed_at**
meaning: date of the last indexing of the passage
type: date

**created_at**
meaning: date of the creation of the document
type: date

**creator**
meaning: author
type: varchar

**link**
meaning: link to the passage. As close as possible to the document. For a pdf -> can't.
type: varchar

**reference**
meaning: exact spec to retrieve the passage.
type: json

**filetype**
meaning: type of the document
type: char

# Search

**query -> vector -> passages -> return links to passages -> (do not do it: fetch text content) -> provide to llm -> return generated answer**
OR
query -> vector -> passages -> return text passage -> provide to llm -> return generated answer

# Access control

No fetching of the underlying data = no access control problem.
=> "C-level product"

# Postgres schema

Connection

# Connection types to create

**Google Drive**
**One Drive**
**X Drive**
**Sharepoint**
**Dropbox**

...
**Local files**
N local files uploaded.
