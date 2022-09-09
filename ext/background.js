const HOST = "localhost";
const PORT = 8080;

chrome.omnibox.onInputEntered.addListener((url) => {
  // Open url
  chrome.tabs.create({ url });
});

chrome.omnibox.onInputChanged.addListener((text, suggest) => {
  if (!text) return;

  const url = `http://${HOST}:${PORT}/search?q=${text}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const suggestedBangs = data.map((result) => {
        return {
          content: result.url,
          description: `<url>${result.source}</url> ${result.title}`,
        };
      });
      suggest(suggestedBangs);
    })
    .catch((error) => {
      console.log(error);
    });
});
