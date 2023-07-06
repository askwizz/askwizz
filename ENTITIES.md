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

**last_update**
meaning: date of the last update of the document
type: date

**creator**
meaning: author of the document
type: varchar

**link**
meaning: link to the passage. As close as possible to the document. For a pdf -> can't.
type: varchar

**document_link**
meaning: link to the document
type: varchar

**reference**
meaning: exact spec to retrieve the passage.
type: json

**filetype**
meaning: type of the document
type: char

**connection_id**
meaning: id of the postgres connection
type: char

**indexor**
meaning: person who indexed the document
type: char

Each user has a collection.
Each source a user sets creates a partition
If the source has already been set, drop the partition.
How to know if the source has already been set ? From the passages of the source, compute a hash. Use it in the name of the partition.
Name of the partition = source-hash.

# Search

**query -> vector -> passages -> return links to passages -> (do not do it: fetch text content) -> (provide to llm) -> return generated answer**
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
