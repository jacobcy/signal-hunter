# link-handler - Smart Link Opener

Automatically detects and handles different types of URLs, with special support for X/Twitter links.

## Commands

### `openclaw link-handler <URL>`

Fetches and displays the content of a given URL.

- For **X/Twitter** links (`x.com`, `twitter.com`), it uses the `bird` skill to fetch the tweet content.
- For other **web pages**, it uses `web_fetch` to extract readable content.
- For **local files**, it uses the `read` tool.

## Examples

```bash
# Handle an X/Twitter link
openclaw link-handler https://x.com/cellinlab/status/2017887388941345122

# Handle a regular web page
openclaw link-handler https://example.com/article
```